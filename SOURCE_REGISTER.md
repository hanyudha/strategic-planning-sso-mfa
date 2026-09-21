# Source Register

## Primary supplied references

### S6 — Ekstrak teks Keycloak Admin Console Server Info Providers
**Berkas asal:** `FireShot Capture 066 - Keycloak Admin Console - dev-sso.uinjkt.ac.id.pdf`
**Berkas teks:** `Pasted text.txt`
**Kode bukti M2:** T-01
**Tanggal tangkapan/konversi:** 21 September 2026
**Konteks:** Ekstrak teks dari halaman Keycloak Admin Console bagian `Server Info` / `Providers`.

Gunakan sebagai bukti teknis M2 untuk:
- daftar provider/SPI Keycloak yang tersedia pada server;
- dukungan protokol login `saml` dan `openid-connect`;
- ketersediaan provider storage seperti `ldap`, `jpa`, `kerberos`, dan migrasi user via REST client;
- ketersediaan provider credential seperti password, OTP, WebAuthn, dan WebAuthn passwordless;
- ketersediaan required action seperti `CONFIGURE_TOTP`, `VERIFY_EMAIL`, `UPDATE_PASSWORD`, dan `UPDATE_PROFILE`;
- ketersediaan provider event listener/store seperti `jboss-logging`, `email`, dan `jpa`; dan
- penggunaan komponen umum Keycloak seperti Infinispan dan JPA/Quarkus.

Jangan gunakan bukti ini untuk menyimpulkan bahwa LDAP, OTP, WebAuthn, email event, atau suatu protokol tertentu sudah aktif pada realm/aplikasi tertentu. Halaman `Providers` menunjukkan kapabilitas/provider yang tersedia, bukan konfigurasi aktif, policy aktif, nilai secret, atau status integrasi setiap client.

### S5 — Panduan penggunaan jaringan internet kampus Wi-Fi SSO
**Berkas:** `Panduan_Penggunaan_Jaringan_Internet_Kampus_Wi_Fi_SSO_UIN_Jakarta.pdf`
**Kode bukti M2:** D-03
**Penerbit/konteks:** PUSTIPANDA UIN Syarif Hidayatullah Jakarta
**Metadata dokumen:** dibuat 28 April 2026; dimodifikasi 29 April 2026

Gunakan sebagai bukti pendukung M2 untuk:
- alur akses Wi-Fi kampus melalui SSID mahasiswa dan staf;
- kelompok pengguna Wi-Fi SSO;
- batas tiga perangkat simultan per akun;
- kebutuhan autentikasi ulang setelah disconnected lebih dari 60 menit;
- alur reset password mandiri melalui menu `Forgot Password`; dan
- kanal serta jam layanan bantuan yang ditampilkan dalam panduan.

Jangan mereplikasi pola kredensial awal/default secara berlebihan ke dokumen akademik. Cukup jelaskan bahwa pola tersebut tersedia pada panduan resmi dan perlu dievaluasi dari sisi keamanan pada analisis berikutnya.

### S4 — Ekspor tiket kata sandi dan masalah login
**Berkas:** `Advanced Search Tickets - 20260921.csv`
**Sistem sumber:** SMILE, berdasarkan keterangan pengguna
**Tanggal ekspor:** 21 September 2026
**Rentang aktual `Date Created`:** 1 Januari 2026 sampai 21 September 2026

Gunakan sebagai bukti operasional agregat untuk:
- volume tiket yang dikumpulkan pengguna sebagai tiket kata sandi atau masalah login;
- distribusi waktu pembuatan tiket;
- status tiket pada saat ekspor; dan
- keterbatasan metadata SLA yang tersedia pada ekspor.

Jangan mereplikasi identitas pelapor, alamat surel, nomor tiket, atau isi subjek tiket ke dokumen akademik. Kolom SLA kosong pada ekspor, sehingga data ini tidak cukup untuk menyimpulkan kepatuhan SLA satu hari kerja.

### S3 — Surat pemberitahuan implementasi Wi-Fi SSO
**Nomor:** B-42/UPT.2/TI.05.04/04/2026
**Tanggal:** 29 April 2026
**Penerbit:** UPT Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA), UIN Syarif Hidayatullah Jakarta
**Perihal:** Pemberitahuan implementasi Single Sign-On (SSO) untuk akses Wi-Fi kampus

Gunakan sebagai bukti primer kasus untuk:
- penerapan SSO pada akses Wi-Fi kampus mulai 1 Mei 2026;
- kelompok pengguna yang dicakup oleh layanan Wi-Fi SSO;
- ketentuan penggunaan Wi-Fi SSO dan batas perangkat simultan; serta
- saluran dukungan yang disebutkan dalam surat/lampiran.

Surat ini membuktikan konteks dan tanggal penerapan **Wi-Fi SSO**, tetapi tidak membuktikan tanggal awal SSO untuk seluruh aplikasi terintegrasi maupun arsitektur SSO secara menyeluruh.

### S1 — Ward & Peppard example paper
**Title:** Perencanaan Strategis Pada Sistem Informasi dengan Menggunakan Metode Ward and Peppard  
**Authors:** Brian Farrel Hermanto; Andeka Rocky Tanaamah  
**Journal:** Jurnal Sistem Komputer dan Informatika (JSON)  
**Volume/Issue:** Vol. 3, No. 2, December 2021  
**Pages:** 155–163  
**DOI:** 10.30865/json.v3i2.3634

Use this source primarily as a structural/example reference for:
- Ward & Peppard framework
- SWOT
- Value Chain
- IS architecture
- Technology architecture
- McFarlan Strategic Grid
- implementation planning

It is a case study of CV. Bumi Printing and must not be treated as factual evidence about the university SSO case.

### S2 — Tugas 2
A two-page supplied document summarizing:
- Internal Business Environment
- External Business Environment
- Internal IS/IT Environment
- External IS/IT Environment
- Business Strategy
- IS Strategy
- IT Strategy
- IS/IT Management Strategy
- SWOT
- PESTEL
- Value Chain
- Porter Five Forces
- McFarlan Strategic Grid
- CSF
- expected IS/IT planning outputs

Use this as course/template context.

### S7 — Screenshot Keycloak Admin Console: User Federation
**Kode bukti M2:** T-02
**Realm:** SSOUIN
**Lingkungan:** Development (`dev-sso.uinjkt.ac.id`)
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Daftar User Federation pada realm SSOUIN. Menunjukkan 16 entry yang seluruhnya menggunakan provider "User Migration Using A REST Client"; hanya eSDM yang enabled.

Gunakan sebagai bukti teknis M2 untuk mekanisme sinkronisasi identitas dan sumber user aktif. Bukti berasal dari lingkungan development; konfigurasi produksi perlu divalidasi.

### S8 — Screenshot Keycloak Admin Console: Events (Login Events)
**Kode bukti M2:** T-03
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Tab Login Events menampilkan event LOGIN_ERROR dengan field Time, Event Type, Client, User, IP Address, Error, dan Details.

Gunakan sebagai bukti bahwa Login Events aktif dan mencatat event. Konfigurasi event (retensi, scope, admin events) perlu bukti tambahan dari tab Config.

### S9 — Screenshot Keycloak Admin Console: Authentication > Required Actions
**Kode bukti M2:** T-04
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Daftar Required Actions menunjukkan Configure OTP dan Terms and Conditions enabled (bukan default); Update Password enabled dan default; Verify Email, Update Profile, Delete Account, dan Update User Locale tidak enabled. WebAuthn registration tidak muncul dalam daftar.

Gunakan sebagai bukti status kesiapan MFA dan kebijakan aksi wajib pengguna.

### S10 — Screenshot Keycloak Admin Console: Clients
**Kode bukti M2:** T-05
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Daftar client pada realm SSOUIN menampilkan 18+ client (list terpotong). Domain SSO: `dev-sso.uinjkt.ac.id`; domain aplikasi mayoritas `devel.uinjkt.ac.id`. Terdapat beberapa client baru yang belum ada di inventaris M1.

Gunakan sebagai bukti inventaris integrasi SSO. Daftar client terpotong dan berasal dari lingkungan development; kelengkapan dan konfigurasi produksi perlu divalidasi.

### S11 — Konfirmasi Password Policy kosong
**Kode bukti M2:** T-06
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal:** 21 September 2026
**Konteks:** Pengguna mengonfirmasi bahwa tab Password Policy pada Authentication tidak memiliki aturan yang diterapkan (kosong). Tidak ada kebijakan panjang, kompleksitas, history, expiration, atau lockout yang dikonfigurasi pada Keycloak.

### S12 — Screenshot Keycloak Admin Console: Authentication > OTP Policy
**Kode bukti M2:** T-07
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Konfigurasi OTP Policy: OTP Type = Time Based (TOTP), Hash Algorithm = SHA1, Number of Digits = 6, Look Around Window = 1, OTP Token Period = 30, Supported Applications = FreeOTP dan Google Authenticator. Ini merupakan konfigurasi default Keycloak.

### S13 — Screenshot Keycloak Admin Console: Events > Config
**Kode bukti M2:** T-08
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Event Listeners: jboss-logging. Login Events: Save Events ON, Saved Types mencakup hampir seluruh event type Keycloak (LOGIN, LOGOUT, REGISTER, UPDATE_PASSWORD, RESET_PASSWORD, LOGIN_ERROR, dan puluhan lainnya), Expiration tidak diisi (kosong). Admin Events: Save Events ON, Include Representation OFF.

Gunakan sebagai bukti konfigurasi logging. Seluruh event type utama dicatat. Retensi (Expiration) tidak dikonfigurasi, yang berarti event mungkin menumpuk tanpa batas atau mengikuti default Keycloak. Admin Events juga aktif.

### S14 — Screenshot Keycloak Admin Console: Client Scopes
**Kode bukti M2:** T-09
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Daftar Client Scopes menunjukkan 10 scope aktif yang mayoritas menggunakan protokol openid-connect (acr, address, email, mapper, microprofile-jwt, offline_access, phone, profile, roles, web-origins) dan satu scope menggunakan protokol saml (role_list).

Gunakan sebagai bukti bahwa Client Scopes didominasi OpenID Connect, bukan SAML. Scope `mapper` tampak sebagai scope kustom (bukan bawaan standar Keycloak).

### S15 — Screenshot Keycloak Admin Console: Clients Halaman 2
**Kode bukti M2:** T-11
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Halaman 2 daftar Clients menampilkan 20 client tambahan: eRegistrasi, eRegistrasiSKI, eRiset, eRisetPostgreSki, eSDM, esdm-sync-service, eSPMI, http://staff1.uinjkt.ac.id:1000/remote/saml/metadata/, local-api, local-cms-uinjkt, local-eAkademik, local-paper-ess, local-sso-soa (disabled), mCampus, mhst, PLO, realm-management, reg-wifi-local, security-admin-console, SKIeKKNLocal. Semua enabled kecuali local-sso-soa.

Temuan penting: (1) eSDM terkonfirmasi sebagai client dengan Base URL `devel.uinjkt.ac.id/client/ski-esdm`; (2) `esdm-sync-service` membuktikan mekanisme sinkronisasi eSDM→Keycloak; (3) client SAML `http://staff1.uinjkt.ac.id:1000/remote/saml/metadata/` membuktikan integrasi SAML aktif; (4) PLO memiliki URL `plo.uinjkt.ac.id` (tanpa prefix dev); (5) eKinerja dan CMS Website tidak ditemukan.

### S16 — Screenshot Keycloak Admin Console: Clients Halaman 3 (terakhir)
**Kode bukti M2:** T-12
**Realm:** SSOUIN
**Lingkungan:** Development
**Tanggal tangkapan:** 21 September 2026
**Konteks:** Halaman 3 (terakhir) menampilkan 4 client: sso (Base URL `app-sso.uinjkt.ac.id/`), ssotesting (disabled, `sso-uinjkt.test`), uhelp sso admin (Not defined), uhelp sso bridge (Not defined).

Total client realm SSOUIN: 44 client di 3 halaman. Inventaris lengkap.

### S17 — Pola Password Default Mahasiswa
**Kode bukti M2:** U-06
**Sumber:** Pengguna (data percakapan)
**Tanggal:** 21 September 2026
**Konteks:** Password default mahasiswa menggunakan pola `Mhs` + NIK. Contoh: jika NIK = 123456789, password default = `Mhs123456789`. Username mahasiswa adalah NIM. Ini bersifat **informasi sensitif** yang menunjukkan pola yang dapat diprediksi. Update Password sebagai Default Action meminta penggantian saat login pertama.

### S18 — Migrasi Mahasiswa dan Siklus Hidup Akun Mahasiswa (Pembuatan & Penonaktifan Otomatis)
**Kode bukti M2:** U-09
**Sumber:** Pengguna (data percakapan)
**Tanggal:** 21 September 2026
**Konteks:** Konfirmasi faktual pengguna mengenai 3 aspek akun mahasiswa:
1. **Migrasi penuh:** Pada SSO produksi, seluruh mahasiswa telah dimigrasi ke Keycloak (menjelaskan mengapa User Federation eAkademik/mahasiswa dalam status disabled).
2. **Alur pembuatan akun baru:** Ketika status CALON MAHASISWA di eRegistrasi berubah menjadi MAHASISWA, trigger event (click/sync) di eRegistrasi mentransfer data ke eAkademik. Data yang masuk ke eAkademik secara otomatis mengaktifkan akun SSO mahasiswa.
3. **Penonaktifan otomatis:** Terdapat fitur otomatis yang mengubah status akun SSO mahasiswa berstatus LULUS menjadi DISABLE secara otomatis 3 bulan setelah kelulusan.

### S19 — Mekanisme Sync Realtime eSDM dan Kebijakan Penonaktifan Langsung untuk Status Nonaktif/Dropout
**Kode bukti M2:** U-10
**Sumber:** Pengguna (data percakapan)
**Tanggal:** 21 September 2026
**Konteks:** Konfirmasi faktual pengguna mengenai 2 poin operasional tambahan:
1. **Mekanisme Sinkronisasi eSDM:** Sinkronisasi data eSDM ke Keycloak (melalui `esdm-sync-service`) berjalan secara **real-time**.
2. **Penonaktifan Langsung (Immediate Disable):** Untuk mahasiswa berstatus **nonaktif** atau **drop-out (DO)**, penonaktifan akun SSO (DISABLE) dilakukan **seketika/langsung** saat status berubah di sistem, berbeda dengan status LULUS yang mendapatkan masa tenggang 3 bulan.

## Evidence Rule

For the actual case:
- Do not invent organizational facts.
- Distinguish supplied case facts from assumptions.
- Record evidence for important claims.
- When external sources are later introduced, record source, date, URL/identifier, and the claim supported.
