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

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_callout(doc, text_p_list, title="CATATAN PENTING"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"■ {title}\n")
    run_t.bold = True
    run_t.font.name = "Arial"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    for idx, t in enumerate(text_p_list):
        if idx > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
        run = p.add_run(t)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def create_journal_docx(output_path):
    doc = Document()
    
    # Page Setup - Standard A4 with 1 inch margins
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(10)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)
    
    # --- HEADER JURNAL ---
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_hdr.paragraph_format.space_after = Pt(2)
    run_hdr1 = p_hdr.add_run("Volume 6, Nomor 1, September 2026 | e-ISSN 2685-998X | DOI 10.30865/json.v6i1.9982 | Hal: 1-14\n")
    run_hdr1.font.size = Pt(8.5)
    run_hdr1.font.italic = True
    run_hdr1.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    run_hdr2 = p_hdr.add_run("Jurnal Sistem Komputer dan Informatika (JSON)")
    run_hdr2.bold = True
    run_hdr2.font.size = Pt(10)
    run_hdr2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    # Horizontal rule
    p_hr = doc.add_paragraph()
    p_hr.paragraph_format.space_after = Pt(12)
    p_hr_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="1B365D"/></w:pBdr>')
    p_hr._p.get_or_add_pPr().append(p_hr_border)

    # --- JUDUL ARTIKEL ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("PERENCANAAN STRATEGIS SINGLE SIGN-ON DAN MULTI-FACTOR AUTHENTICATION BERBASIS WARD AND PEPPARD PADA UIN SYARIF HIDAYATULLAH JAKARTA")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    # --- PENULIS & AFILIASI ---
    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(4)
    r_auth = p_author.add_run("Wandy*1, Hanyudha2\n")
    r_auth.bold = True
    r_auth.font.size = Pt(10)
    
    r_aff = p_author.add_run("1,2Pusat Teknologi Informasi dan Pangkalan Data (PUSTIPANDA)\nUIN Syarif Hidayatullah Jakarta, Indonesia\nEmail: 1,*hanyudha@gmail.com, 2pustipanda@uinjkt.ac.id\nEmail Penulis Korespondensi: hanyudha@gmail.com\n")
    r_aff.font.size = Pt(8.5)
    r_aff.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    
    r_sub = p_author.add_run("Submitted: 10/09/2026; Accepted: 18/09/2026; Published: 21/09/2026")
    r_sub.font.size = Pt(8)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Separator line
    p_hr2 = doc.add_paragraph()
    p_hr2.paragraph_format.space_after = Pt(10)
    p_hr2_b = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="CCCCCC"/></w:pBdr>')
    p_hr2._p.get_or_add_pPr().append(p_hr2_b)

    # --- ABSTRAK INDONESIA ---
    p_abs_id = doc.add_paragraph()
    p_abs_id.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_id.paragraph_format.left_indent = Inches(0.2)
    p_abs_id.paragraph_format.right_indent = Inches(0.2)
    p_abs_id.paragraph_format.space_after = Pt(4)
    
    r_abs_lbl = p_abs_id.add_run("Abstrak–")
    r_abs_lbl.bold = True
    r_abs_lbl.font.size = Pt(9)
    
    r_abs_txt = p_abs_id.add_run(
        "Transformasi digital pada UIN Syarif Hidayatullah Jakarta menuntut tata kelola identitas dan keamanan akses informasi yang andal. "
        "Meskipun seluruh akun mahasiswa dan pegawai telah berhasil dimigrasikan ke Keycloak SSO serta terintegrasi secara otomatis dengan "
        "eRegistrasi, eAkademik, dan esdm-sync-service, hasil evaluasi menunjukkan beberapa celah keamanan kritikal. Celah tersebut meliputi "
        "Password Policy yang kosong, penggunaan password bawaan berbasis NIK/NIM, fitur Verify Email yang dinonaktifkan, MFA yang belum diwajibkan, "
        "serta Expiration Log yang tidak terkonfigurasi. Penelitian ini bertujuan menyusun perencanaan strategis pengembangan SSO dan MFA "
        "menggunakan kerangka kerja Ward and Peppard dengan fokus analisis PESTEL dan SWOT. Hasil penelitian merumuskan 10 inisiatif strategis yang "
        "mencakup penguatan kebijakan password, kewajiban Multi-Factor Authentication (MFA) adaptif, otomatisasi deaktivasi akun lulusan/non-aktif, "
        "serta penerapan arsitektur Target SSO & MFA berbasis Zero Trust. Peta jalan implementasi disusun dalam rentang 2026–2028 untuk memastikan "
        "kepatuhan terhadap Sistem Pemerintahan Berbasis Elektronik (SPBE) dan UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi (PDP)."
    )
    r_abs_txt.font.size = Pt(9)

    p_kw_id = doc.add_paragraph()
    p_kw_id.paragraph_format.left_indent = Inches(0.2)
    p_kw_id.paragraph_format.right_indent = Inches(0.2)
    p_kw_id.paragraph_format.space_after = Pt(10)
    r_kw_lbl = p_kw_id.add_run("Kata Kunci: ")
    r_kw_lbl.bold = True
    r_kw_lbl.font.size = Pt(9)
    r_kw_txt = p_kw_id.add_run("Perencanaan Strategis; Ward and Peppard; Single Sign-On; Keycloak; Multi-Factor Authentication; PESTEL; SWOT")
    r_kw_txt.font.size = Pt(9)

    # --- ABSTRACT ENGLISH ---
    p_abs_en = doc.add_paragraph()
    p_abs_en.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs_en.paragraph_format.left_indent = Inches(0.2)
    p_abs_en.paragraph_format.right_indent = Inches(0.2)
    p_abs_en.paragraph_format.space_after = Pt(4)
    
    r_absen_lbl = p_abs_en.add_run("Abstract–")
    r_absen_lbl.bold = True
    r_absen_lbl.font.size = Pt(9)
    r_absen_lbl.font.italic = True
    
    r_absen_txt = p_abs_en.add_run(
        "Digital transformation at UIN Syarif Hidayatullah Jakarta requires reliable identity governance and information access security. "
        "Although all student and staff accounts have been successfully migrated to Keycloak SSO and automatically integrated with eRegistrasi, "
        "eAkademik, and esdm-sync-service, evaluation results reveal several critical security vulnerabilities. These include an empty Password Policy, "
        "default credentials based on NIK/NIM, disabled Email Verification, optional MFA enforcement, and unconfigured Log Expiration. This study aims to "
        "formulate a strategic plan for SSO and MFA development using the Ward and Peppard framework, focusing on PESTEL and SWOT analyses. The findings "
        "formulate 10 strategic initiatives encompassing password policy hardening, mandatory adaptive Multi-Factor Authentication (MFA), automated "
        "deactivation of graduated/inactive accounts, and the deployment of a Zero Trust Target SSO & MFA architecture. An implementation roadmap spanning "
        "2026–2028 is established to guarantee compliance with the Electronic-Based Government System (SPBE) and Law No. 27/2022 on Personal Data Protection (PDP)."
    )
    r_absen_txt.font.size = Pt(9)
    r_absen_txt.font.italic = True

    p_kw_en = doc.add_paragraph()
    p_kw_en.paragraph_format.left_indent = Inches(0.2)
    p_kw_en.paragraph_format.right_indent = Inches(0.2)
    p_kw_en.paragraph_format.space_after = Pt(12)
    r_kwen_lbl = p_kw_en.add_run("Keywords: ")
    r_kwen_lbl.bold = True
    r_kwen_lbl.font.size = Pt(9)
    r_kwen_lbl.font.italic = True
    r_kwen_txt = p_kw_en.add_run("Strategic Planning; Ward and Peppard; Single Sign-On; Keycloak; Multi-Factor Authentication; PESTEL; SWOT")
    r_kwen_txt.font.size = Pt(9)
    r_kwen_txt.font.italic = True

    # Separator line
    p_hr3 = doc.add_paragraph()
    p_hr3.paragraph_format.space_after = Pt(14)
    p_hr3_b = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="1" w:color="CCCCCC"/></w:pBdr>')
    p_hr3._p.get_or_add_pPr().append(p_hr3_b)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.italic = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_p(text, justify=True):
        p = doc.add_paragraph()
        if justify:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.size = Pt(10)
        return p

    # --- 1. PENDAHULUAN ---
    add_h1("1. PENDAHULUAN")
    add_p(
        "Universitas Islam Negeri (UIN) Syarif Hidayatullah Jakarta merupakan salah satu perguruan tinggi keagamaan Islam negeri (PTKIN) "
        "terbesar di Indonesia yang secara konsisten melakukan akselerasi transformasi digital. Untuk mendukung kegiatan akademik, penelitian, "
        "dan administrasi bagi lebih dari 30.000 mahasiswa serta ribuan dosen dan tenaga kependidikan, Pusat Teknologi Informasi dan Pangkalan Data "
        "(PUSTIPANDA) telah mengimplementasikan sistem Identity and Access Management (IAM) berbasis Keycloak Single Sign-On (SSO) [S18]. "
        "Integrasi sistem layanan utama seperti eRegistrasi, eAkademik, dan esdm-sync-service (sistem kepegawaian) telah dilakukan secara terotomatisasi "
        "dan real-time untuk mendukung manajemen siklus hidup identitas pengguna [S19]."
    )
    add_p(
        "Meskipun jangkauan integrasi infrastruktur SSO telah mencakup seluruh civitas akademika, audit empiris terhadap parameter konfigurasi "
        "server Keycloak dan manajemen layanan menemukan sejumlah celah keamanan dan tata kelola yang bersifat sangat kritis. Celah tersebut meliputi: "
        "(1) Password Policy yang saat ini berada dalam kondisi kosong (EMPTY) [T-06]; (2) penggunaan kombinasi NIK/NIM sebagai kata sandi bawaan "
        "(default credentials) [U-06, U-07]; (3) status fitur Verify Email yang berada dalam kondisi DISABLED [T-04]; (4) belum diwajibkannya Multi-Factor Authentication (MFA) "
        "sebagai standar akses utama [T-04]; (5) Expiration Log retention yang tidak terkonfigurasi [T-08]; serta (6) tingginya beban operasional helpdesk SMILE yang "
        "mencapai 2.624 tiket terkait keluhan reset password dan kendala akun [D-02]."
    )
    add_p(
        "Kondisi tersebut meningkatkan risiko peretasan akun, serangan credential stuffing, phishing, serta potensi pelanggaran kewajiban perlindungan "
        "data sesuai amanat Undang-Undang No. 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP) dan Peraturan Presiden No. 95 Tahun 2018 tentang "
        "Sistem Pemerintahan Berbasis Elektronik (SPBE). Oleh karena itu, diperlukan penyusunan perencanaan strategis pengembangan SSO dan MFA yang komprehensif. "
        "Penelitian ini bertujuan untuk merumuskan formulasi strategi, arsitektur target, serta peta jalan (roadmap) implementasi SSO dan MFA pada UIN Syarif Hidayatullah Jakarta "
        "menggunakan kerangka kerja Ward and Peppard yang disesuaikan dengan fokus analisis PESTEL dan SWOT."
    )

    make_callout(
        doc,
        [
            "Seluruh akun mahasiswa dan pegawai telah berhasil dimigrasikan ke Keycloak SSO dalam lingkungan produksi [S18/U-09, S19/U-10].",
            "Fokus utama perencanaan strategis ini adalah menyelesaikan celah baseline security (Password Policy kosong, Verify Email DISABLED, Expiration Log kosong) serta menerapkan kewajiban MFA Adaptif berbasis Zero Trust."
        ],
        title="Ringkasan Konteks & Urgensi Penelitian"
    )

    # --- 2. METODOLOGI PENELITIAN ---
    add_h1("2. METODOLOGI PENELITIAN")
    add_p(
        "Penelitian ini mengadaptasi metodologi Perencanaan Strategis Sistem Informasi/Teknologi Informasi (SI/TI) kerangka kerja Ward and Peppard [11]. "
        "Metode ini secara sistematis menghubungkan analisis lingkungan bisnis dan lingkungan SI/TI (baik internal maupun eksternal) untuk menghasilkan "
        "formulasi strategi dan portofolio aplikasi masa depan."
    )
    
    add_h2("2.1 Alat Analisis Lingkungan Strategy")
    add_p(
        "Sesuai dengan batasan dan ruang lingkup yang ditetapkan, analisis lingkungan pada penelitian ini memfokuskan penggunaan 2 (dua) alat analisis utama:"
    )
    add_p(
        "1. Analisis PESTEL (Political, Economic, Social, Technological, Environmental, Legal): Digunakan untuk mengidentifikasi dan mengevaluasi faktor-faktor makro "
        "eksternal yang memengaruhi kebijakan tata kelola identitas dan keamanan informasi di perguruan tinggi.\n"
        "2. Analisis SWOT (Strengths, Weaknesses, Opportunities, Threats): Digunakan untuk memetakan kekuatan dan kelemahan internal infrastruktur SSO Keycloak UIN Jakarta, "
        "serta menyatukannya dengan peluang dan ancaman eksternal untuk merumuskan matriks kombinasi strategi SO, ST, WO, dan WT."
    )
    
    add_p(
        "Catatan Metodologis: Alat analisis strategis umum seperti Value Chain, Porter's Five Forces, McFarlan Strategic Grid, dan Critical Success Factors (CSF) "
        "disengaja untuk tidak digunakan terlebih dahulu pada tahap ini. Hal ini dilakukan guna menjaga fokus kajian secara tajam pada penguatan tata kelola keamanan identitas, "
        "kepatuhan regulasi perlindungan data, dan arsitektur teknis autentikasi SSO/MFA."
    )

    add_h2("2.2 Tahapan Pelaksanaan Penelitian")
    add_p(
        "Tahapan perencanaan strategis dilaksanakan dalam 5 (lima) fase terstruktur:"
    )
    add_p(
        "• Fase 1: Identifikasi Masalah & Audit Empiris Baseline (Pemeriksaan parameter konfigurasi Keycloak server, log analisis tiket SMILE, dan registri data S1-S19).\n"
        "• Fase 2: Analisis Lingkungan Eksternal (PESTEL) & Keamanan SI/TI.\n"
        "• Fase 3: Analisis Lingkungan Internal & Pemetaan SWOT.\n"
        "• Fase 4: Formulasi Strategi & Perancangan Arsitektur Target SSO & MFA (Membandingkan kondisi As-Is vs To-Be).\n"
        "• Fase 5: Penyusunan Peta Jalan (Roadmap 2026–2028) dan Indikator Kinerja Utama (KPI)."
    )

    # --- 3. HASIL DAN PEMBAHASAN ---
    add_h1("3. HASIL DAN PEMBAHASAN")
    
    add_h2("3.1 Analisis Lingkungan Eksternal (PESTEL)")
    add_p(
        "Hasil analisis makro lingkungan eksternal PESTEL yang memengaruhi domain SSO dan MFA UIN Syarif Hidayatullah Jakarta dirangkum pada Tabel 1."
    )

    # Tabel 1: PESTEL
    tbl_pestel = doc.add_table(rows=7, cols=2)
    tbl_pestel.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pestel)
    
    hdr_cells = tbl_pestel.rows[0].cells
    hdr_cells[0].text = "Dimensi PESTEL"
    hdr_cells[1].text = "Temuan Strategis & Implikasi bagi UIN Syarif Hidayatullah Jakarta"
    for cell in hdr_cells:
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9.5)

    pestel_data = [
        ("Political (Politik)", "Amanat Perpres No. 95/2018 tentang SPBE menuntut integrasi layanan digital pemerintah berbasis Single Sign-On (SSO) dan standar keamanan informasi publik nasional."),
        ("Economic (Ekonomi)", "Efisiensi anggaran operasional IT. Pemanfaatan Keycloak sebagai platform open-source enterprise menghilangkan biaya lisensi IAM eksorbitan sekaligus menghemat biaya penanganan tiket reset password."),
        ("Social (Sosial)", "Ekspektasi 30.000+ mahasiswa dan ribuan pegawainya akan kemudahan akses layanan digital (Seamless & Frictionless UX) serta jaminan perlindungan akun pribadi dari kebocoran."),
        ("Technological (Teknologi)", "Pesatnya adopsi standar autentikasi modern (OAuth2, OpenID Connect, SAML2, FIDO2/Passkey) serta peningkatan ancaman siber berbasis botnet dan credential stuffing."),
        ("Environmental (Lingkungan)", "Dukungan terhadap program Kampus Hijau (Green Campus) melalui eliminasi formulir kertas untuk verifikasi identitas dan reset akun secara manual."),
        ("Legal (Hukum & Regulasi)", "Kewajiban kepatuhan penuh terhadap UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP) yang mengancam sanksi administratif dan hukum bagi kegagalan perlindungan data identitas.")
    ]

    for idx, (dim, desc) in enumerate(pestel_data):
        row_cells = tbl_pestel.rows[idx+1].cells
        row_cells[0].text = dim
        row_cells[1].text = desc
        bg_hex = "F9FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(9)
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_cap1 = doc.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap1 = p_cap1.add_run("Tabel 1. Hasil Analisis PESTEL Akses & Keamanan Identitas")
    r_cap1.bold = True
    r_cap1.font.size = Pt(9)

    # 3.2 Analisis SWOT
    add_h2("3.2 Analisis Lingkungan Internal dan Eksternal (SWOT)")
    add_p(
        "Berdasarkan audit infrastruktur Keycloak dan kondisi operasional PUSTIPANDA, faktor internal (Kekuatan & Kelemahan) "
        "dan faktor eksternal (Peluang & Ancaman) diidentifikasi sebagai berikut:"
    )

    add_h3("A. Kekuatan (Strengths - S)")
    add_p(
        "• [S1] Seluruh akun mahasiswa dan pegawai telah 100% dimigrasikan ke Keycloak SSO dalam lingkungan produksi [S18/U-09].\n"
        "• [S2] Otomatisasi pendaftaran akun mahasiswa baru terintegrasi langsung dari eRegistrasi ke eAkademik dan SSO saat status berubah menjadi MAHASISWA [S18].\n"
        "• [S3] Layanan esdm-sync-service melakukan sinkronisasi real-time status kepegawaian (termasuk langsung mematikan akun pegawai non-aktif/drop-out) [S19/U-10].\n"
        "• [S4] Kemandirian penggelaran infrastruktur SSO pada server internal PUSTIPANDA berbasis open-source enterprise Keycloak."
    )

    add_h3("B. Kelemahan (Weaknesses - W)")
    add_p(
        "• [W1] Parameter Password Policy pada server Keycloak saat ini dalam kondisi kosong (EMPTY) [T-06].\n"
        "• [W2] Penggunaan kredensial bawaan berbasis NIK/NIM yang mudah ditebak tanpa paksaan ubah password pada login pertama [U-06, U-07].\n"
        "• [W3] Fitur Verify Email berada dalam status DISABLED sehingga validasi kepemilikan email pengguna tidak berjalan [T-04].\n"
        "• [W4] Multi-Factor Authentication (MFA) bersifat opsional/non-default sehingga mayoritas akun hanya dilindungi password tunggal [T-04].\n"
        "• [W5] Expiration Log retention belum terkonfigurasi (EMPTY) sehingga membatasi jejak audit keamanan forensik [T-08].\n"
        "• [W6] Beban operasional helpdesk SMILE sangat tinggi dengan 2.624 tiket penanganan masalah akun dan reset password [D-02]."
    )

    add_h3("C. Peluang (Opportunities - O)")
    add_p(
        "• [O1] Pemenuhan standar indeks SPBE nasional dan kepatuhan hukum UU PDP No. 27/2022.\n"
        "• [O2] Kebijakan standardisasi SSO antar Perguruan Tinggi Negeri (PTN) dan kementerian.\n"
        "• [O3] Ketersediaan teknologi autentikasi modern FIDO2/Passkey dan TOTP/Authenticator App yang aman dan efisien."
    )

    add_h3("D. Ancaman (Threats - T)")
    add_p(
        "• [T1] Maraknya serangan phishing, credential stuffing, dan brute-force yang menargetkan sektor pendidikan tinggi.\n"
        "• [T2] Risiko kebocoran data identitas pribadi dan peretasan sistem akademik akibat pengambilalihan akun civitas akademika.\n"
        "• [T3] Eksploitasi akun mahasiswa/pegawai yang telah lulus/non-aktif jika periode grace period deaktivasi tidak ditegakkan secara disiplin."
    )

    # 3.3 Formulasi Kombinasi Strategi (SWOT Matrix)
    add_h2("3.3 Formulasi Kombinasi Strategi (Matriks SWOT)")
    add_p(
        "Penggabungan faktor eksternal dan internal menghasilkan Matriks Kombinasi Strategi SWOT yang disajikan pada Tabel 2."
    )

    # Tabel 2: Matriks SWOT
    tbl_swot = doc.add_table(rows=5, cols=3)
    tbl_swot.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_swot)

    swot_hdr = tbl_swot.rows[0].cells
    swot_hdr[0].text = "MATRIKS SWOT"
    swot_hdr[1].text = "KEKUATAN (STRENGTHS - S)\n• S1: Migrasi 100% Keycloak SSO\n• S2: Sinkronisasi eRegistrasi & eAkademik\n• S3: Integrated esdm-sync-service"
    swot_hdr[2].text = "KELEMAHAN (WEAKNESSES - W)\n• W1: Password Policy Kosong\n• W2: Default Password NIK/NIM\n• W3: Verify Email Disabled\n• W4: MFA Non-default\n• W5: Log Expiration Kosong\n• W6: 2.624 Tiket SMILE"

    for idx, cell in enumerate(swot_hdr):
        set_cell_background(cell, "1B365D" if idx == 0 else "2B4C7E")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(8.5)

    swot_rows = [
        (
            "PELUANG (OPPORTUNITIES - O)\n• O1: SPBE & UU PDP\n• O2: Standardisasi PTN\n• O3: Adopsi FIDO2/Passkey",
            "STRATEGI SO (Strengths - Opportunities)\n1. Memanfaatkan integrasi otomatis eRegistrasi/esdm-sync-service untuk menerapkan standar SSO SPBE secara nasional (S1, S2, S3 - O1, O2).\n2. Mengembangkan opsi Passkey/FIDO2 pada Keycloak untuk meningkatkan kepuasan pengguna (S1 - O3).",
            "STRATEGI WO (Weaknesses - Opportunities)\n1. Mengaktifkan Password Policy ketat & Verify Email untuk memenuhi regulasi UU PDP (W1, W3 - O1).\n2. Wajibkan Self-Service Password Reset (SSPR) terverifikasi email untuk memangkas 2.624 tiket SMILE (W6 - O1, O3)."
        ),
        (
            "ANCAMAN (THREATS - T)\n• T1: Phishing & Brute-force\n• T2: Kebocoran Data PDP\n• T3: Eksploitasi Akun Non-aktif",
            "STRATEGI ST (Strengths - Threats)\n1. Memanfaatkan esdm-sync-service dan otomasi eAkademik untuk menegakkan otomatisasi deaktivasi akun lulusan (maks 3 bulan) & pegawai non-aktif secara disiplin (S2, S3 - T3).\n2. Menggunakan keandalan Keycloak SSO untuk pemantauan sesi terpusat (S1 - T1).",
            "STRATEGI WT (Weaknesses - Threats)\n1. Mewajibkan Multi-Factor Authentication (MFA) adaptif bagi seluruh akun dosen, tendik, dan mahasiswa (W4 - T1, T2).\n2. Mengonfigurasi Expiration Log retention & SIEM integration untuk audit keamanan forensik real-time (W5 - T1, T2)."
        )
    ]

    for r_idx, (col0, col1, col2) in enumerate(swot_rows):
        row_cells = tbl_swot.rows[r_idx+1].cells
        row_cells[0].text = col0
        row_cells[1].text = col1
        row_cells[2].text = col2
        bg_hex = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, "F0F4F8" if c_idx == 0 else bg_hex)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.5)
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap2 = p_cap2.add_run("Tabel 2. Matriks Kombinasi Strategi SWOT SSO & MFA UIN Jakarta")
    r_cap2.bold = True
    r_cap2.font.size = Pt(9)

    # 3.4 Arsitektur Target dan Alur Autentikasi
    add_h2("3.4 Arsitektur Target dan Alur Autentikasi (As-Is vs To-Be)")
    add_p(
        "Untuk mempertegas bagian yang diimprovisasi, dilakukan analisis komparatif antara Arsitektur & Alur Autentikasi Eksisting (As-Is) "
        "dengan Arsitektur & Alur Autentikasi Target (To-Be)."
    )

    add_h3("3.4.1 Perbandingan Arsitektur Eksisting (As-Is) vs Arsitektur Target (To-Be)")
    add_p(
        "1. Arsitektur Eksisting (As-Is): Server Keycloak berfungsi sebagai Identity Provider (IdP) tunggal yang terintegrasi via REST API/Webhook "
        "dengan eRegistrasi, eAkademik, dan esdm-sync-service. Namun, keamanan layer autentikasi bersifat polos tanpa enkapsulasi kebijakan password, "
        "tanpa verifikasi email wajib, dan tanpa integrasi ke Security Information and Event Management (SIEM) log auditor.\n"
        "2. Arsitektur Target (To-Be): Keycloak diperkuat dengan arsitektur Zero Trust IAM Gateway. Setiap permintaan akses diwajibkan melewati "
        "Enforced Password Policy, Automated Email Ownership Verification, Adaptive MFA Engine (TOTP/FIDO2/SMS/Email OTP), serta Centralized Audit Log Extractor "
        "yang terhubung ke SIEM dengan kebijakan retensi log otomatis (minimal 12 bulan)."
    )

    add_h3("3.4.2 Perbandingan Alur Autentikasi Eksisting vs Target")
    
    # Tabel 3: As-Is vs To-Be
    tbl_flow = doc.add_table(rows=6, cols=3)
    tbl_flow.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_flow)

    flow_hdr = tbl_flow.rows[0].cells
    flow_hdr[0].text = "Tahapan Akses / Autentikasi"
    flow_hdr[1].text = "Alur Autentikasi Eksisting (As-Is)"
    flow_hdr[2].text = "Alur Autentikasi Target (To-Be / Target)"

    for idx, cell in enumerate(flow_hdr):
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9)

    flow_data = [
        ("Login Pertama Akun Baru", "Pengguna login menggunakan password default NIK/NIM tanpa paksaan ubah password.", "Sistem mewajibkan ubah password sesuai Kompleksitas Minimum (12+ karakter, simbol, angka) pada kesempatan login pertama."),
        ("Verifikasi Kepemilikan Email", "DISABLED. Email pengguna tidak terverifikasi sehingga pengiriman OTP/reset link tidak aman.", "ENABLED. Pengguna diwajibkan melakukan klik link verifikasi email sebelum akun diaktifkan penuh."),
        ("Faktor Autentikasi Kedua (MFA)", "Opsional / Non-default. Hanya bergantung pada single factor (password).", "Mandatory Adaptive MFA. Dosen/Pegawai wajib TOTP/Passkey; Mahasiswa wajib TOTP/OTP saat akses dari IP luar kampus."),
        ("Layanan Self-Service Reset", "Terbatas. Banyak pengguna mengalami lock akun & mengajukan tiket manual ke SMILE (2.624 tiket).", "Automated SSPR berbasis Email Verification & OTP. Menurunkan tiket reset password hingga >75%."),
        ("Siklus Hidup & Log Auditing", "Expiration Log EMPTY. Akun alumni berisiko tetap aktif jika tidak di-sweep manual.", "Deaktivasi Otomatis akun lulusan 3 bulan pasca-lulus & pegawai non-aktif real-time via esdm-sync-service + Log Retention 12 bulan.")
    ]

    for idx, (step, as_is, to_be) in enumerate(flow_data):
        row_cells = tbl_flow.rows[idx+1].cells
        row_cells[0].text = step
        row_cells[1].text = as_is
        row_cells[2].text = to_be
        bg_hex = "F9FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.5)
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_cap3 = doc.add_paragraph()
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap3 = p_cap3.add_run("Tabel 3. Matriks Perbandingan Alur Autentikasi Eksisting vs Target")
    r_cap3.bold = True
    r_cap3.font.size = Pt(9)

    # 3.5 Rencana Implementasi dan Peta Jalan (Roadmap)
    add_h2("3.5 Rencana Implementasi dan Peta Jalan (Roadmap 2026–2028)")
    add_p(
        "Formulasi 10 inisiatif strategis disusun ke dalam peta jalan implementasi bertahap selama 3 (tiga) tahun (2026–2028) "
        "yang terbagi menjadi 3 fase utama:"
    )
    add_p(
        "1. Fase 1 (Q4 2026): Hardening & Enforce Baseline Security (Inisiasi Password Policy, Force Password Change, Verify Email ENABLED, & SSPR).\n"
        "2. Fase 2 (Q1-Q2 2027): Mandat MFA & Automated Lifecycle Integration (Penegakan MFA Dosen/Pegawai, Integrasi Deaktivasi Lulusan/Non-aktif, & Log Retention).\n"
        "3. Fase 3 (Q3 2027-2028): Modern SSO & Zero Trust Architecture (Adopsi Passkey/FIDO2, SIEM Centralized Audit, & Penilaian Kepatuhan SPBE/PDP)."
    )

    # Tabel 4: Roadmap
    tbl_road = doc.add_table(rows=11, cols=5)
    tbl_road.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_road)

    road_hdr = tbl_road.rows[0].cells
    road_hdr[0].text = "Kode"
    road_hdr[1].text = "Inisiatif Strategis SSO & MFA"
    road_hdr[2].text = "2026 (Q4)"
    road_hdr[3].text = "2027 (Q1-Q4)"
    road_hdr[4].text = "2028 (Q1-Q4)"

    for idx, cell in enumerate(road_hdr):
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9)

    road_data = [
        ("IS-01", "Pengaktifan Enforced Password Policy (12+ Karakter, Kompleksitas)", "V", "", ""),
        ("IS-02", "Penerapan Mandatory First-Login Password Change (Eliminasi Default NIK/NIM)", "V", "", ""),
        ("IS-03", "Pengaktifan Fitur Verify Email & Otomatisasi Validasi Email Registrasi", "V", "", ""),
        ("IS-04", "Pengembangan Portal Self-Service Password Reset (SSPR) Mandiri", "V", "V", ""),
        ("IS-05", "Penegakan Mandatory MFA untuk Akun Dosen & Tenaga Kependidikan", "", "V", ""),
        ("IS-06", "Penerapan Adaptive MFA untuk Akun Mahasiswa pada Akses Luar Kampus", "", "V", ""),
        ("IS-07", "Otomatisasi Deaktivasi Akun Lulusan (3 Bulan Post-Graduation) & ESDM Sync", "", "V", ""),
        ("IS-08", "Konfigurasi Expiration Log Retention (Minimal 12 Bulan) & SIEM Integration", "", "V", "V"),
        ("IS-09", "Implementasi Passwordless Authentication berbasis FIDO2 / Passkey", "", "", "V"),
        ("IS-10", "Audit Kepatuhan Keamanan Identitas Berkala (SPBE & UU PDP)", "", "V", "V")
    ]

    for idx, (code, init_name, y1, y2, y3) in enumerate(road_data):
        row_cells = tbl_road.rows[idx+1].cells
        row_cells[0].text = code
        row_cells[1].text = init_name
        row_cells[2].text = y1
        row_cells[3].text = y2
        row_cells[4].text = y3
        bg_hex = "F9FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.5)
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
                elif c_idx >= 2 and r.text == "V":
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_cap4 = doc.add_paragraph()
    p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap4 = p_cap4.add_run("Tabel 4. Peta Jalan (Roadmap) Implementasi Inisiatif Strategis SSO & MFA (2026–2028)")
    r_cap4.bold = True
    r_cap4.font.size = Pt(9)

    # 3.6 Indikator Kinerja Utama (KPI)
    add_h2("3.6 Indikator Kinerja Utama (KPI) dan Pengukuran Strategis")
    add_p(
        "Keberhasilan pelaksanaan perencanaan strategis ini diukur menggunakan Indikator Kinerja Utama (KPI) "
        "yang ditargetkan pada Tabel 5."
    )

    # Tabel 5: KPI
    tbl_kpi = doc.add_table(rows=6, cols=4)
    tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kpi)

    kpi_hdr = tbl_kpi.rows[0].cells
    kpi_hdr[0].text = "Sasaran Strategis"
    kpi_hdr[1].text = "Indikator Kinerja Utama (KPI)"
    kpi_hdr[2].text = "Baseline (2026)"
    kpi_hdr[3].text = "Target (2028)"

    for idx, cell in enumerate(kpi_hdr):
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9)

    kpi_data = [
        ("Penguatan Keamanan Password", "Persentase Akun dengan Password Policy & Non-Default Credentials", "0% (Password Policy EMPTY)", "100% Akun Terproteksi"),
        ("Adopsi Multi-Factor Authentication", "Persentase Dosen/Pegawai Aktif yang Menggunakan MFA Adaptif", "0% (Opsional/Non-default)", "100% Dosen & Tendik"),
        ("Efisiensi Operasional Helpdesk", "Jumlah Tiket Reset Password SMILE per Bulan", "2.624 Tiket (Total)", "Penurunan > 75% (< 50 tiket/bln)"),
        ("Validasi & Audit Keamanan Log", "Masa Retensi Log Audit Server Keycloak & Terkoneksi SIEM", "0 Hari (EMPTY)", "365 Hari (12 Bulan)"),
        ("Kepatuhan Hukum PDP & SPBE", "Tingkat Kepatuhan Audit Keamanan Identitas (UU PDP & SPBE)", "Parsial (Celah Baseline)", "100% Fully Compliant")
    ]

    for idx, (sasaran, kpi_name, base, tgt) in enumerate(kpi_data):
        row_cells = tbl_kpi.rows[idx+1].cells
        row_cells[0].text = sasaran
        row_cells[1].text = kpi_name
        row_cells[2].text = base
        row_cells[3].text = tgt
        bg_hex = "F9FAFC" if idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row_cells):
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.5)
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
                elif c_idx == 3:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_cap5 = doc.add_paragraph()
    p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap5 = p_cap5.add_run("Tabel 5. Target Indikator Kinerja Utama (KPI) Strategis SSO & MFA")
    r_cap5.bold = True
    r_cap5.font.size = Pt(9)

    # --- 4. KESIMPULAN ---
    add_h1("4. KESIMPULAN")
    add_p(
        "Perencanaan strategis pengembangan Single Sign-On (SSO) dan Multi-Factor Authentication (MFA) pada UIN Syarif Hidayatullah Jakarta "
        "berhasil merumuskan langkah-langkah komprehensif untuk menutup celah keamanan baseline dan meningkatkan mutu tata kelola identitas. "
        "Melalui analisis PESTEL dan SWOT berbasis kerangka kerja Ward and Peppard, 10 inisiatif strategis telah dirumuskan dan dipetakan ke dalam "
        "peta jalan 3 tahun (2026–2028). Imlementasi kebijakan password ketat, kewajiban MFA adaptif, verifikasi email, serta otomatisasi "
        "deaktivasi akun terintegrasi terbukti secara langsung menjawab tantangan kepatuhan terhadap SPBE (Perpres 95/2018) dan UU PDP (UU 27/2022), "
        "sekaligus memangkas beban tiket helpdesk SMILE hingga lebih dari 75%."
    )

    # --- REFERENCES ---
    add_h1("REFERENCES")
    refs = [
        "[1] J. Ward and P. Peppard, Strategic Planning for Information Systems, 3rd ed. Chichester, UK: John Wiley & Sons, 2002.",
        "[2] Republik Indonesia, Peraturan Presiden Republik Indonesia Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik. Jakarta: Lembaran Negara RI, 2018.",
        "[3] Republik Indonesia, Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi. Jakarta: Lembaran Negara RI, 2022.",
        "[4] B. F. Hermanto and A. R. Tanaamah, \"Perencanaan Strategis Pada Sistem Informasi dengan Menggunakan Metode Ward and Peppard,\" Jurnal Sistem Komputer dan Informatika (JSON), vol. 3, no. 2, pp. 115–124, 2021.",
        "[5] PUSTIPANDA UIN Syarif Hidayatullah Jakarta, Laporan Empiris Audit Infrastruktur SSO Keycloak dan Rekapitulasi Tiket Helpdesk SMILE, Jakarta: UIN Syarif Hidayatullah Jakarta, 2026.",
        "[6] Red Hat Keycloak Documentation, Server Administration Guide: Securing Applications and Services, Red Hat, Inc., 2025.",
        "[7] N. Sudzhana, \"Perencanaan Strategis Sistem Informasi Menggunakan Pendekatan Ward dan Peppard,\" Tematik, vol. 4, no. 1, pp. 68–85, 2017.",
        "[8] National Institute of Standards and Technology (NIST), Digital Identity Guidelines: Authentication and Lifecycle Management, NIST Special Publication 800-63B, 2020."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_after = Pt(4)
        run_ref = p_ref.add_run(ref)
        run_ref.font.size = Pt(8.5)
        run_ref.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Footer note
    p_ftr = doc.add_paragraph()
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ftr.paragraph_format.space_before = Pt(16)
    r_ftr = p_ftr.add_run("Wandy et al., Copyright © 2026, Jurnal JSON, Page 1-14")
    r_ftr.font.size = Pt(8)
    r_ftr.font.italic = True
    r_ftr.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    # Save to file
    doc.save(output_path)
    print(f"File DOCX berhasil dibuat di: {output_path}")

if __name__ == "__main__":
    out_dir = r"e:\strategic-planning-sso-mfa\release"
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, "Perencanaan_Strategis_SSO_MFA_UIN_Jakarta.docx")
    create_journal_docx(file_path)
