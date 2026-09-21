# M10 — Arsitektur Target (Target Architecture)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan Arsitektur Konseptual Target (*To-Be*), Arsitektur & Alur Autentikasi Eksisting (*As-Is*), Matriks Perbandingan Penegasan Improvisasi, serta 3 Alur Autentikasi Target (Enrollment Pertama, Login Rutin MFA, Pemulihan Mandiri). Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan arsitektur teknis untuk Portofolio Strategis (M11) dan Peta Jalan (M12).

---

## 1. Tujuan Arsitektur Target M10

1. Memvisualisasikan arsitektur konseptual eksisting dan alur autentikasi eksisting untuk merekam kelemahan baseline.
2. Menggambarkan cetak biru konseptual (*conceptual blueprint*) target platform Keycloak SSO yang diperkuat dengan modul MFA dan pengerasan keamanan (*security hardening*).
3. Menjelaskan secara tegas bagian-bagian sistem yang diimprovisasi (*improvements & enhancements*).
4. Memetakan alur autentikasi baru (*target authentication flows*) untuk pendaftaran pertama kali, login rutin terproteksi MFA, dan pemulihan kata sandi mandiri (*self-service recovery*).

---

## BAGIAN A: KONDISI EKSISTING (AS-IS BASELINE)

### 2. Diagram Arsitektur Konseptual Eksisting

```text
+-----------------------------------------------------------------------------------+
| ARSITEKTUR KONSEPTUAL EKSISTING SSO (AS-IS) — REALM SSOUIN                        |
+-----------------------------------------------------------------------------------+
| PENGGUNA (Mahasiswa, Dosen, Tendik) -> Akses Browser / Wi-Fi Kampus               |
+-----------------------------------------------------------------------------------+
                                         | (HTTPS Faktor Tunggal)
                                         v
+-----------------------------------------------------------------------------------+
| PLATFORM SSO: KEYCLOAK (DEV: dev-sso.uinjkt.ac.id / PROD: app-sso.uinjkt.ac.id)   |
|                                                                                   |
| [ KONTROL KEAMANAN EKSISTING ]                                                    |
| - Password Policy: KOSONG / TIDAK ADA ATURAN (T-06)                               |
| - Required Actions: Update Password (Default), Verify Email (DISABLED, T-04)      |
| - MFA Status: Configure OTP Enabled tetapi BUKAN Default Action (T-04)            |
| - Log Retention: Login & Admin Events ON, Expiration KOSONG (T-08)                |
+-----------------------------------------------------------------------------------+
      | (REST Migration API)                             | (Direct Database/Local)
      v                                                  v
+-----------------------------------+   +-------------------------------------------+
| SUMBER IDENTITAS DOSEN & TENDIK   |   | SUMBER IDENTITAS MAHASISWA                |
| eSDM (Enabled User Federation /   |   | eAkademik (Migrasi Penuh Mahasiswa di     |
| REST Migration API - T-02)        |   | Produksi, User Federation Disabled)       |
+-----------------------------------+   +-------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| APLIKASI TERINTEGRASI EKSISTING (44 CLIENTS - OIDC & SAML)                        |
| - 44 Client di Keycloak (OIDC didominasi, 1 SAML Staff, Client SKI/Postgre Dev)   |
| - Wi-Fi Kampus SSO (MHS & STAF via RADIUS/Captive Portal)                         |
+-----------------------------------------------------------------------------------+
```

### 3. Alur Autentikasi Eksisting

```text
[ 3.1 ALUR LOGIN ROUTINE EKSISTING ]
Pengguna -> Input Username (NIM/Nama) + Password (NIK/Mhs+NIK) -> SSO Validasi Kata Sandi -> Langsung Masuk Aplikasi (Faktor Tunggal)

[ 3.2 ALUR LUPA PASSWORD EKSISTING ]
Pengguna Lupa Password -> Verify Email Mati -> Mengajukan Tiket Manual ke SMILE -> Petugas PUSTIPANDA Reset Manual (2.624 Tiket, D-02)
```

#### Kelemahan Alur Eksisting:
1. **Satu Faktor Kata Sandi (Single-Factor)**: Pertahanan sepenuhnya bergantung pada kerahasiaan kata sandi tanpa ada verifikasi kedua (MFA).
2. **Kata Sandi Default Terprediksi**: Mahasiswa baru menggunakan `Mhs`+NIK, sedangkan dosen/tendik menggunakan NIK tanpa prefix (U-06, U-07).
3. **Tanpa Pembatas Kualitas Kata Sandi**: Tidak ada aturan panjang minimal atau kompleksitas (*Password Policy* kosong, T-06).
4. **Beban Manual Helpdesk**: Tidak adanya verifikasi email aktif menyebabkan pemulihan kata sandi harus diproses manual melalui helpdesk SMILE (D-02).

---

## BAGIAN B: KONDISI TARGET & IMPROVISASI (TO-BE TARGET)

### 4. Diagram Arsitektur Konseptual Target

```text
+-----------------------------------------------------------------------------------+
| ARSITEKTUR KONSEPTUAL TARGET SSO + MFA (TO-BE IMPROVED)                           |
+-----------------------------------------------------------------------------------+
| PENGGUNA (Mahasiswa, Dosen, Tendik, Admin) -> BYOD / Desktop / Smartphone        |
+-----------------------------------------------------------------------------------+
                                         | (HTTPS / TLS 1.3 Terenkripsi)
                                         v
+-----------------------------------------------------------------------------------+
| LAPISAN PERIMETER & PERLINDUNGAN (WAF & Reverse Proxy / Load Balancer)            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PLATFORM CORE SSO: KEYCLOAK CLUSTER (REALM: SSOUIN)                               |
|                                                                                   |
| [ AUTHENTICATION & POLICY ENGINE (IMPROVED) ]                                     |
| - Password Policy Enforcer (Min 8-12 char, kompleksitas, Lockout 5x gagal) [NEW]  |
| - Required Actions Pipeline: Update Password -> Verify Email -> Configure TOTP    |
|                                                                                   |
| [ MULTI-FACTOR AUTHENTICATION (MFA) ENGINE (IMPROVED) ]                           |
| - Mass MFA: TOTP Provider (RFC 6238 / Authenticator Apps - Google/FreeOTP) [NEW]   |
| - Privileged MFA: FIDO2 / WebAuthn SPI (Passkeys / Biometrik / Hardware Key)[NEW] |
|                                                                                   |
| [ LOGGING & AUDIT ENGINE (IMPROVED) ]                                             |
| - Login & Admin Events Listener (jboss-logging / JPA Store)                       |
| - Event Expiration Policy: Auto-purge 180 Hari [NEW]                              |
+-----------------------------------------------------------------------------------+
      | (REST Migration API)                             | (Direct JPA / Local)
      v                                                  v
+-----------------------------------+   +-------------------------------------------+
| SUMBER IDENTITAS DOSEN & TENDIK   |   | SUMBER IDENTITAS MAHASISWA                |
| eSDM (Sync Real-Time via          |   | eAkademik (Migrasi Penuh Mahasiswa di     |
| `esdm-sync-service`)              |   | Produksi + Auto-Creation via eRegistrasi) |
+-----------------------------------+   +-------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LAPISAN INTEGRASI APLIKASI (44 CLIENTS - OPENID CONNECT & SAML 2.0)               |
| - Layanan Akademik : eAkademik, eRegistrasi, eRiset, eKKN, PLO, LMS, eAlumni, dll |
| - Layanan Keuangan : eFinansi, ePembayaran, eAset, eBeasiswa                      |
| - Layanan SDM      : eSDM, eKinerja                                               |
| - Jaringan Kampus  : Wi-Fi SSO (STAF & MHS) Terproteksi MFA                       |
+-----------------------------------------------------------------------------------+
```

---

## 5. Matriks Perbandingan & Penegasan Improvisasi (As-Is vs To-Be)

| Komponen / Alur | Kondisi Eksisting (As-Is Baseline) | Kondisi Target (To-Be Improved) | Penegasan Improvisasi & Nilai Tambah |
|---|---|---|---|
| **Faktor Autentikasi** | **Faktor Tunggal (Password Saja)**. OTP tersedia tetapi tidak diwajibkan (T-04). | **Multi-Factor Authentication (MFA)**. TOTP diwajibkan untuk massal; WebAuthn untuk admin. | Menghilangkan risiko pembobolan akun akibat *phishing* & *credential stuffing*. |
| **Kebijakan Kata Sandi (Password Policy)** | **KOSONG / TIDAK ADA ATURAN** (T-06). Pengguna bebas memakai kata sandi lemah. | **ENFORCED KETAT**. Min 8-12 karakter, kombinasi simbol/angka, dan *lockout* 5x gagal. | Menutup celah keamanan paling kritis pada Keycloak SSO. |
| **Kata Sandi Default** | **Terprediksi Berbasis NIK/NIM** (`Mhs`+NIK / NIK saja) (U-06, U-07). | **DIHENTIKAN TOTAL**. Wajib ganti kata sandi berstandar tinggi saat login pertama. | Menghilangkan potensi eksploitasi massal pada akun pengguna baru. |
| **Verifikasi Email** | **DISABLED** (T-04). Email pengguna tidak diverifikasi oleh Keycloak. | **ENABLED & MANDATORY**. Email kampus diverifikasi saat pendaftaran pertama. | Menjamin keabsahan kepemilikan email sebagai saluran pemulihan mandiri. |
| **Pemulihan Kata Sandi (Password Recovery)** | **Manual via Helpdesk SMILE** (2.624 tiket manual, D-02). | **Otomatis Mandiri (*Self-Service Recovery*)** via tautan email terverifikasi & konfirmasi OTP. | Memotong beban operasional tiket helpdesk SMILE hingga >80%. |
| **Retensi Log Audit** | **Expiration KOSONG** (T-08). Log menumpuk di database tanpa batas retensi. | **AUTO-PURGE 180 HARI**. Kebijakan retensi otomatis diatur di Keycloak. | Mencegah pembengkakan penyimpanan database dan menjaga kinerja SSO. |
| **Proteksi Akun Privileged (Admin)** | **Sama dengan Pengguna Biasa** (hanya kata sandi faktor tunggal). | **Pelindungan Khusus (FIDO2 / WebAuthn / Passkeys)** resisten *phishing*. | Melindungi aplikasi berdampak tinggi (eSDM, eFinansi, PLO) dari manipulasi data. |

---

## 6. Alur Autentikasi Target (Target Authentication Flows)

### 6.1 Alur Pendaftaran Pertama Kali (*First-Time User Enrollment Flow*)
1. Mahasiswa baru / Pegawai baru melakukan login pertama ke SSO e-Semesta menggunakan kredensial awal.
2. Keycloak mendeteksi akun baru dan memicu **Required Action 1: Update Password**. Pengguna wajib membuat kata sandi baru berstandar tinggi (minimal 8-12 karakter, kombinasi huruf/angka).
3. Keycloak memicu **Required Action 2: Verify Email**. Pengguna menerima tautan verifikasi di email kampus.
4. Keycloak memicu **Required Action 3: Configure OTP**. Pengguna memindai (*scan*) QR Code menggunakan aplikasi Authenticator (Google Authenticator / FreeOTP) dan memasukkan 6-digit kode verifikasi pertama.
5. Akun resmi aktif dan terlindungi MFA. Pengguna diarahkan ke aplikasi tujuan.

```text
[ ALUR ENROLLMENT TARGET ]
Login Pertama -> Wajib Buat Password Baru -> Verifikasi Email Kampus -> Scan QR TOTP -> Akun Terproteksi MFA -> Masuk Aplikasi
```

### 6.2 Alur Login Rutin Terproteksi MFA (*Routine Authentication Flow*)
1. Pengguna mengakses aplikasi terintegrasi (misal: `eAkademik` atau `eSDM`).
2. Pengguna memasukkan Username dan Password baru di halaman SSO Keycloak.
3. SSO memvalidasi Password -> Jika benar, Keycloak menampilkan layar **Enter OTP Code**.
4. Pengguna membuka aplikasi Authenticator di ponsel, melihat kode 6-digit yang berlaku 30 detik, dan memasukkannya ke layar SSO.
5. Keycloak memvalidasi OTP -> Meng-issue token OIDC/SAML -> Pengguna berhasil masuk ke aplikasi.

```text
[ ALUR LOGIN RUTIN TARGET ]
Akses Aplikasi -> Input Username & Password -> Validasi -> Layar Masukkan Kode OTP -> Input 6-Digit TOTP -> Token Diberikan -> Masuk Aplikasi
```

### 6.3 Alur Pemulihan Kata Sandi Mandiri (*Self-Service Password Recovery Flow*)
1. Pengguna memilih menu **Forgot Password** pada halaman login SSO.
2. Pengguna memasukkan NIM atau Email Kampus terverifikasi.
3. Keycloak mengirimkan tautan reset kata sandi ke email kampus terverifikasi.
4. Pengguna membuka tautan, memasukkan kata sandi baru, dan mengonfirmasi TOTP.
5. Kata sandi berhasil diperbarui tanpa perlu membuat tiket SMILE ke helpdesk PUSTIPANDA.

```text
[ ALUR PEMULIHAN MANDIRI TARGET ]
Klik Forgot Password -> Input Email Terverifikasi -> Terima Tautan Reset -> Buat Password Baru -> Konfirmasi OTP -> Selesai Mandiri
```

---

## 7. Kesimpulan M10

Penyajian pembandingan *As-Is* vs *To-Be* pada M10 mempertegas bahwa improvisasi arsitektur target **menutup seluruh celah keamanan kritis yang ada saat ini** (Password Policy kosong, NIK default, MFA non-default, Verify Email mati, log retensi kosong) tanpa memerlukan pembangunan ulang platform (*no greenfield requirement*), melainkan memanfaatkan kapabilitas *native* Keycloak secara optimal.

---

## 8. Langkah Selanjutnya

Setelah M10 dikunci, tahap berikutnya adalah **Milestone 11 (M11: Strategic Portfolio)** untuk mengelompokkan 44 aplikasi institusi dan kapabilitas baru ke dalam **McFarlan Strategic Grid**.
