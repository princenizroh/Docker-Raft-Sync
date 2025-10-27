#!/usr/bin/env python3
"""
Distributed HTTP benchmark for 3-node cluster (locks, queue, cache)

This script uses the ClusterClient (benchmarks/demo_cluster_client.py) to drive HTTP
requests against the cluster HTTP API exposed by the Docker containers
(127.0.0.1:6000, 127.0.0.1:6010, 127.0.0.1:6020 by default).

Usage (from repository root):
  python benchmarks/scenarios/distributed_http_benchmark.py --locks 500 --queue 1000 --cache 500 --concurrency 30

Outputs:
 - JSON results saved to benchmarks/scenarios/distributed_http_benchmark_results.json
 - Prints brief summary and key percentiles

Notes:
 - Ensure the Docker cluster is running and all 3 nodes respond on /status.
 - This script is an HTTP client only (does not start any Raft node).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure repository root is importable when running from project root.
# This import expects `benchmarks/demo_cluster_client.py` to exist.
#
# We'll try multiple robust import fallbacks:
# 1. Normal package import `benchmarks.demo_cluster_client`
# 2. Load the module by file path (benchmarks/demo_cluster_client.py) using importlib
# 3. As a last resort, add a likely repo root to sys.path and retry the package import
try:
    from benchmarks.demo_cluster_client import ClusterClient
except Exception:
    # Fallback 1: try to load module by its file location relative to this file.
    demo_path = (
        Path(__file__).resolve().parents[2] / "benchmarks" / "demo_cluster_client.py"
    )
    if demo_path.exists():
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "demo_cluster_client", str(demo_path)
        )
        module = importlib.util.module_from_spec(spec)
        loader = spec.loader
        assert loader is not None
        loader.exec_module(module)
        ClusterClient = getattr(module, "ClusterClient")
    else:
        # Fallback 2: try to add repository root (two levels up) to sys.path and import again
        repo_root = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(repo_root))
        try:
            from benchmarks.demo_cluster_client import ClusterClient  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "Failed to import ClusterClient from benchmarks/demo_cluster_client.py. "
                "Make sure you run this from the repository root and the file exists. "
                f"Original error: {e}"
            )

OUT_FILE = Path("benchmarks/scenarios/distributed_http_benchmark_results.json")
OUT_DIR = OUT_FILE.parent
OUT_DIR.mkdir(parents=True, exist_ok=True)


def now_ns() -> int:
    return time.perf_counter_ns()


async def run_lock_test(
    client: ClusterClient,
    num_ops: int = 1000,
    concurrency: int = 50,
    resource_pool: int = 100,
) -> Dict[str, Any]:
    """
    Run concurrent acquire/release exclusive locks via HTTP API using ClusterClient.
    Measures per-operation latency (ms) and success count.
    """
    sem = asyncio.Semaphore(concurrency)
    latencies: List[float] = []
    successes = 0

    async def worker(i: int):
        nonlocal successes
        resource = f"res-{i % resource_pool}"
        client_id = f"bench-lock-{i}"
        async with sem:
            t0 = now_ns()
            ok = await client.acquire_lock(resource, client_id, lock_type="EXCLUSIVE")
            t1 = now_ns()
            lat_ms = (t1 - t0) / 1e6
            latencies.append(lat_ms)
            if ok:
                successes += 1
                # release immediately (best-effort)
                await client.release_lock(resource, client_id)

    tasks = [asyncio.create_task(worker(i)) for i in range(num_ops)]
    t_start = time.perf_counter()
    await asyncio.gather(*tasks)
    duration = time.perf_counter() - t_start

    res = {
        "operation": "distributed_locks",
        "total_ops": num_ops,
        "successful_ops": successes,
        "success_rate_percent": (successes / num_ops * 100.0) if num_ops > 0 else 0.0,
        "duration_seconds": duration,
        "throughput_ops_per_sec": (num_ops / duration) if duration > 0 else 0.0,
        "avg_latency_ms": statistics.mean(latencies) if latencies else 0.0,
        "p50_latency_ms": statistics.median(latencies) if latencies else 0.0,
        "p95_latency_ms": (
            statistics.quantiles(latencies, n=20)[18] if len(latencies) > 20 else 0.0
        ),
        "p99_latency_ms": (
            statistics.quantiles(latencies, n=100)[98] if len(latencies) > 100 else 0.0
        ),
        "raw_latencies_ms_sample": latencies[:200],
    }
    return res


async def run_queue_test(
    client: ClusterClient, num_messages: int = 1000, concurrency: int = 50
) -> Dict[str, Any]:
    """
    Enqueue then dequeue messages through HTTP API. Measures enqueue/dequeue latencies.
    Uses simple polling for dequeue operations.
    """
    enqueue_lats: List[float] = []
    dequeue_lats: List[float] = []
    enqueued = 0
    dequeued = 0
    topic = "bench-http-topic"

    enqueue_sem = asyncio.Semaphore(concurrency)

    async def enqueue_worker(i: int):
        nonlocal enqueued
        async with enqueue_sem:
            payload = {"id": i, "payload": f"m-{i}"}
            t0 = now_ns()
            ok = await client.enqueue_message(topic, payload)
            t1 = now_ns()
            enqueue_lats.append((t1 - t0) / 1e6)
            if ok:
                enqueued += 1

    # Enqueue phase
    enqueue_tasks = [
        asyncio.create_task(enqueue_worker(i)) for i in range(num_messages)
    ]
    t_start = time.perf_counter()
    await asyncio.gather(*enqueue_tasks)

    # Dequeue phase: poll until we received enqueued messages or timeout
    dequeue_deadline = time.time() + max(30, math.ceil(num_messages / 50))
    while dequeued < enqueued and time.time() < dequeue_deadline:
        t0 = now_ns()
        msg = await client.dequeue_message(
            topic, consumer_id=f"bench-consumer-{dequeued}"
        )
        t1 = now_ns()
        dequeue_lats.append((t1 - t0) / 1e6)
        if msg:
            dequeued += 1
        # small backoff
        await asyncio.sleep(0.001)

    duration = time.perf_counter() - t_start
    enqueue_throughput = (
        enqueued / (sum(enqueue_lats) / 1000.0) if sum(enqueue_lats) > 0 else 0.0
    )
    dequeue_throughput = (
        dequeued / (sum(dequeue_lats) / 1000.0) if sum(dequeue_lats) > 0 else 0.0
    )

    res = {
        "operation": "distributed_queue",
        "messages_requested": num_messages,
        "messages_enqueued": enqueued,
        "messages_dequeued": dequeued,
        "duration_seconds": duration,
        "enqueue_throughput_msg_per_sec": enqueue_throughput,
        "dequeue_throughput_msg_per_sec": dequeue_throughput,
        "avg_enqueue_latency_ms": statistics.mean(enqueue_lats)
        if enqueue_lats
        else 0.0,
        "avg_dequeue_latency_ms": statistics.mean(dequeue_lats)
        if dequeue_lats
        else 0.0,
        "p50_enqueue_latency_ms": (
            statistics.median(enqueue_lats) if enqueue_lats else 0.0
        ),
        "p95_enqueue_latency_ms": (
            statistics.quantiles(enqueue_lats, n=20)[18]
            if len(enqueue_lats) > 20
            else 0.0
        ),
        "p99_enqueue_latency_ms": (
            statistics.quantiles(enqueue_lats, n=100)[98]
            if len(enqueue_lats) > 100
            else 0.0
        ),
        "p50_dequeue_latency_ms": (
            statistics.median(dequeue_lats) if dequeue_lats else 0.0
        ),
        "p95_dequeue_latency_ms": (
            statistics.quantiles(dequeue_lats, n=20)[18]
            if len(dequeue_lats) > 20
            else 0.0
        ),
        "p99_dequeue_latency_ms": (
            statistics.quantiles(dequeue_lats, n=100)[98]
            if len(dequeue_lats) > 100
            else 0.0
        ),
        "enqueue_latencies_ms_sample": enqueue_lats[:200],
        "dequeue_latencies_ms_sample": dequeue_lats[:200],
    }
    return res


async def run_cache_test(
    client: ClusterClient, num_ops: int = 1000, hit_ratio: float = 0.8
) -> Dict[str, Any]:
    """
    PUT a number of keys to prepopulate (hit_ratio portion), then GETs/misses to measure hit rate & latencies.
    """
    put_lats: List[float] = []
    get_lats: List[float] = []
    hits = 0

    # Prepopulate
    prepopulate = int(num_ops * hit_ratio)
    for i in range(prepopulate):
        t0 = now_ns()
        await client.cache_put(f"key-{i}", {"v": f"value-{i}"})
        t1 = now_ns()
        put_lats.append((t1 - t0) / 1e6)
        # tiny pause
        await asyncio.sleep(0.0001)

    # Mixed gets
    for i in range(num_ops):
        if i < prepopulate:
            key = f"key-{i}"
        else:
            key = f"missing-{i}"
        t0 = now_ns()
        val = await client.cache_get(key)
        t1 = now_ns()
        get_lats.append((t1 - t0) / 1e6)
        if val is not None:
            hits += 1
        await asyncio.sleep(0.0001)

    total_gets = len(get_lats)
    hit_rate = (hits / total_gets * 100.0) if total_gets > 0 else 0.0

    res = {
        "operation": "distributed_cache",
        "puts": len(put_lats),
        "gets": total_gets,
        "hit_count": hits,
        "hit_rate_percent": hit_rate,
        "avg_put_latency_ms": statistics.mean(put_lats) if put_lats else 0.0,
        "avg_get_latency_ms": statistics.mean(get_lats) if get_lats else 0.0,
        "p50_get_latency_ms": statistics.median(get_lats) if get_lats else 0.0,
        "p95_get_latency_ms": (
            statistics.quantiles(get_lats, n=20)[18] if len(get_lats) > 20 else 0.0
        ),
        "p99_get_latency_ms": (
            statistics.quantiles(get_lats, n=100)[98] if len(get_lats) > 100 else 0.0
        ),
        "put_latencies_ms_sample": put_lats[:200],
        "get_latencies_ms_sample": get_lats[:200],
    }
    return res


async def ensure_leader_available(client: ClusterClient, timeout: float = 20.0) -> bool:
    """
    Poll cluster status until a leader is discovered or timeout. Returns True if leader found.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status = await client.get_cluster_status()
            if status and status.get("leader"):
                return True
        except Exception:
            pass
        await asyncio.sleep(0.5)
    return False


async def run_all_tests(
    nodes: List[str],
    locks: int,
    queue: int,
    cache: int,
    concurrency: int,
    cache_hit_ratio: float,
):
    results: Dict[str, Any] = {"meta": {"timestamp": time.time(), "nodes": nodes}}

    async with ClusterClient(nodes) as client:
        print("[*] Checking cluster status...")
        status = await client.get_cluster_status()
        print(
            f"    Cluster healthy_nodes={status.get('healthy_nodes')} leader={status.get('leader')}"
        )

        ok = await ensure_leader_available(client, timeout=30.0)
        if not ok:
            print(
                "[!] No leader discovered within timeout; tests may be unstable but proceeding."
            )

        if locks > 0:
            print(f"[*] Running lock benchmark: {locks} ops, concurrency={concurrency}")
            lock_res = await run_lock_test(
                client, num_ops=locks, concurrency=concurrency
            )
            results["locks"] = lock_res
            print(
                f"    Locks: success_rate={lock_res['success_rate_percent']:.2f}% p95={lock_res['p95_latency_ms']:.2f}ms"
            )

        if queue > 0:
            print(
                f"[*] Running queue benchmark: {queue} messages, concurrency={concurrency}"
            )
            queue_res = await run_queue_test(
                client, num_messages=queue, concurrency=concurrency
            )
            results["queue"] = queue_res
            print(
                f"    Queue: enq_throughput={queue_res['enqueue_throughput_msg_per_sec']:.2f} msg/s deq_throughput={queue_res['dequeue_throughput_msg_per_sec']:.2f} msg/s"
            )

        if cache > 0:
            print(
                f"[*] Running cache benchmark: {cache} ops, hit_ratio={cache_hit_ratio:.2f}"
            )
            cache_res = await run_cache_test(
                client, num_ops=cache, hit_ratio=cache_hit_ratio
            )
            results["cache"] = cache_res
            print(
                f"    Cache: hit_rate={cache_res['hit_rate_percent']:.2f}% p95_get={cache_res['p95_get_latency_ms']:.2f}ms"
            )

    # Save results
    try:
        with OUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {OUT_FILE}")
    except Exception as e:
        print(f"[!] Failed to save results: {e}")

    # Print concise summary
    print("\n=== Benchmark Summary ===")
    for key in ("locks", "queue", "cache"):
        if key in results:
            print(f"-- {key.upper()}:")
            for metric in (
                "throughput_ops_per_sec",
                "enqueue_throughput_msg_per_sec",
                "dequeue_throughput_msg_per_sec",
                "p95_latency_ms",
                "p95_enqueue_latency_ms",
                "p95_dequeue_latency_ms",
                "p95_get_latency_ms",
                "hit_rate_percent",
            ):
                if metric in results[key]:
                    print(f"   {metric}: {results[key][metric]}")
            # show a couple key pctiles if present
            for pkey in ("p50_latency_ms", "p95_latency_ms", "p99_latency_ms"):
                if pkey in results[key]:
                    print(f"   {pkey}: {results[key][pkey]}")
            print("")

    return results


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Distributed HTTP benchmark for 3-node cluster"
    )
    p.add_argument(
        "--nodes",
        nargs="+",
        default=["127.0.0.1:6000", "127.0.0.1:6010", "127.0.0.1:6020"],
        help="HTTP API endpoints for cluster nodes (host:port)",
    )
    p.add_argument("--locks", type=int, default=500, help="number of lock operations")
    p.add_argument("--queue", type=int, default=500, help="number of queue messages")
    p.add_argument("--cache", type=int, default=500, help="number of cache ops")
    p.add_argument(
        "--concurrency",
        type=int,
        default=30,
        help="concurrency for lock/queue enqueues",
    )
    p.add_argument(
        "--cache-hit-ratio",
        type=float,
        default=0.8,
        help="target hit ratio for cache test (0..1)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    try:
        asyncio.run(
            run_all_tests(
                nodes=args.nodes,
                locks=args.locks,
                queue=args.queue,
                cache=args.cache,
                concurrency=args.concurrency,
                cache_hit_ratio=args.cache_hit_ratio,
            )
        )
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    except Exception as e:
        print(f"[!] Fatal error during benchmark: {e}")


if __name__ == "__main__":
    main()
