# -*- coding: utf-8 -*-
"""Generate PROPOSAL KERJA PRAKTIK BUMDes Kalibakung (PDF) - format mirip contoh PDF Fira."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
)
from reportlab.lib import colors

OUT = "docs/PROPOSAL-KP-BUMDES-KALIBAKUNG-v3.pdf"

styles = getSampleStyleSheet()

def st(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

S_TITLE = st("title", fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=6)
S_SUB   = st("sub", fontName="Times-Bold", fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=4)
S_BODY  = st("body", fontName="Times-Roman", fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
S_HEAD  = st("head", fontName="Times-Bold", fontSize=12, leading=15, spaceBefore=10, spaceAfter=6)
S_SUBH  = st("subh", fontName="Times-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
S_SMALL = st("small", fontName="Times-Roman", fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=2)
S_CAP   = st("cap", fontName="Times-Italic", fontSize=10, leading=13, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)

def P(text, style=S_BODY):
    return Paragraph(text, style)

story = []

# ===== HALAMAN JUDUL =====
story += [
    Paragraph("PROPOSAL KERJA PRAKTIK", S_TITLE),
    Spacer(1, 10*mm),
    Paragraph("Rancang Bangun Website BUMDes Desa Kalibakung<br/>Berbasis Web untuk Transparansi Laporan Keuangan,<br/>Unit Usaha, dan Aspirasi Warga", S_SUB),
    Spacer(1, 12*mm),
    Paragraph("Disusun sebagai Salah Satu Syarat<br/>Kelengkapan Kurikulum pada Prodi Teknik Informatika<br/>Fakultas Teknik dan Sains<br/>Universitas Muhammadiyah Purwokerto", styles["Normal"] if False else S_SMALL),
    Spacer(1, 14*mm),
    Paragraph("Disusun oleh:<br/><b>Nama : Nabilla Fitria Setyawan</b><br/><b>NIM : 2303040148</b>", S_SMALL),
    Spacer(1, 20*mm),
    Paragraph("PROGRAM STUDI TEKNIK INFORMATIKA<br/>FAKULTAS TEKNIK DAN SAINS<br/>UNIVERSITAS MUHAMMADIYAH PURWOKERTO<br/>2026", S_SMALL),
    PageBreak(),
]

# ===== LEMBAR PERSETUJUAN =====
story += [
    Paragraph("LEMBAR PERSETUJUAN<br/>PROPOSAL KERJA PRAKTIK", S_TITLE),
    Spacer(1, 6*mm),
    Paragraph("Rancang Bangun Website BUMDes Desa Kalibakung Berbasis Web untuk Transparansi Laporan Keuangan, Unit Usaha, dan Aspirasi Warga", S_SUB),
    Spacer(1, 8*mm),
    Paragraph("Disusun oleh:<br/><b>Nama : Nabilla Fitria Setyawan</b><br/><b>NIM : 2303040148</b>", S_SMALL),
    Spacer(1, 8*mm),
    Paragraph("<b>Proposal Kerja Praktik Mahasiswa tersebut di Atas Dinyatakan Telah Memenuhi Syarat untuk Dilaksanakan</b>", S_SMALL),
    Spacer(1, 8*mm),
    Paragraph("<b>Disetujui : di Purwokerto</b><br/><b>Tanggal :</b>", S_SMALL),
    Spacer(1, 12*mm),
    Table([
        ["Mitra,", "Pembimbing Kerja Praktik,", "Mengetahui,\nKaprodi Teknik Informatika"],
        ["\n\n\n\n\n(______________)", "\n\n\n\n\n(Feri Wibowo, S.Kom., M.Cs.)", "\n\n\n\n\n(Agung Purwo Wicaksono, S.T., M.Kom.)"],
        ["Owner BUMDes", "NIK. 2160523", "NIK. 2160518"],
    ], colWidths=[55*mm, 55*mm, 55*mm]).setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,0), "Times-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Times-Roman"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ])),
    Spacer(1, 6*mm),
    Paragraph("(Tanda tangan dan nama dapat disesuaikan setelah mitra serta dosen pembimbing ditentukan.)", S_SMALL),
    PageBreak(),
]

# ===== DAFTAR GAMBAR & TABEL =====
story += [
    Paragraph("DAFTAR GAMBAR", S_HEAD),
    P("Gambar 1. Tahapan Pelaksanaan", S_BODY),
    P("Gambar 2. Use Case Diagram", S_BODY),
    P("Gambar 3. ERD (Entity Relationship Diagram)", S_BODY),
    Spacer(1, 6*mm),
    Paragraph("DAFTAR TABEL", S_HEAD),
    P("Tabel 1. Jadwal Pelaksanaan", S_BODY),
    PageBreak(),
]

# ===== A. DESKRIPSI PROYEK =====
story += [
    Paragraph("A. Deskripsi Proyek", S_HEAD),
    P("Perkembangan teknologi informasi yang pesat telah memberikan dampak signifikan pada berbagai sektor kehidupan, termasuk sektor pemerintahan desa dan pengelolaan Badan Usaha Milik Desa (BUMDes). Salah satu bentuk pemanfaatan teknologi yang banyak diterapkan adalah penggunaan <i>website</i> sebagai media informasi, promosi, dan transparansi publik (Muttaqin et al., 2021). Dalam konteks ini, BUMDes Desa Kalibakung, Kecamatan Balapulang, Kabupaten Tegal, memiliki potensi besar untuk mengelola unit usaha, laporan keuangan, dan aspirasi warga secara digital."),
    P("Badan Usaha Milik Desa (BUMDes) merupakan lembaga usaha desa yang dikelola oleh masyarakat dan pemerintah desa untuk meningkatkan kesejahteraan masyarakat serta mengoptimalkan potensi ekonomi lokal (Ramadhan &amp; Prasetyo, 2025). BUMDes Desa Kalibakung memiliki beberapa unit usaha yang menjadi tulang punggung perekonomian desa, antara lain pengelolaan air bersih, pengelolaan sampah, sarana olahraga desa, dan pengembangan Desa Wisata Kalimus. Setiap unit usaha memiliki karakteristik, penanggung jawab, dan kebutuhan pencatatan yang berbeda-beda sehingga membutuhkan sistem pengelolaan yang terpusat dan terstruktur."),
    P("Saat ini pengelolaan data usaha, rekap keuangan bulanan, dan penanganan aspirasi warga masih dilakukan secara manual atau tersebar melalui aplikasi pesan singkat. Kondisi tersebut menyebabkan data sulit ditelusuri, rawan tercecer, rentan terhadap kesalahan pencatatan, serta menyulitkan masyarakat untuk memperoleh informasi laporan keuangan yang transparan dan akuntabel. Permasalahan ini sejalan dengan temuan pada penelitian sebelumnya yang menyatakan bahwa pencatatan keuangan BUMDes secara konvensional berisiko menimbulkan kesalahan, keterlambatan, dan kurangnya transparansi (Saifudin, 2024; Sari &amp; Aziz, 2021)."),
    P("Berdasarkan permasalahan tersebut, solusi yang dibutuhkan adalah merancang dan membangun sebuah <b>Website BUMDes Desa Kalibakung</b> yang menyediakan portal publik untuk warga serta dashboard admin untuk pengurus. Website ini menampilkan profil BUMDes, unit usaha, laporan keuangan yang telah dipublikasikan, dan form aspirasi warga. Di sisi admin, sistem menyediakan pengelolaan profil BUMDes, unit usaha, laporan keuangan, aspirasi, notifikasi, serta persetujuan akun pengurus baru melalui verifikasi email."),
    P("Manfaat bagi pengurus BUMDes adalah tersedianya pencatatan yang terstruktur dan transparan, kemudahan mempublikasikan laporan keuangan, serta kendali hak akses antar pengurus. Manfaat bagi warga adalah kemudahan mengakses informasi unit usaha dan laporan keuangan, serta kemudahan menyampaikan aspirasi secara online. Dengan demikian, sistem ini diharapkan mampu mendukung keterbukaan informasi publik dan mendorong partisipasi masyarakat dalam pengawasan keuangan desa (Wardana &amp; Irsyadi, 2026)."),
]

# ===== B. RUANG LINGKUP =====
story += [
    Paragraph("B. Ruang Lingkup", S_HEAD),
    P("Bagian ini menjelaskan lingkup kegiatan, batasan proyek, dan spesifikasi hasil yang ditargetkan."),
    Paragraph("1. Lingkup Kegiatan", S_SUBH),
    Paragraph("a. Penyusunan Proposal", S_SUBH),
    P("Menyusun proposal kerja praktik yang mencakup latar belakang, permasalahan, solusi dan target capaian, manfaat, serta ruang lingkup kegiatan."),
    Paragraph("b. Pengembangan Sistem", S_SUBH),
    P("Melakukan analisis kebutuhan, perancangan, serta implementasi sistem sesuai kebutuhan mitra: profil BUMDes, unit usaha, laporan keuangan, aspirasi warga, notifikasi, dan manajemen akun pengurus."),
    Paragraph("c. Evaluasi Sistem", S_SUBH),
    P("Melakukan pengujian fungsionalitas, pengalaman pengguna, dan responsivitas tampilan terhadap sistem yang telah dibangun."),
    Paragraph("d. Penyusunan Laporan", S_SUBH),
    P("Menyusun laporan lengkap mengenai seluruh proses kegiatan, hasil yang dicapai, kendala, dan solusi selama kerja praktik."),
    Paragraph("2. Batasan Proyek", S_SUBH),
    P("Untuk menjaga fokus dan ketercapaian proyek, batasan proyek ditentukan sebagai berikut:"),
    P("• Sistem dibangun sebagai website informasi dan transparansi BUMDes, bukan e-commerce penuh dengan pembayaran online.<br/>• Sistem tidak mencakup aplikasi mobile khusus, tetapi dirancang responsif agar nyaman diakses melalui perangkat mobile.<br/>• Sistem menggunakan PostgreSQL sebagai basis data dan Prisma sebagai ORM.<br/>• Pengelolaan hak akses dibedakan menjadi Super Admin dan Admin/Pengurus."),
    Paragraph("3. Spesifikasi Hasil yang Ditargetkan", S_SUBH),
    P("• Website portal publik yang menampilkan profil BUMDes, unit usaha, dan laporan keuangan terpublikasi.<br/>• Form aspirasi warga yang terhubung ke dashboard admin.<br/>• Dashboard admin untuk mengelola profil, unit usaha, laporan, aspirasi, dan notifikasi.<br/>• Sistem registrasi pengurus dengan verifikasi email dan persetujuan akun oleh Super Admin."),
]

# ===== C. TAHAPAN PELAKSANAAN =====
story += [
    Paragraph("C. Tahapan Pelaksanaan", S_HEAD),
    P("Dalam melaksanakan Kerja Praktik pada BUMDes Desa Kalibakung, proses pengembangan sistem dilakukan dengan menggunakan metode <i>System Development Life Cycle</i> (SDLC) model Waterfall. SDLC merupakan kerangka kerja yang terstruktur dan sistematis untuk merancang, mengembangkan, dan memelihara sistem informasi (Pricillia &amp; Zulfachmi, 2021). Model Waterfall dipilih karena memiliki tahapan yang berurutan, jelas, dan terukur, mulai dari analisis kebutuhan, perancangan, implementasi, pengujian, hingga pemeliharaan (Royce, 1970; Wardana &amp; Irsyadi, 2026). Pendekatan ini dinilai cocok untuk proyek berskala menengah dengan kebutuhan yang sudah teridentifikasi secara jelas, seperti pada sistem informasi BUMDes. Tahapan pelaksanaan ditunjukkan pada Gambar 1."),
    Image("docs/diagrams/waterfall.png", width=170*mm, height=170*mm*0.3),
    Paragraph("Gambar 1. Tahapan Pelaksanaan", S_CAP),
    P("Tahapan model waterfall meliputi: (1) perencanaan, (2) analisis, (3) perancangan, (4) implementasi, (5) pengujian, dan (6) evaluasi/pemeliharaan."),
    Paragraph("1. Perencanaan", S_SUBH),
    P("Tahap perencanaan merupakan tahap awal yang sangat krusial karena menjadi fondasi keseluruhan proses pengembangan sistem. Pada tahap ini dilakukan observasi langsung terhadap kondisi BUMDes Desa Kalibakung, wawancara dengan pengurus, serta studi pustaka untuk mengidentifikasi kebutuhan awal sistem, ruang lingkup proyek, tujuan pengembangan, dan sumber daya yang diperlukan."),
    Paragraph("2. Analisis Kebutuhan", S_SUBH),
    Paragraph("a. Kebutuhan Data", S_SUBH),
    P("• Data profil BUMDes: nama, alamat, kontak, visi, misi, struktur pengurus, dan jam operasional.<br/>• Data unit usaha: nama, kategori, penanggung jawab, kontak, deskripsi, foto, dan status aktif.<br/>• Data laporan keuangan: bulan, tahun, total pemasukan, total pengeluaran, keterangan, file LPJ, dan status publikasi.<br/>• Data aspirasi: nama pengirim, kategori, dusun, pesan, status tindak lanjut, dan status publikasi.<br/>• Data pengguna: nama, email, password, role, status verifikasi email, dan status persetujuan akun."),
    Paragraph("b. Kebutuhan Aturan", S_SUBH),
    P("Pengunjung dapat melihat profil, unit usaha, laporan terpublikasi, dan mengirim aspirasi tanpa login. Calon pengurus dapat mendaftar menggunakan email, kemudian harus memverifikasi email melalui link yang dikirim sistem. Akun yang sudah terverifikasi harus disetujui oleh Super Admin sebelum dapat login. Admin dapat mengelola profil BUMDes, unit usaha, laporan keuangan, aspirasi, dan notifikasi. Laporan keuangan hanya tampil di portal publik apabila statusnya sudah dipublikasikan."),
    Paragraph("3. Perancangan", S_SUBH),
    Paragraph("a. Use Case Diagram", S_SUBH),
    P("Use Case Diagram menggambarkan interaksi antara aktor dan sistem. Aktor dalam sistem ini adalah Pengunjung/Warga, Calon Pengurus, Admin, Super Admin, dan Sistem Email. Super Admin mewarisi seluruh hak akses Admin serta memiliki hak tambahan untuk menyetujui atau menolak akun pengurus. Use Case Diagram ditunjukkan pada Gambar 2."),
    Image("docs/diagrams/use-case-final.png", width=170*mm, height=170*mm*0.65),
    Paragraph("Gambar 2. Use Case Diagram", S_CAP),
    Paragraph("b. Entity Relationship Diagram (ERD)", S_SUBH),
    P("Entity Relationship Diagram (ERD) digunakan sebagai alat bantu perancangan struktur basis data. ERD memetakan relasi antar tabel users, bumdes, pengurus, unit_usaha, laporan_keuangan, aspirasi, dan notifikasi. ERD ditunjukkan pada Gambar 3."),
    Image("docs/diagrams/erd-final.png", width=170*mm, height=170*mm*0.70),
    Paragraph("Gambar 3. ERD (Entity Relationship Diagram)", S_CAP),
    Paragraph("4. Implementasi", S_SUBH),
    P("Tahap implementasi mengubah desain menjadi kode program. Sistem dibangun menggunakan Nuxt 4 (Vue 3) untuk frontend dan backend, Tailwind CSS untuk antarmuka, Prisma ORM untuk akses data, serta PostgreSQL sebagai basis data. Autentikasi menggunakan JWT yang disimpan pada cookie httpOnly. Pengiriman email verifikasi menggunakan Nodemailer dengan SMTP Gmail."),
    Paragraph("5. Pengujian", S_SUBH),
    P("Metode pengujian yang digunakan adalah Black Box Testing dan pengujian responsivitas. Black Box Testing dilakukan untuk memastikan setiap fitur berjalan sesuai spesifikasi tanpa membedah kode internal (Saifudin, 2024; Zahra et al., 2024), sedangkan pengujian responsivitas dilakukan untuk memastikan tampilan nyaman diakses dari desktop hingga smartphone."),
    Paragraph("6. Evaluasi dan Pemeliharaan", S_SUBH),
    P("Tahap terakhir dilakukan untuk menjamin stabilitas, keamanan transaksi data, dan fungsionalitas sistem setelah beroperasi."),
]

# ===== D. JADWAL PELAKSANAAN =====
story += [
    Paragraph("D. Jadwal Pelaksanaan", S_HEAD),
    P("Jadwal pelaksanaan proyek ditunjukkan pada Tabel 1."),
]

def make_jadwal():
    # 3 bulan x 4 minggu
    header = ["No", "Uraian Kegiatan", "Bulan 1", "", "", "", "Bulan 2", "", "", "", "Bulan 3", "", "", ""]
    minggu = ["", "", "1","2","3","4","1","2","3","4","1","2","3","4"]
    rows = [
        ["1", "Perencanaan", "X","X","","","","","","","","","",""],
        ["2", "Analisis", "", "", "X","X","","","","","","","",""],
        ["3", "Perancangan", "", "", "", "", "X","X","","","","","",""],
        ["4", "Implementasi", "", "", "", "", "", "X","X","X","","","",""],
        ["5", "Pengujian", "", "", "", "", "", "", "", "X","X","","",""],
        ["6", "Evaluasi & Pemeliharaan", "", "", "", "", "", "", "", "", "", "X","X",""],
    ]
    return [header, minggu] + rows

t = Table(make_jadwal())
t.setStyle(TableStyle([
    ("SPAN", (2,0), (5,0)),
    ("SPAN", (6,0), (9,0)),
    ("SPAN", (10,0), (13,0)),
    ("SPAN", (0,0), (0,1)),
    ("SPAN", (1,0), (1,1)),
    ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ("FONTNAME", (0,0), (-1,0), "Times-Bold"),
    ("FONTNAME", (0,1), (-1,1), "Times-Roman"),
    ("FONTNAME", (0,0), (-1,-1), "Times-Roman"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story += [
    Spacer(1, 4*mm),
    Paragraph("Tabel 1. Jadwal Pelaksanaan", S_CAP),
    Spacer(1, 8*mm),
    P("<b>Daftar Pustaka</b>", S_HEAD),
    P("Muttaqin, R., dkk. (2021). <i>E-Commerce: Implementasi, Strategi dan Inovasinya</i>. Medan: Yayasan Kita Menulis."),
    P("Pricillia, T., &amp; Zulfachmi. (2021). Perbandingan Metode Pengembangan Perangkat Lunak (Waterfall, Prototype, RAD). <i>Jurnal Bangkit Indonesia</i>, 10(1), 6–12. https://doi.org/10.52771/bangkitindonesia.v10i1.153"),
    P("Ramadhan, M., &amp; Prasetyo, D. (2025). Rancang Bangun Sistem Informasi Berbasis Website untuk BUMDes sebagai Sarana Informasi bagi Masyarakat. <i>TRI DHARMA MANDIRI: Diseminasi dan Hilirisasi Riset kepada Masyarakat</i>."),
    P("Royce, W. W. (1970). Managing the Development of Large Software Systems. <i>Proceedings of IEEE WESCON</i>, 1–9."),
    P("Saifudin. (2024). Penerapan Metode Waterfall Sisfo Buku Kas Digital pada BUMDes Jaya Usaha. <i>Jurnal Sistem Informasi Akuntansi (JUSTIAN)</i>."),
    P("Sari, E. R., &amp; Aziz, M. A. (2021). Rancang Bangun Sistem Informasi BUMDes Giri Bangun Berbasis Website Menggunakan Metode Waterfall. <i>JURISTIK (Jurnal Riset Teknologi Informasi dan Komputer)</i>, 1(01), 16–26. https://doi.org/10.53863/juristik.v1i01.230"),
    P("Sukamto, R. A., &amp; Shalahuddin, M. (2016). <i>Rekayasa Perangkat Lunak Terstruktur dan Berorientasi Objek</i>. Bandung: Informatika."),
    P("Wardana, A. P., &amp; Irsyadi, F. Y. A. (2026). Pengembangan Portal Web untuk Pengelolaan Informasi Publik Badan Usaha Milik Desa (BUMDes) Wonorejo. <i>Jurnal Media Computer Science</i>, 5(1)."),
    P("Zahra, A., Riani, L., Kurniawan, F., Darmansah, F. Z., Valenza, I. L., Wicaksono, A., &amp; Nasir, M. (2024). Pengujian Black Box pada Website Jasa Angkutan dan Ekspedisi Menggunakan Teknik Boundary Value Analysis. <i>Media Jurnal Informatika</i>, 16(2), 133–139. https://doi.org/10.35194/mji.v16i2.4798"),
]

doc = SimpleDocTemplate(OUT, pagesize=A4,
                       leftMargin=20*mm, rightMargin=20*mm,
                       topMargin=18*mm, bottomMargin=18*mm,
                       title="Proposal KP BUMDes Kalibakung")
doc.build(story)
print("saved", OUT)
