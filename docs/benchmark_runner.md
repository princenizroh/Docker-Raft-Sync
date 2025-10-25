 python .\benchmarks\benchmark_runner.py  

======================================================================
  DISTRIBUTED SYSTEM PERFORMANCE BENCHMARK
======================================================================

[X][X] Benchmarking Raft Consensus...
2025-10-26 01:20:48,319 - src.consensus.raft - INFO - Raft node node-1 started as follower
2025-10-26 01:20:48,319 - src.consensus.raft - INFO - Raft node node-2 started as follower
2025-10-26 01:20:48,320 - src.consensus.raft - INFO - Raft node node-3 started as follower
2025-10-26 01:20:48,501 - src.consensus.raft - INFO - Election timeout (0.18s > 0.18s)
2025-10-26 01:20:48,501 - src.consensus.raft - INFO - Node node-1 starting election (term 1)
2025-10-26 01:20:48,501 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 1)
2025-10-26 01:20:48,531 - src.consensus.raft - INFO - Election timeout (0.21s > 0.20s)
2025-10-26 01:20:48,531 - src.consensus.raft - INFO - Node node-3 starting election (term 1)
2025-10-26 01:20:48,531 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 1)
2025-10-26 01:20:48,562 - src.consensus.raft - INFO - Election timeout (0.24s > 0.24s)
2025-10-26 01:20:48,562 - src.consensus.raft - INFO - Node node-2 starting election (term 1)
2025-10-26 01:20:48,562 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 1)
2025-10-26 01:20:48,702 - src.consensus.raft - INFO - Election timeout (0.17s > 0.16s)
2025-10-26 01:20:48,702 - src.consensus.raft - INFO - Node node-3 starting election (term 2)
2025-10-26 01:20:48,702 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 2)
2025-10-26 01:20:48,779 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:20:48,779 - src.consensus.raft - INFO - Node node-1 starting election (term 2)
2025-10-26 01:20:48,779 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 2)
2025-10-26 01:20:48,826 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:20:48,826 - src.consensus.raft - INFO - Node node-2 starting election (term 2)
2025-10-26 01:20:48,826 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 2)
2025-10-26 01:20:48,888 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:20:48,888 - src.consensus.raft - INFO - Node node-3 starting election (term 3)
2025-10-26 01:20:48,888 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 3)
2025-10-26 01:20:48,968 - src.consensus.raft - INFO - Election timeout (0.19s > 0.19s)
2025-10-26 01:20:48,968 - src.consensus.raft - INFO - Node node-1 starting election (term 3)
2025-10-26 01:20:48,969 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 3)
2025-10-26 01:20:49,015 - src.consensus.raft - INFO - Election timeout (0.19s > 0.17s)
2025-10-26 01:20:49,015 - src.consensus.raft - INFO - Node node-2 starting election (term 3)
2025-10-26 01:20:49,015 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 3)
2025-10-26 01:20:49,077 - src.consensus.raft - INFO - Election timeout (0.19s > 0.18s)
2025-10-26 01:20:49,080 - src.consensus.raft - INFO - Node node-3 starting election (term 4)
2025-10-26 01:20:49,080 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 4)
2025-10-26 01:20:49,263 - src.consensus.raft - INFO - Election timeout (0.29s > 0.28s)
2025-10-26 01:20:49,263 - src.consensus.raft - INFO - Node node-1 starting election (term 4)
2025-10-26 01:20:49,263 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 4)
2025-10-26 01:20:49,294 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:20:49,294 - src.consensus.raft - INFO - Node node-2 starting election (term 4)
2025-10-26 01:20:49,294 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 4)
2025-10-26 01:20:49,340 - src.consensus.raft - INFO - Election timeout (0.26s > 0.25s)
2025-10-26 01:20:49,340 - src.consensus.raft - INFO - Node node-3 starting election (term 5)
2025-10-26 01:20:49,341 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 5)
2025-10-26 01:20:49,510 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:20:49,510 - src.consensus.raft - INFO - Node node-2 starting election (term 5)
2025-10-26 01:20:49,511 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 5)
2025-10-26 01:20:49,526 - src.consensus.raft - INFO - Election timeout (0.26s > 0.26s)
2025-10-26 01:20:49,526 - src.consensus.raft - INFO - Node node-1 starting election (term 5)
2025-10-26 01:20:49,527 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 5)
2025-10-26 01:20:49,619 - src.consensus.raft - INFO - Election timeout (0.28s > 0.27s)
2025-10-26 01:20:49,619 - src.consensus.raft - INFO - Node node-3 starting election (term 6)
2025-10-26 01:20:49,620 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 6)
2025-10-26 01:20:49,728 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:20:49,728 - src.consensus.raft - INFO - Node node-2 starting election (term 6)
2025-10-26 01:20:49,728 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 6)
2025-10-26 01:20:49,744 - src.consensus.raft - INFO - Election timeout (0.22s > 0.20s)
2025-10-26 01:20:49,744 - src.consensus.raft - INFO - Node node-1 starting election (term 6)
2025-10-26 01:20:49,744 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 6)
2025-10-26 01:20:49,821 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:20:49,821 - src.consensus.raft - INFO - Node node-3 starting election (term 7)
2025-10-26 01:20:49,821 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 7)
2025-10-26 01:20:49,899 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:20:49,899 - src.consensus.raft - INFO - Node node-2 starting election (term 7)
2025-10-26 01:20:49,900 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 7)
2025-10-26 01:20:49,914 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 01:20:49,914 - src.consensus.raft - INFO - Node node-1 starting election (term 7)
2025-10-26 01:20:49,914 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 7)
2025-10-26 01:20:50,053 - src.consensus.raft - INFO - Election timeout (0.23s > 0.22s)
2025-10-26 01:20:50,053 - src.consensus.raft - INFO - Node node-3 starting election (term 8)
2025-10-26 01:20:50,053 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 8)
2025-10-26 01:20:50,068 - src.consensus.raft - INFO - Election timeout (0.17s > 0.15s)
2025-10-26 01:20:50,068 - src.consensus.raft - INFO - Node node-2 starting election (term 8)
2025-10-26 01:20:50,068 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 8)
2025-10-26 01:20:50,192 - src.consensus.raft - INFO - Election timeout (0.28s > 0.26s)
2025-10-26 01:20:50,192 - src.consensus.raft - INFO - Node node-1 starting election (term 8)
2025-10-26 01:20:50,193 - src.consensus.raft - INFO - Node node-1 became CANDIDATE (term 8)
2025-10-26 01:20:50,239 - src.consensus.raft - INFO - Election timeout (0.17s > 0.17s)
2025-10-26 01:20:50,239 - src.consensus.raft - INFO - Node node-2 starting election (term 9)
2025-10-26 01:20:50,239 - src.consensus.raft - INFO - Node node-2 became CANDIDATE (term 9)
2025-10-26 01:20:50,255 - src.consensus.raft - INFO - Election timeout (0.20s > 0.19s)
2025-10-26 01:20:50,255 - src.consensus.raft - INFO - Node node-3 starting election (term 9)
2025-10-26 01:20:50,255 - src.consensus.raft - INFO - Node node-3 became CANDIDATE (term 9)
  [X] No leader elected
2025-10-26 01:20:50,302 - src.consensus.raft - INFO - Raft node node-1 stopped
2025-10-26 01:20:50,303 - src.consensus.raft - INFO - Raft node node-2 stopped
2025-10-26 01:20:50,303 - src.consensus.raft - INFO - Raft node node-3 stopped

======================================================================
  NOTE: Full benchmarks require running cluster.
  Use Docker Compose for complete benchmark suite.
======================================================================

======================================================================
  PERFORMANCE BENCHMARK RESULTS
======================================================================

[X] Results saved to benchmark_results.json

======================================================================
  [X] BENCHMARK COMPLETED SUCCESSFULLY
======================================================================