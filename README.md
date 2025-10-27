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
   - Environment-based configuration

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│              Distributed Sync System                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │  Node 1  │◄───┤  Node 2  │───►│  Node 3  │            │
│  │          │    │          │    │          │            │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │            │
│  │ │ Raft │ │    │ │ Raft │ │    │ │ Raft │ │            │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │            │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │            │
│  │ │ Lock │ │    │ │ Lock │ │    │ │ Lock │ │            │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │            │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │            │
│  │ │Queue │ │    │ │Queue │ │    │ │Queue │ │            │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │            │
│  │ ┌──────┐ │    │ ┌──────┐ │    │ ┌──────┐ │            │
│  │ │Cache │ │    │ │Cache │ │    │ │Cache │ │            │
│  │ └──────┘ │    │ └──────┘ │    │ └──────┘ │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Cara Memulai

### Yang Harus Disiapkan

- Python versi 3.10.11 (direkomendasikan)
- WSL2 untuk pengguna Windows (jika menggunakan Docker Desktop)
- Docker Desktop dengan WSL2 backend (Windows)
- Redis (disarankan pakai versi container)
- RAM minimal 8GB
- Storage minimal 20GB
- Koneksi internet stabil

### Langkah Instalasi (Ringkas)

1. Clone repository:
```bash
git clone https://github.com/princenizroh/Docker-Raft-Sync.git
cd Docker-Raft-Sync
```

2. Buat virtual environment dan install dependencies:
```bash
# Buat venv
python -m venv venv

# Aktifkan venv
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# Install deps
pip install -r requirements.txt
```

3. Setup environment (salin file contoh):
```bash
cp .env.example .env
# Edit .env sesuai kebutuhan (PORT, CLUSTER_NODES, REDIS_HOST, dsb.)
```

### Cara Menjalankan Sistem

#### Metode 1: Menjalankan secara lokal (3 terminal) — direkomendasikan untuk debugging
Jalankan tiga proses Node di terminal berbeda. Penting: gunakan `--host 0.0.0.0` supaya server bind ke semua interface ketika diperlukan.

Terminal 1 - Node 1:
```bash
python -m src.nodes.base_node --node-id node-1 --host 0.0.0.0 --port 6000 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

Terminal 2 - Node 2:
```bash
python -m src.nodes.base_node --node-id node-2 --host 0.0.0.0 --port 6010 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

Terminal 3 - Node 3:
```bash
python -m src.nodes.base_node --node-id node-3 --host 0.0.0.0 --port 6020 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

Setelah semua node berjalan, Anda dapat memanggil:
```bash
curl http://localhost:6000/status
curl http://localhost:6010/status
curl http://localhost:6020/status
```

#### Metode 2: Menggunakan Docker Compose (untuk cluster yang tercontainerisasi)
Gunakan file `docker/docker-compose.yml`.

Build dan start:
```bash
# dari root project
cd docker

# Build images
docker compose build

# Start cluster (3 nodes)
docker compose up -d --build

# Atau jika ingin scale service yang dinamai `node`:
docker compose up -d --build --scale node=3
```

Melihat status dan logs:
```bash
docker compose ps
docker compose logs -f
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
```

Stop cluster:
```bash
docker compose down
```

> Catatan: pastikan environment variables di `docker/docker-compose.yml` mengisi `CLUSTER_NODES` dengan host yang dapat di-resolve oleh container lain (contoh: `node-1:dist-node-1:6000,node-2:dist-node-2:6010,node-3:dist-node-3:6020`) dan bahwa aplikasi bind ke `0.0.0.0` di dalam container.

### Menjalankan Demo / Benchmark Singkat

Demo standalone:
```bash
python benchmarks/demo_standalone.py
```

Benchmark dengan Locust:
```bash
# Pastikan locust terinstall
locust -f benchmarks/benchmark_runner.py
# Buka UI Locust: http://localhost:8089
```

Untuk test load internal atau pengukuran lebih canggih, gunakan konfigurasi Locust scenario di `benchmarks/`.

## 📊 Pengujian Sistem

```bash
# Run unit/integration tests
pytest

# Coverage report (opsional)
pytest --cov=src --cov-report=html

# Run specific suites
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

## 📖 Dokumentasi

- `docs/architecture.md`
- `docs/api_spec.yaml`
- `docs/deployment_guide.md`
- `docs/performance_analysis.md`

## ⚠️ Catatan Penting (Debugging & Gotchas)

- CLUSTER_NODES harus konsisten: format yang digunakan dalam project adalah `node-id:host:port`. Jangan mencampur format atau menambahkan token lain yang menyebabkan kesalahan resolusi (contoh bermasalah: `node-3:dist-node-3:5000` ditempatkan di field yang salah).
- Jika mendapatkan `socket.gaierror: [Errno -2] Name or service not known` → periksa nilai `CLUSTER_NODES` dan pastikan hostnya dapat di-resolve dari container/node.
- Jika `curl http://localhost:6000/status` dari host menunjukkan "Empty reply from server" namun container logs menunjukkan `200`:
  - Bisa terjadi restart/flapping pada container (healthcheck bermasalah).
  - Cek `docker ps` apakah container sedang restart.
  - Pastikan server bind ke `0.0.0.0` agar port yang dipublish dapat diakses dari host.
- Untuk membedakan masalah network vs aplikasi, selalu bandingkan:
  - `curl` dari host ke published port, dan
  - `curl` dari dalam container (`docker exec -it <container> curl -v http://127.0.0.1:<port>/status`)
- Healthchecks di `docker-compose` yang terlalu agresif dapat menyebabkan restart loop. Tambahkan `interval`, `timeout`, `retries` yang moderat.

Langkah debugging cepat:
```bash
# Periksa container/status
docker compose -f docker/docker-compose.yml ps
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"

# Ambil logs node tertentu
docker compose -f docker/docker-compose.yml logs --no-color --tail=200 node1
# atau
docker logs --tail 200 dist-node-1

# Tes endpoint dari host
curl -v http://localhost:6000/status

# Tes dari dalam container
docker compose -f docker/docker-compose.yml exec node1 curl -v http://127.0.0.1:6000/status

# Periksa listener & proses di dalam container
docker compose -f docker/docker-compose.yml exec node1 ss -ltnp
docker compose -f docker/docker-compose.yml exec node1 ps aux | egrep 'python|aiohttp|uvloop'
```

## 📈 Hasil Pengujian Performa (contoh)

> Nilai-nilai di bawah hanya contoh yang dihasilkan dalam environment pengembangan; angka nyata tergantung hardware, konfigurasi network, dan pengaturan benchmark.

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

## 🛠️ Teknologi yang Digunakan

- **Language**: Python 3.10+
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

Note: Project ini dikembangkan untuk keperluan akademik. Untuk production use, diperlukan additional hardening and security measures.