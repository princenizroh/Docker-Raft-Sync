#!/usr/bin/env python3
"""
Demo script to showcase system capabilities
"""

import asyncio
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.nodes.lock_manager import DistributedLockManager, LockType
from src.nodes.queue_node import DistributedQueue
from src.nodes.cache_node import DistributedCache


async def demo_locks(lock_manager):
    """Demo distributed locks"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Lock Manager")
    print("=" * 60)
    
    # Wait a bit for initialization
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(3)
    
    print("\n1. Acquiring exclusive lock on 'resource-1'...")
    success = await lock_manager.acquire_lock(
        resource_id="resource-1",
        requester_id="client-1",
        lock_type=LockType.EXCLUSIVE,
        timeout=5.0
    )
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        print("\n2. Trying to acquire shared lock on same resource (should wait)...")
        success2 = await lock_manager.acquire_lock(
            resource_id="resource-1",
            requester_id="client-2",
            lock_type=LockType.SHARED,
            timeout=2.0
        )
        print(f"   Result: {'SUCCESS' if success2 else 'TIMEOUT (Expected)'}")
        
        print("\n3. Releasing lock from client-1...")
        await lock_manager.release_lock("resource-1", "client-1")
        print("   Lock released")
    
    print("\n4. Lock Status:")
    status = lock_manager.get_lock_status("resource-1")
    if status:
        print(f"   Resource: {status['resource_id']}")
        print(f"   Holders: {status['holders']}")
        print(f"   Waiters: {status['waiters']}")


async def demo_queue(queue):
    """Demo distributed queue"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Queue System")
    print("=" * 60)
    
    # Wait a bit for initialization
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(3)
    
    print("\n1. Enqueueing messages...")
    for i in range(5):
        message = f"Message {i}: Hello from distributed queue!"
        success = await queue.enqueue("demo-queue", message)
        print(f"   Enqueued: {message} - {'SUCCESS' if success else 'FAILED'}")
        await asyncio.sleep(0.5)
    
    print("\n2. Dequeueing messages...")
    for i in range(3):
        message = await queue.dequeue("demo-queue", "consumer-1")
        if message:
            print(f"   Dequeued: {message.data}")
            await queue.acknowledge(message.message_id, "consumer-1")
        await asyncio.sleep(0.5)
    
    print("\n3. Queue Statistics:")
    stats = queue.get_queue_stats()
    print(f"   Total messages: {stats['total_messages']}")
    print(f"   Partitions: {stats['partitions']}")
    print(f"   Consumers: {stats['total_consumers']}")


async def demo_cache(cache):
    """Demo distributed cache"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Cache (MESI Protocol)")
    print("=" * 60)
    
    # Wait a bit for initialization
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(3)
    
    print("\n1. Putting values in cache...")
    for i in range(5):
        key = f"key-{i}"
        value = f"value-{i}-{time.time()}"
        success = await cache.put(key, value)
        print(f"   Put: {key} = {value[:30]}... - {'SUCCESS' if success else 'FAILED'}")
        await asyncio.sleep(0.5)
    
    print("\n2. Getting values from cache...")
    for i in range(5):
        key = f"key-{i}"
        value = await cache.get(key)
        print(f"   Get: {key} = {value[:30] if value else 'None'}...")
        await asyncio.sleep(0.3)
    
    print("\n3. Cache Statistics:")
    stats = cache.get_cache_stats()
    print(f"   Total lines: {stats['total_lines']}")
    print(f"   Hit rate: {stats['hit_rate_percent']:.2f}%")
    print(f"   Utilization: {stats['utilization_percent']:.2f}%")
    print(f"   States: {stats['states']}")


async def run_demo_on_node(node_type, node_id, port):
    """Run demo on a specific node type"""
    # Demo node does NOT join cluster as Raft member!
    # It connects to one of the cluster nodes to send requests
    cluster_nodes = []  # EMPTY - not a cluster member!
    
    # Create node based on type
    if node_type == "lock":
        node = DistributedLockManager(
            node_id=node_id,
            host="localhost",
            port=port,
            cluster_nodes=cluster_nodes  # Empty = standalone
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
        print(f"\nStarting {node_type} node {node_id} (standalone mode)...")
        await node.start()
        
        # Wait for cluster to stabilize
        print("\nWaiting for node to become leader...")
        await asyncio.sleep(3)
        
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


async def main():
    """Main entry point - Demo Selector"""
    print("=" * 60)
    print("Distributed Synchronization System - Demo Selector")
    print("=" * 60)
    print()
    print("Select demo mode:")
    print()
    print("  1. STANDALONE MODE (Recommended for testing)")
    print("     - No cluster required")
    print("     - Single independent node")
    print("     - Quick and easy to run")
    print()
    print("  2. CLUSTER MODE (Production-like)")
    print("     - Requires running cluster (start_cluster.py)")
    print("     - Connects as 4th node to cluster")
    print("     - Demonstrates distributed consensus")
    print()
    
    mode_choice = input("Enter mode (1-2): ").strip()
    
    if mode_choice == "1":
        print("\n[STARTING STANDALONE MODE]")
        from benchmarks.demo_standalone import run_standalone_demo
        # Run standalone demo with defaults
        await run_standalone_demo("lock", "demo-node", 6000)
        return
    elif mode_choice == "2":
        print("\n[STARTING CLUSTER MODE]")
        print("\n[INFO] Make sure cluster is running first:")
        print("python scripts/start_cluster.py")
        print("\nConnecting to cluster...")
        
        from benchmarks.demo_cluster_client import main as run_cluster_demo
        await run_cluster_demo()
        return
    
    print("\n[FALLBACK TO STANDALONE MODE]")
    print("Invalid choice, showing demo type selection...")
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
    asyncio.run(run_demo_on_node(node_type, "demo-node", 6000))


if __name__ == "__main__":
    asyncio.run(main())
