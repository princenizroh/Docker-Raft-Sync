"""
Performance Benchmarking Tool
Mengukur throughput, latency, dan scalability sistem
"""

import asyncio
import time
import statistics
import json
from typing import List, Dict, Any
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.consensus.raft import RaftNode, RaftState
from src.nodes.lock_manager import DistributedLockManager, LockType
from src.nodes.queue_node import DistributedQueue
from src.nodes.cache_node import DistributedCache
from src.utils.config import NodeConfig


class BenchmarkResults:
    """Store and display benchmark results"""
    
    def __init__(self):
        self.results = {}
    
    def add_result(self, category: str, metric: str, value: Any):
        """Add a benchmark result"""
        if category not in self.results:
            self.results[category] = {}
        self.results[category][metric] = value
    
    def display(self):
        """Display results in formatted table"""
        print("\n" + "="*70)
        print("  PERFORMANCE BENCHMARK RESULTS")
        print("="*70 + "\n")
        
        for category, metrics in self.results.items():
            print(f"[X][X] {category}")
            print("-" * 70)
            for metric, value in metrics.items():
                if isinstance(value, float):
                    print(f"  {metric:.<50} {value:.2f}")
                else:
                    print(f"  {metric:.<50} {value}")
            print()
    
    def save_json(self, filepath: str):
        """Save results to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"[X] Results saved to {filepath}")


async def benchmark_raft_consensus(results: BenchmarkResults, num_operations: int = 1000):
    """Benchmark Raft consensus operations"""
    print("\n[X][X] Benchmarking Raft Consensus...")
    
    # Setup cluster
    nodes = [
        RaftNode('node-1', ['node-2', 'node-3']),
        RaftNode('node-2', ['node-1', 'node-3']),
        RaftNode('node-3', ['node-1', 'node-2'])
    ]
    
    try:
        # Start nodes
        for node in nodes:
            await node.start()
        
        # Wait for leader election
        await asyncio.sleep(2)
        
        # Find leader
        leader = None
        for node in nodes:
            if node.state == RaftState.LEADER:
                leader = node
                break
        
        if not leader:
            print("  [X] No leader elected")
            return
        
        # Benchmark log replication
        print(f"  Testing {num_operations} log entries...")
        start_time = time.time()
        
        for i in range(num_operations):
            entry = {'operation': 'set', 'key': f'key-{i}', 'value': f'value-{i}'}
            await leader.append_entries([entry])
        
        duration = time.time() - start_time
        throughput = num_operations / duration
        avg_latency = (duration / num_operations) * 1000  # ms
        
        results.add_result('Raft Consensus', 'Operations', num_operations)
        results.add_result('Raft Consensus', 'Duration (seconds)', duration)
        results.add_result('Raft Consensus', 'Throughput (ops/sec)', throughput)
        results.add_result('Raft Consensus', 'Avg Latency (ms)', avg_latency)
        results.add_result('Raft Consensus', 'Leader', leader.node_id)
        results.add_result('Raft Consensus', 'Cluster Size', len(nodes))
        
        print(f"  [X] Throughput: {throughput:.2f} ops/sec")
        print(f"  [X] Avg Latency: {avg_latency:.2f} ms")
        
    finally:
        # Cleanup
        for node in nodes:
            await node.stop()


async def benchmark_distributed_locks(results: BenchmarkResults, num_operations: int = 500):
    """Benchmark distributed lock operations"""
    print("\n[X][X] Benchmarking Distributed Locks...")
    
    config = NodeConfig(
        node_id='lock-node-1',
        host='localhost',
        port=8000,
        cluster_nodes=['lock-node-2', 'lock-node-3']
    )
    
    lock_manager = DistributedLockManager(config)
    
    try:
        await lock_manager.start()
        await asyncio.sleep(1)  # Wait for initialization
        
        # Benchmark exclusive locks
        print(f"  Testing {num_operations} lock acquisitions...")
        latencies = []
        
        for i in range(num_operations):
            resource_id = f'resource-{i % 100}'  # Reuse 100 resources
            
            start = time.time()
            lock_id = await lock_manager.acquire_lock(
                resource_id=resource_id,
                lock_type=LockType.EXCLUSIVE,
                timeout=5.0
            )
            latency = (time.time() - start) * 1000  # ms
            
            if lock_id:
                latencies.append(latency)
                await lock_manager.release_lock(lock_id)
        
        # Calculate statistics
        successful_ops = len(latencies)
        success_rate = (successful_ops / num_operations) * 100
        avg_latency = statistics.mean(latencies) if latencies else 0
        p50_latency = statistics.median(latencies) if latencies else 0
        p95_latency = statistics.quantiles(latencies, n=20)[18] if len(latencies) > 20 else 0
        p99_latency = statistics.quantiles(latencies, n=100)[98] if len(latencies) > 100 else 0
        
        results.add_result('Distributed Locks', 'Total Operations', num_operations)
        results.add_result('Distributed Locks', 'Successful Operations', successful_ops)
        results.add_result('Distributed Locks', 'Success Rate (%)', success_rate)
        results.add_result('Distributed Locks', 'Avg Latency (ms)', avg_latency)
        results.add_result('Distributed Locks', 'P50 Latency (ms)', p50_latency)
        results.add_result('Distributed Locks', 'P95 Latency (ms)', p95_latency)
        results.add_result('Distributed Locks', 'P99 Latency (ms)', p99_latency)
        
        print(f"  [X] Success Rate: {success_rate:.1f}%")
        print(f"  [X] P95 Latency: {p95_latency:.2f} ms")
        
    finally:
        await lock_manager.stop()


async def benchmark_distributed_queue(results: BenchmarkResults, num_messages: int = 1000):
    """Benchmark distributed queue operations"""
    print("\n[X][X] Benchmarking Distributed Queue...")
    
    config = NodeConfig(
        node_id='queue-node-1',
        host='localhost',
        port=8100,
        cluster_nodes=['queue-node-2', 'queue-node-3']
    )
    
    queue = DistributedQueue(config, num_partitions=8)
    
    try:
        await queue.start()
        await asyncio.sleep(1)
        
        # Benchmark enqueue
        print(f"  Testing {num_messages} enqueue operations...")
        enqueue_start = time.time()
        
        for i in range(num_messages):
            message = {
                'id': i,
                'data': f'message-{i}',
                'timestamp': time.time()
            }
            await queue.enqueue('test-topic', message)
        
        enqueue_duration = time.time() - enqueue_start
        enqueue_throughput = num_messages / enqueue_duration
        
        # Benchmark dequeue
        print(f"  Testing {num_messages} dequeue operations...")
        dequeue_start = time.time()
        dequeued = 0
        
        for _ in range(num_messages):
            msg = await queue.dequeue('test-topic')
            if msg:
                dequeued += 1
                await queue.acknowledge(msg['id'])
        
        dequeue_duration = time.time() - dequeue_start
        dequeue_throughput = dequeued / dequeue_duration if dequeue_duration > 0 else 0
        
        results.add_result('Distributed Queue', 'Messages Enqueued', num_messages)
        results.add_result('Distributed Queue', 'Enqueue Throughput (msg/sec)', enqueue_throughput)
        results.add_result('Distributed Queue', 'Avg Enqueue Latency (ms)', (enqueue_duration / num_messages) * 1000)
        results.add_result('Distributed Queue', 'Messages Dequeued', dequeued)
        results.add_result('Distributed Queue', 'Dequeue Throughput (msg/sec)', dequeue_throughput)
        results.add_result('Distributed Queue', 'Avg Dequeue Latency (ms)', (dequeue_duration / dequeued) * 1000 if dequeued > 0 else 0)
        results.add_result('Distributed Queue', 'Message Loss Rate (%)', ((num_messages - dequeued) / num_messages) * 100)
        
        print(f"  [X] Enqueue: {enqueue_throughput:.2f} msg/sec")
        print(f"  [X] Dequeue: {dequeue_throughput:.2f} msg/sec")
        
    finally:
        await queue.stop()


async def benchmark_distributed_cache(results: BenchmarkResults, num_operations: int = 1000):
    """Benchmark distributed cache operations"""
    print("\n[X][X] Benchmarking Distributed Cache...")
    
    config = NodeConfig(
        node_id='cache-node-1',
        host='localhost',
        port=8200,
        cluster_nodes=['cache-node-2', 'cache-node-3']
    )
    
    cache = DistributedCache(config, max_size=1000)
    
    try:
        await cache.start()
        await asyncio.sleep(1)
        
        # Benchmark PUT operations
        print(f"  Testing {num_operations} PUT operations...")
        put_latencies = []
        
        for i in range(num_operations):
            key = f'key-{i}'
            value = f'value-{i}' * 10  # ~100 bytes per value
            
            start = time.time()
            await cache.put(key, value)
            latency = (time.time() - start) * 1000
            put_latencies.append(latency)
        
        # Benchmark GET operations (with hits and misses)
        print(f"  Testing {num_operations} GET operations...")
        get_latencies = []
        hits = 0
        
        for i in range(num_operations):
            # 80% hits, 20% misses
            key = f'key-{i}' if i < num_operations * 0.8 else f'key-missing-{i}'
            
            start = time.time()
            value = await cache.get(key)
            latency = (time.time() - start) * 1000
            get_latencies.append(latency)
            
            if value is not None:
                hits += 1
        
        # Calculate statistics
        avg_put_latency = statistics.mean(put_latencies)
        avg_get_latency = statistics.mean(get_latencies)
        hit_rate = (hits / num_operations) * 100
        put_throughput = num_operations / (sum(put_latencies) / 1000)
        get_throughput = num_operations / (sum(get_latencies) / 1000)
        
        results.add_result('Distributed Cache', 'PUT Operations', num_operations)
        results.add_result('Distributed Cache', 'PUT Throughput (ops/sec)', put_throughput)
        results.add_result('Distributed Cache', 'Avg PUT Latency (ms)', avg_put_latency)
        results.add_result('Distributed Cache', 'GET Operations', num_operations)
        results.add_result('Distributed Cache', 'GET Throughput (ops/sec)', get_throughput)
        results.add_result('Distributed Cache', 'Avg GET Latency (ms)', avg_get_latency)
        results.add_result('Distributed Cache', 'Cache Hits', hits)
        results.add_result('Distributed Cache', 'Hit Rate (%)', hit_rate)
        results.add_result('Distributed Cache', 'Cache Size', len(cache.cache.cache))
        
        print(f"  [X] Hit Rate: {hit_rate:.1f}%")
        print(f"  [X] GET Throughput: {get_throughput:.2f} ops/sec")
        
    finally:
        await cache.stop()


async def main():
    """Run all benchmarks"""
    print("\n" + "="*70)
    print("  DISTRIBUTED SYSTEM PERFORMANCE BENCHMARK")
    print("="*70)
    
    results = BenchmarkResults()
    
    try:
        # Run only Raft benchmark (others require full cluster setup)
        await benchmark_raft_consensus(results, num_operations=500)
        
        print("\n" + "="*70)
        print("  NOTE: Full benchmarks require running cluster.")
        print("  Use Docker Compose for complete benchmark suite.")
        print("="*70)
        
        # Display and save results
        results.display()
        results.save_json('benchmark_results.json')
        
        print("\n" + "="*70)
        print("  [X] BENCHMARK COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n[X] Benchmark error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())

