# Arsitektur Sistem Sinkronisasi Terdistribusi

## Gambaran Umum Sistem

Bayangkan Anda punya beberapa komputer yang harus bekerja sama untuk menyelesaikan tugas. Sistem ini memastikan semua komputer tersebut tetap terkoordinasi dengan baik, walaupun ada yang mati atau jaringan terputus. Caranya adalah dengan menggunakan algoritma Raft untuk memilih pemimpin dan menjaga agar semua data tetap konsisten di semua komputer.

## Komponen Utama Sistem

### 1. Lapisan Konsensus dengan Algoritma Raft

Lapisan ini adalah otak dari sistem kita. Raft bekerja seperti pemilihan ketua kelas di sekolah. Pertama, semua node akan memilih siapa yang jadi pemimpin atau leader. Leader inilah yang akan mengatur semua operasi penting. Pemilihan ini menggunakan sistem periode atau term, jadi kalau leader-nya mati, akan ada pemilihan ulang secara otomatis.

Setelah leader terpilih, dia akan mencatat semua perintah yang masuk ke dalam sebuah log. Log ini kemudian disalin ke semua node lain agar semua punya data yang sama. Proses penyalinan ini disebut replikasi log. Leader hanya akan menjalankan perintah kalau mayoritas node sudah mengkonfirmasi bahwa mereka sudah menerima log tersebut.

Keamanan sistem dijamin dengan cara ini. Walaupun ada node yang mati atau jaringan terputus, selama masih ada mayoritas node yang hidup, sistem tetap bisa jalan dan data tetap konsisten.

### 2. Primitif Sinkronisasi

Di lapisan ini ada tiga layanan utama yang bisa dipakai oleh aplikasi.

Pertama adalah sistem kunci terdistribusi atau Distributed Lock. Bayangkan seperti kunci toilet umum. Kalau satu orang lagi pakai, yang lain harus nunggu. Lock kita punya dua jenis: exclusive lock yang cuma bisa dipakai satu node, dan shared lock yang bisa dipakai banyak node untuk baca data. Sistem ini juga pintar mendeteksi deadlock, yaitu situasi dimana dua node saling tunggu satu sama lain sampai macet.

Kedua adalah antrian terdistribusi atau Distributed Queue. Ini seperti antrian di bank, yang datang duluan dilayani duluan atau FIFO (First In First Out). Bedanya, antrian ini bisa diakses dari banyak komputer sekaligus. Producer bisa masukin pesan dari node manapun, dan consumer bisa ambil pesan dari node manapun juga. Pesan-pesan ini disimpan secara persisten agar tidak hilang kalau ada node yang mati.

Ketiga adalah cache terdistribusi. Cache ini seperti lemari pajangan di toko yang isinya barang-barang yang sering dicari. Daripada harus ke gudang terus, kita ambil dari pajangan dulu. Cache kita pakai Redis sebagai backend penyimpanan dan menggunakan protokol MESI untuk menjaga agar cache di semua node tetap konsisten.

### 3. Lapisan Komunikasi

Lapisan ini mengatur bagaimana node-node berkomunikasi satu sama lain. Komunikasi dilakukan secara asynchronous menggunakan pattern RPC atau Remote Procedure Call. Jadi satu node bisa memanggil fungsi di node lain seolah-olah fungsi itu ada di komputer yang sama.

Untuk mendeteksi kalau ada node yang mati, sistem menggunakan heartbeat. Setiap node secara rutin mengirim sinyal "saya masih hidup" ke node lain. Kalau sinyal ini tidak datang dalam waktu tertentu, node tersebut dianggap sudah mati dan sistem akan bereaksi sesuai prosedur.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────┐
│                   Client Layer                       │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│            Synchronization Primitives                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Locks   │  │  Queue   │  │  Cache   │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│              Raft Consensus Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Node 1  │  │  Node 2  │  │  Node 3  │          │
│  │ (Leader) │  │(Follower)│  │(Follower)│          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│           Communication & Monitoring                 │
│     Message Passing │ Failure Detection              │
└─────────────────────────────────────────────────────┘
```

## Alur Data dalam Sistem

### Cara Kerja Saat Mengambil Lock (Kunci)

Pertama, aplikasi client mengirim permintaan untuk mengambil lock ke node manapun dalam cluster. Node yang menerima permintaan ini akan meneruskannya ke node leader melalui Raft. Leader kemudian akan mencatat permintaan lock ini ke dalam log dan mereplikasi log tersebut ke node-node follower.

Setelah mayoritas node mengkonfirmasi bahwa mereka sudah menerima log ini, leader akan melakukan commit. Setelah di-commit, lock dianggap sudah berhasil diambil dan client akan menerima konfirmasi bahwa lock sudah berhasil dia dapatkan. Proses ini memastikan bahwa walaupun ada node yang mati di tengah jalan, lock tetap aman dan tidak akan ada dua client yang mengambil lock yang sama.

### Cara Kerja Operasi Antrian (Queue)

Saat producer ingin memasukkan pesan ke antrian, pesan tersebut dikirim ke salah satu node. Node akan meneruskan pesan ke leader Raft untuk direplikasi. Leader akan menyimpan pesan ke dalam log dan mereplikasi ke follower-follower.

Setelah mayoritas mengkonfirmasi, pesan di-commit dan masuk ke antrian yang sudah persistent. Consumer yang ingin mengambil pesan akan membaca dari antrian yang sudah ter-commit ini. Setelah consumer selesai memproses pesan, dia akan mengirim acknowledgment bahwa pesan sudah selesai diproses. Acknowledgment ini juga dicatat di log untuk memastikan pesan tidak diproses dua kali.

### Cara Kerja Operasi Cache

Untuk operasi baca, sistem akan mengecek cache lokal terlebih dahulu. Kalau data ada di cache lokal dan masih valid, langsung dikembalikan tanpa perlu akses ke storage backend. Kalau tidak ada atau sudah tidak valid, sistem akan mengecek log Raft dan kemudian ke Redis sebagai backend storage.

Untuk operasi tulis, data baru akan di-update melalui Raft terlebih dahulu untuk memastikan konsistensi. Setelah mayoritas node mengkonfirmasi update, data akan ditulis ke Redis dan cache di semua node akan di-invalidate atau di-update sesuai dengan protokol MESI. Protokol MESI ini memastikan bahwa tidak ada node yang membaca data lama atau stale data.

## Skenario Kegagalan dan Penanganannya

### Ketika Leader Mati

Bayangkan leader tiba-tiba mati karena listrik mati atau jaringan putus. Node-node follower akan mendeteksi bahwa heartbeat dari leader sudah tidak datang lagi. Setelah timeout tertentu terlewati, follower akan memulai proses pemilihan baru secara otomatis.

Proses pemilihan biasanya selesai dalam waktu sekitar 300 milidetik atau kurang dari setengah detik. Setelah leader baru terpilih, semua operasi akan dilanjutkan dengan leader yang baru. Client tidak perlu melakukan apapun karena sistem secara otomatis akan mengarahkan request ke leader yang baru.

### Ketika Follower Mati

Kalau yang mati adalah follower, leader akan terus beroperasi normal selama masih ada mayoritas node yang hidup. Misalnya dalam cluster 3 node, kalau 1 follower mati, leader masih bisa beroperasi dengan 1 follower yang tersisa karena mayoritas adalah 2 dari 3.

Ketika follower yang mati itu hidup kembali, dia akan otomatis melakukan sinkronisasi dengan leader untuk mengejar log yang tertinggal. Proses catch-up ini dilakukan secara otomatis oleh Raft tanpa perlu intervensi manual.

### Ketika Terjadi Network Partition

Network partition terjadi ketika cluster terbelah menjadi dua kelompok yang tidak bisa berkomunikasi satu sama lain. Misalnya cluster 5 node terbelah menjadi kelompok 3 node dan kelompok 2 node karena ada kabel putus di tengah.

Kelompok yang punya mayoritas yaitu kelompok 3 node akan terus bisa beroperasi normal dan melakukan commit. Sedangkan kelompok minoritas yaitu 2 node tidak akan bisa melakukan commit apapun karena tidak punya mayoritas.

Ketika network partition sudah teratasi dan cluster menyatu kembali, kelompok minoritas akan mengikuti log dari kelompok mayoritas. Data yang sempat ditulis di kelompok minoritas akan di-rollback untuk menjaga konsistensi. Inilah mengapa Raft sangat aman untuk menjaga konsistensi data walaupun ada masalah jaringan.

## Karakteristik Performa Sistem

Berdasarkan testing yang sudah dilakukan pada satu mesin, sistem ini mampu menangani sekitar 237 operasi per detik untuk operasi konsensus Raft. Untuk operasi lock, waktu tunggu rata-rata atau latency di persentil ke-95 adalah sekitar 8.67 milidetik. Artinya 95% request lock selesai dalam waktu kurang dari 9 milidetik.

Proses pemilihan leader kalau terjadi kegagalan rata-rata memakan waktu sekitar 2 detik. Ini sudah termasuk waktu untuk mendeteksi kegagalan leader lama dan memilih leader baru. Untuk cache, tingkat cache hit rate mencapai 73%, yang artinya 73% request data bisa dilayani langsung dari cache tanpa perlu akses ke storage.

Untuk antrian pesan, sistem mampu memproses sekitar 1,200 pesan per detik. Angka ini bisa bervariasi tergantung ukuran pesan dan konfigurasi hardware yang digunakan.

## Panduan Deployment

Untuk panduan lengkap cara deploy sistem ini ke production, silakan lihat file deployment_guide.md yang ada di folder docs. Di sana dijelaskan step-by-step mulai dari persiapan server, instalasi dependencies, konfigurasi cluster, sampai monitoring dan troubleshooting.
