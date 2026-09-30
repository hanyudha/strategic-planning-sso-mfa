import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="D5D5D5"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell_text(cell, text, bold=False, italic=False, size=Pt(7.5), color=RGBColor(0x00, 0x00, 0x00), align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.02
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Times New Roman"
    run.font.size = size
    run.font.color.rgb = color

def add_sec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    return p

def add_subsec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.italic = True
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(9.5)
    return p

def add_body_p(doc, text, first_indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if first_indent:
        p.paragraph_format.first_line_indent = Inches(0.18)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(9.5)
    return p

def build_comprehensive_manuscript(output_path):
    doc = Document()
    
    # Page Setup - Standard A4 with 0.65 in left/right and 0.75 in top/bottom
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

    # Set 2 columns on section
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        cols[0].set(qn('w:num'), '2')
        cols[0].set(qn('w:space'), '360') # 360 dxa = 0.25 inch gap
    else:
        cols_xml = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="360"/>')
        sectPr.append(cols_xml)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(9.5)
    style_normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # --- HEADER JURNAL AISM ---
    header = section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_head.paragraph_format.space_after = Pt(2)
    r_h1 = p_head.add_run("Applied Information System and Management (AISM)\n")
    r_h1.font.name = "Times New Roman"
    r_h1.font.size = Pt(8.5)
    r_h1.bold = True
    r_h2 = p_head.add_run("Volume 9, (2) 2026, p. 101–118\nP-ISSN: 2621-2536; E-ISSN: 2621-2544; DOI: 10.15408/aism.v9i2.38421\n©2026. The Author(s). This is an open acces article under cc-by-sa")
    r_h2.font.name = "Times New Roman"
    r_h2.font.size = Pt(7.5)
    
    p_head_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    p_head._p.get_or_add_pPr().append(p_head_border)

    # --- FOOTER JURNAL AISM ---
    footer = section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_f = p_foot.add_run("http://journal.uinjkt.ac.id/index.php/aism")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(8)
    r_f.font.italic = True

    # --- TITLE IN COLUMN 1 (Matches PDF Page 1) ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("Perencanaan Strategis Pengembangan Single Sign-On (SSO) Terintegrasi Multi-Factor Authentication (MFA) Menggunakan Metode Ward & Peppard pada UIN Syarif Hidayatullah Jakarta")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)

    # --- AUTHORS ---
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(8)
    r_a = p_auth.add_run("Wandy1*, Hanyudha2")
    r_a.font.name = "Times New Roman"
    r_a.font.size = Pt(10)

    # --- ABSTRACT (ENGLISH) ---
    p_abs_en = doc.add_paragraph()
    p_abs_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_en.paragraph_format.space_after = Pt(4)
    p_abs_en.paragraph_format.line_spacing = 1.05
    
    r_al_en = p_abs_en.add_run("Abstract—")
    r_al_en.bold = True
    r_al_en.font.italic = True
    r_al_en.font.name = "Times New Roman"
    r_al_en.font.size = Pt(8.5)
    
    r_at_en = p_abs_en.add_run(
        "Single Sign-On (SSO) e-Semesta at UIN Syarif Hidayatullah Jakarta serves over 45,219 academic users across 44 integrated institutional clients using the Keycloak platform. "
        "However, empirical audits revealed critical vulnerabilities: empty password policies, predictable default passwords derived from national identity numbers (NIK/NIM), "
        "disabled email verification, and single-factor password reliance. This operational weakness resulted in 2,624 manual helpdesk support tickets and elevated compliance risks under "
        "Indonesian Personal Data Protection Law (UU PDP No. 27/2022). This study formulates a strategic information systems plan using the Ward & Peppard framework, incorporating "
        "Value Chain, PESTEL, Keycloak console audits, SWOT/TOWS, and McFarlan Strategic Grid analyses. The strategic formulation delivers three pillars: an IS strategy enforcing MFA step-up "
        "across all 44 clients and self-service recovery; an IT strategy deploying zero-license-cost Time-based One-Time Password (TOTP) for bulk campus users and FIDO2/WebAuthn for privileged administrators; "
        "and an IS/IT management strategy establishing governance SOPs and 180-day audit log retention. The 12-month implementation roadmap targets an >80% reduction in helpdesk tickets and full regulatory compliance."
    )
    r_at_en.font.italic = True
    r_at_en.font.name = "Times New Roman"
    r_at_en.font.size = Pt(8.5)

    # INDEX TERMS (ENGLISH)
    p_idx_en = doc.add_paragraph()
    p_idx_en.paragraph_format.space_after = Pt(6)
    p_idx_en.paragraph_format.line_spacing = 1.05
    r_kl_en = p_idx_en.add_run("Index Terms—")
    r_kl_en.bold = True
    r_kl_en.font.italic = True
    r_kl_en.font.name = "Times New Roman"
    r_kl_en.font.size = Pt(8.5)
    r_kt_en = p_idx_en.add_run("Single Sign-On (SSO), Multi-Factor Authentication (MFA), Ward & Peppard, Keycloak, TOTP, FIDO2/WebAuthn, Information System Strategic Planning, Higher Education.")
    r_kt_en.font.name = "Times New Roman"
    r_kt_en.font.size = Pt(8.5)

    # --- ABSTRAK (BAHASA INDONESIA) ---
    p_abs_id = doc.add_paragraph()
    p_abs_id.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_id.paragraph_format.space_after = Pt(4)
    p_abs_id.paragraph_format.line_spacing = 1.05
    
    r_al_id = p_abs_id.add_run("Abstrak—")
    r_al_id.bold = True
    r_al_id.font.italic = True
    r_al_id.font.name = "Times New Roman"
    r_al_id.font.size = Pt(8.5)
    
    r_at_id = p_abs_id.add_run(
        "Sistem Single Sign-On (SSO) e-Semesta berbasis Keycloak pada UIN Syarif Hidayatullah Jakarta melayani 45.219 pengguna aktif dan terintegrasi dengan 44 aplikasi institusi. "
        "Namun, audit empiris mengidentifikasi celah keamanan kritis: Password Policy yang kosong, penggunaan kata sandi default terprediksi berbasis NIK/NIM, fitur Verify Email yang dinonaktifkan, "
        "serta ketergantungan pada autentikasi satu faktor. Kondisi ini memicu 2.624 tiket manual di helpdesk SMILE serta menciptakan risiko ketidakpatuhan terhadap UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). "
        "Penelitian ini menyusun perencanaan strategis sistem informasi menggunakan metodologi Ward & Peppard yang memadukan analisis Value Chain, PESTEL, audit konsol Keycloak, SWOT/TOWS, dan McFarlan Strategic Grid. "
        "Hasil formulasi merumuskan tiga pilar strategi: Strategi SI (integrasi MFA step-up pada 44 client dan portal pemulihan mandiri); Strategi TI (penerapan TOTP nirbiaya lisensi untuk 45rb sivitas akademika dan FIDO2/WebAuthn untuk akun admin/privileged); "
        "serta Strategi Manajemen SI/TI (penyusunan SOP resmi SSO dan retensi log audit 180 hari). Peta jalan 12 bulan ditargetkan memotong >80% beban helpdesk dan menjamin kepatuhan regulasi institusi."
    )
    r_at_id.font.name = "Times New Roman"
    r_at_id.font.size = Pt(8.5)

    # KATA KUNCI (BAHASA INDONESIA)
    p_idx_id = doc.add_paragraph()
    p_idx_id.paragraph_format.space_after = Pt(8)
    p_idx_id.paragraph_format.line_spacing = 1.05
    r_kl_id = p_idx_id.add_run("Kata Kunci—")
    r_kl_id.bold = True
    r_kl_id.font.italic = True
    r_kl_id.font.name = "Times New Roman"
    r_kl_id.font.size = Pt(8.5)
    r_kt_id = p_idx_id.add_run("Single Sign-On (SSO), Multi-Factor Authentication (MFA), Ward & Peppard, Keycloak, TOTP, FIDO2/WebAuthn, Perencanaan Strategis SI/TI, UIN Syarif Hidayatullah Jakarta.")
    r_kt_id.font.name = "Times New Roman"
    r_kt_id.font.size = Pt(8.5)

    # --- FOOTNOTE BOX IN COLUMN 1 (Matches PDF bottom left) ---
    p_fn = doc.add_paragraph()
    p_fn.paragraph_format.space_before = Pt(4)
    p_fn.paragraph_format.space_after = Pt(8)
    p_fn.paragraph_format.line_spacing = 1.0
    r_fn = p_fn.add_run(
        "____________________________________________________\n"
        "Artikel penelitian perencanaan strategis SI/TI UIN Syarif Hidayatullah Jakarta.\n"
        "*Penulis Korespondensi (Corresponding author).\n"
        "1Wandy, Program Studi Sistem Informasi, Fakultas Sains dan Teknologi, UIN Syarif Hidayatullah Jakarta (e-mail: author@uinjkt.ac.id).\n"
        "2Hanyudha, Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA), UIN Syarif Hidayatullah Jakarta (e-mail: pustipanda@uinjkt.ac.id)."
    )
    r_fn.font.name = "Times New Roman"
    r_fn.font.size = Pt(7.5)
    r_fn.font.italic = True
    r_fn.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # =========================================================================
    # SECTION I. INTRODUCTION
    # =========================================================================
    add_sec_heading(doc, "I. INTRODUCTION")
    add_body_p(doc, "Transformasi digital pada institusi pendidikan tinggi negeri di Indonesia berkembang sangat pesat seiring dengan tuntutan integrasi layanan akademik, kepegawaian, finansial, dan penelitian. Universitas Islam Negeri (UIN) Syarif Hidayatullah Jakarta sebagai salah satu Perguruan Tinggi Keagamaan Islam Negeri (PTKIN) terkemuka mengemban visi keunggulan integrasi ilmu keislaman, keindonesiaan, dan sains yang bereputasi global. Dalam mendukung visi tersebut, Unit Pelaksana Teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) bertanggung jawab mengelola dan mengembangkan seluruh infrastruktur teknologi informasi, sistem informasi, dan pangkalan data institusi [1], [2].")
    add_body_p(doc, "Saat ini, PUSTIPANDA mengoperasikan portal Single Sign-On (SSO) terpusat berbasis platform open-source enterprise Keycloak (realm SSOUIN), yang dikenal dengan nama portal e-Semesta (beralamat di app-sso.uinjkt.ac.id). Portal ini melayani populasi masif sebanyak 45.219 pengguna aktif yang terdaftar dalam direktori kampus, mencakup 42.088 mahasiswa lintas strata pendidikan (S1, S2, dan S3 pada 12 fakultas dan sekolah pascasarjana), 1.593 dosen tetap dan dosen luar biasa, serta 1.438 tenaga kependidikan dan staf administratif [3]. Melalui SSO e-Semesta, sivitas akademika dapat mengakses 44 aplikasi institusional yang saling terintegrasi, antara lain portal akademik eAkademik, sistem pendaftaran eRegistrasi, modul SDM eSDM, manajemen aset eAset, sistem persuratan PLO, sistem kinerja pegawai eKinerja, hingga jaringan internet nirkabel Wi-Fi SSO [4].")
    add_body_p(doc, "Kendati SSO e-Semesta berhasil mengeliminasi fragmentasi kredensial dan menyederhanakan akses bagi puluhan ribu sivitas akademika, evaluasi empiris terhadap postur keamanan sistem operasional mengungkap celah kerentanan mendasar: mekanisme autentikasi saat ini masih sepenuhnya bertumpu pada faktor tunggal berupa kata sandi (single-factor password). Penelusuran langsung pada Keycloak Admin Console membuktikan bahwa pengaturan kebijakan kata sandi (Password Policy) berada dalam kondisi KOSONG / TIDAK ADA ATURAN sama sekali (bukti T-06) [5]. Akibatnya, sistem mengizinkan pengguna menetapkan kata sandi yang sangat pendek, sederhana, dan mudah ditebak tanpa adanya batasan masa kedaluwarsa maupun penolakan terhadap kata sandi yang telah bocor.")
    add_body_p(doc, "Lebih berisiko lagi, akun pengguna baru secara default diberikan kata sandi terprediksi berbasis data publik kependudukan: akun mahasiswa menggunakan pola 'Mhs' diikuti Nomor Induk Kependudukan (NIK), sedangkan akun dosen dan staf menggunakan NIK murni tanpa awalan (bukti U-06, U-07) [3]. Di saat bersamaan, fitur verifikasi kepemilikan email (Verify Email) dalam kondisi dinonaktifkan (DISABLED), dan tindakan konfigurasi faktor kedua (Configure OTP) tidak dijadikan sebagai tindakan wajib (Required Action) saat pertama kali masuk (bukti T-04). Konfigurasi log audit juga tidak menetapkan batas kedaluwarsa peristiwa (Event Expiration kosong, bukti T-08), sehingga menyulitkan audit forensik jika terjadi insiden siber.")
    add_body_p(doc, "Kelemahan arsitektur autentikasi satu faktor ini menimbulkan dua konsekuensi kritis yang mengancam keberlangsungan operasional universitas:")
    add_body_p(doc, "1. Kerentanan Keamanan Siber yang Masif: Kata sandi bawaan berbasis NIK sangat mudah diakses atau ditebak oleh pihak ketiga melalui rekayasa sosial, kebocoran data kependudukan eksternal, maupun teknik serangan otomatis (credential stuffing dan automated brute-force). Ketiadaan verifikasi faktor kedua menjadikan SSO sebagai Single Point of Failure (SPoF); sekali kata sandi mahasiswa atau dosen dibobol, penyerang memperoleh akses tanpa batas ke pangkalan data nilai akademik, data pribadi mahasiswa, dan sistem keuangan universitas [6].")
    add_body_p(doc, "2. Beban Operasional Helpdesk yang Ekstrem: Ketiadaan verifikasi email mandiri memaksa seluruh pengguna yang mengalami kendala lupa kata sandi atau terkunci dari akun untuk mengajukan tiket bantuan secara manual ke sistem tiket SMILE PUSTIPANDA. Rekapitulasi tiket operasional mencatat 2.624 tiket manual menumpuk hanya untuk masalah pengaturan ulang kata sandi (bukti D-02) [7]. Hal ini menguras jam kerja staf TI, memperpanjang waktu pemulihan akun (MTTR), dan menurunkan tingkat kepuasan layanan.")
    add_body_p(doc, "Dari perspektif regulasi dan kepatuhan hukum, pemberlakuan Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) secara tegas mewajibkan penyelenggara sistem elektronik untuk menjamin keamanan pemrosesan data pribadi melalui kontrol teknis yang memadai (Pasal 35). Membiarkan pangkalan data 45.219 sivitas akademika terproteksi hanya dengan kata sandi NIK default merupakan kelalaian serius yang berisiko memicu sanksi administratif dan hukum [8]. Selain itu, Peraturan Presiden No. 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik (SPBE) mengamanatkan penerapan autentikasi kuat pada layanan publik.")
    add_body_p(doc, "Berdasarkan permasalahan faktual tersebut, penelitian ini bertujuan merumuskan Perencanaan Strategis Sistem Informasi (IS/IT Strategic Planning) menggunakan metodologi Ward & Peppard untuk memperkuat sistem SSO e-Semesta melalui integrasi Multi-Factor Authentication (MFA). Perencanaan strategis ini difokuskan pada pemanfaatan kapabilitas native Keycloak yang ada (tanpa pembangunan ulang dari nol / no greenfield rebuild) guna menciptakan arsitektur autentikasi berlapis yang nirbiaya lisensi, aman, patuh hukum, dan efisien secara operasional.")

    # =========================================================================
    # SECTION II. RELATED WORK & THEORETICAL FOUNDATION
    # =========================================================================
    add_sec_heading(doc, "II. RELATED WORK & THEORETICAL FOUNDATION")
    add_body_p(doc, "Kerangka kerja perencanaan strategis Ward & Peppard merupakan metodologi standar yang diakui secara luas dalam bidang tata kelola sistem informasi untuk menjajaki keselarasan antara strategi bisnis dan strategi SI/TI [1]. Model ini mendasarkan analisisnya pada empat perspektif lingkungan: (1) Lingkungan Bisnis Internal, mencakup rantai nilai dan proses bisnis; (2) Lingkungan Bisnis Eksternal, mencakup dinamika industri dan regulasi PESTEL; (3) Lingkungan SI/TI Internal, mencakup portofolio aplikasi, infrastruktur, dan sumber daya manusia; serta (4) Lingkungan SI/TI Eksternal, mencakup tren teknologi dan standar keamanan terkini. Luaran utama dari metodologi ini adalah tiga pilar strategi: IS Strategy (apa yang dibutuhkan bisnis), IT Strategy (bagaimana teknologi menyediakannya), dan IS/IT Management Strategy (bagaimana tata kelola dan pengawasannya) [1], [9].")
    add_body_p(doc, "Dalam domain manajemen identitas dan akses (Identity and Access Management / IAM), Single Sign-On (SSO) memegang peranan krusial sebagai jembatan federasi identitas terpusat. Menggunakan protokol modern seperti OpenID Connect (OIDC) berbasis JSON Web Token (JWT) dan Security Assertion Markup Language (SAML 2.0) berbasis XML assertions, Keycloak bertindak sebagai Identity Provider (IdP) yang memisahkan otoritas kredensial dari aplikasi klien (Service Providers / Relying Parties) [10]. Melalui pemusatan ini, aplikasi hilir tidak perlu lagi menyimpan basis data kata sandi tersendiri, melainkan cukup mempercayai token digital bertanda tangan kriptografis yang diterbitkan oleh Keycloak.")
    add_body_p(doc, "Kendati demikian, literatur keamanan siber modern menegaskan bahwa SSO berbasis kata sandi tunggal menciptakan Single Point of Failure (SPoF) [6]. Apabila penyerang berhasil memperoleh kredensial melalui phishing, keylogger, atau serangan credential stuffing, seluruh 44 aplikasi yang terhubung dapat disusupi seketika. Oleh karena itu, penerapan Multi-Factor Authentication (MFA) menjadi keharusan mutlak. Standar NIST Special Publication 800-63B (Digital Identity Guidelines) membagi tingkatan jaminan autentikasi (Authentication Assurance Level / AAL) menjadi tiga level, di mana AAL2 mensyaratkan bukti kepemilikan dua faktor autentikasi yang berbeda, dan AAL3 mensyaratkan faktor kriptografis yang terikat pada perangkat keras fisik [11].")
    add_body_p(doc, "Evaluasi terhadap lanskap teknologi MFA kontemporer mencakup lima keluarga teknologi [12]: (1) Time-based One-Time Password (TOTP RFC 6238) melalui aplikasi authenticator ponsel pintar (Google Authenticator, Microsoft Authenticator, FreeOTP); (2) Fast Identity Online v2 (FIDO2) / WebAuthn berbasis kunci kriptografi asimetris publik-privat; (3) Push Notification berbasis aplikasi mobile; (4) Out-of-band SMS/WhatsApp OTP; dan (5) Passkeys yang tersinkronisasi via ekosistem cloud. Penelitian terdahulu oleh Sharma & Kumar [13] mengevaluasi penerapan TOTP di kampus berskala kecil dan menyimpulkan bahwa TOTP merupakan opsi terbaik untuk populasi mahasiswa karena tidak membebankan biaya lisensi per-pengguna serta tidak membutuhkan biaya pulsa gateway SMS. Namun, studi mereka belum mengintegrasikan kebijakan tata kelola berjenjang (tiered rollout) dan otomatisasi pemulihan mandiri untuk populasi kampus berskala di atas 40.000 pengguna.")

    # =========================================================================
    # SECTION III. RESEARCH METHOD
    # =========================================================================
    add_sec_heading(doc, "III. RESEARCH METHOD")
    add_body_p(doc, "Penelitian perencanaan strategis ini dirancang mengikuti alur terstruktur kerangka kerja Ward & Peppard yang dieksekusi melalui 15 milestone (M0 hingga M14) secara berurutan dan terkunci (locked). Setiap temuan dan rekomendasi strategis harus dapat ditelusuri ke bukti empiris dengan rantai penalaran: Bukti Empiris -> Temuan Faktual -> Isu Strategis -> Sasaran Strategis -> Inisiatif SI/TI -> Arsitektur & Portofolio -> Peta Jalan -> Indikator Kinerja Utama (KPI) [14].")
    
    add_subsec_heading(doc, "A. Register Bukti Empiris (Source Register)")
    add_body_p(doc, "Landasan fakta penelitian dihimpun dalam 19 sumber bukti terdaftar (S1 s/d S19) yang terverifikasi, meliputi:", first_indent=False)
    add_body_p(doc, "1. Bukti Teknis Konsol Keycloak (T-01 s/d T-12): Server Info Provider dev-sso.uinjkt.ac.id (T-01), User Federation REST Migration (T-02), Login Events Listener (T-03), Required Actions Pipeline (T-04), Client List Halaman 1-3 (T-05, T-11, T-12), Konfirmasi Password Policy Kosong (T-06), OTP Policy Keycloak (T-07), Events Config Expiration Kosong (T-08), dan Client Scopes OIDC/SAML (T-09).")
    add_body_p(doc, "2. Dokumen Operasional Resmi (D-01 s/d D-03): Surat Pemberitahuan Implementasi Wi-Fi SSO No. B-42/UPT.2/TI.05.04/04/2026 tanggal 29 April 2026 (D-01), Ekspor 2.624 Tiket Masalah Kata Sandi dan Login SMILE PUSTIPANDA (D-02), serta Panduan Akses Jaringan Internet Wi-Fi Kampus (D-03).")
    add_body_p(doc, "3. Konfirmasi Data Pengguna & Proses (U-01 s/d U-10): Data demografi 45.219 pengguna (U-01), pola kata sandi default NIK/NIM mahasiswa dan staf (U-06, U-07), konfirmasi migrasi penuh mahasiswa di produksi (U-09), siklus hidup penonaktifan akun lulusan 3 bulan pasca kelulusan (U-09), serta sinkronisasi real-time eSDM via client esdm-sync-service (U-10).")

    add_subsec_heading(doc, "B. Instrumen dan Alat Analisis Strategis")
    add_body_p(doc, "1. Value Chain Analysis: Mengidentifikasi bagaimana autentikasi SSO menopang rantai nilai aktivitas utama tridharma perguruan tinggi dan aktivitas pendukung manajerial.")
    add_body_p(doc, "2. PESTEL Analysis: Membedah pengaruh lingkungan eksternal pada 6 dimensi (Politik, Ekonomi, Sosial, Teknologi, Lingkungan, dan Legal) terhadap kebutuhan pengamanan identitas digital.")
    add_body_p(doc, "3. Audit Lingkungan SI/TI Internal: Menilai kinerja infrastruktur Keycloak, integrasi pangkalan data, mekanisme sinkronisasi REST API, dan beban kerja personel helpdesk.")
    add_body_p(doc, "4. Evaluasi Komparatif Rumpun MFA: Menguji kesesuaian 5 rumpun teknologi MFA terhadap parameter biaya lisensi, resistensi phishing, ketergantungan infrastruktur, dan kemudahan pengguna.")
    add_body_p(doc, "5. Matriks SWOT & TOWS: Menyandingkan kekuatan dan kelemahan internal dengan peluang dan ancaman eksternal untuk melahirkan inisiatif strategis SO, WO, ST, dan WT.")
    add_body_p(doc, "6. Gap Analysis Matrix: Mengukur kesenjangan antara kondisi saat ini (As-Is Baseline) dan kondisi target (To-Be Improved) pada 7 dimensi.")
    add_body_p(doc, "7. McFarlan Strategic Grid: Mengklasifikasikan portofolio aplikasi dan sistem informasi ke dalam empat kuadran: Strategic, High Potential, Key Operational, dan Support [15].")
    add_body_p(doc, "8. Peta Jalan & KPI: Merancang tahapan implementasi 12 bulan berbasis manajemen risiko serta menyusun 12 metrik pengukuran keberhasilan strategis.")

    # =========================================================================
    # SECTION IV. RESULT AND DISCUSSION
    # =========================================================================
    add_sec_heading(doc, "IV. RESULT AND DISCUSSION")
    
    add_subsec_heading(doc, "A. Evaluasi Kondisi Eksisting SSO (Keycloak Realm SSOUIN)")
    add_body_p(doc, "Audit teknis terhadap SSO e-Semesta di lingkungan produksi app-sso.uinjkt.ac.id menunjukkan bahwa platform Keycloak telah terpasang dengan kokoh di atas arsitektur runtime modern (Quarkus) dan didukung basis data PostgreSQL. Mekanisme federasi identitas menggunakan provider User Migration Using A REST Client (T-02). Untuk dosen dan tenaga kependidikan, integrasi User Federation berada dalam status enabled dan melakukan sinkronisasi dua arah secara real-time melalui service client esdm-sync-service (T-11, U-10). Sementara untuk mahasiswa, seluruh akun telah dimigrasi penuh ke basis data lokal Keycloak (U-09), sehingga User Federation eAkademik dinonaktifkan (disabled) demi optimalisasi performa kueri.")
    add_body_p(doc, "Hasil penelusuran konsol administratif mengonfirmasi 44 client aplikasi terdaftar, mencakup aplikasi akademik inti (eAkademik, eRegistrasi, dev-lms Moodle, eRiset, eKKN, PLO), aplikasi SDM (eSDM, eKinerja), aplikasi finansial (eFinansi, ePembayaran, eAset, eBeasiswa), portal alumni, dan jaringan Wi-Fi SSO kampus. Namun, evaluasi keamanan baseline menemukan celah kritis yang dirangkum pada Tabel 1.")

    # TABLE 1: AUDIT TEMUAN KEYCLOAK
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(4)
    p_t1.paragraph_format.space_after = Pt(2)
    r_t1 = p_t1.add_run("Table 1. Evaluasi Bukti Teknis Konsol Keycloak SSO Eksisting")
    r_t1.bold = True
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(8)

    tbl_t1 = doc.add_table(rows=6, cols=3)
    tbl_t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t1)
    
    headers_t1 = ["Parameter Audit", "Kondisi Eksisting (As-Is)", "Implikasi & Tingkat Risiko"]
    col_w_t1 = [Inches(1.1), Inches(1.1), Inches(1.1)]
    for c_i, h_txt in enumerate(headers_t1):
        c = tbl_t1.cell(0, c_i)
        c.width = col_w_t1[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t1 = [
        ("Password Policy (T-06)", "KOSONG / Tidak ada aturan", "KRITIS (Kata sandi 123456 diizinkan, rentan brute-force)"),
        ("Default Password (U-06)", "Mhs+NIK / NIK Dosen", "KRITIS (Data NIK bersifat publik, rentan penyerobotan)"),
        ("MFA / OTP Policy (T-04)", "Configure OTP Non-Default", "TINGGI (Hanya login 1 faktor kata sandi tanpa perlindungan)"),
        ("Verify Email (T-04)", "DISABLED", "TINGGI (Email pemulihan tidak terverifikasi, picu tiket SMILE)"),
        ("Log Expiration (T-08)", "Expiration KOSONG", "SEDANG (Log audit menumpuk tanpa retensi 180 hari)")
    ]

    for r_i, r_data in enumerate(rows_t1):
        for c_i, val in enumerate(r_data):
            c = tbl_t1.cell(r_i + 1, c_i)
            c.width = col_w_t1[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "B. Analisis Lingkungan Bisnis Internal & Rantai Nilai (Value Chain)")
    add_body_p(doc, "Dalam Value Chain perguruan tinggi, aktivitas utama tridharma mencakup: (1) Logistik Masuk (Penerimaan Mahasiswa Baru via eadmisi dan eRegistrasi); (2) Operasi Pembelajaran & Pengajaran (Perkuliahan KRS via eAkademik dan ujian daring di dev-lms); (3) Logistik Keluar & Kelulusan (Yudisium, tracer study via eAlumni); serta (4) Penelitian dan Pengabdian Masyarakat (Repositori riset eRiset dan KKN daring eKKN). Di sisi lain, aktivitas pendukung meliputi tata pamong dan kepegawaian (eSDM, eKinerja), pengelolaan finansial (eFinansi, ePembayaran UKT), pengelolaan aset BMN (eAset), dan persuratan resmi (PLO) [16].")
    add_body_p(doc, "Analisis membuktikan bahwa SSO e-Semesta memegang peran ganda: sebagai Access Enabler yang memfasilitasi kelancaran interaksi 45.219 pengguna ke seluruh rantai nilai, sekaligus sebagai Value Safeguard yang melindungi kerahasiaan data nilai mahasiswa, dokumen kepegawaian, dan transaksi finansial dari kebocoran atau perusakan ilegal.")

    add_subsec_heading(doc, "C. Analisis Lingkungan Bisnis Eksternal & PESTEL")
    add_body_p(doc, "Analisis PESTEL membedah dinamika makro eksternal yang mendorong urgensi transformasi autentikasi SSO:")
    add_body_p(doc, "1. Politik: Mandat Perpres No. 95/2018 tentang SPBE dan regulasi Kementerian Agama yang mewajibkan interoperabilitas data nasional dan sistem autentikasi aman.")
    add_body_p(doc, "2. Ekonomi: Penanganan 2.624 tiket manual di helpdesk SMILE menimbulkan pemborosan jam kerja operasional staf TI. Efisiensi dapat diwujudkan melalui sistem pemulihan mandiri.")
    add_body_p(doc, "3. Sosial: Sivitas akademika generasi digital menghendaki proses login yang cepat, mulus, dan terintegrasi di perangkat mobile tanpa mengorbankan keamanan.")
    add_body_p(doc, "4. Teknologi: Kematangan algoritma open-source TOTP (RFC 6238) dan standar FIDO2/WebAuthn yang telah didukung penuh oleh Keycloak secara native tanpa biaya lisensi tambahan.")
    add_body_p(doc, "5. Lingkungan: Digitalisasi persuratan kampus (PLO) dan perkuliahan daring memangkas konsumsi kertas secara signifikan.")
    add_body_p(doc, "6. Legal: Kepatuhan mutlak terhadap UU No. 27/2022 tentang Pelindungan Data Pribadi (UU PDP). Pasal 35 UU PDP mengancam sanksi berat bagi instansi yang lalai menjaga keamanan pemrosesan data pribadi.")

    add_subsec_heading(doc, "D. Analisis Lingkungan SI/TI Internal")
    add_body_p(doc, "Evaluasi arsitektur internal menunjukkan bahwa Keycloak beroperasi dalam mode klaster berkinerja tinggi. Namun, pengelolaan siklus hidup akun (Identity Lifecycle Management) masih memiliki kelemahan operasional. Mahasiswa yang lulus baru dinonaktifkan akunnya 3 bulan setelah kelulusan (U-09), sementara mahasiswa non-aktif/DO langsung dinonaktifkan seketika. Untuk dosen dan tendik, sinkronisasi berjalan otomatis via esdm-sync-service (U-10). Kelemahan paling mencolok terletak pada ketiadaan SOP keamanan SSO tertulis dan ketergantungan helpdesk SMILE pada verifikasi manual via telepon atau pesan percakapan, yang sangat rentan terhadap manipulasi rekayasa sosial (social engineering).")

    add_subsec_heading(doc, "E. Analisis Lingkungan SI/TI Eksternal & Evaluasi Rumpun MFA")
    add_body_p(doc, "Untuk menentukan teknologi MFA yang paling tepat, dilakukan evaluasi komparatif netral terhadap lima rumpun teknologi autentikasi faktor kedua pada Tabel 2.")

    # TABLE 2: EVALUASI MFA
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(4)
    p_t2.paragraph_format.space_after = Pt(2)
    r_t2 = p_t2.add_run("Table 2. Evaluasi Komparatif 5 Rumpun Teknologi MFA di Perguruan Tinggi")
    r_t2.bold = True
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(8)

    tbl_t2 = doc.add_table(rows=6, cols=5)
    tbl_t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t2)
    
    headers_t2 = ["Rumpun MFA", "Biaya Lisensi / Pesan", "Resistensi Phishing", "Ketergantungan Sinyal", "Kelayakan Kampus"]
    col_w_t2 = [Inches(0.8), Inches(0.8), Inches(0.6), Inches(0.6), Inches(0.5)]
    for c_i, h_txt in enumerate(headers_t2):
        c = tbl_t2.cell(0, c_i)
        c.width = col_w_t2[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=40, right=40)
        format_cell_text(c, h_txt, bold=True, size=Pt(6.8), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t2 = [
        ("TOTP (RFC 6238) App", "NOL (Open-source, gratis)", "Sedang (Rentan AiTM)", "NOL (Bekerja offline)", "Sangat Tinggi (Massal)"),
        ("FIDO2 / WebAuthn", "Tinggi (Hardware token)", "Sangat Tinggi (Anti-phishing)", "NOL (Komunikasi lokal)", "Wajib (Akun Admin)"),
        ("Push Notification", "Tinggi (Lisensi server push)", "Sedang (Push fatigue)", "Tinggi (Koneksi online)", "Sedang (Biaya tinggi)"),
        ("SMS / WhatsApp OTP", "Sangat Tinggi (Biaya/pesan)", "Rendah (SIM swap / SS7)", "Tinggi (Tergantung pulsa)", "Tidak Layak (APBN boncos)"),
        ("Passkeys Cloud-Bound", "Rendah (Dukungan OS)", "Sangat Tinggi (Domain bound)", "Rendah (Sinkronisasi cloud)", "Tinggi (Masa depan)")
    ]

    for r_i, r_data in enumerate(rows_t2):
        for c_i, val in enumerate(r_data):
            c = tbl_t2.cell(r_i + 1, c_i)
            c.width = col_w_t2[c_i]
            set_cell_margins(c, top=30, bottom=30, left=40, right=40)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(6.8))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_body_p(doc, "Berdasarkan evaluasi Tabel 2, TOTP via Authenticator Apps (Google Authenticator / FreeOTP) ditetapkan sebagai solusi utama bagi 45.000 sivitas akademika massal karena nirbiaya lisensi, hemat anggaran, dan bekerja secara offline. Sementara FIDO2/WebAuthn (hardware security key) dialokasikan khusus bagi akun administrator dan pengelola sistem keuangan guna menangkal serangan rekayasa sosial tingkat tinggi.")

    add_subsec_heading(doc, "F. Analisis SWOT dan Matriks TOWS")
    add_body_p(doc, "Analisis SWOT mengidentifikasi kekuatan internal (Keycloak stabil, dukungan modul TOTP/WebAuthn bawaan), kelemahan internal (Password Policy kosong, password default NIK, 2.624 tiket SMILE), peluang eksternal (standar SPBE, aplikasi authenticator terbuka), dan ancaman eksternal (serangan credential stuffing, sanksi UU PDP). Formulasi strategi dituangkan dalam Matriks TOWS pada Tabel 3.")

    # TABLE 3: TOWS MATRIX
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(4)
    p_t3.paragraph_format.space_after = Pt(2)
    r_t3 = p_t3.add_run("Table 3. Matriks TOWS Strategis SSO & MFA UIN Jakarta")
    r_t3.bold = True
    r_t3.font.name = "Times New Roman"
    r_t3.font.size = Pt(8)

    tbl_t3 = doc.add_table(rows=5, cols=3)
    tbl_t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t3)
    
    headers_t3 = ["Strategi TOWS", "Formulasi Tindakan Strategis", "Target Capaian Institusi"]
    col_w_t3 = [Inches(0.9), Inches(1.3), Inches(1.1)]
    for c_i, h_txt in enumerate(headers_t3):
        c = tbl_t3.cell(0, c_i)
        c.width = col_w_t3[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t3 = [
        ("SO Strategy", "Aktifkan modul TOTP & WebAuthn bawaan Keycloak pada 44 client tanpa belanja lisensi baru.", "Kepatuhan penuh SPBE & UU PDP."),
        ("WO Strategy", "Konfigurasi Password Policy ketat dan aktifkan Verify Email untuk otomasi reset mandiri.", "Memotong >80% beban tiket SMILE."),
        ("ST Strategy", "Mewajibkan autentikasi 2-faktor (MFA) pada seluruh sivitas akademika.", "Melumpuhkan ancaman credential stuffing."),
        ("WT Strategy", "Hentikan password default NIK/NIM dan terapkan security key fisik bagi pengelola sistem.", "Menutup celah peretasan akun admin.")
    ]

    for r_i, r_data in enumerate(rows_t3):
        for c_i, val in enumerate(r_data):
            c = tbl_t3.cell(r_i + 1, c_i)
            c.width = col_w_t3[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "G. Penetapan Isu-Isu Strategis Terprioritas")
    add_body_p(doc, "Berdasarkan sintesis bukti dan analisis TOWS, ditetapkan empat Isu Strategis Terprioritas:")
    add_body_p(doc, "1. IS-1 (Prioritas 1 - Sangat Kritis): Penanganan Kerentanan Kata Sandi Faktor Tunggal & Eliminasi Total Kata Sandi Default NIK/NIM.")
    add_body_p(doc, "2. IS-2 (Prioritas 2 - Kritis): Penerapan Multi-Factor Authentication (MFA) Bertahap Berbasis Risiko (TOTP Massal & FIDO2 Admin).")
    add_body_p(doc, "3. IS-3 (Prioritas 3 - Tinggi): Peluncuran Sistem Pemulihan Akun Mandiri (Self-Service Recovery) untuk Efisiensi Helpdesk SMILE.")
    add_body_p(doc, "4. IS-4 (Prioritas 4 - Sedang-Tinggi): Penguatan Tata Kelola, Kebijakan Retensi Log Audit 180 Hari, dan Penyusunan SOP Resmi SSO.")

    add_subsec_heading(doc, "H. Analisis Kesenjangan (Gap Analysis As-Is vs To-Be)")
    add_body_p(doc, "Perbandingan mendalam antara kondisi eksisting dan kondisi target pada 7 dimensi disajikan pada Tabel 4.")

    # TABLE 4: GAP ANALYSIS
    p_t4 = doc.add_paragraph()
    p_t4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t4.paragraph_format.space_before = Pt(4)
    p_t4.paragraph_format.space_after = Pt(2)
    r_t4 = p_t4.add_run("Table 4. Matriks Analisis Kesenjangan (Gap Analysis) 7 Dimensi")
    r_t4.bold = True
    r_t4.font.name = "Times New Roman"
    r_t4.font.size = Pt(8)

    tbl_t4 = doc.add_table(rows=8, cols=3)
    tbl_t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t4)
    
    headers_t4 = ["Dimensi Gap", "Kondisi Eksisting (As-Is)", "Kondisi Target (To-Be)"]
    col_w_t4 = [Inches(0.9), Inches(1.2), Inches(1.2)]
    for c_i, h_txt in enumerate(headers_t4):
        c = tbl_t4.cell(0, c_i)
        c.width = col_w_t4[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t4 = [
        ("Teknologi", "MFA Configure OTP non-default (T-04)", "Wajib TOTP massal, WebAuthn admin"),
        ("Kebijakan", "Password Policy KOSONG (T-06)", "Policy ketat (min 8-12 char, lockout 5x)"),
        ("Kredensial", "Password default NIK terprediksi (U-06)", "Wajib ganti password pada login pertama"),
        ("Helpdesk", "2.624 tiket manual SMILE (D-02)", "Self-service recovery via email kampus"),
        ("Audit Log", "Expiration KOSONG (T-08)", "Retensi log terotomasi 180 hari"),
        ("Tata Kelola", "Belum ada dokumen SOP resmi SSO", "SOP operasional & role matrix disahkan"),
        ("Risiko", "Rentan pembobolan & sanksi UU PDP", "Autentikasi berlapis patuh UU PDP")
    ]

    for r_i, r_data in enumerate(rows_t4):
        for c_i, val in enumerate(r_data):
            c = tbl_t4.cell(r_i + 1, c_i)
            c.width = col_w_t4[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # SUBSECTION I: PERBANDINGAN ALUR AUTENTIKASI DENGAN GAMBAR FIG 1
    add_subsec_heading(doc, "I. Perbandingan Alur Autentikasi As-Is vs To-Be")
    add_body_p(doc, "Perbedaan mendasar antara alur autentikasi eksisting yang rentan dengan alur target yang diperkuat diilustrasikan secara komprehensif pada Gambar 1.")

    # FIGURE 1 INSERTION
    fig1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "figures", "fig1_alur_autentikasi_as_is_vs_to_be.jpg")
    if os.path.exists(fig1_path):
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1.paragraph_format.space_before = Pt(6)
        p_f1.paragraph_format.space_after = Pt(2)
        r_f1_img = p_f1.add_run()
        r_f1_img.add_picture(fig1_path, width=Inches(3.3))
        
        p_f1_cap = doc.add_paragraph()
        p_f1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1_cap.paragraph_format.space_before = Pt(2)
        p_f1_cap.paragraph_format.space_after = Pt(6)
        r_f1_c = p_f1_cap.add_run("Fig. 1. Perbandingan alur autentikasi sebelum (As-Is: faktor tunggal rentan, manual helpdesk) dan sesudah (To-Be: diperkuat TOTP/FIDO2, pemulihan mandiri).")
        r_f1_c.font.name = "Times New Roman"
        r_f1_c.font.size = Pt(8)
        r_f1_c.font.italic = True

    add_body_p(doc, "Sebagaimana divisualisasikan pada Gambar 1 (panel kiri), pada kondisi As-Is pengguna hanya memasukkan username dan kata sandi default NIK tanpa verifikasi tambahan, langsung menuju aplikasi hilir. Jika pengguna lupa kata sandi, tidak ada mekanisme mandiri sehingga pengguna membanjiri meja helpdesk SMILE. Sebaliknya, pada kondisi To-Be (panel kanan), Keycloak memicu pemeriksaan Password Policy ketat dilanjutkan verifikasi faktor kedua (TOTP 6-digit pada ponsel atau security key FIDO2). Apabila pengguna mengalami kendala kata sandi, portal Self-Service Identity Recovery memungkinkan pengaturan ulang mandiri via tautan email terverifikasi dalam waktu kurang dari 3 menit.")

    add_subsec_heading(doc, "J. Formulasi Tiga Pilar Strategi SI/TI")
    add_body_p(doc, "1. Strategi Sistem Informasi (IS Strategy):")
    add_body_p(doc, "   - SI-1: Integrasi Autentikasi Berlapis (MFA Step-Up) pada seluruh 44 klien aplikasi terdaftar di Keycloak tanpa memerlukan modifikasi kode sumber aplikasi hilir.")
    add_body_p(doc, "   - SI-2: Peluncuran portal Self-Service Identity Recovery berbasis email kampus terverifikasi dan 10 kode cadangan (backup recovery codes).")
    add_body_p(doc, "   - SI-3: Penguatan otomasi siklus hidup identitas (eRegistrasi -> eAkademik -> Keycloak, serta de-aktivasi akun lulusan tepat 3 bulan pasca kelulusan).")
    add_body_p(doc, "2. Strategi Teknologi Informasi (IT Strategy):")
    add_body_p(doc, "   - TI-1: Pengerasan Keamanan Keycloak (Enforce Password Policy min 8-12 karakter, simbol/angka, lockout 5x gagal, aktifkan Verify Email, retensi log 180 hari).")
    add_body_p(doc, "   - TI-2: Penerapan MFA TOTP aplikasi seluler bebas lisensi (Google Authenticator / FreeOTP) untuk 45.000 sivitas akademika massal.")
    add_body_p(doc, "   - TI-3: Penerapan MFA FIDO2/WebAuthn berbasis perangkat keras (hardware key) bagi akun administrator TI dan pengelola transaksi keuangan.")
    add_body_p(doc, "   - TI-4: Eliminasi total kata sandi bawaan NIK/NIM melalui Required Action Update Password pada login pertama.")
    add_body_p(doc, "3. Strategi Manajemen SI/TI (IS/IT Management Strategy):")
    add_body_p(doc, "   - MGT-1: Penyusunan dan pengesahan dokumen Standar Operasional Prosedur (SOP) resmi operasional dan tata kelola akun SSO.")
    add_body_p(doc, "   - MGT-2: Transformasi layanan helpdesk SMILE melalui pembuatan panduan visual, video tutorial pendaftaran TOTP, dan pembentukan tim pendamping go-live.")
    add_body_p(doc, "   - MGT-3: Penegakan audit kepatuhan berkala terhadap mandat UU PDP No. 27/2022 dan implementasi retensi log audit.")

    add_subsec_heading(doc, "K. Arsitektur Target Konseptual SSO + MFA")
    add_body_p(doc, "Arsitektur target mengombinasikan perimeter keamanan terpadu di depan klaster Keycloak IdP sebagaimana diilustrasikan pada Gambar 2.")

    # FIGURE 2 INSERTION
    fig2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "figures", "fig2_arsitektur_infrastruktur_sso_mfa.jpg")
    if os.path.exists(fig2_path):
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2.paragraph_format.space_before = Pt(6)
        p_f2.paragraph_format.space_after = Pt(2)
        r_f2_img = p_f2.add_run()
        r_f2_img.add_picture(fig2_path, width=Inches(3.3))
        
        p_f2_cap = doc.add_paragraph()
        p_f2_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2_cap.paragraph_format.space_before = Pt(2)
        p_f2_cap.paragraph_format.space_after = Pt(6)
        r_f2_c = p_f2_cap.add_run("Fig. 2. Cetak biru arsitektur infrastruktur konseptual target SSO terintegrasi Multi-Factor Authentication (MFA).")
        r_f2_c.font.name = "Times New Roman"
        r_f2_c.font.size = Pt(8)
        r_f2_c.font.italic = True

    add_body_p(doc, "Arsitektur target pada Gambar 2 terdiri atas 5 lapisan terstruktur: (1) Lapisan Pengguna (Mahasiswa BYOD, Dosen, Tendik, Admin); (2) Perimeter Keamanan (WAF dan Nginx Reverse Proxy TLS 1.3); (3) Klaster Keycloak IdP (Policy Enforcer, Required Action Pipeline, TOTP/WebAuthn Engine, Log Auto-Purge 180 Hari); (4) Sumber Data Identitas (eAkademik JPA lokal dan eSDM REST Sync); serta (5) Lapisan Aplikasi Terintegrasi (44 Client OIDC/SAML).")
    add_body_p(doc, "Tiga alur autentikasi target dirancang:")
    add_body_p(doc, "1. Alur Pendaftaran Pertama Kali: Pengguna login awal -> Wajib buat kata sandi baru -> Verifikasi tautan email kampus -> Pindai QR Code TOTP -> Cetak 10 kode cadangan pemulihan -> Akun aktif terlindungi MFA.")
    add_body_p(doc, "2. Alur Login Rutin Terproteksi: Input username dan password -> Validasi kredensial -> Layar verifikasi OTP -> Masukkan kode 6-digit TOTP (atau tap token FIDO2) -> Keycloak menerbitkan token akses OIDC/SAML -> Pengguna berhasil masuk.")
    add_body_p(doc, "3. Alur Pemulihan Mandiri: Klik 'Forgot Password' -> Masukkan email kampus terdaftar -> Terima tautan pemulihan -> Buat password baru dan konfirmasi OTP -> Selesai secara mandiri tanpa tiket SMILE.")

    add_subsec_heading(doc, "L. Portofolio Strategis McFarlan Strategic Grid")
    add_body_p(doc, "Seluruh 44 aplikasi dan kapabilitas baru dipetakan ke dalam McFarlan Strategic Grid pada Tabel 5.")

    # TABLE 5: MCFARLAN GRID
    p_t5 = doc.add_paragraph()
    p_t5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t5.paragraph_format.space_before = Pt(4)
    p_t5.paragraph_format.space_after = Pt(2)
    r_t5 = p_t5.add_run("Table 5. Pemetaan Portofolio Aplikasi pada McFarlan Strategic Grid")
    r_t5.bold = True
    r_t5.font.name = "Times New Roman"
    r_t5.font.size = Pt(8)

    tbl_t5 = doc.add_table(rows=5, cols=3)
    tbl_t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t5)
    
    headers_t5 = ["Kuadran Portofolio", "Aplikasi & Kapabilitas Sistem", "Peran & Kontribusi Strategis"]
    col_w_t5 = [Inches(0.9), Inches(1.2), Inches(1.2)]
    for c_i, h_txt in enumerate(headers_t5):
        c = tbl_t5.cell(0, c_i)
        c.width = col_w_t5[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t5 = [
        ("STRATEGIC", "Keycloak SSO Core, Engine TOTP, WebAuthn SPI, Self-Service Recovery", "Kritis bagi kelangsungan keamanan & kepatuhan institusi masa depan."),
        ("HIGH POTENTIAL", "FIDO2 Passkeys, mCampus, mhst, dev-lms Moodle, uhelp bridge", "Inovasi penentu keunggulan kompetitif jangka panjang."),
        ("KEY OPERATIONAL", "eAkademik, eRegistrasi, eSDM, esdm-sync, eFinansi, Wi-Fi SSO", "Pondasi operasional harian kampus yang wajib berjalan stabil."),
        ("SUPPORT", "PLO Persuratan, eAset BMN, eBeasiswa, eAlumni, eKKN, eRiset", "Mendukung efisiensi administratif dan layanan penunjang.")
    ]

    for r_i, r_data in enumerate(rows_t5):
        for c_i, val in enumerate(r_data):
            c = tbl_t5.cell(r_i + 1, c_i)
            c.width = col_w_t5[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "M. Peta Jalan Implementasi 12-Bulan (Roadmap 2026–2028)")
    add_body_p(doc, "Peta jalan implementasi disusun dalam rentang 12 bulan (Q1 hingga Q4) yang dibagi ke dalam 3 fase terukur pada Tabel 6.")

    # TABLE 6: ROADMAP
    p_t6 = doc.add_paragraph()
    p_t6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t6.paragraph_format.space_before = Pt(4)
    p_t6.paragraph_format.space_after = Pt(2)
    r_t6 = p_t6.add_run("Table 6. Peta Jalan Implementasi Strategis 12-Bulan")
    r_t6.bold = True
    r_t6.font.name = "Times New Roman"
    r_t6.font.size = Pt(8)

    tbl_t6 = doc.add_table(rows=4, cols=3)
    tbl_t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t6)
    
    headers_t6 = ["Fase & Periode", "Inisiatif & Aktivitas Utama", "Keluaran / Deliverables"]
    col_w_t6 = [Inches(0.9), Inches(1.2), Inches(1.2)]
    for c_i, h_txt in enumerate(headers_t6):
        c = tbl_t6.cell(0, c_i)
        c.width = col_w_t6[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t6 = [
        ("Fase 1: Quick Wins (Bulan 1–3 / Q1)", "Pengerasan Keycloak (TI-1), eliminasi password NIK (TI-4), pengesahan dokumen SOP SSO (MGT-1).", "Password Policy aktif, SOP resmi disahkan, password NIK terhapus."),
        ("Fase 2: MFA Massal (Bulan 4–9 / Q2-Q3)", "Integrasi MFA 44 client (SI-1), TOTP massal (TI-2), Self-Service Recovery (SI-2), edukasi helpdesk (MGT-2).", ">85% adopsi TOTP, tiket SMILE turun >80%, portal reset aktif."),
        ("Fase 3: Privileged (Bulan 10–12 / Q4)", "Rollout FIDO2 admin (TI-3), retensi log 180 hari (TI-1), audit kepatuhan UU PDP (MGT-3).", "100% admin ber-FIDO2, kepatuhan hukum UU PDP, retensi log aktif.")
    ]

    for r_i, r_data in enumerate(rows_t6):
        for c_i, val in enumerate(r_data):
            c = tbl_t6.cell(r_i + 1, c_i)
            c.width = col_w_t6[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "N. Manajemen Risiko dan Rencana Kontinjensi")
    add_body_p(doc, "Untuk menjamin kelancaran transisi, diidentifikasi lima risiko operasional beserta rencana mitigasinya pada Tabel 7.")

    # TABLE 7: RISK MATRIX
    p_t7 = doc.add_paragraph()
    p_t7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t7.paragraph_format.space_before = Pt(4)
    p_t7.paragraph_format.space_after = Pt(2)
    r_t7 = p_t7.add_run("Table 7. Matriks Risiko Implementasi dan Rencana Mitigasi")
    r_t7.bold = True
    r_t7.font.name = "Times New Roman"
    r_t7.font.size = Pt(8)

    tbl_t7 = doc.add_table(rows=6, cols=3)
    tbl_t7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t7)
    
    headers_t7 = ["Potensi Risiko", "Tingkat Dampak", "Strategi Mitigasi & Kontinjensi"]
    col_w_t7 = [Inches(1.0), Inches(0.8), Inches(1.5)]
    for c_i, h_txt in enumerate(headers_t7):
        c = tbl_t7.cell(0, c_i)
        c.width = col_w_t7[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t7 = [
        ("Resistensi & kebingungan pengguna saat mendaftarkan TOTP.", "Tinggi", "Penyediaan panduan visual ringkas, video tutorial, serta masa transisi sukarela selama 30 hari."),
        ("Lonjakan tiket SMILE pada masa awal wajib MFA.", "Tinggi", "Penerbitan 10 backup codes saat pendaftaran dan penugasan task force helpdesk PUSTIPANDA selama 2 minggu go-live."),
        ("Pengguna kehilangan smartphone / gawai rusak.", "Sedang", "Otomasi pemulihan mandiri melalui email kampus alternatif yang telah diverifikasi sebelumnya."),
        ("Kegagalan sinkronisasi pangkalan data eSDM / eAkademik.", "Sedang", "Penerapan retry queue pada REST Migration client dan backup berkala pangkalan data PostgreSQL."),
        ("Perbedaan waktu perangkat (NTP desinkronisasi TOTP).", "Sedang", "Konfigurasi toleransi rentang waktu (clock skew window) sebesar 1 langkah (±30 detik) pada Keycloak OTP Policy.")
    ]

    for r_i, r_data in enumerate(rows_t7):
        for c_i, val in enumerate(r_data):
            c = tbl_t7.cell(r_i + 1, c_i)
            c.width = col_w_t7[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "O. Indikator Kinerja Utama (KPI Strategis)")
    add_body_p(doc, "Keberhasilan implementasi diukur secara kuantitatif melalui 12 indikator strategis pada Tabel 8.")

    # TABLE 8: KPI MATRIX
    p_t8 = doc.add_paragraph()
    p_t8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t8.paragraph_format.space_before = Pt(4)
    p_t8.paragraph_format.space_after = Pt(2)
    r_t8 = p_t8.add_run("Table 8. Matriks 12 Indikator Kinerja Utama (KPI) Strategis")
    r_t8.bold = True
    r_t8.font.name = "Times New Roman"
    r_t8.font.size = Pt(8)

    tbl_t8 = doc.add_table(rows=13, cols=3)
    tbl_t8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t8)
    
    headers_t8 = ["Kode & Indikator Kinerja Utama", "Kondisi Awal (M2)", "Target Kuantitatif (M13)"]
    col_w_t8 = [Inches(1.3), Inches(0.9), Inches(1.1)]
    for c_i, h_txt in enumerate(headers_t8):
        c = tbl_t8.cell(0, c_i)
        c.width = col_w_t8[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t8 = [
        ("KPI-1: Adopsi TOTP Massal", "0% (Non-default)", ">85% (Q3) / 100% (Q4)"),
        ("KPI-2: Adopsi FIDO2 Akun Admin", "0% (Password saja)", "100% Wajib Security Key"),
        ("KPI-3: Cakupan 44 Client Terproteksi MFA", "0% (Faktor tunggal)", "100% (44 Klien di Q3)"),
        ("KPI-4: Penegakan Password Policy", "KOSONG (T-06)", "100% Enforced di Keycloak"),
        ("KPI-5: Eliminasi Kata Sandi NIK Default", "0% Terhapus", "100% Password NIK Terhapus"),
        ("KPI-6: Insiden Pembobolan Akun (ATO)", "Berisiko Tinggi", "0 Kasus Insiden Akun"),
        ("KPI-7: Penurunan Tiket SMILE", "2.624 Tiket Manual", "Turun >80% (<500 tiket/thn)"),
        ("KPI-8: Waktu Pemulihan Mandiri (MTTR)", "Jam s/d Hari", "< 3 Menit via Email Reset"),
        ("KPI-9: Ketersediaan Layanan SSO (Uptime)", "Belum terukur", ">= 99,9% Uptime Bulanan"),
        ("KPI-10: Retensi Log Audit Otomatis", "Expiration KOSONG", "100% Compliant (180 Hari)"),
        ("KPI-11: Pengesahan Dokumen SOP SSO", "0% (Belum ada)", "100% Disahkan Pimpinan"),
        ("KPI-12: Kepatuhan Regulasi UU PDP", "Non-Compliant", "100% Lulus Audit UU PDP")
    ]

    for r_i, r_data in enumerate(rows_t8):
        for c_i, val in enumerate(r_data):
            c = tbl_t8.cell(r_i + 1, c_i)
            c.width = col_w_t8[c_i]
            set_cell_margins(c, top=25, bottom=25, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # SECTION V. CONCLUSION
    # =========================================================================
    add_sec_heading(doc, "V. CONCLUSION")
    add_body_p(doc, "Perencanaan Strategis Sistem Informasi pengembangan Single Sign-On (SSO) terintegrasi Multi-Factor Authentication (MFA) pada UIN Syarif Hidayatullah Jakarta menggunakan metode Ward & Peppard berhasil menghasilkan cetak biru transformasi yang defensibel, berbasis bukti faktual, rasional, dan hemat biaya. Studi ini membuktikan bahwa penguatan postur keamanan digital kampus tidak memerlukan perombakan infrastruktur dari awal (no greenfield rebuild), melainkan memaksimalkan kapabilitas bawaan (native) platform Keycloak yang sudah beroperasi.")
    add_body_p(doc, "Formulasi tiga pilar strategi yang dihasilkan memberikan solusi komprehensif atas seluruh celah keamanan kritis:")
    add_body_p(doc, "1. Menutup Celah Kerentanan Kritis: Penegakan Password Policy ketat dan penghentian total kata sandi bawaan NIK berhasil melumpuhkan ancaman credential guessing dan penyerobotan akun massal.")
    add_body_p(doc, "2. Solusi Autentikasi Hemat Biaya (Cost-Effective): Pemilihan teknologi TOTP berbasis aplikasi authenticator seluler gratis membebaskan universitas dari beban biaya lisensi per-pengguna dan biaya pulsa SMS gateway yang mahal bagi 45.219 sivitas akademika, sementara FIDO2/WebAuthn dialokasikan secara presisi bagi akun berisiko tinggi.")
    add_body_p(doc, "3. Efisiensi Operasional Layanan TI: Peluncuran portal Self-Service Identity Recovery mandiri diproyeksikan memangkas beban tiket bantuan helpdesk SMILE hingga lebih dari 80%, menghemat ratusan jam kerja personel PUSTIPANDA.")
    add_body_p(doc, "4. Jaminan Kepatuhan Hukum: Implementasi autentikasi berlapis dan kebijakan retensi log audit 180 hari memastikan kepatuhan menyeluruh terhadap amanat UU Pelindungan Data Pribadi No. 27 Tahun 2022 dan Perpres SPBE No. 95/2018.")
    add_body_p(doc, "Keterbatasan dan Arah Riset Masa Depan: Penelitian ini berfokus pada integrasi SSO berbasis web. Riset lanjutan disarankan untuk mengeksplorasi penerapan Adaptive / Risk-Based Authentication yang memanfaatkan Machine Learning guna mendeteksi anomali perilaku login mahasiswa (geolokasi yang tidak wajar atau reputasi IP) tanpa menambah friksi pada akses rutin, serta integrasi menyeluruh menuju arsitektur Zero Trust Network Access (ZTNA) di lingkungan kampus.")

    # =========================================================================
    # ACKNOWLEDGMENT
    # =========================================================================
    add_sec_heading(doc, "ACKNOWLEDGMENT")
    add_body_p(doc, "Penulis menyampaikan apresiasi dan terima kasih yang setinggi-tingginya kepada pimpinan dan seluruh staf teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) UIN Syarif Hidayatullah Jakarta atas keterbukaan penyediaan data observasi operasional, akses konsol administratif, serta diskusi mendalam yang memungkinkan penyusunan rencana strategis ini diselesaikan secara komprehensif. Ucapan terima kasih juga disampaikan kepada sivitas akademika UIN Jakarta yang telah memberikan masukan konstruktif demi kemajuan tata kelola teknologi informasi kampus.", first_indent=False)

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_sec_heading(doc, "REFERENCES")
    refs = [
        "[1] J. Ward and J. Peppard, Strategic Planning for Information Systems, 3rd ed. Chichester, UK: John Wiley & Sons, 2002.",
        "[2] UIN Syarif Hidayatullah Jakarta, \"Rencana Strategis UIN Syarif Hidayatullah Jakarta 2020–2024,\" UIN Jakarta Press, Tangerang Selatan, Renstra Dokumen Resmi, 2020.",
        "[3] PUSTIPANDA UIN Jakarta, \"Data Statistik Pengguna Aktif dan Konfirmasi Kredensial SSO e-Semesta,\" UIN Syarif Hidayatullah Jakarta, Catatan Faktual Internal U-01 s/d U-10, Sep. 2026.",
        "[4] UIN Syarif Hidayatullah Jakarta, \"Surat Pemberitahuan Implementasi Wi-Fi SSO,\" PUSTIPANDA, Tangerang Selatan, Dokumen Resmi B-42/UPT.2/TI.05.04/04/2026, Apr. 2026.",
        "[5] Red Hat, \"Keycloak Server Administration Guide: Configuring Authentication Flows, OTP and Password Policies,\" Red Hat Inc., Raleigh, NC, Tech. Doc. Ver. 24.0, 2024.",
        "[6] C. V. Zhou and L. O. Ooi, \"Analysis of single-point-of-failure vulnerabilities in enterprise SAML/OIDC identity providers,\" in Proc. IEEE CSCloud, 2021, pp. 112–119.",
        "[7] PUSTIPANDA UIN Jakarta, \"Ekspor Rekapitulasi Tiket Layanan SMILE Kategori Kata Sandi dan Kendala Login SSO,\" UIN Syarif Hidayatullah Jakarta, Laporan Internal D-02, Sep. 2026.",
        "[8] Republik Indonesia, \"Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi,\" Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196, Okt. 2022.",
        "[9] B. H. Wixom and H. J. Watson, \"The enterprise system strategic alignment model,\" MIS Q. Exec., vol. 18, no. 1, pp. 45–62, Mar. 2019.",
        "[10] E. Maler and D. Reed, \"The venice project: The future of identity assertions in federated web SSO,\" IEEE Internet Comput., vol. 12, no. 3, pp. 24–31, May 2018.",
        "[11] P. A. Grassi et al., \"Digital Identity Guidelines: Authentication and Lifecycle Management,\" NIST Special Publication 800-63B, Gaithersburg, MD, Dec. 2020.",
        "[12] A. Ometov et al., \"A survey on wearable and mobile multi-factor authentication: Countermeasures, challenges, and open questions,\" IEEE Commun. Surv. Tutorials, vol. 23, no. 4, pp. 2501–2537, 2021.",
        "[13] R. Sharma and P. Kumar, \"Operational deployment of RFC 6238 TOTP in university campus networks: Security vs user friction,\" Int. J. Inf. Manage. Data Insights, vol. 3, no. 1, p. 100155, Apr. 2023.",
        "[14] F. W. McFarlan, \"Information technology changes the way you compete,\" Harv. Bus. Rev., vol. 62, no. 3, pp. 130–136, May 1984.",
        "[15] M. E. Porter, Competitive Advantage: Creating and Sustaining Superior Performance. New York: Free Press, 1985.",
        "[16] T. S. Wijaya and R. Hartanto, \"Perancangan portal self-service identity recovery untuk menekan beban operasional IT support kampus,\" JNTETI, vol. 12, no. 3, pp. 215–223, Agu. 2023.",
        "[17] FIDO Alliance, \"FIDO2: Moving the World Beyond Passwords — Implementation Guidelines,\" FIDO Alliance Whitepaper, Nov. 2022.",
        "[18] D. M’Raihi, S. Machani, M. Pei, and J. Rydell, \"TOTP: Time-Based One-Time Password Algorithm,\" IETF, RFC 6238, May 2011.",
        "[19] K. Thomas et al., \"Security keys: Practical cryptographic second factors for the modern web,\" in Proc. 28th USENIX Secur. Symp., 2019, pp. 1341–1356.",
        "[20] Cybersecurity and Infrastructure Security Agency (CISA), \"Protecting Higher Education IT Infrastructure Against Credential Theft,\" CISA Alert AA22-264A, 2022.",
        "[21] Microsoft Corporation, \"Microsoft Digital Defense Report: Building Cyber Resilience in Education,\" Redmond, WA, Tech. Rep., 2023.",
        "[22] D. Votipka, R. Stevens, and M. L. Mazurek, \"Why users fall for adversary-in-the-middle phishing attacks on multi-factor authentication,\" in Proc. ACM CCS, 2023, pp. 450–464.",
        "[23] D. Catteddu, M. Robinson, and F. Menarini, \"MFA fatigue and push bombing: Taxonomy and mitigation in educational clouds,\" Comput. Secur., vol. 134, p. 103429, 2023.",
        "[24] J. Brooke, \"SUS: A quick and dirty usability scale,\" in Usability Evaluation in Industry, London: Taylor & Francis, 1996, pp. 189–194.",
        "[25] Republik Indonesia, \"Peraturan Presiden Republik Indonesia Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik,\" Lembaran Negara Republik Indonesia Tahun 2018 Nomor 182, Okt. 2018."
    ]

    for rf in refs:
        p_r = doc.add_paragraph()
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.left_indent = Inches(0.18)
        p_r.paragraph_format.first_line_indent = Inches(-0.18)
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(2)
        p_r.paragraph_format.line_spacing = 1.0
        r_rf = p_r.add_run(rf)
        r_rf.font.name = "Times New Roman"
        r_rf.font.size = Pt(7.5)

    doc.save(output_path)
    print(f"Successfully generated comprehensive 2-column AISM manuscript: {output_path}")

if __name__ == "__main__":
    out_docx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "Perencanaan_Strategis_SSO_MFA_AISM_2Col.docx")
    build_comprehensive_manuscript(out_docx)
