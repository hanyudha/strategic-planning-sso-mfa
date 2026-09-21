# M1 — Konteks Organisasi

## Status

**LOCKED — dikunci pada 2026-09-21 sebagai baseline M1.**

Dokumen ini menyajikan keluaran Milestone 1 untuk studi *Perencanaan Strategis Pengembangan Single Sign-On (SSO) Terintegrasi Multi-Factor Authentication (MFA) untuk Meningkatkan Keamanan Layanan Digital Perguruan Tinggi*. Isi yang belum didukung bukti diberi tanda `[EVIDENCE NEEDED]`; bagian yang perlu divalidasi diberi tanda `[TO BE VALIDATED]`.

M1 dikunci dengan catatan bahwa beberapa gap bukti masih sengaja dipertahankan secara eksplisit. Gap yang berkaitan dengan arsitektur, mekanisme autentikasi, logging, kontrol keamanan, dan integrasi teknis dibawa ke M2.

Kode sumber bukti: `U-01` = data pengguna putaran pertama, 2026-09-21; `U-02` = data pengguna putaran kedua, 2026-09-21; `U-03` = data pengguna putaran ketiga, 2026-09-21; `O-01` = situs resmi PUSTIPANDA, diakses 2026-09-21; `D-01` = Surat B-42/UPT.2/TI.05.04/04/2026, 29 April 2026; `D-02` = ekspor tiket SMILE, 2026-09-21.

## 1. Tujuan M1

Menetapkan konteks organisasi dan layanan SSO berdasarkan bukti sebelum melakukan analisis lingkungan bisnis, kondisi teknis, gap, atau strategi MFA. M1 tidak memilih produk MFA dan tidak merancang implementasi teknis.

## 2. Profil Organisasi

| Elemen | Informasi | Status bukti / sumber |
|---|---|---|
| Nama resmi institusi | UIN Syarif Hidayatullah Jakarta. | U-01 — data pengguna, 2026-09-21; dikonfirmasi melalui [situs resmi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/tentang-pustipanda) |
| Jenis dan status institusi | Perguruan tinggi; PUSTIPANDA adalah unsur penunjang penyelenggaraan pendidikan di lingkungan universitas. Detail bentuk badan dan akreditasi: `[EVIDENCE NEEDED]`. | [Tentang PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/tentang-pustipanda), diakses 2026-09-21 |
| Lokasi kampus / cakupan layanan | Alamat PUSTIPANDA yang dipublikasikan: Jl. Kertamukti No.10, Pisangan, Ciputat Timur, Kota Tangerang Selatan, Banten 15419. Cakupan kampus/layanan institusi: `[EVIDENCE NEEDED]`. | [Visi dan Misi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/visi-misi), diakses 2026-09-21 |
| Visi institusi | Perguruan Tinggi Bereputasi Global dengan Keunggulan Integrasi Ilmu Keislaman, Keindonesiaan dan Sains. | [Visi dan Misi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/visi-misi), diakses 2026-09-21 |
| Visi unit TI | “Lembaga teknologi informasi perguruan tinggi yang unggul dalam pengembangan integrasi ilmu keislaman, keindonesiaan dan sains yang bereputasi global.” | [Visi dan Misi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/visi-misi), diakses 2026-09-21 |
| Misi unit TI yang relevan | Layanan TI untuk pendidikan/pengajaran bereputasi global; riset bermutu; akses pendidikan tinggi berkeadilan; serta tata kelola berbasis sistem informasi yang profesional, akuntabel, berintegritas, dan entrepreneurial. | [Visi dan Misi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/visi-misi), diakses 2026-09-21 |
| Unit pengelola TI | Unit Pelaksana Teknis (UPT) Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA), dengan tugas mengelola serta mengembangkan sistem informasi dan pangkalan data universitas. | U-01 — data pengguna; [Tentang PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/tentang-pustipanda), diakses 2026-09-21 |
| Unit pemilik proses layanan akademik dan administrasi | `[EVIDENCE NEEDED]` | Struktur organisasi / proses bisnis |
| Populasi pengguna digital | Mahasiswa: 42.088; staf akademik: 1.438; dosen: 1.593. Definisi “staf akademik” dan kemungkinan tumpang tindih dengan dosen perlu dikonfirmasi. | U-01 — data pengguna, 2026-09-21 |
| Strategi transformasi digital yang relevan | `[EVIDENCE NEEDED]` | Renstra / master plan TI |

### Fungsi layanan yang perlu divalidasi

| Fungsi | Peran terhadap SSO/MFA | Bukti yang diperlukan |
|---|---|---|
| Akademik dan pembelajaran | Akses mahasiswa serta dosen ke layanan akademik/pembelajaran. `[TO BE VALIDATED]` | Daftar layanan, pemilik proses, kelompok pengguna |
| Administrasi institusi | Akses tenaga kependidikan ke layanan administrasi. `[TO BE VALIDATED]` | Daftar layanan dan kebutuhan akses |
| Penelitian dan pengabdian | Potensi akses ke layanan riset/kolaborasi. `[TO BE VALIDATED]` | Daftar layanan dan kebijakan akses |
| Manajemen institusi | Potensi akses akun staf/pimpinan ke layanan penting. `[TO BE VALIDATED]` | Daftar layanan dan klasifikasi sensitivitas |

## 3. Peta Pemangku Kepentingan

| Pemangku kepentingan | Kepentingan / kebutuhan yang perlu dikonfirmasi | Peran dalam M1 | Pengaruh | Bukti / narasumber |
|---|---|---|---|---|
| Pimpinan universitas | Menyetujui kebijakan dan perubahan SSO. | Pemilik keputusan/persetujuan | Tinggi | U-02 — data pengguna, 2026-09-21; dokumen penetapan formal perlu ditelusuri |
| UPT PUSTIPANDA / Kepala PUSTIPANDA | Mengelola TI dan SSO, menyediakan reset mandiri e-Semesta, serta menindaklanjuti reset kata sandi lupa melalui bagian layanan/SMILE. | Pengelola operasional dan layanan SSO | Tinggi | U-01, U-02, dan U-03 — data pengguna, 2026-09-21 |
| Akademik Pusat dan akademik fakultas | Pemilik proses eRegistrasi, eAkademik, dan eAkademik Portal; kelancaran akses proses akademik. | Pemilik proses / data akademik | Sedang–tinggi | U-02 dan U-03 — data pengguna, 2026-09-21 |
| Keuangan dan Perencanaan | Pemilik proses eFinansi. | Pemilik proses/data keuangan | Tinggi | U-02 — data pengguna, 2026-09-21 |
| SDM / Kepegawaian | Pemilik proses dan data eSDM; perubahan status/peran serta penonaktifan dosen/tendik diselesaikan pada sistem/unit ini. | Pemilik data/proses SDM | Tinggi | U-02 — data pengguna, 2026-09-21 |
| Pusat Informasi dan Humas | Pemilik CMS Website. | Pemilik aplikasi/proses | Sedang | U-02 — data pengguna, 2026-09-21 |
| Tim BMN | Pemilik eAset. | Pemilik aplikasi/proses | Sedang | U-03 — data pengguna, 2026-09-21 |
| Pusat Tata Usaha | Pemilik ePLO. | Pemilik aplikasi/proses | Sedang | U-03 — data pengguna, 2026-09-21 |
| Mahasiswa | Akses mudah dan aman ke layanan digital. | Pengguna utama | Sedang | U-01 — 42.088 mahasiswa, 2026-09-21 |
| Dosen | Akses pembelajaran, akademik, dan layanan institusi. | Pengguna utama | Sedang | U-01 — 1.593 dosen, 2026-09-21 |
| Staf akademik / tendik | Akses layanan administrasi sesuai tugas. Klasifikasi “staf akademik” dan “tendik” perlu dikonfirmasi. | Pengguna utama | Sedang | U-01 — 1.438 staf akademik, 2026-09-21 |
| Pengelola aplikasi terintegrasi | Keandalan integrasi dan ketepatan otorisasi. `[TO BE VALIDATED]` | Pemilik aplikasi | Tinggi | `[EVIDENCE NEEDED]` |
| Unit hukum/audit/keamanan informasi (jika ada) | Kebijakan, kepatuhan, dan audit autentikasi. `[TO BE VALIDATED]` | Pengawasan / advis | Sedang–tinggi | `[EVIDENCE NEEDED]` |

### Analisis awal keterlibatan

Peta akhir perlu menetapkan pemilik keputusan SSO, pemilik data identitas, pengelola teknis, pemilik aplikasi, serta kelompok pengguna terdampak. Hubungan tersebut belum dapat disimpulkan dari dokumen baseline yang tersedia.

## 4. Konteks Layanan SSO

| Elemen | Kondisi yang diketahui | Status bukti / informasi lanjutan |
|---|---|---|
| Keberadaan SSO | SSO sudah operasional dan digunakan sebagai mekanisme autentikasi layanan digital. Situs resmi PUSTIPANDA mempublikasikannya dengan nama “SSO e-Semesta”. Surat resmi 29 April 2026 memberitahukan penerapan SSO untuk akses Wi-Fi kampus mulai 1 Mei 2026. | Fakta kasus dalam `PROJECT_CONTEXT.md` dan `README.md`; [Katalog Aplikasi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/katalog-aplikasi), diakses 2026-09-21; D-01 |
| MFA | SSO belum terintegrasi MFA. | Fakta kasus dalam `PROJECT_CONTEXT.md` dan `README.md` |
| Identitas pengguna | Data mahasiswa berasal dari eAkademik/eRegistrasi; data dosen dan tendik dari eSDM. Mekanisme sinkronisasi serta pemilik data perlu dikonfirmasi. | U-01 — data pengguna, 2026-09-21 |
| Kategori pengguna | Mahasiswa, dosen, serta staf akademik/tendik. Tidak ada pengguna eksternal (alumni, orang tua, mitra, atau tamu) pada saat informasi ini dikumpulkan. D-01 secara khusus mencakup civitas akademika, dengan SSID berbeda untuk mahasiswa dan dosen/tendik. | U-01 dan U-02 — data pengguna, 2026-09-21; D-01 |
| Layanan terintegrasi | eAkademik, eAkademik Portal, eAset, eBeasiswa, eFinansi, eKinerja, eRegistrasi, CMS Website, ePLO, dan eSDM telah terintegrasi SSO. | U-02 — data pengguna, 2026-09-21 |
| Mekanisme autentikasi saat ini | Kredensial awal mahasiswa dilaporkan dibentuk dari pengenal institusional. Pola persis tidak dicantumkan dalam dokumen perencanaan karena bersifat sensitif; perlu validasi pengelola SSO dan evaluasi kebijakan penggantian kata sandi awal. | U-01 — data pengguna, 2026-09-21; detail sensitif tidak direplikasi |
| Siklus hidup akun | Akun mahasiswa aktif otomatis ketika status calon mahasiswa menjadi mahasiswa di eRegistrasi dan data masuk eAkademik. Akun tendik aktif ketika dibuat di eSDM. Perubahan status/peran serta penonaktifan dosen/tendik dikelola pada eSDM oleh SDM/Kepegawaian dan secara otomatis memperbarui akun serta akses SSO. | U-01, U-02, dan U-03 — data pengguna, 2026-09-21 |
| Pengelolaan akses khusus/privileged | `[EVIDENCE NEEDED]` | Kelompok admin, proses persetujuan, dan kontrol akses |
| Akses Wi-Fi SSO | Akses Wi-Fi kampus melalui SSO berlaku mulai 1 Mei 2026. Satu akun dapat digunakan maksimal pada tiga perangkat secara bersamaan; panduan pengguna menunjukkan autentikasi ulang setelah terputus lebih dari 60 menit. | D-01 |
| Logging dan audit autentikasi | Log login tersedia, dengan akses server SSO yang berwenang pada tim infrastruktur atau data center. Jenis log dan masa retensi: `[EVIDENCE NEEDED]`. | U-01 dan U-03 — data pengguna, 2026-09-21 |
| Dukungan pengguna | Reset mandiri e-Semesta digunakan untuk mengubah kata sandi awal/default menjadi kata sandi pilihan pengguna. SMILE digunakan ketika pengguna lupa kata sandi; bagian layanan PUSTIPANDA mengeksekusi reset ke kondisi default. Target SLA standar: satu hari kerja. Kanal WhatsApp/surel pada D-01 dapat diperlakukan sebagai dukungan tambahan, tetapi alur eskalasinya perlu dikonfirmasi. | U-01, U-02, dan U-03 — data pengguna; D-01 |
| Kebijakan dan SOP | Belum tersedia untuk studi ini. | U-01 — data pengguna, 2026-09-21; perlu penelusuran dokumen |

### Inventaris layanan SSO yang harus dilengkapi

| No. | Nama layanan/aplikasi | Pemilik layanan | Pengguna | Terintegrasi SSO? | Data/proses yang dilayani | Kritikalitas | Bukti |
|---:|---|---|---|---|---|---|---|
| 1 | eAkademik | Akademik Pusat dan akademik fakultas | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | Data mahasiswa dan dosen | Tinggi | U-02 |
| 2 | eRegistrasi | Akademik Pusat | Mahasiswa: `[TO BE VALIDATED]` | Ya | Registrasi mahasiswa | `[EVIDENCE NEEDED]` | U-02 |
| 3 | eSDM | SDM / Kepegawaian | Dosen dan tendik: `[TO BE VALIDATED]` | Ya | Data SDM | `[EVIDENCE NEEDED]` | U-02 |
| 4 | eAkademik Portal | Akademik Pusat dan akademik fakultas | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | `[EVIDENCE NEEDED]` | `[EVIDENCE NEEDED]` | U-02 dan U-03 |
| 5 | eAset | Tim BMN | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | `[EVIDENCE NEEDED]` | `[EVIDENCE NEEDED]` | U-02 dan U-03 |
| 6 | eBeasiswa | Akademik Pusat | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | `[EVIDENCE NEEDED]` | `[EVIDENCE NEEDED]` | U-02 dan U-03 |
| 7 | eFinansi | Keuangan dan Perencanaan | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | Data keuangan | Tinggi | U-02 |
| 8 | eKinerja | Kepegawaian | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | `[EVIDENCE NEEDED]` | `[EVIDENCE NEEDED]` | U-02 dan U-03 |
| 9 | CMS Website | Pusat Informasi dan Humas | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | Pengelolaan konten website: `[TO BE VALIDATED]` | `[EVIDENCE NEEDED]` | U-02 |
| 10 | ePLO | Pusat Tata Usaha | Mahasiswa, dosen, tendik: `[TO BE VALIDATED]` | Ya | `[EVIDENCE NEEDED]` | `[EVIDENCE NEEDED]` | U-02 dan U-03 |
| 11 | Wi-Fi kampus SSO | PUSTIPANDA: `[TO BE VALIDATED]` | Mahasiswa, dosen, dan tendik | Ya | Akses jaringan internet Wi-Fi kampus | Tinggi untuk ketersediaan layanan akses; klasifikasi formal: `[EVIDENCE NEEDED]` | D-01 |

## 5. Evidence Register

| ID | Klaim / informasi | Status | Sumber / narasumber | Tanggal bukti | Kualitas / validasi | Dampak terhadap analisis |
|---|---|---|---|---|---|---|
| E-01 | Institusi merupakan perguruan tinggi. | Tersedia | `PROJECT_CONTEXT.md` | 2026-09-21 | Baseline kasus; detail institusi belum tersedia | Menentukan konteks organisasi studi |
| E-02 | SSO sudah operasional. | Tersedia | `PROJECT_CONTEXT.md`, `README.md` | 2026-09-21 | Baseline kasus | Menetapkan bahwa studi bukan implementasi SSO baru |
| E-03 | SSO belum menggunakan MFA. | Tersedia | `PROJECT_CONTEXT.md`, `README.md` | 2026-09-21 | Baseline kasus | Menetapkan masalah strategis awal |
| E-04 | Identitas institusi, visi, misi, serta peran PUSTIPANDA. | Tersedia dan dikonfirmasi | O-01 — situs resmi PUSTIPANDA | 2026-09-21 | Sumber primer organisasi | Menilai keselarasan strategi dan konteks unit TI |
| E-05 | Pimpinan universitas menyetujui kebijakan/perubahan SSO; PUSTIPANDA mengelola operasional SSO. | Tersedia; penetapan formal perlu validasi | U-02 — data pengguna | 2026-09-21 | Perlu SK/struktur atau konfirmasi narasumber | Menentukan tata kelola dan stakeholder |
| E-06 | Populasi pengguna dan sepuluh aplikasi terintegrasi SSO. | Tersedia; pengguna spesifik dan kritikalitas sebagian aplikasi belum tersedia | U-01, U-02, dan U-03 — data pengguna | 2026-09-21 | Perlu inventaris / wawancara | Menentukan cakupan, prioritas, dan dampak |
| E-06A | Sumber data identitas, aktivasi akun awal, serta pembaruan otomatis akses SSO saat status/peran dosen/tendik berubah di eSDM. | Tersedia; mekanisme sinkronisasi teknis perlu divalidasi pada M2 | U-01, U-02, dan U-03 — data pengguna | 2026-09-21 | Perlu dokumentasi proses / wawancara | Menentukan keterkaitan siklus hidup akun |
| E-07 | Kebijakan/SOP autentikasi dan pengelolaan akun. | Belum tersedia | `[EVIDENCE NEEDED]` | — | Perlu dokumen kebijakan | Menilai kesiapan proses dan governance |
| E-08 | Dukungan gangguan dan reset password tersedia melalui SMILE, dengan target SLA standar satu hari kerja; log login diakses oleh tim infrastruktur/data center yang memiliki akses server SSO. | Sebagian tersedia | U-01, U-02, dan U-03 — data pengguna | 2026-09-21 | Jenis log, retensi, dan prosedur peninjauan belum tersedia | Mengidentifikasi masalah dan kebutuhan kontrol |
| E-09 | Pengguna mengalami kendala lupa kata sandi dan penggantian perangkat. | Tersedia; perlu data volume/dampak | U-01 — data pengguna | 2026-09-21 | Perlu statistik tiket atau wawancara pengguna | Menilai kesiapan dukungan pengguna dan pengalaman autentikasi |
| E-10 | Situs resmi mempublikasikan SSO e-Semesta dan sejumlah aplikasi dalam portofolio PUSTIPANDA. | Tersedia | [Katalog Aplikasi PUSTIPANDA](https://pustipanda.uinjkt.ac.id/id/katalog-aplikasi) | 2026-09-21 | Sumber primer organisasi; tidak membuktikan integrasi SSO setiap aplikasi | Mendukung inventaris dan konteks layanan |
| E-11 | Reset mandiri e-Semesta aktif untuk mengubah kata sandi awal/default menjadi kata sandi pilihan pengguna. | Tersedia; mekanisme teknis rinci di M2 | U-03 — data pengguna; [Panduan Reset Sandi e-Semesta](https://pustipanda.uinjkt.ac.id/id/video-panduan-reset-mandiri-sandi-e-semesta) | 2026-09-21 | Sumber pengguna dan situs resmi saling mendukung | Menentukan alur dukungan pengguna |
| E-12 | PUSTIPANDA memberitahukan penerapan SSO untuk akses Wi-Fi kampus, berlaku mulai 1 Mei 2026. | Tersedia dan terverifikasi | D-01 — Surat B-42/UPT.2/TI.05.04/04/2026, 29 April 2026 | 2026-04-29 | Surat resmi ditandatangani Kepala PUSTIPANDA | Menetapkan tanggal dan cakupan penerapan Wi-Fi SSO |
| E-13 | Ketentuan Wi-Fi SSO mencakup autentikasi civitas akademika, SSID per kategori pengguna, batas tiga perangkat simultan, autentikasi ulang setelah putus lebih dari 60 menit, serta kewajiban menjaga kredensial. | Tersedia dan terverifikasi | D-01 — lampiran ketentuan/panduan Wi-Fi SSO | 2026-04-29 | Lampiran surat resmi | Menentukan konteks layanan dan kendala penggunaan yang relevan |
| E-14 | SMILE aktif untuk kasus lupa kata sandi dan mengembalikan kata sandi ke kondisi default; kanal WhatsApp/surel pada D-01 merupakan dukungan tambahan. | Tersedia; alur eskalasi antar-kanal perlu dikonfirmasi | U-03 — data pengguna; D-01 | 2026-09-21 | Konfirmasi pengguna; SOP layanan belum tersedia | Menentukan alur dukungan pengguna yang akurat |
| E-15 | Ekspor tiket terkait kata sandi atau masalah login berisi 2.624 tiket yang dibuat 1 Januari-21 September 2026. | Tersedia; kriteria pencarian ekspor tidak tersimpan pada CSV | D-02 — ekspor tiket SMILE | 2026-09-21 | Analisis hanya menggunakan agregat tanpa identitas pelapor/isi tiket | Mengukur konteks beban layanan autentikasi |

### Ringkasan agregat tiket autentikasi

Ekspor D-02 disampaikan pengguna sebagai hasil pencarian tiket terkait kata sandi atau masalah login. Rentang aktual pada kolom `Date Created` adalah 1 Januari hingga 21 September 2026; karena itu, klaim cakupan sampai 30 September belum didukung oleh isi ekspor. Data identitas pelapor, alamat surel, dan isi subjek tiket tidak direplikasi dalam dokumen ini.

| Metrik | Nilai | Catatan interpretasi |
|---|---:|---|
| Jumlah tiket | 2.624 | Seluruh tiket dalam ekspor. |
| Status pada waktu ekspor | 1.626 closed, 988 resolved, 10 open | Status closed/resolved tidak otomatis sama dengan pemenuhan SLA. |
| Tiket dengan `Closed Date` | 2.614 | Sepuluh tiket belum memiliki tanggal penutupan. |
| Interval dibuat hingga ditutup | Median 88,4 jam; 1.056 tiket (40,2%) ditutup dalam 24 jam kalender | Ini adalah interval menuju *closed date*, bukan ukuran waktu respons pertama atau pembuktian SLA hari kerja. |
| Kolom SLA | `SLA Plan`, `SLA Due Date`, dan `Due Date` kosong pada seluruh ekspor; `Overdue` bernilai No pada seluruh tiket | Kepatuhan target satu hari kerja tidak dapat dinilai secara andal dari D-02. |
| Sumber tiket | `Email` pada seluruh tiket | Tidak cukup untuk menyimpulkan bahwa tiket tidak berasal dari SMILE, karena integrasi kanal belum dibuktikan. |

| Bulan dibuat | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep (s.d. 21) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jumlah tiket | 633 | 335 | 250 | 172 | 165 | 162 | 291 | 344 | 272 |

## 6. Konteks Masalah Awal

### Pernyataan masalah kerja

SSO institusi telah memusatkan autentikasi untuk layanan digital, namun belum menggunakan MFA. Berdasarkan bukti baseline, institusi perlu merumuskan arah strategis untuk memperkuat keamanan dan tata kelola akses melalui kapabilitas MFA yang sesuai kebutuhan organisasi.

Surat resmi menunjukkan bahwa SSO juga menjadi kontrol autentikasi untuk akses Wi-Fi kampus mulai 1 Mei 2026, dengan tujuan meningkatkan keamanan penggunaan jaringan internet. Bukti ini berlaku khusus untuk layanan Wi-Fi; surat tersebut tidak membuktikan tanggal awal implementasi SSO pada seluruh aplikasi terintegrasi. `[INFERENCE]`

Konteks tersebut mendukung arah organisasi dan PUSTIPANDA untuk menyediakan layanan teknologi informasi yang berkualitas, profesional, akuntabel, dan bereputasi global. `[INFERENCE]` Keterkaitan ini berasal dari visi/misi yang diberikan pengguna; indikator kinerja dan prioritas formal institusi tetap perlu dibuktikan melalui Renstra atau dokumen kebijakan.

Kendala lupa kata sandi dan penggantian perangkat, bersama 2.624 tiket yang dikumpulkan pengguna sebagai kasus kata sandi atau login, menunjukkan bahwa perubahan autentikasi di masa depan perlu mempertimbangkan pengalaman pengguna serta kapasitas layanan bantuan. `[INFERENCE]` Ekspor belum menyimpan kriteria pencarian dan tidak memiliki klasifikasi yang cukup rinci untuk memisahkan volume setiap jenis masalah secara andal.

### Batas inferensi saat ini

Belum ada bukti yang mendukung pernyataan rinci tentang arsitektur/penyedia SSO, pola serangan atau insiden, regulasi yang berlaku, kebijakan internal, dan kelemahan kontrol tertentu. Beberapa pemilik aplikasi, kelompok pengguna spesifik, serta kritikalitas juga belum lengkap. Karena itu, belum dapat ditetapkan prioritas pengguna, model MFA, arsitektur target, maupun KPI akhir.

## 7. Pertanyaan Data M1 yang Masih Terbuka

### A. Bukti tata kelola dan arah organisasi

1. Apakah tersedia Renstra, rencana transformasi digital, struktur organisasi, atau SK yang menegaskan peran PUSTIPANDA dan kewenangan persetujuan pimpinan universitas atas SSO?
2. Apakah terdapat unit keamanan informasi, audit internal, hukum, atau perlindungan data? Apa perannya?
3. Berapa tanggal/acuan statistik populasi mahasiswa, dosen, dan staf akademik yang diberikan, serta apakah kategori staf akademik mencakup tendik?

### B. Inventaris dan proses layanan

4. Siapa pengguna utama eAkademik Portal, eAset, eBeasiswa, eKinerja, dan ePLO; serta data/proses apa yang dilayani masing-masing?
5. Apakah eRegistrasi, eSDM, CMS Website, serta aplikasi lain perlu diberi klasifikasi kritikalitas? Jika ya, apa dasar klasifikasinya?
6. Siapa pemilik proses/prosedur akun mahasiswa saat lulus, mengundurkan diri, atau tidak aktif?

### C. Kebijakan dan kondisi operasional

7. Dokumen kebijakan/SOP apa yang tersedia untuk kata sandi, akun, autentikasi, akses, privasi, dan insiden? Jika belum ada/tersedia, siapa yang dapat mengonfirmasi hal tersebut?
8. Bagaimana hubungan kanal WhatsApp/surel PUSTIPANDA dengan alur reset melalui SMILE? Apakah keduanya merupakan jalur eskalasi layanan yang sama?
9. Tanpa meminta isi log, apakah pengelola dapat mengonfirmasi jenis log login yang tersedia, masa retensi, dan prosedur peninjauannya?
10. Apakah batas tiga perangkat simultan dan autentikasi ulang Wi-Fi setelah terputus lebih dari 60 menit masih berlaku, serta apakah terdapat pengecualian yang terdokumentasi?

## 8. Catatan Penguncian M1

M1 dikunci karena telah tersedia baseline yang cukup untuk konteks organisasi:

- profil serta arah strategis organisasi yang relevan;
- pemilik keputusan, pengelola SSO, pemilik data identitas, dan kelompok pengguna utama;
- inventaris awal layanan yang memakai SSO beserta pemilik dan pengguna utamanya;
- kebijakan/SOP serta bukti kondisi layanan yang tersedia;
- evidence register yang menautkan setiap klaim penting ke sumbernya; dan
- konteks masalah awal yang tidak mengandung fakta atau asumsi tanpa penanda.

Informasi yang belum tersedia tidak dihilangkan, melainkan diberi penanda `[EVIDENCE NEEDED]` atau `[TO BE VALIDATED]` dan akan menjadi bahan pengumpulan data pada milestone berikutnya.

## 9. Batas Milestone

Dokumen ini hanya menyusun konteks organisasi. Analisis arsitektur SSO rinci dimulai pada M2 setelah M1 ditinjau dan dikunci.
