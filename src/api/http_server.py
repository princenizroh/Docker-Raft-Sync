"""
HTTP API Server for Distributed Nodes
Provides REST API for client access to cluster
"""

import asyncio
import json
import logging
from typing import Optional, Callable
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
        self.app = web.Application()
        self.app['node'] = self.node
        self.app.router.add_routes([
            web.get('/', self.handle_root),
            web.get('/status', self.handle_status),
            web.post('/status', self.handle_status)
        ])
        self.runner = None
        self.site = None

    def _create_app(self):
        """Create and configure the web application"""
        app = web.Application()
        app['node'] = self.node
        app.router.add_routes([
            web.get('/', self.handle_root),
            web.get('/status', self.handle_status),
            web.post('/status', self.handle_status)
        ])
        logger.info("HTTP API routes configured")
        return app

    async def handle_root(self, request):
        """Simple test endpoint with JSON response"""
        logger.debug("Handling root request")
        try:
            response = {
                'status': 'ok',
                'node_id': self.node.node_id,
                'server': 'aiohttp'
            }
            logger.debug(f"Returning root response: {response}")
            return web.json_response(response)
        except Exception as e:
            logger.error(f"Error in root handler: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def start(self):
        """Start HTTP API server"""
        try:
            logger.info(f"Starting HTTP API server on {self.host}:{self.port}")
            runner = web.AppRunner(self.app, access_log=None)
            await runner.setup()
            site = web.TCPSite(runner, self.host, self.port, reuse_address=True, reuse_port=True)
            await site.start()
            self.runner = runner
            self.site = site
            logger.info(f"HTTP API server started successfully on {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start HTTP API server: {str(e)}")
            logger.exception(e)
            raise
    
    async def _health_check(self):
        """Run periodic health checks on the HTTP server"""
        while True:
            try:
                # Sleep first to give the server time to start
                await asyncio.sleep(5)  # Increased sleep time
                
                # Simple health check - just verify components exist
                if not self.site or not self.runner:
                    logger.error("HTTP server components not initialized")
                    continue
                    
            except asyncio.CancelledError:
                logger.info("HTTP health check task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in HTTP health check: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def stop(self):
        """Stop HTTP API server"""
        logger.info("Stopping HTTP API server...")
        try:
            # Cancel health check task if running
            if hasattr(self, '_health_task'):
                logger.debug("Cancelling health check task...")
                self._health_task.cancel()
                try:
                    await self._health_task
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    logger.warning(f"Error waiting for health task to cancel: {e}")
                self._health_task = None
            
            # Stop site first
            if self.site:
                logger.debug("Stopping TCP site...")
                try:
                    await asyncio.wait_for(self.site.stop(), timeout=5.0)
                except asyncio.TimeoutError:
                    logger.warning("TCP site stop timed out")
                except Exception as e:
                    logger.error(f"Error stopping TCP site: {e}")
                self.site = None
            
            # Then clean up runner
            if self.runner:
                logger.debug("Cleaning up runner...")
                try:
                    await asyncio.wait_for(self.runner.cleanup(), timeout=5.0)
                except asyncio.TimeoutError:
                    logger.warning("Runner cleanup timed out")
                except Exception as e:
                    logger.error(f"Error cleaning up runner: {e}")
                self.runner = None
            
            # Brief pause to ensure cleanup
            await asyncio.sleep(0.1)
            
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
            status = {
                'node_id': self.node.node_id,
                'is_leader': self.node.raft.is_leader(),
                'state': self.node.raft.state.value,
                'term': self.node.raft.current_term,
                'running': True
            }
            return web.Response(
                text=json.dumps(status),
                content_type='application/json'
            )
        except Exception as e:
            logger.error(f"Error in status handler: {e}")
            return web.Response(
                text=json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )
    
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
            
            # Check if node has acquire_lock method
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
    
    # Queue Endpoints
    
    async def handle_queue_enqueue(self, request):
        """Handle queue enqueue request"""
        try:
            data = await request.json()
            queue_name = data.get('queue_name')
            message_data = data.get('data')
            
            if not queue_name or message_data is None:
                return web.json_response({
                    'success': False,
                    'error': 'Missing queue_name or data'
                }, status=400)
            
            if not hasattr(self.node, 'enqueue'):
                return web.json_response({
                    'success': False,
                    'error': 'Queue not available'
                }, status=400)
            
            success = await self.node.enqueue(queue_name, message_data)
            
            return web.json_response({
                'success': success,
                'queue_name': queue_name
            })
        
        except Exception as e:
            logger.error(f"Error in queue enqueue: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_queue_dequeue(self, request):
        """Handle queue dequeue request"""
        try:
            data = await request.json()
            queue_name = data.get('queue_name')
            consumer_id = data.get('consumer_id')
            
            if not queue_name or not consumer_id:
                return web.json_response({
                    'success': False,
                    'error': 'Missing queue_name or consumer_id'
                }, status=400)
            
            if not hasattr(self.node, 'dequeue'):
                return web.json_response({
                    'success': False,
                    'error': 'Queue not available'
                }, status=400)
            
            message = await self.node.dequeue(queue_name, consumer_id)
            
            if message:
                return web.json_response({
                    'success': True,
                    'message': message.to_dict() if hasattr(message, 'to_dict') else str(message)
                })
            else:
                return web.json_response({
                    'success': False,
                    'message': None
                })
        
        except Exception as e:
            logger.error(f"Error in queue dequeue: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_queue_status(self, request):
        """Handle queue status request"""
        try:
            if not hasattr(self.node, 'get_queue_stats'):
                return web.json_response({'error': 'Queue not available'}, status=400)
            
            status = self.node.get_queue_stats()
            return web.json_response(status)
        
        except Exception as e:
            logger.error(f"Error in queue status: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    # Cache Endpoints
    
    async def handle_cache_get(self, request):
        """Handle cache get request"""
        try:
            data = await request.json()
            key = data.get('key')
            
            if not key:
                return web.json_response({
                    'success': False,
                    'error': 'Missing key'
                }, status=400)
            
            if not hasattr(self.node, 'get'):
                return web.json_response({
                    'success': False,
                    'error': 'Cache not available'
                }, status=400)
            
            value = await self.node.get(key)
            
            return web.json_response({
                'success': value is not None,
                'key': key,
                'value': value
            })
        
        except Exception as e:
            logger.error(f"Error in cache get: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_cache_put(self, request):
        """Handle cache put request"""
        try:
            data = await request.json()
            key = data.get('key')
            value = data.get('value')
            
            if not key or value is None:
                return web.json_response({
                    'success': False,
                    'error': 'Missing key or value'
                }, status=400)
            
            if not hasattr(self.node, 'put'):
                return web.json_response({
                    'success': False,
                    'error': 'Cache not available'
                }, status=400)
            
            success = await self.node.put(key, value)
            
            return web.json_response({
                'success': success,
                'key': key
            })
        
        except Exception as e:
            logger.error(f"Error in cache put: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_cache_delete(self, request):
        """Handle cache delete request"""
        try:
            data = await request.json()
            key = data.get('key')
            
            if not key:
                return web.json_response({
                    'success': False,
                    'error': 'Missing key'
                }, status=400)
            
            if not hasattr(self.node, 'delete'):
                return web.json_response({
                    'success': False,
                    'error': 'Cache not available'
                }, status=400)
            
            success = await self.node.delete(key)
            
            return web.json_response({
                'success': success,
                'key': key
            })
        
        except Exception as e:
            logger.error(f"Error in cache delete: {e}")
            return web.json_response({'success': False, 'error': str(e)}, status=500)
    
    async def handle_cache_status(self, request):
        """Handle cache status request"""
        try:
            if not hasattr(self.node, 'get_cache_stats'):
                return web.json_response({'error': 'Cache not available'}, status=400)
            
            status = self.node.get_cache_stats()
            return web.json_response(status)
        
        except Exception as e:
            logger.error(f"Error in cache status: {e}")
            return web.json_response({'error': str(e)}, status=500)
