255ms ❯ python .\benchmarks\demo_cluster.py
============================================================
Distributed Synchronization System - Cluster Demo
============================================================

[IMPORTANT] CLUSTER MUST BE RUNNING FIRST!

  Terminal 1: python benchmarks/start_cluster.py
  Terminal 2: python benchmarks/demo_cluster.py (this script)

  This demo connects to the existing cluster and
  participates as a 4th node in the Raft consensus.

Select demo type:
  1. Distributed Lock Manager
  2. Distributed Queue System
  3. Distributed Cache (MESI)

Enter choice (1-3): 1
2025-10-26 03:32:06,195 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 03:32:06,195 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 03:32:06,195 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 03:32:06,195 - src.nodes.base_node - INFO - BaseNode demo-node initialized on localhost:6000

Starting lock node demo-node (cluster mode)...
Connecting to cluster nodes...
2025-10-26 03:32:06,196 - src.nodes.base_node - INFO - Starting node demo-node...
2025-10-26 03:32:06,217 - src.communication.message_passing - INFO - Message passing server started on localhost:6000
2025-10-26 03:32:06,217 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 03:32:06,217 - src.consensus.raft - INFO - Raft node demo-node started as follower
2025-10-26 03:32:06,217 - src.nodes.base_node - INFO - Connecting to cluster nodes...
2025-10-26 03:32:06,219 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 03:32:06,220 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 03:32:06,221 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 03:32:06,221 - src.nodes.base_node - INFO - Node demo-node started successfully
2025-10-26 03:32:06,221 - src.nodes.lock_manager - INFO - Distributed Lock Manager started
Waiting for cluster to stabilize...
2025-10-26 03:32:06,381 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 03:32:06,381 - src.consensus.raft - INFO - Node demo-node starting election (term 1)
2025-10-26 03:32:06,381 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 1)
2025-10-26 03:32:06,381 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:06,660 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:06,661 - src.consensus.raft - INFO - Node demo-node starting election (term 2)
2025-10-26 03:32:06,661 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 2)
2025-10-26 03:32:06,661 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:06,829 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:06,829 - src.consensus.raft - INFO - Node demo-node starting election (term 3)
2025-10-26 03:32:06,829 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 3)
2025-10-26 03:32:06,830 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:06,998 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:32:06,999 - src.consensus.raft - INFO - Node demo-node starting election (term 4)
2025-10-26 03:32:06,999 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 4)
2025-10-26 03:32:06,999 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:07,246 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 03:32:07,246 - src.consensus.raft - INFO - Node demo-node starting election (term 5)
2025-10-26 03:32:07,247 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 5)
2025-10-26 03:32:07,247 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:07,463 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 03:32:07,463 - src.consensus.raft - INFO - Node demo-node starting election (term 6)
2025-10-26 03:32:07,463 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 6)
2025-10-26 03:32:07,463 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:07,636 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:07,636 - src.consensus.raft - INFO - Node demo-node starting election (term 7)
2025-10-26 03:32:07,636 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 7)
2025-10-26 03:32:07,636 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:07,898 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:32:07,898 - src.consensus.raft - INFO - Node demo-node starting election (term 8)
2025-10-26 03:32:07,898 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 8)
2025-10-26 03:32:07,898 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:08,052 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 03:32:08,052 - src.consensus.raft - INFO - Node demo-node starting election (term 9)
2025-10-26 03:32:08,052 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 9)
2025-10-26 03:32:08,052 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:08,222 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:08,222 - src.consensus.raft - INFO - Node demo-node starting election (term 10)
2025-10-26 03:32:08,222 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 10)
2025-10-26 03:32:08,223 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:08,471 - src.consensus.raft - INFO - Election timeout (0.25s > 0.25s)
2025-10-26 03:32:08,471 - src.consensus.raft - INFO - Node demo-node starting election (term 11)
2025-10-26 03:32:08,471 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 11)
2025-10-26 03:32:08,471 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:08,733 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:32:08,733 - src.consensus.raft - INFO - Node demo-node starting election (term 12)
2025-10-26 03:32:08,733 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 12)
2025-10-26 03:32:08,733 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:08,902 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:08,902 - src.consensus.raft - INFO - Node demo-node starting election (term 13)
2025-10-26 03:32:08,902 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 13)
2025-10-26 03:32:08,902 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:09,151 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 03:32:09,151 - src.consensus.raft - INFO - Node demo-node starting election (term 14)
2025-10-26 03:32:09,151 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 14)
2025-10-26 03:32:09,151 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:09,341 - src.consensus.raft - INFO - Election timeout (0.19s > 0.19s)
2025-10-26 03:32:09,341 - src.consensus.raft - INFO - Node demo-node starting election (term 15)
2025-10-26 03:32:09,342 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 15)
2025-10-26 03:32:09,342 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:09,528 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 03:32:09,528 - src.consensus.raft - INFO - Node demo-node starting election (term 16)
2025-10-26 03:32:09,528 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 16)
2025-10-26 03:32:09,529 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:09,822 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:32:09,822 - src.consensus.raft - INFO - Node demo-node starting election (term 17)
2025-10-26 03:32:09,822 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 17)
2025-10-26 03:32:09,822 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:10,086 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 03:32:10,086 - src.consensus.raft - INFO - Node demo-node starting election (term 18)
2025-10-26 03:32:10,086 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 18)
2025-10-26 03:32:10,086 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:10,380 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:32:10,381 - src.consensus.raft - INFO - Node demo-node starting election (term 19)
2025-10-26 03:32:10,381 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 19)
2025-10-26 03:32:10,381 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:10,658 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:10,658 - src.consensus.raft - INFO - Node demo-node starting election (term 20)
2025-10-26 03:32:10,658 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 20)
2025-10-26 03:32:10,658 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:10,952 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:32:10,952 - src.consensus.raft - INFO - Node demo-node starting election (term 21)
2025-10-26 03:32:10,952 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 21)
2025-10-26 03:32:10,952 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:11,218 - src.consensus.raft - INFO - Election timeout (0.27s > 0.25s)
2025-10-26 03:32:11,218 - src.consensus.raft - INFO - Node demo-node starting election (term 22)
2025-10-26 03:32:11,218 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 22)
2025-10-26 03:32:11,218 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:11,219 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-1:localhost:5000 (phi=0.00)
2025-10-26 03:32:11,219 - src.nodes.base_node - WARNING - Node failed: node-1:localhost:5000
2025-10-26 03:32:11,219 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-2:localhost:5010 (phi=0.00)
2025-10-26 03:32:11,219 - src.nodes.base_node - WARNING - Node failed: node-2:localhost:5010
2025-10-26 03:32:11,219 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-3:localhost:5020 (phi=0.00)
2025-10-26 03:32:11,219 - src.nodes.base_node - WARNING - Node failed: node-3:localhost:5020

============================================================
DEMO: Distributed Lock Manager (Cluster Mode)
============================================================

[INFO] Waiting for cluster synchronization...
2025-10-26 03:32:11,512 - src.consensus.raft - INFO - Election timeout (0.29s > 0.29s)
2025-10-26 03:32:11,512 - src.consensus.raft - INFO - Node demo-node starting election (term 23)
2025-10-26 03:32:11,513 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 23)
2025-10-26 03:32:11,513 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:11,681 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:32:11,681 - src.consensus.raft - INFO - Node demo-node starting election (term 24)
2025-10-26 03:32:11,681 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 24)
2025-10-26 03:32:11,682 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:11,963 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:32:11,963 - src.consensus.raft - INFO - Node demo-node starting election (term 25)
2025-10-26 03:32:11,963 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 25)
2025-10-26 03:32:11,963 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:12,196 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:12,196 - src.consensus.raft - INFO - Node demo-node starting election (term 26)
2025-10-26 03:32:12,196 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 26)
2025-10-26 03:32:12,196 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:12,366 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:12,366 - src.consensus.raft - INFO - Node demo-node starting election (term 27)
2025-10-26 03:32:12,366 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 27)
2025-10-26 03:32:12,366 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:12,536 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:32:12,536 - src.consensus.raft - INFO - Node demo-node starting election (term 28)
2025-10-26 03:32:12,536 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 28)
2025-10-26 03:32:12,536 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:12,755 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 03:32:12,755 - src.consensus.raft - INFO - Node demo-node starting election (term 29)
2025-10-26 03:32:12,755 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 29)
2025-10-26 03:32:12,755 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:12,991 - src.consensus.raft - INFO - Election timeout (0.24s > 0.22s)
2025-10-26 03:32:12,991 - src.consensus.raft - INFO - Node demo-node starting election (term 30)
2025-10-26 03:32:12,991 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 30)
2025-10-26 03:32:12,991 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:13,145 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 03:32:13,145 - src.consensus.raft - INFO - Node demo-node starting election (term 31)
2025-10-26 03:32:13,145 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 31)
2025-10-26 03:32:13,145 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:13,362 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 03:32:13,362 - src.consensus.raft - INFO - Node demo-node starting election (term 32)
2025-10-26 03:32:13,362 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 32)
2025-10-26 03:32:13,362 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:13,641 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:13,641 - src.consensus.raft - INFO - Node demo-node starting election (term 33)
2025-10-26 03:32:13,641 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 33)
2025-10-26 03:32:13,641 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:13,873 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 03:32:13,873 - src.consensus.raft - INFO - Node demo-node starting election (term 34)
2025-10-26 03:32:13,874 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 34)
2025-10-26 03:32:13,874 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:14,091 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 03:32:14,091 - src.consensus.raft - INFO - Node demo-node starting election (term 35)
2025-10-26 03:32:14,091 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 35)
2025-10-26 03:32:14,091 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:14,318 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:14,318 - src.consensus.raft - INFO - Node demo-node starting election (term 36)
2025-10-26 03:32:14,318 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 36)
2025-10-26 03:32:14,318 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:14,505 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 03:32:14,505 - src.consensus.raft - INFO - Node demo-node starting election (term 37)
2025-10-26 03:32:14,505 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 37)
2025-10-26 03:32:14,505 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:14,722 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 03:32:14,722 - src.consensus.raft - INFO - Node demo-node starting election (term 38)
2025-10-26 03:32:14,722 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 38)
2025-10-26 03:32:14,723 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:15,015 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:32:15,015 - src.consensus.raft - INFO - Node demo-node starting election (term 39)
2025-10-26 03:32:15,015 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 39)
2025-10-26 03:32:15,015 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:15,279 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 03:32:15,279 - src.consensus.raft - INFO - Node demo-node starting election (term 40)
2025-10-26 03:32:15,279 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 40)
2025-10-26 03:32:15,279 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:15,556 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:15,556 - src.consensus.raft - INFO - Node demo-node starting election (term 41)
2025-10-26 03:32:15,556 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 41)
2025-10-26 03:32:15,556 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:15,771 - src.consensus.raft - INFO - Election timeout (0.21s > 0.21s)
2025-10-26 03:32:15,771 - src.consensus.raft - INFO - Node demo-node starting election (term 42)
2025-10-26 03:32:15,771 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 42)
2025-10-26 03:32:15,772 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:15,986 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 03:32:15,986 - src.consensus.raft - INFO - Node demo-node starting election (term 43)
2025-10-26 03:32:15,987 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 43)
2025-10-26 03:32:15,987 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:16,188 - src.consensus.raft - INFO - Election timeout (0.20s > 0.18s)
2025-10-26 03:32:16,188 - src.consensus.raft - INFO - Node demo-node starting election (term 44)
2025-10-26 03:32:16,188 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 44)
2025-10-26 03:32:16,188 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:16,495 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 03:32:16,495 - src.consensus.raft - INFO - Node demo-node starting election (term 45)
2025-10-26 03:32:16,495 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 45)
2025-10-26 03:32:16,495 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:16,695 - src.consensus.raft - INFO - Election timeout (0.20s > 0.18s)
2025-10-26 03:32:16,695 - src.consensus.raft - INFO - Node demo-node starting election (term 46)
2025-10-26 03:32:16,695 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 46)
2025-10-26 03:32:16,696 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:16,895 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 03:32:16,895 - src.consensus.raft - INFO - Node demo-node starting election (term 47)
2025-10-26 03:32:16,896 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 47)
2025-10-26 03:32:16,896 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:17,122 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:17,122 - src.consensus.raft - INFO - Node demo-node starting election (term 48)
2025-10-26 03:32:17,122 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 48)
2025-10-26 03:32:17,122 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:17,308 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 03:32:17,308 - src.consensus.raft - INFO - Node demo-node starting election (term 49)
2025-10-26 03:32:17,308 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 49)
2025-10-26 03:32:17,308 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:17,539 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 03:32:17,539 - src.consensus.raft - INFO - Node demo-node starting election (term 50)
2025-10-26 03:32:17,539 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 50)
2025-10-26 03:32:17,539 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:17,816 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:17,816 - src.consensus.raft - INFO - Node demo-node starting election (term 51)
2025-10-26 03:32:17,816 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 51)
2025-10-26 03:32:17,816 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:18,046 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:18,046 - src.consensus.raft - INFO - Node demo-node starting election (term 52)
2025-10-26 03:32:18,046 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 52)
2025-10-26 03:32:18,046 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:18,321 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 03:32:18,321 - src.consensus.raft - INFO - Node demo-node starting election (term 53)
2025-10-26 03:32:18,321 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 53)
2025-10-26 03:32:18,321 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:18,584 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 03:32:18,584 - src.consensus.raft - INFO - Node demo-node starting election (term 54)
2025-10-26 03:32:18,585 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 54)
2025-10-26 03:32:18,585 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:18,808 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 03:32:18,809 - src.consensus.raft - INFO - Node demo-node starting election (term 55)
2025-10-26 03:32:18,809 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 55)
2025-10-26 03:32:18,809 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:19,023 - src.consensus.raft - INFO - Election timeout (0.21s > 0.20s)
2025-10-26 03:32:19,023 - src.consensus.raft - INFO - Node demo-node starting election (term 56)
2025-10-26 03:32:19,023 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 56)
2025-10-26 03:32:19,023 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:19,193 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:19,193 - src.consensus.raft - INFO - Node demo-node starting election (term 57)
2025-10-26 03:32:19,193 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 57)
2025-10-26 03:32:19,193 - src.nodes.base_node - INFO - Raft state changed to: candidate

1. Acquiring exclusive lock on 'resource-1'...
2025-10-26 03:32:19,224 - src.nodes.base_node - INFO - Not leader, cannot submit command
2025-10-26 03:32:19,224 - src.nodes.lock_manager - WARNING - Failed to submit lock request for resource-1
   Result: FAILED

2. Trying to acquire shared lock on same resource (should wait)...
2025-10-26 03:32:19,225 - src.nodes.base_node - INFO - Not leader, cannot submit command
2025-10-26 03:32:19,225 - src.nodes.lock_manager - WARNING - Failed to submit lock request for resource-1
   Result: TIMEOUT (Expected)

3. Releasing lock from client-1...
2025-10-26 03:32:19,225 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Lock released

4. Lock Status:
   Total locks: 0
   Active clients: 0


============================================================
Demo completed! Press Ctrl+C to exit...
============================================================
2025-10-26 03:32:19,501 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 03:32:19,501 - src.consensus.raft - INFO - Node demo-node starting election (term 58)
2025-10-26 03:32:19,501 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 58)
2025-10-26 03:32:19,502 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:19,780 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:19,780 - src.consensus.raft - INFO - Node demo-node starting election (term 59)
2025-10-26 03:32:19,780 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 59)
2025-10-26 03:32:19,780 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:20,013 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 03:32:20,013 - src.consensus.raft - INFO - Node demo-node starting election (term 60)
2025-10-26 03:32:20,014 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 60)
2025-10-26 03:32:20,014 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:20,264 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 03:32:20,264 - src.consensus.raft - INFO - Node demo-node starting election (term 61)
2025-10-26 03:32:20,264 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 61)
2025-10-26 03:32:20,264 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:20,434 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:32:20,434 - src.consensus.raft - INFO - Node demo-node starting election (term 62)
2025-10-26 03:32:20,435 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 62)
2025-10-26 03:32:20,435 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:20,635 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 03:32:20,635 - src.consensus.raft - INFO - Node demo-node starting election (term 63)
2025-10-26 03:32:20,635 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 63)
2025-10-26 03:32:20,635 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:20,865 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:20,865 - src.consensus.raft - INFO - Node demo-node starting election (term 64)
2025-10-26 03:32:20,865 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 64)
2025-10-26 03:32:20,866 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:21,018 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 03:32:21,018 - src.consensus.raft - INFO - Node demo-node starting election (term 65)
2025-10-26 03:32:21,018 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 65)
2025-10-26 03:32:21,019 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:21,296 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:32:21,296 - src.consensus.raft - INFO - Node demo-node starting election (term 66)
2025-10-26 03:32:21,296 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 66)
2025-10-26 03:32:21,296 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:21,465 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:32:21,465 - src.consensus.raft - INFO - Node demo-node starting election (term 67)
2025-10-26 03:32:21,465 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 67)
2025-10-26 03:32:21,465 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:21,634 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 03:32:21,634 - src.consensus.raft - INFO - Node demo-node starting election (term 68)
2025-10-26 03:32:21,634 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 68)
2025-10-26 03:32:21,635 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:21,865 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:32:21,866 - src.consensus.raft - INFO - Node demo-node starting election (term 69)
2025-10-26 03:32:21,866 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 69)
2025-10-26 03:32:21,866 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:22,112 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 03:32:22,112 - src.consensus.raft - INFO - Node demo-node starting election (term 70)
2025-10-26 03:32:22,112 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 70)
2025-10-26 03:32:22,112 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:22,422 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 03:32:22,422 - src.consensus.raft - INFO - Node demo-node starting election (term 71)
2025-10-26 03:32:22,422 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 71)
2025-10-26 03:32:22,423 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:22,666 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 03:32:22,666 - src.consensus.raft - INFO - Node demo-node starting election (term 72)
2025-10-26 03:32:22,666 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 72)
2025-10-26 03:32:22,666 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:22,971 - src.consensus.raft - INFO - Election timeout (0.30s > 0.29s)
2025-10-26 03:32:22,971 - src.consensus.raft - INFO - Node demo-node starting election (term 73)
2025-10-26 03:32:22,971 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 73)
2025-10-26 03:32:22,971 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:23,263 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:32:23,263 - src.consensus.raft - INFO - Node demo-node starting election (term 74)
2025-10-26 03:32:23,263 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 74)
2025-10-26 03:32:23,263 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:23,546 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:32:23,546 - src.consensus.raft - INFO - Node demo-node starting election (term 75)
2025-10-26 03:32:23,547 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 75)
2025-10-26 03:32:23,547 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:32:23,791 - src.consensus.raft - INFO - Election timeout (0.24s > 0.24s)
2025-10-26 03:32:23,791 - src.consensus.raft - INFO - Node demo-node starting election (term 76)
2025-10-26 03:32:23,791 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 76)
2025-10-26 03:32:23,791 - src.nodes.base_node - INFO - Raft state changed to: candidate
                                                                                                                                princ  Tugas-individu main  100
19.284s ❯ ^C
                                                                                                                                princ  Tugas-individu main  100
❯ python .\benchmarks\demo_cluster.py
============================================================
Distributed Synchronization System - Cluster Demo
============================================================

[IMPORTANT] CLUSTER MUST BE RUNNING FIRST!

  Terminal 1: python benchmarks/start_cluster.py
  Terminal 2: python benchmarks/demo_cluster.py (this script)

  This demo connects to the existing cluster and
  participates as a 4th node in the Raft consensus.

Select demo type:
  1. Distributed Lock Manager
  2. Distributed Queue System
  3. Distributed Cache (MESI)

Enter choice (1-3): 1
2025-10-26 03:40:32,536 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 03:40:32,537 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 03:40:32,537 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 03:40:32,537 - src.nodes.base_node - INFO - BaseNode demo-node initialized on localhost:6000

Starting lock node demo-node (cluster mode)...
Connecting to cluster nodes...
2025-10-26 03:40:32,537 - src.nodes.base_node - INFO - Starting node demo-node...
2025-10-26 03:40:32,547 - src.communication.message_passing - INFO - Message passing server started on localhost:6000
2025-10-26 03:40:32,547 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 03:40:32,547 - src.consensus.raft - INFO - Raft node demo-node started as follower
2025-10-26 03:40:32,547 - src.nodes.base_node - INFO - Connecting to cluster nodes...
2025-10-26 03:40:32,549 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 03:40:32,550 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 03:40:32,552 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 03:40:32,552 - src.nodes.base_node - INFO - Node demo-node started successfully
2025-10-26 03:40:32,553 - src.nodes.lock_manager - INFO - Distributed Lock Manager started
Waiting for cluster to stabilize...
2025-10-26 03:40:32,814 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 03:40:32,815 - src.consensus.raft - INFO - Node demo-node starting election (term 1)
2025-10-26 03:40:32,815 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 1)
2025-10-26 03:40:32,815 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:33,109 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:40:33,109 - src.consensus.raft - INFO - Node demo-node starting election (term 2)
2025-10-26 03:40:33,109 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 2)
2025-10-26 03:40:33,109 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:33,265 - src.consensus.raft - INFO - Election timeout (0.16s > 0.15s)
2025-10-26 03:40:33,265 - src.consensus.raft - INFO - Node demo-node starting election (term 3)
2025-10-26 03:40:33,265 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 3)
2025-10-26 03:40:33,265 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:33,451 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 03:40:33,451 - src.consensus.raft - INFO - Node demo-node starting election (term 4)
2025-10-26 03:40:33,451 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 4)
2025-10-26 03:40:33,451 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:33,668 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 03:40:33,668 - src.consensus.raft - INFO - Node demo-node starting election (term 5)
2025-10-26 03:40:33,668 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 5)
2025-10-26 03:40:33,668 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:33,837 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:40:33,837 - src.consensus.raft - INFO - Node demo-node starting election (term 6)
2025-10-26 03:40:33,837 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 6)
2025-10-26 03:40:33,837 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:34,100 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:34,100 - src.consensus.raft - INFO - Node demo-node starting election (term 7)
2025-10-26 03:40:34,100 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 7)
2025-10-26 03:40:34,100 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:34,393 - src.consensus.raft - INFO - Election timeout (0.29s > 0.29s)
2025-10-26 03:40:34,394 - src.consensus.raft - INFO - Node demo-node starting election (term 8)
2025-10-26 03:40:34,394 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 8)
2025-10-26 03:40:34,394 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:34,563 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:40:34,563 - src.consensus.raft - INFO - Node demo-node starting election (term 9)
2025-10-26 03:40:34,563 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 9)
2025-10-26 03:40:34,563 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:34,855 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 03:40:34,855 - src.consensus.raft - INFO - Node demo-node starting election (term 10)
2025-10-26 03:40:34,855 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 10)
2025-10-26 03:40:34,856 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:35,055 - src.consensus.raft - INFO - Election timeout (0.20s > 0.18s)
2025-10-26 03:40:35,056 - src.consensus.raft - INFO - Node demo-node starting election (term 11)
2025-10-26 03:40:35,056 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 11)
2025-10-26 03:40:35,056 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:35,333 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 03:40:35,334 - src.consensus.raft - INFO - Node demo-node starting election (term 12)
2025-10-26 03:40:35,334 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 12)
2025-10-26 03:40:35,334 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:35,612 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:40:35,612 - src.consensus.raft - INFO - Node demo-node starting election (term 13)
2025-10-26 03:40:35,612 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 13)
2025-10-26 03:40:35,612 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:35,920 - src.consensus.raft - INFO - Election timeout (0.31s > 0.29s)
2025-10-26 03:40:35,920 - src.consensus.raft - INFO - Node demo-node starting election (term 14)
2025-10-26 03:40:35,920 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 14)
2025-10-26 03:40:35,920 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:36,229 - src.consensus.raft - INFO - Election timeout (0.31s > 0.29s)
2025-10-26 03:40:36,229 - src.consensus.raft - INFO - Node demo-node starting election (term 15)
2025-10-26 03:40:36,229 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 15)
2025-10-26 03:40:36,229 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:36,462 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 03:40:36,462 - src.consensus.raft - INFO - Node demo-node starting election (term 16)
2025-10-26 03:40:36,462 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 16)
2025-10-26 03:40:36,462 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:36,663 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 03:40:36,664 - src.consensus.raft - INFO - Node demo-node starting election (term 17)
2025-10-26 03:40:36,664 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 17)
2025-10-26 03:40:36,664 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:36,834 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:40:36,834 - src.consensus.raft - INFO - Node demo-node starting election (term 18)
2025-10-26 03:40:36,834 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 18)
2025-10-26 03:40:36,834 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:37,115 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:40:37,115 - src.consensus.raft - INFO - Node demo-node starting election (term 19)
2025-10-26 03:40:37,115 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 19)
2025-10-26 03:40:37,115 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:37,313 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 03:40:37,314 - src.consensus.raft - INFO - Node demo-node starting election (term 20)
2025-10-26 03:40:37,314 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 20)
2025-10-26 03:40:37,314 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:37,531 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 03:40:37,531 - src.consensus.raft - INFO - Node demo-node starting election (term 21)
2025-10-26 03:40:37,531 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 21)
2025-10-26 03:40:37,532 - src.nodes.base_node - INFO - Raft state changed to: candidate

============================================================
DEMO: Distributed Lock Manager (Cluster Mode)
============================================================

[INFO] Waiting for cluster synchronization...
2025-10-26 03:40:37,730 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 03:40:37,730 - src.consensus.raft - INFO - Node demo-node starting election (term 22)
2025-10-26 03:40:37,731 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 22)
2025-10-26 03:40:37,731 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:37,899 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 03:40:37,899 - src.consensus.raft - INFO - Node demo-node starting election (term 23)
2025-10-26 03:40:37,899 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 23)
2025-10-26 03:40:37,900 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:38,160 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:38,160 - src.consensus.raft - INFO - Node demo-node starting election (term 24)
2025-10-26 03:40:38,160 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 24)
2025-10-26 03:40:38,161 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:38,437 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:40:38,437 - src.consensus.raft - INFO - Node demo-node starting election (term 25)
2025-10-26 03:40:38,437 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 25)
2025-10-26 03:40:38,437 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:38,546 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-1:localhost:5000 (phi=0.00)
2025-10-26 03:40:38,546 - src.nodes.base_node - WARNING - Node failed: node-1:localhost:5000
2025-10-26 03:40:38,547 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-2:localhost:5010 (phi=0.00)
2025-10-26 03:40:38,547 - src.nodes.base_node - WARNING - Node failed: node-2:localhost:5010
2025-10-26 03:40:38,547 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-3:localhost:5020 (phi=0.00)
2025-10-26 03:40:38,547 - src.nodes.base_node - WARNING - Node failed: node-3:localhost:5020
2025-10-26 03:40:38,638 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 03:40:38,638 - src.consensus.raft - INFO - Node demo-node starting election (term 26)
2025-10-26 03:40:38,638 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 26)
2025-10-26 03:40:38,638 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:38,915 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:40:38,915 - src.consensus.raft - INFO - Node demo-node starting election (term 27)
2025-10-26 03:40:38,915 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 27)
2025-10-26 03:40:38,916 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:39,116 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 03:40:39,116 - src.consensus.raft - INFO - Node demo-node starting election (term 28)
2025-10-26 03:40:39,116 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 28)
2025-10-26 03:40:39,116 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:39,301 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 03:40:39,301 - src.consensus.raft - INFO - Node demo-node starting election (term 29)
2025-10-26 03:40:39,301 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 29)
2025-10-26 03:40:39,301 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:39,455 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 03:40:39,455 - src.consensus.raft - INFO - Node demo-node starting election (term 30)
2025-10-26 03:40:39,455 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 30)
2025-10-26 03:40:39,455 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:39,685 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:40:39,685 - src.consensus.raft - INFO - Node demo-node starting election (term 31)
2025-10-26 03:40:39,685 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 31)
2025-10-26 03:40:39,685 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:39,931 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 03:40:39,931 - src.consensus.raft - INFO - Node demo-node starting election (term 32)
2025-10-26 03:40:39,932 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 32)
2025-10-26 03:40:39,932 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:40,197 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:40,197 - src.consensus.raft - INFO - Node demo-node starting election (term 33)
2025-10-26 03:40:40,197 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 33)
2025-10-26 03:40:40,198 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:40,365 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 03:40:40,366 - src.consensus.raft - INFO - Node demo-node starting election (term 34)
2025-10-26 03:40:40,366 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 34)
2025-10-26 03:40:40,366 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:40,550 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 03:40:40,550 - src.consensus.raft - INFO - Node demo-node starting election (term 35)
2025-10-26 03:40:40,550 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 35)
2025-10-26 03:40:40,550 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:40,720 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 03:40:40,720 - src.consensus.raft - INFO - Node demo-node starting election (term 36)
2025-10-26 03:40:40,720 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 36)
2025-10-26 03:40:40,720 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:40,903 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 03:40:40,903 - src.consensus.raft - INFO - Node demo-node starting election (term 37)
2025-10-26 03:40:40,903 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 37)
2025-10-26 03:40:40,903 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:41,166 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:41,166 - src.consensus.raft - INFO - Node demo-node starting election (term 38)
2025-10-26 03:40:41,166 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 38)
2025-10-26 03:40:41,166 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:41,428 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:41,428 - src.consensus.raft - INFO - Node demo-node starting election (term 39)
2025-10-26 03:40:41,428 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 39)
2025-10-26 03:40:41,428 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:41,655 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:40:41,655 - src.consensus.raft - INFO - Node demo-node starting election (term 40)
2025-10-26 03:40:41,655 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 40)
2025-10-26 03:40:41,655 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:41,858 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 03:40:41,858 - src.consensus.raft - INFO - Node demo-node starting election (term 41)
2025-10-26 03:40:41,858 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 41)
2025-10-26 03:40:41,858 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:42,138 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:40:42,138 - src.consensus.raft - INFO - Node demo-node starting election (term 42)
2025-10-26 03:40:42,138 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 42)
2025-10-26 03:40:42,138 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:42,399 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 03:40:42,399 - src.consensus.raft - INFO - Node demo-node starting election (term 43)
2025-10-26 03:40:42,399 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 43)
2025-10-26 03:40:42,399 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:42,708 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 03:40:42,708 - src.consensus.raft - INFO - Node demo-node starting election (term 44)
2025-10-26 03:40:42,708 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 44)
2025-10-26 03:40:42,709 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:42,878 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 03:40:42,878 - src.consensus.raft - INFO - Node demo-node starting election (term 45)
2025-10-26 03:40:42,878 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 45)
2025-10-26 03:40:42,878 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:43,156 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 03:40:43,158 - src.consensus.raft - INFO - Node demo-node starting election (term 46)
2025-10-26 03:40:43,158 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 46)
2025-10-26 03:40:43,159 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:43,402 - src.consensus.raft - INFO - Election timeout (0.24s > 0.24s)
2025-10-26 03:40:43,402 - src.consensus.raft - INFO - Node demo-node starting election (term 47)
2025-10-26 03:40:43,402 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 47)
2025-10-26 03:40:43,402 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:43,680 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 03:40:43,680 - src.consensus.raft - INFO - Node demo-node starting election (term 48)
2025-10-26 03:40:43,680 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 48)
2025-10-26 03:40:43,680 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:43,958 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 03:40:43,958 - src.consensus.raft - INFO - Node demo-node starting election (term 49)
2025-10-26 03:40:43,958 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 49)
2025-10-26 03:40:43,958 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:44,144 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 03:40:44,144 - src.consensus.raft - INFO - Node demo-node starting election (term 50)
2025-10-26 03:40:44,145 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 50)
2025-10-26 03:40:44,145 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:44,345 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 03:40:44,345 - src.consensus.raft - INFO - Node demo-node starting election (term 51)
2025-10-26 03:40:44,345 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 51)
2025-10-26 03:40:44,345 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:44,575 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 03:40:44,576 - src.consensus.raft - INFO - Node demo-node starting election (term 52)
2025-10-26 03:40:44,576 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 52)
2025-10-26 03:40:44,576 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:44,822 - src.consensus.raft - INFO - Election timeout (0.25s > 0.23s)
2025-10-26 03:40:44,822 - src.consensus.raft - INFO - Node demo-node starting election (term 53)
2025-10-26 03:40:44,822 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 53)
2025-10-26 03:40:44,822 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:45,070 - src.consensus.raft - INFO - Election timeout (0.25s > 0.23s)
2025-10-26 03:40:45,070 - src.consensus.raft - INFO - Node demo-node starting election (term 54)
2025-10-26 03:40:45,070 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 54)
2025-10-26 03:40:45,070 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 03:40:45,379 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 03:40:45,379 - src.consensus.raft - INFO - Node demo-node starting election (term 55)
2025-10-26 03:40:45,379 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 55)
2025-10-26 03:40:45,379 - src.nodes.base_node - INFO - Raft state changed to: candidate

1. Acquiring exclusive lock on 'resource-1'...
2025-10-26 03:40:45,563 - src.nodes.base_node - INFO - Not leader, cannot submit command
2025-10-26 03:40:45,563 - src.nodes.lock_manager - WARNING - Failed to submit lock request for resource-1
   Result: FAILED

2. Trying to acquire shared lock on same resource (should wait)...
2025-10-26 03:40:45,564 - src.nodes.base_node - INFO - Not leader, cannot submit command
2025-10-26 03:40:45,564 - src.nodes.lock_manager - WARNING - Failed to submit lock request for resource-1
   Result: TIMEOUT (Expected)

3. Releasing lock from client-1...
2025-10-26 03:40:45,564 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Lock released

4. Lock Status:
   Total locks: 0
   Active clients: 0

