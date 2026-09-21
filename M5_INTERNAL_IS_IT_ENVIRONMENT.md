# M5 — Lingkungan SI/TI Internal (Internal IS/IT Environment)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan analisis lingkungan SI/TI internal UIN Syarif Hidayatullah Jakarta: evaluasi teknis platform Keycloak SSO, pipeline identitas, 44 client terdaftar, celah keamanan internal (*Password Policy* & MFA), serta kapasitas operasional TI. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan SI/TI internal untuk formulasi strategi berikutnya.

---

## 1. Tujuan Analisis M5

1. Evaluasi kedalaman teknis platform Keycloak SSO (realm SSOUIN) dan kapabilitas infrastruktur pendukungnya.
2. Evaluasi pipeline identitas (eSDM & eAkademik) serta keandalan mekanisme sinkronisasi data identitas pengguna.
3. Evaluasi lanskap integrasi 44 client/aplikasi terdaftar dan kesiapan protokol autentikasi (OpenID Connect & SAML).
4. Menganalisis kontrol keamanan internal saat ini (*internal cybersecurity controls gap*).
5. Menganalisis kapasitas SDM dan operasional TI (tim PUSTIPANDA, data center, helpdesk SMILE) dalam mengelola layanan SSO.

---

## 2. Matriks Evaluasi Komponen SI/TI Internal

| Komponen SI/TI | Kondisi & Bukti Teknis | Evaluasi Kapabilitas & Celah (Gap) | Kode Bukti |
|---|---|---|---|
| **Platform SSO** | Keycloak, realm `SSOUIN`, domain dev `dev-sso.uinjkt.ac.id`. Dijalankan di data center kampus. | Platform Keycloak terbukti *robust* dan modern (berbasis Quarkus/JPA & Infinispan). Mendukung ketersediaan provider OTP dan WebAuthn (T-01). Namun, deployment versi & skema *clustering* (multi-node/HA) masih perlu dipastikan. | T-01, U-04 |
| **Sumber Identitas Mahasiswa** | eAkademik / Akademik Pusat. | **Migrasi Penuh**: Seluruh mahasiswa di SSO produksi telah dimigrasi penuh ke Keycloak lokal. Pengaktifan akun mahasiswa baru terintegrasi otomatis via *trigger event* eRegistrasi -> eAkademik. | T-02, U-08, U-09 |
| **Sumber Identitas Dosen/Tendik** | eSDM / Kepegawaian via provider *REST API Migration*. | **Real-Time Sync**: Synchronizer `esdm-sync-service` beroperasi secara *real-time*. eSDM berwenang mengaktifkan/menonaktifkan akun SSO pegawai. Merupakan ketergantungan kritis (*critical dependency*). | T-02, T-11, U-05, U-10 |
| **Integrasi Aplikasi** | 44 Client terdaftar (3 halaman di Keycloak Admin Console). | Didominasi oleh OpenID Connect (10/11 Client Scopes). Terdapat setidaknya 1 integrasi SAML (`staff1.uinjkt.ac.id`). Ditemukan pola client ganda (suffix SKI/Postgre) sebagai *artifact development*. | T-05, T-09, T-10, T-11, T-12, U-08 |
| **Kebijakan Kata Sandi (Password Policy)** | **KOSONG** (tidak ada aturan yang diterapkan). | **Celah Keamanan Kritis**: Tidak ada batasan panjang minimal, kompleksitas karakter, riwayat kata sandi, atau kebocoran kata sandi. Pengguna bebas menggunakan kata sandi apa pun. | T-06 |
| **Faktor Autentikasi Kedua (MFA)** | `Configure OTP` enabled di Required Actions, tetapi **BUKAN Default Action**. | Kapabilitas TOTP tersedia (T-01, T-07), namun belum diwajibkan secara luas (*optional per user*). WebAuthn SPI tersedia di server tetapi Required Action belum di-register. | T-01, T-04, T-07 |
| **Fitur Pemulihan Mandiri (Self-Service Reset)** | Reset mandiri kata sandi tersedia (Update Password = Default Action). Namun `Verify Email` **DISABLED**. | Karena email tidak diverifikasi oleh Keycloak, tautan pemulihan kata sandi memiliki risiko pengiriman ke email yang salah, memaksa pengguna menggunakan tiket SMILE. | T-04, D-01, D-03 |
| **Logging & Audit Events** | **Login Events & Admin Events ON**. Event Listener: `jboss-logging`. | Mencatat hampir seluruh jenis event (LOGIN, LOGOUT, UPDATE_PASSWORD, RESET_PASSWORD, LOGIN_ERROR). **Celah**: Retensi (*Expiration*) kosong, berisiko penumpukan log tanpa batas di database. | T-03, T-08 |
| **Operasional Helpdesk & Bantuan** | SMILE Tiketing & WhatsApp PUSTIPANDA. | SMILE menangani 2.624 tiket login/kata sandi. Tingginya beban penanganan tiket manual menunjukkan perlunya perbaikan fitur *self-service*. | D-02, D-03, U-03 |

---

## 3. Analisis Kesiapan Infrastruktur TI untuk MFA

```text
+-----------------------------------------------------------------------------------+
| EVALUASI KESIAPAN TEKNIS KEYCLOAK SSO UNTUK MFA (M5)                              |
+-----------------------------------------------------------------------------------+
| KAPABILITAS TERSEDIA (READY)        | KEBUTUHAN PENGATURAN (CONFIGURATION GAP)    |
| - Provider TOTP/OTP (SHA1, 6-digit) | - OTP belum dijadikan Default Action        |
| - Provider WebAuthn/FIDO2 (SPI)     | - WebAuthn Required Action belum di-register|
| - Client Scopes OIDC & SAML         | - Password Policy masih KOSONG              |
| - Login & Admin Event Logging       | - Verify Email masih DISABLED               |
| - Sync Real-time eSDM               | - Log Expiration belum dikonfigurasi        |
+-----------------------------------------------------------------------------------+
```

### 3.1 Keunggulan Teknis Platform Keycloak
* Keycloak di realm `SSOUIN` sudah memiliki modul autentikasi MFA bawaan (OTP dan WebAuthn), sehingga **tidak diperlukan pembangunan ulang platform SSO dari nol** (*no greenfield requirement*).
* Integrasi OIDC dan SAML yang sudah berjalan pada 44 aplikasi memberikan dasar yang kuat untuk memperluas autentikasi terpusat.

### 3.2 Celah Teknis & Konfigurasi (*Technical Gaps*)
1. **Kebijakan Keamanan Lemah**: Ketiadaan *Password Policy* dan *Verify Email* menyebabkan fondasi autentikasi faktor tunggal sangat rentan.
2. **Belum Ada Kebijakan Akses Berbasis Risiko (*Risk-Based Access*)**: Saat ini Keycloak belum mengonfigurasi aturan penilaian risiko (misalnya membedakan akses dari jaringan internal kampus vs jaringan publik luar kampus, atau membedakan akun mahasiswa vs akun admin).
3. **Keterbatasan Audit & Log Management**: Log events dicatat secara lengkap, tetapi tanpa kebijakan retensi (*expiration*) dan tanpa integrasi SIEM/monitoring terpusat, audit log sulit dianalisis secara proaktif.

---

## 4. Evaluasi Kapasitas SDM TI & Tata Kelola Operasional

1. **Struktur Pengelolaan TI**:
   * Tim Infrastruktur Data Center: Bertanggung jawab atas ketersediaan server Keycloak dan database SSO.
   * Tim Pengembangan / Integrasi: Mengelola registrasi client aplikasi dan integrasi *REST API migration*.
   * Tim Layanan PUSTIPANDA / Helpdesk: Menangani tiket bantuan pengguna via SMILE dan kanal WhatsApp.
2. **Ketiadaan Dokumen SOP Resmi**:
   * Pengelolaan registrasi client baru, penanganan reset password manual, dan manajemen hak akses admin SSO belum didukung oleh SOP tertulis yang terstandarisasi.
3. **Kapasitas Penanganan Tiket**:
   * 2.624 tiket terkait login dan kata sandi pada sistem SMILE menunjukkan bahwa sebagian besar waktu tim helpdesk tersedot untuk tugas-tugas administratif rutin yang seharusnya dapat diselesaikan mandiri oleh pengguna.

---

## 5. Kesimpulan M5

Hasil evaluasi lingkungan SI/TI internal M5 menyimpulkan bahwa **UIN Syarif Hidayatullah Jakarta memiliki fondasi platform SSO yang kuat (Keycloak)**, namun **sangat lemah pada aspek konfigurasi kebijakan keamanan internal** (*Password Policy* kosong, MFA tidak diwajibkan, *Verify Email* mati).

Penerapan MFA di masa depan dapat memanfaatkan kapabilitas bawaan Keycloak yang sudah ada, dengan syarat celah konfigurasi dasar (kebijakan kata sandi, verifikasi email, dan otomatisasi *self-service*) diperbaiki terlebih dahulu.

---

## 6. Langkah Selanjutnya

Tahap berikutnya adalah **Milestone 6 (M6: External IS/IT Environment)** untuk menganalisis lanskap teknologi MFA eksternal (TOTP, Authenticator App, Push Notification, FIDO2/Passkey) dan kriteria pemilihannya tanpa menunjuk vendor secara prematur.
