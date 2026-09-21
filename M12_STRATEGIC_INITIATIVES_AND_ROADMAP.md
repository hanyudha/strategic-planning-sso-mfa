# M12 — Inisiatif Strategis & Peta Jalan (Strategic Initiatives & Roadmap)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan Taksonomi 10 Inisiatif Strategis, Matriks Pentahapan 3-Fase, Linimasa Peta Jalan Implementasi 12-Bulan (Q1 s/d Q4), serta Rencana Manajemen Risiko & Mitigasi. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan untuk Pengukuran KPI Strategis (M13).

---

## 1. Tujuan Peta Jalan M12

1. Menyusun taksonomi rinci 10 inisiatif strategis (SI-1..3, TI-1..4, MGT-1..3) yang dirumuskan pada M9.
2. Mengurutkan inisiatif ke dalam 3 fase implementasi berurutan (*logical phase sequencing*) berdasarkan dependensi teknis dan prioritas risiko.
3. Menyediakan linimasa (*timeline*) pelaksanaan yang jelas dalam rentang 12 bulan (Q1 s/d Q4).
4. Menganalisis risiko-risiko implementasi utama (khususnya *user friction* dan kendala helpdesk) serta menyusun rencana mitigasinya.

---

## 2. Taksonomi Inisiatif Strategis (Strategic Initiatives Portfolio)

| Kode | Nama Inisiatif | Pemilik (*Owner*) | Luaran (*Deliverables*) | Kompleksitas | Urgensi |
|---|---|---|---|---|---|
| **TI-1** | Keycloak Security Hardening | Tim Infrastruktur | Password Policy aktif, Verify Email ON, Event Expiration 180 hari. | Rendah | **P1 (Kritis)** |
| **TI-4** | Penghentian Kata Sandi NIK Default | Tim Infrastruktur & Dev | Update Password Required Action aktif pada login 1. | Rendah | **P1 (Kritis)** |
| **MGT-1** | Penyusunan Dokumen SOP SSO | Tim Tata Kelola / PUSTIPANDA | Dokumen SOP Operasional, Registrasi Client, & Insiden SSO. | Sedang | **P1 (Kritis)** |
| **SI-1** | Integrasi MFA pada 44 Client | Tim Dev & Integrasi | 44 Client terproteksi Step-Up MFA terpusat di Keycloak. | Sedang–Tinggi | **P2 (Tinggi)** |
| **SI-2** | Automated Self-Service Recovery | Tim Dev & Helpdesk | Portal pemulihan mandiri via email terverifikasi & OTP. | Sedang | **P2 (Tinggi)** |
| **TI-2** | Mass TOTP MFA Rollout | Tim Infrastruktur & Dev | Pendaftaran TOTP mandiri untuk ~45.000 sivitas akademika. | Sedang | **P2 (Tinggi)** |
| **MGT-2** | Edukasi & Efisiensi Helpdesk | Tim Layanan PUSTIPANDA | Panduan visual TOTP, video tutorial, SOP helpdesk SMILE. | Sedang | **P2 (Tinggi)** |
| **SI-3** | Integration Lifecycle Auto-Sync | Tim Dev | Sinkronisasi otomatis eRegistrasi->eAkademik->Keycloak & eSDM. | Sedang | **P3 (Sedang)** |
| **TI-3** | Privileged WebAuthn MFA | Tim Infrastruktur | WebAuthn/FIDO2 Passkeys aktif untuk akun admin eSDM/eFinansi. | Tinggi | **P3 (Sedang)** |
| **MGT-3** | Compliance Audit & Logging Review | Tim Keamanan & Tata Kelola | Laporan audit berkala & verifikasi kepatuhan UU PDP. | Sedang | **P3 (Sedang)** |

---

## 3. Matriks Pentahapan & Pengurutan (Implementation Phase Sequencing)

```text
+-----------------------------------------------------------------------------------+
| PETA JALAN IMPLEMENTASI (ROADMAP SEQUENCING) SSO + MFA UIN JAKARTA                |
+-----------------------------------------------------------------------------------+
| FASE 1: FONDASI KEAMANAN & QUICK WINS (BULAN 1 - 3 / Q1)                          |
| - Hardening Keycloak (TI-1): Enforce Password Policy & Verify Email.               |
| - Wajib Ubah Password Default NIK saat login pertama (TI-4).                     |
| - Penyusunan Dokumen SOP Tata Kelola & Keamanan SSO (MGT-1).                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| FASE 2: IMPLEMENTASI MFA MASSAL & PEMULIHAN MANDIRI (BULAN 4 - 7 / Q2 - Q3)       |
| - Integrasi MFA TOTP pada 44 Client Aplikasi (SI-1, TI-2).                         |
| - Peluncuran Portal Pemulihan Kata Sandi Mandiri / Self-Service (SI-2).            |
| - Program Edukasi Panduan Visual TOTP & Efisiensi Helpdesk SMILE (MGT-2).          |
| - Penguatan Integrasi Otomatis Siklus Hidup Identitas (SI-3).                      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| FASE 3: PRIVILEGED PROTECTION & AUDIT KEPATUHAN (BULAN 8 - 12 / Q4)               |
| - Implementasi MFA FIDO2 / WebAuthn Passkeys untuk Akun Admin (TI-3).              |
| - Pelaksanaan Audit Kepatuhan Regulasi UU PDP & Pembersihan Log 180 Hari (MGT-3).  |
+-----------------------------------------------------------------------------------+
```

---

## 4. Linimasa Peta Jalan Implementasi (Implementation Roadmap Timeline)

```text
+-----------------------------------------------------------------------------------+
| JADWAL WAKTU IMPLEMENTASI (12 BULAN)                                              |
+-----------------------------------------------------------------------------------+
| INISIATIF                  | Q1 (B1-B3)  | Q2 (B4-B6)  | Q3 (B7-B9)  | Q4 (B10-B12)|
|----------------------------|-------------|-------------|-------------|-------------|
| TI-1  Keycloak Hardening   | [========]  |             |             |             |
| TI-4  Stop Password NIK    | [========]  |             |             |             |
| MGT-1 Penyusunan SOP SSO   | [========]  |             |             |             |
| SI-1  MFA pada 44 Client   |             | [=========] | [=========] |             |
| TI-2  Mass TOTP Rollout    |             | [=========] | [=========] |             |
| SI-2  Self-Service Recovery|             | [=========] |             |             |
| MGT-2 Edukasi & SMILE      |             | [=========] | [=========] |             |
| SI-3  Auto-Sync Lifecycle  |             |             | [=========] |             |
| TI-3  Privileged WebAuthn  |             |             |             | [=========] |
| MGT-3 Audit PDP & Log      |             |             |             | [=========] |
+-----------------------------------------------------------------------------------+
```

---

## 5. Manajemen Risiko Implementasi & Rencana Mitigasi

| Risiko Implementasi | Tingkat Risiko | Dampak Operasional | Rencana Mitigasi Strategis |
|---|---|---|---|
| **Resistensi / Kebingungan Pengguna saat Pendaftaran TOTP** | Tinggi | Pengguna gagal login atau membanjiri helpdesk karena tidak paham scan QR Code. | **Mitigasi**: Kampanye edukasi bertahap via email/banner, panduan visual ringkas, video tutorial, dan **masa transisi pendaftaran mandiri selama 30 hari** sebelum MFA diwajibkan secara ketat (*enforced*). |
| **Lonjakan Tiket Helpdesk SMILE pada Hari Pertama (*Go-Live*)** | Sedang–Tinggi | Antrean tiket SMILE membengkak saat aturan MFA diaktifkan. | **Mitigasi**: Menyediakan fitur *backup codes* saat pendaftaran awal dan membentuk *task force* helpdesk dedicated PUSTIPANDA selama 2 minggu pertama *Go-Live*. |
| **Kendala Perangkat / Smartphone Hilang** | Sedang | Pengguna tidak dapat mengakses akun karena kehilangan ponsel *authenticator*. | **Mitigasi**: Menyediakan alur *Self-Service Recovery* via email kampus terverifikasi dan verifikasi identitas mandiri tanpa perlu reset manual oleh admin. |
| **Kegagalan Sync eSDM Real-Time** | Rendah–Sedang | Akun pegawai baru terhambat atau status penonaktifan terlambat. | **Mitigasi**: Penguatan error handling pada `esdm-sync-service`, notifikasi otomatis saat sync gagal, dan peninjauan log berkala. |

---

## 6. Kesimpulan M12

Peta Jalan M12 menetapkan tahapan yang **logis, realistis, dan berisiko rendah (*low-risk execution*)**. Dengan mengedepankan perbaikan kebijakan dasar dan *quick wins* di Fase 1 (Q1), institusi membangun fondasi yang kuat sebelum meluncurkan pendaftaran TOTP massal di Fase 2 (Q2-Q3) dan pelindungan khusus akun admin di Fase 3 (Q4).

---

## 7. Langkah Selanjutnya

Setelah M12 dikunci, tahap berikutnya adalah **Milestone 13 (M13: KPI & Strategic Measurement)** untuk menentukan indikator kinerja utama (*Key Performance Indicators*) yang terukur bagi keberhasilan proyek SSO + MFA.
