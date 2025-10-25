24.48s ❯ python .\benchmarks\demo.py
============================================================
Distributed Synchronization System - Demo
============================================================

Select demo type:
  1. Distributed Lock Manager
  2. Distributed Queue System
  3. Distributed Cache (MESI)

Enter choice (1-3): 2
2025-10-26 01:22:34,762 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:22:34,762 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:22:34,762 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:22:34,762 - src.nodes.base_node - INFO - BaseNode demo-node initialized on localhost:6000

Starting queue node demo-node...
2025-10-26 01:22:34,764 - src.nodes.base_node - INFO - Starting node demo-node...
2025-10-26 01:22:34,780 - src.communication.message_passing - INFO - Message passing server started on localhost:6000
2025-10-26 01:22:34,780 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:22:34,781 - src.consensus.raft - INFO - Raft node demo-node started as follower
2025-10-26 01:22:34,781 - src.nodes.base_node - INFO - Connecting to cluster nodes...
2025-10-26 01:22:34,783 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:22:34,784 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:22:34,785 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:22:34,785 - src.nodes.base_node - INFO - Node demo-node started successfully
2025-10-26 01:22:34,803 - src.nodes.queue_node - INFO - Queue data loaded from persistence
2025-10-26 01:22:34,803 - src.nodes.queue_node - INFO - Distributed Queue started
Waiting for cluster to stabilize...
2025-10-26 01:22:34,999 - src.consensus.raft - INFO - Election timeout (0.24s > 0.22s)
2025-10-26 01:22:34,999 - src.consensus.raft - INFO - Node demo-node starting election (term 1)
2025-10-26 01:22:34,999 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 1)
2025-10-26 01:22:34,999 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:35,263 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:22:35,263 - src.consensus.raft - INFO - Node demo-node starting election (term 2)
2025-10-26 01:22:35,263 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 2)
2025-10-26 01:22:35,263 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:35,544 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:22:35,544 - src.consensus.raft - INFO - Node demo-node starting election (term 3)
2025-10-26 01:22:35,544 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 3)
2025-10-26 01:22:35,544 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:35,745 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:35,745 - src.consensus.raft - INFO - Node demo-node starting election (term 4)
2025-10-26 01:22:35,745 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 4)
2025-10-26 01:22:35,745 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:35,979 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:22:35,979 - src.consensus.raft - INFO - Node demo-node starting election (term 5)
2025-10-26 01:22:35,979 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 5)
2025-10-26 01:22:35,979 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:36,165 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:22:36,165 - src.consensus.raft - INFO - Node demo-node starting election (term 6)
2025-10-26 01:22:36,165 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 6)
2025-10-26 01:22:36,165 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:36,414 - src.consensus.raft - INFO - Election timeout (0.25s > 0.23s)
2025-10-26 01:22:36,414 - src.consensus.raft - INFO - Node demo-node starting election (term 7)
2025-10-26 01:22:36,415 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 7)
2025-10-26 01:22:36,415 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:36,648 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:22:36,649 - src.consensus.raft - INFO - Node demo-node starting election (term 8)
2025-10-26 01:22:36,649 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 8)
2025-10-26 01:22:36,649 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:36,911 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:22:36,911 - src.consensus.raft - INFO - Node demo-node starting election (term 9)
2025-10-26 01:22:36,911 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 9)
2025-10-26 01:22:36,911 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:37,206 - src.consensus.raft - INFO - Election timeout (0.30s > 0.28s)
2025-10-26 01:22:37,206 - src.consensus.raft - INFO - Node demo-node starting election (term 10)
2025-10-26 01:22:37,206 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 10)
2025-10-26 01:22:37,206 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:37,376 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:22:37,376 - src.consensus.raft - INFO - Node demo-node starting election (term 11)
2025-10-26 01:22:37,376 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 11)
2025-10-26 01:22:37,377 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:37,545 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:22:37,545 - src.consensus.raft - INFO - Node demo-node starting election (term 12)
2025-10-26 01:22:37,545 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 12)
2025-10-26 01:22:37,545 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:37,778 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:22:37,778 - src.consensus.raft - INFO - Node demo-node starting election (term 13)
2025-10-26 01:22:37,778 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 13)
2025-10-26 01:22:37,778 - src.nodes.base_node - INFO - Raft state changed to: candidate

============================================================
DEMO: Distributed Queue System
============================================================
Waiting for leader election...
2025-10-26 01:22:38,011 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:22:38,011 - src.consensus.raft - INFO - Node demo-node starting election (term 14)
2025-10-26 01:22:38,011 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 14)
2025-10-26 01:22:38,011 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:38,271 - src.consensus.raft - INFO - Election timeout (0.26s > 0.24s)
2025-10-26 01:22:38,271 - src.consensus.raft - INFO - Node demo-node starting election (term 15)
2025-10-26 01:22:38,271 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 15)
2025-10-26 01:22:38,272 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:38,472 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:38,472 - src.consensus.raft - INFO - Node demo-node starting election (term 16)
2025-10-26 01:22:38,472 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 16)
2025-10-26 01:22:38,473 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:38,627 - src.consensus.raft - INFO - Election timeout (0.16s > 0.15s)
2025-10-26 01:22:38,627 - src.consensus.raft - INFO - Node demo-node starting election (term 17)
2025-10-26 01:22:38,627 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 17)
2025-10-26 01:22:38,627 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:38,830 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:22:38,830 - src.consensus.raft - INFO - Node demo-node starting election (term 18)
2025-10-26 01:22:38,830 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 18)
2025-10-26 01:22:38,830 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:39,095 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:22:39,095 - src.consensus.raft - INFO - Node demo-node starting election (term 19)
2025-10-26 01:22:39,095 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 19)
2025-10-26 01:22:39,095 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:39,390 - src.consensus.raft - INFO - Election timeout (0.30s > 0.28s)
2025-10-26 01:22:39,391 - src.consensus.raft - INFO - Node demo-node starting election (term 20)
2025-10-26 01:22:39,391 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 20)
2025-10-26 01:22:39,391 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:39,562 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:22:39,562 - src.consensus.raft - INFO - Node demo-node starting election (term 21)
2025-10-26 01:22:39,562 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 21)
2025-10-26 01:22:39,562 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:39,731 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 01:22:39,731 - src.consensus.raft - INFO - Node demo-node starting election (term 22)
2025-10-26 01:22:39,731 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 22)
2025-10-26 01:22:39,731 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:39,762 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-1:localhost:5000 (phi=0.00)
2025-10-26 01:22:39,762 - src.nodes.base_node - WARNING - Node failed: node-1:localhost:5000
2025-10-26 01:22:39,762 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-2:localhost:5010 (phi=0.00)
2025-10-26 01:22:39,762 - src.nodes.base_node - WARNING - Node failed: node-2:localhost:5010
2025-10-26 01:22:39,763 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-3:localhost:5020 (phi=0.00)
2025-10-26 01:22:39,763 - src.nodes.base_node - WARNING - Node failed: node-3:localhost:5020
2025-10-26 01:22:40,038 - src.consensus.raft - INFO - Election timeout (0.31s > 0.29s)
2025-10-26 01:22:40,038 - src.consensus.raft - INFO - Node demo-node starting election (term 23)
2025-10-26 01:22:40,039 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 23)
2025-10-26 01:22:40,039 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:40,315 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 01:22:40,315 - src.consensus.raft - INFO - Node demo-node starting election (term 24)
2025-10-26 01:22:40,315 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 24)
2025-10-26 01:22:40,315 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:40,593 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:22:40,593 - src.consensus.raft - INFO - Node demo-node starting election (term 25)
2025-10-26 01:22:40,593 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 25)
2025-10-26 01:22:40,593 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:40,864 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:22:40,864 - src.consensus.raft - INFO - Node demo-node starting election (term 26)
2025-10-26 01:22:40,864 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 26)
2025-10-26 01:22:40,864 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:41,081 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:22:41,081 - src.consensus.raft - INFO - Node demo-node starting election (term 27)
2025-10-26 01:22:41,081 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 27)
2025-10-26 01:22:41,081 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:41,345 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:22:41,345 - src.consensus.raft - INFO - Node demo-node starting election (term 28)
2025-10-26 01:22:41,345 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 28)
2025-10-26 01:22:41,345 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:41,515 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:22:41,515 - src.consensus.raft - INFO - Node demo-node starting election (term 29)
2025-10-26 01:22:41,515 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 29)
2025-10-26 01:22:41,515 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:41,752 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 01:22:41,753 - src.consensus.raft - INFO - Node demo-node starting election (term 30)
2025-10-26 01:22:41,753 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 30)
2025-10-26 01:22:41,753 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:42,023 - src.consensus.raft - INFO - Election timeout (0.27s > 0.27s)
2025-10-26 01:22:42,024 - src.consensus.raft - INFO - Node demo-node starting election (term 31)
2025-10-26 01:22:42,024 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 31)
2025-10-26 01:22:42,024 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:42,225 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:42,225 - src.consensus.raft - INFO - Node demo-node starting election (term 32)
2025-10-26 01:22:42,225 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 32)
2025-10-26 01:22:42,225 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:42,487 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:22:42,487 - src.consensus.raft - INFO - Node demo-node starting election (term 33)
2025-10-26 01:22:42,487 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 33)
2025-10-26 01:22:42,487 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:42,702 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:22:42,702 - src.consensus.raft - INFO - Node demo-node starting election (term 34)
2025-10-26 01:22:42,702 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 34)
2025-10-26 01:22:42,702 - src.nodes.base_node - INFO - Raft state changed to: candidate

1. Enqueueing messages...
2025-10-26 01:22:42,809 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Enqueued: Message 0: Hello from distributed queue! - FAILED
2025-10-26 01:22:42,903 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:42,903 - src.consensus.raft - INFO - Node demo-node starting election (term 35)
2025-10-26 01:22:42,903 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 35)
2025-10-26 01:22:42,903 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:43,184 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:22:43,184 - src.consensus.raft - INFO - Node demo-node starting election (term 36)
2025-10-26 01:22:43,184 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 36)
2025-10-26 01:22:43,184 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:43,307 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Enqueued: Message 1: Hello from distributed queue! - FAILED
2025-10-26 01:22:43,385 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:22:43,385 - src.consensus.raft - INFO - Node demo-node starting election (term 37)
2025-10-26 01:22:43,385 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 37)
2025-10-26 01:22:43,385 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:43,586 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:22:43,587 - src.consensus.raft - INFO - Node demo-node starting election (term 38)
2025-10-26 01:22:43,587 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 38)
2025-10-26 01:22:43,587 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:43,806 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Enqueued: Message 2: Hello from distributed queue! - FAILED
2025-10-26 01:22:43,854 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:22:43,854 - src.consensus.raft - INFO - Node demo-node starting election (term 39)
2025-10-26 01:22:43,854 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 39)
2025-10-26 01:22:43,854 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:44,148 - src.consensus.raft - INFO - Election timeout (0.29s > 0.29s)
2025-10-26 01:22:44,148 - src.consensus.raft - INFO - Node demo-node starting election (term 40)
2025-10-26 01:22:44,149 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 40)
2025-10-26 01:22:44,149 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:44,300 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Enqueued: Message 3: Hello from distributed queue! - FAILED
2025-10-26 01:22:44,424 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 01:22:44,424 - src.consensus.raft - INFO - Node demo-node starting election (term 41)
2025-10-26 01:22:44,424 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 41)
2025-10-26 01:22:44,424 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:44,627 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:44,627 - src.consensus.raft - INFO - Node demo-node starting election (term 42)
2025-10-26 01:22:44,627 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 42)
2025-10-26 01:22:44,627 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:44,800 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Enqueued: Message 4: Hello from distributed queue! - FAILED
2025-10-26 01:22:44,892 - src.consensus.raft - INFO - Election timeout (0.27s > 0.25s)
2025-10-26 01:22:44,892 - src.consensus.raft - INFO - Node demo-node starting election (term 43)
2025-10-26 01:22:44,893 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 43)
2025-10-26 01:22:44,893 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:45,203 - src.consensus.raft - INFO - Election timeout (0.31s > 0.30s)
2025-10-26 01:22:45,203 - src.consensus.raft - INFO - Node demo-node starting election (term 44)
2025-10-26 01:22:45,204 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 44)
2025-10-26 01:22:45,204 - src.nodes.base_node - INFO - Raft state changed to: candidate

2. Dequeueing messages...
2025-10-26 01:22:45,311 - src.nodes.queue_node - WARNING - Not owner of partition 14
2025-10-26 01:22:45,481 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:22:45,481 - src.consensus.raft - INFO - Node demo-node starting election (term 45)
2025-10-26 01:22:45,481 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 45)
2025-10-26 01:22:45,481 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:45,691 - src.consensus.raft - INFO - Election timeout (0.21s > 0.21s)
2025-10-26 01:22:45,691 - src.consensus.raft - INFO - Node demo-node starting election (term 46)
2025-10-26 01:22:45,691 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 46)
2025-10-26 01:22:45,691 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:45,801 - src.nodes.queue_node - WARNING - Not owner of partition 14
2025-10-26 01:22:45,894 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:22:45,894 - src.consensus.raft - INFO - Node demo-node starting election (term 47)
2025-10-26 01:22:45,894 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 47)
2025-10-26 01:22:45,895 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:46,187 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:22:46,187 - src.consensus.raft - INFO - Node demo-node starting election (term 48)
2025-10-26 01:22:46,187 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 48)
2025-10-26 01:22:46,188 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:46,297 - src.nodes.queue_node - WARNING - Not owner of partition 14
2025-10-26 01:22:46,359 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:22:46,359 - src.consensus.raft - INFO - Node demo-node starting election (term 49)
2025-10-26 01:22:46,359 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 49)
2025-10-26 01:22:46,359 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:46,559 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:22:46,559 - src.consensus.raft - INFO - Node demo-node starting election (term 50)
2025-10-26 01:22:46,559 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 50)
2025-10-26 01:22:46,559 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:22:46,714 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 01:22:46,714 - src.consensus.raft - INFO - Node demo-node starting election (term 51)
2025-10-26 01:22:46,714 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 51)
2025-10-26 01:22:46,714 - src.nodes.base_node - INFO - Raft state changed to: candidate

3. Queue Statistics:
   Total messages: 0
   Partitions: 0
   Consumers: 0

============================================================
Demo completed! Press Ctrl+C to exit...
============================================================