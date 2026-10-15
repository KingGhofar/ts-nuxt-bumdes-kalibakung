# -*- coding: utf-8 -*-
"""Gambar Waterfall (ReportLab) -> PNG, tidak bergantung service online."""
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPM

W, H = 620, 180
d = Drawing(W, H)

BOX_W, BOX_H = 96, 46
GAP = 6
START_X = 6
Y = H - BOX_H - 16

tahap = [
    ("1. Perencanaan", "Observasi &\nWawancara"),
    ("2. Analisis", "Kebutuhan Data\n& Aturan"),
    ("3. Perancangan", "Use Case,\nERD, UI"),
    ("4. Implementasi", "Nuxt 4 +\nPostgreSQL"),
    ("5. Pengujian", "Black Box &\nResponsivitas"),
    ("6. Evaluasi", "Pemeliharaan\nSistem"),
]

blue = HexColor("#2563EB")
white = HexColor("#FFFFFF")
dark = HexColor("#0F172A")
gray = HexColor("#475569")

x = START_X
for i, (judul, sub) in enumerate(tahap):
    d.add(Rect(x, Y, BOX_W, BOX_H, rx=8, ry=8, fillColor=blue, strokeColor=None))
    d.add(String(x + BOX_W/2, Y + BOX_H - 16, judul, fontName="Times-Bold", fontSize=10,
                 fillColor=white, textAnchor="middle"))
    # sub multi-baris
    lines = sub.split("\n")
    yy = Y + 14
    for ln in lines:
        d.add(String(x + BOX_W/2, yy, ln, fontName="Times-Roman", fontSize=8,
                     fillColor=white, textAnchor="middle"))
        yy -= 10
    if i < len(tahap) - 1:
        # panah
        ax = x + BOX_W + 2
        ay = Y + BOX_H/2
        bx = x + BOX_W + GAP + 2
        d.add(Line(ax, ay, bx, ay, strokeColor=gray, strokeWidth=1.4))
        d.add(Polygon([bx, ay, bx-6, ay+4, bx-6, ay-4], fillColor=gray, strokeColor=None))
    x += BOX_W + GAP

renderPM.drawToFile(d, "docs/diagrams/waterfall.png", fmt="PNG", dpi=120)
print("saved docs/diagrams/waterfall.png")
