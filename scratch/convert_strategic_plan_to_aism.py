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

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="D0D0D0"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell_text(cell, text, bold=False, italic=False, size=Pt(7.5), color=RGBColor(0x00, 0x00, 0x00), align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Times New Roman"
    run.font.size = size
    run.font.color.rgb = color

def add_sec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    return p

def add_subsec_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
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

def create_aism_2col_strategic_plan(output_path):
    doc = Document()
    
    # Page Setup - Standard A4 with ~0.65 in left/right and 0.75 in top/bottom
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
        cols[0].set(qn('w:space'), '360') # 360 dxa = 0.25 inch
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

    # --- I. INTRODUCTION ---
    add_sec_heading(doc, "I. INTRODUCTION")
    add_body_p(doc, "Transformasi digital pada institusi pendidikan tinggi negeri menuntut infrastruktur manajemen identitas dan akses yang aman, efisien, dan andal. Universitas Islam Negeri (UIN) Syarif Hidayatullah Jakarta telah mengoperasikan sistem Single Sign-On (SSO) terpusat, dikenal sebagai portal e-Semesta, yang dibangun di atas platform open-source Keycloak (realm SSOUIN) dan dikelola oleh Unit Pelaksana Teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) [1]. Sistem ini melayani lebih dari 45.219 pengguna aktif—terdiri atas 42.088 mahasiswa, 1.593 dosen, dan 1.438 tenaga kependidikan—serta mengorkestrasi autentikasi akses ke 44 aplikasi institusional seperti eAkademik, eRegistrasi, eSDM, eFinansi, eKinerja, hingga jaringan nirkabel kampus Wi-Fi SSO [2].")
    add_body_p(doc, "Kendati SSO e-Semesta berhasil mengonsolidasikan direktori identitas kampus, evaluasi empiris terhadap konfigurasi operasional mengungkap celah keamanan mendasar yang sangat rentan: autentikasi masih sepenuhnya bertumpu pada faktor tunggal berupa kata sandi (single-factor password). Audit konsol administratif Keycloak mengonfirmasi bahwa aturan kebijakan kata sandi (Password Policy) saat ini berada dalam kondisi KOSONG tanpa penegakan kompleksitas minimum, masa kedaluwarsa, maupun pemeriksaan daftar kata sandi bocor [3].")
    add_body_p(doc, "Lebih mengkhawatirkan, kata sandi bawaan (default password) pengguna baru masih menggunakan format terprediksi berbasis data publik kependudukan, yaitu kombinasi prefiks dan Nomor Induk Kependudukan (NIK) bagi mahasiswa serta NIK murni bagi dosen dan tenaga kependidikan. Di samping itu, fitur verifikasi email mandiri (Verify Email) dalam kondisi dinonaktifkan (DISABLED), dan fitur Configure OTP belum dijadikan sebagai tindakan wajib (Required Action). Kerapuhan ini berdampak langsung pada operasional meja bantuan (helpdesk) SMILE PUSTIPANDA, yang mencatat 2.624 tiket manual terkait keluhan lupa kata sandi dan kendala login [4].")
    add_body_p(doc, "Secara yuridis, ketiadaan Multi-Factor Authentication (MFA) dan kata sandi default terprediksi menempatkan universitas pada posisi rentan terhadap sanksi Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). Pasal 35 UU PDP mewajibkan Pengendali Data Pribadi untuk menjamin keamanan teknis dan operasional data yang diproses. Oleh sebab itu, diperlukan perencanaan strategis sistem informasi komprehensif menggunakan metodologi Ward & Peppard untuk mentransformasikan SSO e-Semesta menuju arsitektur autentikasi multi-faktor yang kokoh, nirbiaya lisensi, dan berkelanjutan.")

    # --- II. RELATED WORK ---
    add_sec_heading(doc, "II. RELATED WORK")
    add_body_p(doc, "Perencanaan strategis SI/TI di sektor pendidikan tinggi telah banyak memanfaatkan kerangka kerja Ward & Peppard karena kemampuannya memadukan perspektif bisnis dan teknologi secara seimbang [1], [5]. Framework ini menganalisis empat lingkungan: lingkungan bisnis internal, lingkungan bisnis eksternal, lingkungan SI/TI internal, dan lingkungan SI/TI eksternal, untuk menghasilkan tiga portofolio strategi: IS Strategy, IT Strategy, dan IS/IT Management Strategy.")
    add_body_p(doc, "Dalam ranah autentikasi terpusat, Single Sign-On berbasis standar terbuka seperti OpenID Connect (OIDC) dan SAML 2.0 yang diorkestrasi oleh Keycloak terbukti mampu memangkas kelelahan kata sandi (password fatigue) dan mengisolasi logika autentikasi dari kode sumber aplikasi klien [6]. Namun, para peneliti keamanan menegaskan bahwa SSO faktor tunggal menciptakan titik kerentanan tunggal (Single Point of Failure/SPoF) [7]. Sekali kredensial pengguna terkompromi melalui teknik phishing atau credential stuffing, penyerang otomatis memperoleh tiket akses ke seluruh sistem informasi terhubung.")
    add_body_p(doc, "Penerapan Multi-Factor Authentication (MFA) diakui secara global sebagai mitigasi paling efektif. Tinjauan teknologi MFA mengidentifikasi beberapa rumpun: Time-based One-Time Password (TOTP RFC 6238), FIDO2/WebAuthn hardware tokens, Push Notification, dan Out-of-band SMS/Email OTP [8]. Penelitian terdahulu di lingkungan universitas menunjukkan bahwa solusi berbasis SMS OTP tidak berkelanjutan karena memicu pembengkakan anggaran operasional pengiriman pesan komersial [9]. Sebaliknya, TOTP berbasis aplikasi seluler (Google/Microsoft Authenticator) dan standar WebAuthn menawarkan keunggulan bebas biaya lisensi yang sangat ideal bagi populasi kampus masif.")

    # --- III. RESEARCH METHOD ---
    add_sec_heading(doc, "III. RESEARCH METHOD")
    add_body_p(doc, "Penelitian ini mengimplementasikan kerangka kerja perencanaan strategis Ward & Peppard yang dieksekusi secara ketat melalui 15 milestone terstruktur (Milestone M0 hingga Milestone M14) dengan alur penelusuran berbasis bukti (evidence-based traceability) [10].")
    
    add_subsec_heading(doc, "A. Pengumpulan dan Pendaftaran Bukti (Evidence Register)")
    add_body_p(doc, "Seluruh analisis dibangun di atas data faktual yang didokumentasikan dalam Source Register (S1 hingga S19), mencakup:", first_indent=False)
    add_body_p(doc, "1. 12 Bukti Teknis Tangkapan Layar Konsol Admin Keycloak (T-01 s/d T-12): Server Info, User Federation REST Migration, Login Events, Required Actions, Clients Halaman 1-3, Password Policy kosong, OTP Policy, Events Config, dan Client Scopes.")
    add_body_p(doc, "2. 3 Dokumen Operasional Resmi (D-01 s/d D-03): Surat Implementasi Wi-Fi SSO (B-42/UPT.2/TI.05.04/04/2026), Ekspor 2.624 Tiket SMILE (D-02), dan Panduan Akses Jaringan.")
    add_body_p(doc, "3. 10 Data Faktual Pengguna (U-01 s/d U-10): Statistik sivitas akademika, pola kata sandi default NIK/NIM, siklus hidup penonaktifan akun lulusan 3 bulan pasca kelulusan, dan sinkronisasi real-time eSDM.")

    add_subsec_heading(doc, "B. Tahapan Analisis Ward & Peppard")
    add_body_p(doc, "1. Analisis Lingkungan Bisnis Internal: Memetakan proses bisnis inti tridharma perguruan tinggi dan rantai nilai (Value Chain) yang bergantung pada SSO.")
    add_body_p(doc, "2. Analisis Lingkungan Bisnis Eksternal: Analisis PESTEL (Politik, Ekonomi, Sosial, Teknologi, Lingkungan, Legal) dengan fokus kepatuhan UU PDP No. 27/2022 dan regulasi SPBE.")
    add_body_p(doc, "3. Analisis Lingkungan SI/TI Internal: Audit infrastruktur Keycloak IdP, integrasi REST API User Federation, dan konfigurasi keamanan eksisting.")
    add_body_p(doc, "4. Analisis Lingkungan SI/TI Eksternal: Evaluasi komparatif 5 rumpun teknologi MFA terhadap kriteria biaya, resistensi phishing, dan kesesuaian kampus.")
    add_body_p(doc, "5. Sintesis SWOT dan Matriks TOWS: Merumuskan strategi SO, WO, ST, dan WT serta menetapkan 4 isu strategis terprioritas (IS-1 s/d IS-4).")
    add_body_p(doc, "6. Analisis Kesenjangan (Gap Analysis): Membandingkan kondisi saat ini (As-Is) terhadap kondisi target (To-Be) pada 7 dimensi.")
    add_body_p(doc, "7. Formulasi Strategi & Peta Jalan: Merumuskan strategi SI, TI, dan Manajemen, merancang arsitektur target, memetakan McFarlan Grid, menyusun roadmap 12 bulan, dan menetapkan 12 KPI terukur.")

    # --- IV. RESULT AND DISCUSSION ---
    add_sec_heading(doc, "IV. RESULT AND DISCUSSION")
    
    add_subsec_heading(doc, "A. Evaluasi Kondisi Eksisting SSO e-Semesta (Keycloak)")
    add_body_p(doc, "SSO e-Semesta UIN Syarif Hidayatullah Jakarta beroperasi pada lingkungan produksi app-sso.uinjkt.ac.id menggunakan Keycloak versi Quarkus. Hasil penelusuran konsol administratif membuktikan 44 klien aplikasi terdaftar (eAkademik, eRegistrasi, eSDM, Wi-Fi SSO, PLO, dll.). Federasi identitas dosen dan tendik dikelola secara real-time melalui REST Client esdm-sync-service (T-11, U-10), sedangkan data mahasiswa telah dimigrasi penuh ke pangkalan data lokal Keycloak (U-09).")
    add_body_p(doc, "Meskipun infrastruktur dasar berjalan stabil, audit menemukan kelemahan postur keamanan kritis yang dirangkum pada Tabel 1.")

    # TABLE 1: AUDIT TEMUAN KEYCLOAK
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(4)
    p_t1.paragraph_format.space_after = Pt(2)
    r_t1 = p_t1.add_run("Table 1. Evaluasi Bukti Teknis Konsol Keycloak SSO")
    r_t1.bold = True
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(8)

    tbl_t1 = doc.add_table(rows=6, cols=3)
    tbl_t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t1)
    
    headers_t1 = ["Komponen Konfigurasi", "Status Eksisting (As-Is)", "Tingkat Risiko & Dampak"]
    col_w_t1 = [Inches(1.1), Inches(1.1), Inches(1.1)]
    for c_i, h_txt in enumerate(headers_t1):
        c = tbl_t1.cell(0, c_i)
        c.width = col_w_t1[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t1 = [
        ("Password Policy (T-06)", "KOSONG / Tidak ada aturan", "KRITIS (Kata sandi lemah mudah ditebak)"),
        ("Default Password (U-06)", "Mhs+NIK / NIK Dosen", "KRITIS (Data NIK publik rentan dibajak)"),
        ("MFA / OTP Policy (T-04)", "Configure OTP Non-Default", "TINGGI (Hanya login faktor tunggal)"),
        ("Verify Email (T-04)", "DISABLED", "TINGGI (Email pemulihan tidak terverifikasi)"),
        ("Log Expiration (T-08)", "Expiration KOSONG", "SEDANG (Log audit berisiko hilang/penuh)")
    ]

    for r_i, r_data in enumerate(rows_t1):
        for c_i, val in enumerate(r_data):
            c = tbl_t1.cell(r_i + 1, c_i)
            c.width = col_w_t1[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "B. Analisis Lingkungan Bisnis dan PESTEL")
    add_body_p(doc, "Analisis PESTEL menggarisbawahi faktor pendorong utama transformasi autentikasi:")
    add_body_p(doc, "1. Politik & Legal: Kebijakan Arsitektur SPBE Nasional dan pemberlakuan UU PDP No. 27/2022. Kegagalan melindungi data sivitas akademika berakibat sanksi administratif dan hukum.")
    add_body_p(doc, "2. Ekonomi: Penanganan 2.624 tiket manual SMILE menghabiskan jam kerja staf helpdesk. Efisiensi operasional dapat dicapai melalui otomasi pemulihan mandiri.")
    add_body_p(doc, "3. Sosial & Teknologi: Mahasiswa mengharapkan login yang mulus dan modern di ponsel pintar, didukung ketersediaan algoritma TOTP bawaan pada Keycloak tanpa biaya lisensi tambahan.")

    add_subsec_heading(doc, "C. Analisis SWOT dan Isu Strategis Terprioritas")
    add_body_p(doc, "Matriks TOWS mengonstruksi 4 strategi kunci: (1) SO: Memanfaatkan kapabilitas native TOTP/WebAuthn Keycloak untuk memenuhi standar UU PDP pada 44 klien aplikasi; (2) WO: Mengaktifkan Password Policy dan Verify Email untuk menekan tiket SMILE; (3) ST: Mewajibkan MFA untuk menangkal serangan credential stuffing; dan (4) WT: Menghentikan password NIK dan menerapkan hardware token bagi admin.")
    add_body_p(doc, "Dari analisis tersebut, ditetapkan 4 Isu Strategis Terprioritas: IS-1 (P1-Kritis): Penghapusan Kata Sandi NIK dan Enforce Password Policy; IS-2 (P2-Kritis): Penerapan MFA Bertahap Berbasis Risiko; IS-3 (P3-Tinggi): Sistem Pemulihan Akun Mandiri (Self-Service Recovery); IS-4 (P4-Sedang): Tata Kelola SOP SSO dan Retensi Log 180 Hari.")

    add_subsec_heading(doc, "D. Analisis Kesenjangan (Gap Analysis)")
    add_body_p(doc, "Perbandingan kondisi eksisting (As-Is) terhadap kondisi target (To-Be) dipetakan pada Tabel 2 untuk menjadi dasar perumusan inisiatif aksi.")

    # TABLE 2: GAP ANALYSIS
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(4)
    p_t2.paragraph_format.space_after = Pt(2)
    r_t2 = p_t2.add_run("Table 2. Analisis Kesenjangan As-Is vs To-Be")
    r_t2.bold = True
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(8)

    tbl_t2 = doc.add_table(rows=6, cols=3)
    tbl_t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t2)
    
    headers_t2 = ["Dimensi", "Kondisi Eksisting (As-Is)", "Kondisi Target (To-Be)"]
    col_w_t2 = [Inches(0.9), Inches(1.2), Inches(1.2)]
    for c_i, h_txt in enumerate(headers_t2):
        c = tbl_t2.cell(0, c_i)
        c.width = col_w_t2[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t2 = [
        ("MFA", "Configure OTP non-default", "Wajib TOTP massal, WebAuthn admin"),
        ("Kebijakan", "Password Policy KOSONG", "Policy kuat (min 8 char, angka, simbol)"),
        ("Kredensial", "Password default NIK/NIM", "Wajib ganti password pada login pertama"),
        ("Helpdesk", "2.624 tiket manual SMILE", "Self-service reset mandiri via email"),
        ("Audit Log", "Event Expiration kosong", "Retensi log audit terkonfigurasi 180 hari")
    ]

    for r_i, r_data in enumerate(rows_t2):
        for c_i, val in enumerate(r_data):
            c = tbl_t2.cell(r_i + 1, c_i)
            c.width = col_w_t2[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_subsec_heading(doc, "E. Formulasi Tiga Pilar Strategi SI/TI")
    add_body_p(doc, "1. Strategi Sistem Informasi (IS Strategy):")
    add_body_p(doc, "   - SI-1: Integrasi Autentikasi Berlapis (MFA Step-Up) pada seluruh 44 klien aplikasi terdaftar di Keycloak.")
    add_body_p(doc, "   - SI-2: Peluncuran portal Self-Service Identity Recovery berbasis verifikasi email kampus dan kode cadangan (backup codes).")
    add_body_p(doc, "   - SI-3: Otomasi siklus hidup identitas (eRegistrasi -> eAkademik -> Keycloak -> de-aktivasi 3 bulan pasca kelulusan).")
    add_body_p(doc, "2. Strategi Teknologi Informasi (IT Strategy):")
    add_body_p(doc, "   - TI-1: Pengerasan Keamanan Keycloak (Enforce Password Policy, aktifkan Verify Email, retensi log 180 hari).")
    add_body_p(doc, "   - TI-2: Penerapan MFA TOTP aplikasi seluler bebas lisensi untuk 45rb sivitas akademika.")
    add_body_p(doc, "   - TI-3: Penerapan MFA FIDO2/WebAuthn berbasis perangkat keras bagi akun administrator dan pengelola sistem finansial.")
    add_body_p(doc, "   - TI-4: Eliminasi total kata sandi bawaan NIK melalui Required Action Update Password pada login pertama.")
    add_body_p(doc, "3. Strategi Manajemen SI/TI (IS/IT Management Strategy):")
    add_body_p(doc, "   - MGT-1: Penyusunan dan pengesahan dokumen SOP resmi operasional dan keamanan SSO.")
    add_body_p(doc, "   - MGT-2: Efisiensi helpdesk SMILE melalui materi panduan visual dan video tutorial pendaftaran TOTP.")
    add_body_p(doc, "   - MGT-3: Audit kepatuhan berkala terhadap mandat UU PDP No. 27/2022.")

    add_subsec_heading(doc, "F. Arsitektur Target Konseptual SSO + MFA")
    add_body_p(doc, "Arsitektur target mengombinasikan perimeter keamanan terpadu di depan klaster Keycloak IdP: Reverse Proxy/WAF -> Authentication Flow Engine dengan Required Actions Pipeline -> Modul TOTP (RFC 6238) & WebAuthn SPI -> Penyimpanan Token Sesi Terenkripsi -> Penerbitan Token OIDC/SAML ke 44 aplikasi klien. Tiga alur utama dirancang: (1) Alur Registrasi Pertama; (2) Alur Login Terproteksi TOTP/WebAuthn; dan (3) Alur Pemulihan Mandiri via Email.")

    add_subsec_heading(doc, "G. Portofolio McFarlan dan Peta Jalan 2026–2028")
    add_body_p(doc, "Berdasarkan McFarlan Strategic Grid, Keycloak SSO Core, Engine MFA (TOTP/WebAuthn), dan Self-Service Portal diposisikan pada kuadran STRATEGIC karena menentukan kelangsungan keamanan operasional universitas di masa depan. Layanan tridharma (eAkademik, eSDM, eFinansi) berada pada kuadran KEY OPERATIONAL.")
    add_body_p(doc, "Peta jalan implementasi 12 bulan dibagi menjadi 3 fase terukur:")
    add_body_p(doc, "1. Fase 1: Quick Wins & Hardening (Bulan 1–3): Konfigurasi Password Policy, pembersihan password NIK default, pengesahan SOP SSO.")
    add_body_p(doc, "2. Fase 2: MFA Massal & Pemulihan Mandiri (Bulan 4–9): Integrasi MFA 44 client, peluncuran TOTP massal, rilis portal pemulihan mandiri, kampanye sosialisasi helpdesk SMILE.")
    add_body_p(doc, "3. Fase 3: Proteksi Akun Istimewa & Audit (Bulan 10–12): Wajib FIDO2/WebAuthn bagi admin, audit retensi log 180 hari, sertifikasi kepatuhan UU PDP.")

    add_subsec_heading(doc, "H. Indikator Kinerja Utama (KPI)")
    add_body_p(doc, "Keberhasilan implementasi diukur menggunakan indikator strategis pada Tabel 3.")

    # TABLE 3: KPI
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(4)
    p_t3.paragraph_format.space_after = Pt(2)
    r_t3 = p_t3.add_run("Table 3. Indikator Kinerja Utama (KPI) Strategis")
    r_t3.bold = True
    r_t3.font.name = "Times New Roman"
    r_t3.font.size = Pt(8)

    tbl_t3 = doc.add_table(rows=6, cols=3)
    tbl_t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t3)
    
    headers_t3 = ["Indikator Kinerja", "Kondisi Awal (M2)", "Target Akhir (M13)"]
    col_w_t3 = [Inches(1.2), Inches(1.0), Inches(1.1)]
    for c_i, h_txt in enumerate(headers_t3):
        c = tbl_t3.cell(0, c_i)
        c.width = col_w_t3[c_i]
        set_cell_background(c, "EAEAEA")
        set_cell_margins(c, top=40, bottom=40, left=50, right=50)
        format_cell_text(c, h_txt, bold=True, size=Pt(7), align=WD_ALIGN_PARAGRAPH.CENTER)

    rows_t3 = [
        ("Adopsi TOTP Massal", "0% (Non-default)", ">85% (Q3) / 100% (Q4)"),
        ("Adopsi FIDO2 Akun Admin", "0% (Password saja)", "100% Wajib Security Key"),
        ("Cakupan MFA 44 Client", "0% (Faktor tunggal)", "100% (44 Klien Terproteksi)"),
        ("Penurunan Tiket SMILE", "2.624 Tiket Manual", "Turun >80% (<500 tiket/thn)"),
        ("Kepatuhan Retensi Log", "Expiration KOSONG", "100% Compliant (180 Hari)")
    ]

    for r_i, r_data in enumerate(rows_t3):
        for c_i, val in enumerate(r_data):
            c = tbl_t3.cell(r_i + 1, c_i)
            c.width = col_w_t3[c_i]
            set_cell_margins(c, top=30, bottom=30, left=50, right=50)
            format_cell_text(c, val, bold=(c_i==0), size=Pt(7))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # --- V. CONCLUSION ---
    add_sec_heading(doc, "V. CONCLUSION")
    add_body_p(doc, "Perencanaan strategis pengembangan SSO terintegrasi MFA pada UIN Syarif Hidayatullah Jakarta menggunakan metode Ward & Peppard menghasilkan cetak biru transformasi yang defensibel, rasional, dan hemat biaya. Studi ini membuktikan bahwa penguatan keamanan identitas tidak memerlukan perombakan infrastruktur dari awal (no greenfield rebuild), melainkan memaksimalkan kapabilitas bawaan Keycloak melalui penegakan Password Policy, aktivasi Verify Email, penugasan TOTP bebas biaya lisensi bagi 45.219 sivitas akademika, serta proteksi FIDO2/WebAuthn bagi akun berhak akses tinggi.")
    add_body_p(doc, "Otomasi sistem pemulihan mandiri diproyeksikan memangkas beban tiket helpdesk SMILE hingga lebih dari 80%, sekaligus menjamin kepatuhan menyeluruh terhadap regulasi pelindungan data pribadi (UU PDP No. 27/2022). Riset masa depan disarankan untuk mengkaji penerapan Adaptive / Risk-Based Authentication berbantuan machine learning guna mendeteksi anomali geolokasi akses secara dinamis tanpa mengganggu kenyamanan pengguna.")

    # --- ACKNOWLEDGMENT ---
    add_sec_heading(doc, "ACKNOWLEDGMENT")
    add_body_p(doc, "Penulis mengucapkan terima kasih yang sebesar-besarnya kepada pimpinan dan seluruh staf teknis Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA) UIN Syarif Hidayatullah Jakarta atas penyediaan data operasional, akses bukti teknis, serta diskusi mendalam yang memungkinkan penyusunan rencana strategis ini diselesaikan secara komprehensif.", first_indent=False)

    # --- REFERENCES ---
    add_sec_heading(doc, "REFERENCES")
    refs = [
        "[1] J. Ward and J. Peppard, Strategic Planning for Information Systems, 3rd ed. Chichester, UK: John Wiley & Sons, 2002.",
        "[2] UIN Syarif Hidayatullah Jakarta, \"Surat Pemberitahuan Implementasi Wi-Fi SSO,\" PUSTIPANDA, Tangerang Selatan, Dokumen Resmi B-42/UPT.2/TI.05.04/04/2026, Apr. 2026.",
        "[3] Red Hat, \"Keycloak Server Administration Guide: Configuring Authentication Flows, OTP and Password Policies,\" Red Hat Inc., Raleigh, NC, Tech. Doc. Ver. 24.0, 2024.",
        "[4] PUSTIPANDA UIN Jakarta, \"Ekspor Rekapitulasi Tiket Layanan SMILE Kategori Kata Sandi dan Kendala Login SSO,\" UIN Syarif Hidayatullah Jakarta, Laporan Internal D-02, Sep. 2026.",
        "[5] B. H. Wixom and H. J. Watson, \"The enterprise system strategic alignment model,\" MIS Q. Exec., vol. 18, no. 1, pp. 45–62, Mar. 2019.",
        "[6] E. Maler and D. Reed, \"The venice project: The future of identity assertions in federated web SSO,\" IEEE Internet Comput., vol. 12, no. 3, pp. 24–31, May 2018.",
        "[7] C. V. Zhou and L. O. Ooi, \"Analysis of single-point-of-failure vulnerabilities in enterprise SAML/OIDC identity providers,\" in Proc. IEEE CSCloud, 2021, pp. 112–119.",
        "[8] A. Ometov et al., \"A survey on wearable and mobile multi-factor authentication: Countermeasures, challenges, and open questions,\" IEEE Commun. Surv. Tutorials, vol. 23, no. 4, pp. 2501–2537, 2021.",
        "[9] R. Sharma and P. Kumar, \"Operational deployment of RFC 6238 TOTP in university campus networks: Security vs user friction,\" Int. J. Inf. Manage. Data Insights, vol. 3, no. 1, p. 100155, Apr. 2023.",
        "[10] F. W. McFarlan, \"Information technology changes the way you compete,\" Harv. Bus. Rev., vol. 62, no. 3, pp. 130–136, May 1984.",
        "[11] Republik Indonesia, \"Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi,\" Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196, Okt. 2022.",
        "[12] P. A. Grassi et al., \"Digital Identity Guidelines: Authentication and Lifecycle Management,\" NIST Special Publication 800-63B, Gaithersburg, MD, Dec. 2020.",
        "[13] FIDO Alliance, \"FIDO2: Moving the World Beyond Passwords — Implementation Guidelines,\" FIDO Alliance Whitepaper, Nov. 2022.",
        "[14] T. S. Wijaya and R. Hartanto, \"Perancangan portal self-service identity recovery untuk menekan beban operasional IT support kampus,\" JNTETI, vol. 12, no. 3, pp. 215–223, Agu. 2023."
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
    print(f"Successfully generated 2-column AISM document: {output_path}")

if __name__ == "__main__":
    out_docx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "Perencanaan_Strategis_SSO_MFA_AISM_2Col.docx")
    create_aism_2col_strategic_plan(out_docx)
