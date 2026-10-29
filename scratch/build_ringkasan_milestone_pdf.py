"""Bangun PDF ringkasan M0–M14 dan kebutuhan evidence pendukung presentasi."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

OUT = "release/Ringkasan_Milestone_dan_Evidence_SSO_MFA.pdf"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVS-B", FONT_DIR + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV", boldItalic="DV-B")

NAVY = colors.HexColor("#14213D")
ACCENT = colors.HexColor("#B4501A")
SAND = colors.HexColor("#ECE8DE")
SOFT = colors.HexColor("#F7F5EF")
GREY = colors.HexColor("#3D4555")

base = ParagraphStyle("base", fontName="DV", fontSize=9, leading=12.5, textColor=GREY)
body = ParagraphStyle("body", parent=base, fontSize=9.5, leading=13.5, spaceAfter=4)
small = ParagraphStyle("small", parent=base, fontSize=8, leading=10.5)
cell = ParagraphStyle("cell", parent=base, fontSize=8, leading=10.5)
cellb = ParagraphStyle("cellb", parent=cell, fontName="DV-B", textColor=NAVY)
head = ParagraphStyle("head", parent=cell, fontName="DV-B", textColor=colors.white)
h1 = ParagraphStyle("h1", fontName="DVS-B", fontSize=20, leading=25, textColor=NAVY, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="DVS-B", fontSize=14, leading=18, textColor=NAVY,
                    spaceBefore=10, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="DV-B", fontSize=10.5, leading=14, textColor=NAVY,
                    spaceBefore=2, spaceAfter=3)
eyebrow = ParagraphStyle("eyebrow", fontName="DV-B", fontSize=8.5, leading=11,
                         textColor=ACCENT, alignment=TA_LEFT)

W = A4[0] - 36 * mm


def P(text, style=cell):
    return Paragraph(text, style)


def table(rows, widths, header=True, zebra=True):
    data = []
    for i, r in enumerate(rows):
        st = head if (header and i == 0) else cell
        data.append([c if not isinstance(c, str) else P(c, st) for c in r])
    t = Table(data, colWidths=[w * W for w in widths], repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5CFC1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra:
        for i in range(1 if header else 0, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(cmds))
    return t


# ---------------------------------------------------------------------------
# Data ringkasan milestone: (kode, judul, tahap presentasi, tujuan, metode, hasil, bukti)
MILESTONES = [
    ("M0", "Ruang Lingkup &amp; Baseline", "Persiapan",
     "Mengunci objek, batas, dan kerangka studi sebelum analisis dimulai.",
     "Penetapan scope (in/out of scope), kerangka Ward &amp; Peppard.",
     "Objek: SSO e-Semesta yang sudah berjalan, belum ber-MFA. Fokus: perencanaan strategis, bukan membangun SSO baru. "
     "Di luar lingkup: Zero Trust penuh, SOC/SIEM, keamanan jaringan umum, konfigurasi produk rinci, pengadaan vendor, pentest. "
     "Passwordless/FIDO2/adaptive auth hanya arah masa depan.",
     "SCOPE.md, README.md"),
    ("M1", "Konteks Organisasi", "Tahap 1 · Kondisi saat ini",
     "Menetapkan profil organisasi, pemangku kepentingan, dan konteks layanan SSO berbasis bukti.",
     "Profil organisasi, peta stakeholder, evidence register, analisis agregat tiket.",
     "UIN Syarif Hidayatullah Jakarta; pengelola TI: UPT PUSTIPANDA. Populasi: 42.088 mahasiswa, 1.593 dosen, 1.438 staf/tendik. "
     "Stakeholder utama: pimpinan, PUSTIPANDA, Akademik, Keuangan, SDM, pemilik aplikasi, pengguna. "
     "Ekspor SMILE: 2.624 tiket login/kata sandi (1 Jan–21 Sep 2026); median dibuat→ditutup 88,4 jam; 40,2% ditutup ≤24 jam. "
     "Belum ada SOP autentikasi yang tersedia untuk studi.",
     "U-01–U-03, D-01, D-02, situs PUSTIPANDA"),
    ("M2", "Kondisi Saat Ini SSO", "Tahap 1 · Kondisi saat ini",
     "Memotret arsitektur, inventaris integrasi, alur autentikasi, siklus hidup akun, dan kontrol keamanan.",
     "Audit konsol Keycloak (screenshot), wawancara/konfirmasi pengelola, telaah dokumen.",
     "Keycloak realm SSOUIN, 44 client (OIDC dominan + ≥1 SAML). Sumber identitas: eSDM real-time (esdm-sync-service), mahasiswa sudah dimigrasi ke Keycloak. "
     "Password Policy kosong; password default Mhs+NIK / NIK; Configure OTP aktif tapi bukan default; Verify Email off; WebAuthn belum di-register; "
     "Login &amp; Admin Events ON, Expiration kosong. Akun LULUS di-disable 3 bulan pasca lulus; nonaktif/DO seketika.",
     "T-01–T-12, U-05–U-10, D-03"),
    ("M3", "Lingkungan Bisnis Internal", "Tahap 2 · Analisis lingkungan",
     "Memetakan proses bisnis yang bergantung pada autentikasi dan kebutuhan stakeholder.",
     "Analisis proses, stakeholder needs, Value Chain.",
     "SSO berperan ganda: enabler akses (penerimaan → pembelajaran → riset → kelulusan) dan value safeguard (nilai, data SDM, keuangan). "
     "Pain points: penyerobotan akun, tidak ada faktor kedua, beban helpdesk, risiko akun berwenang tinggi.",
     "M1, M2, D-02, U-09, U-10"),
    ("M4", "Lingkungan Bisnis Eksternal", "Tahap 2 · Analisis lingkungan",
     "Memetakan regulasi, ancaman, dan tren eksternal.",
     "Kajian regulasi, threat landscape, PESTEL.",
     "Dua pendorong: kepatuhan (UU PDP No. 27/2022, Perpres 95/2018 SPBE, standar BSSN/ISO 27001 A.9) dan ancaman (credential stuffing, phishing, "
     "penyalahgunaan Wi-Fi, manipulasi data). Tren: hybrid learning, BYOD, ekspektasi kemudahan login.",
     "Teks regulasi (perlu dilampirkan), M2"),
    ("M5", "Lingkungan SI/TI Internal", "Tahap 2 · Analisis lingkungan",
     "Mengevaluasi platform, identitas, integrasi, kontrol keamanan, dan kapasitas SDM TI.",
     "Matriks evaluasi komponen SI/TI, analisis kesiapan MFA.",
     "Platform siap (TOTP &amp; WebAuthn bawaan, OIDC/SAML, logging, sync real-time); celah ada di konfigurasi (OTP non-default, WebAuthn belum "
     "di-register, Password Policy kosong, Verify Email off, retensi log kosong). Belum ada SOP tertulis; helpdesk tersita tiket manual.",
     "T-01–T-12, D-02, D-03, U-03"),
    ("M6", "Lingkungan SI/TI Eksternal", "Tahap 2 · Analisis lingkungan",
     "Memetakan lanskap teknologi MFA tanpa memilih produk lebih dulu.",
     "Matriks perbandingan 5 rumpun MFA berdasarkan 5 kriteria organisasi.",
     "Kriteria: keberlanjutan biaya, dukungan native Keycloak, kemudahan pengguna, ketahanan phishing, bisa offline. "
     "Hasil: TOTP untuk massal; FIDO2/WebAuthn untuk akun privileged; SMS/WA OTP tidak direkomendasikan; passkey arah masa depan.",
     "T-01, T-07, dokumentasi vendor/standar (perlu dilampirkan)"),
    ("M7", "SWOT &amp; Isu Strategis", "Tahap 3 · Prioritas masalah",
     "Mensintesis empat lingkungan menjadi strategi alternatif dan isu prioritas.",
     "SWOT, matriks TOWS (SO, WO, ST, WT).",
     "8 strategi TOWS dikerucutkan menjadi 4 isu: IS-1 password faktor tunggal &amp; default NIK (P1); IS-2 MFA bertahap berbasis risiko (P2); "
     "IS-3 beban helpdesk &amp; self-service (P3); IS-4 tata kelola, retensi log, SOP (P4).",
     "M2–M6"),
    ("M8", "Gap Analysis", "Tahap 3 · Prioritas masalah",
     "Mengukur jarak As-Is ke To-Be dan menetapkan tindakan penutupan.",
     "Matriks gap 7 dimensi.",
     "Dimensi: teknologi, kebijakan, proses, tata kelola, SDM, audit log, risiko. Sebagian besar gap ditutup lewat konfigurasi, kebijakan, dan edukasi, "
     "bukan pembelian teknologi baru.",
     "T-04, T-06, T-08, U-06, D-02"),
    ("M9", "Formulasi Strategi", "Tahap 4 · Strategi &amp; target",
     "Menyusun tiga pilar strategi Ward &amp; Peppard yang dapat ditelusuri ke isu.",
     "IS/IT/IS-IT Management Strategy, matriks keterlacakan.",
     "Strategi SI: SI-1 MFA 44 client, SI-2 self-service recovery, SI-3 otomasi lifecycle. Strategi TI: TI-1 hardening, TI-2 TOTP massal, "
     "TI-3 WebAuthn admin, TI-4 hapus password NIK. Manajemen: MGT-1 SOP, MGT-2 edukasi &amp; helpdesk, MGT-3 audit UU PDP.",
     "M7, M8"),
    ("M10", "Arsitektur Target", "Tahap 4 · Strategi &amp; target",
     "Merancang arsitektur konseptual SSO + MFA (As-Is vs To-Be).",
     "Diagram arsitektur konseptual, alur autentikasi target.",
     "5 lapisan: pengguna, perimeter (WAF + reverse proxy TLS 1.3), Keycloak IdP (policy engine, required actions, TOTP/WebAuthn, log 180 hari), "
     "sumber identitas, 44 aplikasi. 3 alur: pendaftaran pertama, login rutin + OTP, pemulihan mandiri.",
     "M5, M9"),
    ("M11", "Portofolio Strategis", "Tahap 4 · Strategi &amp; target",
     "Memetakan aplikasi/kapabilitas berdasarkan kontribusi strategis.",
     "McFarlan Strategic Grid.",
     "Strategic: Keycloak core, MFA engine, self-service &amp; policy, portal SSO. Key operational: eAkademik, eRegistrasi, eSDM, eKinerja, eFinansi, "
     "ePembayaran, eadmisi, Wi-Fi. High potential: FIDO2/passkey, mCampus, LMS. Support: PLO, eRiset, eKKN, eAset, eBeasiswa, eAlumni.",
     "T-10–T-12, M3"),
    ("M12", "Inisiatif &amp; Roadmap", "Tahap 5 · Roadmap &amp; KPI",
     "Mengurutkan 10 inisiatif dengan pemilik, prioritas, fase, dan risiko.",
     "Taksonomi inisiatif, sequencing, timeline 12 bulan, matriks risiko.",
     "Fase 1 (Q1): TI-1, TI-4, MGT-1. Fase 2 (Q2–Q3): SI-1, TI-2, SI-2, MGT-2, SI-3. Fase 3 (Q4): TI-3, MGT-3. "
     "Risiko: kebingungan TOTP (transisi 30 hari), lonjakan tiket go-live (backup codes, task force 2 minggu), perangkat hilang, kegagalan sync eSDM.",
     "M9, M11"),
    ("M13", "KPI &amp; Pengukuran", "Tahap 5 · Roadmap &amp; KPI",
     "Menetapkan indikator, baseline, target, frekuensi, dan pemilik.",
     "12 KPI dalam 5 domain; mekanisme pemantauan.",
     "Contoh: adopsi TOTP 0% → &gt;85% (Q3); 44 client ber-MFA; tiket SMILE 2.624 → &lt;500/tahun; pemulihan &lt;3 menit; uptime ≥99,9% "
     "(baseline belum ada); retensi log 180 hari; SOP disahkan Q1. Semua angka adalah <b>target</b>, bukan hasil terukur.",
     "M2, D-02, T-06, T-08"),
    ("M14", "Rencana Strategis Final", "Penutup",
     "Mengintegrasikan semua milestone terkunci menjadi dokumen akademik.",
     "Integrasi dokumen, naskah jurnal AISM, SLR.",
     "FINAL_STRATEGIC_PLAN.md, naskah AISM 2 kolom (.docx/.md), SLR, dan deck presentasi.",
     "Seluruh M0–M13"),
]

EVIDENCE = [
    ("T-01", "Keycloak Server Info / Providers", "Kapabilitas tersedia: OIDC/SAML, OTP, WebAuthn, required actions, event store", "7, 8, 9"),
    ("T-02", "User Federation (REST migration)", "16 entry, hanya eSDM enabled", "7, 13"),
    ("T-03", "Login Events", "Event login tercatat (LOGIN_ERROR, dll.)", "7"),
    ("T-04", "Required Actions", "OTP bukan default; Update Password default; Verify Email off; WebAuthn tidak terdaftar", "7, 11"),
    ("T-05, T-10–T-12", "Daftar Clients (3 halaman)", "Total 44 client; client SAML staff; esdm-sync-service", "2, 14"),
    ("T-06", "Password Policy", "Kosong (konfirmasi pengguna)", "7, 11, 16"),
    ("T-07", "OTP Policy", "Default: TOTP SHA1, 6 digit, 30 detik", "8"),
    ("T-08", "Events Config", "Login &amp; Admin Events ON; Expiration kosong", "7, 11, 16"),
    ("T-09", "Client Scopes", "10 OIDC, 1 SAML", "13"),
    ("D-01", "Surat B-42/UPT.2/TI.05.04/04/2026", "Wi-Fi SSO berlaku 1 Mei 2026; batas 3 perangkat", "2"),
    ("D-02", "Ekspor tiket SMILE 20260921", "2.624 tiket; median 88,4 jam ke closed", "2, 7, 16"),
    ("D-03", "Panduan Wi-Fi SSO", "Alur login Wi-Fi; menu Forgot Password", "7"),
    ("U-01", "Data populasi pengguna", "42.088 / 1.593 / 1.438", "2"),
    ("U-06, U-07", "Pola password default", "Mhs+NIK (mahasiswa); NIK (dosen/tendik)", "7"),
    ("U-09, U-10", "Lifecycle akun &amp; sync eSDM", "Migrasi mahasiswa; disable 3 bulan pasca lulus; sync real-time", "7, 12"),
    ("S1, S2", "Paper contoh Ward &amp; Peppard; Tugas 2", "Rujukan struktur metodologi (bukan fakta kasus)", "3, 4"),
]

NEEDED = [
    ("Tinggi", "Validasi konfigurasi <b>produksi</b> (app-sso): screenshot Password Policy, Required Actions, OTP Policy, Events Config",
     "Seluruh bukti T-01–T-12 diambil dari lingkungan development (dev-sso). Penguji bisa menanyakan apakah produksi sama.",
     "Slide 7, 11", "Tim infrastruktur PUSTIPANDA"),
    ("Tinggi", "Klarifikasi alur reset mandiri (Forgot Password) beserta data pemakaiannya",
     "D-03 dan M2 menunjukkan Forgot Password sudah ada, sedangkan deck menulis “tak bisa reset mandiri”. Rumusan yang tepat: reset mandiri ada, tetapi email tidak terverifikasi.",
     "Slide 7, 10, 12", "Tim layanan PUSTIPANDA; log RESET_PASSWORD"),
    ("Tinggi", "Kategori tiket SMILE (lupa password, akun terkunci, lainnya) dan data 12 bulan penuh",
     "Data D-02 hanya mencakup ±8,7 bulan (1 Jan–21 Sep) dan bersumber Email; target KPI-7 “&lt;500/tahun” butuh baseline tahunan yang setara.",
     "Slide 2, 16", "Helpdesk SMILE"),
    ("Tinggi", "Baseline ketersediaan (uptime) SSO 6–12 bulan terakhir",
     "KPI-9 masih [EVIDENCE NEEDED]; target 99,9% belum punya pembanding.",
     "Slide 16", "Tim data center / monitoring"),
    ("Sedang", "Konfirmasi tertulis status SOP/kebijakan autentikasi",
     "Klaim “belum ada SOP” baru berdasar keterangan pengguna (E-07).",
     "Slide 11, 12", "Kepala PUSTIPANDA"),
    ("Sedang", "Renstra/master plan TI universitas",
     "Ward &amp; Peppard menuntut keselarasan dengan strategi bisnis; dokumen ini masih [EVIDENCE NEEDED] di M1.",
     "Slide 3, 12", "Biro perencanaan / PUSTIPANDA"),
    ("Sedang", "Riwayat insiden keamanan akun / account takeover",
     "Baseline KPI-6 hanya “berisiko tinggi”, belum berupa angka.",
     "Slide 9, 16", "Tim keamanan TI"),
    ("Sedang", "Jumlah akun admin/privileged dan estimasi harga security key FIDO2",
     "Dasar target KPI-2 dan anggaran TI-3.",
     "Slide 8, 15, 16", "Tim infrastruktur; katalog vendor"),
    ("Sedang", "Estimasi biaya SMS/WA OTP per pesan × jumlah login",
     "Mendukung klaim bahwa SMS/WA OTP “tidak layak” secara biaya.",
     "Slide 8", "Penawaran penyedia SMS gateway"),
    ("Sedang", "Versi Keycloak dan topologi server (single node/cluster, HA, backup)",
     "Arsitektur target menyebut “Keycloak cluster”; kondisi saat ini belum dibuktikan.",
     "Slide 13", "Tim infrastruktur"),
    ("Rendah", "Daftar client yang aktif di produksi (dev vs prod, mis. eKinerja)",
     "Inventaris 44 client berasal dari dev; ada perbedaan dengan produksi.",
     "Slide 2, 14", "Tim integrasi"),
    ("Rendah", "Definisi dan tanggal data populasi (staf akademik vs tendik)",
     "M1 mencatat kemungkinan tumpang tindih kategori.",
     "Slide 2", "Biro kepegawaian / akademik"),
    ("Rendah", "Survei singkat kepemilikan smartphone dan kesiapan memakai authenticator",
     "Mendukung kelayakan TOTP massal dan masa transisi 30 hari.",
     "Slide 8, 15", "Kuesioner ke sampel pengguna"),
    ("Rendah", "Kutipan pasal regulasi (UU PDP Pasal 35, Perpres 95/2018, pedoman BSSN)",
     "Agar klaim kepatuhan di slide 9 dan 16 punya rujukan pasal yang tepat.",
     "Slide 9, 16", "JDIH / dokumen resmi"),
]

ISSUES = [
    "<b>Reset mandiri.</b> Slide 7 menulis “tak bisa reset mandiri”, padahal M2/M5 dan D-03 menunjukkan menu Forgot Password sudah ada. "
    "Saran rumusan: “reset mandiri ada, tetapi email tidak diverifikasi sehingga banyak pengguna kembali ke SMILE”.",
    "<b>Fase roadmap.</b> Teks M12 menyebut Fase 2 = bulan 4–7 dan Fase 3 = bulan 8–12, sedangkan tabel timeline M12 (dan deck) memakai bulan 4–9 dan 10–12. Pilih satu versi.",
    "<b>Periode baseline tiket.</b> 2.624 tiket mencakup ±8,7 bulan, bukan setahun; bandingkan dengan target tahunan secara hati-hati.",
    "<b>Baseline waktu pemulihan.</b> KPI-8 menyebut “jam s.d. hari”; data D-02 memberi angka yang lebih kuat: median 88,4 jam dari tiket dibuat hingga ditutup.",
    "<b>Sumber lingkungan.</b> Hampir semua bukti teknis berasal dari dev-sso; sebutkan ini secara terbuka jika ditanya.",
    "<b>Data sensitif.</b> SOURCE_REGISTER meminta pola kredensial default tidak direplikasi berlebihan; pertimbangkan menulis “berbasis NIK” tanpa format persisnya di slide publik.",
]


def on_page(c, doc):
    c.saveState()
    c.setFont("DV", 7.5)
    c.setFillColor(GREY)
    c.drawString(18 * mm, 10 * mm, "Ringkasan M0–M14 & Evidence · Perencanaan Strategis SSO + MFA UIN Syarif Hidayatullah Jakarta")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Hal. {doc.page}")
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(18 * mm, A4[1] - 12 * mm, A4[0] - 18 * mm, A4[1] - 12 * mm)
    c.restoreState()


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Ringkasan M0–M14 dan Evidence Pendukung",
                            author="Wandy Hanyudha")
    s = []
    s.append(P("DATA DUKUNG PRESENTASI", eyebrow))
    s.append(P("Ringkasan Milestone M0–M14 dan Evidence Pendukung", h1))
    s.append(P("Perencanaan Strategis SSO Terintegrasi Multi-Factor Authentication · Metode Ward &amp; Peppard · "
               "SSO e-Semesta (Keycloak) UIN Syarif Hidayatullah Jakarta", body))
    s.append(P("Wandy Hanyudha · 2250420010", body))
    s.append(Spacer(1, 6))

    s.append(P("Cara membaca dokumen ini", h3))
    s.append(P("Bagian A merangkum 15 milestone. Kolom “Tahap presentasi” menunjukkan di tahap mana milestone itu dibahas saat presentasi, "
               "sehingga kode M tidak perlu disebut ke audiens. Bagian B memuat bukti yang sudah dipakai beserta nomor slide yang didukungnya. "
               "Bagian C memuat bukti yang <b>masih perlu dikumpulkan</b>, dan Bagian D memuat catatan konsistensi yang sebaiknya dibereskan sebelum presentasi.", body))
    s.append(Spacer(1, 4))

    s.append(P("Peta tahap presentasi ke milestone", h3))
    s.append(table([
        ["Pertanyaan pemandu", "Tahap presentasi", "Milestone"],
        ["Di mana kita sekarang?", "Tahap 1 · Memotret kondisi saat ini", "M1, M2"],
        ["", "Tahap 2 · Menganalisis 4 lingkungan Ward &amp; Peppard", "M3, M4, M5, M6"],
        ["", "Tahap 3 · Menentukan masalah prioritas", "M7, M8"],
        ["Ke mana kita ingin menuju?", "Tahap 4 · Merumuskan strategi &amp; arsitektur target", "M9, M10, M11"],
        ["Bagaimana mencapainya?", "Tahap 5 · Menyusun roadmap &amp; KPI", "M12, M13"],
        ["(Pembuka/penutup)", "Ruang lingkup dan dokumen final", "M0, M14"],
    ], [0.3, 0.48, 0.22]))

    s.append(PageBreak())
    s.append(P("A. Ringkasan Milestone M0–M14", h2))
    s.append(P("Semua milestone berstatus LOCKED per 21 September 2026. Setiap milestone melewati siklus: kumpulkan bukti → analisis → draf → review asumsi → kunci.", body))
    for kode, judul, tahap, tujuan, metode, hasil, bukti in MILESTONES:
        rows = [
            [P(f"{kode} · {judul}", head), P(tahap, ParagraphStyle("t", parent=head, alignment=2))],
            [P("<b>Tujuan</b><br/>" + tujuan), P("<b>Metode / alat</b><br/>" + metode)],
            [P("<b>Hasil utama</b><br/>" + hasil), ""],
            [P("<b>Bukti rujukan:</b> " + bukti, small), ""],
        ]
        t = Table(rows, colWidths=[0.58 * W, 0.42 * W])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("SPAN", (0, 2), (1, 2)), ("SPAN", (0, 3), (1, 3)),
            ("BACKGROUND", (0, 3), (-1, 3), SAND),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5CFC1")),
            ("LINEBELOW", (0, 1), (-1, 2), 0.3, colors.HexColor("#D5CFC1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        s.append(KeepTogether([t, Spacer(1, 7)]))

    s.append(PageBreak())
    s.append(P("B. Register Evidence yang Sudah Dipakai", h2))
    s.append(P("Kode bukti mengikuti SOURCE_REGISTER.md (S1–S19). T = bukti teknis Keycloak, D = dokumen resmi, U = konfirmasi pengguna/pengelola. "
               "Kolom terakhir menunjukkan nomor slide pada deck yang didukung.", body))
    s.append(table([["Kode", "Bukti", "Yang dibuktikan", "Slide"]] + [list(e) for e in EVIDENCE],
                   [0.13, 0.3, 0.45, 0.12]))
    s.append(Spacer(1, 6))
    s.append(P("Catatan: halaman Providers (T-01) membuktikan kapabilitas yang <i>tersedia</i>, bukan konfigurasi yang <i>aktif</i>. "
               "Sebagian besar bukti T berasal dari lingkungan development (dev-sso.uinjkt.ac.id).", small))

    s.append(PageBreak())
    s.append(P("C. Evidence Tambahan yang Dibutuhkan", h2))
    s.append(P("Daftar ini disusun dari penanda [EVIDENCE NEEDED] / [TO BE VALIDATED] di dokumen milestone dan dari klaim deck yang belum punya data pendukung. "
               "Prioritas Tinggi sebaiknya dilengkapi sebelum presentasi; Sedang dan Rendah dapat disebut sebagai keterbatasan atau rencana lanjutan.", body))
    s.append(table([["Prioritas", "Evidence yang dibutuhkan", "Alasan", "Slide", "Sumber / narasumber"]] + [list(n) for n in NEEDED],
                   [0.11, 0.26, 0.35, 0.1, 0.18]))

    s.append(Spacer(1, 10))
    s.append(P("D. Catatan Konsistensi Sebelum Presentasi", h2))
    for i, txt in enumerate(ISSUES, 1):
        s.append(P(f"{i}. {txt}", body))

    s.append(Spacer(1, 8))
    s.append(P("Status: dokumen ini adalah rangkuman rencana strategis. Angka KPI merupakan target, bukan hasil implementasi.", small))

    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)


if __name__ == "__main__":
    build()
    print(OUT)
