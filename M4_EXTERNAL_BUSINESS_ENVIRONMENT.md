# M4 — Lingkungan Bisnis Eksternal (External Business Environment)

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan analisis lingkungan bisnis eksternal UIN Syarif Hidayatullah Jakarta: konteks regulasi (UU PDP, SPBE, BSSN), lanskap ancaman siber eksternal, tren digital perguruan tinggi, serta analisis PESTEL. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan eksternal untuk formulasi strategi berikutnya.

---

## 1. Tujuan Analisis M4

1. Memetakan regulasi, hukum, dan standar nasional yang mengikat tata kelola identitas dan data pribadi sivitas akademika UIN Jakarta.
2. Menganalisis lanskap ancaman siber eksternal yang mengeksploitasi kelemahan autentikasi faktor tunggal (*single-factor authentication*).
3. Memahami tren ekosistem perguruan tinggi (*higher education trends*) dalam hal akses jarak jauh (*remote access*), mobilitas, dan layanan digital.
4. Menyusun analisis PESTEL yang disesuaikan secara khusus dengan konteks autentikasi dan SSO institusi.

---

## 2. Kerangka Regulasi & Kepatuhan Hukum (Legal & Regulatory Context)

| Regulasi / Standar | Ketentuan / Mandat Utama | Implikasi pada Sistem SSO & Autentikasi |
|---|---|---|
| **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)** | Universitas sebagai **Pengendali Data Pribadi** wajib melindungi data pribadi pengguna (NIM, NIK, nama lengkap, IP address, data akademik, data keuangan) dari akses tidak sah, kebocoran, atau pemrosesan ilegal. | Penggunaan password default NIK tanpa MFA dan tanpa Password Policy meningkatkan risiko hukum (*legal risk*) bila terjadi insiden kebocoran akun/data pribadi sivitas akademika. |
| **Perpres No. 95 Tahun 2018 tentang SPBE** | Perguruan tinggi negeri/PTN-BH sebagai bagian dari ekosistem SPBE wajib menerapkan manajemen keamanan informasi terpadu dan autentikasi yang handal. | SSO e-Semesta merupakan bagian dari infrastruktur SPBE universitas yang memerlukan penguatan kontrol akses dan keandalan identitas. |
| **Standar BSSN & ISO/IEC 27001 (A.9 Access Control)** | Mengontrol akses pengguna berdasarkan prinsip *need-to-know*, autentikasi kuat (*strong authentication*), dan manajemen kredensial yang aman. | Mewajibkan penggantian kata sandi default, penerapan kebijakan kompleksitas kata sandi, serta penggunaan Multi-Factor Authentication (MFA) untuk akun berisiko tinggi. |
| **Regulasi Kemendikbudristek / PDDikti** | Pengintegrasian data akademik perguruan tinggi ke pangkalan data nasional secara valid dan akurat. | Kerahasiaan dan integritas data mahasiswa yang ditransfer dari eRegistrasi ke eAkademik harus dilindungi oleh autentikasi SSO yang aman. |

---

## 3. Lanskap Ancaman Siber Eksternal (External Threat Landscape)

Ancaman eksternal yang menargetkan sistem autentikasi perguruan tinggi:

1. **Penyerobotan Kredensial (*Credential Guessing & Stuffing*)**:
   - Penyerang luar dapat dengan mudah memprediksi kombinasi NIK/NIM sebagai kata sandi default pengguna baru (`Mhs`+NIK untuk mahasiswa, NIK untuk dosen/tendik).
   - Ketiadaan *Password Policy* (T-06) dan *Account Lockout* memudahkan penyerang melakukan eksperimen pembongkaran kata sandi secara berulang.
2. **Serangan Menggunakan Rekayasa Sosial (*Phishing & Social Engineering*)**:
   - Kampanye *phishing* yang meniru halaman login Keycloak (`dev-sso.uinjkt.ac.id` / SSO e-Semesta) untuk mencuri kata sandi pengguna.
   - Tanpa faktor autentikasi kedua (MFA), kredensial yang tersedot *phishing* langsung dapat digunakan penyerang untuk menguasai akun.
3. **Penyalahgunaan Akses Jaringan Kampus (*Wi-Fi Hijacking*)**:
   - Akun SSO yang terkompromi dapat disalahgunakan oleh pihak luar untuk memperoleh akses internet gratis melalui Wi-Fi kampus (SSID `STAF.UINJKT.AC.ID` / `MHS.UINJKT.AC.ID`) secara berlebihan, merugikan alokasi bandwidth kampus.
4. **Manipulasi Data Akademik & Keuangan (*Data Tampering*)**:
   - Penyerobotan akun tendik atau dosen dapat mengarah pada pengubahan nilai, pengubahan status akademik, atau manipulasi informasi pembayaran pada aplikasi eFinansi/ePembayaran.

---

## 4. Tren Digital Perguruan Tinggi (Higher Education & Digital Trends)

1. **Perkuliahan Hibrida & Akses Fleksibel (*Hybrid Learning & Anywhere Access*)**:
   - Sivitas akademika membutuhkan akses ke LMS (`dev-lms`), portal riset (`eRiset`), dan perpustakaan digital dari luar area kampus tanpa mengorbankan keamanan.
2. **Mobilitas Perangkat Pengguna (*Bring Your Own Device / BYOD*)**:
   - Mahasiswa dan dosen menggunakan berbagai perangkat pribadi (laptop, *smartphone*, tablet) untuk mengakses layanan e-Semesta. Setiap akun diizinkan hingga 3 perangkat simultan pada Wi-Fi SSO.
3. **Ekspektasi Kemudahan Pengguna (*User Experience Expectation*)**:
   - Pengguna digital saat ini terbiasa dengan metode autentikasi modern yang cepat dan mudah (seperti verifikasi push notification, OTP via aplikasi, atau biometrik/Passkey).

---

## 5. Analisis PESTEL (Sistem Autentikasi SSO UIN Jakarta)

```text
+-----------------------------------------------------------------------------------+
| ANALISIS PESTEL — LINGKUNGAN EKSTERNAL AUTENTIKASI SSO                            |
+-----------------------------------------------------------------------------------+
| POLITICAL     : Kebijakan transformasi digital nasional & SPBE kementerian.      |
| ECONOMIC      : Efisiensi beban biaya operasional penanganan tiket manual.        |
| SOCIAL        : Ekspektasi keamanan & kenyamanan pengguna generasi digital.       |
| TECHNOLOGICAL: Tren evolusi MFA (TOTP, FIDO2/Passkey) & lanskap ancaman siber.    |
| ENVIRONMENTAL : Pengurangan penggunaan kertas melalui digitalisasi dokumen (PLO).|
| LEGAL         : Kepatuhan pada UU PDP No. 27/2022 & Peraturan BSSN.               |
+-----------------------------------------------------------------------------------+
```

### 5.1 Rincian Faktor PESTEL

* **Political (Politik / Kebijakan Publik)**: Dikeluarkannya Perpres SPBE dan kebijakan Kemenag/Kemendikbudristek mendorong universitas negeri memperkuat ketahanan siber dan tata kelola TI terpusat.
* **Economic (Ekonomi / Biaya Operasional)**: Insiden keamanan atau pemulihan kata sandi yang tidak efisien menimbulkan biaya operasional tersembunyi (2.624 tiket SMILE memotong jam kerja produktif staf PUSTIPANDA).
* **Social (Sosial / Budaya Pengguna)**: Keberagaman literasi digital sivitas akademika (mulai dari mahasiswa baru hingga profesor senior) menuntut solusi keamanan yang intuitif dan tidak menimbulkan penolakan (*user friction*).
* **Technological (Teknologi)**: Ketersediaan kapabilitas teknis pada Keycloak (T-01) seperti TOTP, WebAuthn/FIDO2, dan OIDC/SAML membuka peluang penerapan autentikasi modern tanpa perlu membangun sistem baru dari nol.
* **Environmental (Lingkungan)**: Digitalisasi tata kelola melalui aplikasi seperti PLO dan eAkademik mengurangi konsumsi kertas (*paperless campus*), namun meningkatkan ketergantungan pada keamanan SSO.
* **Legal (Hukum & Regulasi)**: Kebocoran data pribadi mahasiswa/pegawai akibat kelemahan kata sandi berpotensi memicu sanksi administratif dan hukum sesuai UU PDP No. 27 Tahun 2022.

---

## 6. Kesimpulan M4 & Kaitan dengan Strategi MFA

Lanskap eksternal menegaskan dua dorongan utama (*twin drivers*) untuk pembaruan sistem SSO:
1. **Dorongan Kepatuhan & Regulasi (*Mandatory Driver*)**: UU PDP dan standar BSSN mewajibkan pelindungan data pribadi yang memadai, sehingga kelemahan password default NIK dan ketiadaan MFA merupakan risiko kepatuhan yang harus segera ditangani.
2. **Dorongan Ancaman Eksternal (*Threat Driver*)**: Maraknya *phishing* dan *credential stuffing* menjadikan autentikasi faktor tunggal (kata sandi saja) tidak lagi memadai untuk melindungi 44 aplikasi digital institusi.

---

## 7. Langkah Selanjutnya

Setelah M4 dikunci, analisis lingkungan lengkap (M1–M4) akan dipadukan pada **Milestone 5 (M5: Internal IS/IT Environment)** dan **Milestone 6 (M6: External IS/IT Environment)** untuk mengevaluasi infrastruktur TI internal dan lanskap teknologi MFA.
