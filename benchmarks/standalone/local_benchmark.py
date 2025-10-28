#!/usr/bin/env python3
"""
Tugas-individu/benchmarks/local_benchmark.py

Benchmark lokal untuk standalone mode (tidak bergabung ke cluster).
Menguji 3 primitive:
 - Distributed Lock Manager
 - Distributed Queue
 - Distributed Cache

Fitur:
 - Mengukur throughput, latency, dan statistik percentil (p50, p95, p99)
 - Menyimpan hasil JSON ke file
 - Menghasilkan plot PNG (jika matplotlib tersedia)

Cara pakai:
  python benchmarks/local_benchmark.py --locks 1000 --queue 2000 --cache 1000

Catatan:
 - Script ini menjalankan setiap node dalam mode standalone (cluster_nodes = []).
 - Pastikan dependencies terinstall (`pip install -r requirements.txt`) termasuk matplotlib.
 - Jika paket tidak tersedia, script akan tetap berjalan dan hanya menyimpan JSON tanpa plotting.
"""

import asyncio
import time
import json
import statistics
import math
import argparse
from pathlib import Path
import sys

# Tambahkan project root ke sys.path agar import 'src' bekerja saat script dijalankan dari folder project
proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from typing import List, Dict, Any

# Import komponen sistem (harus bisa diimport saat menjalankan dari root repo)
try:
    from src.nodes.lock_manager import DistributedLockManager, LockType
    from src.nodes.queue_node import DistributedQueue, QueueMessage
    from src.nodes.cache_node import DistributedCache
except Exception as e:
    raise RuntimeError(
        "Gagal mengimpor modul project. Pastikan Anda menjalankan script ini dari root repository "
        "dan dependencies sudah terpasang. Error: {}".format(e)
    )

# Optional plotting
try:
    import matplotlib.pyplot as plt  # type: ignore

    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False


OUT_DIR = Path("benchmarks")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def percentile(data: List[float], p: float) -> float:
    """Hitung percentile p (0-100) pada list data (menggunakan interpolasi linear)."""
    if not data:
        return 0.0
    s = sorted(data)
    k = (len(s) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    d0 = s[f] * (c - k)
    d1 = s[c] * (k - f)
    return d0 + d1


async def benchmark_locks(num_ops: int = 1000) -> Dict[str, Any]:
    """Benchmark acquire/release exclusive locks repeatedly."""
    node = DistributedLockManager("bench-lock", "127.0.0.1", 7000, [])
    results: Dict[str, Any] = {}
    latencies: List[float] = []
    successes = 0

    await node.start()
    await asyncio.sleep(0.5)  # stabilization

    try:
        start_all = time.monotonic()
        for i in range(num_ops):
            resource = f"res-{i % 100}"  # reuse some resources to create contention
            t0 = time.monotonic()
            try:
                ok = await node.acquire_lock(
                    resource, f"client-{i}", LockType.EXCLUSIVE, timeout=5.0
                )
            except Exception:
                ok = False
            t1 = time.monotonic()
            lat_ms = (t1 - t0) * 1000.0
            latencies.append(lat_ms)
            if ok:
                successes += 1
                # release immediately
                try:
                    await node.release_lock(resource, f"client-{i}")
                except Exception:
                    pass
            # light throttle to avoid busy loop
            await asyncio.sleep(0.0005)
        duration = time.monotonic() - start_all
    finally:
        await node.stop()

    throughput = num_ops / duration if duration > 0 else 0.0
    results["operation"] = "locks_exclusive_acquire_release"
    results["total_ops"] = num_ops
    results["successful_ops"] = successes
    results["duration_seconds"] = duration
    results["throughput_ops_per_sec"] = throughput
    results["avg_latency_ms"] = statistics.mean(latencies) if latencies else 0.0
    results["p50_latency_ms"] = percentile(latencies, 50)
    results["p95_latency_ms"] = percentile(latencies, 95)
    results["p99_latency_ms"] = percentile(latencies, 99)
    results["latencies_ms"] = latencies  # raw for plotting if desired

    return results


async def benchmark_queue(
    num_messages: int = 1000, partition_count: int = 16
) -> Dict[str, Any]:
    """Benchmark enqueue and dequeue operations."""
    node = DistributedQueue(
        "bench-queue", "127.0.0.1", 7100, [], partition_count=partition_count
    )
    results: Dict[str, Any] = {}
    enqueue_lat: List[float] = []
    dequeue_lat: List[float] = []
    enqueued = 0
    dequeued = 0

    await node.start()
    await asyncio.sleep(0.5)

    topic = "bench-topic"

    try:
        # Enqueue
        t_start = time.monotonic()
        for i in range(num_messages):
            msg = {"id": i, "payload": f"message-{i}"}
            t0 = time.monotonic()
            try:
                ok = await node.enqueue(topic, msg)
            except Exception:
                ok = False
            t1 = time.monotonic()
            enqueue_lat.append((t1 - t0) * 1000.0)
            if ok:
                enqueued += 1
            await asyncio.sleep(0.0002)
        enqueue_duration = time.monotonic() - t_start

        # Dequeue
        # Try to dequeue up to enqueued
        t_start = time.monotonic()
        attempts = 0
        while dequeued < enqueued and attempts < enqueued * 3:
            t0 = time.monotonic()
            try:
                msg = await node.dequeue(topic, f"consumer-{attempts % 10}")
            except Exception:
                msg = None
            t1 = time.monotonic()
            dequeue_lat.append((t1 - t0) * 1000.0)
            if msg:
                dequeued += 1
                # acknowledge if possible; some API variants may take (message_id) signature
                try:
                    # message might be QueueMessage object or dict
                    if isinstance(msg, QueueMessage):
                        mid = msg.message_id
                        await node.acknowledge(mid, f"consumer-{attempts % 10}")
                    else:
                        # try dict
                        mid = msg.get("message_id") or msg.get("id")
                        await node.acknowledge(mid, f"consumer-{attempts % 10}")
                except Exception:
                    pass
            attempts += 1
            await asyncio.sleep(0.0005)
        dequeue_duration = time.monotonic() - t_start

    finally:
        await node.stop()

    results["operation"] = "queue_enqueue_dequeue"
    results["messages_requested"] = num_messages
    results["messages_enqueued"] = enqueued
    results["messages_dequeued"] = dequeued
    results["enqueue_duration_seconds"] = enqueue_duration
    results["dequeue_duration_seconds"] = dequeue_duration
    results["enqueue_throughput_msg_per_sec"] = (
        enqueued / enqueue_duration if enqueue_duration > 0 else 0.0
    )
    results["dequeue_throughput_msg_per_sec"] = (
        dequeued / dequeue_duration if dequeue_duration > 0 else 0.0
    )
    results["avg_enqueue_latency_ms"] = (
        statistics.mean(enqueue_lat) if enqueue_lat else 0.0
    )
    results["avg_dequeue_latency_ms"] = (
        statistics.mean(dequeue_lat) if dequeue_lat else 0.0
    )
    results["p50_enqueue_latency_ms"] = percentile(enqueue_lat, 50)
    results["p95_enqueue_latency_ms"] = percentile(enqueue_lat, 95)
    results["p99_enqueue_latency_ms"] = percentile(enqueue_lat, 99)
    results["p50_dequeue_latency_ms"] = percentile(dequeue_lat, 50)
    results["p95_dequeue_latency_ms"] = percentile(dequeue_lat, 95)
    results["p99_dequeue_latency_ms"] = percentile(dequeue_lat, 99)
    results["enqueue_latencies_ms"] = enqueue_lat
    results["dequeue_latencies_ms"] = dequeue_lat

    return results


async def benchmark_cache(
    num_ops: int = 1000, hit_ratio: float = 0.8
) -> Dict[str, Any]:
    """Benchmark cache put/get with a configurable hit ratio."""
    node = DistributedCache("bench-cache", "127.0.0.1", 7200, [], cache_size_mb=16)
    results: Dict[str, Any] = {}
    put_lat: List[float] = []
    get_lat: List[float] = []
    hits = 0

    await node.start()
    await asyncio.sleep(0.5)

    # Pre-populate some keys to control hit ratio
    prepopulate = int(num_ops * hit_ratio)
    try:
        for i in range(prepopulate):
            key = f"key-{i}"
            val = f"value-{i}"
            t0 = time.monotonic()
            try:
                await node.put(key, val)
            except Exception:
                pass
            t1 = time.monotonic()
            put_lat.append((t1 - t0) * 1000.0)
            await asyncio.sleep(0.0002)

        # Perform gets: some hits and some misses
        for i in range(num_ops):
            if i < prepopulate:
                key = f"key-{i}"
            else:
                key = f"missing-{i}"
            t0 = time.monotonic()
            try:
                val = await node.get(key)
            except Exception:
                val = None
            t1 = time.monotonic()
            get_lat.append((t1 - t0) * 1000.0)
            if val is not None:
                hits += 1
            await asyncio.sleep(0.0002)

    finally:
        await node.stop()

    total_puts = len(put_lat)
    total_gets = len(get_lat)
    results["operation"] = "cache_put_get"
    results["puts"] = total_puts
    results["gets"] = total_gets
    results["hit_count"] = hits
    results["hit_rate_percent"] = (hits / total_gets * 100.0) if total_gets > 0 else 0.0
    results["avg_put_latency_ms"] = statistics.mean(put_lat) if put_lat else 0.0
    results["avg_get_latency_ms"] = statistics.mean(get_lat) if get_lat else 0.0
    results["p50_get_latency_ms"] = percentile(get_lat, 50)
    results["p95_get_latency_ms"] = percentile(get_lat, 95)
    results["p99_get_latency_ms"] = percentile(get_lat, 99)
    results["put_latencies_ms"] = put_lat
    results["get_latencies_ms"] = get_lat

    return results


def save_json(results: Dict[str, Any], filename: Path):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {filename}")
    except Exception as e:
        print(f"[!] Gagal menyimpan JSON results: {e}")


def plot_results(results: Dict[str, Any], out_prefix: Path):
    if not MATPLOTLIB_AVAILABLE:
        print("[!] matplotlib tidak tersedia — melewatkan plotting.")
        return

    # Locks plot
    if results.get("locks"):
        r = results["locks"]
        lats = r.get("latencies_ms", [])
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        axs[0].hist(lats, bins=50, color="C0", alpha=0.7)
        axs[0].set_title("Latency Histogram - Locks (ms)")
        axs[0].set_xlabel("Latency (ms)")
        axs[0].set_ylabel("Count")
        axs[1].boxplot(lats, vert=False)
        axs[1].set_title("Latency Boxplot - Locks")
        plt.suptitle("Locks Benchmark")
        p = out_prefix / "locks_latency.png"
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(p)
        plt.close(fig)
        print(f"[+] Locks plot saved to {p}")

    # Queue plot (enqueue & dequeue histograms)
    if results.get("queue"):
        r = results["queue"]
        enq = r.get("enqueue_latencies_ms", [])
        deq = r.get("dequeue_latencies_ms", [])
        fig, axs = plt.subplots(2, 1, figsize=(8, 8))
        axs[0].hist(enq, bins=50, color="C1", alpha=0.7)
        axs[0].set_title("Enqueue Latency Histogram (ms)")
        axs[0].set_xlabel("Latency (ms)")
        axs[1].hist(deq, bins=50, color="C2", alpha=0.7)
        axs[1].set_title("Dequeue Latency Histogram (ms)")
        axs[1].set_xlabel("Latency (ms)")
        plt.suptitle("Queue Benchmark")
        p = out_prefix / "queue_latency.png"
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(p)
        plt.close(fig)
        print(f"[+] Queue plot saved to {p}")

    # Cache plot
    if results.get("cache"):
        r = results["cache"]
        gets = r.get("get_latencies_ms", [])
        puts = r.get("put_latencies_ms", [])
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        axs[0].hist(gets, bins=50, color="C3", alpha=0.7)
        axs[0].set_title("GET Latency Histogram (ms)")
        axs[0].set_xlabel("Latency (ms)")
        axs[1].hist(puts, bins=50, color="C4", alpha=0.7)
        axs[1].set_title("PUT Latency Histogram (ms)")
        axs[1].set_xlabel("Latency (ms)")
        plt.suptitle("Cache Benchmark")
        p = out_prefix / "cache_latency.png"
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        fig.savefig(p)
        plt.close(fig)
        print(f"[+] Cache plot saved to {p}")


async def run_all(locks_ops: int, queue_msgs: int, cache_ops: int):
    summary: Dict[str, Any] = {"meta": {"timestamp": time.time()}}
    if locks_ops > 0:
        print(f"[=] Running lock benchmark: {locks_ops} ops")
        try:
            res = await benchmark_locks(locks_ops)
            summary["locks"] = res
        except Exception as e:
            print(f"[!] Error benchmark_locks: {e}")
    if queue_msgs > 0:
        print(f"[=] Running queue benchmark: {queue_msgs} messages")
        try:
            res = await benchmark_queue(queue_msgs)
            summary["queue"] = res
        except Exception as e:
            print(f"[!] Error benchmark_queue: {e}")
    if cache_ops > 0:
        print(f"[=] Running cache benchmark: {cache_ops} ops")
        try:
            res = await benchmark_cache(cache_ops)
            summary["cache"] = res
        except Exception as e:
            print(f"[!] Error benchmark_cache: {e}")

    # Save JSON
    out_json = OUT_DIR / "local_benchmark_results.json"
    save_json(summary, out_json)

    # Plot
    plot_results(summary, OUT_DIR)

    # Print brief summary
    print("\n=== Benchmark Summary ===")
    for k, v in summary.items():
        if k == "meta":
            continue
        print(f"-- {k.upper()}:")
        print(f"   op: {v.get('operation')}")
        if "throughput_ops_per_sec" in v:
            print(f"   throughput: {v.get('throughput_ops_per_sec'):.2f} ops/sec")
        if "enqueue_throughput_msg_per_sec" in v:
            print(
                f"   enqueue throughput: {v.get('enqueue_throughput_msg_per_sec'):.2f} msg/sec"
            )
        if "dequeue_throughput_msg_per_sec" in v:
            print(
                f"   dequeue throughput: {v.get('dequeue_throughput_msg_per_sec'):.2f} msg/sec"
            )
        if "hit_rate_percent" in v:
            print(f"   hit rate: {v.get('hit_rate_percent'):.2f}%")
        print()

    print(f"[+] Results saved: {out_json}")
    if MATPLOTLIB_AVAILABLE:
        print(f"[+] Plots saved in {OUT_DIR}")


def parse_args():
    p = argparse.ArgumentParser(
        description="Local benchmark for standalone lock/queue/cache"
    )
    p.add_argument(
        "--locks", type=int, default=1000, help="number of lock acquire/release ops"
    )
    p.add_argument(
        "--queue",
        type=int,
        default=1000,
        help="number of queue messages to enqueue/dequeue",
    )
    p.add_argument(
        "--cache",
        type=int,
        default=1000,
        help="number of cache get/put ops (get includes hits/misses)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    try:
        asyncio.run(run_all(args.locks, args.queue, args.cache))
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    except Exception as e:
        print(f"[!] Fatal error: {e}")


if __name__ == "__main__":
    main()
