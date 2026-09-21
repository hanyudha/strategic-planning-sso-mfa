# M7 — SWOT & Isu-Isu Strategis (SWOT & Strategic Issues)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan sintesis matriks SWOT, matriks strategi TOWS (SO, WO, ST, WT), serta 4 isu strategis terprioritas (IS-1 s/d IS-4) untuk pembaruan sistem SSO & MFA UIN Syarif Hidayatullah Jakarta. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan utama untuk Analisis Gap (M8) dan Formulasi Strategi (M9).

---

## 1. Matriks Sintesis SWOT

```text
+-----------------------------------------------------------------------------------+
| SINTESIS SWOT SISTEM AUTENTIKASI SSO UIN SYARIF HIDAYATULLAH JAKARTA              |
+-----------------------------------------------------------------------------------+
| STRENGTHS (Kekuatan Internal)         | WEAKNESSES (Kelemahan Internal)           |
| - Keycloak SSO terpusat & modern.    | - Password Policy KOSONG (T-06).          |
| - Integrasi 44 client/aplikasi.       | - Password default NIK terprediksi.       |
| - Sync eSDM real-time & migrasi mhs. | - MFA belum diwajibkan (non-default).     |
| - Kapabilitas TOTP/WebAuthn ready.    | - Verify Email DISABLED (T-04).           |
| - Audit Logging (Login/Admin) ON.     | - Retensi log events kosong & 2.624 tiket.|
+-----------------------------------------------------------------------------------+
| OPPORTUNITIES (Peluang Eksternal)     | THREATS (Ancaman Eksternal)               |
| - Mandat UU PDP & Perpres SPBE.       | - Credential guessing & stuffing NIK/NIM. |
| - TOTP Keycloak BEBAS BIAYA lisensi.  | - Phishing menembus 1-faktor password.    |
| - FIDO2/Passkey untuk akun admin.     | - Penyalahgunaan Wi-Fi & data tampering.  |
| - Perilaku digitalisasi kampus.       | - Sanksi hukum & pencemaran reputasi.     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Formulasi Strategi Matriks TOWS (SWOT Strategy Matrix)

### 2.1 Strategi SO (Strengths - Opportunities): Memanfaatkan Kekuatan untuk Menangkap Peluang
1. **SO-1**: Memanfaatkan kapabilitas *native* Keycloak (TOTP & WebAuthn) yang sudah tersedia tanpa biaya lisensi untuk menerapkan MFA terpusat guna memenuhi kepatuhan UU PDP No. 27/2022 dan Perpres SPBE.
2. **SO-2**: Menggunakan arsitektur terpusat Keycloak yang sudah terintegrasi dengan 44 client untuk mendistribusikan pelindungan MFA secara langsung ke seluruh ekosistem aplikasi e-Semesta.

### 2.2 Strategi WO (Weaknesses - Opportunities): Mengatasi Kelemahan dengan Memanfaatkan Peluang
1. **WO-1**: Mengonfigurasi *Password Policy* bawaan Keycloak (panjang minimal, kompleksitas, *lockout*) dan mengaktifkan *Verify Email* untuk memenuhi standar keamanan BSSN sekaligus memfasilitasi pemulihan mandiri pengguna.
2. **WO-2**: Mengurangi beban 2.624 tiket helpdesk SMILE melalui otomatisasi pemulihan kata sandi mandiri berbasis verifikasi email dan alur *enrollment* TOTP yang terpandu.

### 2.3 Strategi ST (Strengths - Threats): Menggunakan Kekuatan untuk Menangkal Ancaman
1. **ST-1**: Mewajibkan faktor kedua (TOTP) bagi seluruh sivitas akademika untuk melumpuhkan ancaman *credential guessing* dan *phishing* yang mengeksploitasi kata sandi tunggal pada 44 aplikasi institusi.
2. **ST-2**: Memperketat keamanan akses Wi-Fi kampus melalui penguatan autentikasi SSO terproteksi MFA guna mencegah penyalahgunaan *bandwidth* oleh pihak luar.

### 2.4 Strategi WT (Weaknesses - Threats): Meminimalkan Kelemahan dan Menghindari Ancaman
1. **WT-1**: Menghentikan penggunaan kata sandi default berbasis NIK/NIM secara total dan mengharuskan penggantian kata sandi berstandar tinggi saat login pertama (*Update Password Required Action*).
2. **WT-2**: Menerapkan pelindungan MFA tingkat tinggi (FIDO2/WebAuthn atau TOTP ketat) khusus untuk akun berakses administratif (eSDM, eFinansi, PLO) guna mencegah manipulasi data berisiko tinggi sebelum terjadi insiden kebocoran data.

---

## 3. Identifikasi & Prioritas Isu-Isu Strategis (Strategic Issues)

Berdasarkan matriks TOWS, dirumuskan **4 Isu Strategis Utama** yang diurutkan berdasarkan tingkat urgensi dan dampaknya:

| No. | Isu Strategis | Deskripsi & Urgensi | Tingkat Prioritas |
|---:|---|---|---|
| **IS-1** | **Kerentanan Kata Sandi Faktor Tunggal & Password Default** | Kombinasi *Password Policy* kosong (T-06), kata sandi default berbasis NIK (U-06, U-07), dan *Verify Email* disabled (T-04) menciptakan kerentanan keamanan paling kritis yang dapat dieksploitasi kapan saja melalui *credential guessing*. | **Prioritas 1 (Paling Kritis)** |
| **IS-2** | **Penerapan Multi-Factor Authentication (MFA) Bertahap berbasis Risiko** | MFA belum diwajibkan (*Configure OTP* bukan *Default Action*, T-04). Diperlukan strategi *rollout* MFA (TOTP untuk massal, WebAuthn/FIDO2 untuk admin) yang aman namun tidak menimbulkan penolakan pengguna (*user friction*). | **Prioritas 2 (Kritis)** |
| **IS-3** | **Tingginya Beban Operasional Helpdesk & Ketiadaan Self-Service yang Aman** | Penanganan 2.624 tiket login/reset password di SMILE (D-02) membebankan tim PUSTIPANDA. Diperlukan peningkatan fitur *self-service recovery* yang aman berbasis verifikasi email. | **Prioritas 3 (Tinggi)** |
| **IS-4** | **Penguatan Tata Kelola, Retensi Log Audit, dan SOP Keamanan SSO** | Log events menumpuk tanpa batas retensi (*Expiration* kosong, T-08) dan ketiadaan dokumen SOP resmi tata kelola SSO. Diperlukan penataan kebijakan retensi log dan dokumen SOP operasional. | **Prioritas 4 (Sedang–Tinggi)** |

---

## 4. Kesimpulan M7

Matriks SWOT dan Isu Strategis M7 membuktikan secara ilmiah dan defensibel bahwa:
* Pembaruan sistem SSO UIN Jakarta **bukan sekadar memilih produk MFA**, melainkan **memperbaiki fondasi kebijakan keamanan yang lemah (Password Policy & Default Passwords)** sekaligus **mengaktifkan kapabilitas MFA bawaan Keycloak (TOTP)**.
* Keempat isu strategis (IS-1 s/d IS-4) menjadi masukan langsung untuk Analisis Gap (M8), Formulasi Strategi SI/TI (M9), dan Penyusunan Peta Jalan / Roadmap (M12).

---

## 5. Langkah Selanjutnya

Setelah M7 dikunci, tahap berikutnya adalah **Milestone 8 (M8: Gap Analysis)** untuk membandingkan secara rinci kondisi saat ini (*SSO tanpa MFA*) vs kondisi target (*SSO + MFA terproteksi*) pada aspek Teknologi, Proses, Kebijakan, Tata Kelola, SDM, dan Pengawasan.
