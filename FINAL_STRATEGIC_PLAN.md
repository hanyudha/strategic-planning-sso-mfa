# PERENCANAAN STRATEGIS SISTEM INFORMASI DENGAN METODE WARD & PEPPARD FOR INTEGRATION OF MULTI-FACTOR AUTHENTICATION (MFA) ON SINGLE SIGN-ON (SSO) AT UIN SYARIF HIDAYATULLAH JAKARTA

---

## DOKUMEN RENCANA STRATEGIS FINAL (FINAL STRATEGIC PLAN)
**Milestone 14 — Integrasi Laporan Akhir Akademik**  
**Tanggal Pengesahan:** 21 September 2026  
**Status Dokumen:** DIKUNCI / LOCKED (M0 s/d M14)  
**Institusi:** UIN Syarif Hidayatullah Jakarta  
**Metodologi Utama:** Ward & Peppard Framework  

---

## RINGKASAN EKSEKUTIF

Dokumen Rencana Strategis ini menyajikan perencanaan strategis Sistem Informasi/Teknologi Informasi (SI/TI) untuk transformasi sistem *Single Sign-On* (SSO e-Semesta) di UIN Syarif Hidayatullah Jakarta menuju penerapan *Multi-Factor Authentication* (MFA) yang aman, patuh regulasi, efisien, dan ramah pengguna. 

Studi ini menggunakan metodologi **Ward & Peppard** yang didukung oleh analisis empiris komprehensif, mencakup 19 sumber bukti terdaftar (`S1` s/d `S19`), 12 bukti teknis tangkapan layar Keycloak Admin Console (`T-01` s/d `T-12`), 3 dokumen operasional resmi (`D-01` s/d `D-03`), dan 10 konfirmasi data pengguna (`U-01` s/d `U-10`).

### Temuan Kunci Kondisi Saat Ini (M2 & M5):
1. **SSO e-Semesta (Keycloak Realm SSOUIN)** melayani 45.219+ pengguna (42.088 mahasiswa, 1.593 dosen, 1.438 tendik) dan 44 client/aplikasi terintegrasi.
2. **Celah Keamanan Kritis**: Kebijakan Kata Sandi (*Password Policy*) **KOSONG** (`T-06`), kata sandi default terprediksi berbasis NIK/NIM (`U-06`, `U-07`), faktor kedua (MFA/TOTP) belum diwajibkan (`T-04`), dan *Verify Email* **DISABLED** (`T-04`).
3. **Beban Operasional High Helpdesk**: Layanan helpdesk SMILE menangani **2.624 tiket manual** terkait login/reset kata sandi (`D-02`).

### Solusi Strategis & Peta Jalan (M9, M10, M12):
1. **Tiga Pilar Strategi SI/TI**: Mengintegrasikan MFA pada 44 client (SI-1), meluncurkan *Self-Service Identity Recovery* (SI-2), melakukan *Keycloak Hardening* (TI-1), menerapkan **TOTP Massal Nirbiaya Lisensi** bagi 45rb sivitas akademika (TI-2), menerapkan **FIDO2/WebAuthn** untuk akun admin (TI-3), menghentikan total password NIK default (TI-4), dan menyusun SOP Tata Kelola SSO (MGT-1).
2. **Arsitektur Target (M10)**: Mentransformasi arsitektur faktor tunggal (*As-Is*) menjadi arsitektur berlapis (*To-Be*) dengan *Password Policy Enforcer*, *Required Action Pipeline*, dan retensi log audit 180 hari.
3. **Hasil Terukur (M13)**: Ditargetkan memotong tiket helpdesk SMILE >80% (menjadi <500 tiket/tahun), mencapai >85% adopsi TOTP massal, dan menjamin 100% kepatuhan UU Pelindungan Data Pribadi (UU PDP No. 27/2022).

---

## BAB I: PENDAHULUAN & METODOLOGI (M0 & M1)

### 1.1 Latar Belakang & Identitas Organisasi
UIN Syarif Hidayatullah Jakarta merupakan Perguruan Tinggi Keagamaan Islam Negeri (PTKIN) terkemuka di Indonesia yang menyelenggarakan layanan pendidikan tinggi bagi 45.219+ sivitas akademika. Untuk mendukung tata kelola digital, universitas mengoperasikan portal **SSO e-Semesta** berbasis platform **Keycloak Identity Provider** (realm `SSOUIN`).

### 1.2 Rumusan Masalah Utama
Meskipun SSO e-Semesta telah memfasilitasi akses terpusat ke 44 aplikasi institusi, sistem autentikasi saat ini masih **sepenuhnya bergantung pada kata sandi faktor tunggal (*single-factor password*)**, dengan kata sandi default terprediksi berbasis NIK/NIM dan tanpa penegakan kebijakan kata sandi (*Password Policy* kosong). Hal ini menciptakan risiko tinggi penyerobotan akun (*credential guessing & stuffing*), *phishing*, dan kecacatan kepatuhan hukum sesuai UU PDP No. 27 Tahun 2022.

### 1.3 Metodologi Perencanaan Strategis (Ward & Peppard Framework)
Perencanaan strategis ini mengeksekusi 14 milestone bertahap sesuai kerangka kerja Ward & Peppard:

```text
+-----------------------------------------------------------------------------------+
| ALUR METODOLOGI WARD & PEPPARD (MILESTONE 0 S/D MILESTONE 14)                     |
+-----------------------------------------------------------------------------------+
| [ M0: Scope ] -> [ M1: Org Context ] -> [ M2: Current State SSO ]                 |
|                                                  |                                |
|   +----------------------------------------------+                                |
|   v                                                                               |
| [ M3: Internal Business ] ----> [ M4: External Business ]                          |
| [ M5: Internal IS/IT    ] ----> [ M6: External IS/IT    ]                          |
|                                                  |                                |
|   +----------------------------------------------+                                |
|   v                                                                               |
| [ M7: SWOT & Issues ] -> [ M8: Gap Analysis ] -> [ M9: Strategy Formulation ]     |
|                                                  |                                |
|   +----------------------------------------------+                                |
|   v                                                                               |
| [ M10: Target Arch ]  -> [ M11: Portfolio ]   -> [ M12: Roadmap ]                 |
|                                                  |                                |
|   +----------------------------------------------+                                |
|   v                                                                               |
| [ M13: KPIs & Measurement ] ------------> [ M14: Final Strategic Plan (LOCKED) ]  |
+-----------------------------------------------------------------------------------+
```

---

## BAB II: KONDISI SAAT INI SSO / CURRENT STATE (M2)

### 2.1 Arsitektur SSO Eksisting
Platform SSO menggunakan **Keycloak** (realm `SSOUIN`). Lingkungan *development* berada pada `dev-sso.uinjkt.ac.id`, sedangkan lingkungan produksi berada pada `app-sso.uinjkt.ac.id`. 

Mekanisme federasi identitas menggunakan provider **User Migration Using A REST Client** (`T-02`):
* **Dosen & Tendik**: Dikelola oleh `eSDM` dengan status User Federation *enabled* dan menyinkronkan data secara *real-time* via client `esdm-sync-service` (`T-11`, `U-10`).
* **Mahasiswa**: Seluruh akun mahasiswa di SSO produksi telah dimigrasi penuh ke database lokal Keycloak (`U-09`), sehingga entry User Federation `eAkademik` berada dalam status *disabled* (`T-02`).

### 2.2 Inventaris Integrasi Aplikasi (44 Client Terdaftar)
Hasil penelusuran 3 halaman Keycloak Admin Console (`T-10`, `T-11`, `T-12`) mengonfirmasi **44 client terdaftar**:
1. **Layanan Utama**: `eAkademik`, `eRegistrasi`, `eSDM`, `eAkademik-portal`, `eAset`, `eBeasiswa`, `eFinansi`, `PLO`, `eKinerja` (produksi), `Wi-Fi SSO`.
2. **Aplikasi Baru**: `dev-lms`, `eadmisi`, `eAlumni`, `eKKN`, `ePembayaran`, `eSPMI`, `eRiset`, `mCampus`, `mhst`, `sso`, `uhelp sso admin/bridge`.
3. **Client SKI/Dev**: `eAsetPostgreSKI`, `eBeasiswaPostgreSKI`, `eRegistrasiSKI`, `eKKNPostgre`, `local-api`, `local-cms-uinjkt`, dll.

### 2.3 Kontrol Keamanan Baseline
* **Password Policy**: **KOSONG / TIDAK ADA ATURAN** (`T-06`).
* **Kredensial Default**: Mahasiswa = `Mhs`+NIK; Dosen/Tendik = NIK tanpa prefix (`U-06`, `U-07`).
* **Required Actions**: `Update Password` (Default & Enabled); `Configure OTP` (Enabled, bukan default); `Verify Email` (DISABLED); WebAuthn SPI belum di-register (`T-04`).
* **Logging**: Login Events & Admin Events **ON** (`T-03`, `T-08`), namun Expiration (retensi log) **KOSONG**.

---

## BAB III: ANALISIS LINGKUNGAN BISNIS INTERNAL & RANTAI NILAI (M3)

### 3.1 Pengaruh Autentikasi pada Proses Bisnis Utama
1. **Ranah Akademik**: Penerimaan mahasiswa (`eadmisi`, `eRegistrasi`), perkuliahan harian (`eAkademik`, `dev-lms`), tugas akhir & riset (`eRiset`, `eKKN`, `PLO`), dan kelulusan (`eAlumni`).
2. **Ranah Kepegawaian**: Manajemen SDM (`eSDM`) dan evaluasi kinerja (`eKinerja`).
3. **Ranah Keuangan & Akses Kampus**: Transaksi UKT (`eFinansi`, `ePembayaran`), BMN (`eAset`), dan konektivitas Wi-Fi kampus (`STAF.UINJKT.AC.ID` & `MHS.UINJKT.AC.ID`).

### 3.2 Rantai Nilai Bisnis (Business Value Chain)
Dalam *Value Chain* perguruan tinggi, SSO e-Semesta berfungsi sebagai **Enabler Akses** sekaligus **Value Safeguard** yang melindungi integritas nilai akademik, kerahasiaan data SDM/keuangan, dan reputasi UIN Jakarta.

---

## BAB IV: ANALISIS LINGKUNGAN BISNIS EKSTERNAL & PESTEL (M4)

### 4.1 Mandat Regulasi & Kepatuhan Hukum
* **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)**: Mengikat universitas sebagai Pengendali Data Pribadi untuk menjamin perlindungan data dari akses tidak sah. Kata sandi NIK default tanpa MFA menjadi risiko hukum berkonsekuensi sanksi.
* **Perpres No. 95 Tahun 2018 (SPBE) & Standar BSSN**: Kewajiban penerapan manajemen keamanan informasi terpadu dan autentikasi kuat (*strong authentication*).

### 4.2 Analisis PESTEL
* **Politik**: Kebijakan SPBE kementerian.
* **Ekonomi**: Efisiensi biaya operasional penanganan tiket manual SMILE.
* **Sosial**: Ekspektasi kemudahan pengguna generasi digital.
* **Teknologi**: Ketersediaan kapabilitas TOTP/WebAuthn bawaan Keycloak (nirbiaya lisensi).
* **Environmental**: Kampus ramah lingkungan via digitalisasi persuratan PLO.
* **Legal**: Sanksi hukum pelanggaran pelindungan data pribadi UU PDP.

---

## BAB V & VI: EVALUASI SI/TI INTERNAL & EKSTERNAL (M5 & M6)

### 5.1 Keunggulan & Celah Teknis Keycloak (M5)
* **Keunggulan**: Keycloak SSO berbasis Quarkus & Infinispan terbukti kokoh dan telah mendukung modul TOTP serta WebAuthn SPI secara bawaan (`T-01`).
* **Celah Teknis**: Celah konfigurasi dasar (Password Policy kosong, Verify Email mati, MFA non-default, retensi log kosong).

### 5.2 Evaluasi Rumpun Teknologi MFA (M6)
Evaluasi netral terhadap 5 rumpun teknologi MFA menyimpulkan:
1. **TOTP via Authenticator Apps (Google Authenticator / FreeOTP)**: **Pilihan Terbaik untuk Massal** (~45rb pengguna) karena didukung *native* Keycloak, bebas biaya lisensi/kirim pesan, dan bekerja *offline*.
2. **FIDO2 / WebAuthn Passkeys**: **Pilihan Terbaik untuk Akun Privileged / Admin** karena memberikan ketahanan maksimal terhadap serangan *phishing* & MitM.
3. **SMS / WhatsApp OTP**: **TIDAK DIREKOMENDASIKAN** karena potensi pembengkakan biaya operasional pesan berulang yang tidak berkelanjutan bagi anggaran universitas.

---

## BAB VII: MATRIKS SWOT & ISU-ISU STRATEGIS (M7)

### 7.1 Matriks Strategi TOWS
* **SO Strategy**: Mengaktifkan TOTP & WebAuthn bawaan Keycloak pada 44 client tanpa biaya lisensi untuk memenuhi kepatuhan UU PDP & SPBE.
* **WO Strategy**: Mengonfigurasi Password Policy & Verify Email untuk memenuhi standar BSSN sekaligus memotong tiket helpdesk SMILE.
* **ST Strategy**: Mewajibkan TOTP bagi seluruh pengguna untuk melumpuhkan ancaman *phishing* dan *credential stuffing*.
* **WT Strategy**: Menghentikan password default NIK/NIM dan menerapkan MFA khusus (FIDO2/WebAuthn) pada akun admin.

### 7.2 Isu-Isu Strategis Terprioritas
1. **IS-1 (P1 - Paling Kritis)**: Penanganan Kerentanan Kata Sandi Faktor Tunggal & Password Default NIK/NIM.
2. **IS-2 (P2 - Kritis)**: Penerapan Multi-Factor Authentication (MFA) Bertahap Berbasis Risiko.
3. **IS-3 (P3 - Tinggi)**: Peningkatan Pemulihan Akun Mandiri (*Self-Service Recovery*) untuk Mengurangi Beban Helpdesk SMILE.
4. **IS-4 (P4 - Sedang–Tinggi)**: Penguatan Tata Kelola, Retensi Log Audit (180 Hari), dan SOP Keamanan SSO.

---

## BAB VIII: ANALISIS KESENJANGAN / GAP ANALYSIS (M8)

| Dimensi Gap | Kondisi Saat Ini (As-Is) | Kondisi Target (To-Be) | Tindakan Penutupan Gap (*Closure Action*) |
|---|---|---|---|
| **Teknologi** | MFA `Configure OTP` non-default (`T-04`). | MFA diwajibkan (TOTP massal, WebAuthn admin). | Set OTP sebagai *Default Required Action* & register WebAuthn SPI. |
| **Kebijakan** | Password Policy KOSONG (`T-06`); Verify Email DISABLED. | Password Policy ketat & Verify Email ENABLED. | Konfigurasi Password Policy Enforcer & aktifkan Verify Email di Keycloak. |
| **Proses** | Password default NIK (`U-06`); 2.624 tiket SMILE (`D-02`). | Password NIK terhapus; alur ganti password login 1 & *self-service recovery*. | Wajibkan *Update Password* login 1 & otomatiskan reset mandiri via email. |
| **Tata Kelola** | Belum ada dokumen SOP resmi SSO. | SOP resmi operasional, *role matrix*, & insiden SSO. | Menyusun dan mengesahkan dokumen SOP Keamanan & Operasional SSO. |
| **SDM** | Beban helpdesk tersedot tiket manual. | Helpdesk fokus eskalasi khusus; user paham TOTP. | Kampanye edukasi pendaftaran TOTP & pelatihan SOP helpdesk SMILE. |
| **Audit Log** | Event Expiration KOSONG (`T-08`). | Retensi log audit 180 hari (*auto-purge*). | Konfigurasi *Event Expiration Policy* 180 hari di Keycloak Admin Console. |
| **Risiko** | Autentikasi 1-faktor rentan pembobolan. | Autentikasi 2-faktor yang *compliant* UU PDP. | Integrasi Step-Up MFA pada seluruh 44 client aplikasi institusi. |

---

## BAB IX: FORMULASI TIGA PILAR STRATEGI SI/TI (M9)

### 9.1 Pilar 1: Strategi Sistem Informasi (IS Strategy)
* **SI-1**: Integrasi Layanan Autentikasi Berlapis (MFA Step-Up) pada 44 Client Aplikasi Terdaftar.
* **SI-2**: Peluncuran Sistem Pemulihan Identitas Mandiri (*Self-Service Recovery System*) via Email Terverifikasi.
* **SI-3**: Penguatan Integrasi Otomatis Siklus Hidup Identitas (eRegistrasi -> eAkademik -> Keycloak & eSDM Sync).

### 9.2 Pilar 2: Strategi Teknologi Informasi (IT Strategy)
* **TI-1**: Pengerasan Keamanan Keycloak (*Hardening*: Enforce Password Policy, Verify Email, Event Expiration 180 Hari).
* **TI-2**: Penerapan MFA Rumpun TOTP via Authenticator Apps untuk Massal (~45.000 Sivitas Akademika).
* **TI-3**: Penerapan MFA FIDO2 / WebAuthn Passkeys untuk Akun Administrative / Privileged.
* **TI-4**: Penghentian Total Kata Sandi Default berbasis NIK/NIM via *Update Password Required Action* Login Pertama.

### 9.3 Pilar 3: Strategi Manajemen SI/TI (IS/IT Management Strategy)
* **MGT-1**: Penyusunan dan Pengesahan Dokumentasi SOP Resmi Operasional & Keamanan SSO.
* **MGT-2**: Efisiensi Layanan Helpdesk SMILE melalui Edukasi & Panduan Visual Pendaftaran TOTP Mandiri.
* **MGT-3**: Kepatuhan Regulasi UU PDP No. 27/2022 & Audit Log Keamanan Berkala.

---

## BAB X: ARSITEKTUR KONSEPTUAL TARGET (M10)

### 10.1 Pembandingan Arsitektur As-Is vs To-Be

```text
[ ARSITEKTUR EKSISTING / AS-IS ]
User -> Browser/Wi-Fi -> Keycloak SSO (Password Policy KOSONG, MFA Disabled, Verify Email Off) -> 44 Client (Rentan Phishing)

[ ARSITEKTUR TARGET / TO-BE IMPROVED ]
User -> WAF/Reverse Proxy -> Keycloak Cluster (Enforced Password Policy, Required Action Pipeline, TOTP/WebAuthn Engine, Auto-Purge Log 180 Hari) -> 44 Client (Terproteksi MFA Step-Up)
```

### 10.2 Tiga Alur Autentikasi Target
1. **Alur Pendaftaran Pertama**: Login Kredensial Awal -> Wajib Buat Password Baru Berstandar Tinggi -> Verifikasi Email Kampus -> Scan QR Code TOTP -> Akun Terproteksi MFA -> Masuk Aplikasi.
2. **Alur Login Rutin Terproteksi MFA**: Input Username & Password -> Validasi -> Layar Masukkan Kode OTP 6-Digit -> Input TOTP -> Token OIDC/SAML Issued -> Masuk Aplikasi.
3. **Alur Pemulihan Mandiri**: Klik *Forgot Password* -> Input Email Kampus Terverifikasi -> Terima Tautan Reset -> Buat Password Baru -> Konfirmasi OTP -> Selesai Mandiri (Bebas Tiket SMILE).

---

## BAB XI: PORTOFOLIO STRATEGIS MCFARLAN STRATEGIC GRID (M11)

```text
+-----------------------------------------------------------------------------------+
| MCFARLAN STRATEGIC GRID PORTOFOLIO SI/TI UIN JAKARTA                              |
+-----------------------------------------------------------------------------------+
| STRATEGIC (STRATEGIS)               | HIGH POTENTIAL (POTENSIAL TINGGI)           |
| - Keycloak SSO Core Engine (SSOUIN) | - Biometric Authenticator / FIDO2 Passkeys  |
| - MFA Engine (TOTP & WebAuthn SPI)  | - Mobile Campus Apps (mCampus, mhst)        |
| - Self-Service Recovery & Policy    | - Learning Management System (dev-lms)      |
| - Portal SSO e-Semesta (sso)        | - Integration Bridge (uhelp sso bridge)     |
+-------------------------------------+---------------------------------------------+
| KEY OPERATIONAL (KUNCI OPERASIONAL) | SUPPORT (PENDUKUNG)                         |
| - Layanan Akademik (eAkademik,      | - Tata Usaha & Riset (PLO, eRiset, eKKN)    |
|   eRegistrasi, eAkademik-portal)    | - BMN & Beasiswa (eAset, eBeasiswa)         |
| - Layanan SDM (eSDM, esdm-sync,     | - Layanan Alumni (eAlumni)                  |
|   eKinerja)                         | - Backend SKI/Postgre Dev Clients           |
| - Layanan Keuangan (eFinansi,       | - Helpdesk Admin (uhelp sso admin)          |
|   ePembayaran, eadmisi)             |                                             |
| - Akses Wi-Fi SSO (MHS & STAF)      |                                             |
+-----------------------------------------------------------------------------------+
```

---

## BAB XII: PETA JALAN IMPLEMENTASI & MANAJEMEN RISIKO (M12)

### 12.1 Pentahapan Peta Jalan 12-Bulan (Q1 s/d Q4)
* **Fase 1: Quick Wins & Fondasi Keamanan (Q1 / Bulan 1–3)**: Keycloak Hardening (TI-1), Penghentian Password NIK Default (TI-4), Pengesahan Dokumen SOP SSO (MGT-1).
* **Fase 2: MFA Massal & Pemulihan Mandiri (Q2–Q3 / Bulan 4–9)**: Integrasi MFA 44 Client (SI-1), Rollout TOTP Massal (TI-2), Peluncuran Self-Service Recovery (SI-2), Kampanye Edukasi User & Helpdesk SMILE (MGT-2), Auto-Sync Lifecycle (SI-3).
* **Fase 3: Privileged Protection & Audit Kepatuhan (Q4 / Bulan 10–12)**: Implementasi WebAuthn/FIDO2 Admin (TI-3), Audit Kepatuhan UU PDP & Retensi Log 180 Hari (MGT-3).

### 12.2 Manajemen Risiko & Rencana Mitigasi
1. **Risiko Kebingungan User saat Pendaftaran TOTP**: Mitigasi via panduan visual, video tutorial, dan **masa transisi pendaftaran mandiri 30 hari** sebelum MFA diwajibkan secara penuh.
2. **Risiko Lonjakan Tiket SMILE pada Go-Live**: Mitigasi via fitur *backup codes* dan pembentukan *task force* helpdesk PUSTIPANDA selama 2 minggu *Go-Live*.
3. **Risiko Perangkat Hilang**: Mitigasi via alur pemulihan mandiri berbasis email kampus terverifikasi.

---

## BAB XIII: INDIKATOR KINERJA UTAMA / KPI STRATEGIS (M13)

| Kode KPI | Indikator Kinerja Utama | Baseline M2 | Target M13 | Frekuensi Ukur |
|---|---|---|---|---|
| **KPI-1** | Adopsi TOTP Massal (Mahasiswa, Dosen, Tendik) | 0% (Non-Default) | **>85% (Q3) / 100% (Q4)** | Bulanan |
| **KPI-2** | Adopsi WebAuthn/FIDO2 Akun Admin | 0% (Faktor Tunggal) | **100% (Q1 Admin, Q4 All Privileged)** | Bulanan |
| **KPI-3** | Cakupan 44 Client Terproteksi MFA | 0% (Faktor Tunggal) | **100% (44 Client di Q3)** | Triwulanan |
| **KPI-4** | Penegakan Kebijakan Password Policy | Kosong (`T-06`) | **100% Enforced di Keycloak (Q1)** | Real-time |
| **KPI-5** | Eliminasi Kata Sandi Default NIK/NIM | 0% Terhapus | **100% Password NIK Terhapus (Q1)** | Bulanan |
| **KPI-6** | Insiden Pembobolan Akun (*Account Takeover*) | Berisiko Tinggi | **0 Kasus Insiden (Q2–Q4)** | Bulanan |
| **KPI-7** | Penurunan Volume Tiket Helpdesk SMILE | 2.624 Tiket (`D-02`) | **Penurunan >80% (<500 tiket/tahun)** | Bulanan |
| **KPI-8** | Waktu Pemulihan Akun Mandiri (MTTR) | Jam s/d Hari | **< 3 Menit (Via Email Terverifikasi)** | Real-time |
| **KPI-9** | Ketersediaan Layanan Keycloak SSO (*Uptime*) | `[EVIDENCE NEEDED]` | **>= 99,9% Uptime** | Bulanan |
| **KPI-10** | Kepatuhan Retensi Log Audit 180 Hari | Expiration Kosong (`T-08`) | **100% Compliant (Auto-Purge 180 Hari)** | Bulanan |
| **KPI-11** | Pengesahan Dokumen SOP Resmi SSO | 0% (Belum ada SOP) | **100% SOP Disahkan Pimpinan (Q1)** | Sekali |
| **KPI-12** | Kepatuhan Regulasi UU PDP No. 27/2022 | Non-Compliant | **100% Compliant (Lulus Audit PDP)** | Tahunan |

---

## BAB XIV: KESIMPULAN & REKOMENDASI PENUTUP

Perencanaan Strategis Sistem Informasi integrasi Multi-Factor Authentication (MFA) pada Single Sign-On (SSO) UIN Syarif Hidayatullah Jakarta menghasilkan rekomendasi strategis yang **defensibel, rasional, dan efisien**:
1. **Tidak Memerlukan Pembangunan Ulang Infrastruktur (*No Greenfield Rebuild*)**: Mengoptimalkan kapabilitas *native* platform Keycloak SSO yang sudah ada.
2. **Bebas Biaya Lisensi Berulang (*Cost-Effective*)**: Memilih teknologi TOTP berbasis Authenticator Apps yang bebas biaya per-pesan (menghindari pembengkakan biaya SMS/WA OTP).
3. **Menutup Celah Keamanan Paling Kritis**: Menghapuskan kata sandi default NIK, menegakkan Password Policy ketat, dan mengaktifkan verifikasi email mandiri.
4. **Memotong Beban Operasional Helpdesk**: Mengurangi >80% tiket manual SMILE melalui fitur *Self-Service Identity Recovery*.

---

## LAMPIRAN: REGISTER BUKTI TERDAFTAR (SOURCE REGISTER S1 S/D S19)

* **S1**: Ward & Peppard Example Paper (JSON, 2021).
* **S2**: Dokumentasi Tugas 2 Perencanaan Stratejik.
* **S3**: Surat Pemberitahuan Implementasi Wi-Fi SSO (B-42/UPT.2/TI.05.04/04/2026).
* **S4 / D-02**: Ekspor Tiket Kata Sandi & Masalah Login SMILE (2.624 tiket, 20260921).
* **S5 / D-03**: Panduan Penggunaan Jaringan Internet Kampus Wi-Fi SSO UIN Jakarta.
* **S6 / T-01**: Ekstrak Teks Keycloak Server Info Providers (`dev-sso.uinjkt.ac.id`).
* **S7 / T-02**: Screenshot Keycloak Admin Console: User Federation (REST Migration API).
* **S8 / T-03**: Screenshot Keycloak Admin Console: Login Events.
* **S9 / T-04**: Screenshot Keycloak Admin Console: Required Actions.
* **S10 / T-05**: Screenshot Keycloak Admin Console: Clients Halaman 1 (terpotong).
* **S11 / T-06**: Konfirmasi Password Policy Kosong.
* **S12 / T-07**: Screenshot Keycloak Admin Console: OTP Policy (Default TOTP SHA1 6-digit).
* **S13 / T-08**: Screenshot Keycloak Admin Console: Events Config (Expiration kosong).
* **S14 / T-09**: Screenshot Keycloak Admin Console: Client Scopes (10 OIDC, 1 SAML).
* **S15 / T-11**: Screenshot Keycloak Admin Console: Clients Halaman 2 (eSDM, esdm-sync-service, SAML staff).
* **S16 / T-12**: Screenshot Keycloak Admin Console: Clients Halaman 3 (44 Client total).
* **S17 / U-06**: Pola Password Default Mahasiswa (`Mhs`+NIK).
* **S18 / U-09**: Konfirmasi Migrasi Penuh Mahasiswa di Produksi & Penonaktifan Otomatis 3 Bulan pasca LULUS.
* **S19 / U-10**: Konfirmasi Sinkronisasi Real-Time eSDM via `esdm-sync-service` & Penonaktifan Seketika Mahasiswa Nonaktif/DO.
