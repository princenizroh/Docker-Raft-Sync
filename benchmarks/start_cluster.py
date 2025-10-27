#!/usr/bin/env python3
"""
Quick start script to run a 3-node cluster locally
"""

import subprocess
import sys
import time
import os
import signal

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import asyncio
        import aiohttp
        print("[OK] Dependencies installed")
        return True
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        print("\nInstalling dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False

def start_node(node_id, port, cluster_nodes):
    """Start a single node"""
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    cmd = [
        sys.executable,
        "-m",
        "src.nodes.base_node",
        "--node-id", node_id,
        "--host", "0.0.0.0",
        "--port", str(port),
        "--cluster-nodes", cluster_nodes
    ]
    
    print(f"Starting {node_id} on port {port}...")
    
    # Start process
    if sys.platform == "win32":
        proc = subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        proc = subprocess.Popen(cmd)
    
    return proc

def main():
    print("=" * 60)
    print("Distributed Synchronization System - Quick Start")
    print("=" * 60)
    print()
    
    # Check requirements
    check_python_version()
    check_dependencies()
    
    # Define cluster
    cluster_nodes = "node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020"
    
    nodes = [
        ("node-1", 6000),
        ("node-2", 6010),
        ("node-3", 6020)
    ]
    
    processes = []
    
    try:
        # Start all nodes QUICKLY (reduce delay for faster leader election)
        print("\nStarting cluster nodes...")
        for node_id, port in nodes:
            proc = start_node(node_id, port, cluster_nodes)
            processes.append(proc)
            time.sleep(0.5)  # REDUCED from 2s to 0.5s - faster startup!
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All nodes started!")
        print("=" * 60)
        print("\nWaiting for leader election (5 seconds)...")
        time.sleep(5)  # Wait for leader to be elected
        
        print("\n" + "=" * 60)
        print("[READY] Cluster is ready for connections!")
        print("=" * 60)
        print()
        print("Node URLs:")
        for node_id, port in nodes:
            print(f"  - {node_id}: http://localhost:{port}")
        print()
        print("[INFO] You can now run demos in another terminal:")
        print("       python benchmarks/demo.py")
        print()
        print("Press Ctrl+C to stop the cluster...")
        print()
        
        # Wait for all processes
        for proc in processes:
            proc.wait()
    
    except KeyboardInterrupt:
        print("\n\nShutting down cluster...")
        
        # Terminate all processes
        for proc in processes:
            if sys.platform == "win32":
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                proc.terminate()
        
        # Wait for graceful shutdown
        time.sleep(2)
        
        # Force kill if still running
        for proc in processes:
            if proc.poll() is None:
                proc.kill()
        
        print("[OK] Cluster stopped")
    
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        
        # Clean up
        for proc in processes:
            try:
                proc.kill()
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
