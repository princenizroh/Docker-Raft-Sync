import pytest
import asyncio
import time
from src.consensus.raft import RaftNode, RaftState


@pytest.mark.asyncio
async def test_log_append_throughput():
    node = RaftNode('perf-node', [])
    
    try:
        await node.start()
        node.state = RaftState.LEADER
        node.current_term = 1
        
        num_operations = 100
        start_time = time.time()
        
        for i in range(num_operations):
            await node.append_log(f'op_{i}', {'data': f'value_{i}'})
        
        duration = time.time() - start_time
        throughput = num_operations / max(duration, 0.001)
        assert throughput > 50, f"Throughput too low: {throughput:.2f} ops/sec"
        assert len(node.log) == num_operations
        
        print(f"\n  Throughput: {throughput:.2f} ops/sec")
        print(f"  Duration: {duration:.3f}s")
        
    finally:
        await node.stop()


@pytest.mark.asyncio
async def test_election_timeout_accuracy():
    node = RaftNode('test-node', ['node-2'], election_timeout_min=100, election_timeout_max=200)
    
    await node.start()
    
    await asyncio.sleep(0.5)
    assert node.state == RaftState.CANDIDATE
    assert node.current_term >= 1
    
    await node.stop()


@pytest.mark.asyncio
async def test_concurrent_log_appends():
    node = RaftNode('perf-node', [])
    
    try:
        await node.start()
        node.state = RaftState.LEADER
        node.current_term = 1
        
        async def append_batch(start_idx, count):
            for i in range(start_idx, start_idx + count):
                await node.append_log(f'op_{i}', {'data': f'value_{i}'})
        
        start_time = time.time()
        await asyncio.gather(
            append_batch(0, 20),
            append_batch(20, 20),
            append_batch(40, 20),
            append_batch(60, 20),
            append_batch(80, 20)
        )
        duration = time.time() - start_time
        
        throughput = 100 / max(duration, 0.001)  
        
        assert len(node.log) == 100
        assert throughput > 30, f"Concurrent throughput too low: {throughput:.2f} ops/sec"
        
        print(f"\n  Concurrent Throughput: {throughput:.2f} ops/sec")
        print(f"  Duration: {duration:.3f}s")
        
    finally:
        await node.stop()


@pytest.mark.asyncio
async def test_multiple_nodes_startup_time():
    nodes = [
        RaftNode(f'node-{i}', [f'node-{j}' for j in range(5) if j != i])
        for i in range(5)
    ]
    
    try:
        start_time = time.time()
        
        # Start all nodes
        await asyncio.gather(*[node.start() for node in nodes])
        
        startup_duration = time.time() - start_time
        
        # Should start quickly
        assert startup_duration < 1.0, f"Startup took too long: {startup_duration:.3f}s"
        
        # All should be running
        assert all(node._running for node in nodes)
        
        print(f"\n  5-node startup time: {startup_duration:.3f}s")
        
    finally:
        await asyncio.gather(*[node.stop() for node in nodes])


@pytest.mark.asyncio
async def test_log_retrieval_performance():
    node = RaftNode('perf-node', [])
    
    try:
        await node.start()
        node.state = RaftState.LEADER
        node.current_term = 1
        
        for i in range(50):
            await node.append_log(f'op_{i}', {'data': f'value_{i}'})
        
        start_time = time.time()
        for _ in range(1000):
            status = node.get_status()
        duration = time.time() - start_time
        
        ops_per_sec = 1000 / max(duration, 0.001) 
        assert ops_per_sec > 1000, f"Status retrieval too slow: {ops_per_sec:.2f} ops/sec"
        
        print(f"\n  Status retrieval: {ops_per_sec:.2f} ops/sec")
        
    finally:
        await node.stop()


def test_memory_footprint():
    import sys
    
    node = RaftNode('test-node', ['node-2', 'node-3'])
    
    size = sys.getsizeof(node)
    
    assert size < 10000, f"Node size too large: {size} bytes"
    
    print(f"\n  Node object size: {size} bytes")
