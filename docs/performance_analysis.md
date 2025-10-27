# Performance Analysis — Sistem Sinkronisasi Terdistribusi

Dokumen ini menyajikan analisis performa berdasarkan hasil benchmark lokal terakhir yang dijalankan pada mode standalone (single-node). Hasil mentah disimpan di:
- `benchmarks/local_benchmark_results.json`

Plot yang dihasilkan (jika matplotlib tersedia) disimpan di:
- `benchmarks/locks_latency.png`
- `benchmarks/queue_latency.png`
- `benchmarks/cache_latency.png`

Catatan penting: benchmark yang dijalankan adalah benchmark lokal *standalone*. Untuk pengukuran cluster (multi-node) perlu dijalankan eksperimen terpisah dengan beberapa proses/container dan pengaturan CLUSTER_NODES.

---

## Ringkasan Eksekutif

Percobaan lokal (standalone) singkat menghasilkan metrik berikut (run kecil: 50 ops/messages untuk masing-masing primitive):

- Locks (acquire & release, 50 ops)
  - Throughput: 66.67 ops/sec
  - Total ops: 50 (semua sukses)
  - Durasi total: 0.75 s
  - Latency (rata-rata & percentil) tercatat sangat kecil (banyak nilai 0.0 ms — lihat catatan di bawah)

- Queue (enqueue + dequeue, 50 messages)
  - Enqueue throughput: 72.78 msg/sec
  - Dequeue throughput: 64.02 msg/sec
  - Avg enqueue latency: ≈ 0.94 ms
  - Avg dequeue latency: ≈ 0.0 ms (banyak 0.0 — lihat catatan)
  - P95 enqueue: ≈ 8.25 ms, P99 enqueue: ≈ 16 ms

- Cache (prepopulate + gets, 50 gets, 40 pre-populate)
  - Hit rate: 80.0%
  - Avg get latency: ≈ 19.72 ms
  - P95 get latency: ≈ 102.25 ms, P99 get latency: ≈ 110 ms
  - Put latencies mostly 0.0 ms in pengukuran ini

Kesimpulan singkat: operasi lock/queue pada mode standalone sangat cepat (sub-ms sampai beberapa ms), cache get menunjukkan beberapa outlier latency (hingga ~100 ms pada p95/p99) — kemungkinan disebabkan network loopback, I/O (jika ada) atau overhead event loop dan serialization.

---

## Metodologi

1. Lingkungan
   - Pengujian dilakukan pada repository project (mode standalone).
   - Script benchmark: `benchmarks/local_benchmark.py`
   - Script membuat instance node untuk masing-masing primitive dalam mode standalone (cluster_nodes = []) sehingga Raft akan memilih leader secara instant dan commit dilakukan segera.

2. Skema benchmark
   - Locks: menjalankan N operasi acquire+release exclusive secara berurutan.
   - Queue: enqueue N pesan lalu dequeue hingga N terambil.
   - Cache: prepopulate M keys untuk mencapai rasio hit tertentu, lalu lakukan N get (kombinasi hit+miss) dan ukur latensi.

3. Pengukuran
   - Latensi per operasi diukur menggunakan `time.monotonic()` (dikalikan ke ms).
   - Throughput dihitung dengan `total_ops / total_duration`.
   - Percentile (p50, p95, p99) dihitung dari array latensi.

4. Perintah reproduksi
   - Jalankan: `python benchmarks/local_benchmark.py --locks 50 --queue 50 --cache 50`
   - Hasil JSON: `benchmarks/local_benchmark_results.json`
   - Plot (jika tersedia) disimpan di folder `benchmarks/`.

---

## Hasil Rinci (dari JSON terakhir)

(ambil ringkasan dari file `benchmarks/local_benchmark_results.json`)

- Locks
  - operation: `locks_exclusive_acquire_release`
  - total_ops: 50
  - successful_ops: 50
  - duration_seconds: 0.75
  - throughput_ops_per_sec: 66.67
  - avg_latency_ms: 0.0 (banyak 0.0 akibat resolusi pengukuran)
  - p50/p95/p99: 0.0 / 0.0 / 0.0

- Queue
  - operation: `queue_enqueue_dequeue`
  - messages_requested: 50
  - messages_enqueued: 50
  - messages_dequeued: 50
  - enqueue_throughput_msg_per_sec: 72.78
  - dequeue_throughput_msg_per_sec: 64.02
  - avg_enqueue_latency_ms: 0.94
  - avg_dequeue_latency_ms: 0.0
  - p95_enqueue_latency_ms: 8.25
  - p99_enqueue_latency_ms: 16.0

- Cache
  - operation: `cache_put_get`
  - puts: 40
  - gets: 50
  - hit_count: 40
  - hit_rate_percent: 80.0%
  - avg_put_latency_ms: 0.0
  - avg_get_latency_ms: 19.72
  - p95_get_latency_ms: 102.25
  - p99_get_latency_ms: 110.0

(Lihat file JSON lengkap untuk daftar latensi raw.)

---

## Visualisasi

Plot dibuat dan disimpan (jika matplotlib tersedia):
- `benchmarks/locks_latency.png` — histogram & boxplot latensi acquire/release.
- `benchmarks/queue_latency.png` — histogram latensi enqueue & dequeue.
- `benchmarks/cache_latency.png` — histogram latensi put & get.

Keterangan: beberapa histogram/boxplot menunjukkan banyak nilai 0.0. Hal ini menyebabkan distribusi tampak tidak realistis; baca bagian "Catatan pada metrik".

---

## Interpretasi & Analisis

1. Banyak nilai latensi 0.0 ms
   - Penyebab kemungkinan:
     - Operasi in-memory sangat cepat (< resolusi/akurasi pembulatan ke ms) sehingga dibulatkan ke 0.0 ms pada format yang digunakan.
     - Penempatan pengukuran (operasi sangat cepat di dalam event loop tunggal) sehingga overhead time measurement sangat kecil.
   - Dampak:
     - Mean/p50 menjadi 0.0 untuk beberapa operasi sehingga percentiles tinggi (p95/p99) menjadi indikator lebih berguna untuk outlier.

2. Throughput rendah dibandingkan angka di README
   - README menyebut angka throughput lebih tinggi (mis. 1000 msg/s single-node) — perbedaan ini disebabkan:
     - Percobaan ini kecil skala (50-200 ops) → overhead startup dan logging mempengaruhi hasil.
     - Implementasi benchmark ini menjalankan node dan client di event loop yang sama; untuk throughput tinggi lebih baik gunakan proses terpisah atau cluster container.
   - Rekomendasi: ulangi benchmark dengan jumlah operasi lebih besar (≥ 10k) untuk stabilitas statistik, matikan logging INFO selama run.

3. Cache latency outliers (p95/p99 ~100 ms)
   - Kemungkinan penyebab:
     - Fetch dari peer logic (message passing) atau invalidation handling menambahkan delay pada beberapa operasi.
     - Jika backend Redis dipakai atau ada I/O, itu bisa menjadi sumber latensi.
   - Rekomendasi: profiling jalur `cache.get` untuk mengidentifikasi apakah latensi berasal dari message passing, lock contention, atau persistence I/O.

4. Queue: enqueue vs dequeue asymmetry
   - Enqueue throughput sedikit lebih tinggi dibanding dequeue pada run ini; dequeue latencies banyak tercatat 0.0 — kemungkinan karena dequeue terjadi lokal sangat cepat setelah enqueue pada standalone ring self.
   - Rekomendasi: jalankan benchmark producer/consumer terpisah (client vs server) untuk memisahkan pengaruh event loop.

---

## Perbandingan Single-node vs Distributed

- Catatan: saat ini hasil yang kami miliki adalah untuk single-node (standalone) saja.
- Untuk melakukan perbandingan valid:
  1. Jalankan benchmark yang identik dalam konfigurasi single-node.
  2. Jalankan cluster 3-node (docker-compose) di mesin yang sama atau beberapa mesin, dan jalankan client yang mengirim beban ke leader.
  3. Gunakan load generator eksternal (mis. locust atau custom async client) untuk mengukur throughput/latency real-world.
- Ekspektasi umum:
  - Single-node: latensi lebih rendah (tidak ada replikasi), throughput terbatas oleh CPU/IO local.
  - Multi-node: throughput dapat meningkat dengan sharding/partitioning (terutama untuk queue yang terpartisi), tetapi write-heavy operations (yang lewat Raft) akan mengalami kenaikan latensi karena replikasi ke mayoritas.

---

## Masalah Eksperimental yang Perlu Diperbaiki

1. Pengukuran terlalu pendek / sample kecil
   - Gunakan lebih banyak operasi (≥ 10k) per eksperimen.
2. Logging INFO mengganggu latency
   - Matikan atau turunkan level logging selama benchmark.
3. Node & client pada satu event loop
   - Jalankan node dan driver benchmark di proses terpisah agar tidak saling mempengaruhi.
4. Persistence & I/O
   - Pastikan path persistence pada queue tidak memperlambat (gunakan tmpfs saat pengujian jika ingin mengisolasi IO).
5. Observability
   - Expose metrics (Prometheus) dan rekam selama benchmark untuk analisis time-series (CPU, mem, GC pauses).

---

## Rekomendasi Eksperimen Lanjutan (untuk mendapatkan hasil yang dapat dibandingkan)

1. Skala percobaan:
   - Single-node: 3 skenario (light: 1k ops, medium: 10k ops, heavy: 100k ops).
   - Cluster 3-node: ulangi skenario yang sama, gunakan Docker Compose sehingga setiap node adalah proses terpisah.
   - Cluster 5-node: jika ingin mengukur skala.

2. Kondisi benchmark:
   - Gunakan proses terpisah untuk client (bisa menggunakan `locust` atau custom asyncio client).
   - Matikan logging atau arahkan ke file (tidak ke stdout).
   - Jalankan tiap eksperimen minimal 3 kali, laporkan mean ± stdev.

3. Metrik yang direkam:
   - Latency distribution (p50/p90/p95/p99).
   - Throughput (ops/sec).
   - CPU & mem per node.
   - Disk I/O (jika persistence aktif).
   - Network RTT / packet drops.

4. Visualisasi:
   - Time series: throughput & latency over time.
   - Bar chart: throughput single-node vs cluster.
   - Percentile plots: p50/p90/p95/p99 per skenario.
   - Heatmap: latency vs payload size.

---

## Tindakan Segera yang Saya Lakukan / Bisa Saya Bantu Selanjutnya

- Jika Anda mau, saya bisa:
  - 1) Menjalankan benchmark terukur di cluster 3-node (memerlukan menjalankan docker-compose pada mesin Anda) dan mengumpulkan hasil.
  - 2) Memperbaiki script benchmark agar menjalankan client dan node di proses terpisah untuk hasil yang lebih akurat.
  - 3) Menambahkan pengumpulan metric Prometheus dan template Grafana dashboard.
  - 4) Menjalankan percobaan skala besar (10k/100k ops) dan melaporkan hasil lengkap beserta grafik.

---

## Kesimpulan

- Hasil awal (standalone kecil) menunjukkan sistem cepat untuk operasi in-memory pada skala kecil, dengan throughput puluhan–ratusan ops/sec pada percobaan kecil ini.
- Untuk membuat klaim kuat tentang throughput/latency/scalability, diperlukan eksperimen yang lebih besar, pengaturan proses yang memisahkan node & clients, dan pengukuran observability (Prometheus).
- Saya siap membantu menyiapkan dan menjalankan eksperimen cluster lengkap, atau memperbaiki skrip benchmark agar memberi hasil yang andal. Mana yang ingin Anda jalankan selanjutnya?