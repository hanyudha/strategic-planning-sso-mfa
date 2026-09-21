# M3 — Lingkungan Bisnis Internal (Internal Business Environment)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan analisis lingkungan bisnis internal UIN Syarif Hidayatullah Jakarta: proses bisnis terpengaruh autentikasi, kebutuhan pemangku kepentingan, rantai nilai (*Value Chain*), serta *business pain points*. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan analisis bisnis internal untuk formulasi strategi berikutnya.

M3 bertujuan memahami **apa yang dibutuhkan organisasi dan pengguna** dari sistem autentikasi sebelum merumuskan strategi atau memilih teknologi MFA. Seluruh analisis didasarkan pada bukti terdaftar dari M1 (`U-01` s/d `U-03`, `O-01`, `D-01`, `D-02`) dan M2 (`T-01` s/d `T-12`, `D-03`, `U-04` s/d `U-10`).

---

## 1. Tujuan Analisis M3

1. Memetakan proses bisnis utama dan pendukung universitas yang sangat bergantung pada layanan autentikasi terpusat (SSO e-Semesta).
2. Menganalisis kebutuhan dan harapan setiap kelompok pemangku kepentingan (mahasiswa, dosen, tendik, PUSTIPANDA, pimpinan) terhadap keamanan dan kenyamanan autentikasi.
3. Menyusun Rantai Nilai Bisnis (*Business Value Chain*) perguruan tinggi untuk mengidentifikasi di mana autentikasi memberikan nilai (*value*) dan di mana titik risikonya (*risk points*).
4. Mengidentifikasi masalah bisnis (*business pain points*) terkait autentikasi saat ini sebagai masukan bagi formulasi strategi.

---

## 2. Kaitan Strategis dengan Hasil M1 & M2

Analisis M3 dibangun di atas temuan faktual yang telah dikunci pada M1 dan M2:

| Baseline M1/M2 | Implikasi pada Lingkungan Bisnis Internal (M3) | Kode Bukti |
|---|---|---|
| **SSO e-Semesta melayani 45.219+ pengguna** (42.088 mahasiswa, 1.593 dosen, 1.438 tendik). | Autentikasi adalah layanan kritikal berkecepatan tinggi yang berdampak langsung pada seluruh sivitas akademika setiap hari. Kesalahan desain akan mengganggu skala operasional besar. | M1; U-01, O-01 |
| **44 client terdaftar di Keycloak** mencakup seluruh ranah akademik, SDM, keuangan, riset, admisi, hingga akses Wi-Fi kampus. | Autentikasi SSO merupakan *single point of access* sekaligus *single point of failure* bagi seluruh ekosistem digital kampus. | T-10, T-11, T-12 |
| **Password default berbasis NIK & Password Policy kosong**. | Risiko kompromi akun tinggi yang dapat mengancam integritas data akademik, kerahasiaan data SDM/keuangan, serta penyalahgunaan akses Wi-Fi kampus. | T-06, U-06, U-07 |
| **Beban tiket helpdesk SMILE (2.624 tiket)** terkait login/reset password. | Menunjukkan beban operasional nyata pada tim layanan PUSTIPANDA dan potensi frustrasi pengguna saat mengalami masalah akses. | D-02, U-03 |
| **Otomatisasi siklus hidup akun** (eRegistrasi -> eAkademik -> SSO, serta disable 3 bulan pasca LULUS / seketika saat nonaktif/DO). | Proses bisnis akademik telah memiliki aturan otomatisasi yang harus dijaga keberlanjutannya saat MFA diterapkan. | U-09, U-10 |

---

## 3. Analisis Proses Bisnis yang Terpengaruh Autentikasi

### 3.1 Ranah Layanan Akademik & Kemahasiswaan
* **Admisi & Registrasi Mahasiswa Baru** (`eadmisi`, `eRegistrasi`): Proses krusial dalam penerimaan dan verifikasi calon mahasiswa. Kegagalan autentikasi pada tahap ini berdampak langsung pada kesan pertama pengguna dan kelancaran pencatatan mahasiswa baru.
* **Perkuliahan & Pembelajaran** (`eAkademik`, `eAkademik-portal`, `dev-lms`): Pengisian KRS, penilaian, jadwal perkuliahan, dan materi perkuliahan daring. Akses harian intensif oleh puluhan ribu mahasiswa dan dosen.
* **Tugas Akhir, KKN & Riset** (`eRiset`, `eKKN`, `PLO`): Pengelolaan skripsi/tesis, surat dinas, dan pengabdian masyarakat. Mengandung data penelitian dan dokumen resmi institusi.
* **Kelulusan & Alumni** (`eAlumni`): Transisi status dari mahasiswa aktif menjadi alumni. Penonaktifan akun SSO 3 bulan pasca lulus menjaga batas keamanan data internal universitas.

### 3.2 Ranah Tata Kelola Kepegawaian & Sumber Daya Manusia
* **Pengelolaan Data Pegawai & Dosen** (`eSDM`): Pengelolaan profil, kenaikan pangkat, dan status kepegawaian. eSDM memiliki kewenangan mengaktifkan/menonaktifkan akun SSO pegawai secara *real-time*.
* **Penilaian Kinerja** (`eKinerja`): Evaluasi kinerja dosen dan tendik. Data bersifat sensitif dan rahasia individu.

### 3.3 Ranah Keuangan, Aset & Operasional Kampus
* **Pembayaran & Keuangan** (`eFinansi`, `ePembayaran`): Transaksi dan verifikasi pembayaran UKT/BOPTN. Membutuhkan jaminan integritas data yang sangat tinggi.
* **Inventaris Aset** (`eAset`): Pencatatan Barang Milik Negara (BMN).
* **Akses Internet Kampus** (`Wi-Fi SSO`): Layanan mobilitas harian di area kampus dengan batas 3 perangkat simultan per akun.

---

## 4. Analisis Kebutuhan Pemangku Kepentingan (Stakeholder Needs)

| Pemangku Kepentingan | Peran dalam SSO | Kebutuhan Utama (*Needs*) | Tantangan / Pain Points |
|---|---|---|---|
| **Mahasiswa** | Pengguna akhir skala terbesar (~42rb) | Akses cepat dan stabil ke eAkademik, LMS, dan Wi-Fi; proses pemulihan akun yang mandiri dan tidak rumit. | Password default berisiko; kebingungan saat lupa password; potensi hambatan jika MFA terlalu rumit (*friction*). |
| **Dosen** | Pengguna akademik utama (~1.500) | Kelancaran menginput nilai dan materi; keamanan data pribadi dan karya ilmiah; kemudahan akses dari luar kampus. | Username/password default (NIK) rawan ditebak; risiko kompromi akun yang mempengaruhi data perkuliahan. |
| **Tenaga Kependidikan (Tendik)** | Pengguna operasional & admin aplikasi (~1.400) | Keamanan akses ke aplikasi administratif (eSDM, eFinansi, PLO); pemisahan kewenangan (*role-based access*). | Password default (NIK) rawan ditebak; tidak ada MFA pada akun berwewenang tinggi. |
| **Tim PUSTIPANDA (Helpdesk & Layanan)** | Pengelola operasional & bantuan pengguna | Pengurangan volume tiket reset password; alat bantu pemulihan akun yang aman; prosedur verifikasi identitas yang jelas. | Menangani ribuan tiket manual via SMILE; tidak ada kebijakan verifikasi email pada SSO (T-04). |
| **Tim Infrastruktur & Keamanan IT** | Pengelola server & sistem SSO | Keamanan infrastruktur terpusat; visibilitas audit/logging (Login & Admin Events); keterkendalian retensi log. | Password policy kosong (T-06); log events menumpuk tanpa batas retensi (T-08); ancaman *credential stuffing*. |
| **Pimpinan Universitas** | Pemilik kebijakan & penanggung jawab institusi | Pelindungan reputasi UIN Jakarta; kepatuhan pada regulasi pelindungan data pribadi (UU PDP); keberlanjutan layanan e-Semesta. | Risiko kebocoran data sivitas akademika akibat autentikasi faktor tunggal (*single-factor password*). |

---

## 5. Rantai Nilai Bisnis Universitas (Business Value Chain)

Mengadaptasi kerangka *Value Chain* Ward & Peppard untuk lingkungan perguruan tinggi:

```text
+-----------------------------------------------------------------------------------+
| AKTIVITAS PENDUKUNG (SUPPORT ACTIVITIES)                                          |
| - Tata Kelola Organisasi & Kebijakan: Kebijakan Keamanan Informasi & Sistem      |
| - Manajemen SDM (eSDM): Pengelolaan Dosen & Tendik, Sync Real-time ke SSO         |
| - Pengelolaan Keuangan & BMN (eFinansi, ePembayaran, eAset)                       |
| - Infrastruktur Teknologi & Jaringan (PUSTIPANDA, Keycloak SSO, Wi-Fi Kampus)     |
+-----------------------------------------------------------------------------------+
| AKTIVITAS UTAMA (PRIMARY ACTIVITIES)                                              |
| [Penerimaan Mhs]  -> [Pembelajaran &]   -> [Riset & Pengabdian] -> [Kelulusan &]    |
| (eadmisi,          (eAkademik, LMS,        (eRiset, eKKN, PLO)     (eAlumni,         |
|  eRegistrasi)       Wi-Fi Kampus)                                   Disable SSO)   |
+-----------------------------------------------------------------------------------+
                                        |
                          PERAN SSO: PERLINDUNGAN NILAI
```

### 5.1 Peran Autentikasi dalam Rantai Nilai
* **Sebagai Enabler Akses**: Memungkinkan seluruh aktivitas utama (penerimaan, pembelajaran, riset, kelulusan) dan aktivitas pendukung berjalan secara digital melalui satu identitas terpadu (e-Semesta).
* **Sebagai Penjual/Pelindung Nilai (*Value Safeguard*)**: Melindungi integritas nilai yang dihasilkan (nilai akademik, karya ilmiah, transaksi keuangan, data pribadi) dari ancaman penyerobotan akun dan kebocoran data.

---

## 6. Masalah Bisnis Utama Terkait Autentikasi (Business Pain Points)

Berdasarkan sintesis data M1, M2, dan analisis lingkungan internal M3:

1. **Rentan Terhadap Penyerobotan Akun (*Credential Guessing & Stuffing*)**:
   - Pola password default yang sangat terprediksi berbasis NIK (`Mhs`+NIK untuk mahasiswa; NIK langsung untuk dosen/tendik).
   - Ketiadaan kebijakan password (*Password Policy* kosong di Keycloak, T-06).
   - Username bersifat publik/mudah diketahui (NIM dan nama lengkap).
2. **Ketiadaan Faktor Autentikasi Kedua (MFA)**:
   - Meskipun provider OTP tersedia (T-01) dan `Configure OTP` enabled (T-04), MFA **belum diwajibkan (bukan Default Action)**. Pertahanan sepenuhnya bergantung pada kata sandi tunggal.
3. **Beban Operasional Layanan Bantuan (Helpdesk Overhead)**:
   - Tingginya volume tiket penanganan masalah login/reset password di SMILE (2.624 tiket pada ekspor D-02).
   - Tidak adanya fitur verifikasi email (*Verify Email* disabled, T-04), sehingga pemulihan mandiri terbatas dan mendorong pengguna menghubungi helpdesk.
4. **Risiko Akses Privileged / Admin**:
   - Akun tendik dan dosen yang memiliki akses administratif pada aplikasi kritis (seperti eFinansi, eSDM, eAkademik) hanya dilindungi oleh kata sandi tunggal berbasis NIK.

---

## 7. Kesimpulan & Masukan untuk Milestone Berikutnya

Analisis lingkungan bisnis internal M3 menegaskan bahwa **perbaikan sistem autentikasi SSO bukan sekadar proyek teknis IT, melainkan kebutuhan bisnis strategis universitas** untuk:
* Melindungi reputasi dan data sivitas akademika UIN Jakarta.
* Menjamin kelangsungan operasional 44 aplikasi terintegrasi.
* Mengurangi beban operasional penanganan tiket manual di PUSTIPANDA.
* Memastikan penerapan MFA di masa depan dirancang agar **fleksibel, aman, namun tidak menyulitkan pengguna (*user-friendly*)**.

---

## 8. Langkah Selanjutnya

Setelah M3 disetujui, tahap berikutnya adalah **Milestone 4 (M4: Lingkungan Bisnis Eksternal / External Business Environment)** untuk menganalisis regulasi (UU PDP, Permendikbud), tren teknologi perguruan tinggi, dan lanskap ancaman keamanan eksternal.
