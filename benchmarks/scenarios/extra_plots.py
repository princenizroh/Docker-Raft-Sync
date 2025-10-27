#!/usr/bin/env python3
"""
Extra plots for benchmark percentiles and throughput comparison.

Generates:
 - p50/p95/p99 bar charts per primitive (locks, queue, cache)
 - Throughput comparison chart across primitives (locks ops/s, queue enq/deq msg/s, cache put/get ops/s)
 - Saves PNG files into output directory.

Usage:
  python benchmarks/scenarios/extra_plots.py \
      --input benchmarks/scenarios/distributed_http_benchmark_results.json \
      --single benchmark_results.json \
      --outdir benchmarks/scenarios/plots_extra

Requirements:
  pip install matplotlib seaborn numpy

The script is defensive: it will handle missing keys gracefully and will still
produce charts for whichever data is available in the input JSON.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Third-party plotting libs (commonly available)
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
except Exception as e:
    raise RuntimeError(
        "Missing plotting dependencies. Install with: pip install matplotlib seaborn numpy"
    ) from e

sns.set(style="whitegrid")


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def compute_percentiles(sample: List[float], percentiles=(50, 95, 99)):
    if not sample:
        return {p: 0.0 for p in percentiles}
    arr = np.array(sample, dtype=float)
    # remove zeros or negative samples which may be placeholders
    arr = arr[arr > 0]
    if arr.size == 0:
        return {p: 0.0 for p in percentiles}
    res = {}
    for p in percentiles:
        res[p] = float(np.percentile(arr, p))
    return res


def safe_list(d: Dict[str, Any], key: str) -> List[float]:
    val = d.get(key)
    if not val:
        return []
    try:
        return [float(x) for x in val if x is not None]
    except Exception:
        return []


def plot_percentiles(
    dist_results: Dict[str, Any], outdir: Path, prefix: str = "extra"
) -> Dict[str, str]:
    """
    Create p50/p95/p99 bar charts for locks, queue (enqueue/dequeue), cache (put/get).
    Returns mapping role->filepath.
    """
    ensure_dir(outdir)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    saved = {}

    # Locks: use raw_latencies_ms_sample or p50/p95 available fields
    locks = dist_results.get("locks", {})
    lock_sample = safe_list(locks, "raw_latencies_ms_sample")
    if not lock_sample:
        # maybe the distributed runner recorded p50/p95 directly
        lock_sample = []
    lock_pct = compute_percentiles(lock_sample)
    # If percentiles are zero but fields exist, use fields
    if all(v == 0.0 for v in lock_pct.values()):
        lock_pct = {
            50: locks.get("p50_latency_ms", 0.0) or 0.0,
            95: locks.get("p95_latency_ms", 0.0) or 0.0,
            99: locks.get("p99_latency_ms", 0.0) or 0.0,
        }

    # Queue: enqueue latencies and dequeue latencies
    queue = dist_results.get("queue", {})
    enq_sample = safe_list(queue, "enqueue_latencies_ms_sample")
    deq_sample = safe_list(queue, "dequeue_latencies_ms_sample")
    enq_pct = compute_percentiles(enq_sample)
    deq_pct = compute_percentiles(deq_sample)
    # Fallback to fields if samples absent
    if all(v == 0.0 for v in enq_pct.values()):
        enq_pct = {
            50: queue.get("p50_enqueue_latency_ms", 0.0) or 0.0,
            95: queue.get("p95_enqueue_latency_ms", 0.0) or 0.0,
            99: queue.get("p99_enqueue_latency_ms", 0.0) or 0.0,
        }
    if all(v == 0.0 for v in deq_pct.values()):
        deq_pct = {
            50: queue.get("p50_dequeue_latency_ms", 0.0) or 0.0,
            95: queue.get("p95_dequeue_latency_ms", 0.0) or 0.0,
            99: queue.get("p99_dequeue_latency_ms", 0.0) or 0.0,
        }

    # Cache: get latencies
    cache = dist_results.get("cache", {})
    put_sample = safe_list(cache, "put_latencies_ms_sample")
    get_sample = safe_list(cache, "get_latencies_ms_sample")
    put_pct = compute_percentiles(put_sample)
    get_pct = compute_percentiles(get_sample)
    if all(v == 0.0 for v in put_pct.values()):
        put_pct = {
            50: cache.get("p50_put_latency_ms", 0.0) or 0.0,
            95: cache.get("p95_put_latency_ms", 0.0) or 0.0,
            99: cache.get("p99_put_latency_ms", 0.0) or 0.0,
        }
    if all(v == 0.0 for v in get_pct.values()):
        get_pct = {
            50: cache.get("p50_get_latency_ms", 0.0) or 0.0,
            95: cache.get("p95_get_latency_ms", 0.0) or 0.0,
            99: cache.get("p99_get_latency_ms", 0.0) or 0.0,
        }

    # Build a neighbors layout: each primitive has three bars (p50,p95,p99)
    primitives = []
    values = []
    colors = []
    labels = []

    def append_group(name, pctdict, color):
        primitives.append(name)
        values.append(
            [pctdict.get(50, 0.0), pctdict.get(95, 0.0), pctdict.get(99, 0.0)]
        )
        colors.append(color)
        labels.append(name)

    append_group(
        "locks",
        lock_pct
        if isinstance(lock_pct, dict)
        else {50: lock_pct[50], 95: lock_pct[95], 99: lock_pct[99]},
        "#ff7f0e",
    )
    append_group("queue_enq", enq_pct, "#1f77b4")
    append_group("queue_deq", deq_pct, "#2ca02c")
    append_group("cache_put", put_pct, "#9467bd")
    append_group("cache_get", get_pct, "#8c564b")

    # Prepare plot matrix
    groups = labels
    n_groups = len(groups)
    percentiles = ["p50", "p95", "p99"]
    width = 0.15

    fig, ax = plt.subplots(figsize=(max(8, n_groups * 1.2), 5))
    x = np.arange(len(percentiles))
    for i, (grp_vals, color, grp_label) in enumerate(zip(values, colors, groups)):
        ax.bar(
            x + (i - n_groups / 2) * width + width / 2,
            grp_vals,
            width=width,
            label=grp_label,
            color=color,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(percentiles)
    ax.set_ylabel("Latency (ms)")
    ax.set_title("Latency percentiles (p50/p95/p99) across primitives")
    ax.legend(loc="upper right")
    fname = outdir / f"{prefix}_p50_p95_p99_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    saved["p50_p95_p99"] = str(fname)

    return saved


def plot_throughput_compare(
    dist_results: Dict[str, Any], outdir: Path, prefix: str = "extra"
) -> Dict[str, str]:
    """
    Prepare throughput comparison across primitives.

    Locks: use throughput_ops_per_sec
    Queue: use enqueue_throughput_msg_per_sec and dequeue_throughput_msg_per_sec
    Cache: approximate throughput using ops counts / duration if present, else avg lat inverse
    """
    ensure_dir(outdir)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    locks = dist_results.get("locks", {})
    queue = dist_results.get("queue", {})
    cache = dist_results.get("cache", {})

    # Locks throughput (ops/sec)
    lock_tp = float(locks.get("throughput_ops_per_sec") or 0.0)

    # Queue throughput
    q_enq_tp = float(queue.get("enqueue_throughput_msg_per_sec") or 0.0)
    q_deq_tp = float(queue.get("dequeue_throughput_msg_per_sec") or 0.0)

    # Cache throughput: prefer explicit metrics if present otherwise estimate from counts/duration
    cache_puts = float(cache.get("puts") or 0.0)
    cache_gets = float(cache.get("gets") or 0.0)
    cache_duration = float(dist_results.get("meta", {}).get("duration_seconds") or 0.0)
    # The distributed runner doesn't always include a duration per-op; try reasonable fallback:
    # Use avg lat -> throughput = ops / (avg_latency_s * ops) = 1 / avg_latency_s (approx single-op throughput)
    cache_put_avg_ms = float(cache.get("avg_put_latency_ms") or 0.0)
    cache_get_avg_ms = float(cache.get("avg_get_latency_ms") or 0.0)
    cache_put_tp = 0.0
    cache_get_tp = 0.0
    if cache_puts > 0 and cache_duration > 0:
        cache_put_tp = cache_puts / cache_duration
    elif cache_put_avg_ms > 0:
        cache_put_tp = 1000.0 / cache_put_avg_ms
    if cache_gets > 0 and cache_duration > 0:
        cache_get_tp = cache_gets / cache_duration
    elif cache_get_avg_ms > 0:
        cache_get_tp = 1000.0 / cache_get_avg_ms

    labels = ["locks_ops/s", "queue_enq/s", "queue_deq/s", "cache_put/s", "cache_get/s"]
    values = [lock_tp, q_enq_tp, q_deq_tp, cache_put_tp, cache_get_tp]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b"]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(labels))
    ax.bar(x, values, color=colors)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Throughput (ops/sec or msg/sec)")
    ax.set_title("Throughput comparison across primitives")
    # Annotate bars
    for xi, v in zip(x, values):
        ax.text(
            xi,
            v + max(0.01, max(values) * 0.02),
            f"{v:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fname = outdir / f"{prefix}_throughput_compare_{timestamp}.png"
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)

    return {"throughput_compare": str(fname)}


def main():
    parser = argparse.ArgumentParser(
        description="Extra benchmark plots (p50/p95/p99 + throughput)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="benchmarks/scenarios/distributed_http_benchmark_results.json",
        help="Distributed benchmark results JSON",
    )
    parser.add_argument(
        "--single",
        type=str,
        default="benchmark_results.json",
        help="Optional single-node results JSON for comparison (not required)",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="benchmarks/scenarios/plots_extra",
        help="Directory to write PNG plots",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 2

    outdir = Path(args.outdir)
    ensure_dir(outdir)

    dist_results = load_json(input_path)

    prefix = input_path.stem

    saved_files = {}
    try:
        print("Generating percentile plot...")
        saved_files.update(plot_percentiles(dist_results, outdir, prefix=prefix))
    except Exception as e:
        print(f"Error generating percentiles plot: {e}")

    try:
        print("Generating throughput comparison plot...")
        saved_files.update(plot_throughput_compare(dist_results, outdir, prefix=prefix))
    except Exception as e:
        print(f"Error generating throughput plot: {e}")

    # Optionally compare with single-node results if provided
    single_path = Path(args.single) if args.single else None
    if single_path and single_path.exists():
        try:
            single = load_json(single_path)
            # For now create a simple overlay comparison for locks throughput if available
            print("Generating single vs distributed locks throughput comparison...")
            s_lock_tp = float(
                single.get("Raft Consensus", {}).get("Throughput (ops/sec)", 0.0) or 0.0
            )
            d_lock_tp = float(
                dist_results.get("locks", {}).get("throughput_ops_per_sec", 0.0) or 0.0
            )
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(["single"], [s_lock_tp], color="#1f77b4", label="single")
            ax.bar(["distributed"], [d_lock_tp], color="#ff7f0e", label="distributed")
            ax.set_ylabel("Throughput (ops/sec)")
            ax.set_title("Single-node vs Distributed (locks throughput)")
            fname = (
                outdir
                / f"{prefix}_single_vs_distributed_locks_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.png"
            )
            fig.tight_layout()
            fig.savefig(fname, dpi=150)
            plt.close(fig)
            saved_files["single_vs_distributed_locks"] = str(fname)
        except Exception as e:
            print(f"Error creating single-vs-distributed comparison: {e}")

    print("\nSaved plots:")
    for k, v in saved_files.items():
        print(f" - {k}: {v}")

    print("\nDone.")


if __name__ == "__main__":
    main()
