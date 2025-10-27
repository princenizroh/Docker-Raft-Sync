"""
HTTP API Server for Distributed Nodes
Provides REST API for client access to cluster
"""

import asyncio
import json
import logging
import time
from typing import Optional, Callable
import aiohttp
from aiohttp import web

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HTTPAPIServer:
    """
    HTTP API server for distributed node
    Allows clients to interact without being Raft nodes
    """
    
    def __init__(self, node, host: str, port: int):
        """
        Args:
            node: The distributed node (lock_manager, queue, cache, etc)
            host: API server host
            port: API server port
        """
        self.node = node
        self.host = host
        self.port = port
        self.app = self._create_app()
        self.runner = None
        self.site = None
        
        # Health check task
        self._health_task = None

    def _create_app(self):
        """Create and configure the web application"""
        app = web.Application()
        app['node'] = self.node
        
        # Base routes
        app.router.add_routes([
            web.get('/', self.handle_root),
            web.get('/status', self.handle_status),
            web.post('/status', self.handle_status),
            web.get('/cluster/health', self.handle_cluster_health),
            
            # Lock manager endpoints
            web.post('/lock/acquire', self.handle_lock_acquire),
            web.post('/lock/release', self.handle_lock_release),
            web.post('/lock/status', self.handle_lock_status)
        ])
        
        # Add CORS support
        # Add OPTIONS handler for all routes
        for route in list(app.router.routes()):
            if not any(r.method == 'OPTIONS' and r.path == route.path for r in app.router.routes()):
                app.router.add_route('OPTIONS', route.path, self.handle_options)

        # Add middleware for error handling
        app.middlewares.append(self._error_middleware)
        
        # Log available routes
        logger.info("Available HTTP API routes:")
        for route in app.router.routes():
            logger.info(f"  {route.method:<6} {route.url_for()}")
        
        return app
        
    @web.middleware
    async def _error_middleware(self, request, handler):
        """Global error handling middleware"""
        try:
            # Add CORS headers to every response
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response
            
        except web.HTTPException as e:
            # Log HTTP exceptions at info level
            logger.info(f"HTTP Exception handling {request.method} {request.path}: {e}")
            response = web.json_response({
                'error': str(e),
                'status': e.status,
                'path': request.path
            }, status=e.status)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            
        except asyncio.CancelledError:
            # Handle cancelled requests gracefully
            logger.debug(f"Request cancelled: {request.method} {request.path}")
            response = web.json_response({
                'error': 'Request cancelled',
                'status': 499,
                'path': request.path
            }, status=499)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            
        except Exception as e:
            # Log unexpected errors with traceback
            logger.error(f"Unexpected error handling {request.method} {request.path}: {e}")
            logger.exception(e)
            response = web.json_response({
                'error': 'Internal server error',
                'details': str(e),
                'path': request.path
            }, status=500)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

    async def handle_root(self, request):
        """Simple test endpoint with JSON response"""
        logger.debug("Handling root request")
        try:
            response = {
                'status': 'ok',
                'node_id': self.node.node_id,
                'server': 'aiohttp',
                'time': time.time()
            }
            logger.debug(f"Returning root response: {response}")
            return web.json_response(response)
        except AttributeError as e:
            logger.error(f"Node not properly initialized: {e}")
            return web.json_response({'error': 'Node not initialized'}, status=503)
        except Exception as e:
            logger.error(f"Error in root handler: {e}")
            logger.exception(e)
            return web.json_response({'error': 'Internal server error'}, status=500)

    async def start(self):
        """Start HTTP API server"""
        try:
            logger.info(f"Starting HTTP API server for {self.node.node_id} on {self.host}:{self.port}")
            
            # Set up the HTTP server
            logger.debug("Creating AppRunner...")
            runner = web.AppRunner(self.app)
            await runner.setup()
            self.runner = runner

            logger.debug(f"Creating TCPSite on {self.host}:{self.port}...")
            site = web.TCPSite(
                runner, 
                self.host, 
                self.port,
                reuse_address=True,  # Allow reuse of the address
                backlog=128  # Increase connection queue size
            )

            logger.debug("Starting TCPSite...")
            await site.start()
            self.site = site
            
            # Wait briefly to verify server started
            await asyncio.sleep(0.1)
            
            # Attempt a test request to verify server is listening
            async with aiohttp.ClientSession() as session:
                try:
                    await session.get(f"http://{self.host}:{self.port}/")
                except Exception as e:
                    logger.error(f"Failed to verify server is listening: {e}")
                    await site.stop()
                    await runner.cleanup()
                    return False
            
            logger.info(f"HTTP API server for {self.node.node_id} started successfully on {self.host}:{self.port}")
            return True
            
        except OSError as e:
            logger.error(f"OS Error starting HTTP API server: {e}")
            logger.exception(e)
            return False
        except Exception as e:
            logger.error(f"Error starting HTTP API server: {e}")
            logger.exception(e)
            return False

    async def handle_options(self, request):
        """Handle OPTIONS requests for CORS preflight"""
        response = web.Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response

    async def stop(self):
        """Stop HTTP API server"""
        try:
            # First stop accepting new connections
            if self.site:
                logger.info("Stopping HTTP API server site...")
                await self.site.stop()
                self.site = None

            # Then wait briefly for existing requests to complete
            await asyncio.sleep(0.5)
            
            # Finally cleanup runner and tasks
            if self.runner:
                logger.info("Cleaning up HTTP API server...")
                await self.runner.cleanup()
                self.runner = None
            
            logger.info("HTTP API server stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping HTTP API server: {e}")
            logger.exception(e)
            # Don't re-raise, as this is cleanup code
    
    # Status Endpoints
    
    async def handle_status(self, request):
        """Handle status request"""
        logger.debug("Handling status request")
        try:
            # Basic node checks
            if not self.node or not self.node.raft or not self.node.failure_detector:
                logger.error("Node, Raft, or failure detector not initialized")
                return web.json_response({
                    'error': 'Node components not fully initialized',
                    'status': 'error'
                }, status=503)

            # Collect state information
            status = {
                'status': 'ok',
                'node_id': self.node.node_id,
                'is_leader': self.node.raft.is_leader(),
                'state': self.node.raft.state.value,
                'term': self.node.raft.current_term,
                'running': True,
                'timestamp': time.time(),
                'last_contact': {
                    node_id: int(time.time() - node_status.last_heartbeat)
                    for node_id, node_status in self.node.failure_detector.node_states.items()
                    if node_id != self.node.node_id
                }
            }
            return web.json_response(status)
            
        except AttributeError as e:
            logger.error(f"Node not properly initialized: {e}")
            return web.json_response({
                'error': 'Node not fully initialized',
                'details': str(e),
                'status': 'error'
            }, status=503)
            
        except Exception as e:
            logger.error(f"Error handling status request: {e}")
            logger.exception(e)
            return web.json_response({
                'error': 'Internal server error',
                'status': 'error'
            }, status=500)
        
    async def handle_cluster_health(self, request):
        """Handle cluster health request"""
        logger.debug("Handling cluster health request")
        health = self.node.failure_detector.get_cluster_health()
        return web.json_response({
            'node_id': self.node.node_id,
            'state': self.node.raft.state.value,
            'is_leader': self.node.raft.is_leader(),
            'cluster_health': health,
            'nodes': {
                node_id: {
                    'state': status.state.value,
                    'last_heartbeat': int(time.time() - status.last_heartbeat)
                }
                for node_id, status in self.node.failure_detector.node_states.items()
            }
        })
    
    # Lock Endpoints
    
    async def handle_lock_acquire(self, request):
        """Handle lock acquire request"""
        try:
            data = await request.json()
            resource = data.get('resource')
            client_id = data.get('client_id')
            exclusive = data.get('exclusive', True)
            timeout = data.get('timeout', 10.0)
            
            if not resource or not client_id:
                return web.json_response({
                    'success': False,
                    'error': 'Missing resource or client_id'
                }, status=400)
            
            if not hasattr(self.node, 'acquire_lock'):
                return web.json_response({
                    'success': False,
                    'error': 'Lock manager not available'
                }, status=400)
            
            success = await self.node.acquire_lock(
                resource=resource,
                holder_id=client_id,
                exclusive=exclusive,
                timeout=timeout
            )
            
            return web.json_response({
                'success': success,
                'resource': resource,
                'client_id': client_id,
                'exclusive': exclusive
            })
        
        except Exception as e:
            logger.error(f"Error in lock acquire: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_lock_release(self, request):
        """Handle lock release request"""
        try:
            data = await request.json()
            resource = data.get('resource')
            client_id = data.get('client_id')
            
            if not resource or not client_id:
                return web.json_response({
                    'success': False,
                    'error': 'Missing resource or client_id'
                }, status=400)
            
            if not hasattr(self.node, 'release_lock'):
                return web.json_response({
                    'success': False,
                    'error': 'Lock manager not available'
                }, status=400)
            
            success = await self.node.release_lock(resource, client_id)
            
            return web.json_response({
                'success': success,
                'resource': resource,
                'client_id': client_id
            })
        
        except Exception as e:
            logger.error(f"Error in lock release: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_lock_status(self, request):
        """Handle lock status request"""
        try:
            if not hasattr(self.node, 'get_lock_status'):
                return web.json_response({'error': 'Lock manager not available'}, status=400)
            
            status = self.node.get_lock_status()
            return web.json_response(status)
        
        except Exception as e:
            logger.error(f"Error in lock status: {e}")
            return web.json_response({'error': str(e)}, status=500)