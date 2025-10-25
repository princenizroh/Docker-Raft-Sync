"""
Cluster Demo - Connects to Running Cluster
Requires cluster to be running first (start_cluster.py)
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nodes.lock_manager import DistributedLockManager, LockType
from src.nodes.queue_node import DistributedQueue
from src.nodes.cache_node import DistributedCache


async def demo_locks(node: DistributedLockManager):
    """Demo distributed lock manager"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Lock Manager (Cluster Mode)")
    print("=" * 60)
    print("\n[INFO] Waiting for cluster synchronization...")
    await asyncio.sleep(8)  # Wait for cluster to sync
    
    # Demo 1: Acquire exclusive lock
    print("\n1. Acquiring exclusive lock on 'resource-1'...")
    success = await node.acquire_lock('resource-1', 'client-1', LockType.EXCLUSIVE)
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Demo 2: Try to acquire shared lock (should wait/timeout)
    print("\n2. Trying to acquire shared lock on same resource (should wait)...")
    success = await node.acquire_lock('resource-1', 'client-2', LockType.SHARED, timeout=2.0)
    print(f"   Result: {'SUCCESS' if success else 'TIMEOUT (Expected)'}")
    
    # Demo 3: Release first lock
    print("\n3. Releasing lock from client-1...")
    await node.release_lock('resource-1', 'client-1')
    print("   Lock released")
    
    # Demo 4: Show lock status
    print("\n4. Lock Status:")
    print(f"   Total locks: {len(node.locks)}")
    print(f"   Active clients: {len(node.held_locks)}")
    print()


async def demo_queue(node: DistributedQueue):
    """Demo distributed queue"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Queue System (Cluster Mode)")
    print("=" * 60)
    print("\n[INFO] Waiting for cluster synchronization...")
    await asyncio.sleep(8)
    
    # Demo 1: Enqueue messages
    print("\n1. Enqueueing messages...")
    for i in range(5):
        success = await node.enqueue('test-queue', f"Message {i}: Hello from cluster!")
        print(f"   Enqueued: Message {i} - {'SUCCESS' if success else 'FAILED'}")
        await asyncio.sleep(0.5)
    
    # Demo 2: Dequeue messages
    print("\n2. Dequeueing messages...")
    for _ in range(3):
        message = await node.dequeue('test-queue', 'consumer-1')
        if message:
            print(f"   Dequeued: {message.data}")
            await node.acknowledge('test-queue', message.message_id, 'consumer-1')
        await asyncio.sleep(0.5)
    
    # Demo 3: Show queue stats
    print("\n3. Queue Statistics:")
    total_messages = sum(len(q) for q in node.queues.values())
    print(f"   Total messages: {total_messages}")
    print(f"   Partitions: {len(node.queues)}")
    print(f"   Consumers: {len(node.consumer_offsets)}")
    print()


async def demo_cache(node: DistributedCache):
    """Demo distributed cache with MESI protocol"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Cache (MESI Protocol - Cluster Mode)")
    print("=" * 60)
    print("\n[INFO] Waiting for cluster synchronization...")
    await asyncio.sleep(8)
    
    # Demo 1: Put values
    print("\n1. Putting values in cache...")
    for i in range(5):
        key = f"key-{i}"
        value = f"value-{i}-cluster"
        success = await node.put(key, value)
        print(f"   Put: {key} = {value} - {'SUCCESS' if success else 'FAILED'}")
        await asyncio.sleep(0.5)
    
    # Demo 2: Get values
    print("\n2. Getting values from cache...")
    for i in range(5):
        key = f"key-{i}"
        value = await node.get(key)
        print(f"   Get: {key} = {value}")
    
    # Demo 3: Show cache stats
    print("\n3. Cache Statistics:")
    total_lines = len(node.cache)
    print(f"   Total lines: {total_lines}")
    
    hit_rate = (node.metrics.get_counter('cache_hits') / 
                max(1, node.metrics.get_counter('cache_hits') + node.metrics.get_counter('cache_misses'))) * 100
    print(f"   Hit rate: {hit_rate:.2f}%")
    
    utilization = (total_lines / node.cache_size) * 100
    print(f"   Utilization: {utilization:.2f}%")
    
    states = {'modified': 0, 'exclusive': 0, 'shared': 0, 'invalid': 0}
    for line in node.cache.values():
        states[line.state.value] = states.get(line.state.value, 0) + 1
    print(f"   States: {states}")
    print()


async def run_cluster_demo(node_type, node_id, port):
    """Run demo connected to existing cluster"""
    # Cluster mode: specify existing cluster nodes
    cluster_nodes = [
        "node-1:localhost:5000",
        "node-2:localhost:5010",
        "node-3:localhost:5020"
    ]
    
    # Create node based on type
    if node_type == "lock":
        node = DistributedLockManager(
            node_id=node_id,
            host="localhost",
            port=port,
            cluster_nodes=cluster_nodes
        )
        demo_func = demo_locks
    elif node_type == "queue":
        node = DistributedQueue(
            node_id=node_id,
            host="localhost",
            port=port,
            cluster_nodes=cluster_nodes
        )
        demo_func = demo_queue
    elif node_type == "cache":
        node = DistributedCache(
            node_id=node_id,
            host="localhost",
            port=port,
            cluster_nodes=cluster_nodes
        )
        demo_func = demo_cache
    else:
        print(f"Unknown node type: {node_type}")
        return
    
    try:
        print(f"\nStarting {node_type} node {node_id} (cluster mode)...")
        print("Connecting to cluster nodes...")
        await node.start()
        
        print("Waiting for cluster to stabilize...")
        await asyncio.sleep(5)
        
        # Run demo
        await demo_func(node)
        
        print("\n" + "=" * 60)
        print("Demo completed! Press Ctrl+C to exit...")
        print("=" * 60)
        
        # Keep running
        while True:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        await node.stop()


def main():
    """Main entry point"""
    print("=" * 60)
    print("Distributed Synchronization System - Cluster Demo")
    print("=" * 60)
    print()
    print("[⚠️  WARNING] CLUSTER DEMO HAS ARCHITECTURAL LIMITATION!")
    print()
    print("MASALAH:")
    print("  Demo membuat node ke-4 yang join ke cluster 3-node.")
    print("  4-node cluster perlu 3 votes untuk majority.")
    print("  Demo node TIDAK BISA dapat 3 votes karena cluster")
    print("  nodes tidak recognize node ke-4 (dynamic membership issue).")
    print()
    print("HASIL:")
    print("  Demo node perpetual elections, NEVER becomes leader.")
    print("  Commands GAGAL dengan 'Not leader, cannot submit command'.")
    print()
    print("SOLUSI:")
    print("  Pakai STANDALONE MODE untuk testing:")
    print("    python benchmarks/demo_standalone.py")
    print("  atau")
    print("    .\\run_standalone_demo.ps1")
    print()
    print("CLUSTER MODE memerlukan:")
    print("  1. Client API (bukan full node)")
    print("  2. Command forwarding ke leader")
    print("  3. Dynamic membership support")
    print()
    print("=" * 60)
    
    choice = input("\nLanjutkan cluster demo? (akan GAGAL) [y/N]: ").strip().lower()
    if choice != 'y':
        print("\n✓ Gunakan standalone mode: python benchmarks/demo_standalone.py")
        return
    
    print("\n[IMPORTANT] CLUSTER MUST BE RUNNING FIRST!")
    print()
    print("  Terminal 1: python benchmarks/start_cluster.py")
    print("  Terminal 2: python benchmarks/demo_cluster.py (this script)")
    print()
    print("  This demo connects to the existing cluster and")
    print("  participates as a 4th node in the Raft consensus.")
    print("  [WARNING] This will result in perpetual elections!")
    print()
    print("Select demo type:")
    print("  1. Distributed Lock Manager")
    print("  2. Distributed Queue System")
    print("  3. Distributed Cache (MESI)")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    node_types = {
        "1": "lock",
        "2": "queue",
        "3": "cache"
    }
    
    node_type = node_types.get(choice)
    if not node_type:
        print("Invalid choice!")
        return
    
    # Run demo
    asyncio.run(run_cluster_demo(node_type, "demo-node", 6000))


if __name__ == "__main__":
    main()
