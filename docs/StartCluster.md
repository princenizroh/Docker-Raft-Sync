 python .\benchmarks\start_cluster.py
============================================================
Distributed Synchronization System - Quick Start
============================================================

[OK] Python 3.10 detected
[OK] Dependencies installed
Starting node-1 on port 5000...
C:\Users\princ\scoop\apps\python310\current\lib\runpy.py:126: RuntimeWarning: 'src.nodes.base_node' found in sys.modules after import of package 'src.nodes', but prior to execution of 'src.nodes.base_node'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
2025-10-26 01:19:54,068 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:19:54,068 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:19:54,068 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:19:54,068 - __main__ - INFO - BaseNode node-1 initialized on 0.0.0.0:5000
2025-10-26 01:19:54,068 - __main__ - INFO - Starting node node-1...
2025-10-26 01:19:54,071 - src.communication.message_passing - INFO - Message passing server started on 0.0.0.0:5000
2025-10-26 01:19:54,071 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:19:54,071 - src.consensus.raft - INFO - Raft node node-1 started as follower
2025-10-26 01:19:54,071 - __main__ - INFO - Connecting to cluster nodes...
2025-10-26 01:19:54,084 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:19:54,086 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:19:54,087 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:19:54,087 - __main__ - INFO - Node node-1 started successfully
2025-10-26 01:19:54,301 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:19:54,302 - src.consensus.raft - INFO - Node node-1 starting election (term 1)
2025-10-26 01:19:54,302 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 1)
2025-10-26 01:19:54,302 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:54,503 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:19:54,503 - src.consensus.raft - INFO - Node node-1 starting election (term 2)
2025-10-26 01:19:54,503 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 2)
2025-10-26 01:19:54,504 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:54,737 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:19:54,737 - src.consensus.raft - INFO - Node node-1 starting election (term 3)
2025-10-26 01:19:54,737 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 3)
2025-10-26 01:19:54,737 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:54,907 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:19:54,907 - src.consensus.raft - INFO - Node node-1 starting election (term 4)
2025-10-26 01:19:54,907 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 4)
2025-10-26 01:19:54,907 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:55,076 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:19:55,076 - src.consensus.raft - INFO - Node node-1 starting election (term 5)
2025-10-26 01:19:55,076 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 5)
2025-10-26 01:19:55,076 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:55,292 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:19:55,292 - src.consensus.raft - INFO - Node node-1 starting election (term 6)
2025-10-26 01:19:55,292 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 6)
2025-10-26 01:19:55,292 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:55,571 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:19:55,571 - src.consensus.raft - INFO - Node node-1 starting election (term 7)
2025-10-26 01:19:55,571 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 7)
2025-10-26 01:19:55,571 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:55,756 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:19:55,756 - src.consensus.raft - INFO - Node node-1 starting election (term 8)
2025-10-26 01:19:55,756 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 8)
2025-10-26 01:19:55,757 - __main__ - INFO - Raft state changed to: candidate
Starting node-2 on port 5010...
2025-10-26 01:19:56,050 - src.consensus.raft - INFO - Election timeout (0.29s > 0.29s)
2025-10-26 01:19:56,050 - src.consensus.raft - INFO - Node node-1 starting election (term 9)
2025-10-26 01:19:56,050 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 9)
2025-10-26 01:19:56,050 - __main__ - INFO - Raft state changed to: candidate
C:\Users\princ\scoop\apps\python310\current\lib\runpy.py:126: RuntimeWarning: 'src.nodes.base_node' found in sys.modules after import of package 'src.nodes', but prior to execution of 'src.nodes.base_node'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
2025-10-26 01:19:56,072 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:19:56,072 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:19:56,072 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:19:56,073 - __main__ - INFO - BaseNode node-2 initialized on 0.0.0.0:5010
2025-10-26 01:19:56,073 - __main__ - INFO - Starting node node-2...
2025-10-26 01:19:56,073 - src.communication.message_passing - INFO - Message passing server started on 0.0.0.0:5010
2025-10-26 01:19:56,073 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:19:56,073 - src.consensus.raft - INFO - Raft node node-2 started as follower
2025-10-26 01:19:56,073 - __main__ - INFO - Connecting to cluster nodes...
2025-10-26 01:19:56,086 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:19:56,087 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:19:56,089 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:19:56,089 - __main__ - INFO - Node node-2 started successfully
2025-10-26 01:19:56,232 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 01:19:56,232 - src.consensus.raft - INFO - Node node-1 starting election (term 10)
2025-10-26 01:19:56,232 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 10)
2025-10-26 01:19:56,232 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:56,371 - src.consensus.raft - INFO - Election timeout (0.30s > 0.30s)
2025-10-26 01:19:56,371 - src.consensus.raft - INFO - Node node-2 starting election (term 1)
2025-10-26 01:19:56,371 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 1)
2025-10-26 01:19:56,371 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:56,526 - src.consensus.raft - INFO - Election timeout (0.29s > 0.29s)
2025-10-26 01:19:56,526 - src.consensus.raft - INFO - Node node-1 starting election (term 11)
2025-10-26 01:19:56,526 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 11)
2025-10-26 01:19:56,526 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:56,667 - src.consensus.raft - INFO - Election timeout (0.30s > 0.28s)
2025-10-26 01:19:56,667 - src.consensus.raft - INFO - Node node-2 starting election (term 2)
2025-10-26 01:19:56,667 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 2)
2025-10-26 01:19:56,667 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:56,821 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:19:56,821 - src.consensus.raft - INFO - Node node-1 starting election (term 12)
2025-10-26 01:19:56,821 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 12)
2025-10-26 01:19:56,821 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:56,837 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:19:56,837 - src.consensus.raft - INFO - Node node-2 starting election (term 3)
2025-10-26 01:19:56,837 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 3)
2025-10-26 01:19:56,837 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Election timeout (0.25s > 0.23s)
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Node node-1 starting election (term 13)
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Node node-2 starting election (term 4)
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 13)
2025-10-26 01:19:57,083 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 4)
2025-10-26 01:19:57,083 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,083 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,266 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 01:19:57,266 - src.consensus.raft - INFO - Node node-2 starting election (term 5)
2025-10-26 01:19:57,266 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 5)
2025-10-26 01:19:57,266 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,296 - src.consensus.raft - INFO - Election timeout (0.21s > 0.21s)
2025-10-26 01:19:57,296 - src.consensus.raft - INFO - Node node-1 starting election (term 14)
2025-10-26 01:19:57,297 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 14)
2025-10-26 01:19:57,297 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,450 - src.consensus.raft - INFO - Election timeout (0.18s > 0.17s)
2025-10-26 01:19:57,450 - src.consensus.raft - INFO - Node node-2 starting election (term 6)
2025-10-26 01:19:57,450 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 6)
2025-10-26 01:19:57,451 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,529 - src.consensus.raft - INFO - Election timeout (0.23s > 0.23s)
2025-10-26 01:19:57,529 - src.consensus.raft - INFO - Node node-1 starting election (term 15)
2025-10-26 01:19:57,530 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 15)
2025-10-26 01:19:57,530 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,669 - src.consensus.raft - INFO - Election timeout (0.22s > 0.21s)
2025-10-26 01:19:57,669 - src.consensus.raft - INFO - Node node-2 starting election (term 7)
2025-10-26 01:19:57,669 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 7)
2025-10-26 01:19:57,669 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,731 - src.consensus.raft - INFO - Election timeout (0.20s > 0.20s)
2025-10-26 01:19:57,732 - src.consensus.raft - INFO - Node node-1 starting election (term 16)
2025-10-26 01:19:57,732 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 16)
2025-10-26 01:19:57,732 - __main__ - INFO - Raft state changed to: candidate
Starting node-3 on port 5020...
2025-10-26 01:19:57,916 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 01:19:57,916 - src.consensus.raft - INFO - Node node-1 starting election (term 17)
2025-10-26 01:19:57,916 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 17)
2025-10-26 01:19:57,916 - __main__ - INFO - Raft state changed to: candidate
2025-10-26 01:19:57,965 - src.consensus.raft - INFO - Election timeout (0.30s > 0.28s)
2025-10-26 01:19:57,965 - src.consensus.raft - INFO - Node node-2 starting election (term 8)
2025-10-26 01:19:57,965 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 8)
2025-10-26 01:19:57,965 - __main__ - INFO - Raft state changed to: candidate
C:\Users\princ\scoop\apps\python310\current\lib\runpy.py:126: RuntimeWarning: 'src.nodes.base_node' found in sys.modules after import of package 'src.nodes', but prior to execution of 'src.nodes.base_node'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))
2025-10-26 01:19:58,103 - src.communication.failure_detector - INFO - Registered node for monitoring: node-1:localhost:5000
2025-10-26 01:19:58,103 - src.communication.failure_detector - INFO - Registered node for monitoring: node-2:localhost:5010
2025-10-26 01:19:58,103 - src.communication.failure_detector - INFO - Registered node for monitoring: node-3:localhost:5020
2025-10-26 01:19:58,103 - __main__ - INFO - BaseNode node-3 initialized on 0.0.0.0:5020
2025-10-26 01:19:58,103 - __main__ - INFO - Starting node node-3...
2025-10-26 01:19:58,104 - src.communication.message_passing - INFO - Message passing server started on 0.0.0.0:5020
2025-10-26 01:19:58,104 - src.communication.failure_detector - INFO - Failure detector started
2025-10-26 01:19:58,104 - src.consensus.raft - INFO - Raft node node-3 started as follower
2025-10-26 01:19:58,104 - __main__ - INFO - Connecting to cluster nodes...
2025-10-26 01:19:58,117 - src.communication.message_passing - INFO - Connected to node-1:localhost:5000
2025-10-26 01:19:58,119 - src.communication.message_passing - INFO - Connected to node-2:localhost:5010
2025-10-26 01:19:58,122 - src.communication.message_passing - INFO - Connected to node-3:localhost:5020
2025-10-26 01:19:58,123 - __main__ - INFO - Node node-3 started successfully
