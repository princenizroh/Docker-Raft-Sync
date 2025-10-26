# Deployment Guide - Distributed Synchronization System

## Prerequisites

**Software Requirements:**
- Python 3.8+ (Tested dengan Python 3.10.11)
- Docker 20.10+ dan Docker Compose 2.0+
- Redis 6.0+ (opsional, bisa via Docker)
- Git
- 4GB RAM minimum
- 10GB disk space

**Operating System:**
- Windows 10/11 (dengan PowerShell)
- Linux (Ubuntu 20.04+, CentOS 8+)
- macOS 11+

---

## Quick Start - Standalone Mode (Development)

### 1. Clone Repository
```bash
git clone https://github.com/princenizroh/Docker-Raft-Sync.git
cd Docker-Raft-Sync
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example config
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Edit .env sesuai kebutuhan (opsional)
```

### 4. Run Standalone Demo
```bash
# Kill old processes (Windows)
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Run demo
python benchmarks/demo_standalone.py
```

**Expected:** Node start, jadi leader, dan demo 3 layanan (Lock, Queue, Cache) berjalan.

---

## Production Deployment - 3 Node Cluster

### Method 1: Manual (Multiple Terminals)

#### Terminal 1 - Node 1:
```bash
python -m src.main \
  --node-id node-1 \
  --host 0.0.0.0 \
  --port 5000 \
  --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

#### Terminal 2 - Node 2:
```bash
python -m src.main \
  --node-id node-2 \
  --host 0.0.0.0 \
  --port 5010 \
  --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

#### Terminal 3 - Node 3:
```bash
python -m src.main \
  --node-id node-3 \
  --host 0.0.0.0 \
  --port 5020 \
  --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

**Wait 5-10 seconds** untuk leader election selesai.

---

### Method 2: Using start_cluster.py (Recommended)

```bash
# Start 3-node cluster automatically
python benchmarks/start_cluster.py
```

Script ini akan:
1. Start 3 nodes di background (port 5000, 5010, 5020)
2. Wait untuk leader election
3. Print status cluster

**Check logs:**
```bash
# Lihat logs semua nodes
tail -f logs/*.log

# Atau check process
ps aux | grep python
```

---

### Method 3: Docker Compose (Production Ready)

#### Build Images:
```bash
cd docker
docker-compose build
```

#### Start Cluster:
```bash
# Start dengan logs
docker-compose up

# Atau start detached
docker-compose up -d
```

#### Check Status:
```bash
# List containers
docker-compose ps

# View logs
docker-compose logs -f node-1
docker-compose logs -f node-2
docker-compose logs -f node-3

# View all logs
docker-compose logs -f
```

**Expected Output:**
```
NAME       STATUS    PORTS
node-1     Up        0.0.0.0:5000->5000/tcp
node-2     Up        0.0.0.0:5010->5000/tcp
node-3     Up        0.0.0.0:5020->5000/tcp
redis      Up        0.0.0.0:6379->6379/tcp
```

#### Stop Cluster:
```bash
docker-compose down

# Stop dan remove volumes
docker-compose down -v
```

---

## Testing Deployment

### 1. Run Automated Tests
```bash
# All tests
pytest -v

# Specific tests
pytest tests/unit/test_raft.py -v
pytest tests/integration/test_cluster.py -v
pytest tests/performance/test_benchmarks.py -v
```

### 2. Run Demo Client
```bash
# Standalone mode
python benchmarks/demo_standalone.py

# Cluster mode (after cluster running)
python benchmarks/demo.py
```

### 3. Check Cluster Health
```bash
# Via HTTP (if implemented)
curl http://localhost:5000/health
curl http://localhost:5010/health
curl http://localhost:5020/health

# Check leader
curl http://localhost:5000/status
```

---

## Configuration

### Environment Variables (.env)

```bash
# Node Configuration
NODE_ID=node-1
NODE_HOST=0.0.0.0
NODE_PORT=5000

# Cluster Configuration
CLUSTER_NODES=node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020

# Raft Configuration
ELECTION_TIMEOUT_MIN=150  # milliseconds
ELECTION_TIMEOUT_MAX=300  # milliseconds
HEARTBEAT_INTERVAL=50     # milliseconds

# Redis Configuration (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/node.log
```

### Docker Compose Configuration

Edit `docker/docker-compose.yml` untuk:
- Change ports
- Add more nodes
- Configure resources (CPU, memory limits)
- Add monitoring (Prometheus, Grafana)

---

## Scaling

### Add New Node

#### Manual:
```bash
# Terminal 4 - Node 4
python -m src.main \
  --node-id node-4 \
  --host 0.0.0.0 \
  --port 5030 \
  --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020,node-4:localhost:5030
```

⚠️ **Note:** Dynamic membership belum fully supported. Node baru harus restart cluster atau implement dynamic reconfiguration.

#### Docker:
Edit `docker-compose.yml`, tambah service:
```yaml
node-4:
  build:
    context: ..
    dockerfile: docker/Dockerfile.node
  environment:
    - NODE_ID=node-4
    - NODE_PORT=5000
    - CLUSTER_NODES=node-1:node-1:5000,node-2:node-2:5000,node-3:node-3:5000,node-4:node-4:5000
  ports:
    - "5030:5000"
```

Kemudian:
```bash
docker-compose up -d --scale node-4=1
```

---

## Monitoring

### Check Logs
```bash
# All logs
tail -f logs/*.log

# Specific node
tail -f logs/node-1.log

# Docker logs
docker-compose logs -f node-1
```

### Metrics (if Prometheus enabled)
```bash
# Open Prometheus
http://localhost:9090

# Open Grafana
http://localhost:3000
```

### Performance Metrics
```bash
# Run benchmarks
python benchmarks/load_test_scenarios.py

# Check results
cat benchmarks/benchmark_results.txt
```

---

## Troubleshooting

### Problem: Port Already in Use
**Error:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Windows
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Problem: Leader Not Elected
**Symptom:** Logs show perpetual elections (term 1, 2, 3, 4...)

**Possible Causes:**
1. Cluster nodes tidak bisa saling connect
2. Firewall blocking ports
3. Wrong cluster configuration

**Solution:**
```bash
# Check network connectivity
ping localhost
telnet localhost 5000
telnet localhost 5010

# Check firewall (Windows)
netsh advfirewall firewall show rule name=all

# Disable firewall temporarily untuk testing
# (Windows - Run as Admin)
netsh advfirewall set allprofiles state off
```

### Problem: Node Startup Timeout
**Error:** Node stuck di "Starting..."

**Solution:**
1. Check Python version: `python --version` (harus 3.8+)
2. Check dependencies: `pip list | grep aiohttp`
3. Check logs: `tail -f logs/node-1.log`
4. Restart dengan clean state:
   ```bash
   # Remove logs
   rm -rf logs/*
   
   # Kill processes
   pkill -f python
   
   # Restart
   python benchmarks/start_cluster.py
   ```

### Problem: Docker Build Fails
**Error:** `ERROR: failed to solve`

**Solution:**
```bash
# Clean docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker-compose config
```

### Problem: Tests Failing
**Error:** `pytest` shows failures

**Solution:**
1. Ensure no other processes running:
   ```bash
   pkill -f python
   ```
2. Clean test artifacts:
   ```bash
   rm -rf .pytest_cache __pycache__
   ```
3. Run specific failing test:
   ```bash
   pytest tests/unit/test_raft.py::test_raft_initialization -vv
   ```

### Problem: High Memory Usage
**Symptom:** Node consuming > 1GB RAM

**Solution:**
1. Check log size: `du -h logs/`
2. Rotate logs:
   ```bash
   mv logs/node-1.log logs/node-1.log.old
   ```
3. Limit log level di `.env`:
   ```
   LOG_LEVEL=WARNING
   ```

---

## Security Considerations

### Production Deployment:
1. **Change default ports** di `.env`
2. **Use firewall** untuk restrict access:
   ```bash
   # Linux (ufw)
   ufw allow from <trusted-ip> to any port 5000
   ```
3. **Use TLS/SSL** untuk inter-node communication
4. **Set strong passwords** untuk Redis
5. **Regular updates** untuk dependencies:
   ```bash
   pip list --outdated
   pip install -U <package>
   ```

---

## Backup & Recovery

### Backup Raft Logs:
```bash
# Manual backup
tar -czf backup-$(date +%Y%m%d).tar.gz logs/

# Automated (crontab)
0 2 * * * tar -czf /backup/raft-$(date +\%Y\%m\%d).tar.gz /path/to/logs/
```

### Restore from Backup:
```bash
# Stop cluster
docker-compose down

# Restore logs
tar -xzf backup-20251026.tar.gz

# Start cluster
docker-compose up -d
```

---

## Performance Tuning

### Optimize Election Timeout:
Edit `.env`:
```bash
# Faster elections (higher CPU)
ELECTION_TIMEOUT_MIN=50
ELECTION_TIMEOUT_MAX=150

# Slower elections (lower CPU)
ELECTION_TIMEOUT_MIN=300
ELECTION_TIMEOUT_MAX=600
```

### Optimize Heartbeat:
```bash
# More frequent (higher network)
HEARTBEAT_INTERVAL=25

# Less frequent (lower network)
HEARTBEAT_INTERVAL=100
```

### Docker Resource Limits:
Edit `docker-compose.yml`:
```yaml
services:
  node-1:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## Support

- **GitHub Issues:** https://github.com/princenizroh/Docker-Raft-Sync/issues
- **Email:** [email dari README]
- **Documentation:** See `docs/` folder

---

**Last Updated:** 26 Oktober 2025
