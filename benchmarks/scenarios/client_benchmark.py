"""
Client-only benchmark scenarios for measuring system performance
"""

import asyncio
import time
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nodes.lock_manager import DistributedLockManager
from src.nodes.queue_node import DistributedQueue
from src.nodes.cache_node import DistributedCache

class ScenarioResults:
    def __init__(self):
        self.results = {}
        
    def add_metric(self, scenario, metric, value):
        if scenario not in self.results:
            self.results[scenario] = {}
        self.results[scenario][metric] = value
        
    def save_results(self):
        # Save raw data
        with open('benchmark_results_detailed.json', 'w') as f:
            json.dump(self.results, f, indent=2)
            
        # Generate visualizations
        self._create_throughput_comparison()
        self._create_latency_comparison()
        self._create_scalability_graph()
        
    def _create_throughput_comparison(self):
        scenarios = ['Single Node', '3 Nodes', '5 Nodes']
        lock_throughput = [
            self.results.get(f'Lock_{s}', {}).get('throughput', 0) 
            for s in scenarios
        ]
        queue_throughput = [
            self.results.get(f'Queue_{s}', {}).get('throughput', 0) 
            for s in scenarios
        ]
        cache_throughput = [
            self.results.get(f'Cache_{s}', {}).get('throughput', 0) 
            for s in scenarios
        ]
        
        x = np.arange(len(scenarios))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(x - width, lock_throughput, width, label='Lock Operations')
        ax.bar(x, queue_throughput, width, label='Queue Operations')
        ax.bar(x + width, cache_throughput, width, label='Cache Operations')
        
        ax.set_ylabel('Operations per Second')
        ax.set_title('Throughput Comparison Across Scenarios')
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios)
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('throughput_comparison.png')
        plt.close()
        
    def _create_latency_comparison(self):
        scenarios = ['Single Node', '3 Nodes', '5 Nodes']
        metrics = ['p50_latency', 'p95_latency', 'p99_latency']
        
        data = {
            'Lock': [[self.results.get(f'Lock_{s}', {}).get(m, 0) 
                     for s in scenarios] for m in metrics],
            'Queue': [[self.results.get(f'Queue_{s}', {}).get(m, 0) 
                      for s in scenarios] for m in metrics],
            'Cache': [[self.results.get(f'Cache_{s}', {}).get(m, 0) 
                      for s in scenarios] for m in metrics]
        }
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        for idx, (component, latencies) in enumerate(data.items()):
            ax = [ax1, ax2, ax3][idx]
            x = np.arange(len(scenarios))
            width = 0.25
            
            ax.bar(x - width, latencies[0], width, label='P50')
            ax.bar(x, latencies[1], width, label='P95')
            ax.bar(x + width, latencies[2], width, label='P99')
            
            ax.set_title(f'{component} Latency')
            ax.set_xlabel('Scenario')
            ax.set_ylabel('Latency (ms)')
            ax.set_xticks(x)
            ax.set_xticklabels(scenarios, rotation=45)
            ax.legend()
        
        plt.tight_layout()
        plt.savefig('latency_comparison.png')
        plt.close()
        
    def _create_scalability_graph(self):
        nodes = [1, 3, 5]
        throughputs = {
            'Lock': [self.results.get(f'Lock_{n} Nodes', {}).get('throughput', 0) 
                    for n in [1, 3, 5]],
            'Queue': [self.results.get(f'Queue_{n} Nodes', {}).get('throughput', 0) 
                     for n in [1, 3, 5]],
            'Cache': [self.results.get(f'Cache_{n} Nodes', {}).get('throughput', 0) 
                     for n in [1, 3, 5]]
        }
        
        plt.figure(figsize=(10, 6))
        for component, data in throughputs.items():
            plt.plot(nodes, data, marker='o', label=component)
            
        plt.xlabel('Number of Nodes')
        plt.ylabel('Operations per Second')
        plt.title('System Scalability')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('scalability_graph.png')
        plt.close()

class BenchmarkClient:
    def __init__(self, client_id, node_address):
        self.client_id = client_id
        self.node_address = node_address
        host, port = node_address.split(':')
        self.host = host
        self.port = int(port)
        self.client_port = self.port + 1000  # Use different port range for clients
        
    async def create_lock_manager(self):
        manager = DistributedLockManager(
            node_id=f"benchmark-client-{self.client_id}",
            host='0.0.0.0',  # Bind to all interfaces
            port=self.client_port,
            cluster_nodes=[self.node_address]
        )
        await manager.start()
        return manager
        
    async def create_queue(self):
        queue = DistributedQueue(
            node_id=f"benchmark-client-{self.client_id}",
            host='0.0.0.0',
            port=self.client_port,
            cluster_nodes=[self.node_address]
        )
        await queue.start()
        return queue
        
    async def create_cache(self):
        cache = DistributedCache(
            node_id=f"benchmark-client-{self.client_id}",
            host='0.0.0.0',
            port=self.client_port,
            cluster_nodes=[self.node_address]
        )
        await cache.start()
        return cache

async def run_lock_benchmark(client, num_ops=1000):
    try:
        lock_manager = await client.create_lock_manager()
        print("Starting lock operations...")
        
        start_time = time.time()
        latencies = []
        
        for i in range(num_ops):
            resource_id = f'resource-{i % 100}'
            requester_id = f'requester-{client.client_id}-{i}'
            
            start_op = time.time()
            lock_id = await lock_manager.acquire_lock(resource_id, requester_id, timeout=5.0)
            if lock_id:
                latency = (time.time() - start_op) * 1000
                latencies.append(latency)
                await lock_manager.release_lock(lock_id)
                if i % 100 == 0:
                    print(f"Completed {i}/{num_ops} lock operations...")
        
        duration = time.time() - start_time
        
        if not latencies:
            return {
                'throughput': 0,
                'p50_latency': 0,
                'p95_latency': 0,
                'p99_latency': 0,
                'success_rate': 0
            }
            
        return {
            'throughput': num_ops / duration if duration > 0 else 0,
            'p50_latency': np.percentile(latencies, 50) if latencies else 0,
            'p95_latency': np.percentile(latencies, 95) if latencies else 0,
            'p99_latency': np.percentile(latencies, 99) if latencies else 0,
            'success_rate': (len(latencies) / num_ops) * 100
        }
    finally:
        await lock_manager.stop()

async def run_queue_benchmark(client, num_messages=10000):
    try:
        queue = await client.create_queue()
        print("Starting queue operations...")
        
        # Enqueue
        start_time = time.time()
        enqueue_latencies = []
        
        for i in range(num_messages):
            start_op = time.time()
            await queue.enqueue('test', f'msg-{i}')
            enqueue_latencies.append((time.time() - start_op) * 1000)
            if i % 1000 == 0:
                print(f"Enqueued {i}/{num_messages} messages...")
        
        # Dequeue
        dequeue_latencies = []
        received = 0
        
        print("Starting dequeue operations...")
        while received < num_messages:
            start_op = time.time()
            msg = await queue.dequeue('test')
            if msg:
                dequeue_latencies.append((time.time() - start_op) * 1000)
                received += 1
                if received % 1000 == 0:
                    print(f"Dequeued {received}/{num_messages} messages...")
        
        duration = time.time() - start_time
        
        if not enqueue_latencies or not dequeue_latencies:
            return {
                'throughput': 0,
                'p50_latency': 0,
                'p95_latency': 0,
                'p99_latency': 0,
                'message_loss': 100
            }
        
        all_latencies = enqueue_latencies + dequeue_latencies
        return {
            'throughput': (num_messages * 2) / duration if duration > 0 else 0,
            'p50_latency': np.percentile(all_latencies, 50),
            'p95_latency': np.percentile(all_latencies, 95),
            'p99_latency': np.percentile(all_latencies, 99),
            'message_loss': ((num_messages - received) / num_messages) * 100
        }
    finally:
        await queue.stop()

async def run_cache_benchmark(client, num_ops=5000):
    try:
        cache = await client.create_cache()
        print("Starting cache operations...")
        
        start_time = time.time()
        latencies = []
        hits = 0
        
        # Mix of operations: 40% write, 60% read
        for i in range(num_ops):
            is_write = i % 100 < 40
            key = f'key-{i % 1000}'
            
            start_op = time.time()
            if is_write:
                await cache.put(key, f'value-{i}')
            else:
                value = await cache.get(key)
                if value is not None:
                    hits += 1
                    
            latencies.append((time.time() - start_op) * 1000)
            
            if i % 1000 == 0:
                print(f"Completed {i}/{num_ops} cache operations...")
        
        duration = time.time() - start_time
        read_ops = num_ops * 0.6
        
        if not latencies:
            return {
                'throughput': 0,
                'p50_latency': 0,
                'p95_latency': 0,
                'p99_latency': 0,
                'hit_rate': 0
            }
        
        return {
            'throughput': num_ops / duration if duration > 0 else 0,
            'p50_latency': np.percentile(latencies, 50),
            'p95_latency': np.percentile(latencies, 95),
            'p99_latency': np.percentile(latencies, 99),
            'hit_rate': (hits / read_ops) * 100 if read_ops > 0 else 0
        }
    finally:
        await cache.stop()

async def main():
    results = ScenarioResults()
    
    # Test scenarios with Docker container addresses
    scenarios = [
        ('Single Node', ['dist-node-1:6000']),
        ('3 Nodes', ['dist-node-1:6000', 'dist-node-2:6010', 'dist-node-3:6020']),
        ('5 Nodes', ['dist-node-1:6000', 'dist-node-2:6010', 'dist-node-3:6020',
                    'dist-node-4:6030', 'dist-node-5:6040'])
    ]
    
    for scenario_name, nodes in scenarios:
        print(f"\nRunning {scenario_name} scenario...")
        client = BenchmarkClient('client-1', nodes[0])
        
        # Run component benchmarks
        lock_results = await run_lock_benchmark(client)
        results.add_metric(f'Lock_{scenario_name}', 'throughput', lock_results['throughput'])
        results.add_metric(f'Lock_{scenario_name}', 'p50_latency', lock_results['p50_latency'])
        results.add_metric(f'Lock_{scenario_name}', 'p95_latency', lock_results['p95_latency'])
        results.add_metric(f'Lock_{scenario_name}', 'p99_latency', lock_results['p99_latency'])
        
        queue_results = await run_queue_benchmark(client)
        results.add_metric(f'Queue_{scenario_name}', 'throughput', queue_results['throughput'])
        results.add_metric(f'Queue_{scenario_name}', 'p50_latency', queue_results['p50_latency'])
        results.add_metric(f'Queue_{scenario_name}', 'p95_latency', queue_results['p95_latency'])
        results.add_metric(f'Queue_{scenario_name}', 'p99_latency', queue_results['p99_latency'])
        
        cache_results = await run_cache_benchmark(client)
        results.add_metric(f'Cache_{scenario_name}', 'throughput', cache_results['throughput'])
        results.add_metric(f'Cache_{scenario_name}', 'p50_latency', cache_results['p50_latency'])
        results.add_metric(f'Cache_{scenario_name}', 'p95_latency', cache_results['p95_latency'])
        results.add_metric(f'Cache_{scenario_name}', 'p99_latency', cache_results['p99_latency'])
        
        print(f"Completed {scenario_name} benchmarks:")
        print(f"Lock Throughput: {lock_results['throughput']:.2f} ops/sec")
        print(f"Queue Throughput: {queue_results['throughput']:.2f} ops/sec")
        print(f"Cache Throughput: {cache_results['throughput']:.2f} ops/sec")
    
    # Save results and generate visualizations
    results.save_results()
    print("\nBenchmark complete! Results and visualizations have been saved.")

if __name__ == '__main__':
    asyncio.run(main())