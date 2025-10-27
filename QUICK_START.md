# Panduan Quick Start

## ⚠️ PENTING: Persiapan Awal

### Cleanup Proses
**SELALU matikan proses Python yang berjalan sebelum memulai demo:**

```bash
# Windows PowerShell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Linux/Mac
pkill python3
```

**Mengapa?** 
- Mencegah konflik port
- Menghindari election conflicts
- Memastikan clean state untuk demo

---

## 🚀 Running Demos

### Option 1: Standalone Mode (RECOMMENDED) - Automated Script

**Using PowerShell script (easiest):**
```bash
.\run_standalone_demo.ps1
```
This script automatically:
- Kills old Python processes
- Shows menu to select demo type
- Runs fresh demo

**Manual method:**
```bash
# Kill old processes first!
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Run demo
python benchmarks/demo_standalone.py
```

Select demo type:
- `1` - Lock Manager Demo
- `2` - Queue System Demo  
- `3` - Cache (MESI) Demo

**Advantages:**
- ✅ No cluster setup needed
- ✅ Single independent node
- ✅ Immediate leader election
- ✅ Fast and easy testing

---

### Option 2: Cluster Mode (DEPRECATED - NOT WORKING)

**⚠️ WARNING: CLUSTER MODE TIDAK BERFUNGSI karena architectural limitation!**

**Masalah:**
- Demo creates node ke-4 yang join ke 3-node cluster
- 4-node cluster needs 3/4 votes untuk majority
- Demo node **TIDAK BISA dapat 3 votes** (cluster nodes don't recognize it)
- Result: **Perpetual elections**, never becomes leader
- All commands **GAGAL**: "Not leader, cannot submit command"

**Root Cause:**
- `DistributedLockManager`, `DistributedQueue`, `DistributedCache` adalah **FULL RAFT NODES**
- Demo tries to join sebagai voting member
- Raft doesn't support dynamic membership di implementation ini
- Node ke-4 tidak ter-configure di cluster nodes

**Why This Happens:**
```
Cluster: [node-1, node-2, node-3]  ← 3 nodes, majority = 2
Demo:    demo-node tries to join   ← Makes it 4 nodes, majority = 3

Election:
  demo-node: votes for self (1 vote)
  node-1:    doesn't vote for demo (not in its cluster list)
  node-2:    doesn't vote for demo (not in its cluster list)
  node-3:    doesn't vote for demo (not in its cluster list)
  
Result: demo-node gets 1/3 votes → NOT MAJORITY → Never becomes leader
```

**Solusi Yang Diperlukan (Future Work):**
1. Client API (kirim commands ke leader, bukan jadi node sendiri)
2. Command forwarding (non-leader nodes forward ke leader)
3. Dynamic membership (cluster accept new nodes runtime)

**Pakai Standalone Mode sebagai gantinya:**
```bash
python benchmarks/demo_standalone.py
# atau
.\run_standalone_demo.ps1
```

---

### ~~Option 2: Cluster Mode (Production-like)~~ DEPRECATED

**Jangan gunakan cluster mode!** Script ini exists untuk demonstrasi masalah architectural, bukan untuk actual usage.

Select demo type (1/2/3)

**Advantages:**
- ✅ Realistic distributed scenario
- ✅ Demonstrates Raft consensus
- ✅ Multi-node coordination
- ✅ Production-like behavior

---

### Option 3: Demo Selector
**Interactive menu to choose mode**

```bash
python benchmarks/demo.py
```

1. Choose mode: `1` (Standalone) or `2` (Cluster)
2. Choose demo type: `1` (Lock), `2` (Queue), or `3` (Cache)

---

## 🧪 Running Tests

### All Tests (Verbose)
```bash
pytest tests -v
```

**Expected Output:**
- ✅ 21/21 tests PASSED (100%)
- Detailed logs for each test
- Progress percentage
- Execution time

### Unit Tests Only
```bash
pytest tests/unit -v
```

### Integration Tests Only
```bash
pytest tests/integration -v
```

### Performance Tests Only
```bash
pytest tests/performance -v
```

---

## 📊 Test Configuration

Tests are configured in `pytest.ini` with:
- **Verbose mode** (`-v`) - Shows detailed test names
- **Short traceback** (`--tb=short`) - Concise error messages
- **CLI logging** (`log_cli=true`) - Shows INFO logs during tests
- **Colored output** (`--color=yes`) - Better readability

---

## � Troubleshooting

### Problem: "Not leader, cannot submit command" or perpetual elections

**Symptom:**
```
Node demo-node became CANDIDATE (term 53)
Node demo-node became CANDIDATE (term 54)
Not leader, cannot submit command
Result: FAILED
```

**Causes:** 
1. Port conflict with existing processes
2. Incorrect cluster configuration
3. Network connectivity issues
4. Firewall blocking communication

**Solution:**
```bash
# Kill ALL Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Wait a moment
Start-Sleep -Seconds 2

# Run demo fresh
python benchmarks/demo_standalone.py
```

**Expected output (correct):**
```
Node demo-node won election immediately (standalone with 1 votes)
Node demo-node became LEADER (term 1)
Result: SUCCESS
```

---

## �📁 File Structure

```
benchmarks/
├── demo.py              # Demo selector (choose mode)
├── demo_standalone.py   # Standalone demos (no cluster)
├── demo_cluster.py      # Cluster demos (requires cluster)
├── start_cluster.py     # Start 3-node cluster
└── benchmark_runner.py  # Performance benchmarks

scripts/
├── run_standalone_demo.ps1  # Automated standalone demo
└── run_cluster_demo.ps1     # Automated cluster demo

tests/
├── unit/                # Unit tests (10 tests)
├── integration/         # Integration tests (5 tests)
└── performance/         # Performance tests (6 tests)
```

---

## ✅ What's Working

### Demos (3/3)
- ✅ Lock Manager - Exclusive/Shared locks
- ✅ Queue System - Enqueue/Dequeue with partitions
- ✅ Cache System - MESI protocol

### Tests (21/21)
- ✅ **Integration** (5/5) - Cluster formation, leader election
- ✅ **Performance** (6/6) - Throughput, latency, memory
- ✅ **Unit** (10/10) - Lock manager, Raft consensus

---

## 🎯 Quick Summary

**For Testing (Easiest):**
```bash
.\run_standalone_demo.ps1
```

**For Testing (Manual):**
```bash
# IMPORTANT: Kill old processes first!
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

python benchmarks/demo_standalone.py
```

**For Production Scenario (Easiest):**
```bash
.\run_cluster_demo.ps1
```

**For Production Scenario (Manual):**
```bash
# Terminal 1
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
python benchmarks/start_cluster.py

# Terminal 2
python benchmarks/demo_cluster.py
```

**For Verification:**
```bash
pytest tests -v
```

**Remember:** Always kill old Python processes before starting demos!

All systems operational! 🎉
