# M13 — KPI & Pengukuran Strategis (KPI & Strategic Measurement)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan 12 Indikator Kinerja Utama (*KPI*) Strategis Terukur melintasi 5 domain pengukuran (Adopsi MFA, Postur Keamanan, Efisiensi Helpdesk, Keandalan Sistem & Log, Kepatuhan PDP & SOP), serta mekanisme pemantauan kinerja. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan pengukuran akhir untuk Dokumen Rencana Strategis Final (M14).

---

## 1. Tujuan Pengukuran Strategis M13

1. Menetapkan metrik kinerja kuantitatif yang objektif untuk mengukur keberhasilan implementasi SSO + MFA.
2. Memastikan seluruh inisiatif strategis M9 dan linimasa M12 memiliki tolok ukur ketercapaian (*target threshold*) yang jelas.
3. Mengukur efisiensi operasional helpdesk SMILE, penurunan risiko keamanan siber, tingkat adopsi pengguna, dan kepatuhan regulasi UU PDP.

---

## 2. Matriks Indikator Kinerja Utama (Key Performance Indicators)

```text
+-----------------------------------------------------------------------------------+
| INDIKATOR KINERJA UTAMA (KPI STRATEGIS) SSO + MFA UIN JAKARTA                     |
+-----------------------------------------------------------------------------------+
| 1. ADOPSI & CAKUPAN MFA    : Target 100% Admin (Q1) & >85% Mass User (Q3).       |
| 2. POSTUR KEAMANAN         : 0 Insiden Credential Stuffing & 100% Password Policy |
| 3. EFISIENSI HELPDESK      : Penurunan Tiket SMILE >80% (2.624 -> <500 tiket/th)  |
| 4. KEANDALAN SISTEM        : Uptime SSO >= 99,9% & Log Retention Purge 180 Hari   |
| 5. TATA KELOLA & REGULASI  : 100% SOP Disahkan (Q1) & 100% Kepatuhan UU PDP PDP   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Rincian KPI Terukur Berdasarkan 5 Domain Kinerja

| Kode KPI | Domain Pengukuran | Metrik KPI / Indikator | Nilai Awal (*Baseline M2*) | Target Ketercapaian (*Target M13*) | Frekuensi Ukur | Pemilik KPI |
|---|---|---|---|---|---|---|
| **KPI-1** | Adopsi MFA Massal | Persentase mahasiswa, dosen, dan tendik yang mendaftar TOTP mandiri. | 0% (Configure OTP non-default) | **>85% (Q3) / 100% (Q4)** | Bulanan | PUSTIPANDA / Layanan |
| **KPI-2** | Adopsi MFA Privileged | Persentase akun admin (eSDM, eFinansi, Keycloak) yang terproteksi FIDO2/WebAuthn. | 0% (Hanya kata sandi) | **100% (Q1 Admin, Q4 All Privileged)** | Bulanan | Tim Keamanan IT |
| **KPI-3** | Cakupan Aplikasi MFA | Persentase dari 44 client aplikasi yang terintegrasi Step-Up MFA terpusat. | 0% (Hanya login SSO faktor tunggal) | **100% (44 Client di Q3)** | Triwulanan | Tim Dev & Integrasi |
| **KPI-4** | Penegakan Password Policy | Ketersediaan aturan panjang min 8-12 char, kompleksitas, dan *lockout* 5x gagal. | Kosong / Tidak Ada Aturan (T-06) | **100% Enforced di Keycloak (Q1)** | Real-time | Tim Infrastruktur |
| **KPI-5** | Eliminasi Password NIK | Persentase penggantian kata sandi default NIK/NIM secara mandiri saat login 1. | 0% (Pengguna memakai NIK default) | **100% Password Default Terhapus (Q1)** | Bulanan | Tim Infrastruktur |
| **KPI-6** | Penurunan Insiden Siber | Jumlah insiden pembobolan akun (*account takeover / credential guessing*) tahunan. | Berisiko Tinggi (Password NIK & tanpa MFA) | **0 Kasus Insiden (Q2–Q4)** | Bulanan | Tim Keamanan IT |
| **KPI-7** | Efisiensi Tiket SMILE | Jumlah tiket manual penanganan masalah login/reset kata sandi di SMILE. | 2.624 Tiket (Ekspor D-02) | **Penurunan >80% (<500 tiket/tahun)** | Bulanan | Helpdesk PUSTIPANDA |
| **KPI-8** | Waktu Pemulihan Akun | Rata-rata waktu pemulihan kata sandi mandiri (*Self-Service Recovery MTTR*). | Jam s/d Hari (Proses Manual SMILE) | **< 3 Menit (Via Email Terverifikasi)** | Real-time | PUSTIPANDA / System |
| **KPI-9** | Ketersediaan Layanan SSO | Persentase *uptime* operasional Keycloak Cluster Realm SSOUIN. | `[EVIDENCE NEEDED]` | **>= 99,9% Uptime** | Bulanan | Tim Data Center |
| **KPI-10** | Retensi Log Audit | Kepatuhan *Event Expiration Policy* Keycloak (penghapusan otomatis log >180 hari). | Expiration Kosong (T-08) | **100% Compliant (Auto-Purge 180 Hari)** | Bulanan | Tim Infrastruktur |
| **KPI-11** | Dokumentasi SOP SSO | Persentase dokumen SOP Tata Kelola, Registrasi Client, & Insiden SSO yang disahkan. | 0% (Belum ada SOP resmi) | **100% SOP Disahkan Pimpinan (Q1)** | Sekali | Tim Tata Kelola |
| **KPI-12** | Kepatuhan UU PDP | Pemenuhan standar pelindungan data pribadi sivitas akademika sesuai UU No. 27/2022. | Non-Compliant (Password default NIK) | **100% Compliant (Lulus Audit PDP)** | Tahunan | Pimpinan & Legal |

---

## 4. Mekanisme Pemantauan & Pelaporan Strategis (Monitoring Mechanism)

1. **Dashboard Pemantauan Kinerja SSO (Keycloak Events Monitor)**:
   * Menggunakan log events Keycloak (`jboss-logging` & JPA store) untuk memantau tren login sukses, pendaftaran TOTP harian, dan event *LOGIN_ERROR*.
2. **Laporan Bulanan Tim Layanan PUSTIPANDA**:
   * Evaluasi jumlah tiket SMILE yang berhasil dipotong oleh fitur *Self-Service Recovery*.
3. **Audit Kepatuhan Keamanan & Retensi Log Triwulanan**:
   * Tim Keamanan IT memverifikasi pembersihan otomatis log audit berusia >180 hari dan mengecek kepatuhan pendaftaran MFA pada akun admin baru.

---

## 5. Kesimpulan M13

Kerangka KPI M13 menyediakan tolok ukur kuantitatif yang defensibel. Dengan target utama **penurunan >80% tiket SMILE**, **100% eliminasi kata sandi default NIK**, **>85% adopsi TOTP massal**, dan **100% kepatuhan UU PDP**, proyek penguatan SSO + MFA UIN Syarif Hidayatullah Jakarta memiliki indikator keberhasilan yang jelas dan dapat dipertanggungjawabkan kepada pimpinan universitas.

---

## 6. Langkah Selanjutnya

Setelah M13 dikunci, tahap akhir adalah **Milestone 14 (Final Strategic Plan)** untuk mengintegrasikan seluruh dokumen M0 s/d M13 ke dalam laporan rencana strategis akademik akhir secara utuh.
