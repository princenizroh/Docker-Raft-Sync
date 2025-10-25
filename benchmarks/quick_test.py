"""
Quick test of lock manager - simplified
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nodes.lock_manager import DistributedLockManager, LockType


async def test_lock():
    """Test lock in single process cluster"""
    print("\n=== Creating 3-node cluster ===\n")
    
    nodes = []
    for i in range(1, 4):
        node_id = f"node-{i}"
        port = 5000 + (i-1) * 10
        peers = [f"node-{j}:localhost:{5000 + (j-1)*10}" for j in range(1, 4) if j != i]
        
        node = DistributedLockManager(
            node_id=node_id,
            host="localhost",
            port=port,
            cluster_nodes=peers
        )
        nodes.append(node)
    
    try:
        # Start all nodes
        print("Starting nodes...")
        await asyncio.gather(*[n.start() for n in nodes])
        print("All nodes started\n")
        
        # Wait for leader
        print("Waiting for leader election...")
        await asyncio.sleep(3)
        
        leader = None
        for node in nodes:
            if node.is_leader():
                leader = node
                print(f"Leader: {node.node_id}\n")
                break
        
        if not leader:
            print("ERROR: No leader!\n")
            return
        
        # Try to acquire lock
        print("Acquiring lock...")
        success = await leader.acquire_lock(
            resource_id="test-resource",
            requester_id="test-client",
            lock_type=LockType.EXCLUSIVE,
            timeout=5.0
        )
        
        print(f"Lock acquisition: {'SUCCESS' if success else 'FAILED'}\n")
        
        if success:
            print("Lock acquired! Holding for 2 seconds...")
            await asyncio.sleep(2)
            
            print("Releasing lock...")
            released = await leader.release_lock("test-resource", "test-client")
            print(f"Lock release: {'SUCCESS' if released else 'FAILED'}\n")
        
    finally:
        print("Stopping cluster...")
        for node in nodes:
            await node.stop()
        print("Done!")


if __name__ == "__main__":
    asyncio.run(test_lock())
