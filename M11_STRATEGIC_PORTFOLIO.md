# M11 — Portofolio Strategis (Strategic Portfolio)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan pemetaan Portofolio Strategis Aplikasi & Kapabilitas SI/TI UIN Syarif Hidayatullah Jakarta ke dalam 4 kuadran McFarlan Strategic Grid (Strategic, Key Operational, High Potential, Support), serta implikasi prioritas perlindungan MFA. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan untuk Peta Jalan Implementasi (M12).

---

## 1. Tujuan Portofolio Strategis M11

1. Mengategorikan seluruh 44 client aplikasi terdaftar dan kapabilitas keamanan baru ke dalam 4 kuadran McFarlan Strategic Grid.
2. Membedakan aplikasi mana yang berdampak langsung pada keberhasilan strategis masa depan, kelangsungan operasional harian, inovasi bernilai tinggi, dan pendukung administrasi.
3. Memberikan panduan prioritas pengalokasian sumber daya TI dan perlindungan keamanan MFA berdasarkan kontribusi strategis masing-masing aplikasi.

---

## 2. Matriks McFarlan Strategic Grid (Ward & Peppard)

```text
+-----------------------------------------------------------------------------------+
| MCFARLAN STRATEGIC GRID — SISTEM INFORMASI & KAPABILITAS SSO UIN JAKARTA          |
+-----------------------------------------------------------------------------------+
| STRATEGIC (STRATEGIS)               | HIGH POTENTIAL (POTENSIAL TINGGI)           |
| Kritis untuk keberhasilan masa depan| Berpotensi tinggi, butuh pilot/pembuktian   |
| - Keycloak SSO Core Engine (SSOUIN) | - Biometric Authenticator / FIDO2 Passkeys  |
| - MFA Engine (TOTP Massal & FIDO2)  | - Mobile Campus Apps (mCampus, mhst)        |
| - Self-Service Recovery & Policy    | - Learning Management System (dev-lms)      |
| - Portal SSO e-Semesta (sso)        | - Integration Bridge (uhelp sso bridge)     |
+-------------------------------------+---------------------------------------------+
| KEY OPERATIONAL (KUNCI OPERASIONAL) | SUPPORT (PENDUKUNG)                         |
| Kritis untuk operasional harian     | Mendukung efisiensi, dampak langsung rendah |
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

## 3. Analisis Kategori Kuadran McFarlan

### 3.1 Kuadran STRATEGIC (Strategis)
Aplikasi dan kapabilitas dalam kuadran ini sangat vital bagi keberhasilan transformasi digital dan ketahanan siber universitas di masa depan.
* **Keycloak SSO Core Engine (Realm SSOUIN)**: Pusat autentikasi terpusat yang melindungi seluruh ekosistem digital e-Semesta.
* **MFA Engine (TOTP Massal & FIDO2 Privileged)**: Instrumen kunci untuk menghentikan serangan *credential stuffing* dan memenuhi kepatuhan UU PDP No. 27/2022.
* **Self-Service Identity Recovery & Password Policy Enforcer**: Modul otomatisasi yang menjamin ketahanan layanan dan memotong beban operasional helpdesk.
* **Portal SSO e-Semesta (`sso`)**: Pintu gerbang akses utama pengguna sivitas akademika.

### 3.2 Kuadran KEY OPERATIONAL (Kunci Operasional)
Aplikasi dalam kuadran ini merupakan penopang utama operasional akademik, kepegawaian, dan keuangan harian. Gangguan autentikasi pada kuadran ini akan melumpuhkan aktivitas universitas.
* **Layanan Akademik**: `eAkademik`, `eRegistrasi`, `eAkademik-portal` (proses KRS, penilaian, registrasi mhs baru).
* **Layanan SDM**: `eSDM`, `esdm-sync-service`, `eKinerja` (manajemen data dosen/tendik dan insentif kinerja).
* **Layanan Keuangan & Admisi**: `eFinansi`, `ePembayaran`, `eadmisi` (transaksi UKT & penerimaan mhs).
* **Infrastruktur Jaringan**: `Wi-Fi SSO Kampus` (akses internet harian mahasiswa dan staf di kampus).

### 3.3 Kuadran HIGH POTENTIAL (Potensial Tinggi)
Teknologi dan aplikasi inovatif yang menjanjikan nilai tambah di masa depan, tetapi memerlukan tahap uji coba (*pilot project*) sebelum diterapkan secara luas.
* **Biometric Authenticator / FIDO2 Passkeys**: Penggunaan login biometrik (TouchID/FaceID/Windows Hello) untuk akses admin tanpa kata sandi.
* **Mobile Campus Apps (`mCampus`, `mhst`)**: Aplikasi mobile terpadu bagi mahasiswa/dosen yang memerlukan integrasi SDK SSO & MFA.
* **Learning Management System (`dev-lms`)**: Platform perkuliahan daring yang berpotensi menjadi kritis seiring peningkatan *hybrid learning*.

### 3.4 Kuadran SUPPORT (Pendukung)
Aplikasi yang berfokus pada efisiensi administrasi internal. Kerusakan pada kuadran ini tidak langsung melumpuhkan operasional utama universitas.
* **Tata Usaha & Riset**: `PLO` (persuratan dinas), `eRiset`, `eKKN`.
* **Pengelolaan Aset & Alumni**: `eAset`, `eBeasiswa`, `eAlumni`.
* **Client Backend / Dev Artifacts**: Client bertipe SKI/Postgre (`eAsetPostgreSKI`, `eBeasiswaPostgreSKI`, `eRegistrasiSKI`, `local-api`, dll.).

---

## 4. Implikasi Portofolio terhadap Penerapan MFA & Keamanan

1. **Prioritas Utama Penerapan MFA (*Phase 1 Rollout*)**:
   * Kuadran **STRATEGIC** dan Kuadran **KEY OPERATIONAL** wajib mendapatkan prioritas utama penerapan MFA (TOTP Massal untuk seluruh pengguna dan FIDO2/WebAuthn untuk akun admin eSDM/eFinansi/Keycloak).
2. **Perlakuan Khusus Kuadran HIGH POTENTIAL**:
   * Dilakukan *pilot project* pendaftaran FIDO2/Passkeys pada kelompok terbatas (tim PUSTIPANDA & Admin eSDM) sebelum ekspansi.
3. **Pembersihan Portofolio Kuadran SUPPORT**:
   * Client backend/development yang tidak aktif (seperti `local-sso-soa` dan `ssotesting`) dinonaktifkan untuk mengurangi *attack surface*.

---

## 5. Kesimpulan M11

Pemetaan McFarlan Strategic Grid M11 memberikan kejelasan strategis bahwa **Keycloak SSO dan Modul MFA merupakan aset STRATEGIS teratas** yang melindungi seluruh aplikasi **KEY OPERATIONAL** universitas.

---

## 6. Langkah Selanjutnya

Setelah M11 dikunci, tahap berikutnya adalah **Milestone 12 (M12: Strategic Initiatives & Roadmap)** untuk menyusun urutan pelaksanaan inisiatif (*sequencing*), jadwal implementasi, dan pengelompokan fase.
