# Distributed Synchronization System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen)](https://www.docker.com/)

## 📋 Deskripsi

Sistem sinkronisasi terdistribusi yang mengimplementasikan berbagai algoritma dan protokol untuk menangani koordinasi antar multiple nodes dalam distributed environment. Project ini dikembangkan sebagai bagian dari Tugas Individu 2 - Sistem Parallel dan Terdistribusi.

## ✨ Features

### Core Features (70 poin)

1. **Distributed Lock Manager (25 poin)**
   - Implementasi Raft Consensus Algorithm
   - Support untuk 3+ nodes
   - Shared dan Exclusive Locks
   - Network Partition Handling
   - Distributed Deadlock Detection

2. **Distributed Queue System (20 poin)**
   - Consistent Hashing untuk distribusi
   - Multiple Producers & Consumers
   - Message Persistence & Recovery
   - Node Failure Handling
   - At-least-once Delivery Guarantee

3. **Distributed Cache Coherence (15 poin)**
   - MESI Cache Coherence Protocol
   - Multiple Cache Nodes Support
   - Cache Invalidation & Update Propagation
   - LRU Cache Replacement Policy
   - Performance Metrics Collection

4. **Containerization (10 poin)**
   - Docker support untuk setiap komponen
   - Docker Compose orchestration
   - Dynamic node scaling
   - Environment-based configuration

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│              Distributed Sync System                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │  Node 1  │◄───┤  Node 2  │───►│  Node 3  │         │
│  │          │    │          │    │          │         │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │         │
│  │ │ Raft │ │    │ │ Raft │ │    │ │ Raft │ │         │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │         │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │         │
│  │ │ Lock │ │    │ │ Lock │ │    │ │ Lock │ │         │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │         │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │         │
│  │ │Queue │ │    │ │Queue │ │    │ │Queue │ │         │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │         │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │         │
│  │ │Cache │ │    │ │Cache │ │    │ │Cache │ │         │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │         │
│  └──────────┘    └──────────┘    └──────────┘         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- Redis (optional, untuk state management)
- 4GB RAM minimum
- Windows/Linux/MacOS

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd distributed-sync-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env sesuai kebutuhan
```

### Running with Quick Start Script (Recommended)

```bash
# Run 3-node cluster automatically
python start_cluster.py
```

This will start:
- Node 1 on port 5000
- Node 2 on port 5010
- Node 3 on port 5020

### Running with Docker

```bash
# Navigate to docker directory
cd docker

# Build images
docker-compose build

# Start cluster (3 nodes)
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop cluster
docker-compose down
```

### Running Manually (3 Terminals)

**Terminal 1 - Node 1:**
```bash
python -m src.nodes.base_node --node-id node-1 --host 0.0.0.0 --port 5000 --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

**Terminal 2 - Node 2:**
```bash
python -m src.nodes.base_node --node-id node-2 --host 0.0.0.0 --port 5010 --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

**Terminal 3 - Node 3:**
```bash
python -m src.nodes.base_node --node-id node-3 --host 0.0.0.0 --port 5020 --cluster-nodes node-1:localhost:5000,node-2:localhost:5010,node-3:localhost:5020
```

### Running Interactive Demo

```bash
# Run demo with menu selection
python demo.py
```

Available demos:
1. Distributed Lock Manager - Shows lock acquisition, deadlock detection
2. Distributed Queue System - Shows enqueue/dequeue operations
3. Distributed Cache (MESI) - Shows cache coherence protocol

## 📊 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run performance benchmarks
locust -f benchmarks/benchmark_runner.py
```

## 📖 Documentation

- [Architecture Documentation](docs/architecture.md)
- [API Specification](docs/api_spec.yaml)
- [Deployment Guide](docs/deployment_guide.md)
- [Performance Analysis](docs/performance_analysis.md)

## 🎥 Video Demonstration



## 📈 Performance Metrics

| Metric | Single Node | 3 Nodes | 5 Nodes |
|--------|-------------|---------|---------|
| Throughput | TBD | TBD | TBD |
| Latency (p95) | TBD | TBD | TBD |
| Lock Acquisition | TBD | TBD | TBD |
| Queue Messages/sec | TBD | TBD | TBD |

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Async Framework**: asyncio, aiohttp
- **Messaging**: ZeroMQ
- **State Management**: Redis
- **Testing**: pytest, locust
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus (optional)


## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Mata Kuliah: Sistem Parallel dan Terdistribusi
- Referensi: Raft Consensus Paper, Redis Documentation
- Inspirasi: Distributed Systems: Principles and Paradigms

---

**Note**: Project ini dikembangkan untuk keperluan akademik. Untuk production use, diperlukan additional hardening dan security measures.
