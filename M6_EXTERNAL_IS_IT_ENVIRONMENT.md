# M6 — Lingkungan SI/TI Eksternal (External IS/IT Environment)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan analisis lingkungan SI/TI eksternal: evaluasi objektif 5 rumpun teknologi MFA, matriks perbandingan teknis & biaya, kriteria evaluasi pemilihan MFA, serta rekomendasi netral (TOTP untuk massal, FIDO2/WebAuthn untuk admin). Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan SI/TI eksternal untuk formulasi strategi berikutnya.

---

## 1. Tujuan Analisis M6

1. Memetakan rumpun teknologi MFA yang tersedia di pasaran beserta mekanisme kerja utamanya.
2. Menganalisis kelebihan, kekurangan, dan kesesuaian (*fitment*) masing-masing rumpun teknologi MFA untuk lingkungan perguruan tinggi skala besar (~45.000 pengguna).
3. Merumuskan kriteria evaluasi pemilihan teknologi MFA berdasarkan kebutuhan teknis, anggaran, dan kemudahan pengguna UIN Jakarta.
4. Menyiapkan masukan teknis eksternal untuk proses penyusunan matriks SWOT (M7) dan analisis gap (M8).

---

## 2. Pemetaan Rumpun Teknologi MFA (MFA Technology Families)

Perbandingan objektif terhadap 5 rumpun teknologi autentikasi faktor kedua:

```text
+-----------------------------------------------------------------------------------+
| LANSKAP TEKNOLOGI MFA (M5/M6 EVALUASI EKSTERNAL)                                  |
+-----------------------------------------------------------------------------------+
| 1. TOTP (Aplikasi Authenticator)  : Standar terbuka, bebas biaya, aman, offline.  |
| 2. Push Notification              : Sangat mudah (1-tap), butuh app / lisensi.   |
| 3. FIDO2 / WebAuthn / Passkeys    : Paling aman (anti-phishing), butuh hardware/OS|
| 4. SMS / WhatsApp OTP             : Familiar, tapi BIAYA TINGGI & rentan SIM swap.|
| 5. Email OTP                      : Tanpa app tambahan, tapi rentan jika email jebol.|
+-----------------------------------------------------------------------------------+
```

### 2.1 Time-based One-Time Password (TOTP) via Authenticator Apps
* **Mekanisme**: Menggenerate kode 6-digit yang berubah setiap 30 detik berdasarkan algoritma HMAC/SHA1 (RFC 6238) yang disinkronkan antara server Keycloak dan aplikasi ponsel pengguna (misal: Google Authenticator, FreeOTP, Microsoft Authenticator).
* **Kelebihan**:
  * Standar terbuka dan **didukung penuh secara bawaan (*native*) oleh Keycloak** (T-01, T-07).
  * **Tanpa biaya lisensi atau biaya operasional kirim pesan** (bebas biaya per transaksi).
  * Berjalan secara *offline* tanpa memerlukan koneksi internet/pulsa pada ponsel pengguna saat menggenerate kode.
* **Kelemahan**: Pengguna wajib mengunduh aplikasi *authenticator* pada *smartphone*; membutuhkan proses pendaftaran awal (*enrollment*) via QR code.

### 2.2 Push Notification (Mobile App Approval)
* **Mekanisme**: Server mengirimkan notifikasi *pop-up* ke aplikasi seluler terdaftar. Pengguna cukup menekan tombol "Approve" atau memasukkan angka persetujuan pada ponsel.
* **Kelebihan**: Kemudahan penggunaan (*usability*) sangat tinggi; mengurangi kesalahan pengetikan kode.
* **Kelemahan**: Membutuhkan pengembangan/pemeliharaan aplikasi seluler khusus institusi atau berlangganan layanan *cloud MFA*; berpotensi menimbulkan *MFA fatigue* (pengguna asal menekan *approve*).

### 2.3 FIDO2 / WebAuthn / Passkeys / Hardware Security Keys
* **Mekanisme**: Menggunakan kunci kriptografi asimetris berbasis standar W3C/FIDO2. Dapat berupa perangkat fisik USB/NFC (misal: YubiKey) atau biometrik bawaan perangkat (*platform authenticators* seperti Windows Hello, TouchID/FaceID).
* **Kelebihan**: **Tingkat keamanan tertinggi**; sepenuhnya tahan terhadap serangan *phishing* dan *man-in-the-middle* (MitM) karena kredensial terikat pada domain asli.
* **Kelemahan**: Pengadaan *hardware key* fisik membutuhkan biaya tinggi per unit; dukungan perangkat/browser pada komputer lama pengguna bervariasi.

### 2.4 SMS OTP / WhatsApp OTP
* **Mekanisme**: Server mengirimkan kode OTP berupa teks melalui jaringan seluler (SMS) atau aplikasi perpesanan (WhatsApp).
* **Kelebihan**: Sangat familiar bagi seluruh lapisan pengguna; tidak membutuhkan aplikasi tambahan.
* **Kelemahan**: **Biaya operasional sangat membengkak (*high recurring cost*)** untuk 45.000+ pengguna (biaya SMS per kirim); rentan serangan *SIM swapping*, *GSM interception*, dan kendala sinyal seluler di area kampus tertentu.

### 2.5 Email OTP
* **Mekanisme**: Kode OTP dikirimkan ke alamat email terdaftar pengguna.
* **Kelebihan**: Pengguna tidak memerlukan aplikasi *authenticator* terpisah.
* **Kelemahan**: Memiliki ketergantungan melingkar (*circular dependency*); jika email kampus pengguna dibobol atau menggunakan kata sandi yang sama dengan SSO, faktor kedua menjadi sia-sia.

---

## 3. Matriks Perbandingan Teknologi MFA

| Kriteria Evaluasi | TOTP (Authenticator App) | Push Notification | FIDO2 / WebAuthn | SMS / WA OTP | Email OTP |
|---|---|---|---|---|---|
| **Tingkat Keamanan** | Tinggi | Tinggi | Sangat Tinggi (Anti-Phishing) | Sedang (Rentan SIM Swap) | Rendah–Sedang |
| **Resistensi Phishing** | Sedang | Tinggi | Sangat Tinggi | Rendah | Rendah |
| **Biaya Pengadaan & Operasional** | **Sangat Rendah (Gratis/Nir-biaya)** | Sedang–Tinggi | Tinggi (bila beli hardware) | **Sangat Tinggi (Biaya SMS berulang)** | Sangat Rendah |
| **Kemudahan Pengguna (Usability)** | Baik | Sangat Baik | Sangat Baik | Sangat Baik | Baik |
| **Ketergantungan Jaringan Seluler** | **Tidak Ada (Bisa Offline)** | Butuh Internet | Tidak Ada / Lokal | Butuh Sinyal Seluler | Butuh Internet |
| **Dukungan Bawaan Keycloak** | **Sudah Tersedia (Ready, T-01)** | Butuh SPI/Custom | Sudah Tersedia (T-01) | Butuh Custom SPI & Gateway | Butuh Email Server |
| **Kesesuaian Skala UIN (45rb User)** | **Sangat Sesuai** | Sesuai | Sesuai (untuk Admin/Privileged) | Tidak Sesuai (Anggaran) | Kurang Sesuai |

---

## 4. Kriteria Pemilihan Teknologi MFA UIN Syarif Hidayatullah Jakarta

Berdasarkan analisis kebutuhan internal (M3, M5) dan regulasi eksternal (M4), kriteria pemilihan teknologi MFA bagi UIN Jakarta ditetapkan sebagai berikut:

1. **Efisiensi Anggaran Berkelanjutan (*Cost Sustainability*)**: Solusi tidak boleh membebani anggaran operasional bulanan universitas dengan biaya per-transaksi pesan (seperti SMS OTP).
2. **Kesesuaian Kapabilitas Platform (*Keycloak Native Alignment*)**: Mengutamakan teknologi yang sudah didukung secara *native* oleh Keycloak SSO (seperti TOTP dan WebAuthn) untuk meminimalkan kustomisasi rumit.
3. **Pengalaman Pengguna yang Intuitif (*Low User Friction*)**: Memastikan alur registrasi (*enrollment*) dan autentikasi mudah dipahami oleh mahasiswa maupun dosen tanpa menghambat aktivitas akademik.
4. **Resistensi Keamanan terhadap Phishing (*Security Posture*)**: Mampu melindungi akun berwewenang tinggi (admin/tendik/dosen) dari serangan *credential theft*.
5. **Independensi Akses (*Offline Capability*)**: Dapat digunakan meskipun sinyal seluler di dalam gedung kampus kurang stabil.

---

## 5. Kesimpulan M6

Analisis SI/TI eksternal M6 menyimpulkan bahwa:
* **TOTP berbasis Aplikasi Authenticator (Google Authenticator / FreeOTP)** merupakan opsi paling ideal sebagai **MFA standar untuk massal (mahasiswa, dosen, tendik)** karena bebas biaya operasional, berjalan *offline*, dan didukung langsung oleh Keycloak.
* **FIDO2 / WebAuthn (Passkeys / Biometrik / Hardware Keys)** dapat dipertimbangkan sebagai opsi **MFA tingkat tinggi untuk akun berisiko tinggi (*privileged/admin accounts*)** untuk memberikan pelindungan maksimal dari serangan *phishing*.
* **SMS / WhatsApp OTP TIDAK DIREKOMENDASIKAN** untuk penggunaan massal karena potensi pembengkakan anggaran operasional yang tidak berkelanjutan bagi institusi.

---

## 6. Langkah Selanjutnya

Setelah M6 dikunci, seluruh hasil analisis lingkungan (M1 s/d M6) akan diintegrasikan pada **Milestone 7 (M7: SWOT & Strategic Issues)** untuk menyusun matriks SWOT dan mengidentifikasi isu-isu strategis utama.
