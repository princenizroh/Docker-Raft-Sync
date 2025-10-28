import pytest
import asyncio
from src.consensus.raft import RaftNode, RaftState, LogEntry


@pytest.mark.asyncio
async def test_raft_initialization():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"]
    )
    
    assert node.node_id == "node-1"
    assert node.state == RaftState.FOLLOWER
    assert node.current_term == 0
    assert node.voted_for is None
    assert len(node.log) == 0


@pytest.mark.asyncio
async def test_raft_start_stop():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"]
    )
    
    await node.start()
    assert node._running is True
    
    await node.stop()
    assert node._running is False


@pytest.mark.asyncio
async def test_raft_election_timeout():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"],
        election_timeout_min=100,
        election_timeout_max=200
    )
    
    messages_sent = []
    
    async def mock_sender(target, message):
        messages_sent.append((target, message))
    
    node.set_message_sender(mock_sender)
    
    await node.start()
    
    await asyncio.sleep(0.5)
    
    assert node.state == RaftState.CANDIDATE
    assert node.current_term > 0
    assert len(messages_sent) > 0
    
    await node.stop()


@pytest.mark.asyncio
async def test_raft_vote_request():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"]
    )
    
    messages_sent = []
    
    async def mock_sender(target, message):
        messages_sent.append((target, message))
    
    node.set_message_sender(mock_sender)
    
    await node.start()
    
    await node.handle_request_vote({
        'term': 1,
        'candidate_id': 'node-2',
        'last_log_index': 0,
        'last_log_term': 0
    })
    
    assert len(messages_sent) > 0
    vote_response = messages_sent[0][1]
    assert vote_response['type'] == 'vote_response'
    assert vote_response['vote_granted'] is True
    
    await node.stop()


@pytest.mark.asyncio
async def test_raft_log_append():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"]
    )
    
    await node.start()
    
    node.state = RaftState.LEADER
    node.current_term = 1
    
    success = await node.append_log("test_command", {"data": "test"})
    
    assert success is True
    assert len(node.log) == 1
    assert node.log[0].command == "test_command"
    assert node.log[0].term == 1
    
    await node.stop()


def test_raft_status():
    node = RaftNode(
        node_id="node-1",
        cluster_nodes=["node-2", "node-3"]
    )
    
    status = node.get_status()
    
    assert status['node_id'] == "node-1"
    assert status['state'] == RaftState.FOLLOWER.value
    assert status['term'] == 0
    assert status['log_length'] == 0
