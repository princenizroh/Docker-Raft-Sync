#!/usr/bin/env python3
"""
Plot benchmark results produced by distributed_http_benchmark.py

Generates PNG plots for:
 - Locks: success rate, throughput, latency percentiles and histogram
 - Queue: enqueue/dequeue throughput, latency histogram
 - Cache: hit rate, put/get latency distributions
 - (Optional) Comparison single-node vs distributed if you provide a single-node results JSON

Usage:
  python benchmarks/scenarios/plot_benchmark_results.py \
      --input benchmarks/scenarios/distributed_http_benchmark_results.json \
      --single benchmark_results.json \
      --outdir benchmarks/scenarios/plots \
      --show

Outputs:
 - PNG files placed in the output directory with timestamps.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np

# seaborn is optional; fall back gracefully if unavailable
try:
    import seaborn as sns

    sns.set(style="whitegrid")
except Exception:
    sns = None


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_outdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def pct(value: float) -> str:
    return f"{value:.2f}%"


def safe_get(d: Dict, *keys, default=None):
    cur = d
    try:
        for k in keys:
            cur = cur[k]
        return cur
    except Exception:
        return default


def plot_locks(locks: Dict[str, Any], outdir: Path, prefix: str):
    """Plot lock-related metrics"""
    op = locks.get("operation", "locks")
    total = locks.get("total_ops", 0)
    success = locks.get("successful_ops", 0)
    success_rate = locks.get("success_rate_percent", 0.0)
    throughput = locks.get("throughput_ops_per_sec", 0.0)
    avg_latency = locks.get("avg_latency_ms", 0.0)

    p50 = locks.get("p50_latency_ms", 0.0)
    p95 = locks.get("p95_latency_ms", 0.0)
    p99 = locks.get("p99_latency_ms", 0.0)

    lat_sample: List[float] = locks.get("raw_latencies_ms_sample", []) or []

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Summary bar chart: Success rate & throughput
    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax2 = ax1.twinx()

    ax1.bar(["success_rate"], [success_rate], color="#2ca02c", width=0.4)
    ax2.bar(["throughput"], [throughput], color="#1f77b4", alpha=0.6, width=0.4)

    ax1.set_ylabel("Success rate (%)")
    ax2.set_ylabel("Throughput (ops/s)")
    ax1.set_ylim(0, 100)
    ax2.set_ylim(0, max(throughput * 1.2, 1.0))

    ax1.set_title(f"Locks summary - {op} (total={total})")
    file1 = outdir / f"{prefix}_locks_summary_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file1, dpi=150)
    plt.close(fig)

    # Latency histogram + percentiles line
    if lat_sample:
        arr = np.array(lat_sample)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(arr, bins=40, color="#ff7f0e", alpha=0.8)
        ax.set_xlabel("Latency (ms)")
        ax.set_ylabel("Count")
        ax.set_title(f"Lock latencies (sample size={len(arr)})")

        # percentiles
        for q in (50, 95, 99):
            v = np.percentile(arr, q) if len(arr) else 0.0
            ax.axvline(v, linestyle="--", label=f"P{q}={v:.2f}ms")

        ax.legend()
        file2 = outdir / f"{prefix}_locks_latency_hist_{timestamp}.png"
        fig.tight_layout()
        fig.savefig(file2, dpi=150)
        plt.close(fig)
    else:
        file2 = None

    # Print summary to stdout
    print(
        f"[locks] total={total} success={success} success_rate={success_rate:.2f}% throughput={throughput:.2f} ops/s avg_lat={avg_latency:.2f}ms p50={p50} p95={p95} p99={p99}"
    )
    return {"summary_plot": str(file1), "latency_hist": str(file2) if file2 else None}


def plot_queue(queue: Dict[str, Any], outdir: Path, prefix: str):
    """Plot queue metrics"""
    requested = queue.get("messages_requested", 0)
    enq = queue.get("messages_enqueued", 0)
    deq = queue.get("messages_dequeued", 0)
    duration = queue.get("duration_seconds", 0.0)
    enq_throughput = queue.get("enqueue_throughput_msg_per_sec", 0.0)
    deq_throughput = queue.get("dequeue_throughput_msg_per_sec", 0.0)

    enq_lats: List[float] = queue.get("enqueue_latencies_ms_sample", []) or []
    deq_lats: List[float] = queue.get("dequeue_latencies_ms_sample", []) or []

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Bar chart for counts and throughput
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    axs[0].bar(
        ["requested", "enqueued", "dequeued"],
        [requested, enq, deq],
        color=["#7f7f7f", "#2ca02c", "#d62728"],
    )
    axs[0].set_title("Queue counts")
    axs[0].set_ylabel("Messages")

    axs[1].bar(
        ["enq_throughput", "deq_throughput"],
        [enq_throughput, deq_throughput],
        color=["#1f77b4", "#9467bd"],
    )
    axs[1].set_title("Queue throughput (msg/s)")
    file1 = outdir / f"{prefix}_queue_counts_throughput_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file1, dpi=150)
    plt.close(fig)

    # Latency histograms
    file2 = None
    if enq_lats or deq_lats:
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        if enq_lats:
            axs[0].hist(enq_lats, bins=30, color="#1f77b4", alpha=0.8)
            axs[0].set_title(f"Enqueue latencies (n={len(enq_lats)})")
            axs[0].set_xlabel("ms")
        else:
            axs[0].text(0.5, 0.5, "No enqueue samples", ha="center")

        if deq_lats:
            axs[1].hist(deq_lats, bins=30, color="#ff7f0e", alpha=0.8)
            axs[1].set_title(f"Dequeue latencies (n={len(deq_lats)})")
            axs[1].set_xlabel("ms")
        else:
            axs[1].text(0.5, 0.5, "No dequeue samples", ha="center")

        file2 = outdir / f"{prefix}_queue_latency_hist_{timestamp}.png"
        fig.tight_layout()
        fig.savefig(file2, dpi=150)
        plt.close(fig)

    print(
        f"[queue] requested={requested} enqueued={enq} dequeued={deq} enq_throughput={enq_throughput:.2f} deq_throughput={deq_throughput:.2f}"
    )
    return {
        "counts_throughput": str(file1),
        "latency_hist": str(file2) if file2 else None,
    }


def plot_cache(cache: Dict[str, Any], outdir: Path, prefix: str):
    """Plot cache metrics"""
    puts = cache.get("puts", 0)
    gets = cache.get("gets", 0)
    hit_count = cache.get("hit_count", 0)
    hit_rate = cache.get("hit_rate_percent", 0.0)
    avg_put = cache.get("avg_put_latency_ms", 0.0)
    avg_get = cache.get("avg_get_latency_ms", 0.0)

    put_lats: List[float] = cache.get("put_latencies_ms_sample", []) or []
    get_lats: List[float] = cache.get("get_latencies_ms_sample", []) or []

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Hit rate and counts
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(["hit_rate"], [hit_rate], color="#2ca02c")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Hit rate (%)")
    ax.set_title("Cache hit rate")
    file1 = outdir / f"{prefix}_cache_hitrate_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file1, dpi=150)
    plt.close(fig)

    # Latency distributions
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    if put_lats:
        axs[0].hist(put_lats, bins=30, color="#1f77b4", alpha=0.8)
        axs[0].set_title(f"PUT latencies (n={len(put_lats)}) avg={avg_put:.2f}ms")
    else:
        axs[0].text(0.5, 0.5, "No PUT samples", ha="center")

    if get_lats:
        axs[1].hist(get_lats, bins=30, color="#ff7f0e", alpha=0.8)
        axs[1].set_title(f"GET latencies (n={len(get_lats)}) avg={avg_get:.2f}ms")
    else:
        axs[1].text(0.5, 0.5, "No GET samples", ha="center")

    file2 = outdir / f"{prefix}_cache_latency_hist_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file2, dpi=150)
    plt.close(fig)

    print(
        f"[cache] puts={puts} gets={gets} hit_rate={hit_rate:.2f}% avg_put={avg_put:.2f} avg_get={avg_get:.2f}"
    )
    return {"hitrate": str(file1), "latency_hist": str(file2)}


def compare_single_vs_distributed(
    single: Dict[str, Any], dist: Dict[str, Any], outdir: Path, prefix: str
):
    """
    If single-node results available, produce comparison plots.
    Assumes both JSONs use the same keys, but will handle missing fields gracefully.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Compare locks: success rate and throughput
    s_locks = single.get("locks", {}) if single else {}
    d_locks = dist.get("locks", {}) if dist else {}

    s_rate = s_locks.get("success_rate_percent", 0.0)
    d_rate = d_locks.get("success_rate_percent", 0.0)
    s_tp = s_locks.get("throughput_ops_per_sec", 0.0)
    d_tp = d_locks.get("throughput_ops_per_sec", 0.0)

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ind = np.arange(2)
    width = 0.35
    ax1.bar(
        ind - width / 2,
        [s_rate, s_tp],
        width,
        label="single (rate,tp)",
        color="#8c564b",
    )
    ax1.bar(
        ind + width / 2,
        [d_rate, d_tp],
        width,
        label="distributed (rate,tp)",
        color="#2ca02c",
    )
    ax1.set_xticks(ind)
    ax1.set_xticklabels(["success_rate(%)", "throughput(ops/s)"])
    ax1.set_title("Locks: single vs distributed (note: different scales)")
    ax1.legend()
    file1 = outdir / f"{prefix}_compare_locks_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file1, dpi=150)
    plt.close(fig)

    # Cache: compare hit rate
    s_cache = single.get("cache", {}) if single else {}
    d_cache = dist.get("cache", {}) if dist else {}
    s_hit = s_cache.get("hit_rate_percent", 0.0)
    d_hit = d_cache.get("hit_rate_percent", 0.0)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["single", "distributed"], [s_hit, d_hit], color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Hit rate (%)")
    ax.set_title("Cache hit rate: single vs distributed")
    file2 = outdir / f"{prefix}_compare_cache_hitrate_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(file2, dpi=150)
    plt.close(fig)

    return {"locks_compare": str(file1), "cache_compare": str(file2)}


def run_all_plots(
    input_path: Path,
    outdir: Path,
    single_path: Optional[Path] = None,
    show: bool = False,
):
    ensure_outdir(outdir)

    print(f"Loading distributed results from: {input_path}")
    dist = load_json(input_path)

    prefix = input_path.stem

    result_images = {}

    # Locks
    locks = dist.get("locks", {})
    if locks:
        result_images["locks"] = plot_locks(locks, outdir, prefix)
    else:
        print("No locks results found in input JSON")

    # Queue
    queue = dist.get("queue", {})
    if queue:
        result_images["queue"] = plot_queue(queue, outdir, prefix)
    else:
        print("No queue results found in input JSON")

    # Cache
    cache = dist.get("cache", {})
    if cache:
        result_images["cache"] = plot_cache(cache, outdir, prefix)
    else:
        print("No cache results found in input JSON")

    # Comparison with single-node results (optional)
    comp_res = None
    if single_path and single_path.exists():
        print(f"Loading single-node results from: {single_path}")
        single = load_json(single_path)
        comp_res = compare_single_vs_distributed(single, dist, outdir, prefix)
        result_images["compare"] = comp_res
    elif single_path:
        print(f"Single-node results file not found: {single_path}")

    # Optionally show results
    if show:
        # If show is requested, open the saved images using matplotlib (blocking)
        # We'll simply display the first few images found.
        import PIL.Image

        files_to_show = []
        for v in result_images.values():
            if isinstance(v, dict):
                for path_str in v.values():
                    if path_str:
                        files_to_show.append(Path(path_str))
            elif isinstance(v, str):
                files_to_show.append(Path(v))

        files_to_show = [p for p in files_to_show if p and p.exists()][:6]
        if files_to_show:
            for p in files_to_show:
                img = PIL.Image.open(p)
                plt.figure(figsize=(10, 6))
                plt.imshow(img)
                plt.axis("off")
            plt.show()
        else:
            print("No images available to show.")

    print("\nPlots generated:")
    for k, v in result_images.items():
        print(f" - {k}: {v}")

    if comp_res:
        print("\nComparison plots:")
        for k, v in comp_res.items():
            print(f" - {k}: {v}")


def parse_args():
    p = argparse.ArgumentParser(description="Plot distributed benchmark results")
    p.add_argument(
        "--input",
        type=str,
        default="benchmarks/scenarios/distributed_http_benchmark_results.json",
        help="Path to distributed benchmark results JSON",
    )
    p.add_argument(
        "--single",
        type=str,
        default="benchmark_results.json",
        help="Optional single-node benchmark results JSON for comparison",
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="benchmarks/scenarios/plots",
        help="Output directory for PNG plots",
    )
    p.add_argument(
        "--show",
        action="store_true",
        help="Display a few generated plots interactively (requires GUI environment)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    outdir = Path(args.outdir)
    single_path = Path(args.single) if args.single else None

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 2

    run_all_plots(input_path, outdir, single_path, show=args.show)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
