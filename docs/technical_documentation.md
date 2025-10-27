# Dokumentasi Teknis — Sistem Sinkronisasi Terdistribusi

Dokumen ini menyajikan dokumentasi teknis dalam Bahasa Indonesia yang menjelaskan desain, implementasi, antarmuka, alur data, konfigurasi, dan panduan operasional proyek yang terdapat di folder `Tugas-individu/src/`. Tujuan dokumen ini adalah memenuhi kebutuhan pengembang, asisten pengajar, dan penilai untuk memahami perilaku sistem, cara menjalankan, serta tempat memeriksa bagian kode yang relevan.

Catatan: Analisis performa akan disiapkan terpisah di `docs/performance_analysis.md` setelah benchmark dijalankan.

---

## Ringkasan singkat

Sistem menyediakan tiga primitif sinkronisasi utama:
- Distributed Lock Manager (kunci eksklusif dan bersama, deteksi deadlock)
- Distributed Queue (partisi, persistensi, jaminan at-least-once)
- Distributed Cache (protokol MESI, penggantian LRU)

Konsensus dicapai menggunakan algoritma Raft (pemilihan leader, replikasi log, commit). Komunikasi antar-node memakai modul message passing berbasis TCP (asyncio streams). Deteksi kegagalan node menggunakan varian phi-accrual.

Kode sumber utama berada di folder `src/`.

---

## Tujuan dokumen

Dokumen ini menjelaskan hal-hal berikut dengan jelas dan terukur:
1. Struktur proyek dan lokasi berkas penting.
2. Deskripsi teknis tiap komponen dan kontrak antarlapis.
3. API publik (HTTP) serta tipe pesan internal.
4. Alur data end-to-end untuk operasi lock, queue, dan cache.
5. Instruksi konfigurasi dan deployment (singkat).
6. Troubleshooting umum dan lokasi log/health checks.
7. Rekomendasi pengembangan lanjutan.

---

## Struktur proyek & berkas penting

- `src/consensus/raft.py` — Implementasi Raft: `RaftNode`, `LogEntry`, election, append_entries, commit.
- `src/nodes/base_node.py` — `BaseNode` yang menyatukan MessagePassing, FailureDetector, Raft, dan HTTP API opsional.
- `src/nodes/lock_manager.py` — `DistributedLockManager`: logika pengelolaan kunci dan deteksi deadlock.
- `src/nodes/queue_node.py` — `DistributedQueue`: consistent hashing, partisi, persistensi message.
- `src/nodes/cache_node.py` — `DistributedCache`: MESI, LRU cache, invalidasi/update.
- `src/communication/message_passing.py` — `Message` dataclass dan kelas `MessagePassing`.
- `src/communication/failure_detector.py` — Failure detector (phi-accrual).
- `src/api/http_server.py` — Server HTTP opsional (dipakai bila diaktifkan).
- `benchmarks/` — Skrip demo dan benchmark.
- `docker/` — Dockerfile dan docker-compose untuk cluster 3-node + Redis (opsional).
- `tests/` — Unit, integration, dan performance tests (pytest).

---

## Deskripsi komponen & kontrak

### 1) Raft (`src/consensus/raft.py`)
- Tipe utama:
  - `RaftState`: FOLLOWER, CANDIDATE, LEADER.
  - `LogEntry`: term, index, command, data, timestamp.
  - `RaftNode`: implementasi inti Raft.
- Tanggung jawab:
  - Timer election dan inisiasi pemilihan.
  - RPC handlers: `handle_request_vote`, `handle_append_entries`.
  - Leader actions: kirim heartbeat / append_entries.
  - Commit & apply entries: `_update_commit_index`, `_apply_committed_entries`.
- Titik integrasi:
  - `message_sender` (callback) untuk mengirim payload RPC ke peer.
  - `state_change_callback` & `commit_callback` untuk notifikasi state/commit.
- Catatan penting:
  - Pada mode standalone (`cluster_nodes = []`), `append_log` meng-commit segera (nyaman untuk demo, bukan perilaku cluster multi-node).

### 2) Message Passing (`src/communication/message_passing.py`)
- `Message` memiliki field: `msg_type`, `sender_id`, `receiver_id`, `term`, `payload`, `timestamp`, `message_id`.
- `MessagePassing`:
  - Server TCP menggunakan `asyncio.start_server`.
  - Koneksi disimpan keyed by `sender_id`; alamat node diharapkan dalam format `node-id:host:port`.
  - Register handler per `msg_type` (mis. `request_vote`, `append_entries`, `heartbeat`, `cache_invalidate`).
  - API publik: `start()`, `stop()`, `send_message(target_node, message)`, `broadcast_message`, `register_handler`.
- Detail implementasi:
  - Saat koneksi masuk, pesan pertama berisi `sender_id` dipakai untuk mengikat writer ke sender sehingga subsequent messages dikenali.

### 3) Failure Detector (`src/communication/failure_detector.py`)
- Menggunakan sliding-window statistik interval heartbeat untuk menghitung nilai phi.
- Node state: ALIVE, SUSPECTED, FAILED.
- Callback tersedia untuk failure & recovery.
- Parameter yang bisa dikonfigurasi: `heartbeat_interval`, `phi_threshold`, `window_size`, `min_samples`, dsb.

### 4) BaseNode (`src/nodes/base_node.py`)
- Menyatukan MessagePassing, FailureDetector, dan Raft.
- Mendaftarkan handlers yang memanggil Raft RPC handlers saat menerima pesan.
- Menyediakan `submit_command(command, data)` — hanya berfungsi bila node adalah leader (lainnya akan mengembalikan False).
- Callback commit akan memicu `process_committed_entry` pada subclass (lock/queue/cache).
- HTTP API opsional diinisialisasi bila `enable_http_api` true; port default di-deduce dari `node-id` (konvensi `node-1`, `node-2`, ...).

### 5) Distributed Lock Manager (`src/nodes/lock_manager.py`)
- Struktur state: `locks` (resource_id -> Lock), `held_locks` (client -> set resources), `wait_for_graph`.
- Alur:
  - `acquire_lock(...)` membuat `LockRequest`, submit `acquire_lock` ke Raft, lalu menunggu grant via perubahan state yang diterapkan pada commit.
  - `release_lock(...)` submit `release_lock` ke Raft.
- Deteksi deadlock:
  - Wait-for graph di-scan periodik menggunakan DFS untuk menemukan siklus; resolusi memilih abort salah satu partisipan (heuristik youngest).

### 6) Distributed Queue (`src/nodes/queue_node.py`)
- Partitioning: `partition = hash(queue_name) % partition_count`.
- Konsistent hashing mengalokasikan partition ke node (class `ConsistentHash`).
- Durability: periodic persistence ke disk (pickle) di `persistence_path` per node.
- Lifecyle message:
  - `enqueue`: submit `'enqueue'` command ke Raft; on commit append ke partition queue.
  - `dequeue`: dilakukan oleh owner partition; `mark_delivered` & `acknowledge` mengikuti untuk at-least-once semantics.

### 7) Distributed Cache (`src/nodes/cache_node.py`)
- MESI states: `MODIFIED`, `EXCLUSIVE`, `SHARED`, `INVALID`.
- `LRUCache` memakai `OrderedDict` untuk eviction.
- `get`: jika miss, coba fetch dari peer via message passing; jika ditemukan, simpan sebagai `SHARED`.
- `put`: broadcast invalidation ke peer, set local line `MODIFIED`, submit `cache_put` ke Raft untuk durability.
- `process_committed_entry` menerapkan `cache_put` dan `cache_delete` setelah commit.

---

## API REST (opsional) — ringkasan

Spesifikasi OpenAPI: `docs/api_spec.yaml`.

Endpoint umum (apabila HTTP API diaktifkan):
- `POST /locks/{lock_id}` — mengambil lock. Body: { lock_type: "exclusive"|"shared", timeout: ms }.
- `DELETE /locks/{lock_id}` — melepas lock.
- `POST /queue/{queue_id}/enqueue` — enqueue pesan.
- `POST /queue/{queue_id}/dequeue` — dequeue pesan.
- `GET /cache/{key}`, `PUT /cache/{key}` — operasi cache.
- `GET /health` — status node (is_leader, term).

Pattern client:
- Client yang tidak langsung terhubung ke leader harus menemukan leader dahulu (mis. coba `/status` pada semua node) atau menggunakan client library yang otomatis memilih leader. Implementasi forwarding pada follower belum tersedia secara default.

---

## Alur data end-to-end — contoh use-case

### 1) Acquire Lock (exclusive)
1. Client mengirim request ke node A (HTTP API atau client library).
2. Jika node A adalah leader: `submit_command('acquire_lock', request)` → Raft append_log → replikasi ke followers.
3. Setelah mayoritas commit, `commit_callback` memicu `DistributedLockManager._process_acquire_lock` → state lock diperbarui (grant atau antrian).
4. Client yang menunggu akan melihat grant melalui API atau polling state.

Jika node A bukan leader: client harus menemukan leader dan mengirim request ke leader.

### 2) Enqueue Message
1. Client mengirim enqueue ke node X.
2. Node X mengirim `enqueue` command ke leader Raft (atau jika X leader langsung append).
3. Setelah commit, `_process_enqueue` menambahkan `QueueMessage` ke partition queue lokal dan persist ke disk periodik.
4. Consumer melakukan `dequeue` pada owner partition; delivery dan ack mengikuti.

### 3) Cache Put
1. Client mengirim `PUT /cache/{key}` ke leader.
2. Leader broadcast `CACHE_INVALIDATE` ke semua peer via MessagePassing.
3. Leader memasukkan entry lokal state `MODIFIED` dan submit `cache_put` ke Raft.
4. Setelah commit, followers menerapkan update melalui `process_committed_entry`.

---

## Konfigurasi & environment variables penting

- `CLUSTER_NODES` — comma-separated daftar node dalam format `node-id:host:port`. (Sangat penting untuk konsistensi alamat.)
- Raft & failure detector tuning (lihat `docker/docker-compose.yml`):
  - `RAFT_HEARTBEAT_INTERVAL` (ms)
  - `RAFT_ELECTION_TIMEOUT_MIN`, `RAFT_ELECTION_TIMEOUT_MAX` (ms)
  - `FAILURE_DETECTOR_PHI_THRESHOLD`, `FAILURE_DETECTOR_WINDOW_SIZE`, dsb.
- `ENABLE_HTTP_API` — jika true, `BaseNode` akan mencoba menyiapkan HTTP API server.
- Catatan: `BaseNode` menurunkan port HTTP berdasarkan pola `node-<n>`; jika memakai ID berbeda, periksa log HTTP initialization.

---

## Cara menjalankan (ringkasan praktis)

### Standalone (demo cepat)
```/dev/null/example_standalone.sh#L1-12
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
python benchmarks/demo_standalone.py
```
Pilih demo: 1 = Lock, 2 = Queue, 3 = Cache. Standalone menggunakan `cluster_nodes = []` sehingga node menjadi leader segera.

### Docker (3-node cluster)
```/dev/null/example_docker.sh#L1-12
cd docker
docker-compose build
docker-compose up -d
# cek logs: docker-compose logs -f
# cek health: docker-compose ps
```

### Manual 3-proses (tanpa Docker)
- Terminal 1:
```/dev/null/example_node1.sh#L1-2
python -m src.nodes.base_node --node-id node-1 --host 0.0.0.0 --port 6000 --cluster-nodes node-1:localhost:6000,node-2:localhost:6010,node-3:localhost:6020
```
- Terminal 2/3: ganti node-id dan port sesuai.

---

## Monitoring & logging

- Logging: menggunakan `logging` Python; output ke stdout (terlihat di `docker-compose logs` bila dijalankan lewat Docker).
- Metrics: terdapat utilitas metrics di `src/utils/metrics.py` (counter/gauge). Untuk produksi, ekspos endpoint Prometheus di HTTP API dan konfigurasi Prometheus/Grafana.
- Health checks: `docker-compose.yml` memanfaatkan `/status` atau endpoint HTTP API untuk healthcheck.

---

## Troubleshooting & permasalahan umum

- "Not leader, cannot submit command":
  - Penyebab: memanggil `submit_command` pada follower. Solusi: temukan leader (cek `/status`) dan kirim request ke leader, atau gunakan demo standalone.
- Konflik port / proses Python lama:
  - Hentikan proses Python yang berjalan pada port terkait (lihat QUICK_START.md).
- Cluster gagal elect leader:
  - Periksa format `CLUSTER_NODES`, konektivitas TCP antar node, dan parameter election timeout.
- File persistensi queue tidak ditemukan / tulis gagal:
  - Pastikan path `persistence_path` dapat ditulis oleh proses, periksa permission dan working directory.

---

## Testing & quality assurance

- Unit tests:
  - `pytest tests/unit -v`
- Integration tests:
  - `pytest tests/integration -v`
- Performance tests:
  - `pytest tests/performance -v`
  - atau gunakan `benchmarks/benchmark_runner.py` dan `locust` untuk skenario beban kustom.
- Perhatian: pastikan tidak ada layanan lain menempati port yang digunakan oleh tes cluster/integrasi.

---

## Rekomendasi pengembangan & peningkatan

- Implementasikan request forwarding pada follower sehingga client dapat mengirim request ke follower dan otomatis diteruskan ke leader.
- Tambahkan support dynamic membership (Raft config change) untuk menambah/mengurangi node secara aman.
- Optimisasi throughput: batch append_entries, serialisasi cepat (mis. msgpack), persistence asinkron/batched.
- Ekspos metric Prometheus dan sediakan template dashboard Grafana (p95/p99, commit latency, queue depth).
- Tambahkan TLS/auth untuk MessagePassing dan HTTP API demi keamanan produksi.

---

## Batasan yang diketahui

- Dynamic membership belum didukung; membership bersifat statis pada startup.
- `submit_command` pada follower mengembalikan False — tidak ada forwarding otomatis.
- Mode standalone melakukan commit instan; ini adalah shortcut demo, bukan perilaku cluster multi-node.
- Keamanan (TLS, otentikasi) tidak diimplementasikan.

---

## Anchor kode: tempat untuk memeriksa implementasi

- Logika election & append: `src/consensus/raft.py` (`_start_election`, `_send_append_entries`).
- Transport & handler: `src/communication/message_passing.py`.
- Alur lock: `src/nodes/lock_manager.py` (`acquire_lock`, `_process_acquire_lock`).
- Persistensi queue & consistent hash: `src/nodes/queue_node.py`.
- MESI handlers: `src/nodes/cache_node.py` (`_handle_cache_get`, `_handle_cache_put`, `_handle_cache_invalidate`).

---
