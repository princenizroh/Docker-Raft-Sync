❯ python .\benchmarks\demo.py
============================================================
Distributed Synchronization System - Demo
============================================================

Select demo type:
  1. Distributed Lock Manager
  2. Distributed Queue System
  3. Distributed Cache (MESI)

Enter choice (1-3): 3
2025-10-26 01:24:04,104 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:24:04,104 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:24:04,104 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:24:04,104 - src.nodes.base_node - INFO - BaseNode demo-node initialized on localhost:6000

Starting cache node demo-node...
2025-10-26 01:24:04,104 - src.nodes.base_node - INFO - Starting node demo-node...
2025-10-26 01:24:04,115 - src.communication.message_passing - INFO - Message passing server started on localhost:6000
2025-10-26 01:24:04,115 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:24:04,115 - src.consensus.raft - INFO - Raft node demo-node started as follower
2025-10-26 01:24:04,115 - src.nodes.base_node - INFO - Connecting to cluster nodes...
2025-10-26 01:24:04,116 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:24:04,117 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:24:04,119 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:24:04,119 - src.nodes.base_node - INFO - Node demo-node started successfully
Waiting for cluster to stabilize...
2025-10-26 01:24:04,361 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:24:04,361 - src.consensus.raft - INFO - Node demo-node starting election (term 1)
2025-10-26 01:24:04,361 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 1)
2025-10-26 01:24:04,361 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:04,564 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:24:04,564 - src.consensus.raft - INFO - Node demo-node starting election (term 2)
2025-10-26 01:24:04,564 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 2)
2025-10-26 01:24:04,564 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:04,795 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:24:04,795 - src.consensus.raft - INFO - Node demo-node starting election (term 3)
2025-10-26 01:24:04,795 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 3)
2025-10-26 01:24:04,795 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:05,014 - src.consensus.raft - INFO - Election timeout (0.22s > 0.22s)
2025-10-26 01:24:05,014 - src.consensus.raft - INFO - Node demo-node starting election (term 4)
2025-10-26 01:24:05,014 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 4)
2025-10-26 01:24:05,014 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:05,278 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:24:05,278 - src.consensus.raft - INFO - Node demo-node starting election (term 5)
2025-10-26 01:24:05,278 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 5)
2025-10-26 01:24:05,278 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:05,450 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:24:05,450 - src.consensus.raft - INFO - Node demo-node starting election (term 6)
2025-10-26 01:24:05,450 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 6)
2025-10-26 01:24:05,450 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:05,700 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:24:05,700 - src.consensus.raft - INFO - Node demo-node starting election (term 7)
2025-10-26 01:24:05,700 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 7)
2025-10-26 01:24:05,700 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:05,869 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:24:05,869 - src.consensus.raft - INFO - Node demo-node starting election (term 8)
2025-10-26 01:24:05,869 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 8)
2025-10-26 01:24:05,869 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:06,041 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:24:06,041 - src.consensus.raft - INFO - Node demo-node starting election (term 9)
2025-10-26 01:24:06,041 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 9)
2025-10-26 01:24:06,041 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:06,228 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:24:06,228 - src.consensus.raft - INFO - Node demo-node starting election (term 10)
2025-10-26 01:24:06,229 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 10)
2025-10-26 01:24:06,229 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:06,432 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:24:06,432 - src.consensus.raft - INFO - Node demo-node starting election (term 11)
2025-10-26 01:24:06,433 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 11)
2025-10-26 01:24:06,433 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:06,661 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:24:06,661 - src.consensus.raft - INFO - Node demo-node starting election (term 12)
2025-10-26 01:24:06,661 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 12)
2025-10-26 01:24:06,661 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:06,865 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:24:06,865 - src.consensus.raft - INFO - Node demo-node starting election (term 13)
2025-10-26 01:24:06,865 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 13)
2025-10-26 01:24:06,865 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:07,050 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:24:07,050 - src.consensus.raft - INFO - Node demo-node starting election (term 14)
2025-10-26 01:24:07,050 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 14)
2025-10-26 01:24:07,050 - src.nodes.base_node - INFO - Raft state changed to: candidate

============================================================
DEMO: Distributed Cache (MESI Protocol)
============================================================
Waiting for leader election...
2025-10-26 01:24:07,346 - src.consensus.raft - INFO - Election timeout (0.30s > 0.29s)
2025-10-26 01:24:07,346 - src.consensus.raft - INFO - Node demo-node starting election (term 15)
2025-10-26 01:24:07,346 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 15)
2025-10-26 01:24:07,346 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:07,652 - src.consensus.raft - INFO - Election timeout (0.31s > 0.29s)
2025-10-26 01:24:07,652 - src.consensus.raft - INFO - Node demo-node starting election (term 16)
2025-10-26 01:24:07,652 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 16)
2025-10-26 01:24:07,652 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:07,946 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:24:07,946 - src.consensus.raft - INFO - Node demo-node starting election (term 17)
2025-10-26 01:24:07,946 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 17)
2025-10-26 01:24:07,946 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:08,164 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:24:08,164 - src.consensus.raft - INFO - Node demo-node starting election (term 18)
2025-10-26 01:24:08,164 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 18)
2025-10-26 01:24:08,164 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:08,349 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:24:08,349 - src.consensus.raft - INFO - Node demo-node starting election (term 19)
2025-10-26 01:24:08,349 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 19)
2025-10-26 01:24:08,349 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:08,535 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:24:08,535 - src.consensus.raft - INFO - Node demo-node starting election (term 20)
2025-10-26 01:24:08,535 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 20)
2025-10-26 01:24:08,535 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:08,798 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:24:08,798 - src.consensus.raft - INFO - Node demo-node starting election (term 21)
2025-10-26 01:24:08,798 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 21)
2025-10-26 01:24:08,798 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:09,078 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 01:24:09,078 - src.consensus.raft - INFO - Node demo-node starting election (term 22)
2025-10-26 01:24:09,078 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 22)
2025-10-26 01:24:09,078 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:09,108 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-1:localhost:5000 (phi=0.00)
2025-10-26 01:24:09,108 - src.nodes.base_node - WARNING - Node failed: node-1:localhost:5000
2025-10-26 01:24:09,108 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-2:localhost:5010 (phi=0.00)
2025-10-26 01:24:09,108 - src.nodes.base_node - WARNING - Node failed: node-2:localhost:5010
2025-10-26 01:24:09,108 - src.communication.failure_detector - WARNING - Node marked as FAILED: node-3:localhost:5020 (phi=0.00)
2025-10-26 01:24:09,108 - src.nodes.base_node - WARNING - Node failed: node-3:localhost:5020
2025-10-26 01:24:09,373 - src.consensus.raft - INFO - Election timeout (0.30s > 0.29s)
2025-10-26 01:24:09,373 - src.consensus.raft - INFO - Node demo-node starting election (term 23)
2025-10-26 01:24:09,373 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 23)
2025-10-26 01:24:09,373 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:09,588 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:24:09,588 - src.consensus.raft - INFO - Node demo-node starting election (term 24)
2025-10-26 01:24:09,588 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 24)
2025-10-26 01:24:09,589 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:09,854 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:24:09,854 - src.consensus.raft - INFO - Node demo-node starting election (term 25)
2025-10-26 01:24:09,854 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 25)
2025-10-26 01:24:09,854 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:10,134 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:24:10,135 - src.consensus.raft - INFO - Node demo-node starting election (term 26)
2025-10-26 01:24:10,135 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 26)
2025-10-26 01:24:10,135 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:10,310 - src.consensus.raft - INFO - Election timeout (0.18s > 0.16s)
2025-10-26 01:24:10,311 - src.consensus.raft - INFO - Node demo-node starting election (term 27)
2025-10-26 01:24:10,311 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 27)
2025-10-26 01:24:10,311 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:10,580 - src.consensus.raft - INFO - Election timeout (0.27s > 0.26s)
2025-10-26 01:24:10,580 - src.consensus.raft - INFO - Node demo-node starting election (term 28)
2025-10-26 01:24:10,580 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 28)
2025-10-26 01:24:10,580 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:10,844 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:24:10,845 - src.consensus.raft - INFO - Node demo-node starting election (term 29)
2025-10-26 01:24:10,845 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 29)
2025-10-26 01:24:10,845 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:11,031 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:24:11,031 - src.consensus.raft - INFO - Node demo-node starting election (term 30)
2025-10-26 01:24:11,031 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 30)
2025-10-26 01:24:11,031 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:11,200 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:24:11,200 - src.consensus.raft - INFO - Node demo-node starting election (term 31)
2025-10-26 01:24:11,200 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 31)
2025-10-26 01:24:11,200 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:11,433 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:24:11,433 - src.consensus.raft - INFO - Node demo-node starting election (term 32)
2025-10-26 01:24:11,433 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 32)
2025-10-26 01:24:11,434 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:11,712 - src.consensus.raft - INFO - Election timeout (0.28s > 0.28s)
2025-10-26 01:24:11,712 - src.consensus.raft - INFO - Node demo-node starting election (term 33)
2025-10-26 01:24:11,712 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 33)
2025-10-26 01:24:11,712 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:11,963 - src.consensus.raft - INFO - Election timeout (0.25s > 0.24s)
2025-10-26 01:24:11,963 - src.consensus.raft - INFO - Node demo-node starting election (term 34)
2025-10-26 01:24:11,963 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 34)
2025-10-26 01:24:11,963 - src.nodes.base_node - INFO - Raft state changed to: candidate

1. Putting values in cache...
2025-10-26 01:24:12,104 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Put: key-0 = value-0-1761413052.1033995... - FAILED
2025-10-26 01:24:12,150 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:24:12,150 - src.consensus.raft - INFO - Node demo-node starting election (term 35)
2025-10-26 01:24:12,150 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 35)
2025-10-26 01:24:12,150 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:12,352 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:24:12,352 - src.consensus.raft - INFO - Node demo-node starting election (term 36)
2025-10-26 01:24:12,352 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 36)
2025-10-26 01:24:12,352 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:12,600 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Put: key-1 = value-1-1761413052.6005182... - FAILED
2025-10-26 01:24:12,615 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:24:12,615 - src.consensus.raft - INFO - Node demo-node starting election (term 37)
2025-10-26 01:24:12,615 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 37)
2025-10-26 01:24:12,615 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:12,859 - src.consensus.raft - INFO - Election timeout (0.24s > 0.23s)
2025-10-26 01:24:12,859 - src.consensus.raft - INFO - Node demo-node starting election (term 38)
2025-10-26 01:24:12,859 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 38)
2025-10-26 01:24:12,859 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:13,014 - src.consensus.raft - INFO - Election timeout (0.15s > 0.15s)
2025-10-26 01:24:13,014 - src.consensus.raft - INFO - Node demo-node starting election (term 39)
2025-10-26 01:24:13,014 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 39)
2025-10-26 01:24:13,014 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:13,108 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Put: key-2 = value-2-1761413053.1073472... - FAILED
2025-10-26 01:24:13,276 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:24:13,276 - src.consensus.raft - INFO - Node demo-node starting election (term 40)
2025-10-26 01:24:13,276 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 40)
2025-10-26 01:24:13,276 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:13,539 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:24:13,539 - src.consensus.raft - INFO - Node demo-node starting election (term 41)
2025-10-26 01:24:13,539 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 41)
2025-10-26 01:24:13,539 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:13,601 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Put: key-3 = value-3-1761413053.6010137... - FAILED
2025-10-26 01:24:13,710 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:24:13,710 - src.consensus.raft - INFO - Node demo-node starting election (term 42)
2025-10-26 01:24:13,710 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 42)
2025-10-26 01:24:13,710 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:13,881 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:24:13,881 - src.consensus.raft - INFO - Node demo-node starting election (term 43)
2025-10-26 01:24:13,881 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 43)
2025-10-26 01:24:13,881 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:14,099 - src.nodes.base_node - INFO - Not leader, cannot submit command
   Put: key-4 = value-4-1761413054.0993612... - FAILED
2025-10-26 01:24:14,145 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:24:14,145 - src.consensus.raft - INFO - Node demo-node starting election (term 44)
2025-10-26 01:24:14,146 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 44)
2025-10-26 01:24:14,146 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:14,409 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:24:14,409 - src.consensus.raft - INFO - Node demo-node starting election (term 45)
2025-10-26 01:24:14,409 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 45)
2025-10-26 01:24:14,409 - src.nodes.base_node - INFO - Raft state changed to: candidate

2. Getting values from cache...
   Get: key-0 = value-0-1761413052.1033995...
2025-10-26 01:24:14,690 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:24:14,690 - src.consensus.raft - INFO - Node demo-node starting election (term 46)
2025-10-26 01:24:14,691 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 46)
2025-10-26 01:24:14,691 - src.nodes.base_node - INFO - Raft state changed to: candidate
   Get: key-1 = value-1-1761413052.6005182...
2025-10-26 01:24:14,908 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:24:14,908 - src.consensus.raft - INFO - Node demo-node starting election (term 47)
2025-10-26 01:24:14,909 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 47)
2025-10-26 01:24:14,909 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:15,095 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:24:15,095 - src.consensus.raft - INFO - Node demo-node starting election (term 48)
2025-10-26 01:24:15,095 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 48)
2025-10-26 01:24:15,095 - src.nodes.base_node - INFO - Raft state changed to: candidate
   Get: key-2 = value-2-1761413053.1073472...
2025-10-26 01:24:15,297 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:24:15,297 - src.consensus.raft - INFO - Node demo-node starting election (term 49)
2025-10-26 01:24:15,297 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 49)
2025-10-26 01:24:15,297 - src.nodes.base_node - INFO - Raft state changed to: candidate
2025-10-26 01:24:15,453 - src.consensus.raft - INFO - Election timeout (0.16s > 0.15s)
2025-10-26 01:24:15,453 - src.consensus.raft - INFO - Node demo-node starting election (term 50)
2025-10-26 01:24:15,453 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 50)
2025-10-26 01:24:15,453 - src.nodes.base_node - INFO - Raft state changed to: candidate
   Get: key-3 = value-3-1761413053.6010137...
2025-10-26 01:24:15,624 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:24:15,624 - src.consensus.raft - INFO - Node demo-node starting election (term 51)
2025-10-26 01:24:15,624 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 51)
2025-10-26 01:24:15,624 - src.nodes.base_node - INFO - Raft state changed to: candidate
   Get: key-4 = value-4-1761413054.0993612...
2025-10-26 01:24:15,843 - src.consensus.raft - INFO - Election timeout (0.22s > 0.22s)
2025-10-26 01:24:15,843 - src.consensus.raft - INFO - Node demo-node starting election (term 52)
2025-10-26 01:24:15,843 - src.consensus.raft - INFO - Node demo-node became CANDIDATE (term 52)
2025-10-26 01:24:15,843 - src.nodes.base_node - INFO - Raft state changed to: candidate

3. Cache Statistics:
2025-10-26 01:24:16,090 - src.nodes.base_node - INFO - Stopping node demo-node...
2025-10-26 01:24:16,090 - src.consensus.raft - INFO - Raft node demo-node stopped
2025-10-26 01:24:16,090 - src.communication.failure_detector - INFO - Failure detector stopped
2025-10-26 01:24:16,091 - src.communication.message_passing - INFO - Connection closed: node-1:localhost:5000
2025-10-26 01:24:16,091 - src.communication.message_passing - INFO - Connection closed: node-2:localhost:5010
2025-10-26 01:24:16,093 - src.communication.message_passing - INFO - Connection closed: node-3:localhost:5020
Traceback (most recent call last):
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\demo.py", line 171, in run_demo_on_node
    await demo_func(node)
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\demo.py", line 118, in demo_cache
    stats = cache.get_cache_stats()
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\..\src\nodes\cache_node.py", line 364, in get_cache_stats
    for key in self.cache.keys():
RuntimeError: OrderedDict mutated during iteration

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\demo.py", line 217, in <module>
    main()
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\demo.py", line 213, in main
    asyncio.run(run_demo_on_node(node_type, "demo-node", 6000))
  File "C:\Users\princ\scoop\apps\python310\current\lib\asyncio\runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "C:\Users\princ\scoop\apps\python310\current\lib\asyncio\base_events.py", line 649, in run_until_complete
    return future.result()
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\demo.py", line 184, in run_demo_on_node
    await node.stop()
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\..\src\nodes\base_node.py", line 136, in stop
    await self.message_passing.stop()
  File "D:\Pemrograman\Python\Tugas-individu\distributed-sync-system\benchmarks\..\src\communication\message_passing.py", line 112, in stop
    for writer in self.connections.values():
RuntimeError: dictionary changed size during iteration
                                                                       