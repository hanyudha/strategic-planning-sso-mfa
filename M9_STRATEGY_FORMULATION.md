# M9 — Formulasi Strategi SI/TI (Strategy Formulation)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan formulasi 3 pilar strategi SI/TI Ward & Peppard: Strategi SI (SI-1 s/d SI-3), Strategi TI (TI-1 s/d TI-4), Strategi Manajemen SI/TI (MGT-1 s/d MGT-3), dan Matriks Keterlacakan Strategis. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan utama untuk Arsitektur Target (M10) dan Peta Jalan (M12).

---

## 1. Tujuan Formulasi Strategi M9

1. Menentukan portal layanan dan aplikasi sistem informasi (*IS Strategy*) yang diperlukan untuk menjawab kebutuhan bisnis institusi.
2. Menetapkan arsitektur teknologi, konfigurasi keamanan, dan pemilihan instrumen MFA (*IT Strategy*) yang efisien dan berkelanjutan.
3. Merumuskan struktur tata kelola, manajemen SDM, prosedur operasional (SOP), dan kepatuhan hukum (*IS/IT Management Strategy*).
4. Menjamin keterlacakan strategis (*strategic traceability*) dari bukti fisik (M1/M2) -> temuan (M3-M6) -> isu strategis (M7) -> gap (M8) -> formulasi strategi (M9).

---

## 2. Arsitektur Tiga Pilar Strategi SI/TI (Ward & Peppard)

```text
+-----------------------------------------------------------------------------------+
| TRIPLE-PILLAR STRATEGY FORMULATION (WARD & PEPPARD FRAMEWORK)                     |
+-----------------------------------------------------------------------------------+
| 1. STRATEGI SISTEM INFORMASI (IS STRATEGY)                                        |
|    - Berfokus pada: Aplikasi & Layanan Bisnis yang Dibutuhkan Institusi.         |
|    - Inisiatif utama: MFA pada 44 Client, Self-Service Recovery, Lifecycle Auto.  |
+-----------------------------------------------------------------------------------+
| 2. STRATEGI TEKNOLOGI INFORMASI (IT STRATEGY)                                     |
|    - Berfokus pada: Infrastruktur, Arsitektur Keycloak, Konfigurasi & Pilihan MFA.|
|    - Inisiatif utama: Keycloak Hardening (Policy), TOTP Massal, FIDO2/Admin.      |
+-----------------------------------------------------------------------------------+
| 3. STRATEGI MANAJEMEN SI/TI (IS/IT MANAGEMENT STRATEGY)                           |
|    - Berfokus pada: Tata Kelola, Dokumen SOP, SDM Helpdesk, Kepatuhan UU PDP.     |
|    - Inisiatif utama: Formulasi SOP SSO, Edukasi User, Audit Log & Retensi.       |
+-----------------------------------------------------------------------------------+
```

---

## 3. Pilar 1: Strategi Sistem Informasi (IS Strategy)

Strategi SI berfokus pada **apa yang perlu diberikan oleh sistem informasi** untuk mendukung proses akademik dan administratif UIN Jakarta secara aman:

| Kode Inisiatif | Nama Inisiatif SI | Deskripsi Strategis | Cakupan Aplikasi / Sistem |
|---|---|---|---|
| **SI-1** | **Penerapan Layanan Autentikasi Berlapis (MFA Integration)** | Mengintegrasikan perlindungan faktor kedua pada seluruh aplikasi terintegrasi SSO e-Semesta secara bertahap berbasis risiko. | 44 Client di Keycloak (eAkademik, eRegistrasi, eSDM, eFinansi, PLO, LMS, Wi-Fi, dll.) |
| **SI-2** | **Otomatisasi Pemulihan Identitas Mandiri (*Self-Service Recovery System*)** | Menyediakan alur ubah kata sandi dan pemulihan kata sandi mandiri yang aman via email terverifikasi untuk mengurangi ketergantungan pada helpdesk. | Portal SSO e-Semesta (`dev-sso.uinjkt.ac.id` / `app-sso.uinjkt.ac.id`) & SMILE Tiketing |
| **SI-3** | **Penguatan Integrasi Siklus Hidup Identitas Otomatis** | Mengunci alur otomatisasi akun: eRegistrasi -> eAkademik -> Keycloak untuk mahasiswa baru; serta penonaktifan otomatis 3 bulan pasca LULUS / seketika saat nonaktif/DO dan sync eSDM real-time. | eRegistrasi, eAkademik, eSDM, `esdm-sync-service`, Keycloak Realm SSOUIN |

---

## 4. Pilar 2: Strategi Teknologi Informasi (IT Strategy)

Strategi TI berfokus pada **bagaimana teknologi dispesifikasikan dan dikonfigurasi** untuk merealisasikan Strategi SI secara efisien:

| Kode Inisiatif | Nama Inisiatif TI | Spesifikasi Teknis & Konfigurasi | Keterangan & Rationale |
|---|---|---|---|
| **TI-1** | **Pengerasan Keamanan Keycloak (*Keycloak Hardening & Policy Enforcement*)** | (1) Mengaktifkan *Password Policy*: Min 8-12 karakter, kombinasi huruf/angka/simbol, *lockout* 5x gagal; (2) Mengaktifkan *Verify Email*; (3) Mengonfigurasi *Event Expiration* 180 hari. | Menutup celah T-04, T-06, T-08 tanpa biaya tambahan. |
| **TI-2** | **Penerapan MFA Rumpun TOTP untuk Penggunaan Massal (*Mass TOTP Rollout*)** | Menggunakan standar TOTP (RFC 6238) via aplikasi Authenticator (Google Authenticator / FreeOTP) sebagai faktor kedua standar bagi ~45.000 mahasiswa, dosen, dan tendik. | Didukung *native* oleh Keycloak (T-01, T-07); **bebas biaya lisensi/pesan berulang**. |
| **TI-3** | **Penerapan MFA FIDO2/WebAuthn untuk Akun Administrative (*Privileged MFA*)** | Mendaftarkan Required Action WebAuthn di Keycloak untuk akun berakses administratif tinggi (admin eSDM, eFinansi, PLO, data center). | Memberikan ketahanan maksimal dari serangan *phishing* & MitM pada akun berisiko tinggi. |
| **TI-4** | **Penghentian Total Kata Sandi Default berbasis NIK/NIM** | Mewajibkan *Update Password Required Action* saat login pertama untuk seluruh pengguna baru dan memaksa penggantian bagi akun aktif bersandi default. | Menghilangkan risiko *credential guessing* (U-06, U-07). |

---

## 5. Pilar 3: Strategi Manajemen SI/TI (IS/IT Management Strategy)

Strategi Manajemen SI/TI berfokus pada **bagaimana sumber daya, tata kelola, dan SDM dikelola** agar investasi SI/TI berkelanjutan:

| Kode Inisiatif | Nama Inisiatif Manajemen | Rencana Aksi Operasional & Tata Kelola | Dampak yang Diharapkan |
|---|---|---|---|
| **MGT-1** | **Penyusunan Dokumentasi SOP Resmi Operasional & Keamanan SSO** | Menyusun dan mengesahkan Dokumen SOP Tata Kelola SSO, SOP Registrasi Client Baru, SOP Manajemen Hak Akses Admin, dan SOP Penanganan Insiden Keamanan. | Kepastian hukum internal, standarisasi operasional, dan eliminasi ketergantungan personal. |
| **MGT-2** | **Efisiensi Layanan Helpdesk SMILE & Program Sosialisasi Pengguna** | Meluncurkan panduan visual/video pendaftaran TOTP mandiri bagi mahasiswa/dosen dan pelatihan SOP eskalasi tiket bagi tim PUSTIPANDA. | Mengurangi beban 2.624 tiket manual di SMILE (D-02) secara signifikan. |
| **MGT-3** | **Kepatuhan Regulasi UU PDP & Audit Keamanan Berkala** | Melakukan peninjauan berkala terhadap log audit (*Login & Admin Events*) dan memastikan pemrosesan data pribadi di SSO sesuai ketentuan UU No. 27 Tahun 2022. | Menghindarkan institusi dari sanksi hukum dan menjaga reputasi publik UIN Jakarta. |

---

## 6. Matriks Keterlacakan Strategis (Strategic Traceability Matrix)

| Masalah / Celah Baseline (M2/M8) | Isu Strategis (M7) | Pilar & Kode Inisiatif Strategi (M9) |
|---|---|---|
| Password Policy KOSONG (T-06) & Password default NIK (U-06, U-07) | **IS-1**: Kerentanan Kata Sandi Faktor Tunggal & Password Default | **TI-1** (Keycloak Hardening), **TI-4** (Penghentian Password NIK) |
| MFA belum diwajibkan (T-04, T-07) & 44 aplikasi rentan phishing | **IS-2**: Penerapan MFA Bertahap berbasis Risiko | **SI-1** (MFA 44 Client), **TI-2** (Mass TOTP), **TI-3** (Privileged WebAuthn) |
| 2.624 Tiket SMILE (D-02) & Verify Email DISABLED (T-04) | **IS-3**: Tingginya Beban Helpdesk & Ketiadaan Self-Service | **SI-2** (Self-Service Recovery), **MGT-2** (Efisiensi Helpdesk SMILE) |
| Ketiadaan SOP formal & Retensi Log Expiration KOSONG (T-08) | **IS-4**: Penguatan Tata Kelola, Retensi Log Audit, & SOP | **TI-1** (Event Expiration), **MGT-1** (Dokumentasi SOP), **MGT-3** (UU PDP & Audit) |

---

## 7. Kesimpulan M9

Formulasi strategi M9 berhasil menyusun roadmap intervensi holistik yang mencakup aspek **Aplikasi (SI)**, **Teknologi & Keamanan (TI)**, serta **Tata Kelola & SDM (Manajemen)**. Ketiga pilar ini saling menguatkan untuk mengubah SSO e-Semesta dari sistem faktor tunggal yang rentan menjadi benteng autentikasi terpusat yang aman, patuh regulasi, dan ramah pengguna.

---

## 8. Langkah Selanjutnya

Setelah M9 dikunci, tahap berikutnya adalah **Milestone 10 (M10: Target Architecture)** untuk menggambarkan arsitektur konseptual target SSO + MFA secara rinci.
