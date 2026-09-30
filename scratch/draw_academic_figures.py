import os
from PIL import Image, ImageDraw, ImageFont

def draw_arrow(draw, start, end, width=2, arrow_size=8, fill="black"):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=fill, width=width)
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    # Arrow head points
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6),
          y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6),
          y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def draw_box(draw, bbox, title, lines=[], fill="#FFFFFF", outline="#000000", font_title=None, font_text=None, width=2, corner_radius=0):
    x1, y1, x2, y2 = bbox
    if corner_radius > 0:
        draw.rounded_rectangle(bbox, radius=corner_radius, fill=fill, outline=outline, width=width)
    else:
        draw.rectangle(bbox, fill=fill, outline=outline, width=width)
    
    # Calculate vertical spacing
    total_lines = (1 if title else 0) + len(lines)
    line_h = 24
    curr_y = y1 + ( (y2 - y1) - (total_lines * line_h) ) / 2
    
    if title:
        bbox_t = font_title.getbbox(title)
        tw = bbox_t[2] - bbox_t[0]
        draw.text((x1 + (x2 - x1 - tw) / 2, curr_y), title, fill="black", font=font_title)
        curr_y += line_h + 4
        
    for l in lines:
        bbox_l = font_text.getbbox(l)
        lw = bbox_l[2] - bbox_l[0]
        draw.text((x1 + (x2 - x1 - lw) / 2, curr_y), l, fill="black", font=font_text)
        curr_y += line_h

def draw_cylinder(draw, bbox, title, lines=[], fill="#FFFFFF", outline="#000000", font_title=None, font_text=None, width=2):
    x1, y1, x2, y2 = bbox
    cap_h = 16
    # Body
    draw.rectangle([x1, y1 + cap_h, x2, y2 - cap_h], fill=fill, outline=fill)
    draw.line([(x1, y1 + cap_h), (x1, y2 - cap_h)], fill=outline, width=width)
    draw.line([(x2, y1 + cap_h), (x2, y2 - cap_h)], fill=outline, width=width)
    # Bottom ellipse
    draw.ellipse([x1, y2 - cap_h * 2, x2, y2], fill=fill, outline=outline, width=width)
    # Top ellipse
    draw.ellipse([x1, y1, x2, y1 + cap_h * 2], fill=fill, outline=outline, width=width)
    
    # Text
    total_lines = (1 if title else 0) + len(lines)
    line_h = 22
    curr_y = y1 + cap_h + 10
    if title:
        bbox_t = font_title.getbbox(title)
        tw = bbox_t[2] - bbox_t[0]
        draw.text((x1 + (x2 - x1 - tw) / 2, curr_y), title, fill="black", font=font_title)
        curr_y += line_h
    for l in lines:
        bbox_l = font_text.getbbox(l)
        lw = bbox_l[2] - bbox_l[0]
        draw.text((x1 + (x2 - x1 - lw) / 2, curr_y), l, fill="black", font=font_text)
        curr_y += line_h

def generate_academic_figures(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 19)
    font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
    font_text = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    font_small_i = ImageFont.truetype("C:/Windows/Fonts/ariali.ttf", 13)

    # -------------------------------------------------------------------------
    # FIGURE 1: ALUR AUTENTIKASI AS-IS VS TO-BE (LINE ART DRAW.IO STYLE)
    # -------------------------------------------------------------------------
    W1, H1 = 1800, 1100
    img1 = Image.new("RGB", (W1, H1), "#FFFFFF")
    d1 = ImageDraw.Draw(img1)

    # Header / Title
    d1.text((50, 30), "PERBANDINGAN ALUR AUTENTIKASI: SEBELUM (AS-IS) VS SESUDAH (TO-BE)", fill="black", font=font_large)
    d1.line([(50, 70), (1750, 70)], fill="black", width=2)

    # LEFT PANEL: AS-IS (SEBELUM)
    d1.rectangle([50, 90, 880, 1050], fill="#FFFFFF", outline="#000000", width=2)
    d1.rectangle([50, 90, 880, 135], fill="#E5E5E5", outline="#000000", width=2)
    d1.text((70, 100), "KONDISI EKSISTING / SEBELUM (AS-IS): FAKTOR TUNGGAL", fill="black", font=font_title)

    # Box 1.1: Pengguna As-Is
    draw_box(d1, [100, 170, 380, 270], "Pengguna", ["Mahasiswa / Dosen / Tendik", "Akses Web / Wi-Fi Kampus"], font_title=font_bold, font_text=font_text)
    
    # Arrow Pengguna -> SSO
    draw_arrow(d1, (380, 220), (520, 220), width=2, arrow_size=10)
    d1.text((395, 185), "Input NIM/NIP +", fill="black", font=font_small)
    d1.text((395, 202), "Password NIK", fill="black", font=font_small_i)
    d1.text((395, 225), "(Default)", fill="black", font=font_small_i)

    # Box 1.2: Keycloak As-Is
    draw_box(d1, [520, 170, 830, 280], "Keycloak SSO (SSOUIN)", ["Password Policy KOSONG", "Verify Email: DISABLED", "MFA: Non-Default"], font_title=font_bold, font_text=font_text)

    # Arrow SSO -> Aplikasi
    draw_arrow(d1, (675, 280), (675, 360), width=2, arrow_size=10)
    d1.text((685, 305), "Validasi 1-Faktor Saja", fill="black", font=font_small_i)
    d1.text((685, 325), "(Tanpa Verifikasi Kedua)", fill="black", font=font_small)

    # Box 1.3: Aplikasi As-Is
    draw_box(d1, [520, 360, 830, 470], "Aplikasi Terintegrasi (44 Client)", ["eAkademik, eSDM, Finansi, dll.", "[ RENTAN TERHADAP PHISHING &", "CREDENTIAL STUFFING ]"], font_title=font_bold, font_text=font_text)

    # Alur Lupa Password As-Is (Bagian Bawah)
    d1.line([(70, 520), (860, 520)], fill="#777777", width=1)
    d1.text((70, 535), "Alur Penanganan Lupa Password / Kendala Akun Eksisting:", fill="black", font=font_bold)

    draw_box(d1, [100, 590, 380, 680], "Pengguna Lupa Password", ["Email Verifikasi Nonaktif", "Tidak Ada Reset Mandiri"], font_title=font_bold, font_text=font_text)
    
    draw_arrow(d1, (380, 635), (520, 635), width=2, arrow_size=10)
    d1.text((395, 605), "Pengajuan Tiket", fill="black", font=font_small)
    d1.text((395, 622), "Manual ke SMILE", fill="black", font=font_small)

    draw_box(d1, [520, 580, 830, 710], "Helpdesk SMILE PUSTIPANDA", ["2.624 Tiket Manual Menumpuk", "Petugas Verifikasi Manual", "Reset Password Manual"], font_title=font_bold, font_text=font_text)

    draw_arrow(d1, (675, 710), (675, 780), width=2, arrow_size=10)
    
    draw_box(d1, [520, 780, 830, 870], "Dampak Operasional", ["Antrean Layanan Tinggi", "Waktu Tunggu Berjam-jam", "Beban Operasional Tinggi"], font_title=font_bold, font_text=font_text)

    # Evaluasi Ringkas As-Is
    d1.rectangle([100, 900, 830, 1020], fill="#F8F8F8", outline="#000000", width=1)
    d1.text((115, 915), "Ringkasan Celah Keamanan As-Is:", fill="black", font=font_bold)
    d1.text((115, 940), "• Single Point of Failure (SPoF) pada kata sandi tunggal.", fill="black", font=font_text)
    d1.text((115, 965), "• Kredensial default NIK mudah dieksploitasi pihak ketiga.", fill="black", font=font_text)
    d1.text((115, 990), "• Beban operasional helpdesk tinggi akibat ketiadaan reset mandiri.", fill="black", font=font_text)

    # RIGHT PANEL: TO-BE (SESUDAH)
    d1.rectangle([920, 90, 1750, 1050], fill="#FFFFFF", outline="#000000", width=2)
    d1.rectangle([920, 90, 1750, 135], fill="#E5E5E5", outline="#000000", width=2)
    d1.text((940, 100), "KONDISI TARGET / SESUDAH (TO-BE): MULTI-FACTOR AUTHENTICATION", fill="black", font=font_title)

    # Box 2.1: Pengguna To-Be
    draw_box(d1, [960, 170, 1220, 270], "Pengguna", ["Sivitas Akademika UIN", "Login via Web / Mobile"], font_title=font_bold, font_text=font_text)

    draw_arrow(d1, (1220, 220), (1340, 220), width=2, arrow_size=10)
    d1.text((1230, 195), "1. Input Username +", fill="black", font=font_small)
    d1.text((1230, 215), "Password Kompleks", fill="black", font=font_small)

    # Box 2.2: Keycloak SSO To-Be
    draw_box(d1, [1340, 170, 1700, 270], "Keycloak Cluster (IdP)", ["Password Policy Enforced", "Verify Email: Terverifikasi", "Required Action Pipeline"], font_title=font_bold, font_text=font_text)

    # Down Arrow to MFA Factor
    draw_arrow(d1, (1520, 270), (1520, 330), width=2, arrow_size=10)
    d1.text((1530, 290), "2. Tantangan Faktor Ke-2", fill="black", font=font_small_i)

    # Box 2.3: MFA Verification Step
    draw_box(d1, [1310, 330, 1710, 480], "Mesin Autentikasi MFA", [
        "A. Massal (45rb Sivitas): TOTP 6-Digit (FreeOTP/Google Auth)",
        "B. Privileged (Admin): FIDO2 / WebAuthn Hardware Token",
        "[ Kriptografis, Bebas Biaya Lisensi & Tahan Phishing ]"
    ], font_title=font_bold, font_text=font_text)

    draw_arrow(d1, (1520, 480), (1520, 540), width=2, arrow_size=10)
    d1.text((1530, 500), "3. Token OIDC/SAML Issued", fill="black", font=font_small_i)

    # Box 2.4: Aplikasi Terproteksi To-Be
    draw_box(d1, [1310, 540, 1710, 640], "44 Klien Aplikasi Terproteksi", [
        "Akses Aman: eAkademik, eSDM, eFinansi, Wi-Fi",
        "[ Terproteksi Penuh Sesuai UU PDP No. 27/2022 ]"
    ], font_title=font_bold, font_text=font_text)

    # Alur Lupa Password To-Be (Self-Service)
    d1.line([(940, 670), (1730, 670)], fill="#777777", width=1)
    d1.text((940, 685), "Alur Pemulihan Mandiri Terotomasi (Self-Service Recovery):", fill="black", font=font_bold)

    draw_box(d1, [960, 725, 1220, 825], "Pengguna Lupa Password", ["Klik 'Forgot Password'", "Input Email Kampus"], font_title=font_bold, font_text=font_text)

    draw_arrow(d1, (1220, 775), (1330, 775), width=2, arrow_size=10)
    d1.text((1235, 750), "Kirim Tautan", fill="black", font=font_small)
    d1.text((1235, 768), "Reset Mandiri", fill="black", font=font_small)

    draw_box(d1, [1330, 720, 1710, 830], "Portal Pemulihan Mandiri", [
        "Tautan Dikirim ke Email Terverifikasi",
        "Pengguna Buat Password Baru + Konfirmasi OTP",
        "Selesai Mandiri (< 3 Menit) Tanpa Tiket SMILE"
    ], font_title=font_bold, font_text=font_text)

    # Evaluasi Ringkas To-Be
    d1.rectangle([960, 870, 1710, 1020], fill="#F8F8F8", outline="#000000", width=1)
    d1.text((980, 885), "Keunggulan Strategis To-Be:", fill="black", font=font_bold)
    d1.text((980, 910), "• Menutup vektor credential stuffing dan password guessing hingga >98,5%.", fill="black", font=font_text)
    d1.text((980, 935), "• Efisiensi biaya: TOTP nirbiaya lisensi & bebas biaya pulsa SMS.", fill="black", font=font_text)
    d1.text((980, 960), "• Memotong >80% beban tiket manual SMILE melalui reset mandiri.", fill="black", font=font_text)
    d1.text((980, 985), "• Menjamin kepatuhan yuridis UU Pelindungan Data Pribadi (UU PDP).", fill="black", font=font_text)

    out_fig1 = os.path.join(output_dir, "fig1_alur_autentikasi_as_is_vs_to_be.png")
    img1.save(out_fig1, "PNG", dpi=(300, 300))
    # Also save as jpg for direct docx compatibility
    img1.save(os.path.join(output_dir, "fig1_alur_autentikasi_as_is_vs_to_be.jpg"), "JPEG", quality=95)
    print(f"Saved: {out_fig1}")

    # -------------------------------------------------------------------------
    # FIGURE 2: ARSITEKTUR INFRASTRUKTUR KONSEPTUAL SSO-MFA (VISIO STYLE)
    # -------------------------------------------------------------------------
    W2, H2 = 1800, 1200
    img2 = Image.new("RGB", (W2, H2), "#FFFFFF")
    d2 = ImageDraw.Draw(img2)

    # Header / Title
    d2.text((50, 30), "ARSITEKTUR INFRASTRUKTUR KONSEPTUAL TARGET SSO + MFA (REALM SSOUIN)", fill="black", font=font_large)
    d2.line([(50, 70), (1750, 70)], fill="black", width=2)

    # LAYER 1: USER ACCESS LAYER
    d2.rectangle([60, 90, 1740, 230], fill="#FFFFFF", outline="#000000", width=2)
    d2.rectangle([60, 90, 340, 125], fill="#EAEAEA", outline="#000000", width=1)
    d2.text((70, 98), "1. LAPISAN PENGGUNA (USER ACCESS)", fill="black", font=font_bold)

    draw_box(d2, [90, 135, 450, 215], "Mahasiswa (42.088 User)", ["BYOD Smartphone / Laptop", "Portal Akademik, LMS, Wi-Fi"], font_title=font_bold, font_text=font_small)
    draw_box(d2, [490, 135, 850, 215], "Dosen (1.593 User)", ["Workstation Kampus / Laptop", "SIAKAD, eSDM, Riset"], font_title=font_bold, font_text=font_small)
    draw_box(d2, [890, 135, 1250, 215], "Tenaga Kependidikan (1.438 User)", ["PC Kantor / Administrasi", "eSDM, eFinansi, PLO Surat"], font_title=font_bold, font_text=font_small)
    draw_box(d2, [1290, 135, 1710, 215], "Admin TI & Keuangan (Privileged)", ["Terminal Administrasi Khusus", "Hak Akses Database & Konfigurasi"], font_title=font_bold, font_text=font_small)

    # Arrows Layer 1 -> Layer 2
    for x in [270, 670, 1070, 1500]:
        draw_arrow(d2, (x, 230), (x, 270), width=2, arrow_size=8)
    d2.text((750, 240), "Protokol HTTPS / TLS 1.3 Terenkripsi", fill="black", font=font_small_i)

    # LAYER 2: SECURITY & PERIMETER LAYER
    d2.rectangle([60, 270, 1740, 380], fill="#FFFFFF", outline="#000000", width=2)
    d2.rectangle([60, 270, 370, 305], fill="#EAEAEA", outline="#000000", width=1)
    d2.text((70, 278), "2. PERIMETER KEAMANAN & JARINGAN", fill="black", font=font_bold)

    draw_box(d2, [150, 315, 850, 370], "Web Application Firewall (WAF)", ["Inspeksi Paket, Anti-DDoS, Rate Limiting, OWASP Top-10 Rules"], font_title=font_bold, font_text=font_small)
    draw_arrow(d2, (850, 342), (950, 342), width=2, arrow_size=8)
    draw_box(d2, [950, 315, 1650, 370], "Nginx Reverse Proxy / Load Balancer", ["Terminasi TLS 1.3, SSL Offloading, Distribusi Beban Klaster Keycloak"], font_title=font_bold, font_text=font_small)

    # Arrows Layer 2 -> Layer 3
    draw_arrow(d2, (1300, 380), (1300, 420), width=2, arrow_size=8)
    draw_arrow(d2, (500, 380), (500, 420), width=2, arrow_size=8)

    # LAYER 3: CORE IDENTITY PROVIDER (KEYCLOAK CLUSTER)
    d2.rectangle([60, 420, 1740, 690], fill="#FFFFFF", outline="#000000", width=2)
    d2.rectangle([60, 420, 450, 455], fill="#EAEAEA", outline="#000000", width=1)
    d2.text((70, 428), "3. CORE IDENTITY PROVIDER: KEYCLOAK CLUSTER (REALM SSOUIN)", fill="black", font=font_bold)

    # Sub-box 3.1: Password Policy
    draw_box(d2, [90, 470, 450, 660], "Policy Engine", [
        "Password Policy Enforcer:",
        "- Min 8-12 Karakter",
        "- Simbol, Angka, Upper/Lower",
        "- Cek Blacklist Kata Sandi",
        "- Lockout 5x Gagal Login",
        "- Verify Email Terverifikasi"
    ], font_title=font_bold, font_text=font_small)

    # Arrow 3.1 -> 3.2
    draw_arrow(d2, (450, 565), (500, 565), width=2, arrow_size=8)

    # Sub-box 3.2: Required Action Pipeline
    draw_box(d2, [500, 470, 860, 660], "Required Actions Pipeline", [
        "Eksekusi Alur Wajib:",
        "1. Update Password Awal",
        "   (Hapus NIK Default)",
        "2. Verify Email Kampus",
        "3. Configure OTP Massal",
        "4. Cetak 10 Recovery Codes"
    ], font_title=font_bold, font_text=font_small)

    # Arrow 3.2 -> 3.3
    draw_arrow(d2, (860, 565), (910, 565), width=2, arrow_size=8)

    # Sub-box 3.3: MFA Engine
    draw_box(d2, [910, 470, 1340, 660], "Multi-Factor Auth Engine", [
        "A. TOTP Engine (RFC 6238):",
        "   - Bebas Lisensi / FreeOTP",
        "   - Waktu Validasi 30 Detik",
        "B. FIDO2 / WebAuthn SPI:",
        "   - Hardware USB/NFC Key",
        "   - Wajib Akun Privileged / Admin"
    ], font_title=font_bold, font_text=font_small)

    # Arrow 3.3 -> 3.4
    draw_arrow(d2, (1340, 565), (1390, 565), width=2, arrow_size=8)

    # Sub-box 3.4: Audit Log
    draw_box(d2, [1390, 470, 1710, 660], "Logging & Audit Engine", [
        "Keycloak Events Config:",
        "- Login Events Listener",
        "- Admin Audit Trail",
        "- Event Expiration Policy:",
        "  Auto-Purge 180 Hari",
        "- Kepatuhan UU PDP No. 27"
    ], font_title=font_bold, font_text=font_small)

    # Arrows Layer 3 <-> Layer 4
    draw_arrow(d2, (450, 690), (450, 740), width=2, arrow_size=8)
    draw_arrow(d2, (450, 740), (450, 690), width=2, arrow_size=8)
    draw_arrow(d2, (1350, 690), (1350, 740), width=2, arrow_size=8)
    draw_arrow(d2, (1350, 740), (1350, 690), width=2, arrow_size=8)

    # LAYER 4: DATA SOURCES & SYNC
    d2.rectangle([60, 740, 1740, 890], fill="#FFFFFF", outline="#000000", width=2)
    d2.rectangle([60, 740, 400, 775], fill="#EAEAEA", outline="#000000", width=1)
    d2.text((70, 748), "4. SUMBER DATA IDENTITAS & FEDERASI", fill="black", font=font_bold)

    draw_cylinder(d2, [150, 785, 550, 875], "eAkademik DB (PostgreSQL)", ["Pangkalan Data Mahasiswa", "Migrasi Penuh Lokal JPA"], font_title=font_bold, font_text=font_small)

    draw_box(d2, [630, 800, 1170, 865], "eSDM REST User Federation API", ["Sinkronisasi Real-Time Akun Pegawai & Dosen via 'esdm-sync-service'"], font_title=font_bold, font_text=font_small)
    draw_arrow(d2, (1170, 832), (1250, 832), width=2, arrow_size=8)

    draw_cylinder(d2, [1250, 785, 1650, 875], "eSDM Database (Oracle/Postgre)", ["Pangkalan Data Kepegawaian", "Sumber Identitas Dosen/Tendik"], font_title=font_bold, font_text=font_small)

    # Arrows Layer 3 -> Layer 5 (Token Issuance)
    draw_arrow(d2, (1125, 690), (1125, 930), width=2, arrow_size=8)
    d2.text((1135, 710), "Penerbitan Token Akses (OpenID Connect / SAML 2.0)", fill="black", font=font_small_i)

    # LAYER 5: INTEGRATED APPLICATIONS (44 CLIENTS)
    d2.rectangle([60, 930, 1740, 1150], fill="#FFFFFF", outline="#000000", width=2)
    d2.rectangle([60, 930, 460, 965], fill="#EAEAEA", outline="#000000", width=1)
    d2.text((70, 938), "5. LAPISAN APLIKASI TERINTEGRASI (44 CLIENTS TERDAFTAR)", fill="black", font=font_bold)

    draw_box(d2, [90, 980, 390, 1120], "Layanan Akademik", [
        "• eAkademik Portal",
        "• eRegistrasi Mhs",
        "• dev-lms (Moodle)",
        "• eRiset & eKKN",
        "• PLO Persuratan"
    ], font_title=font_bold, font_text=font_small)

    draw_box(d2, [430, 980, 730, 1120], "Layanan Kepegawaian", [
        "• eSDM Portal",
        "• eKinerja Pegawai",
        "• esdm-sync-service",
        "• SAML Staff Portal"
    ], font_title=font_bold, font_text=font_small)

    draw_box(d2, [770, 980, 1070, 1120], "Layanan Finansial & BMN", [
        "• eFinansi UKT",
        "• ePembayaran",
        "• eAset & BMN",
        "• eBeasiswa Portal"
    ], font_title=font_bold, font_text=font_small)

    draw_box(d2, [1110, 980, 1410, 1120], "Aplikasi Mobile & Dukungan", [
        "• mCampus & mhst",
        "• uhelp SSO Bridge",
        "• eAlumni Portal",
        "• eAdmisi Seleksi"
    ], font_title=font_bold, font_text=font_small)

    draw_box(d2, [1450, 980, 1710, 1120], "Jaringan Kampus", [
        "• Wi-Fi SSO MHS",
        "• Wi-Fi SSO STAF",
        "  (FreeRADIUS Bridge",
        "   & Captive Portal)"
    ], font_title=font_bold, font_text=font_small)

    out_fig2 = os.path.join(output_dir, "fig2_arsitektur_infrastruktur_sso_mfa.png")
    img2.save(out_fig2, "PNG", dpi=(300, 300))
    # Also save as jpg
    img2.save(os.path.join(output_dir, "fig2_arsitektur_infrastruktur_sso_mfa.jpg"), "JPEG", quality=95)
    print(f"Saved: {out_fig2}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "release", "figures")
    generate_academic_figures(out_dir)
