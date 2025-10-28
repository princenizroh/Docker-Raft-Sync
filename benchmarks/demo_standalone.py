# Standalone demo - no cluster required

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
    print("DEMO: Distributed Lock Manager (Standalone)")
    print("=" * 60)
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(5)

    # Demo 1: Acquire exclusive lock
    print("\n1. Acquiring exclusive lock on 'resource-1'...")
    success = await node.acquire_lock("resource-1", "client-1", LockType.EXCLUSIVE)
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")

    # Demo 2: Try to acquire shared lock (should wait/timeout)
    print("\n2. Trying to acquire shared lock on same resource (should wait)...")
    success = await node.acquire_lock(
        "resource-1", "client-2", LockType.SHARED, timeout=2.0
    )
    print(f"   Result: {'SUCCESS' if success else 'TIMEOUT (Expected)'}")

    # Demo 3: Release first lock
    print("\n3. Releasing lock from client-1...")
    await node.release_lock("resource-1", "client-1")
    print("   Lock released")

    # Demo 4: Show lock status
    print("\n4. Lock Status:")
    print()


async def demo_queue(node: DistributedQueue):
    """Demo distributed queue"""
    print("\n" + "=" * 60)
    print("DEMO: Distributed Queue System (Standalone)")
    print("=" * 60)
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(5)

    # Demo 1: Enqueue messages
    print("\n1. Enqueueing messages...")
    for i in range(5):
        success = await node.enqueue(
            "test-queue", f"Message {i}: Hello from distributed queue!"
        )
        print(
            f"   Enqueued: Message {i}: Hello from distributed queue! - {'SUCCESS' if success else 'FAILED'}"
        )
        await asyncio.sleep(0.5)

    # Demo 2: Dequeue messages
    print("\n2. Dequeueing messages...")
    for _ in range(3):
        message = await node.dequeue("test-queue", "consumer-1")
        if message:
            print(f"   Dequeued: {message.data}")
            await node.acknowledge("test-queue", message.message_id, "consumer-1")
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
    print("DEMO: Distributed Cache (MESI Protocol - Standalone)")
    print("=" * 60)
    print("\n[INFO] Waiting for node initialization...")
    await asyncio.sleep(5)

    # Demo 1: Put values
    print("\n1. Putting values in cache...")
    for i in range(5):
        key = f"key-{i}"
        value = f"value-{i}-{id(key)}"
        success = await node.put(key, value)
        print(f"   Put: {key} = {value}... - {'SUCCESS' if success else 'FAILED'}")
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

    hit_rate = (
        node.metrics.get_counter("cache_hits")
        / max(
            1,
            node.metrics.get_counter("cache_hits")
            + node.metrics.get_counter("cache_misses"),
        )
    ) * 100
    print(f"   Hit rate: {hit_rate:.2f}%")

    utilization = (total_lines / node.cache_size) * 100
    print(f"   Utilization: {utilization:.2f}%")

    states = {"modified": 0, "exclusive": 0, "shared": 0, "invalid": 0}
    for line in node.cache.values():
        states[line.state.value] = states.get(line.state.value, 0) + 1
    print(f"   States: {states}")
    print()


async def run_standalone_demo(node_type, node_id, port):
    """Run standalone demo (no cluster needed)"""
    # Standalone mode: cluster_nodes=[] means no cluster membership
    cluster_nodes = []

    # Create node based on type
    if node_type == "lock":
        node = DistributedLockManager(
            node_id=node_id, host="localhost", port=port, cluster_nodes=cluster_nodes
        )
        demo_func = demo_locks
    elif node_type == "queue":
        node = DistributedQueue(
            node_id=node_id, host="localhost", port=port, cluster_nodes=cluster_nodes
        )
        demo_func = demo_queue
    elif node_type == "cache":
        node = DistributedCache(
            node_id=node_id, host="localhost", port=port, cluster_nodes=cluster_nodes
        )
        demo_func = demo_cache
    else:
        print(f"Unknown node type: {node_type}")
        return

    try:
        print(f"\nStarting {node_type} node {node_id} (standalone mode)...")
        await node.start()

        # Wait for node to become leader
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


def main():
    """Main entry point"""
    print("=" * 60)
    print("Distributed Synchronization System - Standalone Demo")
    print("=" * 60)
    print()
    print("[INFO] Standalone mode - NO CLUSTER REQUIRED")
    print("  - Demo creates its own independent node")
    print("  - Node becomes leader immediately")
    print("  - All operations work without cluster")
    print()
    print("Select demo type:")
    print("  1. Distributed Lock Manager")
    print("  2. Distributed Queue System")
    print("  3. Distributed Cache (MESI)")
    print()

    choice = input("Enter choice (1-3): ").strip()

    node_types = {"1": "lock", "2": "queue", "3": "cache"}

    node_type = node_types.get(choice)
    if not node_type:
        print("Invalid choice!")
        return

    # Run demo
    asyncio.run(run_standalone_demo(node_type, "demo-node", 6000))


if __name__ == "__main__":
    main()
