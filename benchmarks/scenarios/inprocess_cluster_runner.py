#!/usr/bin/env python3
"""
In-process Cluster Runner

Starts a 3-node cluster in-process (lock / queue / cache) using the
ClusterManager from scripts.start_cluster_api and runs the HTTP-based
distributed benchmarks (benchmarks/scenarios/distributed_http_benchmark.py)
against the in-process cluster HTTP API endpoints.

Usage (from repository root):
  python benchmarks/scenarios/inprocess_cluster_runner.py lock --locks 500 --concurrency 30

Example:
  python benchmarks/scenarios/inprocess_cluster_runner.py lock --locks 100 --concurrency 10

Notes:
- This runner starts nodes inside the same Python process (no Docker,
  no subprocesses). It uses the ClusterManager.start_nodes()/stop_nodes()
  coroutine APIs to manage lifecycle.
- The default HTTP endpoints follow the conventions used by the repo:
    lock  -> 127.0.0.1:6000, 127.0.0.1:6010, 127.0.0.1:6020
    queue -> 127.0.0.1:7001, 127.0.0.1:7002, 127.0.0.1:7003
    cache -> 127.0.0.1:8001, 127.0.0.1:8002, 127.0.0.1:8003
- Results are written to ./benchmarks/scenarios/inprocess_results_<role>_<ts>.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Ensure repository root is importable when running from project root
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

# Imports from the repository
from scripts.start_cluster_api import ClusterManager
from benchmarks.scenarios.distributed_http_benchmark import run_all_tests

# Basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("inprocess_cluster_runner")


ROLE_ENDPOINTS = {
    "lock": ["127.0.0.1:6000", "127.0.0.1:6010", "127.0.0.1:6020"],
    "queue": ["127.0.0.1:7001", "127.0.0.1:7002", "127.0.0.1:7003"],
    "cache": ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="In-process cluster + HTTP benchmark runner"
    )
    p.add_argument(
        "role",
        choices=["lock", "queue", "cache"],
        help="Which primitive cluster to start and test",
    )
    p.add_argument("--locks", type=int, default=500, help="Number of lock operations")
    p.add_argument("--queue", type=int, default=500, help="Number of queue messages")
    p.add_argument("--cache", type=int, default=500, help="Number of cache ops")
    p.add_argument(
        "--concurrency", type=int, default=30, help="HTTP client concurrency for tests"
    )
    p.add_argument(
        "--wait-after-start",
        type=float,
        default=2.5,
        help="Seconds to wait after cluster start for leader election",
    )
    p.add_argument(
        "--output-dir",
        default="benchmarks/scenarios",
        help="Directory to write JSON results into",
    )
    return p.parse_args()


async def start_cluster_and_run(
    role: str,
    locks: int,
    queue: int,
    cache: int,
    concurrency: int,
    wait_after_start: float,
    output_dir: str,
) -> int:
    """
    Start ClusterManager(role) in-process, run the HTTP benchmark (only for the selected
    primitive), collect results, stop cluster, and write JSON output.
    Returns 0 on success, non-zero on failure.
    """
    # Validate mapping
    endpoints = ROLE_ENDPOINTS.get(role)
    if not endpoints:
        logger.error("No endpoints mapping for role '%s'", role)
        return 2

    cluster = ClusterManager(role)
    logger.info("Starting in-process %s cluster...", role)
    try:
        ok = await cluster.start_nodes()
        if ok is False:
            logger.error("ClusterManager.start_nodes() returned failure")
            return 3
    except Exception as e:
        logger.exception("Failed to start cluster in-process: %s", e)
        # Attempt best-effort cleanup
        try:
            await cluster.stop_nodes()
        except Exception:
            pass
        return 4

    # Allow a small window for leader election / stabilization
    logger.info(
        "Waiting %.2fs for cluster stabilization / leader election...", wait_after_start
    )
    await asyncio.sleep(wait_after_start)

    # Build nodes list for HTTP client (ClusterClient expects host:port strings)
    nodes = endpoints

    try:
        logger.info("Running distributed HTTP tests against endpoints: %s", nodes)

        # Only run the primitive requested by the role
        locks_ops = locks if role == "lock" else 0
        queue_ops = queue if role == "queue" else 0
        cache_ops = cache if role == "cache" else 0

        start_ts = time.time()
        results = await run_all_tests(
            nodes=nodes,
            locks=locks_ops,
            queue=queue_ops,
            cache=cache_ops,
            concurrency=concurrency,
            cache_hit_ratio=0.8,
        )
        duration = time.time() - start_ts

        # Augment results with metadata
        meta = {
            "role": role,
            "nodes": nodes,
            "requested_ops": {
                "locks": locks_ops,
                "queue": queue_ops,
                "cache": cache_ops,
            },
            "concurrency": concurrency,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        output = {"meta": meta, "results": results}

        # Save results
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_file = out_dir / f"inprocess_results_{role}_{ts}.json"
        try:
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, default=str)
            logger.info("Saved benchmark results to: %s", out_file)
        except Exception as e:
            logger.exception("Failed to save results to %s: %s", out_file, e)
            return 5

    except Exception as e:
        logger.exception("Benchmark run failed: %s", e)
        return 6

    finally:
        logger.info("Stopping in-process cluster...")
        try:
            await cluster.stop_nodes()
            # give a moment for cleanup
            await asyncio.sleep(0.2)
        except Exception as e:
            logger.exception("Error stopping cluster: %s", e)

    logger.info("Completed in-process run for role=%s", role)
    return 0


def main() -> int:
    args = parse_args()
    try:
        return asyncio.run(
            start_cluster_and_run(
                role=args.role,
                locks=args.locks,
                queue=args.queue,
                cache=args.cache,
                concurrency=args.concurrency,
                wait_after_start=args.wait_after_start,
                output_dir=args.output_dir,
            )
        )
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.exception("Fatal error in runner: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
