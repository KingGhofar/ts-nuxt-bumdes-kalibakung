# -*- coding: utf-8 -*-
"""PROPOSAL KP v4 — sesuai pedoman penulisan UMP:
Times New Roman 12, spasi dobel, margin 4/3/4/3, indentasi alinea 1.27 cm,
halaman judul + logo, persetujuan 4 pihak, isi A-E, sitasi Harvard, daftar pustaka APA.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
    HRFlowable,
)
from reportlab.lib import colors

OUT = "docs/PROPOSAL-KP-BUMDES-KALIBAKUNG-v4.pdf"

# ============ STYLE ============
def st(name, **kw):
    return ParagraphStyle(name, **kw)

S_TITLE = st("title", fontName="Times-Bold", fontSize=14, leading=20, alignment=TA_CENTER, spaceAfter=4)
S_JUDUL = st("judul", fontName="Times-Bold", fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=2)
S_BODY  = st("body", fontName="Times-Roman", fontSize=12, leading=22, alignment=TA_JUSTIFY,
             firstLineIndent=1.27*cm, spaceAfter=6)
S_HEAD  = st("head", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT)
S_SUBH  = st("subh", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT)
S_SMALL = st("small", fontName="Times-Roman", fontSize=12, leading=20, alignment=TA_CENTER, spaceAfter=2)
S_CAP   = st("cap", fontName="Times-Roman", fontSize=12, leading=16, alignment=TA_CENTER, spaceBefore=6, spaceAfter=12)
S_REF   = st("ref", fontName="Times-Roman", fontSize=12, leading=16, alignment=TA_LEFT,
             leftIndent=1.27*cm, firstLineIndent=-1.27*cm, spaceAfter=8)
S_REF_TITLE = st("reft", fontName="Times-Bold", fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=14)

def P(text, style=S_BODY):
    return Paragraph(text, style)

def judul(text):
    return Paragraph(text, S_HEAD)

story = []

# ============ HALAMAN JUDUL (Lampiran 5) ============
story += [
    Spacer(1, 10*mm),
    # Placeholder Logo UMP — ganti dengan file logo asli bila tersedia
    Paragraph("LOGO UMP", st("logo", fontName="Times-Bold", fontSize=12, alignment=TA_CENTER)),
    Spacer(1, 16*mm),
    Paragraph("PROPOSAL KERJA PRAKTIK", S_TITLE),
    Spacer(1, 10*mm),
    Paragraph("RANCANG BANGUN WEBSITE BUMDes DESA KALIBAKUNG<br/>BERBASIS WEB UNTUK TRANSPARANSI LAPORAN KEUANGAN,<br/>UNIT USAHA, DAN ASPIRASI WARGA", S_JUDUL),
    Spacer(1, 18*mm),
    Paragraph("Disusun oleh:", S_SMALL),
    Paragraph("<b>Nabilla Fitria Setyawan</b><br/><b>2303040148</b>", S_SMALL),
    Spacer(1, 18*mm),
    Paragraph("PROGRAM STUDI TEKNIK INFORMATIKA<br/>FAKULTAS TEKNIK DAN SAINS<br/>UNIVERSITAS MUHAMMADIYAH PURWOKERTO<br/>2026", S_SMALL),
    PageBreak(),
]

# ============ HALAMAN PERSETUJUAN (Lampiran 6) ============
story += [
    Paragraph("LEMBAR PERSETUJUAN<br/>PROPOSAL KERJA PRAKTIK", S_TITLE),
    Spacer(1, 8*mm),
    Paragraph("RANCANG BANGUN WEBSITE BUMDes DESA KALIBAKUNG BERBASIS WEB UNTUK TRANSPARANSI LAPORAN KEUANGAN, UNIT USAHA, DAN ASPIRASI WARGA", S_JUDUL),
    Spacer(1, 8*mm),
    Paragraph("Disusun oleh:", S_SMALL),
    Paragraph("<b>Nabilla Fitria Setyawan</b><br/><b>2303040148</b>", S_SMALL),
    Spacer(1, 10*mm),
    Paragraph("<b>Proposal Kerja Praktik ini telah disetujui dan ditandatangani oleh mahasiswa, pembimbing, mitra, dan Ketua Program Studi.</b>", S_SMALL),
    Spacer(1, 10*mm),
    Paragraph("Disetujui di : Purwokerto<br/>Tanggal : .........................................", S_SMALL),
    Spacer(1, 14*mm),
]

ttd = Table([
    ["Mahasiswa,", "Pembimbing,", "Mitra,", "Mengetahui,\nKaprodi Teknik Informatika,"],
    ["\n\n\n\n\n( Nabilla Fitria Setyawan )", "\n\n\n\n\n( ......................................... )", "\n\n\n\n\n( ......................................... )", "\n\n\n\n\n( ......................................... )"],
    ["NIM. 2303040148", "NIK. ......................", "", "NIK. ......................"],
], colWidths=[44*mm, 44*mm, 44*mm, 44*mm])
ttd.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("FONTNAME", (0,0), (-1,0), "Times-Roman"),
    ("FONTNAME", (0,1), (-1,2), "Times-Roman"),
    ("FONTSIZE", (0,0), (-1,-1), 11),
    ("LEFTPADDING", (0,0), (-1,-1), 2),
    ("RIGHTPADDING", (0,0), (-1,-1), 2),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(ttd)
story.append(PageBreak())

# ============ A. DESKRIPSI PROYEK ============
story += [
    judul("A. Deskripsi Proyek"),
    P("Perkembangan teknologi informasi yang pesat telah memberikan dampak signifikan pada berbagai sektor kehidupan, termasuk sektor pemerintahan desa dan pengelolaan Badan Usaha Milik Desa (BUMDes). Salah satu bentuk pemanfaatan teknologi yang banyak diterapkan adalah penggunaan <i>website</i> sebagai media informasi, promosi, dan transparansi publik (Muttaqin dkk., 2021). Dalam konteks ini, BUMDes Desa Kalibakung, Kecamatan Balapulang, Kabupaten Tegal, memiliki potensi besar untuk mengelola unit usaha, laporan keuangan, dan aspirasi warga secara digital."),
    P("Badan Usaha Milik Desa (BUMDes) merupakan lembaga usaha desa yang dikelola oleh masyarakat dan pemerintah desa untuk meningkatkan kesejahteraan masyarakat serta mengoptimalkan potensi ekonomi lokal (Ramadhan &amp; Prasetyo, 2025). BUMDes Desa Kalibakung memiliki beberapa unit usaha yang menjadi tulang punggung perekonomian desa, antara lain pengelolaan air bersih, pengelolaan sampah, sarana olahraga desa, dan pengembangan Desa Wisata Kalimus. Setiap unit usaha memiliki karakteristik, penanggung jawab, dan kebutuhan pencatatan yang berbeda-beda sehingga membutuhkan sistem pengelolaan yang terpusat dan terstruktur."),
    P("Saat ini pengelolaan data usaha, rekap keuangan bulanan, dan penanganan aspirasi warga masih dilakukan secara manual atau tersebar melalui aplikasi pesan singkat. Kondisi tersebut menyebabkan data sulit ditelusuri, rawan tercecer, rentan terhadap kesalahan pencatatan, serta menyulitkan masyarakat untuk memperoleh informasi laporan keuangan yang transparan dan akuntabel. Permasalahan ini sejalan dengan temuan pada penelitian sebelumnya yang menyatakan bahwa pencatatan keuangan BUMDes secara konvensional berisiko menimbulkan kesalahan, keterlambatan, dan kurangnya transparansi (Saifudin, 2024; Sari &amp; Aziz, 2021)."),
    P("Berdasarkan permasalahan tersebut, solusi yang dibutuhkan adalah merancang dan membangun sebuah <b>Website BUMDes Desa Kalibakung</b> yang menyediakan portal publik untuk warga serta dashboard admin untuk pengurus. Website ini menampilkan profil BUMDes, unit usaha, laporan keuangan yang telah dipublikasikan, dan form aspirasi warga. Di sisi admin, sistem menyediakan pengelolaan profil BUMDes, unit usaha, laporan keuangan, aspirasi, notifikasi, serta persetujuan akun pengurus baru melalui verifikasi email."),
    P("Manfaat bagi pengurus BUMDes adalah tersedianya pencatatan yang terstruktur dan transparan, kemudahan mempublikasikan laporan keuangan, serta kendali hak akses antar pengurus. Manfaat bagi warga adalah kemudahan mengakses informasi unit usaha dan laporan keuangan, serta kemudahan menyampaikan aspirasi secara online. Dengan demikian, sistem ini diharapkan mampu mendukung keterbukaan informasi publik dan mendorong partisipasi masyarakat dalam pengawasan keuangan desa (Wardana &amp; Irsyadi, 2026)."),
    Paragraph("Data mitra Kerja Praktik:", S_SUBH),
    P("Nama Mitra : BUMDes Desa Kalibakung<br/>Alamat : Jl. Raya Kalibakung-Guci RT 01 RW 03, Desa Kalibakung, Kecamatan Balapulang, Kabupaten Tegal, Jawa Tengah 52464<br/>Bidang Usaha : Pengelolaan unit usaha desa, transparansi keuangan, dan layanan masyarakat desa.", st("mitra", fontName="Times-Roman", fontSize=12, leading=22, alignment=TA_LEFT, spaceAfter=6)),
]

# ============ B. RUANG LINGKUP ============
story += [
    judul("B. Ruang Lingkup"),
    P("Bagian ini menjelaskan secara jelas mengenai lingkup kegiatan yang akan dilakukan dalam proyek, batasan-batasan yang menjadi acuan selama proses pengembangan sistem, serta spesifikasi hasil akhir yang ditargetkan."),
    Paragraph("1. Lingkup Kegiatan", S_SUBH),
    Paragraph("a. Penyusunan Proposal", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Menyusun proposal kerja praktik yang mencakup latar belakang, permasalahan, solusi dan target capaian, manfaat, serta ruang lingkup kegiatan yang akan dilakukan. Proposal ini bertujuan memberikan gambaran awal mengenai proyek yang akan dikembangkan selama masa kerja praktik."),
    Paragraph("b. Pengembangan Sistem", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Melakukan analisis kebutuhan, perancangan, serta implementasi sistem yang dibutuhkan oleh mitra, seperti profil BUMDes, unit usaha, laporan keuangan, aspirasi warga, notifikasi, dan manajemen akun pengurus. Pengembangan dilakukan dengan memperhatikan kebutuhan pengguna dan teknologi yang sesuai."),
    Paragraph("c. Evaluasi Sistem", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Setelah sistem dikembangkan, dilakukan pengujian dan evaluasi terhadap sistem yang telah dibuat. Evaluasi mencakup uji fungsionalitas, kenyamanan pengguna (user experience), dan efektivitas sistem dalam mendukung kegiatan operasional mitra."),
    Paragraph("d. Penyusunan Laporan", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Sebagai bentuk pertanggungjawaban akhir, disusun laporan lengkap mengenai seluruh proses kegiatan, hasil yang dicapai, kendala yang dihadapi, serta solusi yang diterapkan selama masa kerja praktik."),
    Paragraph("2. Batasan Proyek", S_SUBH),
    P("Untuk menjaga fokus dan ketercapaian proyek sesuai dengan waktu yang tersedia, batasan proyek ditentukan sebagai berikut:"),
    P("1) Sistem dibangun berupa website informasi dan transparansi BUMDes, bukan sistem e-commerce penuh dengan fitur pembayaran online atau pelacakan pengiriman.<br/>2) Sistem tidak mencakup aplikasi mobile khusus, namun dirancang responsif sehingga dapat diakses melalui perangkat mobile.<br/>3) Sistem menggunakan PostgreSQL sebagai basis data dan Prisma sebagai ORM.<br/>4) Pengelolaan hak akses dibedakan menjadi Super Admin dan Admin/Pengurus, dengan Super Admin memiliki hak menyetujui atau menolak akun pengurus baru.", st("list", fontName="Times-Roman", fontSize=12, leading=22, alignment=TA_JUSTIFY, spaceAfter=6)),
    Paragraph("3. Spesifikasi Hasil yang Ditargetkan", S_SUBH),
    P("1) Sebuah website portal publik yang menampilkan profil BUMDes, unit usaha, dan laporan keuangan terpublikasi.<br/>2) Form aspirasi warga yang terhubung ke dashboard admin.<br/>3) Dashboard admin untuk mengelola profil BUMDes, unit usaha, laporan keuangan, aspirasi, dan notifikasi.<br/>4) Sistem registrasi pengurus dengan verifikasi email dan persetujuan akun oleh Super Admin.", st("list", fontName="Times-Roman", fontSize=12, leading=22, alignment=TA_JUSTIFY, spaceAfter=6)),
]

# ============ C. TAHAPAN PELAKSANAAN ============
story += [
    judul("C. Tahapan Pelaksanaan"),
    P("Dalam melaksanakan Kerja Praktik pada BUMDes Desa Kalibakung, proses pengembangan sistem dilakukan dengan menggunakan metode <i>System Development Life Cycle</i> (SDLC) model Waterfall. SDLC merupakan kerangka kerja yang terstruktur dan sistematis untuk merancang, mengembangkan, dan memelihara sistem informasi (Pricillia &amp; Zulfachmi, 2021). Model Waterfall dipilih karena memiliki tahapan yang berurutan, jelas, dan terukur, mulai dari analisis kebutuhan, perancangan, implementasi, pengujian, hingga pemeliharaan (Royce, 1970; Wardana &amp; Irsyadi, 2026). Pendekatan ini dinilai cocok untuk proyek berskala menengah dengan kebutuhan yang sudah teridentifikasi secara jelas, seperti pada sistem informasi BUMDes. Tahapan pelaksanaan ditunjukkan pada Gambar 1."),
    Image("docs/diagrams/waterfall.png", width=165*mm, height=165*mm*0.3),
    Paragraph("Gambar 1. Tahapan Pelaksanaan", S_CAP),
    Paragraph("1. Perencanaan", S_SUBH),
    P("Tahap perencanaan merupakan tahap awal yang sangat krusial karena menjadi fondasi keseluruhan proses pengembangan sistem. Pada tahap ini dilakukan identifikasi terhadap kebutuhan awal sistem, ruang lingkup proyek, tujuan utama pengembangan, dan sumber daya yang diperlukan. Pengumpulan data dilakukan melalui observasi langsung terhadap kondisi BUMDes Desa Kalibakung, wawancara dengan pengurus, serta studi pustaka."),
    Paragraph("2. Analisis Kebutuhan", S_SUBH),
    Paragraph("a. Kebutuhan Data", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("1) Data profil BUMDes: nama, alamat, kontak, visi, misi, struktur pengurus, dan jam operasional.<br/>2) Data unit usaha: nama, kategori, penanggung jawab, kontak, deskripsi, foto, dan status aktif.<br/>3) Data laporan keuangan: bulan, tahun, total pemasukan, total pengeluaran, keterangan, file LPJ, dan status publikasi.<br/>4) Data aspirasi: nama pengirim, kategori, dusun, pesan, status tindak lanjut, dan status publikasi.<br/>5) Data pengguna: nama, email, password, role, status verifikasi email, dan status persetujuan akun.", st("list", fontName="Times-Roman", fontSize=12, leading=22, alignment=TA_JUSTIFY, spaceAfter=6)),
    Paragraph("b. Kebutuhan Aturan", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Pengunjung dapat melihat profil, unit usaha, laporan terpublikasi, dan mengirim aspirasi tanpa login. Calon pengurus dapat mendaftar menggunakan email, kemudian harus memverifikasi email melalui link yang dikirim sistem. Akun yang sudah terverifikasi harus disetujui oleh Super Admin sebelum dapat login. Admin dapat mengelola profil BUMDes, unit usaha, laporan keuangan, aspirasi, dan notifikasi. Laporan keuangan hanya tampil di portal publik apabila statusnya sudah dipublikasikan."),
    Paragraph("3. Perancangan", S_SUBH),
    Paragraph("a. Use Case Diagram", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Use Case Diagram menggambarkan interaksi antara aktor dan sistem. Aktor dalam sistem ini adalah Pengunjung/Warga, Calon Pengurus, Admin, Super Admin, dan Sistem Email. Super Admin mewarisi seluruh hak akses Admin serta memiliki hak tambahan untuk menyetujui atau menolak akun pengurus. Use Case Diagram ditunjukkan pada Gambar 2."),
    Image("docs/diagrams/use-case-final.png", width=165*mm, height=165*mm*0.65),
    Paragraph("Gambar 2. Use Case Diagram", S_CAP),
    Paragraph("b. Entity Relationship Diagram (ERD)", st("subh2", fontName="Times-Bold", fontSize=12, leading=20, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT)),
    P("Entity Relationship Diagram (ERD) digunakan sebagai alat bantu perancangan struktur basis data. ERD memetakan relasi antar tabel users, bumdes, pengurus, unit_usaha, laporan_keuangan, aspirasi, dan notifikasi. ERD ditunjukkan pada Gambar 3."),
    Image("docs/diagrams/erd-final.png", width=165*mm, height=165*mm*0.70),
    Paragraph("Gambar 3. Entity Relationship Diagram (ERD)", S_CAP),
    Paragraph("4. Implementasi", S_SUBH),
    P("Tahap implementasi mengubah desain menjadi kode program. Sistem dibangun menggunakan Nuxt 4 (Vue 3) untuk frontend dan backend, Tailwind CSS untuk antarmuka, Prisma ORM untuk akses data, serta PostgreSQL sebagai basis data. Autentikasi menggunakan JWT yang disimpan pada cookie httpOnly. Pengiriman email verifikasi menggunakan Nodemailer dengan SMTP Gmail."),
    Paragraph("5. Pengujian", S_SUBH),
    P("Metode pengujian yang digunakan adalah Black Box Testing dan pengujian responsivitas. Black Box Testing dilakukan untuk mengevaluasi apakah setiap fitur utama dalam website dapat berjalan sesuai spesifikasi tanpa melihat kode program secara langsung (Saifudin, 2024; Zahra dkk., 2024). Sedangkan pengujian responsivitas dilakukan untuk memastikan tampilan website dapat beradaptasi secara optimal pada berbagai ukuran layar, mulai dari desktop hingga smartphone."),
    Paragraph("6. Evaluasi dan Pemeliharaan", S_SUBH),
    P("Tahap terakhir dilakukan untuk menjamin stabilitas, keamanan transaksi data, dan fungsionalitas sistem setelah beroperasi."),
]

# ============ D. JADWAL PELAKSANAAN ============
story += [
    judul("D. Jadwal Pelaksanaan"),
    P("Jadwal pelaksanaan proyek disajikan dalam bentuk tabel. Jadwal pelaksanaan ditunjukkan pada Tabel 1."),
]

def buat_jadwal():
    # Kolom: No | Kegiatan | M1..M4 | M5..M8 | M9..M12
    header = ["No", "Kegiatan", "Bulan 1", "", "", "", "Bulan 2", "", "", "", "Bulan 3", "", "", ""]
    minggu = ["", "", "1", "2", "3", "4", "1", "2", "3", "4", "1", "2", "3", "4"]
    rows = [
        ["1", "Perencanaan", "■", "■", "", "", "", "", "", "", "", "", "", ""],
        ["2", "Analisis Kebutuhan", "", "", "■", "■", "", "", "", "", "", "", "", ""],
        ["3", "Perancangan", "", "", "", "", "■", "■", "", "", "", "", "", ""],
        ["4", "Implementasi", "", "", "", "", "", "■", "■", "■", "", "", "", ""],
        ["5", "Pengujian", "", "", "", "", "", "", "", "■", "■", "", "", ""],
        ["6", "Evaluasi & Pemeliharaan", "", "", "", "", "", "", "", "", "", "■", "■", ""],
    ]
    return [header, minggu] + rows

t = Table(buat_jadwal())
# Style: hanya 3 garis horizontal (di bawah judul kolom & penutup), tanpa garis vertikal.
t.setStyle(TableStyle([
    ("SPAN", (2,0), (5,0)),
    ("SPAN", (6,0), (9,0)),
    ("SPAN", (10,0), (13,0)),
    ("SPAN", (0,0), (0,1)),
    ("SPAN", (1,0), (1,1)),
    ("FONTNAME", (0,0), (-1,-1), "Times-Roman"),
    ("FONTNAME", (0,0), (-1,0), "Times-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN", (1,1), (1,-1), "LEFT"),
    ("LINEABOVE", (0,0), (-1,0), 1, colors.black),
    ("LINEABOVE", (0,1), (-1,1), 1, colors.black),
    ("LINEBELOW", (0,-1), (-1,-1), 1, colors.black),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story += [
    Paragraph("Tabel 1. Jadwal Pelaksanaan", S_CAP),
]

# ============ E. BIAYA ============
story += [
    judul("E. Biaya (jika diperlukan)"),
    P("Rincian biaya pelaksanaan Kerja Praktik ditunjukkan pada Tabel 2."),
]

biaya = [
    ["No", "Uraian", "Jumlah"],
    ["1", "Domain dan hosting (1 tahun)", "Rp 500.000"],
    ["2", "Lisensi/operasional email SMTP", "Rp 100.000"],
    ["3", "Dokumentasi dan cetak laporan", "Rp 200.000"],
    ["4", "Transportasi dan komunikasi", "Rp 200.000"],
    ["", "Total", "Rp 1.000.000"],
]
t2 = Table(biaya, colWidths=[15*mm, 110*mm, 50*mm])
t2.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Times-Roman"),
    ("FONTNAME", (0,0), (-1,0), "Times-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 11),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
    ("ALIGN", (2,0), (2,-1), "RIGHT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LINEABOVE", (0,0), (-1,0), 1, colors.black),
    ("LINEABOVE", (0,1), (-1,1), 1, colors.black),
    ("LINEBELOW", (0,-1), (-1,-1), 1, colors.black),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("SPAN", (0,4), (1,4)),
]))
story.append(t2)
story += [
    Paragraph("Tabel 2. Rincian Biaya Pelaksanaan", S_CAP),
]

# ============ DAFTAR PUSTAKA ============
story += [
    Paragraph("DAFTAR PUSTAKA", S_REF_TITLE),
    Paragraph("Muttaqin, R., dkk. (2021). <i>E-Commerce: Implementasi, Strategi dan Inovasinya</i>. Medan: Yayasan Kita Menulis.", S_REF),
    Paragraph("Pricillia, T., &amp; Zulfachmi. (2021). Perbandingan Metode Pengembangan Perangkat Lunak (Waterfall, Prototype, RAD). <i>Jurnal Bangkit Indonesia</i>, 10(1), 6–12. https://doi.org/10.52771/bangkitindonesia.v10i1.153", S_REF),
    Paragraph("Ramadhan, M., &amp; Prasetyo, D. (2025). Rancang Bangun Sistem Informasi Berbasis Website untuk BUMDes sebagai Sarana Informasi bagi Masyarakat. <i>TRI DHARMA MANDIRI: Diseminasi dan Hilirisasi Riset kepada Masyarakat</i>.", S_REF),
    Paragraph("Royce, W. W. (1970). Managing the Development of Large Software Systems. <i>Proceedings of IEEE WESCON</i>, 1–9.", S_REF),
    Paragraph("Saifudin. (2024). Penerapan Metode Waterfall Sisfo Buku Kas Digital pada BUMDes Jaya Usaha. <i>Jurnal Sistem Informasi Akuntansi (JUSTIAN)</i>.", S_REF),
    Paragraph("Sari, E. R., &amp; Aziz, M. A. (2021). Rancang Bangun Sistem Informasi BUMDes Giri Bangun Berbasis Website Menggunakan Metode Waterfall. <i>JURISTIK (Jurnal Riset Teknologi Informasi dan Komputer)</i>, 1(01), 16–26. https://doi.org/10.53863/juristik.v1i01.230", S_REF),
    Paragraph("Sukamto, R. A., &amp; Shalahuddin, M. (2016). <i>Rekayasa Perangkat Lunak Terstruktur dan Berorientasi Objek</i>. Bandung: Informatika.", S_REF),
    Paragraph("Wardana, A. P., &amp; Irsyadi, F. Y. A. (2026). Pengembangan Portal Web untuk Pengelolaan Informasi Publik Badan Usaha Milik Desa (BUMDes) Wonorejo. <i>Jurnal Media Computer Science</i>, 5(1).", S_REF),
    Paragraph("Zahra, A., Riani, L., Kurniawan, F., Darmansah, F. Z., Valenza, I. L., Wicaksono, A., &amp; Nasir, M. (2024). Pengujian Black Box pada Website Jasa Angkutan dan Ekspedisi Menggunakan Teknik Boundary Value Analysis. <i>Media Jurnal Informatika</i>, 16(2), 133–139. https://doi.org/10.35194/mji.v16i2.4798", S_REF),
]

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=4*cm, rightMargin=3*cm,
    topMargin=4*cm, bottomMargin=3*cm,
    title="Proposal KP BUMDes Kalibakung",
)
doc.build(story)
print("saved", OUT)
