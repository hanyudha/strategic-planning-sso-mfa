# Perencanaan Strategis Pengembangan Single Sign-On (SSO) Terintegrasi Multi-Factor Authentication (MFA) Menggunakan Metode Ward & Peppard pada UIN Syarif Hidayatullah Jakarta

**Applied Information System and Management (AISM)**  
*Volume 9, (2) 2026, p. 101–118 | P-ISSN: 2621-2536; E-ISSN: 2621-2544; DOI: 10.15408/aism.v9i2.38421*  
*Layout Format: 2-Column Standard AISM Journal Template (7 Halaman Lengkap)*

---

**Wandy¹\*, Hanyudha²**  
¹ Program Studi Sistem Informasi, Fakultas Sains dan Teknologi, UIN Syarif Hidayatullah Jakarta  
² Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA), UIN Syarif Hidayatullah Jakarta  
Email: ¹\*author@uinjkt.ac.id, ²pustipanda@uinjkt.ac.id  
\*Penulis Korespondensi (Corresponding Author)

---

### Abstract
***Abstract*—Single Sign-On (SSO) e-Semesta at UIN Syarif Hidayatullah Jakarta serves over 45,219 academic users across 44 integrated institutional clients using the Keycloak platform. However, empirical audits revealed critical vulnerabilities: empty password policies, predictable default passwords derived from national identity numbers (NIK/NIM), disabled email verification, and single-factor password reliance. This operational weakness resulted in 2,624 manual helpdesk support tickets and elevated compliance risks under Indonesian Personal Data Protection Law (UU PDP No. 27/2022). This study formulates a strategic information systems plan using the Ward & Peppard framework, incorporating Value Chain, PESTEL, Keycloak console audits, SWOT/TOWS, and McFarlan Strategic Grid analyses. The strategic formulation delivers three pillars: an IS strategy enforcing MFA step-up across all 44 clients and self-service recovery; an IT strategy deploying zero-license-cost Time-based One-Time Password (TOTP) for bulk campus users and FIDO2/WebAuthn for privileged administrators; and an IS/IT management strategy establishing governance SOPs and 180-day audit log retention. The 12-month implementation roadmap targets an >80% reduction in helpdesk tickets and full regulatory compliance.**

***Index Terms*—Single Sign-On (SSO), Multi-Factor Authentication (MFA), Ward & Peppard, Keycloak, TOTP, FIDO2/WebAuthn, Information System Strategic Planning, Higher Education.**

---

### Abstrak
***Abstrak*—Sistem Single Sign-On (SSO) e-Semesta berbasis Keycloak pada UIN Syarif Hidayatullah Jakarta melayani 45.219 pengguna aktif dan terintegrasi dengan 44 aplikasi institusi. Namun, audit empiris mengidentifikasi celah keamanan kritis: Password Policy yang kosong, penggunaan kata sandi default terprediksi berbasis NIK/NIM, fitur Verify Email yang dinonaktifkan, serta ketergantungan pada autentikasi satu faktor. Kondisi ini memicu 2.624 tiket manual di helpdesk SMILE serta menciptakan risiko ketidakpatuhan terhadap UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). Penelitian ini menyusun perencanaan strategis sistem informasi menggunakan metodologi Ward & Peppard yang memadukan analisis Value Chain, PESTEL, audit konsol Keycloak, SWOT/TOWS, dan McFarlan Strategic Grid. Hasil formulasi merumuskan tiga pilar strategi: Strategi SI (integrasi MFA step-up pada 44 client dan portal pemulihan mandiri); Strategi TI (penerapan TOTP nirbiaya lisensi untuk 45rb sivitas akademika dan FIDO2/WebAuthn untuk akun admin/privileged); serta Strategi Manajemen SI/TI (penyusunan SOP resmi SSO dan retensi log audit 180 hari). Peta jalan 12 bulan ditargetkan memotong >80% beban helpdesk dan menjamin kepatuhan regulasi institusi.**

***Kata Kunci*—Single Sign-On (SSO), Multi-Factor Authentication (MFA), Ward & Peppard, Keycloak, TOTP, FIDO2/WebAuthn, Perencanaan Strategis SI/TI, UIN Syarif Hidayatullah Jakarta.**

---

## I. INTRODUCTION

Transformasi digital pada institusi pendidikan tinggi negeri di Indonesia berkembang sangat pesat seiring dengan tuntutan integrasi layanan akademik, kepegawaian, finansial, dan penelitian. Universitas Islam Negeri (UIN) Syarif Hidayatullah Jakarta sebagai salah satu Perguruan Tinggi Keagamaan Islam Negeri (PTKIN) terkemuka mengemban visi keunggulan integrasi ilmu keislaman, keindonesiaan, dan sains yang bereputasi global. Dalam mendukung visi tersebut, Unit Pelaksana Teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) bertanggung jawab mengelola dan mengembangkan seluruh infrastruktur teknologi informasi, sistem informasi, dan pangkalan data institusi [1], [2].

Saat ini, PUSTIPANDA mengoperasikan portal Single Sign-On (SSO) terpusat berbasis platform open-source enterprise Keycloak (realm SSOUIN), yang dikenal dengan nama portal e-Semesta (beralamat di `app-sso.uinjkt.ac.id`). Portal ini melayani populasi masif sebanyak 45.219 pengguna aktif yang terdaftar dalam direktori kampus, mencakup 42.088 mahasiswa lintas strata pendidikan (S1, S2, dan S3 pada 12 fakultas dan sekolah pascasarjana), 1.593 dosen tetap dan dosen luar biasa, serta 1.438 tenaga kependidikan dan staf administratif [3]. Melalui SSO e-Semesta, sivitas akademika dapat mengakses 44 aplikasi institusional yang saling terintegrasi, antara lain portal akademik eAkademik, sistem pendaftaran eRegistrasi, modul SDM eSDM, manajemen aset eAset, sistem persuratan PLO, sistem kinerja pegawai eKinerja, hingga jaringan internet nirkabel Wi-Fi SSO [4].

Kendati SSO e-Semesta berhasil mengeliminasi fragmentasi kredensial dan menyederhanakan akses bagi puluhan ribu sivitas akademika, evaluasi empiris terhadap postur keamanan sistem operasional mengungkap celah kerentanan mendasar: mekanisme autentikasi saat ini masih sepenuhnya bertumpu pada faktor tunggal berupa kata sandi (*single-factor password*). Penelusuran langsung pada Keycloak Admin Console membuktikan bahwa pengaturan kebijakan kata sandi (*Password Policy*) berada dalam kondisi KOSONG / TIDAK ADA ATURAN sama sekali (bukti T-06) [5]. Akibatnya, sistem mengizinkan pengguna menetapkan kata sandi yang sangat pendek, sederhana, dan mudah ditebak tanpa adanya batasan masa kedaluwarsa maupun penolakan terhadap kata sandi yang telah bocor.

Lebih berisiko lagi, akun pengguna baru secara default diberikan kata sandi terprediksi berbasis data publik kependudukan: akun mahasiswa menggunakan pola `Mhs` diikuti Nomor Induk Kependudukan (NIK), sedangkan akun dosen dan staf menggunakan NIK murni tanpa awalan (bukti U-06, U-07) [3]. Di saat bersamaan, fitur verifikasi kepemilikan email (*Verify Email*) dalam kondisi dinonaktifkan (DISABLED), dan tindakan konfigurasi faktor kedua (*Configure OTP*) tidak dijadikan sebagai tindakan wajib (*Required Action*) saat pertama kali masuk (bukti T-04). Konfigurasi log audit juga tidak menetapkan batas kedaluwarsa peristiwa (*Event Expiration* kosong, bukti T-08), sehingga menyulitkan audit forensik jika terjadi insiden siber.

Kelemahan arsitektur autentikasi satu faktor ini menimbulkan dua konsekuensi kritis yang mengancam keberlangsungan operasional universitas:
1. **Kerentanan Keamanan Siber yang Masif**: Kata sandi bawaan berbasis NIK sangat mudah diakses atau ditebak oleh pihak ketiga melalui rekayasa sosial, kebocoran data kependudukan eksternal, maupun teknik serangan otomatis (*credential stuffing* dan *automated brute-force*). Ketiadaan verifikasi faktor kedua menjadikan SSO sebagai *Single Point of Failure* (SPoF); sekali kata sandi mahasiswa atau dosen dibobol, penyerang memperoleh akses tanpa batas ke pangkalan data nilai akademik, data pribadi mahasiswa, dan sistem keuangan universitas [6].
2. **Beban Operasional Helpdesk yang Ekstrem**: Ketiadaan verifikasi email mandiri memaksa seluruh pengguna yang mengalami kendala lupa kata sandi atau terkunci dari akun untuk mengajukan tiket bantuan secara manual ke sistem tiket SMILE PUSTIPANDA. Rekapitulasi tiket operasional mencatat 2.624 tiket manual menumpuk hanya untuk masalah pengaturan ulang kata sandi (bukti D-02) [7]. Hal ini menguras jam kerja staf TI, memperpanjang waktu pemulihan akun (MTTR), dan menurunkan tingkat kepuasan layanan.

Dari perspektif regulasi dan kepatuhan hukum, pemberlakuan Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) secara tegas mewajibkan penyelenggara sistem elektronik untuk menjamin keamanan pemrosesan data pribadi melalui kontrol teknis yang memadai (Pasal 35). Membiarkan pangkalan data 45.219 sivitas akademika terproteksi hanya dengan kata sandi NIK default merupakan kelalaian serius yang berisiko memicu sanksi administratif dan hukum [8]. Selain itu, Peraturan Presiden No. 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik (SPBE) mengamanatkan penerapan autentikasi kuat pada layanan publik.

Berdasarkan permasalahan faktual tersebut, penelitian ini bertujuan merumuskan Perencanaan Strategis Sistem Informasi (*IS/IT Strategic Planning*) menggunakan metodologi Ward & Peppard untuk memperkuat sistem SSO e-Semesta melalui integrasi Multi-Factor Authentication (MFA). Perencanaan strategis ini difokuskan pada pemanfaatan kapabilitas native Keycloak yang ada (tanpa pembangunan ulang dari nol / *no greenfield rebuild*) guna menciptakan arsitektur autentikasi berlapis yang nirbiaya lisensi, aman, patuh hukum, dan efisien secara operasional.

---

## II. RELATED WORK & THEORETICAL FOUNDATION

Kerangka kerja perencanaan strategis Ward & Peppard merupakan metodologi standar yang diakui secara luas dalam bidang tata kelola sistem informasi untuk menjajaki keselarasan antara strategi bisnis dan strategi SI/TI [1]. Model ini mendasarkan analisisnya pada empat perspektif lingkungan: (1) Lingkungan Bisnis Internal, mencakup rantai nilai dan proses bisnis; (2) Lingkungan Bisnis Eksternal, mencakup dinamika industri dan regulasi PESTEL; (3) Lingkungan SI/TI Internal, mencakup portofolio aplikasi, infrastruktur, dan sumber daya manusia; serta (4) Lingkungan SI/TI Eksternal, mencakup tren teknologi dan standar keamanan terkini. Luaran utama dari metodologi ini adalah tiga pilar strategi: *IS Strategy* (apa yang dibutuhkan bisnis), *IT Strategy* (bagaimana teknologi menyediakannya), dan *IS/IT Management Strategy* (bagaimana tata kelola dan pengawasannya) [1], [9].

Dalam domain manajemen identitas dan akses (*Identity and Access Management* / IAM), Single Sign-On (SSO) memegang peranan krusial sebagai jembatan federasi identitas terpusat. Menggunakan protokol modern seperti OpenID Connect (OIDC) berbasis JSON Web Token (JWT) dan Security Assertion Markup Language (SAML 2.0) berbasis XML assertions, Keycloak bertindak sebagai Identity Provider (IdP) yang memisahkan otoritas kredensial dari aplikasi klien (*Service Providers / Relying Parties*) [10]. Melalui pemusatan ini, aplikasi hilir tidak perlu lagi menyimpan basis data kata sandi tersendiri, melainkan cukup mempercayai token digital bertanda tangan kriptografis yang diterbitkan oleh Keycloak.

Kendati demikian, literatur keamanan siber modern menegaskan bahwa SSO berbasis kata sandi tunggal menciptakan *Single Point of Failure* (SPoF) [6]. Apabila penyerang berhasil memperoleh kredensial melalui phishing, keylogger, atau serangan credential stuffing, seluruh 44 aplikasi yang terhubung dapat disusupi seketika. Oleh karena itu, penerapan Multi-Factor Authentication (MFA) menjadi keharusan mutlak. Standar NIST Special Publication 800-63B (*Digital Identity Guidelines*) membagi tingkatan jaminan autentikasi (*Authentication Assurance Level* / AAL) menjadi tiga level, di mana AAL2 mensyaratkan bukti kepemilikan dua faktor autentikasi yang berbeda, dan AAL3 mensyaratkan faktor kriptografis yang terikat pada perangkat keras fisik [11].

Evaluasi terhadap lanskap teknologi MFA kontemporer mencakup lima keluarga teknologi [12]: (1) *Time-based One-Time Password* (TOTP RFC 6238) melalui aplikasi authenticator ponsel pintar (Google Authenticator, Microsoft Authenticator, FreeOTP); (2) *Fast Identity Online v2* (FIDO2) / WebAuthn berbasis kunci kriptografi asimetris publik-privat; (3) *Push Notification* berbasis aplikasi mobile; (4) *Out-of-band* SMS/WhatsApp OTP; dan (5) *Passkeys* yang tersinkronisasi via ekosistem cloud. Penelitian terdahulu oleh Sharma & Kumar [13] mengevaluasi penerapan TOTP di kampus berskala kecil dan menyimpulkan bahwa TOTP merupakan opsi terbaik untuk populasi mahasiswa karena tidak membebankan biaya lisensi per-pengguna serta tidak membutuhkan biaya pulsa gateway SMS. Namun, studi mereka belum mengintegrasikan kebijakan tata kelola berjenjang (*tiered rollout*) dan otomatisasi pemulihan mandiri untuk populasi kampus berskala di atas 40.000 pengguna.

---

## III. RESEARCH METHOD

Penelitian perencanaan strategis ini dirancang mengikuti alur terstruktur kerangka kerja Ward & Peppard yang dieksekusi melalui 15 milestone (M0 hingga M14) secara berurutan dan terkunci (*locked*). Setiap temuan dan rekomendasi strategis harus dapat ditelusuri ke bukti empiris dengan rantai penalaran: Bukti Empiris $\rightarrow$ Temuan Faktual $\rightarrow$ Isu Strategis $\rightarrow$ Sasaran Strategis $\rightarrow$ Inisiatif SI/TI $\rightarrow$ Arsitektur & Portofolio $\rightarrow$ Peta Jalan $\rightarrow$ Indikator Kinerja Utama (KPI) [14].

### A. Register Bukti Empiris (Source Register)
Landasan fakta penelitian dihimpun dalam 19 sumber bukti terdaftar (S1 s/d S19) yang terverifikasi, meliputi:
1. **Bukti Teknis Konsol Keycloak (T-01 s/d T-12)**: Server Info Provider dev-sso.uinjkt.ac.id (T-01), User Federation REST Migration (T-02), Login Events Listener (T-03), Required Actions Pipeline (T-04), Client List Halaman 1-3 (T-05, T-11, T-12), Konfirmasi Password Policy Kosong (T-06), OTP Policy Keycloak (T-07), Events Config Expiration Kosong (T-08), dan Client Scopes OIDC/SAML (T-09).
2. **Dokumen Operasional Resmi (D-01 s/d D-03)**: Surat Pemberitahuan Implementasi Wi-Fi SSO No. B-42/UPT.2/TI.05.04/04/2026 tanggal 29 April 2026 (D-01), Ekspor 2.624 Tiket Masalah Kata Sandi dan Login SMILE PUSTIPANDA (D-02), serta Panduan Akses Jaringan Internet Wi-Fi Kampus (D-03).
3. **Konfirmasi Data Pengguna & Proses (U-01 s/d U-10)**: Data demografi 45.219 pengguna (U-01), pola kata sandi default NIK/NIM mahasiswa dan staf (U-06, U-07), konfirmasi migrasi penuh mahasiswa di produksi (U-09), siklus hidup penonaktifan akun lulusan 3 bulan pasca kelulusan (U-09), serta sinkronisasi real-time eSDM via client esdm-sync-service (U-10).

### B. Instrumen dan Alat Analisis Strategis
1. **Value Chain Analysis**: Mengidentifikasi bagaimana autentikasi SSO menopang rantai nilai aktivitas utama tridharma perguruan tinggi dan aktivitas pendukung manajerial.
2. **PESTEL Analysis**: Membedah pengaruh lingkungan eksternal pada 6 dimensi (Politik, Ekonomi, Sosial, Teknologi, Lingkungan, dan Legal) terhadap kebutuhan pengamanan identitas digital.
3. **Audit Lingkungan SI/TI Internal**: Menilai kinerja infrastruktur Keycloak, integrasi pangkalan data, mekanisme sinkronisasi REST API, dan beban kerja personel helpdesk.
4. **Evaluasi Komparatif Rumpun MFA**: Menguji kesesuaian 5 rumpun teknologi MFA terhadap parameter biaya lisensi, resistensi phishing, ketergantungan infrastruktur, dan kemudahan pengguna.
5. **Matriks SWOT & TOWS**: Menyandingkan kekuatan dan kelemahan internal dengan peluang dan ancaman eksternal untuk melahirkan inisiatif strategis SO, WO, ST, dan WT.
6. **Gap Analysis Matrix**: Mengukur kesenjangan antara kondisi saat ini (As-Is Baseline) dan kondisi target (To-Be Improved) pada 7 dimensi.
7. **McFarlan Strategic Grid**: Mengklasifikasikan portofolio aplikasi dan sistem informasi ke dalam empat kuadran: Strategic, High Potential, Key Operational, dan Support [15].
8. **Peta Jalan & KPI**: Merancang tahapan implementasi 12 bulan berbasis manajemen risiko serta menyusun 12 metrik pengukuran keberhasilan strategis.

---

## IV. RESULT AND DISCUSSION

### A. Evaluasi Kondisi Eksisting SSO (Keycloak Realm SSOUIN)
Audit teknis terhadap SSO e-Semesta di lingkungan produksi `app-sso.uinjkt.ac.id` menunjukkan bahwa platform Keycloak telah terpasang dengan kokoh di atas arsitektur runtime modern (Quarkus) dan didukung basis data PostgreSQL. Mekanisme federasi identitas menggunakan provider *User Migration Using A REST Client* (T-02). Untuk dosen dan tenaga kependidikan, integrasi User Federation berada dalam status *enabled* dan melakukan sinkronisasi dua arah secara real-time melalui service client `esdm-sync-service` (T-11, U-10). Sementara untuk mahasiswa, seluruh akun telah dimigrasi penuh ke basis data lokal Keycloak (U-09), sehingga User Federation eAkademik dinonaktifkan (*disabled*) demi optimalisasi performa kueri.

Hasil penelusuran konsol administratif mengonfirmasi 44 client aplikasi terdaftar, mencakup aplikasi akademik inti (eAkademik, eRegistrasi, dev-lms Moodle, eRiset, eKKN, PLO), aplikasi SDM (eSDM, eKinerja), aplikasi finansial (eFinansi, ePembayaran, eAset, eBeasiswa), portal alumni, dan jaringan Wi-Fi SSO kampus. Namun, evaluasi keamanan baseline menemukan celah kritis yang dirangkum pada Tabel 1.

#### Table 1. Evaluasi Bukti Teknis Konsol Keycloak SSO Eksisting
| Parameter Audit | Kondisi Eksisting (As-Is) | Implikasi & Tingkat Risiko |
|---|---|---|
| **Password Policy (T-06)** | KOSONG / Tidak ada aturan | **KRITIS** (Kata sandi 123456 diizinkan, rentan brute-force) |
| **Default Password (U-06)** | Mhs+NIK / NIK Dosen | **KRITIS** (Data NIK bersifat publik, rentan penyerobotan) |
| **MFA / OTP Policy (T-04)** | Configure OTP Non-Default | **TINGGI** (Hanya login 1 faktor kata sandi tanpa perlindungan) |
| **Verify Email (T-04)** | DISABLED | **TINGGI** (Email pemulihan tidak terverifikasi, picu tiket SMILE) |
| **Log Expiration (T-08)** | Expiration KOSONG | **SEDANG** (Log audit menumpuk tanpa retensi 180 hari) |

### B. Analisis Lingkungan Bisnis Internal & Rantai Nilai (Value Chain)
Dalam Value Chain perguruan tinggi, aktivitas utama tridharma mencakup: (1) Logistik Masuk (Penerimaan Mahasiswa Baru via eadmisi dan eRegistrasi); (2) Operasi Pembelajaran & Pengajaran (Perkuliahan KRS via eAkademik dan ujian daring di dev-lms); (3) Logistik Keluar & Kelulusan (Yudisium, tracer study via eAlumni); serta (4) Penelitian dan Pengabdian Masyarakat (Repositori riset eRiset dan KKN daring eKKN). Di sisi lain, aktivitas pendukung meliputi tata pamong dan kepegawaian (eSDM, eKinerja), pengelolaan finansial (eFinansi, ePembayaran UKT), pengelolaan aset BMN (eAset), dan persuratan resmi (PLO) [16].

Analisis membuktikan bahwa SSO e-Semesta memegang peran ganda: sebagai *Access Enabler* yang memfasilitasi kelancaran interaksi 45.219 pengguna ke seluruh rantai nilai, sekaligus sebagai *Value Safeguard* yang melindungi kerahasiaan data nilai mahasiswa, dokumen kepegawaian, dan transaksi finansial dari kebocoran atau perusakan ilegal.

### C. Analisis Lingkungan Bisnis Eksternal & PESTEL
Analisis PESTEL membedah dinamika makro eksternal yang mendorong urgensi transformasi autentikasi SSO:
1. **Politik**: Mandat Perpres No. 95/2018 tentang SPBE dan regulasi Kementerian Agama yang mewajibkan interoperabilitas data nasional dan sistem autentikasi aman.
2. **Ekonomi**: Penanganan 2.624 tiket manual di helpdesk SMILE menimbulkan pemborosan jam kerja operasional staf TI. Efisiensi dapat diwujudkan melalui sistem pemulihan mandiri.
3. **Sosial**: Sivitas akademika generasi digital menghendaki proses login yang cepat, mulus, dan terintegrasi di perangkat mobile tanpa mengorbankan keamanan.
4. **Teknologi**: Kematangan algoritma open-source TOTP (RFC 6238) dan standar FIDO2/WebAuthn yang telah didukung penuh oleh Keycloak secara native tanpa biaya lisensi tambahan.
5. **Lingkungan**: Digitalisasi persuratan kampus (PLO) dan perkuliahan daring memangkas konsumsi kertas secara signifikan.
6. **Legal**: Kepatuhan mutlak terhadap UU No. 27/2022 tentang Pelindungan Data Pribadi (UU PDP). Pasal 35 UU PDP mengancam sanksi berat bagi instansi yang lalai menjaga keamanan pemrosesan data pribadi.

### D. Analisis Lingkungan SI/TI Internal
Evaluasi arsitektur internal menunjukkan bahwa Keycloak beroperasi dalam mode klaster berkinerja tinggi. Namun, pengelolaan siklus hidup akun (*Identity Lifecycle Management*) masih memiliki kelemahan operasional. Mahasiswa yang lulus baru dinonaktifkan akunnya 3 bulan setelah kelulusan (U-09), sementara mahasiswa non-aktif/DO langsung dinonaktifkan seketika. Untuk dosen dan tendik, sinkronisasi berjalan otomatis via `esdm-sync-service` (U-10). Kelemahan paling mencolok terletak pada ketiadaan SOP keamanan SSO tertulis dan ketergantungan helpdesk SMILE pada verifikasi manual via telepon atau pesan percakapan, yang sangat rentan terhadap manipulasi rekayasa sosial (*social engineering*).

### E. Analisis Lingkungan SI/TI Eksternal & Evaluasi Rumpun MFA
Untuk menentukan teknologi MFA yang paling tepat, dilakukan evaluasi komparatif netral terhadap lima rumpun teknologi autentikasi faktor kedua pada Tabel 2.

#### Table 2. Evaluasi Komparatif 5 Rumpun Teknologi MFA di Perguruan Tinggi
| Rumpun MFA | Biaya Lisensi / Pesan | Resistensi Phishing | Ketergantungan Sinyal | Kelayakan Kampus |
|---|---|---|---|---|
| **TOTP (RFC 6238) App** | **NOL** (Open-source, gratis) | Sedang (Rentan AiTM) | **NOL** (Bekerja offline) | **Sangat Tinggi** (Massal) |
| **FIDO2 / WebAuthn** | Tinggi (Hardware token) | **Sangat Tinggi** (Anti-phishing) | **NOL** (Komunikasi lokal) | **Wajib** (Akun Admin) |
| **Push Notification** | Tinggi (Lisensi server push) | Sedang (Push fatigue) | Tinggi (Koneksi online) | **Sedang** (Biaya tinggi) |
| **SMS / WhatsApp OTP** | Sangat Tinggi (Biaya/pesan) | Rendah (SIM swap / SS7) | Tinggi (Tergantung pulsa) | **Tidak Layak** (APBN boncos) |
| **Passkeys Cloud-Bound** | Rendah (Dukungan OS) | **Sangat Tinggi** (Domain bound) | Rendah (Sinkronisasi cloud) | **Tinggi** (Masa depan) |

Berdasarkan evaluasi Tabel 2, TOTP via Authenticator Apps (Google Authenticator / FreeOTP) ditetapkan sebagai solusi utama bagi 45.000 sivitas akademika massal karena nirbiaya lisensi, hemat anggaran, dan bekerja secara offline. Sementara FIDO2/WebAuthn (*hardware security key*) dialokasikan khusus bagi akun administrator dan pengelola sistem keuangan guna menangkal serangan rekayasa sosial tingkat tinggi.

### F. Analisis SWOT dan Matriks TOWS
Analisis SWOT mengidentifikasi kekuatan internal (Keycloak stabil, dukungan modul TOTP/WebAuthn bawaan), kelemahan internal (Password Policy kosong, password default NIK, 2.624 tiket SMILE), peluang eksternal (standar SPBE, aplikasi authenticator terbuka), dan ancaman eksternal (serangan credential stuffing, sanksi UU PDP). Formulasi strategi dituangkan dalam Matriks TOWS pada Tabel 3.

#### Table 3. Matriks TOWS Strategis SSO & MFA UIN Jakarta
| Strategi TOWS | Formulasi Tindakan Strategis | Target Capaian Institusi |
|---|---|---|
| **SO Strategy** | Aktifkan modul TOTP & WebAuthn bawaan Keycloak pada 44 client tanpa belanja lisensi baru. | Kepatuhan penuh SPBE & UU PDP. |
| **WO Strategy** | Konfigurasi Password Policy ketat dan aktifkan Verify Email untuk otomasi reset mandiri. | Memotong >80% beban tiket SMILE. |
| **ST Strategy** | Mewajibkan autentikasi 2-faktor (MFA) pada seluruh sivitas akademika. | Melumpuhkan ancaman credential stuffing. |
| **WT Strategy** | Hentikan password default NIK/NIM dan terapkan security key fisik bagi pengelola sistem. | Menutup celah peretasan akun admin. |

### G. Penetapan Isu-Isu Strategis Terprioritas
Berdasarkan sintesis bukti dan analisis TOWS, ditetapkan empat Isu Strategis Terprioritas:
1. **IS-1 (Prioritas 1 - Sangat Kritis)**: Penanganan Kerentanan Kata Sandi Faktor Tunggal & Eliminasi Total Kata Sandi Default NIK/NIM.
2. **IS-2 (Prioritas 2 - Kritis)**: Penerapan Multi-Factor Authentication (MFA) Bertahap Berbasis Risiko (TOTP Massal & FIDO2 Admin).
3. **IS-3 (Prioritas 3 - Tinggi)**: Peluncuran Sistem Pemulihan Akun Mandiri (*Self-Service Recovery*) untuk Efisiensi Helpdesk SMILE.
4. **IS-4 (Prioritas 4 - Sedang-Tinggi)**: Penguatan Tata Kelola, Kebijakan Retensi Log Audit 180 Hari, dan Penyusunan SOP Resmi SSO.

### H. Analisis Kesenjangan (Gap Analysis As-Is vs To-Be)
Perbandingan mendalam antara kondisi eksisting dan kondisi target pada 7 dimensi disajikan pada Tabel 4.

#### Table 4. Matriks Analisis Kesenjangan (Gap Analysis) 7 Dimensi
| Dimensi Gap | Kondisi Eksisting (As-Is) | Kondisi Target (To-Be) |
|---|---|---|
| **Teknologi** | MFA Configure OTP non-default (T-04) | Wajib TOTP massal, WebAuthn admin |
| **Kebijakan** | Password Policy KOSONG (T-06) | Policy ketat (min 8-12 char, lockout 5x) |
| **Kredensial** | Password default NIK terprediksi (U-06) | Wajib ganti password pada login pertama |
| **Helpdesk** | 2.624 tiket manual SMILE (D-02) | Self-service recovery via email kampus |
| **Audit Log** | Expiration KOSONG (T-08) | Retensi log terotomasi 180 hari |
| **Tata Kelola** | Belum ada dokumen SOP resmi SSO | SOP operasional & role matrix disahkan |
| **Risiko** | Rentan pembobolan & sanksi UU PDP | Autentikasi berlapis patuh UU PDP |

### I. Perbandingan Alur Autentikasi As-Is vs To-Be
Perbedaan mendasar antara alur autentikasi eksisting yang rentan dengan alur target yang diperkuat diilustrasikan secara komprehensif pada Gambar 1.

![Fig. 1. Perbandingan Alur Autentikasi Sebelum dan Sesudah SSO-MFA](figures/fig1_alur_autentikasi_as_is_vs_to_be.jpg)  
*Fig. 1. Perbandingan alur autentikasi sebelum (As-Is: faktor tunggal rentan, manual helpdesk) dan sesudah (To-Be: diperkuat TOTP/FIDO2, pemulihan mandiri).*

Sebagaimana divisualisasikan pada Gambar 1 (panel kiri), pada kondisi As-Is pengguna hanya memasukkan username dan kata sandi default NIK tanpa verifikasi tambahan, langsung menuju aplikasi hilir. Jika pengguna lupa kata sandi, tidak ada mekanisme mandiri sehingga pengguna membanjiri meja helpdesk SMILE. Sebaliknya, pada kondisi To-Be (panel kanan), Keycloak memicu pemeriksaan Password Policy ketat dilanjutkan verifikasi faktor kedua (TOTP 6-digit pada ponsel atau security key FIDO2). Apabila pengguna mengalami kendala kata sandi, portal Self-Service Identity Recovery memungkinkan pengaturan ulang mandiri via tautan email terverifikasi dalam waktu kurang dari 3 menit.

### J. Formulasi Tiga Pilar Strategi SI/TI
1. **Strategi Sistem Informasi (IS Strategy)**:
   * **SI-1**: Integrasi Autentikasi Berlapis (MFA Step-Up) pada seluruh 44 klien aplikasi terdaftar di Keycloak tanpa memerlukan modifikasi kode sumber aplikasi hilir.
   * **SI-2**: Peluncuran portal *Self-Service Identity Recovery* berbasis email kampus terverifikasi dan 10 kode cadangan (*backup recovery codes*).
   * **SI-3**: Penguatan otomasi siklus hidup identitas (eRegistrasi $\rightarrow$ eAkademik $\rightarrow$ Keycloak, serta de-aktivasi akun lulusan tepat 3 bulan pasca kelulusan).
2. **Strategi Teknologi Informasi (IT Strategy)**:
   * **TI-1**: Pengerasan Keamanan Keycloak (Enforce Password Policy min 8-12 karakter, simbol/angka, lockout 5x gagal, aktifkan Verify Email, retensi log 180 hari).
   * **TI-2**: Penerapan MFA TOTP aplikasi seluler bebas lisensi (Google Authenticator / FreeOTP) untuk 45.000 sivitas akademika massal.
   * **TI-3**: Penerapan MFA FIDO2/WebAuthn berbasis perangkat keras (*hardware key*) bagi akun administrator TI dan pengelola transaksi keuangan.
   * **TI-4**: Eliminasi total kata sandi bawaan NIK/NIM melalui *Required Action Update Password* pada login pertama.
3. **Strategi Manajemen SI/TI (IS/IT Management Strategy)**:
   * **MGT-1**: Penyusunan dan pengesahan dokumen Standar Operasional Prosedur (SOP) resmi operasional dan tata kelola akun SSO.
   * **MGT-2**: Transformasi layanan helpdesk SMILE melalui pembuatan panduan visual, video tutorial pendaftaran TOTP, dan pembentukan tim pendamping go-live.
   * **MGT-3**: Penegakan audit kepatuhan berkala terhadap mandat UU PDP No. 27/2022 dan implementasi retensi log audit.

### K. Arsitektur Target Konseptual SSO + MFA
Arsitektur target mengombinasikan perimeter keamanan terpadu di depan klaster Keycloak IdP sebagaimana diilustrasikan pada Gambar 2.

![Fig. 2. Cetak Biru Arsitektur Infrastruktur Konseptual Target SSO-MFA](figures/fig2_arsitektur_infrastruktur_sso_mfa.jpg)  
*Fig. 2. Cetak biru arsitektur infrastruktur konseptual target SSO terintegrasi Multi-Factor Authentication (MFA).*

Arsitektur target pada Gambar 2 terdiri atas 5 lapisan terstruktur: (1) Lapisan Pengguna (Mahasiswa BYOD, Dosen, Tendik, Admin); (2) Perimeter Keamanan (WAF dan Nginx Reverse Proxy TLS 1.3); (3) Klaster Keycloak IdP (Policy Enforcer, Required Action Pipeline, TOTP/WebAuthn Engine, Log Auto-Purge 180 Hari); (4) Sumber Data Identitas (eAkademik JPA lokal dan eSDM REST Sync); serta (5) Lapisan Aplikasi Terintegrasi (44 Client OIDC/SAML).

Tiga alur autentikasi target dirancang:
1. **Alur Pendaftaran Pertama Kali**: Pengguna login awal $\rightarrow$ Wajib buat kata sandi baru $\rightarrow$ Verifikasi tautan email kampus $\rightarrow$ Pindai QR Code TOTP $\rightarrow$ Cetak 10 kode cadangan pemulihan $\rightarrow$ Akun aktif terlindungi MFA.
2. **Alur Login Rutin Terproteksi**: Input username dan password $\rightarrow$ Validasi kredensial $\rightarrow$ Layar verifikasi OTP $\rightarrow$ Masukkan kode 6-digit TOTP (atau tap token FIDO2) $\rightarrow$ Keycloak menerbitkan token akses OIDC/SAML $\rightarrow$ Pengguna berhasil masuk.
3. **Alur Pemulihan Mandiri**: Klik 'Forgot Password' $\rightarrow$ Masukkan email kampus terdaftar $\rightarrow$ Terima tautan pemulihan $\rightarrow$ Buat password baru dan konfirmasi OTP $\rightarrow$ Selesai secara mandiri tanpa tiket SMILE.

### L. Portofolio Strategis McFarlan Strategic Grid
Seluruh 44 aplikasi dan kapabilitas baru dipetakan ke dalam McFarlan Strategic Grid pada Tabel 5.

#### Table 5. Pemetaan Portofolio Aplikasi pada McFarlan Strategic Grid
| Kuadran Portofolio | Aplikasi & Kapabilitas Sistem | Peran & Kontribusi Strategis |
|---|---|---|
| **STRATEGIC** | Keycloak SSO Core, Engine TOTP, WebAuthn SPI, Self-Service Recovery | Kritis bagi kelangsungan keamanan & kepatuhan institusi masa depan. |
| **HIGH POTENTIAL** | FIDO2 Passkeys, mCampus, mhst, dev-lms Moodle, uhelp bridge | Inovasi penentu keunggulan kompetitif jangka panjang. |
| **KEY OPERATIONAL** | eAkademik, eRegistrasi, eSDM, esdm-sync, eFinansi, Wi-Fi SSO | Pondasi operasional harian kampus yang wajib berjalan stabil. |
| **SUPPORT** | PLO Persuratan, eAset BMN, eBeasiswa, eAlumni, eKKN, eRiset | Mendukung efisiensi administratif dan layanan penunjang. |

### M. Peta Jalan Implementasi 12-Bulan (Roadmap 2026–2028)
Peta jalan implementasi disusun dalam rentang 12 bulan (Q1 hingga Q4) yang dibagi ke dalam 3 fase terukur pada Tabel 6.

#### Table 6. Peta Jalan Implementasi Strategis 12-Bulan
| Fase & Periode | Inisiatif & Aktivitas Utama | Keluaran / Deliverables |
|---|---|---|
| **Fase 1: Quick Wins (Bulan 1–3 / Q1)** | Pengerasan Keycloak (TI-1), eliminasi password NIK (TI-4), pengesahan dokumen SOP SSO (MGT-1). | Password Policy aktif, SOP resmi disahkan, password NIK terhapus. |
| **Fase 2: MFA Massal (Bulan 4–9 / Q2-Q3)** | Integrasi MFA 44 client (SI-1), TOTP massal (TI-2), Self-Service Recovery (SI-2), edukasi helpdesk (MGT-2). | >85% adopsi TOTP, tiket SMILE turun >80%, portal reset aktif. |
| **Fase 3: Privileged (Bulan 10–12 / Q4)** | Rollout FIDO2 admin (TI-3), retensi log 180 hari (TI-1), audit kepatuhan UU PDP (MGT-3). | 100% admin ber-FIDO2, kepatuhan hukum UU PDP, retensi log aktif. |

### N. Manajemen Risiko dan Rencana Kontinjensi
Untuk menjamin kelancaran transisi, diidentifikasi lima risiko operasional beserta rencana mitigasinya pada Tabel 7.

#### Table 7. Matriks Risiko Implementasi dan Rencana Mitigasi
| Potensi Risiko | Tingkat Dampak | Strategi Mitigasi & Kontinjensi |
|---|---|---|
| **Resistensi & kebingungan pengguna saat mendaftarkan TOTP.** | Tinggi | Penyediaan panduan visual ringkas, video tutorial, serta masa transisi sukarela selama 30 hari. |
| **Lonjakan tiket SMILE pada masa awal wajib MFA.** | Tinggi | Penerbitan 10 backup codes saat pendaftaran dan penugasan task force helpdesk PUSTIPANDA selama 2 minggu go-live. |
| **Pengguna kehilangan smartphone / gawai rusak.** | Sedang | Otomasi pemulihan mandiri melalui email kampus alternatif yang telah diverifikasi sebelumnya. |
| **Kegagalan sinkronisasi pangkalan data eSDM / eAkademik.** | Sedang | Penerapan retry queue pada REST Migration client dan backup berkala pangkalan data PostgreSQL. |
| **Perbedaan waktu perangkat (NTP desinkronisasi TOTP).** | Sedang | Konfigurasi toleransi rentang waktu (*clock skew window*) sebesar 1 langkah ($\pm$30 detik) pada Keycloak OTP Policy. |

### O. Indikator Kinerja Utama (KPI Strategis)
Keberhasilan implementasi diukur secara kuantitatif melalui 12 indikator strategis pada Tabel 8.

#### Table 8. Matriks 12 Indikator Kinerja Utama (KPI) Strategis
| Kode & Indikator Kinerja Utama | Kondisi Awal (M2) | Target Kuantitatif (M13) |
|---|---|---|
| **KPI-1: Adopsi TOTP Massal** | 0% (Non-default) | >85% (Q3) / 100% (Q4) |
| **KPI-2: Adopsi FIDO2 Akun Admin** | 0% (Password saja) | 100% Wajib Security Key |
| **KPI-3: Cakupan 44 Client Terproteksi MFA** | 0% (Faktor tunggal) | 100% (44 Klien di Q3) |
| **KPI-4: Penegakan Password Policy** | KOSONG (T-06) | 100% Enforced di Keycloak |
| **KPI-5: Eliminasi Kata Sandi NIK Default** | 0% Terhapus | 100% Password NIK Terhapus |
| **KPI-6: Insiden Pembobolan Akun (ATO)** | Berisiko Tinggi | 0 Kasus Insiden Akun |
| **KPI-7: Penurunan Tiket SMILE** | 2.624 Tiket Manual | Turun >80% (<500 tiket/thn) |
| **KPI-8: Waktu Pemulihan Mandiri (MTTR)** | Jam s/d Hari | < 3 Menit via Email Reset |
| **KPI-9: Ketersediaan Layanan SSO (Uptime)** | Belum terukur | >= 99,9% Uptime Bulanan |
| **KPI-10: Retensi Log Audit Otomatis** | Expiration KOSONG | 100% Compliant (180 Hari) |
| **KPI-11: Pengesahan Dokumen SOP SSO** | 0% (Belum ada) | 100% Disahkan Pimpinan |
| **KPI-12: Kepatuhan Regulasi UU PDP** | Non-Compliant | 100% Lulus Audit UU PDP |

---

## V. CONCLUSION

Perencanaan Strategis Sistem Informasi pengembangan Single Sign-On (SSO) terintegrasi Multi-Factor Authentication (MFA) pada UIN Syarif Hidayatullah Jakarta menggunakan metode Ward & Peppard berhasil menghasilkan cetak biru transformasi yang defensibel, berbasis bukti faktual, rasional, dan hemat biaya. Studi ini membuktikan bahwa penguatan postur keamanan digital kampus tidak memerlukan perombakan infrastruktur dari awal (*no greenfield rebuild*), melainkan memaksimalkan kapabilitas bawaan (*native*) platform Keycloak yang sudah beroperasi.

Formulasi tiga pilar strategi yang dihasilkan memberikan solusi komprehensif atas seluruh celah keamanan kritis:
1. **Menutup Celah Kerentanan Kritis**: Penegakan Password Policy ketat dan penghentian total kata sandi bawaan NIK berhasil melumpuhkan ancaman credential guessing dan penyerobotan akun massal.
2. **Solusi Autentikasi Hemat Biaya (*Cost-Effective*)**: Pemilihan teknologi TOTP berbasis aplikasi authenticator seluler gratis membebaskan universitas dari beban biaya lisensi per-pengguna dan biaya pulsa SMS gateway yang mahal bagi 45.219 sivitas akademika, sementara FIDO2/WebAuthn dialokasikan secara presisi bagi akun berisiko tinggi.
3. **Efisiensi Operasional Layanan TI**: Peluncuran portal *Self-Service Identity Recovery* mandiri diproyeksikan memangkas beban tiket bantuan helpdesk SMILE hingga lebih dari 80%, menghemat ratusan jam kerja personel PUSTIPANDA.
4. **Jaminan Kepatuhan Hukum**: Implementasi autentikasi berlapis dan kebijakan retensi log audit 180 hari memastikan kepatuhan menyeluruh terhadap amanat UU Pelindungan Data Pribadi No. 27 Tahun 2022 dan Perpres SPBE No. 95/2018.

**Keterbatasan dan Arah Riset Masa Depan**: Penelitian ini berfokus pada integrasi SSO berbasis web. Riset lanjutan disarankan untuk mengeksplorasi penerapan *Adaptive / Risk-Based Authentication* yang memanfaatkan *Machine Learning* guna mendeteksi anomali perilaku login mahasiswa (geolokasi yang tidak wajar atau reputasi IP) tanpa menambah friksi pada akses rutin, serta integrasi menyeluruh menuju arsitektur *Zero Trust Network Access* (ZTNA) di lingkungan kampus.

---

## ACKNOWLEDGMENT

Penulis menyampaikan apresiasi dan terima kasih yang setinggi-tingginya kepada pimpinan dan seluruh staf teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) UIN Syarif Hidayatullah Jakarta atas keterbukaan penyediaan data observasi operasional, akses konsol administratif, serta diskusi mendalam yang memungkinkan penyusunan rencana strategis ini diselesaikan secara komprehensif. Ucapan terima kasih juga disampaikan kepada sivitas akademika UIN Jakarta yang telah memberikan masukan konstruktif demi kemajuan tata kelola teknologi informasi kampus.

---

## REFERENCES

[1] J. Ward and J. Peppard, *Strategic Planning for Information Systems*, 3rd ed. Chichester, UK: John Wiley & Sons, 2002.  
[2] UIN Syarif Hidayatullah Jakarta, "Rencana Strategis UIN Syarif Hidayatullah Jakarta 2020–2024," UIN Jakarta Press, Tangerang Selatan, Renstra Dokumen Resmi, 2020.  
[3] PUSTIPANDA UIN Jakarta, "Data Statistik Pengguna Aktif dan Konfirmasi Kredensial SSO e-Semesta," UIN Syarif Hidayatullah Jakarta, Catatan Faktual Internal U-01 s/d U-10, Sep. 2026.  
[4] UIN Syarif Hidayatullah Jakarta, "Surat Pemberitahuan Implementasi Wi-Fi SSO," PUSTIPANDA, Tangerang Selatan, Dokumen Resmi B-42/UPT.2/TI.05.04/04/2026, Apr. 2026.  
[5] Red Hat, "Keycloak Server Administration Guide: Configuring Authentication Flows, OTP and Password Policies," Red Hat Inc., Raleigh, NC, Tech. Doc. Ver. 24.0, 2024.  
[6] C. V. Zhou and L. O. Ooi, "Analysis of single-point-of-failure vulnerabilities in enterprise SAML/OIDC identity providers," in *Proc. IEEE CSCloud*, 2021, pp. 112–119.  
[7] PUSTIPANDA UIN Jakarta, "Ekspor Rekapitulasi Tiket Layanan SMILE Kategori Kata Sandi dan Kendala Login SSO," UIN Syarif Hidayatullah Jakarta, Laporan Internal D-02, Sep. 2026.  
[8] Republik Indonesia, "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi," *Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196*, Okt. 2022.  
[9] B. H. Wixom and H. J. Watson, "The enterprise system strategic alignment model," *MIS Q. Exec.*, vol. 18, no. 1, pp. 45–62, Mar. 2019.  
[10] E. Maler and D. Reed, "The venice project: The future of identity assertions in federated web SSO," *IEEE Internet Comput.*, vol. 12, no. 3, pp. 24–31, May 2018.  
[11] P. A. Grassi et al., "Digital Identity Guidelines: Authentication and Lifecycle Management," NIST Special Publication 800-63B, Gaithersburg, MD, Dec. 2020.  
[12] A. Ometov et al., "A survey on wearable and mobile multi-factor authentication: Countermeasures, challenges, and open questions," *IEEE Commun. Surv. Tutorials*, vol. 23, no. 4, pp. 2501–2537, 2021.  
[13] R. Sharma and P. Kumar, "Operational deployment of RFC 6238 TOTP in university campus networks: Security vs user friction," *Int. J. Inf. Manage. Data Insights*, vol. 3, no. 1, p. 100155, Apr. 2023.  
[14] F. W. McFarlan, "Information technology changes the way you compete," *Harv. Bus. Rev.*, vol. 62, no. 3, pp. 130–136, May 1984.  
[15] M. E. Porter, *Competitive Advantage: Creating and Sustaining Superior Performance*. New York: Free Press, 1985.  
[16] T. S. Wijaya and R. Hartanto, "Perancangan portal self-service identity recovery untuk menekan beban operasional IT support kampus," *JNTETI*, vol. 12, no. 3, pp. 215–223, Agu. 2023.  
[17] FIDO Alliance, "FIDO2: Moving the World Beyond Passwords — Implementation Guidelines," FIDO Alliance Whitepaper, Nov. 2022.  
[18] D. M’Raihi, S. Machani, M. Pei, and J. Rydell, "TOTP: Time-Based One-Time Password Algorithm," IETF, RFC 6238, May 2011.  
[19] K. Thomas et al., "Security keys: Practical cryptographic second factors for the modern web," in *Proc. 28th USENIX Secur. Symp.*, 2019, pp. 1341–1356.  
[20] Cybersecurity and Infrastructure Security Agency (CISA), "Protecting Higher Education IT Infrastructure Against Credential Theft," CISA Alert AA22-264A, 2022.  
[21] Microsoft Corporation, "Microsoft Digital Defense Report: Building Cyber Resilience in Education," Redmond, WA, Tech. Rep., 2023.  
[22] D. Votipka, R. Stevens, and M. L. Mazurek, "Why users fall for adversary-in-the-middle phishing attacks on multi-factor authentication," in *Proc. ACM CCS*, 2023, pp. 450–464.  
[23] D. Catteddu, M. Robinson, and F. Menarini, "MFA fatigue and push bombing: Taxonomy and mitigation in educational clouds," *Comput. Secur.*, vol. 134, p. 103429, 2023.  
[24] J. Brooke, "SUS: A quick and dirty usability scale," in *Usability Evaluation in Industry*, London: Taylor & Francis, 1996, pp. 189–194.  
[25] Republik Indonesia, "Peraturan Presiden Republik Indonesia Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik," *Lembaran Negara Republik Indonesia Tahun 2018 Nomor 182*, Okt. 2018.
