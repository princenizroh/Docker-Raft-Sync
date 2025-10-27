"""
Start 3-Node Cluster with HTTP API
Starts distributed lock, queue, and cache nodes
"""

import asyncio
import sys
import logging
import signal
from typing import List

# Add parent directory to path
sys.path.insert(0, '.')

from src.nodes.lock_manager import DistributedLockManager
from src.nodes.queue_node import DistributedQueue
from src.nodes.cache_node import DistributedCache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClusterManager:
    """Manage 3-node cluster"""
    
    def __init__(self, node_type: str = 'lock'):
        self.node_type = node_type
        self.nodes: List = []
        self.running = False
        
        # Define cluster configuration
        self.node_configs = [
            {
                'node_id': 'node-1',
                'host': '127.0.0.1',  # Use localhost
                'port': 5001,       # Different ports for each node
                'api_port': 6000    # API port
            },
            {
                'node_id': 'node-2', 
                'host': '127.0.0.1',
                'port': 5002,
                'api_port': 6010
            },
            {
                'node_id': 'node-3',
                'host': '127.0.0.1',
                'port': 5003,
                'api_port': 6020
            }
        ]
        
        # Internal cluster configuration
        if node_type == 'lock':
            # For Raft cluster config
            self.cluster_config = [
                f"{config['node_id']}:{config['host']}:{config['port']}"
                for config in self.node_configs
            ]
                # Configure ports
            for config in self.node_configs:
                config['raft_port'] = config['port']  # Store original Raft port
                config['http_port'] = config['api_port']  # Store HTTP API port separately
        elif node_type == 'queue':
            self.cluster_config = [
                "qnode1:localhost:6001",
                "qnode2:localhost:6002",
                "qnode3:localhost:6003"
            ]
            self.node_configs = [
                {'node_id': 'qnode1', 'host': 'localhost', 'port': 6001},
                {'node_id': 'qnode2', 'host': 'localhost', 'port': 6002},
                {'node_id': 'qnode3', 'host': 'localhost', 'port': 6003}
            ]
        elif node_type == 'cache':
            self.cluster_config = [
                "cnode1:localhost:7001",
                "cnode2:localhost:7002",
                "cnode3:localhost:7003"
            ]
            self.node_configs = [
                {'node_id': 'cnode1', 'host': 'localhost', 'port': 7001},
                {'node_id': 'cnode2', 'host': 'localhost', 'port': 7002},
                {'node_id': 'cnode3', 'host': 'localhost', 'port': 7003}
            ]
    
    async def start_nodes(self):
        """Start all nodes in cluster"""
        logger.info(f"Starting {self.node_type} cluster with 3 nodes...")
        
        # Connect to existing nodes in Docker
        for config in self.node_configs:
            if self.node_type == 'lock':
                # Use direct node connection instead of client
                from src.nodes.lock_manager import DistributedLockManager
                node = DistributedLockManager(
                    node_id=config['node_id'],
                    host=config['host'],
                    port=config['raft_port'],  # Use Raft port for cluster communication
                    cluster_nodes=self.cluster_config,
                    enable_http_api=True  # Enable HTTP API from the start
                )
            elif self.node_type == 'queue':
                node = DistributedQueue(
                    node_id=config['node_id'],
                    host=config['host'],
                    port=config['port'],
                    cluster_nodes=self.cluster_config,
                    partition_count=8
                )
                # Enable HTTP API manually
                from src.api.http_server import HTTPAPIServer
                node.http_server = HTTPAPIServer(node, config['host'], config['port'] + 1000)
                node.enable_http_api = True
            
            elif self.node_type == 'cache':
                node = DistributedCache(
                    node_id=config['node_id'],
                    host=config['host'],
                    port=config['port'],
                    cluster_nodes=self.cluster_config,
                    cache_size_mb=64
                )
                # Enable HTTP API manually
                from src.api.http_server import HTTPAPIServer
                node.http_server = HTTPAPIServer(node, config['host'], config['port'] + 1000)
                node.enable_http_api = True
            
            self.nodes.append(node)
        
        # First try to verify ports are available
        logger.info("Verifying ports are available...")
        import socket

        def check_port(host, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind((host, port))
                sock.close()
                return True
            except Exception as e:
                logger.error(f"Port {port} is not available: {e}")
                return False

        # Check Raft ports
        for config in self.node_configs:
            if not check_port(config['host'], config['port']):
                logger.error(f"Raft port {config['port']} is in use")
                return False

        # Check HTTP ports
        for config in self.node_configs:
            if not check_port(config['host'], config['api_port']):
                logger.error(f"HTTP port {config['api_port']} is in use")
                return False

        # Start nodes one by one
        for i, node in enumerate(self.nodes):
            logger.info(f"Starting {node.node_id}...")
            try:
                await node.start()
            except Exception as e:
                logger.error(f"Error starting {node.node_id}: {e}")
                return False

            # Brief pause between nodes
            if i < len(self.nodes) - 1:
                await asyncio.sleep(0.5)

        # Wait for nodes to settle
        await asyncio.sleep(1.0)
        
        # HTTP servers have already been started by each node's start() method
        
        self.running = True
        logger.info("All nodes started successfully!")
        
        # Print cluster information
        self._print_cluster_info()
        
        # Wait for leader election
        await asyncio.sleep(2.0)
        await self._print_leader_info()
    
    async def run_forever(self):
        """Run cluster indefinitely until stopped"""
        try:
            # Just keep running until cancelled
            while self.running:
                await asyncio.sleep(1)
                # Verify HTTP servers are still running
                for server in [node.http_server for node in self.nodes]:
                    if not server or not server.site or not server.runner:
                        logger.error("HTTP server components lost")
                        self.running = False
                        return
                
        except asyncio.CancelledError:
            self.running = False
            raise
            
    async def stop_nodes(self):
        """Stop all nodes"""
        logger.info("Stopping all nodes...")
        self.running = False
        
        for node in self.nodes:
            try:
                # Stop HTTP server first if present
                if hasattr(node, 'http_server') and node.http_server:
                    try:
                        if node.http_server.site:
                            await node.http_server.site.stop()
                        if node.http_server.runner:
                            await node.http_server.runner.cleanup()
                    except Exception as e:
                        logger.error(f"Error stopping HTTP server for {node.node_id}: {e}")

                # Then stop the node itself
                await node.stop()
            except Exception as e:
                logger.error(f"Error stopping {node.node_id}: {e}")
        
        logger.info("All nodes stopped")
    
    def _print_cluster_info(self):
        """Print cluster information"""
        print("\n" + "="*60)
        print(f"CLUSTER STARTED: {self.node_type.upper()}")
        print("="*60)
        
        for node, config in zip(self.nodes, self.node_configs):
            print(f"  {node.node_id}:")
            print(f"    Raft Port:  {config['port']}")
            print(f"    HTTP API:   {config['api_port']}")
        
        print("\nHTTP API Endpoints:")
        if self.node_type == 'lock':
            print("  POST /lock/acquire   - Acquire distributed lock")
            print("  POST /lock/release   - Release distributed lock")
            print("  POST /lock/status    - Get lock status")
        elif self.node_type == 'queue':
            print("  POST /queue/enqueue  - Enqueue message")
            print("  POST /queue/dequeue  - Dequeue message")
            print("  POST /queue/status   - Get queue status")
        elif self.node_type == 'cache':
            print("  POST /cache/get      - Get cached value")
            print("  POST /cache/put      - Put value in cache")
            print("  POST /cache/delete   - Delete cached value")
            print("  POST /cache/status   - Get cache status")
        
        print("\nCommon Endpoints:")
        print("  POST /status         - Get node status")
        print("="*60 + "\n")
    
    async def _print_leader_info(self):
        """Print leader information"""
        for node in self.nodes:
            status = await node.get_status()
            if status.get("raft_state") == "leader":
                print(f"✓ Leader detected: {node.node_id}")
                print(f"  API available at: http://{node.host}:{node.port}")
                return
            
        print("⚠ No leader detected in Docker cluster")
    
    async def _monitor_cluster(self):
        """Monitor Docker cluster forever"""
        try:
            while self.running:
                await asyncio.sleep(5)  # Check every 5 seconds
                
                # Monitor Docker containers
                await self._check_docker_cluster_health()
        
        except asyncio.CancelledError:
            pass
            
    async def _check_docker_cluster_health(self):
        """Check Docker cluster health"""
        try:
            healthy = 0
            for node in self.nodes:
                try:
                    status = await node.get_status()
                    if status and status.get("status") != "error":
                        healthy += 1
                except Exception as e:
                    logger.error(f"Error checking {node.node_id} status: {e}")
                    
            if healthy < len(self.nodes):
                logger.warning(f"Docker cluster health: {healthy}/{len(self.nodes)} nodes responding")
                
        except Exception as e:
            logger.error(f"Error checking cluster health: {e}")
    
    def _check_cluster_health(self):
        """Check cluster health"""
        healthy = sum(1 for node in self.nodes if node.running)
        
        if healthy < len(self.nodes):
            logger.warning(f"Cluster health: {healthy}/{len(self.nodes)} nodes running")


async def main():
    """Main function"""
    # Parse arguments
    node_type = 'lock'  # default
    
    if len(sys.argv) > 1:
        node_type = sys.argv[1]
        if node_type not in ['lock', 'queue', 'cache']:
            print(f"Error: Invalid node type '{node_type}'")
            print("Usage: python scripts/start_cluster_api.py [lock|queue|cache]")
            sys.exit(1)

    print("\n" + "="*60)
    print(f"STARTING 3-NODE {node_type.upper()} CLUSTER WITH HTTP API")
    print("="*60 + "\n")
    
    # Check Docker containers first
    try:
        result = await asyncio.create_subprocess_shell(
            'docker ps --filter "name=dist-node"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        
        if result.returncode != 0:
            print("❌ Error checking Docker containers!")
            print(f"Error: {stderr.decode()}")
            sys.exit(1)
            
        output = stdout.decode()
        if 'dist-node' not in output:
            print("❌ Docker containers not running!")
            print("Please start containers first:")
            print("  cd docker")
            print("  docker-compose up --build -d")
            sys.exit(1)
            
        print("✓ Docker containers detected")
    except Exception as e:
        print(f"❌ Error checking Docker containers: {e}")
    # Create cluster manager
    cluster = ClusterManager(node_type)
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(cluster.stop_nodes())
        loop.stop()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            signal.signal(sig, lambda s, f: signal_handler())
    
    try:
        # Start cluster
        await cluster.start_nodes()
        
        print("\n" + "="*60)
        print("CLUSTER READY!")
        print("="*60)
        print("\nTest with client:")
        print(f"  python benchmarks/demo_cluster_client.py")
        print("\nPress Ctrl+C to stop...")
        print("="*60 + "\n")
        
        # Run forever
        while True:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    
    except Exception as e:
        logger.error(f"Error running cluster: {e}", exc_info=True)
    
    finally:
        # Cleanup
        await cluster.stop_nodes()
        
        # Give time for cleanup
        await asyncio.sleep(1.0)
        
        print("\nCluster stopped\n")


if __name__ == '__main__':
    try:
        # Use a custom event loop policy for Windows
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Run with proper cleanup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            # Ensure we have time for cleanup
            print("\nShutting down...")
            tasks = asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
            tasks.cancel()
            loop.run_until_complete(tasks)
            loop.stop()
        finally:
            loop.close()
            print("\nShutdown complete")
            sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
