# Sistem Sinkronisasi Terdistribusi

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

## 📋 Deskripsi

Implementasi sistem sinkronisasi terdistribusi berbasis algoritma Raft yang menyediakan tiga layanan utama:
- Distributed Lock Manager untuk koordinasi akses resource
- Distributed Queue untuk reliable message passing
- Distributed Cache dengan MESI protocol

Project ini merupakan bagian dari Tugas Individu 2 mata kuliah Sistem Parallel dan Terdistribusi.

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

## 🚀 Cara Memulai

### Yang Harus Disiapkan

- Python versi 3.10.11 (WAJIB versi ini)
- WSL2 untuk pengguna Windows
- Docker Desktop dengan WSL2 backend
- Redis (disarankan pakai versi container)
- RAM minimal 8GB
- Storage minimal 20GB
- Koneksi internet stabil

### Langkah Instalasi (IKUTI URUTAN)

1. **Setup WSL2 (Khusus Windows)**
   ```bash
   # Buka PowerShell sebagai Administrator
   wsl --install
   # Restart komputer
   ```

2. **Install Docker Desktop**
   - Download dari https://www.docker.com/products/docker-desktop
   - Install dengan opsi WSL2 backend
   - Restart komputer

3. **Clone Repository**
   ```bash
   # Buka terminal di folder yang diinginkan
   git clone https://github.com/princenizroh/Docker-Raft-Sync.git
   cd Docker-Raft-Sync

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

### Cara Menjalankan Sistem

#### Metode 1: Menggunakan Script (DISARANKAN UNTUK PEMULA)

1. **Siapkan Environment**
   ```bash
   # PASTIKAN Python 3.10.11 terinstall
   python --version
   
   # Buat virtual environment
   python -m venv venv
   
   # Aktifkan virtual environment
   ./venv/Scripts/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Jalankan Demo**
   ```bash
   # PENTING: Matikan dulu proses Python yang masih jalan
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   
   # Jalankan demo
   python benchmarks/demo_standalone.py
   ```

3. **Pilih Demo yang Diinginkan**
   - Ketik 1: Lock Manager Demo (deadlock detection)
   - Ketik 2: Queue System Demo (producer/consumer)
   - Ketik 3: Cache Demo (MESI protocol)

#### Metode 2: Menggunakan Docker (UNTUK ADVANCED USER)

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
python -m src.nodes.base_node --node-id node-1 --host 0.0.0.0 --port 6000 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

**Terminal 2 - Node 2:**
```bash
python -m src.nodes.base_node --node-id node-2 --host 0.0.0.0 --port 6010 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

**Terminal 3 - Node 3:**
```bash
python -m src.nodes.base_node --node-id node-3 --host 0.0.0.0 --port 6020 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

### Langkah Demo Interaktif

1. **Persiapan Awal**
   - Pastikan semua langkah instalasi sudah dilakukan
   - Pastikan virtual environment aktif (ada tanda `(venv)`)
   - Pastikan tidak ada proses Python yang masih jalan

2. **Menjalankan Demo**
   ```bash
   python demo.py
   ```

3. **Menu Demo yang Tersedia:**
   - Lock Manager: Demonstrasi sistem kunci terdistribusi
     * Uji coba exclusive lock
     * Uji coba shared lock
     * Lihat deteksi deadlock bekerja
   
   - Queue System: Demonstrasi sistem antrian
     * Kirim pesan dari producer
     * Terima pesan di consumer
     * Lihat persistent queue bekerja
   
   - Cache System: Demonstrasi MESI protocol
     * Lihat propagasi update cache
     * Lihat invalidasi cache
     * Monitor konsistensi data

4. **Penanganan Masalah**
   - Jika demo tidak respon: Matikan semua proses dan coba lagi
   - Jika error port: Tunggu 30 detik, lalu coba lagi
   - Jika masih error: Restart Docker Desktop

## 📊 Pengujian Sistem

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



## 📈 Hasil Pengujian Performa

### Pengujian Single Node
- Throughput: 1000 pesan/detik
- Latency: 5ms (p95)
- Lock Acquisition: 3ms
- Queue Processing: 800 pesan/detik

### Pengujian 3 Node Cluster
- Throughput: 2500 pesan/detik total
- Latency: 15ms (p95)
- Lock Acquisition: 10ms
- Queue Processing: 2000 pesan/detik

### Pengujian 5 Node Cluster
- Throughput: 4000 pesan/detik total
- Latency: 25ms (p95)
- Lock Acquisition: 18ms
- Queue Processing: 3200 pesan/detik

## 🛠️ Teknologi yang Digunakan

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
