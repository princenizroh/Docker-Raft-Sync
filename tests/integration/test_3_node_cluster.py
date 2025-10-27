# """
# Comprehensive 3-Node Cluster Integration Tests
# Tests distributed lock, queue, and cache with 3 nodes
# """

# import asyncio
# import pytest
# import time
# import logging
# from typing import List

# from src.nodes.lock_manager import DistributedLockManager, LockType, DeadlockError
# from src.nodes.queue_node import DistributedQueue
# from src.nodes.cache_node import DistributedCache

# logger = logging.getLogger(__name__)


# @pytest.fixture
# async def three_node_cluster():
#     """Setup 3-node cluster"""
#     nodes = []
    
#     # Define cluster nodes - using high ports to avoid conflicts
#     cluster_config = [
#         "node1:localhost:8001",
#         "node2:localhost:8002",
#         "node3:localhost:8003"
#     ]
    
#     # Create 3 lock manager nodes
#     for i in range(1, 4):
#         node = DistributedLockManager(
#             node_id=f"node{i}",
#             host="localhost",
#             port=8000 + i,
#             cluster_nodes=cluster_config
#         )
#         nodes.append(node)
    
#     # Start all nodes
#     for node in nodes:
#         await node.start()
    
#     # Wait for cluster to stabilize
#     await asyncio.sleep(2.0)
    
#     yield nodes
    
#     # Cleanup
#     for node in nodes:
#         await node.stop()


# @pytest.fixture
# async def three_queue_nodes():
#     """Setup 3 queue nodes"""
#     nodes = []
    
#     cluster_config = [
#         "qnode1:localhost:8101",
#         "qnode2:localhost:8102",
#         "qnode3:localhost:8103"
#     ]
    
#     for i in range(1, 4):
#         node = DistributedQueue(
#             node_id=f"qnode{i}",
#             host="localhost",
#             port=8100 + i,
#             cluster_nodes=cluster_config,
#             partition_count=8
#         )
#         nodes.append(node)
    
#     for node in nodes:
#         await node.start()
    
#     await asyncio.sleep(2.0)
    
#     yield nodes
    
#     for node in nodes:
#         await node.stop()


# @pytest.fixture
# async def three_cache_nodes():
#     """Setup 3 cache nodes"""
#     nodes = []
    
#     cluster_config = [
#         "cnode1:localhost:8201",
#         "cnode2:localhost:8202",
#         "cnode3:localhost:8203"
#     ]
    
#     for i in range(1, 4):
#         node = DistributedCache(
#             node_id=f"cnode{i}",
#             host="localhost",
#             port=8200 + i,
#             cluster_nodes=cluster_config,
#             cache_size_mb=64
#         )
#         nodes.append(node)
    
#     for node in nodes:
#         await node.start()
    
#     await asyncio.sleep(2.0)
    
#     yield nodes
    
#     for node in nodes:
#         await node.stop()


# class TestThreeNodeLockCluster:
#     """Test 3-node lock manager cluster"""
    
#     @pytest.mark.asyncio
#     async def test_cluster_formation(self, three_node_cluster):
#         """Test that 3 nodes form a cluster"""
#         nodes = three_node_cluster
        
#         # Check all nodes are running
#         for node in nodes:
#             assert node.running
        
#         # Wait for leader election
#         await asyncio.sleep(2.0)
        
#         # Verify leader elected
#         leaders = [n for n in nodes if n.raft.state == 'leader']
#         assert len(leaders) == 1, "Should have exactly one leader"
        
#         # Verify followers
#         followers = [n for n in nodes if n.raft.state == 'follower']
#         assert len(followers) == 2, "Should have exactly two followers"
    
#     @pytest.mark.asyncio
#     async def test_distributed_lock_across_nodes(self, three_node_cluster):
#         """Test distributed lock works across 3 nodes"""
#         nodes = three_node_cluster
        
#         # Wait for stable leader
#         await asyncio.sleep(2.0)
        
#         resource = "test_resource_123"
        
#         # Node 1 acquires lock
#         success1 = await nodes[0].acquire_lock(resource, nodes[0].node_id, lock_type=LockType.EXCLUSIVE)
#         assert success1, "Node 1 should acquire lock"
        
#         # Node 2 tries to acquire same lock (should fail)
#         success2 = await nodes[1].acquire_lock(resource, nodes[1].node_id, lock_type=LockType.EXCLUSIVE)
#         assert not success2, "Node 2 should NOT acquire lock (already held)"
        
#         # Node 1 releases lock
#         released = await nodes[0].release_lock(resource, nodes[0].node_id)
#         assert released, "Node 1 should release lock"
        
#         # Wait for replication
#         await asyncio.sleep(0.5)
        
#         # Node 2 acquires lock now
#         success3 = await nodes[1].acquire_lock(resource, nodes[1].node_id, lock_type=LockType.EXCLUSIVE)
#         assert success3, "Node 2 should acquire lock after release"
    
#     @pytest.mark.asyncio
#     async def test_shared_locks_multiple_nodes(self, three_node_cluster):
#         """Test multiple nodes can hold shared locks"""
#         nodes = three_node_cluster
        
#         await asyncio.sleep(2.0)
        
#         resource = "shared_resource_456"
        
#         # All 3 nodes acquire shared locks
#         results = []
#         for i, node in enumerate(nodes):
#             success = await node.acquire_lock(resource, node.node_id, lock_type=LockType.SHARED)
#             results.append(success)
#             await asyncio.sleep(0.3)
        
#         # All should succeed
#         assert all(results), "All nodes should acquire shared locks"
        
#         # Verify lock status
#         status = nodes[0].get_lock_status()
#         assert resource in status['locks']
#         assert len(status['locks'][resource]) >= 2, "Multiple holders expected"
    
#     @pytest.mark.asyncio
#     async def test_leader_failure_recovery(self, three_node_cluster):
#         """Test cluster recovers from leader failure"""
#         nodes = three_node_cluster
        
#         # Wait for initial leader election
#         await asyncio.sleep(5.0)  # Increased wait time
        
#         # Try multiple times to find the leader
#         leader = None
#         for _ in range(3):  # Try up to 3 times
#             for node in nodes:
#                 if node.raft.state == 'leader':
#                     leader = node
#                     break
#             if leader:
#                 break
#             await asyncio.sleep(1.0)
        
#         assert leader is not None, "No leader elected after multiple attempts"
#         logger.info(f"Current leader: {leader.node_id}")
        
#         # Acquire lock on leader
#         resource = "fail_test_789"
#         success = await leader.acquire_lock(resource, leader.node_id, lock_type=LockType.SHARED)
#         assert success
        
#         # Simulate leader failure (stop it)
#         await leader.stop()
        
#         # Wait for new leader election
#         await asyncio.sleep(3.0)
        
#         # Verify new leader elected from remaining nodes
#         remaining = [n for n in nodes if n.running]
#         leaders = [n for n in remaining if n.raft.state == 'leader']
        
#         assert len(leaders) == 1, "New leader should be elected"
#         assert leaders[0].node_id != leader.node_id, "Different node should become leader"
    
#     @pytest.mark.asyncio
#     async def test_deadlock_detection_multi_node(self, three_node_cluster):
#         """Test deadlock detection across multiple nodes"""
#         nodes = three_node_cluster
        
#         await asyncio.sleep(2.0)
        
#         # Create circular dependency
#         # Node1 holds A, wants B
#         # Node2 holds B, wants C
#         # Node3 holds C, wants A
        
#         # Node1 acquires A
#         await nodes[0].acquire_lock("resource_A", "node1", lock_type=LockType.EXCLUSIVE)
#         await asyncio.sleep(0.3)
        
#         # Node2 acquires B
#         await nodes[1].acquire_lock("resource_B", "node2", lock_type=LockType.EXCLUSIVE)
#         await asyncio.sleep(0.3)
        
#         # Node3 acquires C
#         await nodes[2].acquire_lock("resource_C", "node3", lock_type=LockType.EXCLUSIVE)
#         await asyncio.sleep(0.3)
        
#         # Create circular wait (should detect deadlock)
#         # This is tricky - our current implementation may abort one transaction
        
#         # Check deadlock detection works
#         status_a = nodes[0].get_lock_status("resource_A")
#         status_b = nodes[1].get_lock_status("resource_B")  
#         status_c = nodes[2].get_lock_status("resource_C")
        
#         logger.info(f"Lock status A: {status_a}")
#         logger.info(f"Lock status B: {status_b}")
#         logger.info(f"Lock status C: {status_c}")
        
#         # Verify each resource is held exclusively
#         assert status_a['holder'] == "node1"
#         assert status_b['holder'] == "node2"
#         assert status_c['holder'] == "node3"
        
#         # Try to create deadlock and verify detection
#         with pytest.raises(DeadlockError):
#             await nodes[1].acquire_lock("resource_A", "node2", lock_type=LockType.EXCLUSIVE)


# class TestThreeNodeQueueCluster:
#     """Test 3-node queue cluster"""
    
#     @pytest.mark.asyncio
#     async def test_queue_cluster_formation(self, three_queue_nodes):
#         """Test queue cluster forms properly"""
#         nodes = three_queue_nodes
        
#         for node in nodes:
#             assert node.running
        
#         await asyncio.sleep(2.0)
        
#         # Verify consistent hashing setup
#         for node in nodes:
#             assert node.consistent_hash is not None
#             assert len(node.consistent_hash.nodes) > 0
    
#     @pytest.mark.asyncio
#     async def test_message_enqueue_dequeue_cluster(self, three_queue_nodes):
#         """Test message enqueue/dequeue across cluster"""
#         nodes = three_queue_nodes
        
#         await asyncio.sleep(2.0)
        
#         queue_name = "test_queue_123"
        
#         # Enqueue messages from different nodes
#         messages = []
#         for i in range(10):
#             node = nodes[i % 3]  # Round-robin across nodes
#             msg_data = f"Message_{i}"
#             success = await node.enqueue(queue_name, msg_data)
#             if success:
#                 messages.append(msg_data)
#             await asyncio.sleep(0.1)
        
#         # Wait for replication
#         await asyncio.sleep(1.0)
        
#         # Dequeue from different node
#         dequeued = []
#         for _ in range(5):
#             for node in nodes:
#                 msg = await node.dequeue(queue_name, f"consumer_{node.node_id}")
#                 if msg:
#                     dequeued.append(msg.data)
#                     await asyncio.sleep(0.1)
        
#         assert len(dequeued) > 0, "Should dequeue some messages"
    
#     @pytest.mark.asyncio
#     async def test_at_least_once_delivery(self, three_queue_nodes):
#         """Test at-least-once delivery guarantee"""
#         nodes = three_queue_nodes
        
#         await asyncio.sleep(2.0)
        
#         queue_name = "delivery_test"
        
#         # Enqueue message
#         test_msg = "important_message"
#         success = await nodes[0].enqueue(queue_name, test_msg)
#         assert success
        
#         await asyncio.sleep(0.5)
        
#         # Dequeue but don't acknowledge
#         msg = await nodes[1].dequeue(queue_name, "consumer_1")
        
#         if msg:
#             assert msg.data == test_msg
#             assert msg.delivered, "Message should be marked as delivered"
            
#             # Acknowledge delivery
#             ack = await nodes[1].acknowledge(msg.message_id, "consumer_1")
#             assert ack


# class TestThreeNodeCacheCluster:
#     """Test 3-node cache cluster with MESI protocol"""
    
#     @pytest.mark.asyncio
#     async def test_cache_cluster_formation(self, three_cache_nodes):
#         """Test cache cluster forms properly"""
#         nodes = three_cache_nodes
        
#         for node in nodes:
#             assert node.running
        
#         await asyncio.sleep(2.0)
    
#     @pytest.mark.asyncio
#     async def test_mesi_protocol_invalidation(self, three_cache_nodes):
#         """Test MESI protocol invalidation across nodes"""
#         nodes = three_cache_nodes
        
#         await asyncio.sleep(2.0)
        
#         key = "test_key_123"
#         value1 = "initial_value"
        
#         # Node 1 writes value
#         success = await nodes[0].put(key, value1)
#         assert success, "Failed to put initial value"
        
#         # Wait for broadcast
#         await asyncio.sleep(1.0)  # Increased wait time
        
#         # Node 2 reads value (should be SHARED)
#         read_val = await nodes[1].get(key)
#         assert read_val == value1, f"Expected {value1}, got {read_val}"
        
#         # Node 3 writes new value (should invalidate others)
#         value2 = "updated_value"
#         success = await nodes[2].put(key, value2)
#         assert success, "Failed to put updated value"
        
#         await asyncio.sleep(1.0)  # Increased wait time
        
#         # Node 1 reads again (should get updated value)
#         read_val2 = await nodes[0].get(key)
#         assert read_val2 == value2, f"Expected {value2}, got {read_val2}"
        
#         # Verify cache state
#         status0 = await nodes[0].get_cache_status(key)
#         status1 = await nodes[1].get_cache_status(key)
#         status2 = await nodes[2].get_cache_status(key)
        
#         assert status2["state"] == "MODIFIED", "Writer should be in MODIFIED state"
#         assert status0["state"] in ["INVALID", "SHARED"], "Other nodes should be INVALID or SHARED"
#         assert status1["state"] in ["INVALID", "SHARED"], "Other nodes should be INVALID or SHARED"
        
#         # Verify cache coherence maintained
#         stats = nodes[0].get_cache_stats()
#         logger.info(f"Cache stats: {stats}")
    
#     @pytest.mark.asyncio
#     async def test_cache_lru_eviction(self, three_cache_nodes):
#         """Test LRU eviction works in cluster"""
#         nodes = three_cache_nodes
        
#         await asyncio.sleep(2.0)
        
#         # Fill cache to capacity
#         for i in range(100):
#             await nodes[0].put(f"key_{i}", f"value_{i}")
#             await asyncio.sleep(0.05)
        
#         # Wait for replication
#         await asyncio.sleep(1.0)
        
#         # Check cache stats
#         stats = nodes[0].get_cache_stats()
#         logger.info(f"Cache utilization: {stats['utilization_percent']}%")
        
#         # Verify LRU eviction happened
#         assert stats['total_lines'] <= stats['capacity']
    
#     @pytest.mark.asyncio
#     async def test_cache_hit_rate(self, three_cache_nodes):
#         """Test cache hit rate measurement"""
#         nodes = three_cache_nodes
        
#         await asyncio.sleep(2.0)
        
#         # Write some values
#         for i in range(10):
#             await nodes[0].put(f"key_{i}", f"value_{i}")
#             await asyncio.sleep(0.05)
        
#         await asyncio.sleep(0.5)
        
#         # Read same values (should be cache hits)
#         for i in range(10):
#             await nodes[1].get(f"key_{i}")
#             await asyncio.sleep(0.05)
        
#         # Check hit rate
#         stats = nodes[1].get_cache_stats()
#         logger.info(f"Cache hit rate: {stats['hit_rate_percent']}%")
        
#         assert stats['hits'] > 0, "Should have cache hits"


# class TestNetworkPartition:
#     """Test network partition scenarios"""
    
#     @pytest.mark.asyncio
#     async def test_partition_detection(self, three_node_cluster):
#         """Test cluster detects network partition"""
#         nodes = three_node_cluster
        
#         await asyncio.sleep(2.0)
        
#         # Wait for leader election
#         await asyncio.sleep(5.0)  # Increased wait time
        
#         # Try multiple times to find the leader
#         leader = None
#         for _ in range(3):  # Try up to 3 times
#             for node in nodes:
#                 if node.raft.state == 'leader':
#                     leader = node
#                     break
#             if leader:
#                 break
#             await asyncio.sleep(1.0)
            
#         assert leader is not None, "No leader elected after multiple attempts"
#         logger.info(f"Found leader: {leader.node_id}")
        
#         # Find a follower node
#         follower = None
#         for node in nodes:
#             if node.raft.state == 'follower':
#                 follower = node
#                 break
                
#         assert follower is not None, "No follower found"
        
#         # This simulates network partition
#         old_send = follower.message_passing.send_message
        
#         async def blocked_send(*args, **kwargs):
#             logger.info("Simulating network partition - message blocked")
#             return False
        
#         follower.message_passing.send_message = blocked_send
        
#         # Wait for partition to be detected
#         await asyncio.sleep(3.0)
        
#         # Restore communication
#         follower.message_passing.send_message = old_send
        
#         # Wait for recovery
#         await asyncio.sleep(2.0)
        
#         # Verify cluster recovers
#         leaders = [n for n in nodes if n.running and n.raft.state == 'leader']
#         assert len(leaders) == 1


# if __name__ == '__main__':
#     pytest.main([__file__, '-v', '-s'])
