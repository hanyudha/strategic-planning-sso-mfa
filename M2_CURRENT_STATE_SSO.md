# M2 — Kondisi Saat Ini SSO

## Status

**DIKUNCI / LOCKED (2026-09-21)**

Dokumen ini mendokumentasikan baseline kondisi SSO saat ini secara faktual: arsitektur, komponen, alur autentikasi, integrasi 44 aplikasi/client, siklus hidup akun (pembuatan & penonaktifan otomatis), peran administratif, logging, dan kontrol keamanan yang sudah ada. Milestone ini dikunci atas persetujuan pengguna pada 2026-09-21 dan menjadi rujukan faktual untuk analisis pada milestone berikutnya.

M2 tidak memilih produk MFA dan tidak menetapkan arsitektur target. Informasi yang belum didukung bukti diberi tanda `[EVIDENCE NEEDED]`; informasi yang perlu dikonfirmasi diberi tanda `[TO BE VALIDATED]`; kesimpulan awal diberi tanda `[INFERENCE]`. Bukti dari lingkungan development diberi tanda `[DEV ENV — TO BE VALIDATED ON PRODUCTION]`.

Kode sumber bukti awal mengikuti M1: `U-01`, `U-02`, `U-03`, `O-01`, `D-01`, dan `D-02`. Bukti baru M2: `U-04` = data pengguna putaran M2, 2026-09-21; `D-03` = Panduan Penggunaan Jaringan Internet Kampus Wi-Fi SSO UIN Jakarta; `T-01` = ekstrak teks Keycloak Admin Console `Server Info` / `Providers`, 2026-09-21; `T-02` = screenshot User Federation; `T-03` = screenshot Events/Login Events; `T-04` = screenshot Required Actions; `T-05` = screenshot Clients (halaman 1 awal, terpotong); `T-06` = konfirmasi Password Policy kosong; `T-07` = screenshot OTP Policy; `T-08` = screenshot Events > Config; `T-09` = screenshot Client Scopes; `T-10` = screenshot Clients halaman 1 (lengkap); `T-11` = screenshot Clients halaman 2; `T-12` = screenshot Clients halaman 3 (terakhir); `U-05` = data pengguna: peran eSDM dan atribut login per kategori; `U-06` = data pengguna: pola password default mahasiswa; `U-07` = data pengguna: username/password dosen & tendik; `U-08` = data pengguna: peran eAkademik & dev artifact client; `U-09` = data pengguna: migrasi mahasiswa produksi, alur eRegistrasi->eAkademik, penonaktifan otomatis 3 bulan pasca LULUS; `U-10` = data pengguna: sinkronisasi real-time eSDM & penonaktifan langsung mahasiswa nonaktif/DO. Seluruh bukti teknis berasal dari lingkungan development.

Seluruh bukti T-02 sampai T-10 berasal dari lingkungan development Keycloak (`dev-sso.uinjkt.ac.id`). Pengguna menyampaikan bahwa akses hanya diberikan untuk lingkungan development, namun konfigurasi kemungkinan sama dengan produksi. Konfirmasi kesesuaian dengan produksi tetap diperlukan.

## 1. Tujuan M2

Menyusun baseline kondisi SSO saat ini agar analisis internal IS/IT, gap, strategi MFA, dan roadmap pada milestone berikutnya tidak dibangun di atas asumsi teknis yang belum terbukti.

## 2. Fakta yang Dibawa dari M1

| Area | Kondisi yang sudah diketahui | Status bukti |
|---|---|---|
| Keberadaan SSO | SSO sudah operasional dan dipublikasikan sebagai SSO e-Semesta. | M1; O-01 |
| MFA | SSO belum terintegrasi MFA. | Baseline project |
| Pengguna utama | Mahasiswa, dosen, dan staf akademik/tendik. | M1; U-01 sampai U-03 |
| Jumlah pengguna awal | Mahasiswa 42.088; staf akademik 1.438; dosen 1.593. | M1; tanggal/acuan statistik perlu dikonfirmasi |
| Sumber identitas mahasiswa | eAkademik/eRegistrasi. | M1; U-01 |
| Sumber identitas dosen/tendik | eSDM. | M1; U-01 |
| Aplikasi terintegrasi | eAkademik, eAkademik Portal, eAset, eBeasiswa, eFinansi, eKinerja, eRegistrasi, CMS Website, ePLO, eSDM. | M1; U-02 dan U-03 |
| Wi-Fi SSO | Akses Wi-Fi kampus melalui SSO berlaku mulai 1 Mei 2026; maksimal tiga perangkat simultan per akun; autentikasi ulang setelah terputus lebih dari 60 menit perlu divalidasi sebagai ketentuan yang masih berlaku. | M1; D-01 |
| Reset kata sandi | Reset mandiri e-Semesta untuk mengubah kata sandi awal/default; SMILE untuk kasus lupa kata sandi yang direset oleh layanan PUSTIPANDA. | M1; U-03 dan D-01 |
| Log login | Log login dilaporkan tersedia; akses server SSO berada pada tim infrastruktur atau data center. | M1; U-01 dan U-03 |
| Platform SSO | SSO e-Semesta menggunakan Keycloak. | U-04 |
| Lokasi layanan SSO | SSO berjalan di data center kampus. | U-04 |
| Pola sinkronisasi data | Sinkronisasi eSDM ke SSO terkonfirmasi berjalan **real-time** via `esdm-sync-service`. | U-04, U-10; T-11 |
| Protokol integrasi | Integrasi dilaporkan menggunakan SAML 2.0 Identity Provider Metadata. | U-04; perlu validasi per aplikasi |
| Pola otorisasi | Role induk berasal dari SSO, sedangkan fungsi aplikasi seperti create, read, update, dan delete dapat dikonfigurasi di masing-masing aplikasi. | U-04 |
| Kapabilitas teknis Keycloak | Halaman `Server Info` / `Providers` menunjukkan ketersediaan provider SAML, OpenID Connect, LDAP storage, JPA, Infinispan, OTP, WebAuthn, required actions, dan event provider. Ini belum membuktikan konfigurasi aktif pada realm/aplikasi. | T-01 |

## 3. Arsitektur Saat Ini

### 3.1 Gambaran arsitektur konseptual

```text
[Pengguna]
    -> [SSO e-Semesta / Keycloak, realm SSOUIN]
    -> [Aplikasi terintegrasi (18+ client) / Wi-Fi]
    -> [Sumber data identitas: eSDM via REST API migration (aktif)]
```

Platform SSO adalah Keycloak dengan realm bernama **SSOUIN**. Domain SSO pada lingkungan development: `dev-sso.uinjkt.ac.id`; domain aplikasi mayoritas `devel.uinjkt.ac.id`. `[DEV ENV — TO BE VALIDATED ON PRODUCTION]`

Mekanisme sinkronisasi identitas menggunakan **User Migration Using A REST Client** — bukan LDAP, bukan Kerberos, bukan Active Directory. Dari 16 entry User Federation, hanya **eSDM yang aktif (enabled)**; semua entry lain dinonaktifkan. Pola ini mengindikasikan *lazy migration*: user dimigrasi ke database lokal Keycloak saat login pertama kali melalui REST API ke aplikasi sumber. T-02; `[DEV ENV — TO BE VALIDATED ON PRODUCTION]`

Komponen server rinci (jumlah node, database, load balancer, reverse proxy) belum dibuktikan.

### 3.2 Komponen yang perlu diidentifikasi

| Komponen | Kondisi saat ini | Bukti yang dibutuhkan |
|---|---|---|
| Identity Provider / platform SSO | Keycloak, realm **SSOUIN**. | Versi bila boleh dan peran komponen; T-02 sampai T-05 |
| Portal SSO / domain layanan | Lingkungan development: `dev-sso.uinjkt.ac.id`. Domain produksi: `[TO BE VALIDATED]`. | Konfirmasi domain produksi |
| Direktori pengguna / User Federation | **Seluruh 16 entry menggunakan provider "User Migration Using A REST Client"**. Hanya **eSDM yang enabled**. User Federation entry eAkademik disabled karena **pada SSO produksi seluruh mahasiswa telah dimigrasi penuh ke Keycloak** (U-09). LDAP/AD/Kerberos tidak digunakan sebagai mekanisme federasi aktif. | T-02, U-09; `[DEV ENV — TO BE VALIDATED ON PRODUCTION]` |
| Database SSO | Keycloak memiliki provider JPA/Quarkus dan store Infinispan/JPA. Database aktif dan topologi penyimpanan masih `[EVIDENCE NEEDED]`. | Jenis database dan fungsi penyimpanan yang digunakan |
| Server/aplikasi SSO | Berjalan di data center kampus. | Jumlah node bila boleh, sistem operasi/platform runtime, dan skema ketersediaan |
| Integrasi aplikasi | 20+ client terdaftar pada realm SSOUIN (halaman 1 penuh; ada halaman berikutnya). Provider login `saml` dan `openid-connect` tersedia. Client Scopes didominasi OIDC (T-09). Protokol per client belum diidentifikasi. | T-05, T-10; `[DEV ENV]`; perlu halaman 2 dan protokol per client |
| Integrasi Wi-Fi | Entry `Reg Guest Wifi` ada pada User Federation tetapi disabled. | T-02; relasi antara SSO, captive portal/RADIUS/perangkat jaringan masih `[EVIDENCE NEEDED]` |
| Monitoring | `[EVIDENCE NEEDED]` | Tools/pihak pemantau dan indikator dasar |
| Backup/restore | `[EVIDENCE NEEDED]` | Kebijakan dan tanggung jawab pemulihan layanan |

## 4. Inventaris Teknis Integrasi

Daftar client lengkap realm SSOUIN diperoleh dari 3 halaman Clients (T-10, T-11, T-12). Total **44 client** terdaftar. `[DEV ENV]`

### 4.1 Inventaris dari M1 (diperbarui dengan bukti M2)

| No. | Layanan | Pemilik layanan | Client ID di Keycloak | Base URL (dev) | Catatan M2 |
|---:|---|---|---|---|---|
| 1 | eAkademik | Akademik Pusat dan akademik fakultas | `eAkademik` | `devel.uinjkt.ac.id/eakademik` | **Mengelola akun mahasiswa** (U-08). Client tambahan: `eAkademikClient`. User Federation entry disabled karena pada SSO produksi **seluruh mahasiswa telah dimigrasi penuh ke Keycloak** (U-09). T-02, T-10, U-09 |
| 2 | eRegistrasi | Akademik Pusat | `eRegistrasi` | `devel.uinjkt.ac.id/eregistrasi/` | Client tambahan: `eRegistrasiSKI`; T-11 |
| 3 | eSDM | SDM / Kepegawaian | `eSDM` | `devel.uinjkt.ac.id/client/ski-esdm` | **Mengelola akun dosen dan pegawai (tendik)**, TIDAK mengelola mahasiswa (U-08). User Federation **enabled**; berwenang enable/disable akun SSO; client tambahan: `esdm-sync-service`; T-02, T-11, U-05 |
| 4 | eAkademik Portal | Akademik Pusat dan akademik fakultas | `eAkademik-portal` | `devel.uinjkt.ac.id/portal` | T-10 |
| 5 | eAset | Tim BMN | `eAset` | `devel.uinjkt.ac.id/easet/` | Client tambahan: `eAsetPostgreSKI`; T-10 |
| 6 | eBeasiswa | Akademik Pusat | `eBeasiswa` | `devel.uinjkt.ac.id/client/ski.ebeasiswa` | Client tambahan: `eBeasiswaPostgreSKI`; T-10 |
| 7 | eFinansi | Keuangan dan Perencanaan | `eFinansi` | `devel.uinjkt.ac.id/efinansi/` | T-10 |
| 8 | eKinerja | Kepegawaian | **Tidak ditemukan di development** | — | Pengguna menyampaikan kemungkinan ada di SSO production. Ini mengonfirmasi perbedaan antara lingkungan dev dan prod. U-07 |
| 9 | CMS Website | Pusat Informasi dan Humas | **Tidak ditemukan** | — | Tidak ada client yang jelas sebagai CMS Website. Kemungkinan `local-cms-uinjkt` (T-11), tapi ini terlihat sebagai local/dev. Perlu konfirmasi. |
| 10 | ePLO | Pusat Tata Usaha | `PLO` | `plo.uinjkt.ac.id/` | URL tanpa prefix "dev" — kemungkinan URL produksi; T-11 |
| 11 | Wi-Fi kampus SSO | PUSTIPANDA | — | — | Tidak terdaftar sebagai client; User Federation: `Reg Guest Wifi` (disabled); client: `reg-wifi-local` (T-11) |

### 4.2 Aplikasi/client baru yang ditemukan di Keycloak (belum ada di inventaris M1)

`[DEV ENV — TO BE VALIDATED ON PRODUCTION]`

| No. | Client ID | Base URL (dev) | Kategori dugaan | Perlu dikonfirmasi |
|---:|---|---|---|---|
| 12 | `dev-lms` | `dev-lms.uinjkt.ac.id` | Learning Management System | Pemilik, pengguna, status operasional |
| 13 | `eadmisi` | `admisi.uinjkt.ac.id` | Penerimaan mahasiswa baru | Pemilik, pengguna, status operasional |
| 14 | `eAlumni` | `devel.uinjkt.ac.id/ealumni-bo` | Sistem alumni (back-office) | Pemilik, pengguna, status operasional |
| 15 | `eKKN` | `devel.uinjkt.ac.id/ekkn/` | Kuliah Kerja Nyata | Pemilik, pengguna, status operasional |
| 16 | `eDashboard` | Not defined | Dashboard/monitoring | Pemilik, pengguna, fungsi |
| 17 | `ePembayaran` | `devel.uinjkt.ac.id/epembayaran/` | Pembayaran | Pemilik, pengguna, status operasional |
| 18 | `eSPMI` | Not defined | Sistem Penjaminan Mutu Internal | Pemilik, pengguna, status operasional; T-11 |
| 19 | `eRiset` | `devel.uinjkt.ac.id/eriset/` | Riset/penelitian | Pemilik, pengguna, status operasional; T-11 |
| 20 | `mCampus` | Not defined | Mobile campus app | Pemilik, pengguna, platform; T-11 |
| 21 | `mhst` | Not defined | Mahasiswa (mobile?) | Pemilik, pengguna, platform; T-11 |
| 22 | `sso` | `app-sso.uinjkt.ac.id/` | Portal SSO utama | Fungsi dan relasi dengan SSO e-Semesta; T-12 |
| 23 | `uhelp sso admin` | Not defined | UHelp admin — helpdesk/ticketing? | Pemilik, relasi dengan SMILE; T-12 |
| 24 | `uhelp sso bridge` | Not defined | UHelp bridge — integrasi helpdesk? | Pemilik, relasi dengan SMILE; T-12 |

### 4.3 Client teknis, backend, dan development

Client dengan suffix "SKI" / "PostgreSKI" kemungkinan merupakan konfigurasi development saja dan tidak memiliki fungsi khusus di production (U-08).

| Client ID | Base URL (dev) | Kategori | Catatan |
|---|---|---|---|
| `eAkademikClient` | Not defined | Backend eAkademik | Relasi dengan `eAkademik` |
| `eRegistrasiSKI` | `devel.uinjkt.ac.id/client/ski-eregistrasi/` | Backend eRegistrasi | T-11 |
| `eAsetPostgreSKI` | `devel.uinjkt.ac.id/client/ski-easet/` | Backend eAset | |
| `eBeasiswaPostgreSKI` | `devel.uinjkt.ac.id/postgres/ebeasiswa/` | Backend eBeasiswa | |
| `eKKNPostgre` | `devel.uinjkt.ac.id/client/ski-ekkn/` | Backend eKKN | |
| `ePembayaranSKI` | `devel.uinjkt.ac.id/client/ski-epembayaran/` | Backend ePembayaran | T-10 |
| `eRisetPostgreSki` | `devel.uinjkt.ac.id/postgres/eriset/` | Backend eRiset | T-11 |
| `esdm-sync-service` | Not defined | **Service sinkronisasi eSDM** | Bukti mekanisme sync eSDM→Keycloak; T-11 |
| `SKIeKKNLocal` | Not defined | Local dev eKKN SKI | T-11 |
| `http://staff1.uinjkt.ac.id:1000/remote/saml/metadata/` | Not defined | **Client SAML** | Bukti integrasi SAML aktif untuk staff; T-11 |
| `local-api` | Not defined | Local API dev | T-11 |
| `local-cms-uinjkt` | Not defined | Local CMS dev | Kemungkinan terkait CMS Website; T-11 |
| `local-eAkademik` | `localhost:8000/` | Local eAkademik dev | T-11 |
| `local-paper-ess` | Not defined | Local Paper ESS dev | T-11 |
| `local-sso-soa` | Not defined | Local SSO SOA dev | **Disabled**; T-11 |
| `reg-wifi-local` | Not defined | Local WiFi registration dev | T-11 |
| `ssotesting` | `sso-uinjkt.test` | Testing SSO | **Disabled**; T-12 |
| `Contoh localhost` | — | Konfigurasi percobaan | User Federation only |
| `eRset PostgresQL SKI` | — | Backend eRset/eRiset | User Federation only |

### 4.4 Keycloak built-in clients

`account`, `account-console`, `admin-cli`, `broker`, `realm-management`, `security-admin-console` — client bawaan Keycloak, bukan aplikasi bisnis.

## 5. Alur Autentikasi Saat Ini

### 5.1 Login aplikasi

1. Pengguna mengakses aplikasi terintegrasi SSO.
2. Pengguna diarahkan ke SSO e-Semesta berbasis Keycloak (realm SSOUIN).
3. Pengguna memasukkan kredensial sesuai kategori:
   - **Mahasiswa**: Username = NIM, password default = `Mhs` + NIK (contoh: NIK 123456789 → password `Mhs123456789`). U-05, U-06
   - **Dosen**: Username = nama lengkap dengan format dot (contoh: `wandy.hanyudha`), password default = NIK (tanpa prefix). U-07
   - **Pegawai/Tendik**: Username = nama lengkap dengan format dot (contoh: `wandy.hanyudha`), password default = NIK (tanpa prefix). U-07
4. SSO memvalidasi identitas. Sumber identitas aktif:
   - **Dosen/Tendik**: eSDM melalui REST API migration (T-02). eSDM berwenang enable/disable akun (U-05). Sync via `esdm-sync-service` (T-11).
   - **Mahasiswa**: Dikelola oleh eAkademik/Akademik Pusat (U-08). Terkonfirmasi pada SSO produksi seluruh mahasiswa telah dimigrasi penuh ke Keycloak (U-09).
5. SSO mengirim hasil autentikasi dan role induk ke aplikasi. Protokol per client belum diidentifikasi (Client Scopes didominasi OIDC per T-09, namun U-04 melaporkan SAML 2.0).
6. Aplikasi memberikan akses sesuai role dan konfigurasi fungsi internal aplikasi. Contoh pola: role `Developer` dari SSO dapat dipetakan di eRegistrasi ke fungsi create, read, update, dan delete pada menu tertentu. Sumber: U-04.

### 5.2 Login Wi-Fi

1. Pengguna memilih SSID sesuai kelompok pengguna.
2. Mahasiswa memilih `MHS.UINJKT.AC.ID`; tenaga kependidikan dan dosen memilih `STAF.UINJKT.AC.ID`.
3. Mahasiswa menggunakan NIM sebagai username; tenaga kependidikan dan dosen menggunakan email kampus.
4. Pengguna memasukkan password e-Semesta atau kredensial awal sesuai kategori yang dijelaskan dalam panduan. Detail pola kredensial awal tidak direplikasi di sini karena perlu diperlakukan sebagai informasi sensitif.
5. Sistem membatasi penggunaan maksimal tiga perangkat simultan per akun.
6. Pengguna melakukan autentikasi ulang apabila koneksi terputus lebih dari 60 menit.

Sumber alur Wi-Fi: D-03.

Alur Wi-Fi di atas berasal dari D-01 dan D-03, tetapi detail teknis seperti captive portal, RADIUS, atau integrasi perangkat jaringan belum dibuktikan.

### 5.3 Reset password mandiri

Panduan Wi-Fi SSO menunjukkan alur reset password mandiri:

1. Pengguna memilih menu `Forgot Password` pada halaman sign in.
2. Pengguna memasukkan NIM atau email kampus.
3. Sistem mengirim informasi ke email kampus pengguna.
4. Pengguna memilih tautan reset credentials.
5. Pengguna membuat password baru.

Alur ini mendukung informasi M1 bahwa reset mandiri e-Semesta digunakan untuk mengubah atau memulihkan password oleh pengguna. Detail kontrol verifikasi, masa berlaku tautan, dan logging reset masih `[EVIDENCE NEEDED]`.

## 6. Siklus Hidup Akun

| Peristiwa | Kondisi yang diketahui | Kebutuhan bukti M2 |
|---|---|---|
| Calon mahasiswa menjadi mahasiswa | Status CALON MAHASISWA di eRegistrasi berubah menjadi MAHASISWA -> trigger event (click/sync) di eRegistrasi mentransfer data ke eAkademik -> akun SSO mahasiswa otomatis aktif. | U-09; detail teknis trigger event dan jadwal sync ke Keycloak |
| Dosen/tendik dibuat | Akun aktif ketika dibuat di eSDM. | Prosedur pembuatan, atribut wajib, dan validasi status |
| Perubahan status/peran dosen/tendik | Perubahan di eSDM otomatis memperbarui akun dan akses SSO. | Mekanisme teknis, jeda sinkronisasi, dan cakupan aplikasi |
| Penonaktifan dosen/tendik | Diselesaikan melalui eSDM/SDM/Kepegawaian dan otomatis berdampak ke SSO. eSDM berwenang enable/disable akun SSO. | U-05; bukti proses, SLA penonaktifan, dan pengecekan akses tersisa |
| Sinkronisasi data identitas | eSDM merupakan sumber identitas aktif melalui REST API migration. Sinkronisasi eSDM->Keycloak via `esdm-sync-service` berjalan secara **real-time** (U-10). eSDM berwenang enable/disable akun SSO. Mahasiswa sudah dimigrasi penuh ke Keycloak di produksi. | T-02, T-11, U-05, U-09, U-10 |
| Mahasiswa lulus/nonaktif/mengundurkan diri | Fitur otomatisasi penonaktifan: Mahasiswa berstatus **LULUS** di-DISABLE otomatis **3 bulan** setelah kelulusan (U-09); Mahasiswa berstatus **NONAKTIF / DROP-OUT** di-DISABLE secara **LANGSUNG/SEKETIKA** saat status berubah (U-10). | U-09, U-10 |
| Reset kata sandi mandiri | Aktif untuk mengganti kata sandi awal/default menjadi kata sandi pilihan pengguna. | Alur teknis, persyaratan verifikasi, dan log aktivitas |
| Reset kata sandi melalui SMILE | Digunakan untuk lupa kata sandi dan dieksekusi oleh layanan PUSTIPANDA. | Prosedur verifikasi identitas dan otorisasi petugas |

## 7. Peran Administratif

| Peran | Kondisi yang diketahui | Bukti yang dibutuhkan |
|---|---|---|
| Tim layanan PUSTIPANDA | Menindaklanjuti reset kata sandi melalui SMILE. | Daftar kewenangan tanpa nama personal, prosedur approval, dan audit aktivitas |
| Tim infrastruktur/data center | Memiliki akses server SSO dan log login. | Ruang lingkup akses, prosedur perubahan, dan review akses |
| Admin aplikasi | `[EVIDENCE NEEDED]` | Pemilik admin per aplikasi dan relasi dengan SSO |
| Admin data sumber identitas | `[EVIDENCE NEEDED]` | Siapa yang mengelola atribut mahasiswa/dosen/tendik |
| Pengambil keputusan akses khusus | `[EVIDENCE NEEDED]` | Proses persetujuan akses admin/privileged |

## 8. Logging, Audit, dan Monitoring

| Area | Kondisi saat ini | Kebutuhan bukti |
|---|---|---|
| Log login / Login Events | **Aktif (Save Events: ON).** Saved Types mencakup **hampir seluruh event type Keycloak** termasuk LOGIN, LOGOUT, REGISTER, UPDATE_PASSWORD, RESET_PASSWORD, LOGIN_ERROR, TOKEN_EXCHANGE, IMPERSONATE, dan puluhan lainnya. Event Listener: `jboss-logging`. Field per event: Time, Event Type, Client, User, IP Address, Error, Details. | T-03 dan T-08; `[DEV ENV]`. Prosedur review event oleh tim operasional masih `[EVIDENCE NEEDED]` |
| Admin Events | **Aktif (Save Events: ON).** Include Representation: OFF. Mencatat perubahan administratif pada Keycloak. | T-08; `[DEV ENV]`. Siapa yang meninjau admin events dan prosedur review masih `[EVIDENCE NEEDED]` |
| Event Expiration / Retensi | **Tidak dikonfigurasi (kosong).** Expiration pada Login Events Settings tidak diisi. Ini berarti event mungkin menumpuk tanpa batas atau mengikuti default Keycloak. | T-08; `[DEV ENV]`. Risiko: pertumbuhan data event tanpa batas; perlu kebijakan retensi |
| Akses log | Tim infrastruktur/data center memiliki akses server SSO. | Prosedur akses, otorisasi, dan review berkala |
| Log reset kata sandi | RESET_PASSWORD dan SEND_RESET_PASSWORD termasuk dalam Saved Types. Apakah event ini benar-benar tercatat untuk setiap reset perlu divalidasi. | T-08; `[DEV ENV]` |
| Log perubahan akun/peran | UPDATE_PASSWORD, UPDATE_PROFILE, UPDATE_EMAIL termasuk dalam Saved Types. Admin Events aktif dan dapat mencatat perubahan administratif. | T-08; `[DEV ENV]` |
| Monitoring ketersediaan SSO | `[EVIDENCE NEEDED]` | Tools, indikator, notifikasi, dan penanggung jawab |
| Laporan insiden/gangguan | SMILE menjadi portal layanan gangguan; ekspor D-02 tersedia sebagai agregat tiket login/kata sandi. | Kategori tiket, SLA formal, dan proses eskalasi |
| Kanal bantuan panduan Wi-Fi | Panduan mencantumkan WhatsApp PUSTIPANDA dan jam layanan hari kerja. | Hubungan kanal ini dengan SMILE dan pencatatan tiket masih perlu dikonfirmasi |

## 9. Kontrol Keamanan yang Sudah Diketahui

| Kontrol | Status awal | Catatan | Bukti |
|---|---|---|---|
| SSO terpusat | Tersedia, realm SSOUIN | 18+ client terdaftar | T-05 |
| MFA / Configure OTP | **Enabled sebagai Required Action, tetapi BUKAN Default Action** | OTP dapat diaktifkan per user secara selektif, namun tidak otomatis diminta ke semua user. Ini mengonfirmasi bahwa MFA belum diterapkan secara luas. | T-04; `[DEV ENV]` |
| Update Password (default) | **Enabled DAN Default Action** | Setiap user baru otomatis diminta mengganti password saat login pertama. Konsisten dengan informasi M1 tentang reset mandiri password awal. | T-04; `[DEV ENV]` |
| Terms and Conditions | **Enabled, bukan default** | Dapat dipicu per user tetapi tidak otomatis. | T-04; `[DEV ENV]` |
| Verify Email | **TIDAK enabled** | Email pengguna tidak diverifikasi oleh Keycloak. Ini menjadi risiko apabila MFA recovery nantinya mengandalkan email. | T-04; `[DEV ENV]` |
| WebAuthn Required Action | **Tidak muncul dalam daftar Required Actions** | Meskipun provider WebAuthn tersedia (T-01), Required Action untuk registrasi WebAuthn belum di-register. WebAuthn belum siap sebagai opsi MFA. | T-04; `[DEV ENV]` |
| Reset mandiri kata sandi | Tersedia | Konsisten dengan Update Password sebagai Default Action. | T-04; D-03 |
| Reset melalui layanan | Tersedia melalui SMILE | Perlu prosedur verifikasi pengguna. | U-03 |
| Batas perangkat Wi-Fi | Tersedia dalam D-01 | Perlu validasi ketentuan masih berlaku. | D-01 |
| Autentikasi ulang Wi-Fi | Tersedia dalam D-01 | Perlu validasi teknis dan pengecualian. | D-01 |
| Logging login | **Login Events dan Admin Events aktif** | Seluruh event type utama dicatat. Retensi tidak dikonfigurasi. | T-03 dan T-08; `[DEV ENV]` |
| Kebijakan/SOP autentikasi | `[EVIDENCE NEEDED]` | Jika belum ada, perlu konfirmasi formal. | — |
| Password Policy | **KOSONG — tidak ada aturan password yang diterapkan** | Tidak ada kebijakan panjang minimal, kompleksitas, history, expiration, atau lockout. User dapat menggunakan password apa pun tanpa batasan. Ini merupakan **temuan keamanan kritis**. | T-06; `[DEV ENV]` |
| OTP Policy | **Konfigurasi default Keycloak** | TOTP, SHA1, 6 digit, period 30 detik, Look Around Window 1. Supported: FreeOTP dan Google Authenticator. Ini adalah nilai default — belum dikustomisasi untuk kebutuhan organisasi. | T-07; `[DEV ENV]` |
| Client Scopes | **Didominasi OpenID Connect** | 10 scope: 9 menggunakan openid-connect (acr, address, email, mapper, microprofile-jwt, offline_access, phone, profile, roles, web-origins), 1 menggunakan saml (role_list). Scope `mapper` tampak kustom. Ini mengindikasikan **integrasi mungkin lebih banyak menggunakan OIDC daripada SAML**. | T-09; `[DEV ENV]` |
| Role induk dari SSO | Tersedia menurut informasi pengguna | Perlu contoh atribut/claim role dan pemetaan ke aplikasi. | U-04 |
| Otorisasi fungsi pada aplikasi | Dikelola pada aplikasi masing-masing | Perlu contoh matriks role-menu dari aplikasi prioritas. | U-04 |

## 10. Bukti Teknis Keycloak dari `Server Info` / `Providers`

Ekstrak T-01 menunjukkan provider/SPI yang tersedia pada server Keycloak. Bukti ini berguna untuk mengenali kapabilitas platform, tetapi tidak boleh diperlakukan sebagai daftar konfigurasi aktif pada realm atau client.

| Area | Provider/kapabilitas yang terlihat | Interpretasi untuk M2 |
|---|---|---|
| Login protocol | `saml`, `openid-connect` | Server mendukung SAML dan OIDC; integrasi aplikasi tetap perlu divalidasi per client. |
| Client/authenticator | `client-secret`, `client-jwt`, `client-x509`, `client-secret-jwt`, SAML/OIDC client installation | Server memiliki beberapa opsi autentikasi client; jenis yang aktif per aplikasi belum diketahui. |
| Storage/user source | `ldap`, `jpa`, `kerberos`, user migration via REST client | LDAP tersedia sebagai kapabilitas, tetapi sumber identitas aktif masih harus dibuktikan dari user federation/realm configuration. |
| Credential/MFA capability | `keycloak-password`, `keycloak-otp`, `keycloak-webauthn`, `keycloak-webauthn-passwordless` | OTP dan WebAuthn tersedia sebagai kapabilitas Keycloak; baseline project tetap menyatakan MFA belum diterapkan. |
| Required action | `CONFIGURE_TOTP`, `VERIFY_EMAIL`, `UPDATE_PASSWORD`, `UPDATE_PROFILE`, WebAuthn registration | Tersedia mekanisme bawaan untuk aksi pengguna, termasuk TOTP dan pembaruan password/profil; status aktif policy belum diketahui. |
| Event/logging | `eventsListener` `jboss-logging` dan `email`; `eventsStore` `jpa` | Mendukung pencatatan event, tetapi jenis event, retensi, dan review operasional masih perlu bukti tambahan. |
| Cache/session | beberapa provider `infinispan`; `userSessions` `infinispan`; `userSessionPersister` `disabled`/`jpa` | Menunjukkan komponen cache/session Keycloak tersedia; topologi deployment dan konfigurasi aktif belum diketahui. |
| Password policy options | panjang, history, regex, not username/email, upper/lower/digits/special chars, hash algorithm/iterations, force expired password change | Opsi policy tersedia; nilai policy aktif belum diketahui. |

## 11. Temuan Awal M2

1. SSO sudah menjadi kontrol autentikasi utama untuk layanan digital, dengan Keycloak sebagai platform SSO pada realm SSOUIN. Total **44 client** terdaftar dalam 3 halaman. `[INFERENCE]`; T-10, T-11, T-12
2. **Arsitektur sumber identitas dua jalur**: eSDM mengelola akun **dosen dan pegawai (tendik)** melalui REST API migration (enabled). eAkademik / Akademik Pusat mengelola akun **mahasiswa** (seluruh mahasiswa telah dimigrasi penuh ke Keycloak pada SSO produksi, sehingga User Federation entry disabled). Fakta; T-02, U-05, U-08, U-09; `[DEV ENV / PROD CONFIRMED]`
3. **Client `esdm-sync-service`** menyinkronkan data eSDM→Keycloak secara **real-time**. Fakta; T-11, U-10; `[DEV ENV / PROD CONFIRMED]`
4. **Configure OTP enabled tetapi bukan Default Action.** MFA secara teknis dapat diaktifkan per user, namun tidak diminta secara otomatis. MFA belum diterapkan secara luas. Fakta; T-04; `[DEV ENV]`
5. **Update Password adalah satu-satunya Default Action.** User baru otomatis diminta mengganti password saat login pertama. Fakta; T-04; `[DEV ENV]`
6. **Password default SEMUA pengguna berbasis NIK**, dengan pola yang dapat diprediksi. Mahasiswa: `Mhs` + NIK. Dosen dan tendik: **NIK langsung tanpa prefix**. Karena username bersifat publik/mudah ditebak (NIM untuk mahasiswa, `nama.lengkap` untuk dosen/tendik) dan NIK berpotensi dapat diakses, password default rentan terhadap *credential guessing*. **Meskipun Update Password adalah Default Action**, tidak ada jaminan semua user sudah mengganti, dan **tidak ada Password Policy** yang membatasi kualitas password baru. Fakta; U-06, U-07; **temuan keamanan kritis**
7. **Password Policy KOSONG.** Tidak ada aturan password yang diterapkan: panjang minimal, kompleksitas, history, expiration, atau lockout. **Temuan keamanan kritis.** Fakta; T-06; `[DEV ENV]`
8. **Verify Email tidak enabled.** Email pengguna tidak diverifikasi oleh Keycloak. Risiko untuk MFA recovery. Fakta; T-04; `[DEV ENV]`
9. **WebAuthn Required Action belum di-register.** WebAuthn belum siap sebagai opsi MFA. Fakta; T-04; `[DEV ENV]`
10. **OTP Policy menggunakan konfigurasi default Keycloak.** TOTP, SHA1, 6 digit, 30 detik. Belum dikustomisasi. Fakta; T-07; `[DEV ENV]`
11. **Login Events dan Admin Events keduanya aktif**, mencakup hampir seluruh event type. **Expiration tidak dikonfigurasi** — event mungkin menumpuk tanpa batas. Fakta; T-08; `[DEV ENV]`
12. **Client Scopes didominasi OpenID Connect** (10 dari 11 scope). Namun ditemukan client SAML (`http://staff1.uinjkt.ac.id:1000/remote/saml/metadata/`) yang membuktikan setidaknya **ada integrasi SAML aktif untuk staff**. Kedua protokol digunakan. Fakta; T-09, T-11; `[DEV ENV]`
13. Inventaris aplikasi terintegrasi SSO **jauh lebih banyak** dari M1. Ditemukan **13 aplikasi/client baru** termasuk dev-lms, eadmisi, eAlumni, eKKN, ePembayaran, eSPMI, eRiset, mCampus, mhst, sso, eDashboard, uhelp sso admin, dan uhelp sso bridge. Fakta; T-10 sampai T-12; `[DEV ENV]`
14. **eKinerja tidak ditemukan di lingkungan development**, namun kemungkinan ada di SSO production. Ini mengonfirmasi bahwa **konfigurasi development tidak identik dengan production** dan ada perbedaan inventaris client. CMS Website juga belum ditemukan. Fakta; T-10, T-11, T-12; U-07
15. Terdapat **pola client ganda** pada 6 aplikasi (eAset, eBeasiswa, eKKN, ePembayaran, eRegistrasi, eRiset memiliki client tambahan bertipe SKI/Postgre). `[INFERENCE]`; T-10, T-11
16. Adanya reset mandiri, reset melalui SMILE, dan 2.624 tiket terkait login/kata sandi menunjukkan bahwa desain MFA perlu mempertimbangkan beban layanan dan pengalaman pengguna. `[INFERENCE]`
17. Kombinasi **tidak ada password policy** (T-06), **password default yang dapat diprediksi** (U-06), **tidak ada MFA aktif** (T-04), dan **tidak ada verifikasi email** (T-04) menunjukkan bahwa pertahanan autentikasi saat ini **sepenuhnya bergantung pada kerahasiaan satu faktor (password)** tanpa kontrol teknis pendukung yang memadai. `[INFERENCE]`
18. **Siklus hidup akun mahasiswa memiliki fitur otomatisasi penuh**: pembuatan/pengaktifan SSO dipicu saat status CALON MAHASISWA berubah menjadi MAHASISWA di eRegistrasi (lalu ditransfer ke eAkademik via trigger event), penonaktifan mahasiswa LULUS dilakukan secara otomatis (DISABLE) 3 bulan pasca kelulusan, dan penonaktifan mahasiswa NONAKTIF/DROP-OUT dilakukan secara **langsung/seketika** saat status berubah di sistem. Fakta; U-09, U-10

## 12. Data yang Dibutuhkan dari Pengguna untuk Melengkapi M2

### A. Pertanyaan yang sudah terjawab (sebagian/penuh)

| Pertanyaan | Jawaban | Bukti |
|---|---|---|
| User Federation: LDAP/AD/custom? | **REST API migration**; hanya eSDM enabled. Seluruh mahasiswa sudah dimigrasi penuh pada SSO produksi | T-02, U-09 |
| Password Policy aktif? | **Kosong** | T-06 |
| OTP Policy? | **Default Keycloak**: TOTP, SHA1, 6 digit, 30 detik | T-07 |
| Login/Admin Events aktif? Retensi? | **Keduanya ON**, semua event type, **Expiration kosong** | T-08 |
| Required Actions? | OTP enabled (bukan default); Update Password default; Verify Email off; WebAuthn tidak di-register | T-04 |
| Atribut login? | Mahasiswa: NIM (username) + `Mhs`+NIK (password default); Dosen/Tendik: `nama.lengkap` (username) + NIK (password default) | U-05, U-06, U-07 |
| Daftar client lengkap? | **44 client** di 3 halaman; eRegistrasi, eSDM, eSPMI, eRiset, PLO terkonfirmasi; eKinerja kemungkinan hanya di production | T-10, T-11, T-12, U-07 |
| Mekanisme sync eSDM? | **Real-time** via client `esdm-sync-service` | T-11, U-10 |
| SAML vs OIDC? | Client Scopes didominasi OIDC; setidaknya 1 client SAML aktif (`staff1.uinjkt.ac.id`) | T-09, T-11 |
| Migrasi mahasiswa? | **Seluruh mahasiswa telah dimigrasi penuh** ke Keycloak pada SSO produksi | U-09 |
| Pembuatan akun mahasiswa baru? | Otomatis: Status CALON MAHASISWA -> MAHASISWA di eRegistrasi mentransfer data ke eAkademik via trigger event (click/sync), langsung mengaktifkan akun SSO | U-09 |
| Penonaktifan akun mahasiswa lulus? | **Otomatis**: Akun mahasiswa berstatus LULUS di-DISABLE secara otomatis 3 bulan setelah kelulusan | U-09 |
| Penonaktifan mahasiswa nonaktif/DO? | **Otomatis & Seketika (Immediate Disable)** saat status berubah menjadi nonaktif atau drop-out | U-10 |

### B. Pertanyaan yang masih terbuka

#### Lingkungan dan arsitektur
1. Keycloak versi berapa yang digunakan? `[TO BE CONFIRMED WITH PUSTIPANDA / TIM TEKNIS]`
2. Apakah Keycloak terdiri dari satu server atau beberapa node? `[TO BE CONFIRMED WITH PUSTIPANDA / TIM TEKNIS]`
3. Perbedaan development vs production sudah terkonfirmasi (eKinerja hanya di production). Apakah ada perbedaan lain yang diketahui selain inventaris client? Domain produksi SSO?

#### Integrasi dan client
4. Client SAML `http://staff1.uinjkt.ac.id:1000/remote/saml/metadata/` — ini belum teridentifikasi. `[TO BE CONFIRMED WITH PUSTIPANDA / TIM TEKNIS]`
5. **CMS Website** dilaporkan terintegrasi SSO di M1 tetapi tidak ditemukan di development. Apakah terkait `local-cms-uinjkt`?
6. Aplikasi baru: **dev-lms**, **eadmisi**, **eAlumni**, **eKKN**, **ePembayaran**, **eSPMI**, **eRiset**, **mCampus**, **mhst**, **sso**, **uhelp sso admin/bridge** — mana yang aktif digunakan?

#### Wi-Fi dan session
7. Bagaimana alur login Wi-Fi secara teknis? Captive portal, RADIUS, atau lainnya?
8. Berapa session timeout SSO?

#### Kebijakan dan operasional
9. Apakah sudah ada user yang secara individual diminta Configure OTP?
10. Apakah ada kebijakan/SOP tertulis untuk autentikasi?
11. Siapa yang meninjau Login/Admin Events?
12. Siapa saja peran admin SSO (tanpa nama personal)?
13. Apakah ada backup/restore atau DR?
14. Apakah ada riwayat insiden SSO?

## 13. Batas Milestone

M2 hanya mendeskripsikan kondisi SSO saat ini dan temuan awal. Analisis lingkungan bisnis internal dimulai pada M3 setelah M2 dikunci.
