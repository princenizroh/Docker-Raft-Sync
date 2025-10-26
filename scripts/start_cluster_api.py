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
        
        # Define cluster configuration - connecting to Docker containers
        if node_type == 'lock':
            # Connect to Raft ports
            self.cluster_config = [
                "node1:localhost:5000",  # Node 1 Raft port
                "node2:localhost:5010",  # Node 2 Raft port
                "node3:localhost:5020"   # Node 3 Raft port
            ]
            # Connect to HTTP API ports
            self.node_configs = [
                {'node_id': 'node1', 'host': 'localhost', 'port': 5001, 'container': True},  # Node 1 HTTP API
                {'node_id': 'node2', 'host': 'localhost', 'port': 5011, 'container': True},  # Node 2 HTTP API
                {'node_id': 'node3', 'host': 'localhost', 'port': 5021, 'container': True}   # Node 3 HTTP API
            ]
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
                # Instead of creating new servers, create client connections
                from src.api.http_client import HTTPAPIClient
                node = HTTPAPIClient(
                    node_id=config['node_id'],
                    host=config['host'],
                    port=config['port'],
                    cluster_nodes=self.cluster_config
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
        
        # Start all nodes
        for i, node in enumerate(self.nodes):
            logger.info(f"Starting {node.node_id}...")
            await node.start()
            
            # Stagger startup to avoid election conflicts
            if i < len(self.nodes) - 1:
                await asyncio.sleep(0.5)
        
        self.running = True
        logger.info("All nodes started successfully!")
        
        # Print cluster information
        self._print_cluster_info()
        
        # Wait for leader election
        await asyncio.sleep(2.0)
        await self._print_leader_info()
    
    async def stop_nodes(self):
        """Stop all nodes"""
        logger.info("Stopping all nodes...")
        self.running = False
        
        for node in self.nodes:
            try:
                await node.stop()
            except Exception as e:
                logger.error(f"Error stopping {node.node_id}: {e}")
        
        logger.info("All nodes stopped")
    
    def _print_cluster_info(self):
        """Print cluster information"""
        print("\n" + "="*60)
        print(f"CLUSTER STARTED: {self.node_type.upper()}")
        print("="*60)
        
        for node in self.nodes:
            api_port = node.port + 1000
            print(f"  {node.node_id}:")
            print(f"    Raft Port:  {node.port}")
            print(f"    HTTP API:   {api_port}")
        
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
    
    async def run_forever(self):
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
        healthy = 0
        for node in self.nodes:
            status = await node.get_status()
            if status.get("status") != "error":
                healthy += 1
                
        if healthy < len(self.nodes):
            logger.warning(f"Docker cluster health: {healthy}/{len(self.nodes)} nodes responding")
    
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
        await cluster.run_forever()
    
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
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
        sys.exit(0)
