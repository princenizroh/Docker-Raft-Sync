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


Repository ini adalah implementasi eksperimen sistem terdistribusi berbasis Raft yang menyediakan tiga primitive utama:
- Distributed Lock Manager
- Distributed Queue
- Distributed Cache (coherence)

Dokumentasi ini memberikan panduan singkat yang terstruktur untuk fitur, skrip, demo, pengujian, dan langkah-langkah praktis agar Anda bisa menjalankan, menguji, dan merekam demonstrasi sistem ini.

---

## Isi singkat README (quick links)
- Deskripsi singkat & tujuan
- Prasyarat
- Daftar fitur
- Skrip & demo penting (apa yang untuk dijalankan)
- Cara menjalankan (Docker / Local / In-process)
- Cara menjalankan benchmark & menyimpan output
- Menjalankan test suite
- Troubleshooting umum
- Lokasi output (JSON / PNG)
- Tips rekaman video & link panduan

---

## 1. Tujuan proyek
Tujuan: menyediakan rangkaian eksperimen dan tooling untuk mempelajari perilaku Raft pada kasus nyata — sinkronisasi akses (locks), antrian terdistribusi (queue), dan caching koheren (cache). Kode di repository ini bersifat educational / demo — bukan ready-for-production.

---

## 2. Prasyarat
- Python 3.8+ (direkomendasikan 3.10+)
- pip
- virtualenv / venv
- Docker & Docker Compose (jika ingin menjalankan container)
- (Opsional) WSL2 pada Windows untuk kemudahan Docker + bash utilities
- Redis (container disediakan di docker-compose)

---

## 3. Fitur utama
- Implementasi Raft (minimal/demo) untuk leader election dan replikasi log
- HTTP API pada tiap node untuk primitive:
  - Locks: acquire / release (shared/exclusive)
  - Queue: enqueue / dequeue
  - Cache: put / get (sederhana)
- Beberapa tooling benchmark:
  - `distributed_http_benchmark.py` — HTTP benchmark client (locks, queue, cache)
  - `inprocess_cluster_runner.py` — jalankan cluster in-process + benchmark
  - `auto_distributed_test_runner.py` — runner otomatis (local atau docker) untuk seluruh role
- Demo helpers:
  - `benchmarks/demo_cluster_client.py` — client helper yang dipakai benchmark
  - `benchmarks/demo_standalone.py` — contoh demo singkat
- Utilities untuk plotting hasil benchmark (PNG) dan menyimpan JSON

---

## 4. Struktur file penting (ringkas)
- `docker/docker-compose.yml` — konfigurasi Docker Compose untuk menjalankan cluster 3-node + redis
- `src/consensus/raft.py` — implementasi Raft (demo)
- `src/api/http_server.py` — HTTP API handlers (status, lock, queue, cache)
- `scripts/start_cluster_api.py` — script untuk memulai node (dipakai oleh runner)
- `benchmarks/scenarios/` — folder berisi runner dan benchmark clients:
  - `distributed_http_benchmark.py`
  - `inprocess_cluster_runner.py`
  - `auto_distributed_test_runner.py`
  - `client_benchmark.py`, `extra_plots.py`, dsb.
- `benchmarks/VIDEO_DEMO_INSTRUCTIONS.md` — panduan video demo dan runbook
- `benchmarks/VIDEO_SCRIPT_VERBATIM.md` — naskah verbatim untuk rekaman video

---

## 5. Cara men-setup environment (singkat)
1. Clone:
```/dev/null/README.md#L1-3
git clone <repo-url>
cd <repo-root>
```

2. Virtual environment & dependencies:
```/dev/null/README.md#L4-9
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
pip install -r requirements.txt
```

3. Salin .env contoh (opsional, jika ada):
```/dev/null/README.md#L10-12
cp .env.example .env
# lalu edit .env sesuai kebutuhan (API ports, CLUSTER_NODES, REDIS_HOST)
```

---

## 6. Cara menjalankan (pilih satu workflow)

Catatan: semua perintah diasumsikan dijalankan dari root repository.

A. Docker (3-node container)
1. Build & start:
```
cd docker
docker compose build --no-cache
docker compose up -d --force-recreate
```

2. issue
Jika mengalami issue dan tidak mendapatkan leader
```
docker compose restart
```

3. Verifikasi:
```
docker compose ps
docker compose logs --tail=200 dist-node-1 dist-node-2 dist-node-3
# cek HTTP status (default ports: 6000,6010,6020)
curl http://127.0.0.1:6000/status
curl http://127.0.0.1:6010/status
curl http://127.0.0.1:6020/status
```

4. Stop:
```
cd docker
docker compose down
```

Catatan: Pastikan `CLUSTER_NODES` di `docker/docker-compose.yml` berisi host yang dapat di-resolve oleh container (gunakan container hostnames seperti `dist-node-1` di string CLUSTER_NODES bila perlu).

---

B. Local (subprocess per node) — debugging
Jalankan tiga proses node pada terminal berbeda (contoh untuk lock nodes):
```
python -m src.nodes.base_node --node-id node-1 --host 0.0.0.0 --port 6000 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
python -m src.nodes.base_node --node-id node-2 --host 0.0.0.0 --port 6010 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
python -m src.nodes.base_node --node-id node-3 --host 0.0.0.0 --port 6020 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```

Kemudian cek status:
```
curl http://localhost:6000/status
curl http://localhost:6010/status
```

---

C. In-process (recommended untuk demo cepat)
Runner otomatis memulai cluster (di satu proses Python), menunggu stabil, menjalankan benchmark singkat, lalu stop:
```
python benchmarks/scenarios/inprocess_cluster_runner.py lock --locks 500 --concurrency 30
# Ganti 'lock' menjadi 'queue' atau 'cache' untuk masing-masing primitive.
```

---

## 7. Menjalankan benchmark HTTP (client)
- Distributed HTTP benchmark client:
```
python benchmarks/scenarios/distributed_http_benchmark.py \
  --nodes 127.0.0.1:6000 127.0.0.1:6010 127.0.0.1:6020 \
  --locks 500 --queue 500 --cache 500 --concurrency 30
```
- Auto runner (local atau docker mode) untuk menjalankan semua role berurutan:
```
python benchmarks/scenarios/auto_distributed_test_runner.py --mode local --locks 500 --queue 500 --cache 500 --concurrency 30
# atau
python benchmarks/scenarios/auto_distributed_test_runner.py --mode docker --reuse-cluster --locks 500 --queue 500 --cache 500
```

Output default:
- JSON hasil: `benchmarks/scenarios/distributed_http_benchmark_results.json`
- Auto runner hasil per-role: `benchmarks/scenarios/results/distributed_benchmark_<role>_<ts>.json`
- In-process results: `benchmarks/scenarios/inprocess_results_<role>_<ts>.json`
- Plot PNG: `benchmarks/scenarios/plots/*.png`

---

## 8. Menjalankan test suite
- Unit & integration:
```/dev/null/README.md#L48-51
pytest
# atau spesifik:
pytest tests/unit/
pytest tests/integration/
```
- Coverage (jika terpasang):
```
pytest --cov=src --cov-report=html
```

---

## 9. Skrip & file demo yang sering dipakai (ringkasan)
- `scripts/start_cluster_api.py` — helper untuk start cluster per-role (dipakai oleh auto runner)
- `benchmarks/demo_cluster_client.py` — client helper (ClusterClient)
- `benchmarks/demo_standalone.py` — demo singkat
- `benchmarks/scenarios/`:
  - `distributed_http_benchmark.py` — client HTTP untuk benchmark
  - `inprocess_cluster_runner.py` — start in-process cluster + benchmark
  - `auto_distributed_test_runner.py` — orchestration local/docker untuk semua role
  - `client_benchmark.py` / `load_test_scenarios.py` — skenario client-only (opsional)
  - `extra_plots.py` — plotting tambahan
- `benchmarks/VIDEO_DEMO_INSTRUCTIONS.md` — runbook perekaman video
- `benchmarks/VIDEO_SCRIPT_VERBATIM.md` — naskah verbatim rekaman

---

## 🛠️ Teknologi yang Digunakan

- **Language**: Python 3.10+
- **Async Framework**: asyncio, aiohttp
- **Messaging**: ZeroMQ
- **State Management**: Redis
- **Testing**: pytest
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus (optional)

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Mata Kuliah: Sistem Parallel dan Terdistribusi
- Referensi: Raft Consensus Paper, Redis Documentation
- Inspirasi: Distributed Systems: Principles and Paradigms

---
