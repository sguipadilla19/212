# Gera dados da casa em metros a partir das coordenadas (pt) extraídas de planta.pdf.
# Escala 1:100 -> 1 m = 28,3465 pt. Origem: canto noroeste da área coberta (pilar do eixo 1 / eixo A).
import json, base64, os, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.normpath(os.path.join(HERE, "..", "..", "planta.pdf"))
OUT_JSON = os.path.join(HERE, "casa.json")
OUT_SLIM = os.path.normpath(os.path.join(HERE, "..", "dados_casa.json"))

S = 28.3465; X0 = 91.2; Y0 = 190.44
def mx(x): return round((x - X0) / S, 3)
def mz(y): return round((y - Y0) / S, 3)
def R(x0, x1, y0, y1): return {"x0": mx(x0), "x1": mx(x1), "z0": mz(y0), "z1": mz(y1)}

H = 2.80
WIN = (1.10, 2.10); WINH = (1.60, 2.10); WINBIG = (0.60, 2.10); DOOR = (0.0, 2.10); OPEN = (0.0, 2.10)

def wall(x0, x1, y0, y1, ops=(), kind="int"):
    w = R(x0, x1, y0, y1); w["kind"] = kind
    horiz = (x1 - x0) >= (y1 - y0)
    w["axis"] = "x" if horiz else "z"
    w["ops"] = [{"a0": mx(a) if horiz else mz(a), "a1": mx(b) if horiz else mz(b), "z0": t[0], "z1": t[1], "type": ty}
                for (a, b, t, ty) in ops]
    core = w["x0"] >= mx(284.7) and w["x1"] <= mx(494.8) and w["z1"] <= mz(316.1)
    right = w["x0"] >= mx(494.7)
    w["base"] = 0.2 if (core or right) else 0.0
    return w

walls = [
    # ---------- ALA OESTE ----------
    wall(146.46, 494.76, 246.60, 250.86, [(221.88, 262.92, WIN, "win"), (320.88, 357.72, WINH, "win"), (423.12, 464.16, WIN, "win")], "ext"),
    wall(146.46, 508.08, 435.06, 439.32, [(213.12, 275.76, WINBIG, "win"), (359.52, 400.68, WIN, "win"), (420.96, 462.12, WIN, "win")], "ext"),
    wall(146.46, 150.72, 246.60, 439.32, [(261.48, 302.52, WIN, "win"), (316.08, 338.76, DOOR, "door"), (369.72, 410.88, WIN, "win")], "ext"),
    wall(494.76, 508.14, 190.44, 341.52, [(221.04, 243.72, OPEN, "open")], "ext"),
    wall(184.68, 508.08, 341.52, 345.78, [(279.96, 302.64, DOOR, "door"), (325.56, 359.88, OPEN, "open"), (401.88, 424.56, DOOR, "door")]),
    wall(192.36, 196.68, 250.86, 341.52),
    wall(150.72, 192.36, 308.94, 313.20, [(152.40, 173.40, DOOR, "door")]),
    wall(284.76, 289.02, 250.86, 311.76),
    wall(267.72, 318.84, 311.76, 316.02),
    wall(314.52, 318.78, 250.86, 311.76, [(291.96, 311.76, DOOR, "door")]),
    wall(359.88, 364.14, 250.86, 311.76, [(291.96, 311.76, DOOR, "door")]),
    wall(389.64, 393.90, 250.86, 311.76),
    wall(359.88, 410.88, 311.76, 316.02),
    wall(262.92, 267.24, 218.76, 246.60, kind="ext"),
    wall(418.80, 423.12, 218.76, 246.60, kind="ext"),
    # ---------- ALA LESTE ----------
    wall(547.56, 737.70, 190.44, 194.76, [(597.36, 622.92, WINH, "win")], "ext"),
    wall(508.14, 554.88, 243.72, 248.04, [(518.80, 542.00, DOOR, "door")], "ext"),
    wall(554.88, 559.14, 194.76, 268.44),
    wall(622.92, 627.12, 190.44, 268.44),
    wall(557.76, 622.92, 264.18, 268.44, [(600.24, 622.92, DOOR, "door")]),
    wall(629.16, 644.16, 264.18, 268.44),
    wall(554.88, 559.14, 268.44, 298.20, [(268.44, 298.20, DOOR, "door")]),
    wall(547.80, 648.42, 298.20, 302.40),
    wall(543.54, 547.80, 298.20, 345.84),
    wall(611.58, 615.84, 302.40, 341.52),
    wall(644.16, 648.42, 298.20, 341.52),
    wall(543.54, 737.70, 341.52, 345.78, [(567.60, 593.16, DOOR, "door"), (615.84, 641.28, OPEN, "open")]),
    wall(733.44, 737.70, 190.44, 439.32, [(208.92, 249.96, WIN, "win"), (284.40, 325.56, WIN, "win"), (345.84, 435.12, WIN, "win")], "ext"),
    wall(543.54, 737.70, 435.06, 439.32, [(641.28, 733.44, WIN, "win")], "ext"),
    wall(503.88, 508.08, 413.76, 439.32, kind="ext"),
    wall(543.54, 547.80, 412.44, 439.32, kind="ext"),
    wall(508.08, 543.54, 413.76, 417.60, [(508.08, 518.80, (0.0, 2.10), "glass"), (518.80, 543.54, DOOR, "door")], "ext"),
]

# ---------- PILARES / VIGAS ----------
pillars = []
for cx in [95.46, 158.10, 240.30, 324.18, 410.94, 473.58]:
    pillars.append(R(cx - 4.26, cx + 4.26, 190.44, 198.96))
for cy in [255.06, 340.86, 435.06]:
    pillars.append(R(91.2, 99.72, cy - 4.26, cy + 4.26))
    pillars.append(R(763.2, 771.72, cy - 4.26, cy + 4.26))
pillars.append(R(763.2, 771.72, 190.44, 198.96))
beams = [R(91.2, 477.84, 190.44, 198.96), R(91.2, 99.72, 190.44, 439.32), R(763.2, 771.72, 190.44, 439.32)]

# ---------- PISOS (com nome do cômodo para área) ----------
def floor(x0, x1, y0, y1, lvl, mat, name, outdoor=False):
    f = R(x0, x1, y0, y1); f.update({"lvl": lvl, "mat": mat, "name": name, "out": outdoor}); return f
floors = [
    floor(150.72, 508.08, 345.78, 435.06, 0.0, "wood", "Sala de Estar / Jantar"),
    floor(150.72, 192.36, 313.20, 341.52, 0.0, "wood", "Nicho / Q. Elétrico"),
    floor(150.72, 192.36, 250.86, 308.94, 0.0, "tile", "Lavabo"),
    floor(196.68, 284.76, 250.86, 341.52, 0.0, "wood", "Dormitório 01"),
    floor(284.76, 312.30, 316.02, 341.52, 0.0, "wood", "Dormitório 01"),
    floor(312.30, 366.50, 316.02, 341.52, 0.20, "tile", "Hall dos Banhos"),
    floor(318.78, 359.88, 250.86, 316.02, 0.20, "tile", "Hall dos Banhos"),
    floor(289.02, 314.52, 250.86, 311.76, 0.20, "tile", "WC"),
    floor(364.14, 389.64, 250.86, 311.76, 0.20, "tile", "Chuveiro"),
    floor(366.50, 393.90, 316.02, 341.52, 0.20, "wood", "Dormitório 02"),
    floor(393.90, 494.76, 250.86, 341.52, 0.20, "wood", "Dormitório 02"),
    floor(508.14, 554.88, 248.04, 345.78, 0.20, "stone", "Corredor"),
    floor(508.08, 543.54, 345.78, 413.76, 0.20, "stone", "Hall de Entrada"),
    floor(508.14, 547.56, 190.44, 243.72, 0.20, "stone", "Vestíbulo Norte", True),
    floor(508.08, 543.54, 417.60, 439.32, 0.05, "stone", "Alpendre", True),
    floor(547.80, 733.44, 345.78, 435.06, 0.20, "stone", "Cozinha"),
    floor(547.80, 611.58, 302.40, 341.52, 0.20, "stone", "Lugar de Guardado"),
    floor(615.84, 644.16, 302.40, 341.52, 0.20, "stone", "Despensa"),
    floor(559.14, 733.44, 268.44, 341.52, 0.20, "wood", "Suíte"),
    floor(627.12, 733.44, 194.76, 268.44, 0.20, "wood", "Suíte"),
    floor(559.14, 622.92, 194.76, 264.18, 0.20, "tile", "Banho da Suíte"),
    floor(99.72, 146.46, 198.96, 439.32, 0.0, "deck", "Varanda Oeste", True),
    floor(146.46, 494.76, 198.96, 246.60, 0.0, "deck", "Varanda Norte / Lavanderia", True),
    floor(737.70, 771.72, 194.76, 435.06, 0.20, "deck", "Varanda Leste", True),
    floor(82.44, 795.0, 439.32, 478.0, -0.30, "concrete", "Calçada", True),
    floor(82.44, 99.72, 160.0, 439.32, -0.30, "concrete", "Calçada", True),
    floor(771.72, 795.0, 160.0, 439.32, -0.30, "concrete", "Calçada", True),
    floor(82.44, 795.0, 160.0, 190.44, -0.30, "concrete", "Calçada", True),
]
roofs = [R(82.44, 508.14, 186.0, 443.0), R(508.14, 795.0, 186.0, 443.0)]

# ---------- ESCADAS (degraus) ----------
# {x0,x1,z0,z1, top, bottom, dir}: desce na direção dir a partir do nível top até bottom
def stair(x0, x1, y0, y1, top, bottom, d):
    s = R(x0, x1, y0, y1); s.update({"top": top, "bottom": bottom, "dir": d}); return s
stairs = [
    stair(508.08, 543.54, 439.32, 453.0, 0.05, -0.30, "S"),     # alpendre -> calçada
    stair(146.46, 167.76, 439.32, 510.12, 0.0, -0.30, "E"),     # escada sudoeste (como na planta)
    stair(559.14, 580.38, 439.32, 473.28, 0.05, -0.30, "E"),    # acesso ao ateliê
    stair(771.72, 788.0, 194.76, 435.06, 0.20, -0.30, "E"),     # varanda leste -> jardim
    stair(90.0, 99.72, 198.96, 439.32, 0.0, -0.30, "W"),        # varanda oeste -> jardim
    stair(99.72, 494.76, 186.0, 198.96, 0.0, -0.30, "N"),       # varanda norte -> jardim
]

# ---------- PORTAS: dobradiça, direção aberta (na planta) e direção fechada ----------
def door(hx, hy, open_, closed, ln, base):
    return {"hx": mx(hx), "hz": mz(hy), "open": open_, "closed": closed, "len": ln, "base": base}
doors = [
    door(152.40, 311.07, "N", "E", 0.73, 0.0),    # lavabo
    door(312.30, 316.02, "W", "S", 0.74, 0.2),    # dorm 1 -> hall banhos
    door(366.50, 316.02, "E", "S", 0.74, 0.2),    # dorm 2 -> hall banhos
    door(316.65, 311.76, "W", "N", 0.68, 0.2),    # WC
    door(362.01, 311.76, "E", "N", 0.67, 0.2),    # chuveiro
    door(542.00, 245.88, "N", "W", 0.82, 0.2),    # vestíbulo norte
    door(542.00, 415.68, "N", "W", 0.82, 0.2),    # porta principal
    door(622.92, 266.31, "N", "W", 0.73, 0.2),    # banho suíte
    door(557.01, 298.20, "E", "N", 0.82, 0.2),    # suíte
    door(568.80, 343.65, "N", "E", 0.82, 0.2),    # lugar de guardado
    door(302.64, 343.65, "N", "W", 0.80, 0.0),    # dormitório 01 (sala)
    door(424.56, 343.65, "N", "W", 0.80, 0.2),    # dormitório 02 (sala)
    door(148.59, 338.76, "E", "N", 0.80, 0.0),    # porta oeste do nicho
]

# ---------- MOBILIÁRIO (tipado) ----------
def item(t, x0, x1, y0, y1, lvl, **kw):
    b = R(x0, x1, y0, y1); b.update({"t": t, "lvl": lvl}); b.update(kw); return b
furn = [
    # dormitório 1
    item("bed", 205.0, 230.2, 252.0, 310.6, 0.0, head="N", single=True, color=0x7f93b8),
    item("wardrobe", 267.72, 284.76, 250.86, 311.76, 0.0, face="W"),
    item("rug", 200.0, 262.0, 275.0, 335.0, 0.0, color=0xb9a899),
    # dormitório 2
    item("bed", 422.5, 448.5, 253.0, 310.0, 0.2, head="N", single=True, color=0xa3b58a),
    item("bed", 467.0, 492.0, 253.0, 310.0, 0.2, head="N", single=True, color=0xd6a86f),
    item("wardrobe", 393.90, 410.88, 250.86, 311.76, 0.2, face="E"),
    item("rug", 418.0, 492.0, 312.0, 336.0, 0.2, color=0xa8b0b8),
    # suíte
    item("bed", 665.4, 708.6, 196.4, 251.0, 0.2, head="N", single=False, color=0x8d8aa6),
    item("nightstand", 652.0, 664.0, 196.4, 205.5, 0.2), item("nightstand", 709.8, 721.8, 196.4, 205.5, 0.2),
    item("wardrobe", 627.12, 644.16, 194.76, 264.18, 0.2, face="E"),
    item("rug", 648.0, 726.0, 236.0, 300.0, 0.2, color=0xc4b8a9),
    item("plant", 716.0, 730.0, 320.0, 338.0, 0.2),
    # banho suíte
    item("shower", 559.14, 597.72, 194.76, 220.20, 0.2),
    item("toilet", 601.0, 621.0, 198.0, 222.0, 0.2, face="S"),
    item("vanity", 559.14, 571.2, 222.0, 262.0, 0.2, face="E", basins=2),
    # núcleo de banhos
    item("toilet", 296.0, 309.0, 252.0, 270.0, 0.2, face="S"),
    item("shower", 364.14, 389.64, 250.86, 276.36, 0.2),
    item("vanity", 318.84, 359.88, 250.86, 264.18, 0.2, face="S", basins=2),
    # lavabo
    item("toilet", 173.3, 186.0, 259.0, 275.0, 0.0, face="W"),
    item("vanity", 175.5, 192.36, 287.1, 307.26, 0.0, face="W", basins=1),
    # sala de estar
    item("sofa", 213.0, 268.0, 410.7, 433.7, 0.0, back="S", color=0x4f5f7a),
    item("armchair", 167.0, 187.6, 374.0, 396.0, 0.0, back="W", color=0x8a6f5a),
    item("armchair", 167.0, 187.6, 398.0, 420.0, 0.0, back="W", color=0x8a6f5a),
    item("armchair", 297.0, 317.6, 374.0, 396.0, 0.0, back="E", color=0x8a6f5a),
    item("armchair", 297.0, 317.6, 398.0, 420.0, 0.0, back="E", color=0x8a6f5a),
    item("roundtable", 224.5, 260.0, 378.5, 399.0, 0.0, h=0.42),
    item("rack", 196.9, 284.3, 347.5, 360.0, 0.0),
    item("tv", 220.0, 262.0, 349.0, 351.5, 0.0),
    item("rug", 160.0, 325.0, 366.0, 432.0, 0.0, color=0xb3a08c),
    item("plant", 152.0, 164.0, 420.0, 432.0, 0.0),
    # sala de jantar
    item("table", 372.8, 444.0, 372.7, 402.7, 0.0),
    *[item("chair", x, x + 11.5, 359.5, 372.0, 0.0, back="N") for x in (381.0, 401.5, 422.0)],
    *[item("chair", x, x + 11.5, 403.0, 415.5, 0.0, back="S") for x in (381.0, 401.5, 422.0)],
    item("rug", 362.0, 455.0, 352.0, 424.0, 0.0, color=0x7d7a86),
    item("cabinet", 321.0, 361.3, 418.7, 431.4, 0.0, face="N", glass=True),
    item("cabinet", 462.5, 504.0, 418.7, 431.4, 0.0, face="N", glass=True),
    # varanda oeste
    item("armchair", 111.8, 131.3, 348.6, 370.4, 0.0, back="W", color=0x6d7d6a),
    item("armchair", 109.5, 130.0, 403.8, 423.4, 0.0, back="W", color=0x6d7d6a),
    item("roundtable", 114.0, 127.8, 378.5, 392.3, 0.0, h=0.45),
    item("plant", 104.0, 116.0, 206.0, 218.0, 0.0),
    # lavanderia
    item("tank", 276.12, 332.88, 231.6, 246.6, 0.0),
    item("washer", 342.24, 358.08, 229.0, 244.62, 0.0), item("washer", 361.56, 377.40, 229.0, 244.62, 0.0),
    # cozinha
    item("counter", 629.52, 716.40, 418.08, 435.06, 0.2, back="S", sink=(675.5, 690.8)),
    item("counter", 594.0, 629.58, 368.3, 435.06, 0.2, back="W"),
    item("island", 647.4, 689.0, 369.0, 387.0, 0.2, cooktop=(668.0, 684.0)),
    item("stool", 651.7, 665.3, 352.0, 368.0, 0.2), item("stool", 673.8, 686.6, 352.0, 368.0, 0.2),
    item("fridge", 617.4, 643.8, 322.4, 339.8, 0.2, face="S"),
    item("plant", 722.0, 732.0, 350.0, 360.0, 0.2),
    # hall / corredor
    item("plant", 511.0, 521.0, 335.0, 345.0, 0.2),
]

labels = [(230, 392, "Sala de Estar"), (410, 392, "Sala de Jantar"), (238, 285, "Dormitório 01"), (450, 285, "Dormitório 02"), (171, 280, "Lavabo"), (171, 328, "Q. Elétrico"),
          (301, 290, "WC"), (339, 290, "Banho"), (377, 292, "Chuveiro"), (300, 230, "Lavanderia"), (680, 395, "Cozinha"), (690, 300, "Suíte"), (590, 235, "Banho Suíte"),
          (580, 322, "Lugar de Guardado"), (630, 315, "Despensa"), (527, 380, "Hall"), (530, 215, "Acesso do Escritório"), (525, 428, "Acesso Principal"),
          (123, 300, "Varanda Oeste"), (300, 210, "Varanda Norte"), (754, 300, "Varanda Leste"), (530, 300, "Corredor")]
labels = [{"x": mx(x), "z": mz(y), "t": t} for x, y, t in labels]

lights = [(230, 392), (410, 392), (238, 290), (450, 290), (171, 280), (339, 300), (680, 395), (690, 300), (590, 230), (530, 300), (527, 380), (300, 230), (580, 322), (123, 320), (754, 300)]
lights = [{"x": mx(x), "z": mz(y)} for x, y in lights]

spots = [("Entrada principal", 470, 540, -20), ("Sala de Estar", 300, 405, 60), ("Sala de Jantar", 420, 420, -30), ("Dormitório 01", 275, 330, 60), ("Dormitório 02", 455, 330, -40),
         ("Núcleo de banhos", 339, 335, 0), ("Cozinha", 722, 352, 135), ("Suíte", 700, 330, 20), ("Varanda oeste", 123, 250, 180), ("Lavanderia", 300, 225, 0), ("Vestíbulo norte", 527, 205, 180)]
spots = [{"name": n, "x": mx(x), "z": mz(y), "yaw": yaw} for n, x, y, yaw in spots]

# tour guiado: (x, y em pt, yaw, pausa em s, texto opcional, altura de voo opcional)
tour_pts = [
    (470, 540, -20, 3.0, "Fachada sul e acesso principal"), (525, 470, 0, 0.5, None), (526, 428, 0, 0.5, None), (527, 395, 0, 0.3, None), (527, 380, -90, 2.0, "Hall de entrada"),
    (600, 395, -90, 0.3, None), (640, 393, -60, 3.0, "Cozinha com ilha e despensa"), (560, 395, 0, 0.3, None), (530, 352, 0, 0.3, None), (530, 300, 0, 1.5, "Corredor para a suíte"),
    (556, 283, -90, 0.3, None), (640, 300, -60, 3.0, "Suíte com closet"), (611, 276, 0, 0.3, None), (611, 252, 0, 0.3, None), (592, 235, 90, 2.0, "Banho da suíte"),
    (611, 252, 180, 0.3, None), (611, 278, 180, 0.3, None), (562, 283, 90, 0.3, None), (530, 300, 180, 0.3, None), (527, 360, 180, 0.3, None), (500, 385, 90, 0.5, None),
    (420, 395, 90, 3.0, "Sala de jantar"), (300, 400, 90, 0.5, None), (230, 395, 0, 3.0, "Sala de estar"), (171, 335, 0, 0.3, None), (164, 322, 0, 0.3, None),
    (164, 285, 0, 2.0, "Lavabo"), (164, 322, 180, 0.3, None), (171, 335, 180, 0.3, None), (240, 380, 0, 0.3, None), (291, 365, 0, 0.3, None), (291, 332, 0, 0.3, None),
    (240, 295, 150, 3.0, "Dormitório 01"), (298, 328, 0, 0.3, None), (339, 328, 0, 0.3, None), (339, 288, 0, 2.5, "Núcleo de banhos compartilhado"), (339, 328, 0, 0.3, None),
    (381, 328, 0, 0.3, None), (450, 295, -150, 3.0, "Dormitório 02"), (413, 330, 0, 0.3, None), (413, 365, 0, 0.3, None), (343, 365, 0, 0.3, None), (160, 400, 90, 0.3, None),
    (148, 327, 90, 0.3, None), (123, 320, 0, 2.0, "Varanda oeste"), (123, 222, -90, 0.5, None), (300, 222, -90, 2.5, "Lavanderia na varanda norte"), (480, 222, -90, 0.3, None),
    (440, 330, 0, 6.0, "Vista aérea", 16.0),
]
tour = [{"x": mx(p[0]), "z": mz(p[1]), "yaw": p[2], "dwell": p[3], "text": p[4], "fly": (p[5] if len(p) > 5 else None)} for p in tour_pts]

# árvores (posições fixas, em m, fora da casa)
trees = [(-7, -3, 1.0), (-8, 9, 1.2), (-4, 16, 0.9), (8, 17, 1.1), (19, 16.5, 1.0), (30, 11, 1.2), (31, -2, 1.0), (22, -7, 0.9), (9, -7.5, 1.1), (-2, -8, 1.0), (35, 5, 0.9), (-10, 3, 1.1)]
trees = [{"x": x, "z": z, "s": s} for x, z, s in trees]

doc = pymupdf.open(PDF); page = doc[0]
clip = pymupdf.Rect(78, 183, 800, 482)
pix = page.get_pixmap(matrix=pymupdf.Matrix(2.2, 2.2), clip=clip)
pix.save(os.path.join(HERE, "minimap.png"))
b64 = base64.b64encode(open(os.path.join(HERE, "minimap.png"), "rb").read()).decode()
minimap = {"x0": mx(clip.x0), "x1": mx(clip.x1), "z0": mz(clip.y0), "z1": mz(clip.y1), "w": pix.width, "h": pix.height, "png": "data:image/png;base64," + b64}

data = {"H": H, "walls": walls, "pillars": pillars, "beams": beams, "floors": floors, "roofs": roofs, "stairs": stairs, "doors": doors, "furn": furn,
        "labels": labels, "lights": lights, "spots": spots, "tour": tour, "trees": trees,
        "bounds": {"x0": mx(82.44), "x1": mx(795), "z0": mz(160), "z1": mz(478)}, "minimap": minimap}
json.dump(data, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False)
slim = {k: v for k, v in data.items() if k != "minimap"}
json.dump(slim, open(OUT_SLIM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("walls", len(walls), "furn", len(furn), "floors", len(floors), "doors", len(doors), "tour", len(tour), "json KB", len(json.dumps(data)) // 1024)
