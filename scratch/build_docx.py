import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def make_callout(doc, text_list, title="CATATAN KUNCI"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border thick primary color
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Arial"
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor(0, 51, 102)
    
    for t in text_list:
        p_sub = cell.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(2)
        run = p_sub.add_run(t)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(51, 51, 51)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def generate_docx():
    doc = Document()
    
    # Set page margins (1 inch all around)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles config
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)
    
    # Title Page / Cover Section
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("PERENCANAAN STRATEGIS SISTEM INFORMASI DENGAN METODE WARD & PEPPARD UNTUK INTEGRASI MULTI-FACTOR AUTHENTICATION (MFA) PADA SINGLE SIGN-ON (SSO)")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(16)
    run_title.font.color.rgb = RGBColor(0, 51, 102)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    run_sub = p_sub.add_run("Studi Kasus: UIN Syarif Hidayatullah Jakarta")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(102, 102, 102)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(36)
    run_meta = p_meta.add_run("DOKUMEN RENCANA STRATEGIS FINAL (FINAL STRATEGIC PLAN)\nFokus Analisis: SWOT & PESTEL\nTanggal Pengesahan: 21 September 2026\nStatus: DIKUNCI / LOCKED (M0 - M14)")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(10)
    run_meta.font.color.rgb = RGBColor(128, 128, 128)
    
    doc.add_page_break()
    
    # Helper to add headings
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(8)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 51, 102)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 77, 153)
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(51, 51, 51)
        return h

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(bold_prefix + " ")
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(10.5)
        r2 = p.add_run(text)
        r2.font.name = "Arial"
        r2.font.size = Pt(10.5)
        return p

    def format_table(table, col_widths, headers, data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "003366")
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.bold = True
                r.font.name = "Arial"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
                
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = cell_value
                set_cell_background(row_cells[col_idx], bg)
                set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
                p = row_cells[col_idx].paragraphs[0]
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(9.0)
                    r.font.color.rgb = RGBColor(51, 51, 51)
                    
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
                
        set_table_borders(table)

    # ----------------------------------------------------
    # RINGKASAN EKSEKUTIF
    # ----------------------------------------------------
    add_h1("RINGKASAN EKSEKUTIF")
    add_p("Dokumen Rencana Strategis ini menyajikan perencanaan strategis Sistem Informasi/Teknologi Informasi (SI/TI) untuk transformasi sistem Single Sign-On (SSO e-Semesta) di UIN Syarif Hidayatullah Jakarta menuju penerapan Multi-Factor Authentication (MFA) yang aman, patuh regulasi, efisien, dan ramah pengguna.")
    add_p("Studi ini mengadopsi metodologi Ward & Peppard dengan fokus analisis lingkungan menggunakan analisis SWOT (Strengths, Weaknesses, Opportunities, Threats) dan analisis PESTEL (Political, Economic, Social, Technological, Environmental, Legal). Seluruh analisis didasarkan pada 19 sumber bukti terdaftar (S1 s/d S19), 12 bukti teknis tangkapan layar Keycloak Admin Console (T-01 s/d T-12), 3 dokumen operasional resmi (D-01 s/d D-03), dan 10 konfirmasi data pengguna (U-01 s/d U-10).")
    
    make_callout(doc, [
        "Sistem SSO e-Semesta (Keycloak realm SSOUIN) melayani 45.219+ pengguna (42.088 mahasiswa, 1.593 dosen, 1.438 tendik) dan 44 client/aplikasi terintegrasi.",
        "Celah Keamanan Kritis: Kebijakan Kata Sandi (Password Policy) KOSONG (T-06), kata sandi default terprediksi berbasis NIK/NIM (U-06, U-07), MFA belum diwajibkan (T-04), dan Verify Email DISABLED (T-04).",
        "Beban Operasional Helpdesk SMILE menangani 2.624 tiket manual terkait masalah login/reset kata sandi (D-02).",
        "Rekomendasi Strategis: Penerapan TOTP Massal nirbiaya lisensi untuk 45rb pengguna, FIDO2/WebAuthn untuk admin, Password Policy Enforcer, dan Self-Service Recovery mandiri.",
        "Target Hasil (KPI): Penurunan tiket helpdesk SMILE >80% (menjadi <500 tiket/tahun), adopsi TOTP massal >85%, dan 100% kepatuhan UU PDP No. 27/2022."
    ], title="RANGKUMAN HASIL STRATEGIS")

    # ----------------------------------------------------
    # BAB I: PENDAHULUAN & ORGANIZATIONAL CONTEXT
    # ----------------------------------------------------
    add_h1("BAB I: PENDAHULUAN & ORGANIZATIONAL CONTEXT")
    add_h2("1.1 Profil Institusi & Konteks Layanan SSO")
    add_p("UIN Syarif Hidayatullah Jakarta merupakan Perguruan Tinggi Keagamaan Islam Negeri (PTKIN) terkemuka yang menyelenggarakan layanan pendidikan tinggi bagi 45.219+ sivitas akademika. Untuk memfasilitasi akses digital terpadu, institusi mengoperasikan portal SSO e-Semesta berbasis platform Keycloak Identity Provider (realm SSOUIN).")
    
    add_h2("1.2 Perumusan Masalah Utama")
    add_p("Meskipun SSO e-Semesta telah mengintegrasikan 44 aplikasi institusi, sistem autentikasi saat ini masih sepenuhnya bergantung pada kata sandi faktor tunggal (single-factor password). Kondisi ini diperparah oleh penggunaan kata sandi default terprediksi berbasis NIK/NIM dan ketiadaan kebijakan kata sandi (Password Policy kosong). Hal ini menciptakan kerentanan tinggi terhadap serangan penyerobotan akun (credential guessing & stuffing), phishing, dan ketidakpatuhan terhadap regulasi pelindungan data pribadi (UU PDP No. 27 Tahun 2022).")
    
    add_h2("1.3 Pendekatan Metodologi Ward & Peppard")
    add_p("Perencanaan strategis ini mengeksekusi kerangka kerja Ward & Peppard yang disesuaikan, berfokus pada analisis lingkungan bisnis internal/eksternal dan SI/TI internal/eksternal menggunakan analisis SWOT dan PESTEL. Sesuai arahan, analisis Value Chain, Porter Five Forces, McFarlan Strategic Grid, dan Critical Success Factors (CSF) dieliminasi untuk menjaga fokus studi.")

    # ----------------------------------------------------
    # BAB II: KONDISI SAAT INI SSO (CURRENT STATE BASELINE)
    # ----------------------------------------------------
    add_h1("BAB II: KONDISI SAAT INI SSO (CURRENT STATE BASELINE)")
    add_h2("2.1 Arsitektur SSO Eksisting")
    add_p("Platform SSO menggunakan Keycloak (realm SSOUIN). Domain development berada pada dev-sso.uinjkt.ac.id, sedangkan lingkungan produksi berada pada app-sso.uinjkt.ac.id. Mekanisme federasi identitas menggunakan provider User Migration Using A REST Client (T-02):")
    add_bullet("Dosen & Tendik:", "Dikelola oleh eSDM dengan status User Federation enabled dan menyinkronkan data secara real-time via client esdm-sync-service (T-11, U-10).")
    add_bullet("Mahasiswa:", "Seluruh akun mahasiswa di SSO produksi telah dimigrasi penuh ke database lokal Keycloak (U-09), sehingga entry User Federation eAkademik berada pada status disabled (T-02).")

    add_h2("2.2 Inventaris Integrasi Aplikasi (44 Client Terdaftar)")
    add_p("Hasil penelusuran 3 halaman Keycloak Admin Console (T-10, T-11, T-12) mengonfirmasi 44 client terdaftar yang mencakup ranah akademik (eAkademik, eRegistrasi, dev-lms, eRiset, eKKN, PLO), keuangan (eFinansi, ePembayaran, eAset, eBeasiswa), SDM (eSDM, eKinerja), dan akses jaringan kampus (Wi-Fi SSO MHS & STAF).")

    add_h2("2.3 Evaluasi Kontrol Keamanan Baseline")
    t_base = doc.add_table(rows=5, cols=3)
    format_table(t_base, [1.8, 3.2, 1.5], 
                 ["Komponen Keamanan", "Kondisi Eksisting (As-Is)", "Kode Bukti"],
                 [
                     ["Password Policy", "KOSONG — Tidak ada aturan panjang minimal, kompleksitas, atau lockout.", "T-06"],
                     ["Kredensial Default", "Mahasiswa: Mhs+NIK; Dosen/Tendik: NIK saja tanpa prefix (Terprediksi).", "U-06, U-07"],
                     ["Required Actions", "Update Password = Default & Enabled; Configure OTP = Enabled (Non-default); Verify Email = DISABLED.", "T-04"],
                     ["Logging & Audit", "Login Events & Admin Events = ON; Expiration (retensi log) = KOSONG.", "T-03, T-08"]
                 ])

    # ----------------------------------------------------
    # BAB III: ANALISIS LINGKUNGAN BISNIS INTERNAL
    # ----------------------------------------------------
    add_h1("BAB III: ANALISIS LINGKUNGAN BISNIS INTERNAL")
    add_h2("3.1 Pemetaan Layanan Bisnis Terdampak Autentikasi")
    add_bullet("Layanan Akademik & Kemahasiswaan:", "Penerimaan mhs (eadmisi, eRegistrasi), perkuliahan (eAkademik, dev-lms), riset & KKN (eRiset, eKKN, PLO), dan alumni (eAlumni).")
    add_bullet("Layanan Tata Kelola SDM:", "Pengelolaan pegawai/dosen (eSDM) dan penilaian kinerja (eKinerja). eSDM berwenang enable/disable akun SSO secara real-time.")
    add_bullet("Layanan Keuangan & Aset:", "Pembayaran UKT/BOPTN (eFinansi, ePembayaran) dan pencatatan BMN (eAset).")
    add_bullet("Layanan Operasional Jaringan:", "Akses internet Wi-Fi SSO kampus dengan batas 3 perangkat simultan per akun (D-01, D-03).")

    add_h2("3.2 Analisis Kebutuhan Pemangku Kepentingan (Stakeholder Needs)")
    t_stake = doc.add_table(rows=5, cols=3)
    format_table(t_stake, [1.8, 2.7, 2.0],
                 ["Pemangku Kepentingan", "Kebutuhan Utama (Needs)", "Tantangan / Pain Points"],
                 [
                     ["Mahasiswa (~42rb)", "Akses cepat/stabil ke eAkademik & Wi-Fi; pemulihan akun mandiri.", "Password default berisiko; kebingungan saat lupa password."],
                     ["Dosen & Tendik (~3rb)", "Kelancaran input nilai/materi & akses aplikasi administratif (eSDM, eFinansi).", "Password default (NIK) rawan ditebak; tidak ada MFA."],
                     ["Tim Helpdesk PUSTIPANDA", "Pengurangan tiket reset password manual & prosedur verifikasi jelas.", "Menangani 2.624 tiket manual via SMILE (D-02); Verify Email mati."],
                     ["Pimpinan Universitas", "Pelindungan reputasi UIN Jakarta, kepatuhan UU PDP, keberlanjutan e-Semesta.", "Risiko kebocoran data akibat autentikasi faktor tunggal."]
                 ])

    # ----------------------------------------------------
    # BAB IV: ANALISIS LINGKUNGAN BISNIS EKSTERNAL & PESTEL
    # ----------------------------------------------------
    add_h1("BAB IV: ANALISIS LINGKUNGAN BISNIS EKSTERNAL & PESTEL")
    add_h2("4.1 Kerangka Regulasi & Kepatuhan Hukum")
    add_p("Sebagai Pengendali Data Pribadi berdasarkan UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP), UIN Jakarta wajib melindungi data pribadi sivitas akademika dari akses tidak sah. Penggunaan kata sandi default NIK tanpa MFA merupakan risiko kepatuhan hukum serius. Selain itu, Perpres No. 95 Tahun 2018 tentang SPBE dan standar keamanan BSSN/ISO 27001 mewajibkan penerapan autentikasi kuat (strong authentication).")

    add_h2("4.2 Analisis PESTEL (Sistem Autentikasi SSO UIN Jakarta)")
    t_pestel = doc.add_table(rows=7, cols=2)
    format_table(t_pestel, [1.8, 4.7],
                 ["Faktor PESTEL", "Analisis & Implikasi pada SSO UIN Jakarta"],
                 [
                     ["Political (Politik)", "Kebijakan SPBE nasional mendorong penguatan keamanan informasi terpadu di PTN."],
                     ["Economic (Ekonomi)", "Efisiensi anggaran dengan menekan beban operasional 2.624 tiket SMILE dan menghindari biaya lisensi OTP SMS/WA."],
                     ["Social (Sosial)", "Variasi literasi digital sivitas akademika menuntut solusi MFA yang ramah pengguna (user-friendly)."],
                     ["Technological (Teknologi)", "Ketersediaan kapabilitas TOTP/WebAuthn bawaan Keycloak membuka peluang penerapan MFA nirbiaya lisensi."],
                     ["Environmental (Lingkungan)", "Digitalisasi tata kelola (PLO paperless) meningkatkan ketergantungan pada keandalan SSO."],
                     ["Legal (Hukum)", "Kepatuhan wajib pada UU PDP No. 27/2022 untuk menghindari sanksi administratif/hukum akibat kebocoran data."]
                 ])

    # ----------------------------------------------------
    # BAB V & VI: EVALUASI SI/TI INTERNAL & EKSTERNAL
    # ----------------------------------------------------
    add_h1("BAB V & VI: EVALUASI SI/TI INTERNAL & EKSTERNAL")
    add_h2("5.1 Evaluasi Platform & Celah Teknis Keycloak (M5)")
    add_p("Keycloak SSO (realm SSOUIN) berbasis Quarkus/JPA dan Infinispan terbukti kokoh dan telah mendukung modul TOTP serta WebAuthn SPI secara bawaan (T-01). Namun, celah teknis mendasar terletak pada konfigurasi keamanan: Password Policy kosong (T-06), Verify Email disabled (T-04), MFA belum diwajibkan (T-04), dan Expiration log retention kosong (T-08).")

    add_h2("5.2 Evaluasi Rumpun Teknologi MFA (M6)")
    add_p("Evaluasi netral terhadap 5 rumpun teknologi MFA menyimpulkan:")
    add_bullet("TOTP via Authenticator Apps (Google/FreeOTP):", "Pilihan Terbaik untuk Massal (~45rb pengguna) karena didukung native Keycloak, bebas biaya lisensi/pesan, dan bekerja offline.")
    add_bullet("FIDO2 / WebAuthn Passkeys:", "Pilihan Terbaik untuk Akun Privileged / Admin karena memberikan ketahanan maksimal terhadap serangan phishing & MitM.")
    add_bullet("SMS / WhatsApp OTP:", "TIDAK DIREKOMENDASIKAN karena potensi pembengkakan biaya operasional pesan berulang yang tidak terkelola bagi anggaran universitas.")

    # ----------------------------------------------------
    # BAB VII: ANALISIS SWOT & ISU-ISU STRATEGIS
    # ----------------------------------------------------
    add_h1("BAB VII: ANALISIS SWOT & ISU-ISU STRATEGIS")
    add_h2("7.1 Matriks Analisis SWOT")
    t_swot = doc.add_table(rows=5, cols=2)
    format_table(t_swot, [3.25, 3.25],
                 ["STRENGTHS (Kekuatan Internal)", "WEAKNESSES (Kelemahan Internal)"],
                 [
                     ["• Keycloak SSO terpusat & modern berbasis Quarkus/JPA.\n• Integrasi terpusat pada 44 client aplikasi.\n• Sync real-time eSDM & migrasi mhs penuh di prod.\n• Kapabilitas TOTP & WebAuthn ready secara native.\n• Audit logging (Login/Admin Events) aktif.",
                      "• Password Policy KOSONG (T-06).\n• Password default NIK/NIM terprediksi (U-06, U-07).\n• MFA belum diwajibkan (non-default Required Action).\n• Verify Email DISABLED (T-04).\n• Retensi log Expiration KOSONG & 2.624 tiket SMILE."]
                 ])
    
    t_swot_2 = doc.add_table(rows=2, cols=2)
    format_table(t_swot_2, [3.25, 3.25],
                 ["OPPORTUNITIES (Peluang Eksternal)", "THREATS (Ancaman Eksternal)"],
                 [
                     ["• Mandat regulasi UU PDP No. 27/2022 & Perpres SPBE.\n• TOTP Keycloak BEBAS BIAYA lisensi/pesan berulang.\n• Adopsi FIDO2/Passkey untuk akun admin.\n• Budaya digitalisasi & hybrid learning perguruan tinggi.",
                      "• Serangan credential guessing & stuffing pada NIK/NIM.\n• Phishing menembus autentikasi faktor tunggal.\n• Penyalahgunaan akses Wi-Fi SSO oleh pihak luar.\n• Sanksi hukum UU PDP & pencemaran reputasi institusi."]
                 ])

    add_h2("7.2 Formulasi Strategi Matriks TOWS")
    add_bullet("Strategi SO:", "Memanfaatkan kapabilitas native Keycloak (TOTP & WebAuthn) nirbiaya lisensi pada 44 client terintegrasi untuk memenuhi kepatuhan UU PDP & SPBE.")
    add_bullet("Strategi WO:", "Mengonfigurasi Password Policy & Verify Email di Keycloak untuk memenuhi standar BSSN sekaligus memotong tiket helpdesk SMILE.")
    add_bullet("Strategi ST:", "Mewajibkan TOTP bagi seluruh pengguna untuk melumpuhkan ancaman phishing dan credential stuffing.")
    add_bullet("Strategi WT:", "Menghentikan kata sandi default NIK/NIM dan menerapkan pelindungan FIDO2/WebAuthn khusus pada akun admin.")

    add_h2("7.3 4 Isu Strategis Terprioritas")
    add_bullet("IS-1 (Prioritas 1 - Kritis):", "Penanganan Kerentanan Kata Sandi Faktor Tunggal & Password Default NIK/NIM.")
    add_bullet("IS-2 (Prioritas 2 - Kritis):", "Penerapan Multi-Factor Authentication (MFA/TOTP) Bertahap Berbasis Risiko.")
    add_bullet("IS-3 (Prioritas 3 - Tinggi):", "Peningkatan Pemulihan Akun Mandiri (Self-Service Recovery) untuk Mengurangi Beban Helpdesk SMILE.")
    add_bullet("IS-4 (Prioritas 4 - Sedang-Tinggi):", "Penguatan Tata Kelola, Retensi Log Audit (180 Hari), dan SOP Keamanan SSO.")

    # ----------------------------------------------------
    # BAB VIII: ANALISIS KESENJANGAN (GAP ANALYSIS)
    # ----------------------------------------------------
    add_h1("BAB VIII: ANALISIS KESENJANGAN (GAP ANALYSIS)")
    t_gap = doc.add_table(rows=8, cols=4)
    format_table(t_gap, [1.2, 1.8, 1.8, 1.7],
                 ["Dimensi", "Kondisi Saat Ini (As-Is)", "Kondisi Target (To-Be)", "Tindakan Penutupan Gap"],
                 [
                     ["Teknologi", "MFA Configure OTP non-default; WebAuthn belum di-register.", "MFA diwajibkan (TOTP massal, WebAuthn admin).", "Set OTP sebagai Default Action & register WebAuthn SPI."],
                     ["Kebijakan", "Password Policy KOSONG (T-06); Verify Email DISABLED.", "Password Policy ketat & Verify Email ENABLED.", "Enforce Password Policy & aktifkan Verify Email."],
                     ["Proses", "Password default NIK; 2.624 tiket SMILE manual.", "Password NIK terhapus; self-service recovery mandiri.", "Wajibkan Update Password login 1 & reset mandiri via email."],
                     ["Tata Kelola", "Belum ada dokumen SOP resmi SSO.", "SOP resmi operasional, role matrix, & insiden SSO.", "Menyusun dan mengesahkan dokumen SOP Keamanan SSO."],
                     ["SDM", "Beban helpdesk tersedot tiket manual.", "Helpdesk fokus eskalasi; user paham TOTP.", "Kampanye edukasi TOTP & pelatihan SOP helpdesk."],
                     ["Audit Log", "Event Expiration KOSONG (T-08).", "Retensi log audit 180 hari (auto-purge).", "Konfirmasi Expiration Policy 180 hari di Keycloak."],
                     ["Risiko", "Autentikasi 1-faktor rentan pembobolan.", "Autentikasi 2-faktor yang compliant UU PDP.", "Integrasi Step-Up MFA pada 44 client aplikasi."]
                 ])

    # ----------------------------------------------------
    # BAB IX: FORMULASI TIGA PILAR STRATEGI SI/TI
    # ----------------------------------------------------
    add_h1("BAB IX: FORMULASI TIGA PILAR STRATEGI SI/TI")
    add_h2("9.1 Pilar 1: Strategi Sistem Informasi (IS Strategy)")
    add_bullet("SI-1:", "Integrasi Layanan Autentikasi Berlapis (MFA Step-Up) pada 44 Client Aplikasi Terdaftar.")
    add_bullet("SI-2:", "Peluncuran Sistem Pemulihan Identitas Mandiri (Self-Service Recovery System) via Email Terverifikasi.")
    add_bullet("SI-3:", "Penguatan Integrasi Otomatis Siklus Hidup Identitas (eRegistrasi -> eAkademik -> Keycloak & eSDM Sync).")

    add_h2("9.2 Pilar 2: Strategi Teknologi Informasi (IT Strategy)")
    add_bullet("TI-1:", "Pengerasan Keamanan Keycloak (Hardening: Enforce Password Policy, Verify Email, Event Expiration 180 Hari).")
    add_bullet("TI-2:", "Penerapan MFA Rumpun TOTP via Authenticator Apps untuk Massal (~45.000 Sivitas Akademika).")
    add_bullet("TI-3:", "Penerapan MFA FIDO2 / WebAuthn Passkeys untuk Akun Administrative / Privileged.")
    add_bullet("TI-4:", "Penghentian Total Kata Sandi Default berbasis NIK/NIM via Update Password Required Action Login Pertama.")

    add_h2("9.3 Pilar 3: Strategi Manajemen SI/TI (IS/IT Management Strategy)")
    add_bullet("MGT-1:", "Penyusunan dan Pengesahan Dokumentasi SOP Resmi Operasional & Keamanan SSO.")
    add_bullet("MGT-2:", "Efisiensi Layanan Helpdesk SMILE melalui Edukasi & Panduan Visual Pendaftaran TOTP Mandiri.")
    add_bullet("MGT-3:", "Kepatuhan Regulasi UU PDP No. 27/2022 & Audit Log Keamanan Berkala.")

    # ----------------------------------------------------
    # BAB X: ARSITEKTUR KONSEPTUAL TARGET & ALUR AUTENTIKASI
    # ----------------------------------------------------
    add_h1("BAB X: ARSITEKTUR KONSEPTUAL TARGET & ALUR AUTENTIKASI")
    add_h2("10.1 Pembandingan Arsitektur Eksisting (As-Is) vs Target (To-Be)")
    add_p("Arsitektur Eksisting (As-Is) menempatkan Keycloak tanpa Password Policy, tanpa Verify Email, dan tanpa MFA diwajibkan, sehingga 44 aplikasi rentan terhadap phishing. Arsitektur Target (To-Be) menambahkan WAF/Reverse Proxy di lapisan perimeter, mengaktifkan Password Policy Enforcer, Required Action Pipeline, TOTP & WebAuthn Engine, serta Event Expiration 180 Hari.")

    add_h2("10.2 Pembandingan Alur Autentikasi")
    t_flow = doc.add_table(rows=4, cols=3)
    format_table(t_flow, [1.8, 2.3, 2.4],
                 ["Jenis Alur", "Alur Eksisting (As-Is)", "Alur Target Terimprovisasi (To-Be)"],
                 [
                     ["Login Rutin", "Input Username + Password Default NIK -> Langsung Masuk (Faktor Tunggal).", "Input Username & Password -> Validasi -> Input 6-Digit TOTP -> Token Issued -> Masuk."],
                     ["Login Pertama", "Input Password Default NIK -> Ganti Password (tanpa kriteria kompleksitas).", "Input Kredensial Awal -> Wajib Password Kompleks -> Verifikasi Email Kampus -> Scan QR TOTP."],
                     ["Lupa Password", "Verify Email Mati -> Mengajukan Tiket Manual ke SMILE (2.624 tiket, D-02).", "Klik Forgot Password -> Tautan Reset ke Email Terverifikasi -> Reset Password & Konfirmasi TOTP."]
                 ])

    # ----------------------------------------------------
    # BAB XI: PETA JALAN IMPLEMENTASI & MANAJEMEN RISIKO
    # ----------------------------------------------------
    add_h1("BAB XI: PETA JALAN IMPLEMENTASI & MANAJEMEN RISIKO")
    add_h2("11.1 Pentahapan Peta Jalan 12-Bulan (Q1 s/d Q4)")
    add_bullet("Fase 1: Quick Wins & Fondasi Keamanan (Q1 / Bulan 1–3):", "Keycloak Hardening (TI-1), Penghentian Password NIK Default (TI-4), Pengesahan Dokumen SOP SSO (MGT-1).")
    add_bullet("Fase 2: MFA Massal & Pemulihan Mandiri (Q2–Q3 / Bulan 4–9):", "Integrasi MFA 44 Client (SI-1), Rollout TOTP Massal (TI-2), Peluncuran Self-Service Recovery (SI-2), Kampanye Edukasi User & Helpdesk SMILE (MGT-2), Auto-Sync Lifecycle (SI-3).")
    add_bullet("Fase 3: Privileged Protection & Audit Kepatuhan (Q4 / Bulan 10–12):", "Implementasi WebAuthn/FIDO2 Admin (TI-3), Audit Kepatuhan UU PDP & Retensi Log 180 Hari (MGT-3).")

    add_h2("11.2 Manajemen Risiko & Mitigasi Strategis")
    add_bullet("Risiko Kebingungan User TOTP:", "Mitigasi via panduan visual, video tutorial, dan masa transisi pendaftaran mandiri 30 hari sebelum MFA enforced.")
    add_bullet("Risiko Lonjakan Tiket SMILE:", "Mitigasi via fitur backup codes dan task force helpdesk dedicated PUSTIPANDA selama 2 minggu Go-Live.")
    add_bullet("Risiko Perangkat Hilang:", "Mitigasi via alur pemulihan mandiri berbasis email kampus terverifikasi.")

    # ----------------------------------------------------
    # BAB XII: INDIKATOR KINERJA UTAMA (KPI STRATEGIS)
    # ----------------------------------------------------
    add_h1("BAB XII: INDIKATOR KINERJA UTAMA (KPI STRATEGIS)")
    t_kpi = doc.add_table(rows=7, cols=4)
    format_table(t_kpi, [1.5, 2.5, 1.2, 1.3],
                 ["Kode KPI", "Indikator Kinerja Utama", "Baseline M2", "Target M13"],
                 [
                     ["KPI-1", "Adopsi TOTP Massal (Mahasiswa, Dosen, Tendik)", "0% (Non-Default)", ">85% (Q3) / 100% (Q4)"],
                     ["KPI-2", "Adopsi WebAuthn/FIDO2 Akun Admin", "0% (Faktor Tunggal)", "100% (Q1 Admin, Q4 All)"],
                     ["KPI-4", "Penegakan Kebijakan Password Policy", "Kosong (T-06)", "100% Enforced di Q1"],
                     ["KPI-5", "Eliminasi Kata Sandi Default NIK/NIM", "0% Terhapus", "100% Terhapus di Q1"],
                     ["KPI-7", "Penurunan Volume Tiket Helpdesk SMILE", "2.624 Tiket (D-02)", "Penurunan >80% (<500/th)"],
                     ["KPI-12", "Kepatuhan Regulasi UU PDP No. 27/2022", "Non-Compliant", "100% Compliant (Audit)"]
                 ])

    # ----------------------------------------------------
    # BAB XIII: KESIMPULAN & REKOMENDASI PENUTUP
    # ----------------------------------------------------
    add_h1("BAB XIII: KESIMPULAN & REKOMENDASI PENUTUP")
    add_p("Perencanaan Strategis Sistem Informasi integrasi Multi-Factor Authentication (MFA) pada Single Sign-On (SSO) UIN Syarif Hidayatullah Jakarta menyimpulkan:")
    add_bullet("Tanpa Pembangunan Ulang Infrastruktur:", "Mengoptimalkan kapabilitas native platform Keycloak SSO yang sudah ada.")
    add_bullet("Bebas Biaya Lisensi Berulang:", "Memilih teknologi TOTP berbasis Authenticator Apps yang bebas biaya per-pesan.")
    add_bullet("Menutup Celah Kritis:", "Menghapuskan kata sandi default NIK, menegakkan Password Policy ketat, dan mengaktifkan verifikasi email mandiri.")
    add_bullet("Efisiensi Operasional:", "Memotong >80% tiket manual SMILE melalui fitur Self-Service Identity Recovery.")

    # ----------------------------------------------------
    # LAMPIRAN: REGISTER BUKTI TERDAFTAR
    # ----------------------------------------------------
    add_h1("LAMPIRAN: REGISTER BUKTI TERDAFTAR (SOURCE REGISTER)")
    add_p("Dokumen rencana strategis ini disusun berdasarkan 19 bukti terverifikasi:")
    add_bullet("S1 - S5 / D-01..D-03:", "Ward & Peppard Paper, Tugas 2, Surat Wi-Fi SSO, Ekspor 2.624 Tiket SMILE (D-02), Panduan Wi-Fi SSO (D-03).")
    add_bullet("S6 - S16 / T-01..T-12:", "Tangkapan Layar Keycloak Admin Console (Server Info, User Federation, Login Events, Required Actions, Clients H1-H3, Password Policy Kosong, OTP Policy, Events Config, Client Scopes).")
    add_bullet("S17 - S19 / U-06..U-10:", "Konfirmasi data pengguna (Password Default Mhs/Dosen/Tendik U-06/U-07, Migrasi Mahasiswa Penuh & Deaktivasi 3 Bulan Pasca LULUS U-09, Sync Real-Time eSDM & Immediate Disable Nonaktif/DO U-10).")

    doc.save("e:/strategic-planning-sso-mfa/Perencanaan_Strategis_SSO_MFA_UIN_Jakarta.docx")
    print("DOCX successfully generated at e:/strategic-planning-sso-mfa/Perencanaan_Strategis_SSO_MFA_UIN_Jakarta.docx")

if __name__ == "__main__":
    generate_docx()
