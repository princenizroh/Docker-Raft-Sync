# Deployment Guide - Distributed Synchronization System

## Prerequisites
- Python 3.10+
- Redis Server
- Docker (optional)
- 3+ machines/VMs for production cluster

## Local Development Setup

### 1. Clone and Install Dependencies
```bash
git clone <repository-url>
cd distributed-sync-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Redis
```bash
redis-server
```

### 4. Run Single Node
```bash
python -m pytest tests/unit/ -v  # Verify tests pass
python benchmarks/demo.py        # Test Raft consensus
```

## Production Deployment

### Option 1: Docker Compose (RECOMMENDED)

#### Step 1: Build dan Start Cluster
```powershell
# Navigate ke project root
cd distributed-sync-system

# Build images (first time only)
docker-compose -f docker/docker-compose.yml build

# Start cluster (3 nodes + Redis)
docker-compose -f docker/docker-compose.yml up -d

# Verify containers running
docker-compose -f docker/docker-compose.yml ps
```

**Expected Output:**
```
NAME           IMAGE                      STATUS
dist-node-1    distributed-sync:latest    Up 10 seconds
dist-node-2    distributed-sync:latest    Up 10 seconds  
dist-node-3    distributed-sync:latest    Up 10 seconds
redis          redis:7-alpine             Up 15 seconds
prometheus     prom/prometheus:latest     Up 10 seconds
```

#### Step 2: Check Cluster Health
```powershell
# Check node-1 logs
docker logs dist-node-1 --tail 50

# Check node-2 logs  
docker logs dist-node-2 --tail 50

# Check node-3 logs
docker logs dist-node-3 --tail 50

# Should see: "Raft node started", "Election timeout", "Node became CANDIDATE/LEADER"
```

#### Step 3: Verify Cluster Working
```powershell
# Check Redis connection
docker exec -it docker-redis-1 redis-cli ping
# Should return: PONG

# Check node-1 logs untuk lihat Raft consensus
docker logs dist-node-1 --tail 30

# Check node-2 logs
docker logs dist-node-2 --tail 30

# Check node-3 logs  
docker logs dist-node-3 --tail 30

# Should see: "Node became CANDIDATE", "Node became LEADER", "Election timeout"
```

#### Step 4: View Real-Time Logs
```powershell
# View real-time logs from all nodes
docker-compose -f docker/docker-compose.yml logs -f

# Press Ctrl+C to stop viewing logs
```

#### Step 5: Stop Cluster
```powershell
# Stop containers (preserve data)
docker-compose -f docker/docker-compose.yml stop

# Stop and remove containers (delete data)
docker-compose -f docker/docker-compose.yml down

# Stop and remove everything including volumes
docker-compose -f docker/docker-compose.yml down -v
```

#### Troubleshooting Docker

**Problem: "Cannot connect to Docker daemon"**
```powershell
# Start Docker Desktop
# Wait until Docker icon shows "Running"
```

**Problem: Port already in use (5000, 5010, 5020)**
```powershell
# Find process using port
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

**Problem: Container exits immediately**
```powershell
# Check logs for errors
docker logs dist-node-1

# Common issue: Missing dependencies
docker-compose -f docker/docker-compose.yml build --no-cache
```

---

### Option 2: Manual Multi-Node Setup (Advanced)

#### Node 1 (Leader candidate)
```bash
export NODE_ID=node-1
export NODE_HOST=0.0.0.0
export NODE_PORT=5000
export CLUSTER_NODES=node-1:192.168.1.10:5000,node-2:192.168.1.11:5000,node-3:192.168.1.12:5000
python -m src.main
```

#### Node 2
```bash
export NODE_ID=node-2
export NODE_HOST=0.0.0.0
export NODE_PORT=5000
export CLUSTER_NODES=node-1:192.168.1.10:5000,node-2:192.168.1.11:5000,node-3:192.168.1.12:5000
python -m src.main
```

#### Node 3
```bash
export NODE_ID=node-3
export NODE_HOST=0.0.0.0
export NODE_PORT=5000
export CLUSTER_NODES=node-1:192.168.1.10:5000,node-2:192.168.1.11:5000,node-3:192.168.1.12:5000
python -m src.main
```

## Configuration Reference

### Environment Variables
- `NODE_ID`: Unique identifier for this node (required)
- `NODE_HOST`: Bind address (default: 0.0.0.0)
- `NODE_PORT`: HTTP port (default: 5000)
- `CLUSTER_NODES`: Comma-separated list of all cluster nodes
- `REDIS_HOST`: Redis server address (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `RAFT_ELECTION_TIMEOUT_MIN`: Min election timeout ms (default: 150)
- `RAFT_ELECTION_TIMEOUT_MAX`: Max election timeout ms (default: 300)
- `RAFT_HEARTBEAT_INTERVAL`: Heartbeat interval ms (default: 50)

## Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "role": "leader",
  "term": 42
}
```

### Metrics Collection
Metrics are exposed at `/metrics` endpoint (Prometheus format)

## Troubleshooting

### Split Brain / No Leader
- Check network connectivity between nodes
- Verify CLUSTER_NODES configuration matches on all nodes
- Ensure at least 3 nodes are running
- Check logs for election timeouts

### High Latency
- Check Redis connection latency
- Verify network latency between nodes < 10ms
- Monitor CPU usage on nodes

### Lock Deadlocks
- Review application lock acquisition patterns
- Check deadlock detection logs
- Consider increasing lock timeout values

## Performance Tuning

### Raft Timings
For low-latency networks:
```
RAFT_ELECTION_TIMEOUT_MIN=150
RAFT_ELECTION_TIMEOUT_MAX=300
RAFT_HEARTBEAT_INTERVAL=50
```

For high-latency networks:
```
RAFT_ELECTION_TIMEOUT_MIN=300
RAFT_ELECTION_TIMEOUT_MAX=600
RAFT_HEARTBEAT_INTERVAL=100
```

### Redis Tuning
```redis
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
```

## Security Recommendations

1. **Network Isolation**: Use VPN or private network for inter-node communication
2. **Redis Authentication**: Set `requirepass` in redis.conf
3. **TLS/SSL**: Enable TLS for production deployments
4. **Firewall Rules**: Restrict ports to cluster IPs only

## Backup and Recovery

### Log Persistence
Raft logs are automatically persisted in `data/` directory

### Backup Strategy
```bash
# Regular backups
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Recovery
```bash
# Restore from backup
tar -xzf backup-20250125.tar.gz
```

## Scaling

### Adding Nodes
1. Update CLUSTER_NODES on all existing nodes
2. Start new node with updated configuration
3. New node will sync automatically

### Removing Nodes
1. Gracefully shutdown node
2. Update CLUSTER_NODES on remaining nodes
3. Ensure quorum is maintained (N/2 + 1 nodes)

## Production Checklist

- [ ] 3+ nodes deployed
- [ ] Redis configured with persistence
- [ ] Environment variables set correctly
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Firewall rules in place
- [ ] Load testing completed
- [ ] Disaster recovery plan documented
