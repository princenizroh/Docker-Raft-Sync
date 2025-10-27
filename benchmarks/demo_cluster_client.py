"""
3-Node Cluster Demo Client
Demonstrates distributed system features WITHOUT being a Raft node
Uses RPC/HTTP to communicate with cluster
"""

import asyncio
import aiohttp
import logging
import sys
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClusterClient:
    """
    Client for interacting with distributed system cluster
    NOT a Raft node - communicates via RPC
    """
    
    def __init__(self, cluster_nodes: list):
        """
        Args:
            cluster_nodes: List of node addresses ["host:port", ...]
        """
        self.cluster_nodes = cluster_nodes
        self.session: Optional[aiohttp.ClientSession] = None
        self.leader_node: Optional[str] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _send_request(self, node: str, endpoint: str, data: dict) -> Optional[dict]:
        """Send HTTP request to node"""
        try:
            url = f"http://{node}{endpoint}"
            async with self.session.post(url, json=data, timeout=5.0) as resp:
                response_data = await resp.json()
                if resp.status == 200:
                    return response_data
                else:
                    error_msg = response_data.get('error', 'Unknown error')
                    logger.warning(f"Request to {node} failed ({resp.status}): {error_msg}")
                    return None
        except aiohttp.ClientError as e:
            logger.debug(f"Network error contacting {node}: {e}")
            return None
        except asyncio.TimeoutError:
            logger.debug(f"Timeout contacting {node}")
            return None
        except Exception as e:
            logger.debug(f"Unexpected error contacting {node}: {e}")
            return None
    
    async def _find_leader(self) -> Optional[str]:
        """Find current cluster leader"""
        for node in self.cluster_nodes:
            result = await self._send_request(node, "/status", {})
            if result and result.get('is_leader'):
                logger.info(f"Found leader: {node}")
                self.leader_node = node
                return node
        
        logger.warning("No leader found")
        return None
    
    async def acquire_lock(self, resource: str, client_id: str, lock_type: str = 'EXCLUSIVE') -> bool:
        """Acquire distributed lock
        
        Args:
            resource: Resource to lock
            client_id: ID of client requesting lock
            lock_type: 'EXCLUSIVE' or 'SHARED'
        """
        if not self.leader_node:
            await self._find_leader()
        
        if not self.leader_node:
            logger.error("Cannot acquire lock: no leader available")
            return False
        
        data = {
            'resource': resource,
            'client_id': client_id,
            'lock_type': lock_type.upper(),
            'timeout': 30.0
        }
        
        result = await self._send_request(self.leader_node, "/lock/acquire", data)
        
        if result and result.get('success'):
            logger.info(f"✓ Lock acquired: {resource} (type={lock_type})")
            return True
        else:
            logger.warning(f"✗ Failed to acquire lock: {resource}")
            return False
    
    async def release_lock(self, resource: str, client_id: str) -> bool:
        """Release distributed lock"""
        if not self.leader_node:
            await self._find_leader()
        
        data = {
            'resource': resource,
            'client_id': client_id,
            'force': False  # Add force flag
        }
        
        result = await self._send_request(self.leader_node, "/lock/release", data)
        
        if result and result.get('success'):
            logger.info(f"✓ Lock released: {resource}")
            return True
        else:
            logger.warning(f"✗ Failed to release lock: {resource}")
            return False
    
    async def enqueue_message(self, queue_name: str, data: Any) -> bool:
        """Enqueue message to distributed queue"""
        if not self.leader_node:
            await self._find_leader()
        
        payload = {
            'queue_name': queue_name,
            'data': data
        }
        
        result = await self._send_request(self.leader_node, "/queue/enqueue", payload)
        
        if result and result.get('success'):
            logger.info(f"✓ Message enqueued to {queue_name}: {data}")
            return True
        else:
            logger.warning(f"✗ Failed to enqueue message")
            return False
    
    async def dequeue_message(self, queue_name: str, consumer_id: str) -> Optional[Any]:
        """Dequeue message from distributed queue"""
        if not self.leader_node:
            await self._find_leader()
        
        payload = {
            'queue_name': queue_name,
            'consumer_id': consumer_id
        }
        
        result = await self._send_request(self.leader_node, "/queue/dequeue", payload)
        
        if result and result.get('message'):
            msg = result['message']
            logger.info(f"✓ Message dequeued from {queue_name}: {msg.get('data')}")
            return msg
        else:
            logger.info(f"No messages in queue: {queue_name}")
            return None
    
    async def cache_get(self, key: str) -> Optional[Any]:
        """Get value from distributed cache"""
        if not self.leader_node:
            await self._find_leader()
        
        payload = {'key': key}
        
        result = await self._send_request(self.leader_node, "/cache/get", payload)
        
        if result and result.get('value') is not None:
            logger.info(f"✓ Cache HIT: {key} = {result['value']}")
            return result['value']
        else:
            logger.info(f"✗ Cache MISS: {key}")
            return None
    
    async def cache_put(self, key: str, value: Any) -> bool:
        """Put value in distributed cache"""
        if not self.leader_node:
            await self._find_leader()
        
        payload = {
            'key': key,
            'value': value
        }
        
        result = await self._send_request(self.leader_node, "/cache/put", payload)
        
        if result and result.get('success'):
            logger.info(f"✓ Cache PUT: {key} = {value}")
            return True
        else:
            logger.warning(f"✗ Failed to cache PUT: {key}")
            return False
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get cluster status"""
        status = {
            'nodes': [],
            'leader': None,
            'healthy_nodes': 0
        }
        
        for node in self.cluster_nodes:
            node_status = await self._send_request(node, "/status", {})
            if node_status:
                status['nodes'].append({
                    'address': node,
                    'is_leader': node_status.get('is_leader', False),
                    'state': node_status.get('state', 'unknown')
                })
                status['healthy_nodes'] += 1
                
                if node_status.get('is_leader'):
                    status['leader'] = node
        
        return status


async def demo_locks(client: ClusterClient):
    """Demo distributed lock manager"""
    print("\n" + "="*60)
    print("DEMO 1: DISTRIBUTED LOCK MANAGER")
    print("="*60)
    
    resource = "critical_resource"
    client_id = "demo_client"
    
    print(f"\n1. Acquiring exclusive lock on '{resource}'...")
    success = await client.acquire_lock(resource, client_id, lock_type='EXCLUSIVE')
    
    if success:
        print("   ✓ Lock acquired successfully!")
        
        print(f"\n2. Attempting second lock (should fail)...")
        success2 = await client.acquire_lock(resource, "other_client", lock_type='EXCLUSIVE')
        
        if not success2:
            print("   ✓ Second lock correctly denied!")
        
        print(f"\n3. Releasing lock...")
        await asyncio.sleep(1)
        released = await client.release_lock(resource, client_id)
        
        if released:
            print("   ✓ Lock released successfully!")
    else:
        print("   ✗ Failed to acquire lock (cluster may not be ready)")
    
    print("\n4. Testing shared locks...")
    shared_resource = "shared_data"
    
    # Multiple clients with shared locks
    for i in range(3):
        success = await client.acquire_lock(shared_resource, f"reader_{i}", lock_type='SHARED')
        if success:
            print(f"   ✓ Reader {i} acquired shared lock")
        await asyncio.sleep(0.2)


async def demo_queue(client: ClusterClient):
    """Demo distributed queue"""
    print("\n" + "="*60)
    print("DEMO 2: DISTRIBUTED QUEUE")
    print("="*60)
    
    queue_name = "task_queue"
    
    print(f"\n1. Enqueuing messages to '{queue_name}'...")
    messages = ["Task 1: Process data", "Task 2: Send email", "Task 3: Update DB"]
    
    for i, msg in enumerate(messages, 1):
        success = await client.enqueue_message(queue_name, msg)
        if success:
            print(f"   ✓ Message {i} enqueued")
        await asyncio.sleep(0.3)
    
    print(f"\n2. Dequeuing messages...")
    await asyncio.sleep(0.5)
    
    for i in range(3):
        msg = await client.dequeue_message(queue_name, f"worker_{i}")
        if msg:
            print(f"   ✓ Worker {i} received: {msg.get('data')}")
        await asyncio.sleep(0.3)


async def demo_cache(client: ClusterClient):
    """Demo distributed cache"""
    print("\n" + "="*60)
    print("DEMO 3: DISTRIBUTED CACHE")
    print("="*60)
    
    print("\n1. Writing to cache...")
    cache_data = {
        "user:1001": {"name": "Alice", "score": 95},
        "user:1002": {"name": "Bob", "score": 87},
        "user:1003": {"name": "Charlie", "score": 92}
    }
    
    for key, value in cache_data.items():
        success = await client.cache_put(key, value)
        if success:
            print(f"   ✓ Cached: {key}")
        await asyncio.sleep(0.2)
    
    print("\n2. Reading from cache...")
    await asyncio.sleep(0.5)
    
    for key in cache_data.keys():
        value = await client.cache_get(key)
        if value:
            print(f"   ✓ Retrieved: {key} = {value}")
        await asyncio.sleep(0.2)
    
    print("\n3. Cache invalidation test...")
    await client.cache_put("user:1001", {"name": "Alice", "score": 100})
    print("   ✓ Updated user:1001 (other nodes should invalidate)")


async def demo_cluster_status(client: ClusterClient):
    """Demo cluster status"""
    print("\n" + "="*60)
    print("DEMO 4: CLUSTER STATUS")
    print("="*60)
    
    status = await client.get_cluster_status()
    
    print(f"\nCluster Health:")
    print(f"  Healthy Nodes: {status['healthy_nodes']}/{len(client.cluster_nodes)}")
    print(f"  Current Leader: {status['leader'] or 'NO LEADER'}")
    
    print(f"\nNode Details:")
    for node in status['nodes']:
        role = "LEADER" if node['is_leader'] else "FOLLOWER"
        print(f"  - {node['address']}: {role} ({node['state']})")


async def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("DISTRIBUTED SYSTEM 3-NODE CLUSTER DEMO")
    print("="*60)
    print("\nThis demo connects to a running 3-node cluster")
    print("Make sure nodes are started with: python scripts/start_cluster.py")
    print("="*60)
    
    # Define cluster nodes - connecting to Docker containers
    cluster_nodes = [
        "localhost:6000",  # dist-node-1
        "localhost:6010",  # dist-node-2
        "localhost:6020"   # dist-node-3
    ]
    
    async with ClusterClient(cluster_nodes) as client:
        # Check cluster status first
        print("\nChecking cluster status...")
        await demo_cluster_status(client)
        
        # Wait for user confirmation
        if len(sys.argv) > 1 and sys.argv[1] == "--auto":
            print("\nAuto mode: continuing with demos...")
        else:
            input("\nPress ENTER to continue with demos...")
        
        try:
            # Run demos
            await demo_locks(client)
            await asyncio.sleep(1)
            
            await demo_queue(client)
            await asyncio.sleep(1)
            
            await demo_cache(client)
            await asyncio.sleep(1)
            
            # Final status check
            await demo_cluster_status(client)
            
        except Exception as e:
            logger.error(f"Demo error: {e}")
            print("\n✗ Demo failed - cluster may not be running properly")
            print("   Make sure to start cluster first:")
            print("   python scripts/start_cluster.py")
    
    print("\n" + "="*60)
    print("DEMO COMPLETED")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
