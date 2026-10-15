# -*- coding: utf-8 -*-
"""Render Use Case & ERD langsung dengan ReportLab (tanpa browser/service online)."""
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Ellipse
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPM

BLUE = HexColor("#2563EB")
BLUE_DARK = HexColor("#1D4ED8")
INK = HexColor("#0F172A")
GRAY = HexColor("#64748B")
LINE_GRAY = HexColor("#94A3B8")
WHITE = HexColor("#FFFFFF")
BOX_FILL = HexColor("#EFF6FF")
BOX_BORDER = HexColor("#BFDBFE")

# ================= USE CASE =================
W, H = 820, 560
d = Drawing(W, H)

def kotak_aktor(x, y, w, h, label):
    d.add(Rect(x, y, w, h, rx=10, ry=10, fillColor=INK, strokeColor=None))
    d.add(String(x + w/2, y + h/2 - 4, label, fontName="Times-Bold", fontSize=9,
                 fillColor=WHITE, textAnchor="middle"))

def oval(x, y, w, h, label):
    d.add(Ellipse(x, y, w, h, fillColor=BOX_FILL, strokeColor=BOX_BORDER, strokeWidth=1))
    # label center (sederhana: satu baris)
    d.add(String(x + w/2, y + h/2 - 4, label, fontName="Times-Roman", fontSize=8,
                 fillColor=INK, textAnchor="middle"))

def garis(x1, y1, x2, y2, dashed=False):
    if dashed:
        d.add(Line(x1, y1, x2, y2, strokeColor=LINE_GRAY, strokeWidth=1, strokeDashArray=[3,3]))
    else:
        d.add(Line(x1, y1, x2, y2, strokeColor=LINE_GRAY, strokeWidth=1))

# Aktor (kiri)
aktor = [("Pengunjung / Warga", 60), ("Calon Pengurus", 200), ("Sistem Email", 340)]
for i, (nama, y) in enumerate(aktor):
    kotak_aktor(20, y, 130, 34, nama)

# Use case (kanan)
uc = [
    ("Melihat Beranda & Profil BUMDes", 520), ("Melihat Unit Usaha", 490),
    ("Melihat Laporan Keuangan Publik", 460), ("Mengirim Aspirasi Warga", 430),
    ("Mendaftar Akun (Register)", 370), ("Verifikasi Email", 340),
]
for i, (nama, y) in enumerate(uc):
    oval(300, y-14, 200, 28, nama)
    # garis dari aktor ke use case (perkiraan)

# Admin & Super Admin (kanan bawah)
kotak_aktor(480, 200, 130, 34, "Pengurus / Admin")
kotak_aktor(640, 200, 130, 34, "Super Admin")

uc_admin = [
    ("Login", 150), ("Kelola Profil BUMDes", 120), ("Kelola Unit Usaha", 90),
    ("Kelola Laporan Keuangan", 60), ("Kelola Aspirasi", 30),
    ("Kelola Notifikasi", 0), ("Kelola Pengaturan", -30),
]
for i, (nama, y) in enumerate(uc_admin):
    oval(430, y-12, 180, 24, nama)

oval(660, 240, 150, 24, "Setujui/Tolak Akun")

# Garis penghubung sederhana
garis(150, 540, 300, 520)   # pengunjung -> lihat beranda
garis(150, 220, 300, 370)   # calon pengurus -> daftar
garis(150, 360, 300, 340, dashed=True)  # sistem email -> verifikasi
garis(610, 200, 560, 140)   # admin -> login
garis(770, 200, 810, 252)   # super admin -> setujui

renderPM.drawToFile(d, "docs/diagrams/use-case-final.png", fmt="PNG", dpi=120)
print("use-case OK")

# ================= ERD =================
W, H = 900, 650
d2 = Drawing(W, H)

def entitas(x, y, w, nama, attrs):
    d2.add(Rect(x, y, w, 24, rx=4, ry=4, fillColor=BLUE, strokeColor=None))
    d2.add(String(x + w/2, y + 6, nama, fontName="Times-Bold", fontSize=10,
                 fillColor=WHITE, textAnchor="middle"))
    yy = y - 14
    for a in attrs:
        d2.add(String(x + 6, yy, a, fontName="Times-Roman", fontSize=7,
                     fillColor=INK))
        yy -= 10

entitas(20, 560, 170, "USERS", ["id PK", "nama", "email UK", "password", "jabatan", "telepon", "nik", "unit_kerja", "avatar", "role", "email_verified", "approved", "verify_token_hash", "verify_token_expires", "created_at"])
entitas(230, 560, 170, "BUMDES", ["id PK", "nama", "tahun_berdiri", "dasar_hukum", "email", "telepon", "alamat", "deskripsi", "visi", "misi", "logo", "jam_operasional"])
entitas(440, 560, 170, "PENGURUS", ["id PK", "bumdes_id FK", "nama", "jabatan", "keterangan", "foto", "urutan"])
entitas(650, 560, 170, "UNIT_USAHA", ["id PK", "bumdes_id FK", "nama", "kategori", "penanggung_jawab", "kontak", "deskripsi", "foto", "metrik_label", "metrik_nilai", "aktif", "created_at"])

entitas(20, 200, 190, "LAPORAN_KEUANGAN", ["id PK", "bumdes_id FK", "created_by FK", "bulan", "tahun", "total_pemasukan", "total_pengeluaran", "keterangan", "file_lpj", "status", "created_at", "updated_at"])
entitas(270, 200, 170, "ASPIRASI", ["id PK", "nama", "kategori", "whatsapp", "dusun", "pesan", "status", "catatan_internal", "publik", "created_at"])
entitas(490, 200, 170, "NOTIFIKASI", ["id PK", "judul", "pesan", "tipe", "dibaca", "created_at"])

# Garis relasi sederhana
garis = lambda x1,y1,x2,y2: d2.add(Line(x1,y1,x2,y2, strokeColor=LINE_GRAY, strokeWidth=1))
garis(105, 560, 115, 330)
garis(315, 560, 315, 330)
garis(315, 560, 105, 330)

renderPM.drawToFile(d2, "docs/diagrams/erd-final.png", fmt="PNG", dpi=120)
print("erd OK")
