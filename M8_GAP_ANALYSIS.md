# M8 — Analisis Kesenjangan (Gap Analysis)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan analisis kesenjangan (*gap analysis*) antara kondisi SSO saat ini dan kondisi target pada 7 dimensi (Teknologi, Kebijakan, Proses, Tata Kelola, SDM, Pemantauan, dan Risiko), serta matriks tindakan penutupan gap (*gap closure actions*). Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi dasar langsung untuk Formulasi Strategi SI/TI (M9).

---

## 1. Tujuan Analisis M8

1. Memetakan kesenjangan (*gaps*) nyata antara kondisi operasional SSO saat ini dan kondisi target yang aman, compliant, serta efisien.
2. Mengelompokkan kesenjangan ke dalam 7 dimensi: Teknologi, Kebijakan, Proses & Siklus Hidup, Tata Kelola, SDM/Kapasitas, Pemantauan/Audit, dan Pengendalian Risiko.
3. Menetapkan tindakan penutupan gap (*gap closure actions*) sebagai jembatan menuju Formulasi Strategi SI/TI (M9) dan Peta Jalan Implementasi (M12).

---

## 2. Pemetaan Kesenjangan Rinci Melintasi 7 Dimensi

```text
+-----------------------------------------------------------------------------------+
| ANALISIS KESENJANGAN (M8) — MATRIKS DARI CURRENT STATE KE TARGET STATE            |
+-----------------------------------------------------------------------------------+
| DIMENSI           | KONDISI SAAT INI (CURRENT)   | KONDISI TARGET (TARGET)    |
|-------------------|------------------------------|----------------------------|
| 1. Teknologi      | SSO tanpa MFA diwajibkan;    | SSO terproteksi MFA (TOTP  |
|                   | WebAuthn belum di-register.  | massal, FIDO2/WebAuthn admin|
| 2. Kebijakan      | Password policy KOSONG (T-06)| Password policy ketat &    |
|                   | & Verify Email DISABLED.     | Verify Email ENABLED.      |
| 3. Proses         | 2.624 tiket SMILE manual;    | Self-service recovery      |
|                   | password default NIK/NIM.    | otomatis & 1st login reset.|
| 4. Tata Kelola    | Belum ada dokumen SOP SSO.   | SOP formal governance SSO. |
| 5. SDM & Kapasitas| Beban helpdesk tinggi;       | Edukasi user awareness &   |
|                   | literasi keamanan bervariasi.| SOP helpdesk terstandar.  |
| 6. Audit & Log    | Retensi log Expiration KOSONG| Retensi log teratur (90-   |
|                   | di Keycloak (T-08).          | 180 hari) & SIEM alerts.  |
| 7. Risiko Keamanan| Autentikasi 1-faktor rentan  | Autentikasi 2-faktor anti- |
|                   | credential guessing/phishing.| phishing & compliant UU PDP|
+-----------------------------------------------------------------------------------+
```

---

## 3. Matriks Matrikulasi Kesenjangan & Tindakan Penutupan (*Gap Closure Actions*)

| Dimensi | Kondisi Saat Ini (M2/M5) | Kondisi Target (Strategis) | Kesenjangan (*Gap*) | Tindakan Penutupan Gap (*Closure Action*) |
|---|---|---|---|---|
| **1. Teknologi** | MFA (`Configure OTP`) enabled tetapi bukan *Default Action* (T-04); WebAuthn SPI belum di-register. | MFA diwajibkan secara bertahap (TOTP untuk massal, FIDO2/WebAuthn untuk admin). | Belum ada pemicuan MFA otomatis dan penataan kebijakan pendaftaran (*enrollment flow*). | Mengonfigurasi OTP sebagai *Default Required Action* dan meregister WebAuthn SPI pada Keycloak. |
| **2. Kebijakan** | *Password Policy* KOSONG (T-06); *Verify Email* DISABLED (T-04). | Kebijakan kata sandi berstandar tinggi (panjang, kompleksitas, *lockout*) & verifikasi email aktif. | Ketiadaan aturan teknis pembatas kata sandi dan ketiadaan verifikasi kepemilikan email. | Mengonfigurasi *Password Policy* di Keycloak Admin Console dan mengaktifkan *Verify Email*. |
| **3. Proses** | Password default NIK/NIM (U-06, U-07); 2.624 tiket SMILE penanganan manual (D-02). | Penghentian total password NIK; alur penggantian mandiri saat login pertama & *self-service reset*. | Alur pembuatan akun belum mewajibkan password baru mandiri; pemulihan masih bergantung pada tiket. | Mewajibkan *Update Password* saat login pertama dan mengotomatiskan reset password mandiri via email. |
| **4. Tata Kelola** | Pengelolaan SSO berjalan tanpa dokumen SOP resmi tertulis; peran admin belum teratur formal. | Dokumen SOP resmi tata kelola SSO, *role-based admin matrix*, dan prosedur manajemen insiden. | Belum ada panduan baku operasional, batas kewenangan admin, dan prosedur pemulihan insiden. | Menyusun dan mengesahkan dokumen SOP Operasional & Keamanan SSO e-Semesta UIN Jakarta. |
| **5. SDM & Kapasitas** | Beban jam kerja staf helpdesk tersedot tiket manual; literasi keamanan pengguna bervariasi. | Staf helpdesk fokus pada kasus eskalasi khusus; sivitas akademika paham alur MFA. | Celah pemahaman pengguna mengenai MFA & beban kerja helpdesk yang tidak efisien. | Melaksanakan sosialisasi/panduan pendaftaran MFA bagi pengguna dan pelatihan SOP bagi helpdesk. |
| **6. Pemantauan & Audit** | Login & Admin Events aktif (T-03, T-08), tetapi *Expiration* (retensi) KOSONG. | Log audit tersimpan dengan batas retensi terukur (misal: 180 hari) dan terpantau berkala. | Risiko penumpukan data log di database Keycloak dan ketiadaan prosedur peninjauan log rutin. | Mengonfigurasi kebijakan *Event Expiration* di Keycloak dan menetapkan jadwal audit log berkala. |
| **7. Keamanan & Risiko** | Pertahanan autentikasi bergantung penuh pada 1-faktor kata sandi tunggal (*single point of failure*). | Pertahanan autentikasi berlapis (MFA) yang *compliant* dengan UU PDP No. 27/2022. | Kerentanan tinggi terhadap penyerobotan akun, pencurian kredensial, dan sanksi hukum. | Mengintegrasikan MFA pada seluruh 44 client aplikasi e-Semesta secara terpusat. |

---

## 4. Kesimpulan M8

Analisis kesenjangan M8 menegaskan bahwa penutupan *gap* dari kondisi saat ini menuju kondisi target **tidak membutuhkan perombakan total infrastruktur** (*no infrastructure rebuild*), melainkan berfokus pada:
1. **Peningkatan Konfigurasi Teknis (*Technical Re-configuration*)**: Mengisi Password Policy, mengaktifkan Verify Email, menetapkan OTP sebagai Default Action, dan membatasi retensi log.
2. **Pemberdayaan Alur Otomatis (*Process Automation*)**: Menghentikan kata sandi default NIK dan mengaktifkan *self-service recovery* mandiri.
3. **Formalisasi Tata Kelola (*Governance Formalization*)**: Menyusun SOP resmi dan melaksanakan edukasi pendaftaran MFA bagi sivitas akademika.

---

## 5. Langkah Selanjutnya

Hasil analisis kesenjangan M8 menjadi masukan teknis langsung untuk **Milestone 9 (M9: Strategy Formulation)** dalam merumuskan 3 Pilar Strategi SI/TI: *IS Strategy*, *IT Strategy*, dan *IS/IT Management Strategy*.
