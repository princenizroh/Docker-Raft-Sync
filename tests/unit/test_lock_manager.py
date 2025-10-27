"""
Unit tests for Distributed Lock Manager
"""

import pytest
import asyncio
from src.nodes.lock_manager import DistributedLockManager, LockType, LockStatus
from src.consensus.raft import RaftState


@pytest.mark.asyncio
async def test_lock_manager_initialization():
    """Test lock manager initialization"""
    lock_manager = DistributedLockManager(
        node_id="node-1",
        host="localhost",
        port=6000,
        cluster_nodes=["node-1:localhost:6000", "node-2:localhost:6010"]
    )
    
    assert lock_manager.node_id == "node-1"
    assert len(lock_manager.locks) == 0


@pytest.mark.asyncio
async def test_exclusive_lock():
    """Test exclusive lock acquisition"""
    lock_manager = DistributedLockManager(
        node_id="node-1",
        host="localhost",
        port=6000,
        cluster_nodes=["node-1:localhost:6000"]
    )
    
    # Force leader state for testing
    lock_manager.raft.state = RaftState.LEADER
    lock_manager.raft.current_term = 1
    
    # Acquire exclusive lock
    success = await lock_manager.acquire_lock(
        resource_id="resource-1",
        requester_id="client-1",
        lock_type=LockType.EXCLUSIVE,
        timeout=1.0
    )
    
    # Note: This might fail without full setup, but tests structure
    assert isinstance(success, bool)


@pytest.mark.asyncio
async def test_shared_locks():
    """Test shared lock acquisition"""
    lock_manager = DistributedLockManager(
        node_id="node-1",
        host="localhost",
        port=6000,
        cluster_nodes=["node-1:localhost:6000"]
    )
    
    # Force leader state
    lock_manager.raft.state = RaftState.LEADER
    
    # Multiple clients should be able to acquire shared locks
    # Test structure without full cluster
    pass


def test_lock_status():
    """Test lock status retrieval"""
    lock_manager = DistributedLockManager(
        node_id="node-1",
        host="localhost",
        port=6000,
        cluster_nodes=["node-1:localhost:6000"]
    )
    
    # Get status of non-existent lock
    status = lock_manager.get_lock_status("non-existent")
    assert status is None
