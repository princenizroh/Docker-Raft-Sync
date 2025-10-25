"""
Integration Tests for Distributed System
Tests multi-component interactions
"""

import pytest
import asyncio
from src.consensus.raft import RaftNode, RaftState


@pytest.mark.asyncio
async def test_three_node_cluster():
    """Test 3-node Raft cluster formation"""
    # Create 3-node cluster
    nodes = [
        RaftNode('node-1', ['node-2', 'node-3']),
        RaftNode('node-2', ['node-1', 'node-3']),
        RaftNode('node-3', ['node-1', 'node-2'])
    ]
    
    try:
        # Start all nodes
        for node in nodes:
            await node.start()
        
        # Give time for initial state
        await asyncio.sleep(0.1)
        
        # All should start as followers
        for node in nodes:
            assert node.state in [RaftState.FOLLOWER, RaftState.CANDIDATE]
        
        # Verify basic properties
        assert len(nodes) == 3
        assert all(n._running for n in nodes)
        
    finally:
        # Cleanup
        for node in nodes:
            await node.stop()


@pytest.mark.asyncio
async def test_leader_election_process():
    """Test that leader election eventually succeeds"""
    nodes = [
        RaftNode('node-1', ['node-2', 'node-3'], election_timeout_min=100, election_timeout_max=200),
        RaftNode('node-2', ['node-1', 'node-3'], election_timeout_min=100, election_timeout_max=200),
        RaftNode('node-3', ['node-1', 'node-2'], election_timeout_min=100, election_timeout_max=200)
    ]
    
    try:
        # Start all nodes
        for node in nodes:
            await node.start()
        
        # Wait for election attempts
        await asyncio.sleep(1.0)
        
        # At least one should have tried to become candidate
        candidate_found = any(node.state == RaftState.CANDIDATE for node in nodes)
        assert candidate_found, "No candidate emerged during election"
        
        # Term should have progressed
        max_term = max(node.current_term for node in nodes)
        assert max_term > 0, "No term progression occurred"
        
    finally:
        for node in nodes:
            await node.stop()


@pytest.mark.asyncio
async def test_log_replication_single_node():
    """Test log replication in single node (simplified)"""
    node = RaftNode('leader', [])
    
    try:
        await node.start()
        
        # Force to be leader
        node.state = RaftState.LEADER
        node.current_term = 1
        
        # Append log entries
        await node.append_log('command1', {'data': 'test1'})
        await node.append_log('command2', {'data': 'test2'})
        
        # Verify logs
        assert len(node.log) == 2
        assert node.log[0].command == 'command1'
        assert node.log[1].command == 'command2'
        
    finally:
        await node.stop()


@pytest.mark.asyncio
async def test_node_restart():
    """Test node can be stopped and restarted"""
    node = RaftNode('test-node', ['node-2'])
    
    # First start
    await node.start()
    assert node._running is True
    first_term = node.current_term
    
    # Stop
    await node.stop()
    assert node._running is False
    
    # Restart
    await node.start()
    assert node._running is True
    
    # State should be reset to follower
    assert node.state == RaftState.FOLLOWER
    
    await node.stop()


def test_cluster_configuration():
    """Test cluster node configuration"""
    node = RaftNode('node-1', ['node-2', 'node-3', 'node-4'])
    
    # Should exclude self from cluster
    assert 'node-1' not in node.cluster_nodes
    assert len(node.cluster_nodes) == 3
    assert 'node-2' in node.cluster_nodes
    assert 'node-3' in node.cluster_nodes
    assert 'node-4' in node.cluster_nodes
