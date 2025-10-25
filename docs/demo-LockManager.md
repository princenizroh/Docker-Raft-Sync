2.255s ❯ python .\benchmarks\demo.py
============================================================
Distributed Synchronization System - Demo
============================================================

Select demo type:
  1. Distributed Lock Manager
  2. Distributed Queue System
  3. Distributed Cache (MESI)

Enter choice (1-3): 1
2025-10-26 01:21:25,255 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:21:25,255 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:21:25,255 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:21:25,256 - src.nodes.base_node - INFO - BaseNode demo-node initialized on localhost:6000

Starting lock node demo-node...
2025-10-26 01:21:25,256 - src.nodes.base_node - INFO - Starting node demo-node...
2025-10-26 01:21:25,273 - src.communication.message_passing - INFO - Message passing server started on localhost:6000
2025-10-26 01:21:25,273 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:21:25,273 - src.consensus.raft - INFO - Raft node demo-node started as follower
2025-10-26 01:21:25,273 - src.nodes.base_node - INFO - Connecting to cluster nodes...
2025-10-26 01:21:25,275 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:21:25,276 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:21:25,277 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:21:25,277 - src.nodes.base_node - INFO - Node demo-node started successfully
2025-10-26 01:21:25,277 - src.nodes.lock_manager - INFO - Distributed Lock Manager started
Waiting for cluster to stabilize...
2025-10-26 01:21:25,435 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 01:21:25,435 - src.consensus.raft - INFO - Node demo-node starting election (term 1)
2025-10-26 01:21:25,435 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 1)
2025-10-26 01:21:25,435 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:25,612 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 01:21:25,612 - src.consensus.raft - INFO - Node demo-node starting election (term 2)
2025-10-26 01:21:25,612 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 2)
2025-10-26 01:21:25,612 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:25,878 - src.consensus.raft - INFO - Election timeout (0.27s > 0.25s)
2025-10-26 01:21:25,878 - src.consensus.raft - INFO - Node demo-node starting election (term 3)
2025-10-26 01:21:25,878 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 3)
2025-10-26 01:21:25,878 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:26,080 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:26,080 - src.consensus.raft - INFO - Node demo-node starting election (term 4)
2025-10-26 01:21:26,080 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 4)
2025-10-26 01:21:26,081 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:26,249 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:21:26,250 - src.consensus.raft - INFO - Node demo-node starting election (term 5)
2025-10-26 01:21:26,250 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 5)
2025-10-26 01:21:26,250 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:26,479 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:21:26,479 - src.consensus.raft - INFO - Node demo-node starting election (term 6)
2025-10-26 01:21:26,480 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 6)
2025-10-26 01:21:26,480 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:26,727 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:26,727 - src.consensus.raft - INFO - Node demo-node starting election (term 7)
2025-10-26 01:21:26,727 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 7)
2025-10-26 01:21:26,727 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:26,898 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:26,898 - src.consensus.raft - INFO - Node demo-node starting election (term 8)
2025-10-26 01:21:26,899 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 8)
2025-10-26 01:21:26,899 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:27,208 - src.consensus.raft - INFO - Election timeout (0.31s > 0.29s)
2025-10-26 01:21:27,208 - src.consensus.raft - INFO - Node demo-node starting election (term 9)
2025-10-26 01:21:27,208 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 9)
2025-10-26 01:21:27,208 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:27,439 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:21:27,439 - src.consensus.raft - INFO - Node demo-node starting election (term 10)
2025-10-26 01:21:27,439 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 10)
2025-10-26 01:21:27,440 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:27,608 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:21:27,609 - src.consensus.raft - INFO - Node demo-node starting election (term 11)
2025-10-26 01:21:27,609 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 11)
2025-10-26 01:21:27,609 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:27,776 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:27,776 - src.consensus.raft - INFO - Node demo-node starting election (term 12)
2025-10-26 01:21:27,776 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 12)
2025-10-26 01:21:27,776 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:27,947 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:21:27,947 - src.consensus.raft - INFO - Node demo-node starting election (term 13)
2025-10-26 01:21:27,947 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 13)
2025-10-26 01:21:27,948 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:28,211 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:21:28,211 - src.consensus.raft - INFO - Node demo-node starting election (term 14)
2025-10-26 01:21:28,211 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 14)
2025-10-26 01:21:28,211 - src.nodes.base_node - INFO - Raft state changed to: candidate

============================================================
DEMO: Distributed Lock Manager
============================================================
Waiting for leader election...
2025-10-26 01:21:28,397 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:21:28,397 - src.consensus.raft - INFO - Node demo-node starting election (term 15)
2025-10-26 01:21:28,397 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 15)
2025-10-26 01:21:28,397 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:28,676 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:21:28,677 - src.consensus.raft - INFO - Node demo-node starting election (term 16)
2025-10-26 01:21:28,677 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 16)
2025-10-26 01:21:28,677 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:28,908 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:21:28,908 - src.consensus.raft - INFO - Node demo-node starting election (term 17)
2025-10-26 01:21:28,908 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 17)
2025-10-26 01:21:28,908 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:29,109 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:29,109 - src.consensus.raft - INFO - Node demo-node starting election (term 18)
2025-10-26 01:21:29,109 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 18)
2025-10-26 01:21:29,109 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:29,339 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:21:29,339 - src.consensus.raft - INFO - Node demo-node starting election (term 19)
2025-10-26 01:21:29,340 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 19)
2025-10-26 01:21:29,340 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:29,616 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:21:29,616 - src.consensus.raft - INFO - Node demo-node starting election (term 20)
2025-10-26 01:21:29,616 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 20)
2025-10-26 01:21:29,616 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:29,925 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 01:21:29,925 - src.consensus.raft - INFO - Node demo-node starting election (term 21)
2025-10-26 01:21:29,925 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 21)
2025-10-26 01:21:29,925 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:30,205 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:21:30,205 - src.consensus.raft - INFO - Node demo-node starting election (term 22)
2025-10-26 01:21:30,205 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 22)
2025-10-26 01:21:30,205 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:30,422 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:30,422 - src.consensus.raft - INFO - Node demo-node starting election (term 23)
2025-10-26 01:21:30,422 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 23)
2025-10-26 01:21:30,422 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:30,643 - src.consensus.raft - INFO - Election timeout (0.22s > 0.22s)
2025-10-26 01:21:30,643 - src.consensus.raft - INFO - Node demo-node starting election (term 24)
2025-10-26 01:21:30,644 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 24)
2025-10-26 01:21:30,644 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:30,910 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:21:30,910 - src.consensus.raft - INFO - Node demo-node starting election (term 25)
2025-10-26 01:21:30,910 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 25)
2025-10-26 01:21:30,910 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:31,171 - src.consensus.raft - INFO - Election timeout (0.26s > 0.24s)
2025-10-26 01:21:31,171 - src.consensus.raft - INFO - Node demo-node starting election (term 26)
2025-10-26 01:21:31,171 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 26)
2025-10-26 01:21:31,171 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:31,263 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-1:localhost:5000 (phi=0.00)
2025-10-26 01:21:31,264 - src.nodes.base_node - WARNING - Node failed: node-1:localhost:5000
2025-10-26 01:21:31,264 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-2:localhost:5010 (phi=0.00)
2025-10-26 01:21:31,264 - src.nodes.base_node - WARNING - Node failed: node-2:localhost:5010
2025-10-26 01:21:31,264 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-3:localhost:5020 (phi=0.00)
2025-10-26 01:21:31,264 - src.nodes.base_node - WARNING - Node failed: node-3:localhost:5020
2025-10-26 01:21:31,362 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:21:31,362 - src.consensus.raft - INFO - Node demo-node starting election (term 27)
2025-10-26 01:21:31,362 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 27)
2025-10-26 01:21:31,362 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:31,607 - src.consensus.raft - INFO - Election timeout (0.24s > 0.24s)
2025-10-26 01:21:31,608 - src.consensus.raft - INFO - Node demo-node starting election (term 28)
2025-10-26 01:21:31,608 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 28)
2025-10-26 01:21:31,609 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:31,893 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:21:31,893 - src.consensus.raft - INFO - Node demo-node starting election (term 29)
2025-10-26 01:21:31,893 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 29)
2025-10-26 01:21:31,893 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:32,109 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:32,109 - src.consensus.raft - INFO - Node demo-node starting election (term 30)
2025-10-26 01:21:32,109 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 30)
2025-10-26 01:21:32,109 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:32,403 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:21:32,403 - src.consensus.raft - INFO - Node demo-node starting election (term 31)
2025-10-26 01:21:32,403 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 31)
2025-10-26 01:21:32,403 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:32,669 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:21:32,669 - src.consensus.raft - INFO - Node demo-node starting election (term 32)
2025-10-26 01:21:32,669 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 32)
2025-10-26 01:21:32,669 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:32,870 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:21:32,870 - src.consensus.raft - INFO - Node demo-node starting election (term 33)
2025-10-26 01:21:32,870 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 33)
2025-10-26 01:21:32,870 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:33,042 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:33,042 - src.consensus.raft - INFO - Node demo-node starting election (term 34)
2025-10-26 01:21:33,042 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 34)
2025-10-26 01:21:33,042 - src.nodes.base_node - INFO - Raft state changed to: candidate

1. Acquiring exclusive lock on 'resource-1'...
2025-10-26 01:21:33,258 - src.nodes.base_node - INFO - Not leader, cannot submit command
2025-10-26 01:21:33,259 - src.nodes.lock_manager - WARNING - Failed to submit lock request for resource-1
   Result: FAILED

4. Lock Status:

============================================================
Demo completed! Press Ctrl+C to exit...
============================================================
2025-10-26 01:21:33,336 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:21:33,336 - src.consensus.raft - INFO - Node demo-node starting election (term 35)
2025-10-26 01:21:33,336 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 35)
2025-10-26 01:21:33,336 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:33,537 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:33,537 - src.consensus.raft - INFO - Node demo-node starting election (term 36)
2025-10-26 01:21:33,537 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 36)
2025-10-26 01:21:33,537 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:33,800 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:21:33,800 - src.consensus.raft - INFO - Node demo-node starting election (term 37)
2025-10-26 01:21:33,800 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 37)
2025-10-26 01:21:33,800 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:34,003 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:34,003 - src.consensus.raft - INFO - Node demo-node starting election (term 38)
2025-10-26 01:21:34,003 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 38)
2025-10-26 01:21:34,003 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:34,252 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:34,252 - src.consensus.raft - INFO - Node demo-node starting election (term 39)
2025-10-26 01:21:34,252 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 39)
2025-10-26 01:21:34,252 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:34,439 - src.consensus.raft - INFO - Election timeout (0.19s > 0.19s)
2025-10-26 01:21:34,440 - src.consensus.raft - INFO - Node demo-node starting election (term 40)
2025-10-26 01:21:34,440 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 40)
2025-10-26 01:21:34,440 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:34,636 - src.consensus.raft - INFO - Election timeout (0.20s > 0.18s)
2025-10-26 01:21:34,636 - src.consensus.raft - INFO - Node demo-node starting election (term 41)
2025-10-26 01:21:34,636 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 41)
2025-10-26 01:21:34,636 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:34,870 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:21:34,871 - src.consensus.raft - INFO - Node demo-node starting election (term 42)
2025-10-26 01:21:34,871 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 42)
2025-10-26 01:21:34,871 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:35,057 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:21:35,057 - src.consensus.raft - INFO - Node demo-node starting election (term 43)
2025-10-26 01:21:35,057 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 43)
2025-10-26 01:21:35,057 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:35,275 - src.consensus.raft - INFO - Election timeout (0.22s > 0.22s)
2025-10-26 01:21:35,275 - src.consensus.raft - INFO - Node demo-node starting election (term 44)
2025-10-26 01:21:35,275 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 44)
2025-10-26 01:21:35,276 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:35,492 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:35,492 - src.consensus.raft - INFO - Node demo-node starting election (term 45)
2025-10-26 01:21:35,492 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 45)
2025-10-26 01:21:35,492 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:35,758 - src.consensus.raft - INFO - Election timeout (0.27s > 0.25s)
2025-10-26 01:21:35,758 - src.consensus.raft - INFO - Node demo-node starting election (term 46)
2025-10-26 01:21:35,758 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 46)
2025-10-26 01:21:35,758 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:36,053 - src.consensus.raft - INFO - Election timeout (0.30s > 0.29s)
2025-10-26 01:21:36,053 - src.consensus.raft - INFO - Node demo-node starting election (term 47)
2025-10-26 01:21:36,053 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 47)
2025-10-26 01:21:36,053 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:36,237 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 01:21:36,237 - src.consensus.raft - INFO - Node demo-node starting election (term 48)
2025-10-26 01:21:36,238 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 48)
2025-10-26 01:21:36,238 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:36,450 - src.consensus.raft - INFO - Election timeout (0.21s > 0.21s)
2025-10-26 01:21:36,450 - src.consensus.raft - INFO - Node demo-node starting election (term 49)
2025-10-26 01:21:36,450 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 49)
2025-10-26 01:21:36,450 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:36,665 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:21:36,665 - src.consensus.raft - INFO - Node demo-node starting election (term 50)
2025-10-26 01:21:36,665 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 50)
2025-10-26 01:21:36,665 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:36,881 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:36,881 - src.consensus.raft - INFO - Node demo-node starting election (term 51)
2025-10-26 01:21:36,881 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 51)
2025-10-26 01:21:36,881 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:37,108 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:21:37,108 - src.consensus.raft - INFO - Node demo-node starting election (term 52)
2025-10-26 01:21:37,108 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 52)
2025-10-26 01:21:37,108 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:37,355 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:37,355 - src.consensus.raft - INFO - Node demo-node starting election (term 53)
2025-10-26 01:21:37,356 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 53)
2025-10-26 01:21:37,356 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:37,632 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:21:37,632 - src.consensus.raft - INFO - Node demo-node starting election (term 54)
2025-10-26 01:21:37,632 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 54)
2025-10-26 01:21:37,632 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:37,801 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:37,801 - src.consensus.raft - INFO - Node demo-node starting election (term 55)
2025-10-26 01:21:37,801 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 55)
2025-10-26 01:21:37,801 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:38,034 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:21:38,034 - src.consensus.raft - INFO - Node demo-node starting election (term 56)
2025-10-26 01:21:38,034 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 56)
2025-10-26 01:21:38,035 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:38,311 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:21:38,311 - src.consensus.raft - INFO - Node demo-node starting election (term 57)
2025-10-26 01:21:38,311 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 57)
2025-10-26 01:21:38,311 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:38,463 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 01:21:38,463 - src.consensus.raft - INFO - Node demo-node starting election (term 58)
2025-10-26 01:21:38,463 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 58)
2025-10-26 01:21:38,463 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:38,680 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:38,680 - src.consensus.raft - INFO - Node demo-node starting election (term 59)
2025-10-26 01:21:38,680 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 59)
2025-10-26 01:21:38,680 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:38,866 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:21:38,866 - src.consensus.raft - INFO - Node demo-node starting election (term 60)
2025-10-26 01:21:38,866 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 60)
2025-10-26 01:21:38,866 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:39,112 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:39,112 - src.consensus.raft - INFO - Node demo-node starting election (term 61)
2025-10-26 01:21:39,112 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 61)
2025-10-26 01:21:39,112 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:39,283 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:39,283 - src.consensus.raft - INFO - Node demo-node starting election (term 62)
2025-10-26 01:21:39,283 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 62)
2025-10-26 01:21:39,283 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:39,563 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:21:39,563 - src.consensus.raft - INFO - Node demo-node starting election (term 63)
2025-10-26 01:21:39,563 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 63)
2025-10-26 01:21:39,563 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:39,811 - src.consensus.raft - INFO - Election timeout (0.25s > 0.25s)
2025-10-26 01:21:39,811 - src.consensus.raft - INFO - Node demo-node starting election (term 64)
2025-10-26 01:21:39,811 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 64)
2025-10-26 01:21:39,811 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:39,982 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:21:39,982 - src.consensus.raft - INFO - Node demo-node starting election (term 65)
2025-10-26 01:21:39,982 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 65)
2025-10-26 01:21:39,982 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:40,185 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:21:40,185 - src.consensus.raft - INFO - Node demo-node starting election (term 66)
2025-10-26 01:21:40,185 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 66)
2025-10-26 01:21:40,186 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:40,432 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:40,432 - src.consensus.raft - INFO - Node demo-node starting election (term 67)
2025-10-26 01:21:40,432 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 67)
2025-10-26 01:21:40,432 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:40,664 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:21:40,664 - src.consensus.raft - INFO - Node demo-node starting election (term 68)
2025-10-26 01:21:40,664 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 68)
2025-10-26 01:21:40,664 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:40,911 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:40,911 - src.consensus.raft - INFO - Node demo-node starting election (term 69)
2025-10-26 01:21:40,911 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 69)
2025-10-26 01:21:40,911 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:41,100 - src.consensus.raft - INFO - Election timeout (0.19s > 0.19s)
2025-10-26 01:21:41,100 - src.consensus.raft - INFO - Node demo-node starting election (term 70)
2025-10-26 01:21:41,100 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 70)
2025-10-26 01:21:41,100 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:41,285 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 01:21:41,285 - src.consensus.raft - INFO - Node demo-node starting election (term 71)
2025-10-26 01:21:41,285 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 71)
2025-10-26 01:21:41,285 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:41,521 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 01:21:41,521 - src.consensus.raft - INFO - Node demo-node starting election (term 72)
2025-10-26 01:21:41,521 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 72)
2025-10-26 01:21:41,521 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:41,814 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:21:41,814 - src.consensus.raft - INFO - Node demo-node starting election (term 73)
2025-10-26 01:21:41,814 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 73)
2025-10-26 01:21:41,814 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:42,122 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 01:21:42,122 - src.consensus.raft - INFO - Node demo-node starting election (term 74)
2025-10-26 01:21:42,122 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 74)
2025-10-26 01:21:42,122 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:42,276 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 01:21:42,276 - src.consensus.raft - INFO - Node demo-node starting election (term 75)
2025-10-26 01:21:42,276 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 75)
2025-10-26 01:21:42,276 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:42,449 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:21:42,449 - src.consensus.raft - INFO - Node demo-node starting election (term 76)
2025-10-26 01:21:42,449 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 76)
2025-10-26 01:21:42,449 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:42,729 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:21:42,729 - src.consensus.raft - INFO - Node demo-node starting election (term 77)
2025-10-26 01:21:42,729 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 77)
2025-10-26 01:21:42,729 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:43,007 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:21:43,007 - src.consensus.raft - INFO - Node demo-node starting election (term 78)
2025-10-26 01:21:43,007 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 78)
2025-10-26 01:21:43,007 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:43,195 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:21:43,195 - src.consensus.raft - INFO - Node demo-node starting election (term 79)
2025-10-26 01:21:43,195 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 79)
2025-10-26 01:21:43,195 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:43,412 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:21:43,412 - src.consensus.raft - INFO - Node demo-node starting election (term 80)
2025-10-26 01:21:43,412 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 80)
2025-10-26 01:21:43,412 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:43,653 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 01:21:43,653 - src.consensus.raft - INFO - Node demo-node starting election (term 81)
2025-10-26 01:21:43,653 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 81)
2025-10-26 01:21:43,653 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:43,870 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:21:43,870 - src.consensus.raft - INFO - Node demo-node starting election (term 82)
2025-10-26 01:21:43,870 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 82)
2025-10-26 01:21:43,870 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:44,102 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:21:44,102 - src.consensus.raft - INFO - Node demo-node starting election (term 83)
2025-10-26 01:21:44,103 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 83)
2025-10-26 01:21:44,103 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:44,304 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:44,304 - src.consensus.raft - INFO - Node demo-node starting election (term 84)
2025-10-26 01:21:44,304 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 84)
2025-10-26 01:21:44,304 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:44,554 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:44,554 - src.consensus.raft - INFO - Node demo-node starting election (term 85)
2025-10-26 01:21:44,554 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 85)
2025-10-26 01:21:44,555 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:44,770 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:21:44,770 - src.consensus.raft - INFO - Node demo-node starting election (term 86)
2025-10-26 01:21:44,771 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 86)
2025-10-26 01:21:44,771 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:45,034 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:21:45,034 - src.consensus.raft - INFO - Node demo-node starting election (term 87)
2025-10-26 01:21:45,034 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 87)
2025-10-26 01:21:45,034 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:45,297 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:21:45,297 - src.consensus.raft - INFO - Node demo-node starting election (term 88)
2025-10-26 01:21:45,297 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 88)
2025-10-26 01:21:45,298 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:45,499 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:21:45,500 - src.consensus.raft - INFO - Node demo-node starting election (term 89)
2025-10-26 01:21:45,500 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 89)
2025-10-26 01:21:45,500 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:45,701 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:21:45,701 - src.consensus.raft - INFO - Node demo-node starting election (term 90)
2025-10-26 01:21:45,701 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 90)
2025-10-26 01:21:45,701 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:45,887 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:21:45,887 - src.consensus.raft - INFO - Node demo-node starting election (term 91)
2025-10-26 01:21:45,887 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 91)
2025-10-26 01:21:45,887 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:46,134 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:21:46,134 - src.consensus.raft - INFO - Node demo-node starting election (term 92)
2025-10-26 01:21:46,134 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 92)
2025-10-26 01:21:46,134 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:46,429 - src.consensus.raft - INFO - Election timeout (0.30s > 0.29s)
2025-10-26 01:21:46,429 - src.consensus.raft - INFO - Node demo-node starting election (term 93)
2025-10-26 01:21:46,429 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 93)
2025-10-26 01:21:46,429 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:46,693 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:21:46,693 - src.consensus.raft - INFO - Node demo-node starting election (term 94)
2025-10-26 01:21:46,693 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 94)
2025-10-26 01:21:46,693 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:46,990 - src.consensus.raft - INFO - Election timeout (0.30s > 0.30s)
2025-10-26 01:21:46,990 - src.consensus.raft - INFO - Node demo-node starting election (term 95)
2025-10-26 01:21:46,990 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 95)
2025-10-26 01:21:46,990 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:47,253 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:21:47,253 - src.consensus.raft - INFO - Node demo-node starting election (term 96)
2025-10-26 01:21:47,253 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 96)
2025-10-26 01:21:47,253 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:21:47,497 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 01:21:47,497 - src.consensus.raft - INFO - Node demo-node starting election (term 97)
2025-10-26 01:21:47,497 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 97)
2025-10-26 01:21:47,497 - src.nodes.base_node - INFO - Raft state changed to: candidate