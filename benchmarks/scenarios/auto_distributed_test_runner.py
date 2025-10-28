from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

try:
    from benchmarks.scenarios.distributed_http_benchmark import run_all_tests
except Exception:
    run_all_tests = None  # type: ignore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("auto_test_runner")


ROLE_ENDPOINTS = {
    "lock": ["127.0.0.1:6000", "127.0.0.1:6010", "127.0.0.1:6020"],
    "queue": ["127.0.0.1:7001", "127.0.0.1:7002", "127.0.0.1:7003"],
    "cache": ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Automated distributed HTTP benchmark runner"
    )
    p.add_argument(
        "--mode",
        choices=["local", "docker"],
        default="local",
        help="How to start clusters: 'local' uses scripts/start_cluster_api.py, 'docker' runs docker-compose",
    )
    p.add_argument("--locks", type=int, default=500, help="Number of lock operations")
    p.add_argument("--queue", type=int, default=500, help="Number of queue messages")
    p.add_argument("--cache", type=int, default=500, help="Number of cache ops")
    p.add_argument(
        "--concurrency",
        type=int,
        default=30,
        help="Concurrency used by HTTP benchmark client",
    )
    p.add_argument(
        "--wait-start",
        type=int,
        default=25,
        help="Seconds to wait for cluster to start/respond before failing",
    )
    p.add_argument(
        "--output-dir",
        default="benchmarks/scenarios/results",
        help="Directory to write JSON results into",
    )
    p.add_argument(
        "--reuse-cluster",
        action="store_true",
        help="If set, reuse a running cluster across roles (only relevant for docker mode)",
    )
    p.add_argument(
        "--no-stop",
        action="store_true",
        help="If set, do not stop local cluster subprocesses after tests (helpful for debugging)",
    )
    return p.parse_args()


async def wait_for_endpoints(
    endpoints: List[str], timeout: float = 20.0, interval: float = 0.5
) -> bool:
    """
    Poll /status on each endpoint until all respond successfully or timeout.
    Returns True if all endpoints responded, False on timeout.
    """
    import aiohttp

    deadline = time.time() + timeout
    missing = set(endpoints)
    async with aiohttp.ClientSession() as session:
        while time.time() < deadline:
            to_remove = []
            for ep in list(missing):
                url = f"http://{ep}/status"
                try:
                    async with session.get(url, timeout=3.0) as resp:
                        if resp.status == 200:
                            j = await resp.json()
                            # Basic sanity: expects 'status' key or 'is_leader'
                            if isinstance(j, dict) and (
                                "status" in j or "is_leader" in j
                            ):
                                to_remove.append(ep)
                        else:
                            logger.debug(
                                "Status %s returned status %s", url, resp.status
                            )
                except Exception as e:
                    logger.debug("Endpoint %s not ready: %s", url, e)
                    continue

            for r in to_remove:
                missing.discard(r)

            if not missing:
                return True

            await asyncio.sleep(interval)

    return False


def start_local_cluster_process(role: str) -> subprocess.Popen:
    """
    Start `python scripts/start_cluster_api.py <role>` as a subprocess.
    Returns the Popen handle. The subprocess is started with SKIP_DOCKER_CHECK=1 so it does not require docker.
    """
    if role not in ("lock", "queue", "cache"):
        raise ValueError("Invalid role for local cluster start")

    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "start_cluster_api.py"), role]

    env = os.environ.copy()
    env["SKIP_DOCKER_CHECK"] = "1"
    env["PYTHONUNBUFFERED"] = "1"

    logger.info("Starting local cluster for role=%s with cmd: %s", role, " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        cwd=str(REPO_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        text=True,
    )
    return proc


def stop_process(proc: subprocess.Popen, name: str, timeout: float = 5.0) -> None:
    """Terminate a subprocess gracefully, then kill if needed."""
    if proc.poll() is not None:
        logger.info("Process %s already exited (rc=%s)", name, proc.returncode)
        return

    logger.info("Stopping process %s (pid=%s)", name, proc.pid)
    try:
        proc.terminate()
    except Exception:
        logger.exception("Error terminating process %s", name)

    try:
        proc.wait(timeout=timeout)
        logger.info("Process %s stopped", name)
    except subprocess.TimeoutExpired:
        logger.warning("Process %s did not stop in %ss; killing", name, timeout)
        try:
            proc.kill()
        except Exception:
            logger.exception("Failed to kill process %s", name)


def try_run_docker_compose() -> bool:
    """
    Try to run docker compose up -d --build in the ./docker directory.
    Tries both `docker compose` and `docker-compose`.
    Returns True on success, False otherwise.
    """
    docker_dir = REPO_ROOT / "docker"
    if not docker_dir.exists():
        logger.error("docker directory not found at %s", docker_dir)
        return False

    cmds = [
        ["docker", "compose", "up", "-d", "--build"],
        ["docker-compose", "up", "-d", "--build"],
    ]

    for cmd in cmds:
        try:
            logger.info("Running docker command: %s (in %s)", " ".join(cmd), docker_dir)
            res = subprocess.run(
                cmd, cwd=str(docker_dir), check=True, capture_output=True, text=True
            )
            logger.info("Docker compose returned: %s", res.stdout[:400])
            return True
        except subprocess.CalledProcessError as e:
            logger.warning("Docker command failed: %s ; stderr: %s", e, e.stderr[:400])
            continue
        except FileNotFoundError:
            logger.debug("Command not found: %s", cmd[0])
            continue

    logger.error("Unable to invoke docker compose with available commands")
    return False


async def run_role_test(
    role: str,
    mode: str,
    locks: int,
    queue: int,
    cache: int,
    concurrency: int,
    wait_start: int,
    output_dir: Path,
    reuse_cluster: bool,
    no_stop: bool,
) -> Optional[Dict]:
    """
    For the given role, start the cluster (docker/local), wait until endpoints are up,
    run the HTTP benchmark slice for that role, collect results, save JSON, and stop the cluster.
    Returns the results dict or None on failure.
    """
    endpoints = ROLE_ENDPOINTS.get(role)
    if not endpoints:
        logger.error("Unknown role endpoints mapping for %s", role)
        return None

    proc = None
    docker_started = False

    try:
        if mode == "local":
            proc = start_local_cluster_process(role)
        else:
            if not reuse_cluster:
                ok = try_run_docker_compose()
                if not ok:
                    logger.error("Failed to start docker compose cluster")
                    return None
                docker_started = True
            else:
                logger.info(
                    "Assuming docker cluster already running (reuse_cluster=True)"
                )

        logger.info(
            "Waiting up to %ss for endpoints to respond: %s", wait_start, endpoints
        )
        ok = await wait_for_endpoints(endpoints, timeout=wait_start)
        if not ok:
            logger.error(
                "Endpoints did not respond within timeout; collecting logs (if available) and aborting"
            )
            if proc and proc.stdout:
                logger.info("---- Last 400 chars of cluster process output ----")
                try:
                    out = proc.stdout.read() or ""
                    logger.info(out[-400:])
                except Exception:
                    pass
            return None

        logger.info("Endpoints are responsive; starting benchmark for role=%s", role)

        # Build nodes param and specific op counts: we want to run only the primitive relevant to the role
        nodes = endpoints
        # Map role to which counters to pass
        locks_ops = locks if role == "lock" else 0
        queue_ops = queue if role == "queue" else 0
        cache_ops = cache if role == "cache" else 0

        if run_all_tests is None:
            logger.error(
                "Internal import failure: cannot run benchmarks because run_all_tests is unavailable"
            )
            return None

        logger.info(
            "Invoking benchmark runner: locks=%s queue=%s cache=%s concurrency=%s",
            locks_ops,
            queue_ops,
            cache_ops,
            concurrency,
        )

        results = await run_all_tests(
            nodes=nodes,
            locks=locks_ops,
            queue=queue_ops,
            cache=cache_ops,
            concurrency=concurrency,
            cache_hit_ratio=0.8,
        )

        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"distributed_benchmark_{role}_{ts}.json"
        try:
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, default=str)
            logger.info("Saved results to %s", out_file)
        except Exception as e:
            logger.exception("Failed to save results: %s", e)

        return results

    finally:
        if mode == "local" and proc:
            if no_stop:
                logger.info(
                    "no-stop flag set; leaving local cluster process running (pid=%s)",
                    proc.pid,
                )
            else:
                stop_process(proc, f"local-cluster-{role}")
        elif mode == "docker" and docker_started and not reuse_cluster:
            try:
                docker_dir = REPO_ROOT / "docker"
                logger.info("Stopping docker compose stack (down)...")
                for cmd in (["docker", "compose", "down"], ["docker-compose", "down"]):
                    try:
                        subprocess.run(
                            cmd,
                            cwd=str(docker_dir),
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        logger.info(
                            "Docker compose down succeeded with cmd: %s", " ".join(cmd)
                        )
                        break
                    except Exception as e:
                        logger.debug("docker down with %s failed: %s", cmd, e)
                        continue
            except Exception:
                logger.exception("Error while stopping docker compose stack")


async def main_async(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    roles_to_run = ["lock", "queue", "cache"]

    overall = {
        "meta": {"started_at": datetime.utcnow().isoformat(), "mode": args.mode},
        "results": {},
    }

    # If docker mode + reuse_cluster==False, the docker compose will be started/stopped per-role by run_role_test.
    # Optionally user may set reuse_cluster True to start docker once and reuse.
    if args.mode == "docker" and args.reuse_cluster:
        ok = try_run_docker_compose()
        if not ok:
            logger.error("Failed to start docker compose (initial start). Aborting.")
            return 2
        # If reusing docker cluster, we'll not stop it until the end.
        logger.info("Docker compose started and will be reused across roles")

    # Sequentially run each role cluster + benchmark
    for role in roles_to_run:
        logger.info("==== Running tests for role: %s ====", role)
        res = await run_role_test(
            role=role,
            mode=args.mode,
            locks=args.locks,
            queue=args.queue,
            cache=args.cache,
            concurrency=args.concurrency,
            wait_start=args.wait_start,
            output_dir=output_dir,
            reuse_cluster=args.reuse_cluster,
            no_stop=args.no_stop,
        )
        overall["results"][role] = res or {"error": "failed"}
        # brief cooldown between runs
        await asyncio.sleep(1.0)

    # If docker mode and we started compose with reuse_cluster, bring it down now
    if args.mode == "docker" and args.reuse_cluster:
        try:
            docker_dir = REPO_ROOT / "docker"
            logger.info("Tearing down reused docker compose stack...")
            for cmd in (["docker", "compose", "down"], ["docker-compose", "down"]):
                try:
                    subprocess.run(
                        cmd,
                        cwd=str(docker_dir),
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    logger.info(
                        "Docker compose down succeeded with cmd: %s", " ".join(cmd)
                    )
                    break
                except Exception:
                    continue
        except Exception:
            logger.exception("Error while tearing down reused docker compose stack")

    # Save aggregate summary
    summary_file = (
        output_dir
        / f"distributed_benchmark_summary_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    try:
        with summary_file.open("w", encoding="utf-8") as f:
            json.dump(overall, f, indent=2, default=str)
        logger.info("Saved aggregate summary to %s", summary_file)
    except Exception:
        logger.exception("Failed to save aggregate summary")

    logger.info("All done. Results directory: %s", output_dir.resolve())
    return 0


def main() -> int:
    args = parse_args()
    try:
        # Graceful termination on signals
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: logger.info("Signal received, exiting..."))

        asyncio.run(main_async(args))
        return 0
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception:
        logger.exception("Fatal error in auto runner")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
