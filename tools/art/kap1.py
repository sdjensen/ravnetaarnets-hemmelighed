"""Kapitel 1-scener, tegnet med kit.py i træsnits-/tuschstil."""
import math
from kit import (Tegning, Form, form, rect, glat, kantet, f, INK, PAPER, PAPER2, SEPIA, STEN,
                 GOLD, BLOOD, MOSS, ARCANE, W, H)
import figurer as fg
import elementer as el

S = {}
BG, MG, SU, FG, LY = "background", "midground-architecture", "subject", "foreground-framing", "lighting-overlay"


def scene(fn):
    S[fn.__name__.replace("_", "-")] = fn
    return fn


def stjerner(t, n=24, ymax=200):
    return "".join(f'<circle cx="{f(t.u(30, 770))}" cy="{f(t.u(25, ymax))}" r="{f(t.u(0.8, 2))}" fill="{INK}" opacity=".7"/>' for _ in range(n))


def gulv(t, y=400, fyld=el.TRAE):
    return t.planker(rect(0, y, W, H - y + 10), "h", 18, fyld)


def stenvaeg(t, y1=H, fyld=STEN, morkhed=0.3):
    return t.mur(rect(-5, -5, W + 10, y1 + 5), 22, (34, 62), fyld=fyld, morkhed=morkhed)


# ====================================================================== Vildmose
@scene
def vildmose_landsby():
    t = Tegning("Landsbyen Vildmose i måneskin", 1)
    t.tegn(BG, t.himmel(ARCANE, h=360, op=0.6), stjerner(t), el.maane(t, 640, 96, 44))
    t.tegn(BG, t.sky(230, 120, 200, 22), t.sky(470, 70, 150, 16))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 280, 270, 50, 0.55), 1, PAPER2, kant=1.4, op=0.8))
    for x in range(20, 800, 34):
        t.tegn(BG, t.gran(x + t.u(-10, 10), 292 + t.u(-6, 6), t.u(40, 70), op=0.5, lys=False))
    t.tegn(MG, t.lag_land([(-10, 330), (200, 312), (420, 322), (620, 306), (810, 320)], 1, PAPER2, kant=1.8))
    t.tegn(MG, el.hus(t, 80, 362, 130, 72), el.hus(t, 300, 340, 100, 58, skorsten=False), el.hus(t, 560, 372, 150, 84))
    sti = t.sti_vej(420, 470, 380, 324, 240, 14, sving=40)
    t.tegn(MG, t.sti(sti, PAPER, INK, 1.6), t.prikker(sti, 70, 1, op=0.5), t.skraver(sti, 0, 8, 0.8, op=0.35))
    hegn = ""
    for x in range(230, 330, 22):
        hegn += f'<path d="M{x} {396 + (x - 230) * 0.1:.0f} v-34" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    hegn += f'<path d="M226 378 L332 386 M226 366 L332 374" stroke="{INK}" stroke-width="2.4"/>'
    t.tegn(MG, hegn, t.graes(0, 800, 380, 120, 10, ybund=445))
    t.tegn(SU, fg.placer(fg.kappefigur(kant=GOLD), 476, 404, 0.9), f'<path d="M496 330 L500 404" stroke="{INK}" stroke-width="3.5"/>',
           f'<path d="M492 330 h14 v16 h-14z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(FG, t.lag_land([(-10, 440), (120, 424), (260, 448)], 3, SEPIA, kant=2), t.loevtrae(40, 446, 300, bar=True))
    t.tegn(FG, t.sten(720, 436, 40), t.sten(670, 444, 24), t.graes(620, 800, 446, 30, 14))
    t.tegn(LY, t.gloed(499, 338, 60, GOLD, 0.8))
    for cx, cy in ((106, 330), (324, 318), (590, 333)):
        t.tegn(LY, t.gloed(cx, cy, 36, GOLD, 0.6))
    return t.svg()


# ====================================================================== Kroen
@scene
def den_sorte_gryde():
    t = Tegning("Kroen Den Sorte Gryde", 41)
    t.tegn(BG, stenvaeg(t, 400))
    t.tegn(BG, t.planker(rect(-5, -5, W + 10, 42), "h", 14, el.TRAE), t.planker(rect(110, 37, 26, 365), "v", 13, el.TRAE),
           t.planker(rect(420, 37, 26, 365), "v", 13, el.TRAE))
    urter = ""
    for i, x in enumerate(range(170, 380, 34)):
        urter += f'<path d="M{x} 40 v{14 + i % 2 * 8}" stroke="{INK}" stroke-width="1.5"/>'
        urter += f'<path d="M{x - 9} {54 + i % 2 * 8} q9 -6 18 0 l-9 {40 + i % 3 * 6}z" fill="{MOSS}" stroke="{INK}" stroke-width="1.6"/>'
    t.tegn(MG, urter)
    # ildsted
    ramme = rect(520, 150, 270, 260)
    t.tegn(MG, t.mur(ramme, 20, (24, 44), morkhed=0.4))
    aab = el.bue(560, 410, 190, 200)
    t.tegn(MG, t.sti(aab, INK, INK, 2.5), t.gloed(655, 380, 140, BLOOD, 0.7), el.ild(t, 655, 410, 120, 90),
           el.gryde(t, 655, 352, 96), el.kaede(655, 230, 655, 306, 12), el.damp(655, 300, 3, 50))
    t.tegn(MG, f'<path d="M504 150 H806 V132 H504Z" fill="{INK}"/>')
    t.tegn(MG, t.planker(rect(160, 196, 230, 12), "h", 12, el.TRAE))
    for i, x in enumerate(range(176, 380, 30)):
        t.tegn(MG, f'<path d="M{x} 196 v-26 q0 -8 6 -12 v-10 h6 v10 q6 4 6 12 v26z" fill="{(MOSS, BLOOD, SEPIA, ARCANE)[i % 4]}" stroke="{INK}" stroke-width="1.8"/>')
    t.tegn(MG, f'<path d="M300 40 V96" stroke="{INK}" stroke-width="2"/><path d="M286 96 h28 l-4 34 h-20z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/><path d="M282 96 h36 l-8 -10 h-20z" fill="{INK}"/>')
    t.tegn(MG, gulv(t, 404))
    # bord med krus og terninger
    t.tegn(MG, el.bord(t, 170, 330, 300))
    krus = rect(250, 296, 30, 34)
    t.tegn(SU, t.modelleret(krus, el.TRAE, (1, 0), 2, kerne=False, bredde=2), f'<path d="M280 304 q14 0 14 12 q0 10 -14 10" fill="none" stroke="{INK}" stroke-width="3"/>')
    for x, y, rot in ((340, 316, 12), (372, 318, -8)):
        t.tegn(SU, f'<g transform="rotate({rot} {x + 9} {y + 9})"><rect x="{x}" y="{y}" width="16" height="16" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                   f'<circle cx="{x + 5}" cy="{y + 5}" r="1.8" fill="{INK}"/><circle cx="{x + 11}" cy="{y + 11}" r="1.8" fill="{INK}"/></g>')
    t.tegn(SU, f'<path d="M400 332 v-28 q0 -6 6 -6 h18 q6 0 6 6 v28z" fill="{SEPIA}" stroke="{INK}" stroke-width="2"/>')
    # den fremmede (venstre) og den gamle kone ved ilden
    t.tegn(SU, fg.placer(fg.kappefigur(kant=PAPER), 120, 452, 1.55),
           f'<path d="M108 312 q6 -4 12 0 M128 312 q6 -4 12 0" stroke="{GOLD}" stroke-width="2.4" fill="none"/>')
    t.tegn(SU, fg.placer(fg.kappefigur(kant=GOLD), 500, 452, 1.15, spejl=True))
    t.tegn(FG, f'<path d="M-5 -5 H40 V455 H-5Z" fill="{INK}"/>')
    t.tegn(LY, t.gloed(655, 360, 240, GOLD, 0.45), t.gloed(300, 114, 90, GOLD, 0.6))
    return t.svg()


# ====================================================================== Gråskoven
@scene
def graaskoven():
    t = Tegning("Gråskoven", 24)
    t.tegn(BG, t.himmel(MOSS, h=450, op=0.35))
    t.tegn(BG, t.straaler(420, -40, [76, 84, 92, 100, 108], 520, 0.05, GOLD, 0.55))
    for i in range(16):
        x = 30 + i * 50 + t.u(-15, 15)
        t.tegn(BG, t.gran(x, 330, t.u(170, 250), op=0.16 + t.u(0, 0.1), lys=False))
    t.tegn(BG, t.taage(240, 100, 0.85))
    for x, y, h in ((150, 330, 220), (270, 326, 160), (520, 330, 230), (650, 322, 180), (370, 318, 130)):
        t.tegn(MG, t.loevtrae(x, y, h))
    t.tegn(MG, t.lag_land([(-10, 340), (200, 326), (400, 334), (600, 322), (810, 336)], 2, PAPER2, kant=1.8))
    sti = t.sti_vej(420, 460, 406, 336, 200, 10, sving=60)
    t.tegn(MG, t.sti(sti, PAPER, INK, 1.6), t.skraver(sti, 0, 7, 0.8, op=0.45), t.prikker(sti, 50, 1, op=0.5))
    t.tegn(MG, t.graes(180, 660, 350, 80, 9, ybund=440))
    t.tegn(SU, t.loevtrae(620, 386, 220, kroneskala=0.9))
    t.tegn(SU, fg.placer(fg.gammel_mand(), 574, 390, 0.95, spejl=True))
    for x, b in ((40, 74), (765, 84)):
        stamme = form([(x - b / 2, -10), (x + b / 2, -10), (x + b * 0.45, 300), (x + b * 0.75, 460), (x - b * 0.75, 460), (x - b * 0.45, 300)], blod=False)
        t.tegn(FG, t.modelleret(stamme, SEPIA, (1, 0.2) if x < 400 else (-1, 0.2), 3, bredde=2.5, vinkel=80))
    for cx in (110, 200, 680, 720):
        d = ""
        for k in range(7):
            a = math.radians(-150 + k * 20)
            ex, ey = cx + math.cos(a) * 70, 450 + math.sin(a) * 60
            d += f"M{cx} 452 Q{f((cx + ex) / 2)} {f(ey - 20)} {f(ex)} {f(ey)} "
            for j in range(1, 6):
                px, py = cx + (ex - cx) * j / 6, 452 + (ey - 452) * j / 6 - 8 * math.sin(math.pi * j / 6)
                d += f"M{f(px)} {f(py)} l{f(t.u(4, 8))} {f(t.u(-8, -4))} M{f(px)} {f(py)} l{f(t.u(-8, -4))} {f(t.u(-6, -2))} "
        t.tegn(FG, f'<path d="{d}" stroke="{INK}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    t.tegn(LY, t.straaler(420, -40, [84, 92, 100], 520, 0.03, PAPER, 0.5))
    return t.svg()


# ====================================================================== Stencirklen
@scene
def stencirklen():
    t = Tegning("Stencirklen med sværdet i stenen", 30)
    t.tegn(BG, t.himmel(ARCANE, h=300, op=0.35))
    for x in range(-10, 820, 26):
        t.tegn(BG, t.gran(x, 250 + t.u(-8, 8), t.u(110, 170), op=0.75, lys=True))
    t.tegn(BG, t.taage(200, 70, 0.7))
    t.tegn(MG, t.lag_land([(-10, 260), (200, 250), (400, 256), (600, 248), (810, 260)], 1, PAPER, kant=1.6))
    sten = [(110, 360, 70, 150), (230, 312, 52, 112), (338, 290, 40, 82), (462, 290, 40, 82), (570, 312, 52, 112), (690, 360, 70, 150)]
    for x, y, b, h in sten:
        pts = [(x - b / 2, y), (x - b * 0.45, y - h * 0.7), (x - b * 0.2, y - h), (x + b * 0.25, y - h * 0.94), (x + b * 0.5, y - h * 0.6), (x + b / 2, y)]
        pts = [(px + t.u(-3, 3), py + t.u(-3, 3)) for px, py in pts]
        t.tegn(MG, t.modelleret(form(pts, blod=False), STEN, (1 if x < 400 else -1, 0.3), 2, bredde=2.4))
        t.tegn(MG, f'<path d="M{f(x - b * 0.3)} {f(y - h * 0.5)} l{f(b * 0.2)} 6 l-4 10 M{f(x)} {f(y - h * 0.75)} l6 8" stroke="{INK}" stroke-width="1.6" fill="none"/>')
        t.tegn(MG, f'<path d="M{f(x - b / 2)} {f(y)} q{f(b * 0.25)} -18 {f(b * 0.55)} -6 q-8 8 -{f(b * 0.55)} 6z" fill="{MOSS}" stroke="{INK}" stroke-width="1.2"/>')
    t.tegn(MG, t.graes(0, 800, 300, 120, 10, ybund=440))
    alter = form([(330, 392), (346, 344), (454, 344), (470, 392)], blod=False)
    t.tegn(SU, t.modelleret(alter, STEN, (1, 0.2), 3, bredde=2.6), f'<path d="M322 392 H478 V408 H322Z" fill="{INK}"/>')
    t.tegn(SU, t.gloed(400, 250, 160, ARCANE, 0.7), t.gloed(400, 250, 60, PAPER, 0.9))
    klinge = form([(394, 344), (394, 220), (400, 206), (406, 220), (406, 344)], blod=False)
    t.tegn(SU, t.sti(klinge, PAPER, INK, 2), f'<path d="M376 222 H424 V230 H376Z M396 222 V186 H404 V222Z" fill="{INK}"/>',
           f'<circle cx="400" cy="180" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
           f'<path d="M397 250 l3 6 3 -6 M397 272 h6 M400 290 v8 M397 312 l6 6" stroke="{ARCANE}" stroke-width="2" fill="none"/>')
    t.tegn(FG, t.lag_land([(-10, 430), (200, 420), (400, 440), (600, 418), (810, 432)], 3, SEPIA, kant=2))
    t.tegn(FG, t.gran(20, 460, 380, 160), t.gran(790, 460, 400, 170))
    t.tegn(LY, t.straaler(400, 210, list(range(0, 360, 30)), 170, 0.04, PAPER, 0.5), t.taage(380, 50, 0.6))
    return t.svg()


# ====================================================================== Ulvene
@scene
def ulvene():
    t = Tegning("Ulvene i Gråskoven", 52)
    t.tegn(BG, t.himmel(BLOOD, h=280, op=0.3), el.halvmaane(t, 650, 70, 26))
    for x in range(-20, 840, 22):
        t.tegn(BG, t.gran(x, 280 + t.u(-10, 10), t.u(160, 250), op=0.9, lys=True))
    for x in range(0, 820, 30):
        t.tegn(BG, t.gran(x + 10, 300, t.u(90, 140), op=1, lys=True))
    t.tegn(BG, f'<g fill="{GOLD}"><path d="M612 230 q8 -6 16 0 q-8 4 -16 0z M640 230 q8 -6 16 0 q-8 4 -16 0z"/></g>')
    t.tegn(MG, t.lag_land([(-10, 330), (200, 316), (400, 326), (600, 312), (810, 328)], 2, PAPER2, kant=2))
    t.tegn(MG, t.graes(0, 800, 330, 110, 10, ybund=430))
    t.tegn(SU, fg.placer(fg.ulv(), 220, 404, 0.78), fg.placer(fg.ulv(), 600, 410, 0.66, spejl=True))
    torn = ""
    for sx, retn in ((0, 1), (800, -1)):
        for k in range(3):
            y0 = 380 + k * 22
            torn += f"M{sx} {y0} Q{sx + retn * 100} {y0 - 70} {sx + retn * 210} {y0 - 10} "
            for j in range(1, 8):
                px = sx + retn * 210 * j / 8
                py = y0 - 55 * math.sin(math.pi * j / 8) + 10 * j / 8
                torn += f"M{f(px)} {f(py)} l{retn * 6} -9 M{f(px)} {f(py)} l{retn * -4} 8 "
    t.tegn(FG, f'<path d="{torn}" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    t.tegn(FG, t.lag_land([(-10, 440), (400, 430), (810, 442)], 3, SEPIA, kant=2))
    t.tegn(LY, t.gloed(400, 340, 300, BLOOD, 0.3))
    return t.svg()


# ====================================================================== Floden
@scene
def soelvaa_faergen():
    t = Tegning("Færgemanden ved floden Sølvå", 9)
    t.tegn(BG, t.himmel(ARCANE, h=220, op=0.5), t.sky(180, 80, 220, 22), t.sky(600, 60, 180, 18))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 196, 186, 30), 2, PAPER2, kant=1.6))
    for x in (60, 100, 150, 600, 650, 700, 760):
        t.tegn(BG, t.gran(x, 206, t.u(50, 80)))
    t.tegn(BG, t.loevtrae(300, 206, 90), t.loevtrae(480, 204, 70))
    t.tegn(MG, f'<rect x="0" y="206" width="800" height="200" fill="{PAPER}"/>', t.vand(0, 206, 800, 400), t.taage(206, 30, 0.6))
    # færgen
    flaade = form([(240, 318), (560, 318), (530, 344), (270, 344)], blod=False)
    t.tegn(SU, t.planker(flaade, "v", 20, el.TRAE), f'<path d="M232 318 H568" stroke="{INK}" stroke-width="5"/>')
    t.tegn(SU, fg.placer(fg.kappefigur(kant=PAPER), 450, 318, 1.15))
    t.tegn(SU, f'<path d="M380 120 L600 400" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    t.tegn(SU, f'<path d="M300 318 V278 M290 278 h20 v-26 h-20z" stroke="{INK}" stroke-width="3" fill="{GOLD}"/>')
    t.tegn(SU, f'<path d="M260 352 Q400 362 540 352" stroke="{INK}" stroke-width="1.5" fill="none" opacity=".6"/>')
    t.tegn(FG, t.lag_land([(-10, 400), (200, 390), (400, 410), (600, 396), (810, 404)], 3, SEPIA, kant=2))
    siv = ""
    for x in list(range(10, 140, 9)) + list(range(660, 800, 9)):
        h = t.u(50, 110)
        siv += f'<path d="M{x} 420 q{f(t.u(-6, 6))} -{f(h * 0.5)} {f(t.u(-10, 10))} -{f(h)}" stroke="{INK}" stroke-width="2.4" fill="none"/>'
        if t.r.random() < 0.3:
            siv += f'<ellipse cx="{x}" cy="{f(420 - h * 0.85)}" rx="4" ry="12" fill="{SEPIA}" stroke="{INK}" stroke-width="1.5"/>'
    t.tegn(FG, siv)
    t.tegn(LY, t.gloed(300, 265, 70, GOLD, 0.7))
    return t.svg()


# ====================================================================== Troldebroen
@scene
def troldebroen():
    t = Tegning("Trolden på stenbroen", 21)
    t.tegn(BG, t.himmel(ARCANE, h=250, op=0.4), t.sky(620, 70, 220, 20))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 200, 190, 60, 0.55), 1, PAPER2, blod=False, kant=1.4))
    for x in range(-10, 820, 40):
        t.tegn(BG, t.gran(x, 226, t.u(40, 70), op=0.7))
    t.tegn(MG, f'<rect x="0" y="300" width="800" height="150" fill="{PAPER}"/>', t.vand(0, 300, 800, 440))
    bro = Form("M-10 214 H810 V344 H650 Q646 262 400 258 Q154 262 150 344 H-10Z", (-10, 214, 810, 344))
    t.tegn(MG, t.mur(bro, 18, (26, 46), morkhed=0.25))
    bue = Form("M150 344 Q154 262 400 258 Q646 262 650 344Z", (150, 258, 650, 344))
    t.tegn(MG, t.sti(bue, INK, INK, 2), t.vand(180, 300, 620, 344, 1.5).replace(INK, PAPER).replace('stroke-width="1.3"', 'stroke-width="1" opacity=".35"'))
    t.tegn(MG, f'<path d="M-10 206 H810 V222 H-10Z" fill="{STEN}" stroke="{INK}" stroke-width="2.4"/>')
    t.tegn(SU, fg.placer(fg.trold(t=t), 560, 214, 1.05))
    t.tegn(SU, f'<path d="M470 214 Q440 200 420 206 Q410 210 414 214Z" fill="{INK}"/>',
           f'<path d="M424 208 v14 M436 206 v16 M448 208 v14 M460 210 v12" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>',
           f'<path d="M646 200 Q690 180 712 140" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    koelle = form([(700, 156), (738, 52), (760, 40), (774, 58), (726, 166)])
    t.tegn(SU, t.modelleret(koelle, el.TRAE, (1, 0.2), 3, bredde=2.4))
    t.tegn(FG, t.lag_land([(-10, 420), (160, 406), (300, 440), (320, 460)], 3, SEPIA, kant=2),
           t.lag_land([(480, 460), (560, 420), (700, 404), (810, 412)], 3, SEPIA, kant=2))
    t.tegn(FG, t.sten(110, 420, 40), t.sten(700, 414, 46), t.graes(0, 260, 430, 30, 14), t.graes(560, 800, 420, 30, 14))
    return t.svg()


# ====================================================================== Ravnetårnet
@scene
def ravnetaarnet():
    t = Tegning("Ravnetårnet", 61)
    t.tegn(BG, t.himmel(ARCANE, h=360, op=0.6), el.maane(t, 470, 120, 74))
    t.tegn(BG, t.sky(250, 110, 190, 26), t.sky(640, 210, 220, 24), t.sky(130, 190, 140, 18))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 300, 280, 90, 0.55), 1, PAPER2, blod=False, kant=1.4, op=0.75))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 330, 320, 40, 0.5), 2, PAPER2, kant=1.5))
    bakke = [(-10, 420), (120, 380), (260, 330), (360, 318), (440, 316), (540, 330), (680, 372), (810, 400)]
    t.tegn(MG, t.lag_land(bakke, 2, SEPIA, kant=2.2, vinkel=20))
    t.tegn(MG, t.lag_land([(-10, 440), (200, 416), (420, 430), (640, 410), (810, 430)], 3, SEPIA, kant=0, vinkel=-25, op=0.6))
    t.tegn(MG, t.graes(40, 760, 330, 90, 10, ybund=440))
    sti = form([(330, 452), (360, 420), (430, 396), (452, 370), (418, 346), (406, 326), (416, 326), (430, 346), (468, 370), (450, 400), (390, 426), (370, 452)])
    t.tegn(MG, t.sti(sti, PAPER2, INK, 1.6), t.prikker(sti, 60, 1, op=0.6))
    krop = form([(360, 322), (372, 78), (488, 78), (500, 322)], blod=False)
    t.tegn(MG, t.mur(krop, 17, (22, 40), morkhed=0.18))
    skygge_side = form([(448, 78), (488, 78), (500, 322), (452, 322)], blod=False)
    t.tegn(MG, t.skraver(skygge_side, 70, 3.5, 1.1), t.skraver(skygge_side, -20, 4.5, 1, op=0.8))
    tinder = "M362 78 h136 v-26 h-14 v12 h-16 v-12 h-16 v12 h-16 v-12 h-16 v12 h-16 v-12 h-16 v12 h-14 v-12 h-12Z"
    t.tegn(MG, f'<path d="{tinder}" fill="{STEN}" stroke="{INK}" stroke-width="2.2"/>', t.skraver(Form(tinder, (360, 52, 500, 80)), 70, 4))
    t.tegn(MG, f'<path d="M356 80 H504 V92 H356Z" fill="{INK}"/>')
    t.tegn(MG, f'<path d="M410 182 Q430 140 450 182 V236 H410Z" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>', f'<path d="M404 236 H456 V246 H404Z" fill="{INK}"/>')
    t.tegn(MG, f'<path d="M408 322 V274 Q430 244 452 274 V322Z" fill="{SEPIA}" stroke="{INK}" stroke-width="3"/>',
           f'<path d="M418 268 V322 M430 258 V322 M442 268 V322 M408 290 H452" stroke="{INK}" stroke-width="2"/>', f'<circle cx="444" cy="300" r="2.5" fill="{GOLD}"/>')
    efeu = "".join(f'<path d="M{f(370 + t.u(0, 30))} {f(300 - i * 14)} q4 -6 9 -2 q-3 5 -9 2z"/>' for i in range(14))
    t.tegn(MG, f'<g fill="{MOSS}" stroke="{INK}" stroke-width=".8">{efeu}</g>')
    t.tegn(SU, fg.placer(fg.ravn_siddende(), 426, 236, 0.85))
    for x, y, s in ((210, 70, 1.6), (250, 52, 1.1), (610, 60, 1.3), (660, 90, 0.9), (580, 110, 0.8)):
        t.tegn(SU, t.fugl(x, y, s))
    t.tegn(FG, t.lag_land([(-10, 446), (100, 432), (200, 446), (300, 452)], 3, SEPIA, kant=2))
    t.tegn(FG, t.loevtrae(70, 440, 330, bar=True))
    t.tegn(FG, t.sten(640, 430, 46), t.sten(700, 440, 34), t.sten(600, 444, 22))
    t.tegn(FG, t.graes(560, 790, 446, 40, 14), t.graes(0, 220, 446, 30, 16))
    t.tegn(LY, t.gloed(430, 205, 70, GOLD, 0.8), t.gloed(430, 205, 30, PAPER, 0.6))
    return t.svg()


# ====================================================================== Ravnesumpen
def birk(t, x, y, h):
    b = h * 0.05
    stamme = form([(x - b, y), (x - b * 0.8, y - h * 0.6), (x - b * 0.4, y - h), (x + b * 0.4, y - h), (x + b * 0.8, y - h * 0.6), (x + b, y)], blod=False)
    ud = t.sti(stamme, PAPER, INK, 2)
    for i in range(7):
        yy = y - h * t.u(0.05, 0.95)
        ud += f'<path d="M{f(x - b * 0.9)} {f(yy)} h{f(b * t.u(0.6, 1.4))}" stroke="{INK}" stroke-width="{f(t.u(2, 4))}"/>'
    ud += t.skraver(stamme, 90, 3, 1, halv=(1, 0, 0.2))
    for s in (-1, 1):
        yy = y - h * t.u(0.55, 0.8)
        ud += f'<path d="M{f(x)} {f(yy)} q{s * h * 0.15:.0f} {-h * 0.12:.0f} {s * h * 0.28:.0f} {-h * 0.1:.0f} M{f(x + s * h * 0.15)} {f(yy - h * 0.08)} l{s * 10} -16" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return ud


@scene
def ravnesumpen():
    t = Tegning("Ravnesumpen med de blå lys", 55)
    t.tegn(BG, t.himmel(ARCANE, h=280, op=0.4))
    t.tegn(BG, f'<path d="M560 262 L574 90 H622 L636 262Z M566 90 H628 V72 H566Z" fill="{INK}" opacity=".55"/>')
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 262, 252, 20), 2, PAPER2, kant=1.4, op=0.8), t.taage(220, 80, 0.8))
    t.tegn(MG, f'<rect y="270" width="800" height="180" fill="{PAPER2}"/>', t.vand(0, 270, 800, 440, 1.2))
    for cx, cy, rx in ((200, 330, 70), (530, 364, 90), (360, 300, 50)):
        t.tegn(MG, t.modelleret(form([(cx + rx * math.cos(a / 10 * 6.28), cy + rx * 0.14 * math.sin(a / 10 * 6.28)) for a in range(10)]), MOSS, (0, 1), 1, kerne=False, bredde=1.6))
    for x, h in ((110, 220), (250, 170), (470, 200), (660, 240), (740, 150)):
        t.tegn(MG, birk(t, x, 400, h))
    for cx, cy in ((330, 252), (400, 230), (560, 272), (300, 302), (620, 220)):
        t.tegn(SU, t.gloed(cx, cy, 34, ARCANE, 0.9), f'<circle cx="{cx}" cy="{cy}" r="4" fill="{PAPER}"/>')
    t.tegn(FG, t.lag_land([(-10, 412), (160, 400), (320, 420), (480, 432), (640, 402), (810, 416)], 3, SEPIA, kant=2))
    siv = "".join(f'<path d="M{x} 420 q{f(t.u(-5, 5))} -30 {f(t.u(-8, 8))} -{f(t.u(40, 90))}" stroke="{INK}" stroke-width="2.4" fill="none"/>' for x in list(range(10, 90, 8)) + list(range(700, 800, 8)))
    t.tegn(FG, siv)
    t.tegn(LY, t.taage(300, 50, 0.6), t.taage(360, 40, 0.5))
    return t.svg()


# ====================================================================== Kælderen
@scene
def kaelderen():
    t = Tegning("Fangen i tårnets kælder", 68)
    t.tegn(BG, f'<rect width="800" height="450" fill="{INK}"/>')
    hvaelv = Form("M60 460 V180 Q60 40 400 40 Q740 40 740 180 V460Z", (60, 40, 740, 460))
    t.tegn(MG, t.mur(hvaelv, 24, (40, 70), morkhed=0.45))
    rist = rect(340, 40, 120, 50)
    t.tegn(MG, t.sti(rist, INK, INK, 2), f'<path d="M362 40 V90 M386 40 V90 M410 40 V90 M434 40 V90" stroke="{STEN}" stroke-width="5"/>')
    t.tegn(MG, f'<path d="M60 410 H740 V460 H60Z" fill="{SEPIA}"/>', t.graes(120, 680, 414, 60, 8, farve=GOLD, bredde=1.2))
    t.tegn(SU, el.kaede(340, 190, 362, 300, 12), el.kaede(460, 190, 438, 300, 12))
    t.tegn(SU, f'<rect x="330" y="182" width="20" height="12" fill="{INK}"/><rect x="450" y="182" width="20" height="12" fill="{INK}"/>')
    t.tegn(SU, fg.placer(fg.kappefigur(kant=PAPER), 400, 414, 1.25))
    t.tegn(SU, f'<path d="M366 300 L384 330 M434 300 L416 330" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    rotter = ""
    for x, y in ((130, 404), (650, 400), (600, 408)):
        rotter += (f'<path d="M{x} {y} q10 -14 24 -8 q8 4 12 8 z M{x} {y - 2} q-16 2 -26 10" fill="{INK}" stroke="{INK}" stroke-width="2"/>'
                   f'<circle cx="{x + 28}" cy="{y - 6}" r="1.6" fill="{BLOOD}"/>')
    t.tegn(SU, rotter)
    t.tegn(FG, f'<path d="M-5 -5 H60 V455 H-5Z M740 -5 H805 V455 H740Z" fill="{INK}"/>')
    lysskakt = Form("M340 90 L240 410 H560 L460 90Z", (240, 90, 560, 410))
    t.tegn(LY, f'<path d="{lysskakt.d}" fill="{PAPER}" opacity=".22"/>', t.gloed(400, 340, 160, PAPER, 0.3))
    return t.svg()


# ====================================================================== Skeletvagten
@scene
def skeletvagten():
    t = Tegning("Skeletvagten på vindeltrappen", 66)
    t.tegn(BG, stenvaeg(t, 450, morkhed=0.3))
    aab = el.bue(210, 460, 380, 430)
    t.tegn(MG, t.sti(aab, INK, INK, 3))
    for i in range(7):
        y = 450 - i * 30
        x0 = 230 + i * 34
        trin = rect(x0, y - 30, 590 - x0 - 30, 30)
        t.tegn(MG, t.modelleret(trin, STEN, (1, 0.5), 1 + (i > 3), kerne=False, bredde=1.8))
    t.tegn(MG, t.sti(aab, "none", INK, 4))
    t.tegn(MG, el.fakkel(t, 130, 250))
    t.tegn(SU, fg.placer(fg.skelet(), 406, 360, 0.9))
    t.tegn(FG, f'<path d="M-5 -5 H40 Q30 225 44 455 H-5Z M805 -5 H760 Q770 225 756 455 H805Z" fill="{INK}"/>')
    t.tegn(LY, t.gloed(130, 170, 240, GOLD, 0.5), t.gloed(408, 228, 30, BLOOD, 0.7))
    return t.svg()


# ====================================================================== Morvaks kammer
@scene
def morvaks_kammer():
    t = Tegning("Troldmanden Morvaks kammer", 29)
    t.tegn(BG, stenvaeg(t, 450, fyld=PAPER2, morkhed=0.35))
    vindue = Form("M310 120 A90 90 0 1 1 490 120 A90 90 0 1 1 310 120Z", (310, 30, 490, 210))
    t.tegn(MG, t.sti(vindue, ARCANE, None, op=0.5), el.maane(t, 430, 100, 22, glorie=False),
           f'<circle cx="400" cy="120" r="90" fill="none" stroke="{INK}" stroke-width="14"/><path d="M400 30 V210 M310 120 H490" stroke="{INK}" stroke-width="7"/>')
    t.tegn(MG, el.reol(t, 20, 40, 160, 370, 4), el.reol(t, 620, 40, 160, 370, 4))
    t.tegn(MG, gulv(t, 410))
    # lænestol med sovende troldmand
    stol = form([(190, 420), (190, 250), (214, 214), (316, 214), (340, 250), (340, 420)])
    t.tegn(SU, t.modelleret(stol, BLOOD, (1, 0.4), 3, bredde=2.6))
    t.tegn(SU, fg.placer(fg.kappefigur(hat=True, kant=ARCANE), 266, 404, 1.45))
    t.tegn(SU, f'<path d="M248 290 q18 60 36 0 q-6 60 -18 80 q-12 -20 -18 -80z" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>',
           f'<path d="M254 274 q4 3 8 0 M272 274 q4 3 8 0" stroke="{PAPER}" stroke-width="2" fill="none"/>')
    t.tegn(SU, el.bord(t, 420, 330, 180))
    t.tegn(SU, t.gloed(510, 314, 120, ARCANE, 0.9), f'<path d="M490 330 q20 -36 40 0" stroke="{GOLD}" stroke-width="3" fill="none"/>',
           f'<circle cx="510" cy="314" r="12" fill="#cfe3f5" stroke="{INK}" stroke-width="2.5"/>')
    t.tegn(SU, f'<path d="M570 330 V292 H582 V330Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>', el.ild(t, 576, 292, 10, 18, gloed=True))
    t.tegn(SU, fg.placer(fg.ravn_siddende(), 700, 40, 0.8, spejl=True))
    t.tegn(SU, f'<path d="M440 330 v-10 h40 v10z M446 320 v-8 h30 v8z" fill="{BLOOD}" stroke="{INK}" stroke-width="1.5"/>')
    return t.svg()


# ====================================================================== Hjemkomsten
@scene
def hjemkomsten():
    t = Tegning("Hjemkomsten til Vildmose", 100)
    t.tegn(BG, t.himmel(GOLD, h=340, op=0.6), t.straaler(400, 300, list(range(185, 360, 12)), 560, 0.035, GOLD, 0.7))
    sol = form([(400 + 80 * math.cos(a / 24 * 6.283), 300 + 80 * math.sin(a / 24 * 6.283)) for a in range(24)])
    t.tegn(BG, t.gloed(400, 300, 220, GOLD, 0.7), t.sti(sol, GOLD, INK, 2.5), t.skraver(sol, 0, 6, 1, op=0.4, halv=(0, 1, 0.1)))
    t.tegn(BG, t.sky(170, 160, 200, 18), t.sky(640, 140, 220, 20))
    t.tegn(MG, t.lag_land([(-10, 330), (200, 300), (400, 318), (600, 296), (810, 316)], 2, SEPIA, kant=2.2))
    t.tegn(MG, el.hus(t, 70, 340, 120, 64), el.hus(t, 600, 330, 130, 70), el.hus(t, 230, 326, 80, 46, skorsten=False, vindue=False))
    t.tegn(SU, fg.placer(fg.vandrer(sværd=False), 360, 318, 0.9), fg.placer(fg.kappefigur(kant=GOLD), 450, 318, 0.82))
    t.tegn(SU, f'<path d="M402 318 V236 H410 V318Z" fill="{INK}"/><path d="M386 244 Q406 212 426 244" stroke="{GOLD}" stroke-width="3" fill="none"/>',
           t.gloed(406, 228, 50, ARCANE, 0.8), f'<circle cx="406" cy="228" r="11" fill="#cfe3f5" stroke="{INK}" stroke-width="2"/>')
    t.tegn(FG, t.lag_land([(-10, 420), (300, 404), (520, 420), (810, 400)], 3, SEPIA, kant=2), t.graes(0, 800, 420, 80, 14))
    for x, y, s in ((140, 90, 1.4), (180, 70, 1), (620, 60, 1.2), (660, 86, 0.9)):
        t.tegn(FG, t.fugl(x, y, s))
    return t.svg()


# ====================================================================== Værkstedet
@scene
def alkymistvaerkstedet():
    t = Tegning("Troldmandens værksted med nissen i buret", 46)
    t.tegn(BG, stenvaeg(t, 450, morkhed=0.25))
    vindue = el.bue(40, 270, 110, 200)
    t.tegn(MG, t.sti(vindue, ARCANE, INK, 6, op=0.9), el.halvmaane(t, 104, 120, 14), f'<path d="M95 70 V270 M40 170 H150" stroke="{INK}" stroke-width="5"/>')
    for y in (120, 210):
        t.tegn(MG, t.planker(rect(440, y, 340, 12), "h", 12, el.TRAE))
    farver = (MOSS, ARCANE, BLOOD, GOLD)
    for i, x in enumerate(range(462, 770, 44)):
        t.tegn(MG, el.kolbe(t, x, 108, 10 + i % 3 * 3, farver[i % 4], 12))
    for i, x in enumerate(range(470, 770, 52)):
        t.tegn(MG, f'<rect x="{x}" y="{176 + i % 2 * 6}" width="{16 + i % 3 * 4}" height="{34 - i % 2 * 6}" fill="{PAPER2}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(MG, f'<path d="M574 162 h26 v48 h-26z" fill="{BLOOD}" stroke="{INK}" stroke-width="2.4"/><rect x="578" y="176" width="18" height="12" fill="{PAPER}" stroke="{INK}"/>')
    t.tegn(MG, el.bord(t, 200, 330, 560))
    t.tegn(MG, el.kolbe(t, 300, 300, 24, MOSS), el.kolbe(t, 420, 306, 18, ARCANE), el.kolbe(t, 660, 298, 26, BLOOD))
    t.tegn(MG, f'<path d="M300 258 Q320 200 380 210 Q420 220 420 270 M660 252 Q680 220 720 240 L730 300" stroke="{INK}" stroke-width="4" fill="none"/>')
    t.tegn(MG, el.damp(300, 250, 3, 50), el.damp(660, 246, 2, 40))
    t.tegn(SU, f'<path d="M250 0 V44" stroke="{INK}" stroke-width="3"/>', t.gloed(250, 140, 110, MOSS, 0.6))
    t.tegn(SU, fg.placer(fg.nisse(), 250, 150, 1.0))
    t.tegn(SU, f'<g stroke="{INK}" stroke-width="3" fill="none"><path d="M190 190 V90 Q190 40 250 40 Q310 40 310 90 V190"/>'
               f'<path d="M210 190 V64 M230 190 V48 M250 190 V44 M270 190 V48 M290 190 V64"/><path d="M186 190 H314 M190 110 H310" stroke-width="5"/></g>')
    t.tegn(FG, f'<path d="M-5 430 H805 V455 H-5Z" fill="{INK}"/>')
    return t.svg()


# ====================================================================== Marnas hytte
@scene
def marnas_hytte():
    t = Tegning("Fiskerkonen Marnas hytte", 19)
    t.tegn(BG, t.planker(rect(-5, -5, W + 10, 420), "v", 30, el.TRAE))
    vindue = rect(600, 80, 120, 100)
    t.tegn(MG, t.sti(vindue, ARCANE, INK, 6, op=0.8), t.vand(604, 140, 716, 176, 1.2), f'<path d="M660 80 V180 M600 130 H720" stroke="{INK}" stroke-width="4"/>')
    net = Form("M380 30 L560 30 L520 170 L420 170Z", (380, 30, 560, 170))
    t.tegn(MG, t.skraver(net, 60, 8, 1.2), t.skraver(net, -60, 8, 1.2), t.sti(net, "none", INK, 2))
    fisk = ""
    for x in (230, 270, 310):
        fisk += f'<path d="M{x} 30 v20" stroke="{INK}" stroke-width="1.5"/><path d="M{x - 8} 50 q8 -6 16 0 q-2 22 -8 42 q-6 -20 -8 -42z M{x - 6} 94 l6 -6 6 6z" fill="{STEN}" stroke="{INK}" stroke-width="1.6"/>'
    t.tegn(MG, fisk, f'<path d="M210 30 H330" stroke="{INK}" stroke-width="3"/>')
    ildsted = rect(30, 170, 250, 250)
    t.tegn(MG, t.mur(ildsted, 20, (24, 44), morkhed=0.35))
    aab = el.bue(70, 420, 170, 170)
    t.tegn(MG, t.sti(aab, INK, INK, 2), el.ild(t, 155, 420, 110, 80), el.gryde(t, 155, 362, 90), el.kaede(155, 230, 155, 316, 12))
    t.tegn(MG, gulv(t, 416))
    t.tegn(MG, el.bord(t, 330, 360, 220))
    skaal = Form("M400 360 Q430 336 460 360Z", (400, 336, 460, 360))
    t.tegn(SU, t.modelleret(skaal, PAPER, (1, 0.3), 2, kerne=False), el.damp(430, 344, 3, 40))
    marna = form([(590, 452), (594, 380), (606, 330), (624, 306), (660, 300), (690, 314), (706, 352), (714, 452)])
    t.tegn(SU, t.modelleret(marna, MOSS, (1, 0.3), 2, bredde=2.6))
    forklaede = form([(624, 340), (676, 338), (690, 452), (612, 452)])
    t.tegn(SU, t.modelleret(forklaede, PAPER, (1, 0.2), 1, kerne=False, bredde=2))
    hoved = form([(650 + 24 * math.cos(a / 12 * 6.283), 272 + 28 * math.sin(a / 12 * 6.283)) for a in range(12)])
    t.tegn(SU, t.modelleret(hoved, PAPER2, (1, 0.3), 2, kerne=False, bredde=2.2))
    t.tegn(SU, f'<path d="M624 270 Q622 236 650 232 Q680 236 678 270 Q666 252 650 252 Q634 252 624 270Z M626 268 Q610 296 618 312 L630 292Z" fill="{BLOOD}" stroke="{INK}" stroke-width="2"/>',
           f'<path d="M638 274 h8 M654 274 h8 M650 278 l-3 8 h5 M642 292 q8 3 14 0" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    t.tegn(SU, f'<path d="M612 350 Q570 352 548 330" stroke="{INK}" stroke-width="16" stroke-linecap="round" fill="none"/>',
           f'<path d="M612 350 Q570 352 548 330" stroke="{MOSS}" stroke-width="10" stroke-linecap="round" fill="none"/>',
           f'<path d="M546 330 L500 276" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><path d="M496 272 q-12 -8 -4 -18 q12 2 10 16z" fill="{INK}"/>')
    t.tegn(LY, t.gloed(155, 380, 240, GOLD, 0.5))
    return t.svg()


# ====================================================================== Ulvehulen
@scene
def ulvehulen():
    t = Tegning("Ulvehulen under det væltede træ", 56)
    t.tegn(BG, t.himmel(MOSS, h=200, op=0.3))
    for x in range(100, 720, 40):
        t.tegn(BG, t.gran(x, 170, t.u(60, 110), op=0.6))
    t.tegn(BG, t.lag_land([(-10, 180), (400, 166), (810, 180)], 1, PAPER, kant=1.4))
    hule = Form("M-10 460 V170 Q120 100 400 110 Q680 100 810 170 V460 H700 Q690 260 400 236 Q110 260 100 460Z", (-10, 100, 810, 460))
    t.tegn(MG, t.sti(hule, SEPIA, None), t.tone(hule, 4, 50), t.sti(hule, "none", INK, 3))
    stamme = form([(-10, 120), (400, 86), (810, 116), (810, 150), (400, 120), (-10, 156)])
    t.tegn(MG, t.modelleret(stamme, el.TRAE, (0, 1), 3, bredde=2.6, vinkel=10))
    roedder = "".join(f'<path d="M{x} {118 + abs(x - 400) * 0.06:.0f} q{t.u(-12, 12):.0f} {t.u(30, 60):.0f} {t.u(-6, 6):.0f} {t.u(70, 140):.0f}" stroke="{INK}" stroke-width="{t.u(2.5, 5):.1f}" fill="none" stroke-linecap="round"/>' for x in range(150, 660, 40))
    t.tegn(MG, roedder)
    gulvf = Form("M100 460 Q110 360 400 340 Q690 360 700 460Z", (100, 340, 700, 460))
    t.tegn(MG, t.sti(gulvf, PAPER2, None), t.prikker(gulvf, 160, 1.1, op=0.6), t.tone(gulvf, 1, 10))
    t.tegn(SU, fg.placer(fg.ulv(snerren=False), 250, 418, 0.36), fg.placer(fg.ulv(snerren=False), 360, 430, 0.3, spejl=True),
           fg.placer(fg.ulv(snerren=False), 190, 438, 0.28))
    t.tegn(SU, f'<circle cx="520" cy="384" r="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><circle cx="515" cy="382" r="3" fill="{INK}"/><circle cx="525" cy="382" r="3" fill="{INK}"/>')
    brynje = form([(534, 392), (590, 388), (640, 408), (630, 426), (580, 414), (530, 406)])
    t.tegn(SU, t.sti(brynje, STEN, INK, 2), t.skraver(brynje, 45, 3, 0.9), t.skraver(brynje, -45, 3, 0.9))
    t.tegn(SU, f'<path d="M640 408 L680 402 M600 416 L604 438 M560 410 L556 436" stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>',
           f'<path d="M584 420 q10 -12 22 0 q-2 16 -22 0z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(LY, t.gloed(400, 380, 300, GOLD, 0.25))
    return t.svg()


# ====================================================================== Ravnens angreb
@scene
def ravnens_angreb():
    t = Tegning("Ravnen Korvus angriber", 92)
    t.tegn(BG, t.himmel(BLOOD, h=360, op=0.5), t.sky(160, 120, 230, 20), t.sky(640, 260, 200, 18))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 320, 300, 40), 1, PAPER2, kant=1.6))
    t.tegn(BG, f'<path d="M90 320 L104 200 H132 L146 320Z M96 200 H140 V186 H96Z" fill="{INK}" opacity=".8"/>', t.gloed(118, 240, 20, GOLD, 0.8))
    t.tegn(MG, t.lag_land([(-10, 360), (200, 336), (420, 352), (640, 340), (810, 356)], 2, SEPIA, kant=2.2))
    t.tegn(MG, t.graes(0, 800, 360, 80, 12, ybund=440))
    t.tegn(SU, fg.placer(fg.ravn_flyvende(), 500, 160, 0.95))
    t.tegn(SU, fg.placer(fg.vandrer(), 250, 360, 1.25))
    t.tegn(SU, t.gloed(244, 290, 40, ARCANE, 0.9), f'<circle cx="244" cy="290" r="7" fill="#cfe3f5" stroke="{INK}" stroke-width="2"/>')
    t.tegn(FG, t.lag_land([(-10, 430), (300, 418), (600, 436), (810, 420)], 3, SEPIA, kant=2), t.loevtrae(760, 440, 260, bar=True))
    for x, y, s in ((380, 60, 1), (660, 40, 0.8), (330, 110, 0.7)):
        t.tegn(FG, t.fugl(x, y, s))
    return t.svg()


# ====================================================================== Den mørke fremmede
@scene
def den_moerke_fremmede():
    t = Tegning("Den mørke fremmede i krohjørnet", 42)
    t.tegn(BG, stenvaeg(t, 450, fyld=PAPER2, morkhed=0.5))
    t.tegn(BG, t.planker(rect(-5, -5, W + 10, 60), "h", 18, el.TRAE))
    figur = form([(250, 330), (240, 200), (290, 110), (360, 70), (420, 66), (480, 74), (550, 110), (600, 200), (590, 330)])
    t.tegn(SU, t.sti(figur, INK, None), t.kantlys("M480 74 Q550 110 600 200 L590 330", GOLD, 2.2, 0.8))
    ansigt = form([(360, 150), (420, 118), (480, 150), (470, 220), (420, 238), (370, 220)])
    t.tegn(SU, t.sti(ansigt, "#1d1712", None))
    t.tegn(SU, f'<g fill="{GOLD}"><path d="M384 170 q10 -6 20 0 q-10 5 -20 0z M436 170 q10 -6 20 0 q-10 5 -20 0z"/></g>',
           f'<path d="M394 204 Q420 218 446 204" stroke="{PAPER}" stroke-width="2.2" fill="none" opacity=".7"/>')
    t.tegn(MG, t.planker(rect(-5, 320, W + 10, 140), "h", 22, el.TRAE))
    kort = form([(150, 340), (430, 336), (446, 410), (130, 418)])
    t.tegn(SU, t.sti(kort, PAPER, INK, 2.2), t.tone(kort, 1, 80, halv=(1, 0.3, 0.3)))
    t.tegn(SU, f'<path d="M270 400 L276 352 H292 L298 400Z M268 352 h32 v-8 h-32z" fill="{INK}"/>',
           f'<path d="M170 392 q40 -20 80 -6 t80 -10 q30 -8 60 6" stroke="{INK}" stroke-width="1.6" fill="none" stroke-dasharray="6 4"/>',
           f'<path d="M380 380 l8 -8 8 8 -8 8z" fill="{BLOOD}"/>')
    t.tegn(SU, f'<path d="M520 340 Q540 300 580 304" stroke="{INK}" stroke-width="26" stroke-linecap="round" fill="none"/>')
    t.tegn(SU, f'<path d="M560 336 v-48 q0 -8 8 -8 h34 q8 0 8 8 v48z" fill="{SEPIA}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(SU, f'<path d="M660 336 V280 H674 V336Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>', el.ild(t, 667, 280, 12, 22))
    t.tegn(FG, f'<path d="M-5 -5 H60 V455 H-5Z M740 -5 H805 V455 H740Z" fill="{INK}"/>')
    t.tegn(LY, t.gloed(667, 270, 260, GOLD, 0.5))
    return t.svg()


# ====================================================================== Skattekammeret
@scene
def skattekammeret():
    t = Tegning("Morvaks skattekammer", 87)
    t.tegn(BG, f'<rect width="800" height="450" fill="{INK}"/>')
    rum = Form("M40 460 V170 Q40 40 400 40 Q760 40 760 170 V460Z", (40, 40, 760, 460))
    t.tegn(MG, t.mur(rum, 22, (34, 60), morkhed=0.35))
    skjold = form([(160 + 58 * math.cos(a / 16 * 6.283), 190 + 58 * math.sin(a / 16 * 6.283)) for a in range(16)])
    t.tegn(MG, t.modelleret(skjold, MOSS, (1, 0.5), 3, bredde=3), f'<circle cx="160" cy="190" r="16" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>',
           f'<path d="M160 132 l-6 -14 h12z M218 190 l14 -6 v12z M102 190 l-14 -6 v12z M160 248 l-6 14 h12z" fill="{INK}"/>')
    for (x1, y1, x2, y2) in ((590, 110, 720, 270), (720, 110, 590, 270)):
        t.tegn(MG, f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M{x1} {y1} L{x2} {y2}" stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>')
    t.tegn(MG, el.fakkel(t, 470, 220, 50))
    for cx, cy, b in ((180, 460, 180), (620, 460, 170), (400, 470, 120)):
        bunke = form([(cx - b, cy), (cx - b * 0.6, cy - b * 0.35), (cx, cy - b * 0.55), (cx + b * 0.6, cy - b * 0.35), (cx + b, cy)])
        t.tegn(MG, t.modelleret(bunke, GOLD, (1, 0.4), 2, kerne=False, bredde=2.4))
        mont = "".join(f'<ellipse cx="{f(cx + t.u(-b * 0.7, b * 0.7))}" cy="{f(cy - t.u(5, b * 0.3))}" rx="9" ry="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>' for _ in range(16))
        t.tegn(MG, mont)
    kiste = rect(300, 330, 200, 80)
    laag = Form("M300 330 Q300 270 400 268 Q500 270 500 330Z", (300, 268, 500, 330))
    t.tegn(SU, t.planker(kiste, "v", 24, el.TRAE), t.planker(laag, "v", 24, el.TRAE),
           f'<path d="M300 352 H500 M332 330 V410 M468 330 V410 M336 280 V330 M464 280 V330" stroke="{INK}" stroke-width="6"/>',
           f'<path d="M388 346 h24 v24 h-24z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(FG, f'<path d="M-5 430 H805 V455 H-5Z" fill="{INK}"/>')
    t.tegn(LY, t.gloed(400, 380, 240, GOLD, 0.4), t.gloed(470, 140, 160, GOLD, 0.4))
    return t.svg()


# ====================================================================== Edderkoppekløften
@scene
def edderkoppekloeften():
    t = Tegning("Kæmpeedderkoppen i kløften", 32)
    t.tegn(BG, t.himmel(PAPER, h=450, op=0.6), t.straaler(400, -60, [82, 88, 94, 100], 520, 0.04, PAPER, 0.8))
    venstre = form([(-10, -10), (330, -10), (300, 80), (320, 160), (290, 240), (330, 320), (300, 400), (340, 460), (-10, 460)], blod=False)
    hoejre = form([(810, -10), (470, -10), (500, 90), (476, 170), (510, 250), (470, 330), (500, 400), (460, 460), (810, 460)], blod=False)
    t.tegn(MG, t.modelleret(venstre, SEPIA, (-1, 0.3), 3, bredde=3, vinkel=70), t.modelleret(hoejre, SEPIA, (1, 0.3), 4, bredde=3, vinkel=110))
    t.tegn(MG, f'<path d="M60 80 l60 20 l40 -10 M40 200 l90 -10 M80 320 l70 14 M700 100 l-70 16 M740 230 l-90 -6 M690 360 l-80 10" stroke="{INK}" stroke-width="2.4" fill="none"/>')
    t.tegn(MG, el.spind(330, 90, 70), el.spind(482, 300, 80), el.spind(120, 380, 60, 0.6))
    t.tegn(SU, fg.placer(fg.edderkop(), 400, 300, 1.0))
    t.tegn(SU, f'<path d="M610 100 V170" stroke="{INK}" stroke-width="2"/>')
    kokon = form([(592, 186), (610, 166), (628, 186), (632, 230), (610, 270), (588, 230)])
    t.tegn(SU, t.sti(kokon, PAPER, INK, 2.4), t.skraver(kokon, 20, 7, 1.2), t.skraver(kokon, -20, 9, 1, op=0.6))
    t.tegn(FG, t.lag_land([(-10, 420), (200, 404), (400, 430), (600, 408), (810, 420)], 4, INK, kant=2))
    t.tegn(FG, f'<circle cx="150" cy="418" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/><path d="M160 422 l30 4 M190 426 l16 -6" stroke="{PAPER}" stroke-width="3"/>')
    t.tegn(LY, t.gloed(400, 148, 40, BLOOD, 0.8))
    return t.svg()
