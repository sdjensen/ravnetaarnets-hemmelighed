"""Kapitel 2-scener (Skyggekongen), tegnet med kit.py i træsnits-/tuschstil."""
import math
from kit import (Tegning, Form, form, rect, glat, kantet, f, INK, PAPER, PAPER2, SEPIA, STEN,
                 GOLD, BLOOD, MOSS, ARCANE, W, H)
import figurer as fg
import elementer as el
from kap1 import stjerner, gulv, stenvaeg

S = {}
BG, MG, SU, FG, LY = "background", "midground-architecture", "subject", "foreground-framing", "lighting-overlay"
LILLA = "#5a3a6e"
LYSLILLA = "#c9a0dc"
ASKE = "#8a817a"
MOERK = "#2a2230"


def scene(fn):
    S[fn.__name__.replace("_", "-")] = fn
    return fn


def skygge(x, y, h, spejl=1, op=0.85):
    """Høj, spinkel skyggeskikkelse med lange fingre og røde øjne."""
    s = spejl
    d = (f"M{f(x - 18 * s)} {f(y)} Q{f(x - 24 * s)} {f(y - h * 0.5)} {f(x - 8 * s)} {f(y - h * 0.86)} "
         f"Q{f(x)} {f(y - h - 6)} {f(x + 12 * s)} {f(y - h * 0.86)} Q{f(x + 28 * s)} {f(y - h * 0.5)} {f(x + 20 * s)} {f(y)} "
         f"Q{f(x + 10 * s)} {f(y - 18)} {f(x)} {f(y - 4)} Q{f(x - 10 * s)} {f(y - 20)} {f(x - 18 * s)} {f(y)}Z")
    arme = ""
    for k in range(4):
        arme += f"M{f(x + 16 * s)} {f(y - h * 0.62)} q{f(28 * s)} {f(-10 + k * 8)} {f((44 + k * 4) * s)} {f(4 + k * 10)} "
    return (f'<g opacity="{op}"><path d="{d}" fill="{MOERK}"/><path d="{arme}" stroke="{MOERK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{f(x - 2 * s)}" cy="{f(y - h * 0.8)}" r="2.5" fill="{BLOOD}"/><circle cx="{f(x + 8 * s)}" cy="{f(y - h * 0.8)}" r="2.5" fill="{BLOOD}"/></g>')


def krage(x, y, s=1):
    return fg.placer(fg.ravn_siddende(), x, y, 0.5 * s)


def dvaerg_statue(t, x, y, s=1, spejl=False):
    sx = -s if spejl else s
    krop = Form("M-40 0 V-100 Q-40 -150 0 -154 Q40 -150 40 -100 V0Z", (-40, -154, 40, 0))
    hoved = form([(24 * math.cos(a / 12 * 6.283), -176 + 24 * math.sin(a / 12 * 6.283)) for a in range(12)])
    skaeg = Form("M-22 -168 Q0 -90 22 -168 Q10 -160 0 -160 Q-10 -160 -22 -168Z", (-22, -168, 22, -100))
    hjelm = Form("M-27 -184 Q0 -222 27 -184Z", (-27, -222, 27, -184))
    ud = t.modelleret(krop, STEN, (1, 0.3), 2, bredde=2.4) + t.modelleret(hoved, STEN, (1, 0.3), 2, kerne=False, bredde=2.2)
    ud += t.modelleret(skaeg, "#c8bca8", (1, 0.2), 1, kerne=False, bredde=2) + t.modelleret(hjelm, SEPIA, (1, 0.3), 2, kerne=False, bredde=2.2)
    ud += f'<path d="M-26 -194 Q-44 -204 -42 -226 Q-32 -210 -18 -204Z M26 -194 Q44 -204 42 -226 Q32 -210 18 -204Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    ud += f'<path d="M-10 -178 h6 M4 -178 h6 M-8 -150 v30 M0 -150 v40 M8 -150 v30" stroke="{INK}" stroke-width="1.8"/>'
    oekse = Form("M50 -210 Q90 -200 90 -170 Q90 -140 50 -134 Q64 -170 50 -210Z", (50, -210, 90, -134))
    ud += f'<path d="M50 -230 V0" stroke="{INK}" stroke-width="7"/>' + t.modelleret(oekse, STEN, (1, 0.2), 2, kerne=False, bredde=2.2)
    ud += f'<path d="M-50 10 H60 V0 H-50Z" fill="{INK}"/>'
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(s)})">{ud}</g>'


# ====================================================================== Månestenen i mørke
@scene
def maanesten_i_moerke():
    t = Tegning("Månestenen bliver sort", 101)
    t.tegn(BG, t.himmel(LILLA, h=360, op=0.55), stjerner(t, 18), el.halvmaane(t, 120, 80, 30))
    t.tegn(BG, t.sky(330, 90, 220, 20), t.sky(620, 130, 200, 18))
    t.tegn(BG, t.lag_land(t.kam(-10, 810, 290, 280, 40), 2, PAPER2, kant=1.4, op=0.8))
    for x in range(10, 800, 30):
        t.tegn(BG, t.gran(x, 300 + t.u(-6, 6), t.u(40, 70), op=0.55, lys=False))
    t.tegn(MG, t.lag_land([(-10, 340), (200, 322), (420, 330), (620, 316), (810, 332)], 2, PAPER2, kant=1.8))
    t.tegn(MG, el.hus(t, 50, 372, 140, 76, roeg=False), el.hus(t, 610, 376, 150, 80, roeg=False))
    hegn = ""
    for x in list(range(220, 320, 24)) + list(range(480, 580, 24)):
        hegn += f'<path d="M{x} 392 v-36" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    t.tegn(MG, hegn, f'<path d="M216 370 H324 M476 370 H584" stroke="{INK}" stroke-width="2.4"/>')
    t.tegn(MG, krage(244, 356), krage(296, 356, 0.9), krage(552, 356))
    t.tegn(SU, t.modelleret(rect(394, 236, 12, 190), el.TRAE, (1, 0), 2, kerne=False, bredde=2))
    t.tegn(SU, t.gloed(400, 250, 150, MOERK, 0.9), t.gloed(400, 250, 50, BLOOD, 0.5))
    t.tegn(SU, f'<path d="M372 250 Q400 212 428 250" stroke="{GOLD}" stroke-width="4" fill="none"/>',
           f'<circle cx="400" cy="256" r="20" fill="{MOERK}" stroke="{INK}" stroke-width="3"/><path d="M390 248 q10 -6 20 4" stroke="{BLOOD}" stroke-width="2" fill="none"/>')
    t.tegn(SU, skygge(190, 430, 140), skygge(640, 436, 150, -1), skygge(310, 440, 96), skygge(520, 444, 110, -1))
    t.tegn(FG, t.lag_land([(-10, 430), (300, 418), (520, 434), (810, 420)], 3, SEPIA, kant=2), t.graes(0, 800, 432, 70, 12))
    for cx, cy in ((84, 336), (646, 340)):
        t.tegn(LY, t.gloed(cx, cy, 36, GOLD, 0.6))
    return t.svg()


# ====================================================================== Heden
@scene
def heden():
    t = Tegning("Den øde hede med vejviseren", 102)
    t.tegn(BG, t.himmel(ASKE, h=300, op=0.5), t.sky(420, 70, 260, 22), t.sky(700, 110, 160, 16))
    bjerge = t.kam(-10, 360, 250, 240, 170, 0.55)
    t.tegn(BG, t.lag_land(bjerge, 2, PAPER, blod=False, kant=1.8, vinkel=60))
    ruin = "M560 262 V214 H576 V190 H592 V222 H612 V176 H622 V154 L630 140 L638 154 V206 H660 V196 H682 V262Z M690 262 V220 H708 V202 H720 V262Z"
    t.tegn(BG, f'<path d="{ruin}" fill="{INK}" opacity=".7"/>')
    t.tegn(MG, t.lag_land([(-10, 270), (200, 258), (400, 266), (600, 254), (810, 270)], 1, PAPER2, kant=1.8))
    lyng = "".join(f'<circle cx="{f(t.u(0, 800))}" cy="{f(t.u(290, 440))}" r="{f(t.u(1.5, 3.5))}"/>' for _ in range(220))
    t.tegn(MG, f'<g fill="{BLOOD}" opacity=".55">{lyng}</g>', t.graes(0, 800, 290, 140, 9, ybund=440))
    hoved_vej = t.sti_vej(404, 470, 404, 372, 170, 46, sving=0)
    t.tegn(MG, t.sti(hoved_vej, PAPER, INK, 1.6), t.prikker(hoved_vej, 40, 1, op=0.5))
    for d in ("M392 376 Q300 330 170 296", "M416 376 Q520 330 650 292", "M404 374 Q408 330 404 276"):
        t.tegn(MG, f'<path d="{d}" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="{d}" stroke="{PAPER}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    t.tegn(SU, t.modelleret(rect(396, 170, 14, 210), el.TRAE, (1, 0), 2, kerne=False, bredde=2.2))
    for (x1, y1, x2, retn) in ((410, 186, 494, 1), (396, 222, 316, -1), (410, 258, 480, 1)):
        pil = form([(x1, y1), (x2, y1), (x2 + 14 * retn, y1 + 13), (x2, y1 + 26), (x1, y1 + 26)], blod=False)
        t.tegn(SU, t.planker(pil, "h", 13, PAPER2), f'<path d="M{min(x1, x2) + 10} {y1 + 13} h{abs(x2 - x1) - 24}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 3"/>')
    t.tegn(SU, krage(404, 170, 1.3))
    t.tegn(SU, t.loevtrae(620, 300, 170, bar=True), krage(660, 196), krage(586, 214, 0.9), krage(626, 160, 0.9))
    t.tegn(FG, t.lag_land([(-10, 430), (260, 416), (520, 438), (810, 422)], 3, SEPIA, kant=2), t.graes(0, 800, 432, 60, 16))
    return t.svg()


# ====================================================================== Heksehytten
@scene
def heksehytten():
    t = Tegning("Heksens hytte på pæle over mosen", 104)
    t.tegn(BG, t.himmel(MOSS, h=330, op=0.45))
    for x in (40, 110, 680, 760):
        t.tegn(BG, t.loevtrae(x, 330, t.u(160, 220), bar=True))
    t.tegn(BG, t.taage(250, 90, 0.7))
    t.tegn(MG, f'<rect y="330" width="800" height="120" fill="{PAPER2}"/>', t.vand(0, 330, 800, 440))
    for x1, x2 in ((300, 320), (400, 396), (500, 480)):
        t.tegn(MG, t.modelleret(form([(x1 - 6, 420), (x2 - 5, 248), (x2 + 5, 248), (x1 + 6, 420)], blod=False), el.TRAE, (1, 0), 2, kerne=False, bredde=2))
    t.tegn(MG, f'<path d="M300 330 L500 340 M320 290 L480 300" stroke="{INK}" stroke-width="4"/>')
    vaeg = form([(280, 256), (520, 246), (510, 150), (290, 160)], blod=False)
    t.tegn(MG, t.planker(vaeg, "v", 26, el.TRAE))
    tag = form([(256, 172), (300, 90), (420, 36), (520, 76), (548, 166), (420, 148)])
    t.tegn(MG, t.sti(tag, SEPIA, None), t.skraver(tag, 80, 3.2, 1.2), t.skraver(tag, 20, 4, 1, halv=(1, 0.2, 0.1)), t.sti(tag, "none", INK, 2.4))
    t.tegn(MG, f'<path d="M470 74 V26 H492 V84" fill="{STEN}" stroke="{INK}" stroke-width="2"/>', el.damp(482, 24, 2, 40))
    t.tegn(MG, f'<path d="M330 246 V196 Q350 176 370 196 V246Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
           f'<path d="M440 210 h40 v-28 h-40z" fill="{MOSS}" stroke="{INK}" stroke-width="2.5"/><path d="M460 182 v28 M440 196 h40" stroke="{INK}" stroke-width="2"/>')
    t.tegn(MG, f'<g stroke="{INK}" stroke-width="3"><path d="M350 256 L340 400 M370 256 L362 400 M343 290 h22 M342 330 h22 M341 370 h22"/></g>')
    t.tegn(SU, fg.placer(fg.kappefigur(hat=True, kant=GOLD), 350, 246, 0.55))
    t.tegn(SU, el.ild(t, 600, 420, 60, 40), el.gryde(t, 600, 404, 80), el.damp(600, 370, 3, 60))
    t.tegn(SU, t.gloed(600, 380, 90, MOSS, 0.7))
    t.tegn(FG, t.lag_land([(-10, 430), (200, 420), (400, 440), (810, 426)], 3, SEPIA, kant=2))
    siv = "".join(f'<path d="M{x} 432 q{f(t.u(-5, 5))} -30 {f(t.u(-8, 8))} -{f(t.u(40, 90))}" stroke="{INK}" stroke-width="2.4" fill="none"/>' for x in list(range(10, 100, 8)) + list(range(700, 800, 8)))
    t.tegn(FG, siv)
    t.tegn(LY, t.gloed(350, 220, 70, GOLD, 0.6), t.gloed(460, 196, 50, MOSS, 0.6), t.taage(350, 50, 0.6))
    return t.svg()


# ====================================================================== Bjergpasset
@scene
def bjergpasset():
    t = Tegning("Det sneklædte bjergpas", 110)
    t.tegn(BG, t.himmel(ARCANE, h=300, op=0.45))
    for (x0, x1, y, amp, op) in ((-10, 500, 200, 220, 0.75), (300, 810, 210, 240, 0.85)):
        kam = t.kam(x0, x1, y, y + 10, amp, 0.52)
        t.tegn(BG, t.lag_land(kam, 1, PAPER, blod=False, kant=1.8, vinkel=60, op=op))
    for (x0, x1, y, amp) in ((-10, 420, 290, 110), (380, 810, 280, 120)):
        kam = t.kam(x0, x1, y, y, amp, 0.55)
        land = t.land(kam, blod=False)
        t.tegn(BG, t.sti(land, PAPER, None), t.tone(land, 2, 110, halv=(1, 0.2, 0.0)), f'<path d="{kantet(kam, False)}" fill="none" stroke="{INK}" stroke-width="2"/>')
    t.tegn(MG, t.lag_land([(-10, 320), (120, 300), (260, 336), (380, 330), (560, 300), (700, 280), (810, 290)], 3, SEPIA, kant=2.4, vinkel=40))
    sti = Form("M-10 360 Q200 330 380 352 Q520 368 700 330 L810 320 V350 Q620 380 470 386 Q260 396 -10 392Z", (-10, 320, 810, 396))
    t.tegn(MG, t.sti(sti, PAPER, INK, 2), t.prikker(sti, 80, 1.2, op=0.5))
    klippe = form([(-10, 330), (-10, 150), (40, 130), (110, 140), (150, 170), (170, 330)], blod=False)
    t.tegn(MG, t.modelleret(klippe, SEPIA, (1, 0.3), 3, bredde=2.4, vinkel=70))
    top = [(30 + i * 12, 150 + t.u(-6, 6)) for i in range(9)]
    bund = [(30 + i * 12, 300 + t.u(-20, 24)) for i in range(9)]
    is_fald = form(top + list(reversed(bund)))
    t.tegn(MG, t.sti(is_fald, "#c8dbe8", INK, 2), t.gloed(80, 230, 90, ARCANE, 0.45))
    t.tegn(MG, "".join(f'<path d="M{f(x)} {f(y0 + 6)} q{f(t.u(-4, 4))} {f((y1 - y0) * 0.5)} {f(t.u(-3, 3))} {f(y1 - y0 - 10)}" stroke="{ARCANE}" stroke-width="{f(t.u(1.2, 2.6))}" fill="none"/>' for (x, y0), (_, y1) in zip(top, bund)))
    t.tegn(MG, "".join(f'<path d="M{f(x - 3)} {f(y)} l3 {f(t.u(10, 22))} l3 -{f(t.u(10, 22))}" fill="#c8dbe8" stroke="{INK}" stroke-width="1.2"/>' for x, y in bund[1:-1]))
    hule = Form("M600 330 Q600 262 650 256 Q700 262 700 330Z", (600, 256, 700, 330))
    t.tegn(MG, t.sti(hule, INK, INK, 2.5))
    t.tegn(SU, fg.placer(fg.vandrer(sværd=False), 420, 372, 0.6))
    t.tegn(FG, t.lag_land([(-10, 430), (240, 412), (500, 440), (810, 418)], 4, INK, kant=2))
    sne = "".join(f'<circle cx="{f(t.u(20, 780))}" cy="{f(t.u(20, 420))}" r="{f(t.u(1.5, 3.5))}" fill="{PAPER}" stroke="{INK}" stroke-width=".7"/>' for _ in range(60))
    t.tegn(LY, sne)
    return t.svg()


# ====================================================================== Mineskakten
@scene
def mineskakten():
    t = Tegning("Den gamle dværgemine", 114)
    t.tegn(BG, f'<rect width="800" height="450" fill="#1d1712"/>')
    sten = Form("M-10 -10 H810 V460 H-10Z M322 271 V179 H478 V271Z", (-10, -10, 810, 460))
    t.tegn(BG, t.tone(Form("M-10 -10 H810 V460 H-10Z", (-10, -10, 810, 460)), 2, 30).replace(INK, SEPIA))
    for w, h, b in ((380, 230, 26), (280, 166, 20), (196, 116, 15), (134, 80, 11), (90, 54, 8)):
        venstre = rect(400 - w, 225 - h, b, h * 2)
        hoejre = rect(400 + w - b, 225 - h, b, h * 2)
        top = rect(400 - w, 225 - h, w * 2, b * 0.9)
        for p in (venstre, hoejre, top):
            t.tegn(MG, t.modelleret(p, el.TRAE, (1, 0.6), 2, kerne=False, bredde=2))
    t.tegn(MG, f'<path d="M322 271 V179 H478 V271Z" fill="{INK}"/>')
    t.tegn(MG, f'<path d="M290 460 L388 271 M510 460 L412 271" stroke="{STEN}" stroke-width="5"/><path d="M290 460 L388 271 M510 460 L412 271" stroke="{INK}" stroke-width="1.5"/>')
    sveller = "".join(f'<path d="M{f(400 - 120 * k)} {f(271 + 190 * k)} H{f(400 + 120 * k)}" stroke="{el.TRAE}" stroke-width="{f(3 + 6 * k)}"/>' for k in (0.15, 0.3, 0.5, 0.75, 1.0))
    t.tegn(MG, sveller)
    vogn = form([(520, 400), (540, 336), (690, 336), (710, 400)], blod=False)
    t.tegn(SU, t.planker(vogn, "v", 24, el.TRAE), f'<path d="M540 336 q30 -26 60 -6 q30 -20 60 -2 q20 -6 30 8z" fill="{STEN}" stroke="{INK}" stroke-width="2"/>')
    for cx in (560, 670):
        t.tegn(SU, f'<circle cx="{cx}" cy="410" r="16" fill="{INK}" stroke="{STEN}" stroke-width="4"/>')
    t.tegn(SU, f'<g fill="{GOLD}"><path d="M372 220 q4 -3 8 0 q-4 2 -8 0z M384 220 q4 -3 8 0 q-4 2 -8 0z M410 236 q4 -3 8 0 q-4 2 -8 0z M422 236 q4 -3 8 0 q-4 2 -8 0z"/></g>',
           t.gloed(398, 228, 40, GOLD, 0.4))
    t.tegn(FG, el.fakkel(t, 100, 360, 60))
    t.tegn(LY, t.gloed(100, 280, 260, GOLD, 0.45))
    return t.svg()


# ====================================================================== Dværgeporten
@scene
def dvaergeporten():
    t = Tegning("Dværgeporten i Jernbjerget", 116)
    klippe = Form("M-10 -10 H810 V460 H-10Z", (-10, -10, 810, 460))
    t.tegn(BG, t.sti(klippe, SEPIA, None), t.tone(klippe, 2, 70))
    revner = "".join(f'<path d="M{f(t.u(0, 800))} {f(t.u(0, 420))} l{f(t.u(-40, 40))} {f(t.u(20, 60))} l{f(t.u(-30, 30))} {f(t.u(20, 50))}" stroke="{INK}" stroke-width="2.4" fill="none"/>' for _ in range(14))
    t.tegn(BG, revner)
    ramme = el.bue(250, 412, 300, 360)
    t.tegn(MG, t.modelleret(ramme, STEN, (1, 0.3), 2, bredde=3))
    port = el.bue(276, 412, 248, 330)
    t.tegn(MG, t.planker(port, "v", 31, "#4a3a28"), f'<path d="M400 82 V412" stroke="{INK}" stroke-width="6"/>',
           f'<path d="M276 200 H524 M276 300 H524" stroke="{INK}" stroke-width="6"/>',
           f'<circle cx="380" cy="300" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="2"/><circle cx="420" cy="300" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>')
    t.tegn(MG, f'<g stroke="{GOLD}" stroke-width="3.2" fill="none" stroke-linecap="round"><path d="M330 140 l10 -16 10 16 M372 122 v20 l10 -10 M418 124 l10 18 l10 -18 M458 140 l10 -16 l6 16"/>'
               f'<path d="M320 250 h20 M330 240 v20 M460 250 l12 -10 l0 20 M360 172 l8 8 -8 8 M432 172 l-8 8 8 8"/></g>', t.gloed(400, 180, 160, GOLD, 0.35))
    for i, (x0, w) in enumerate(((210, 380), (230, 340))):
        trin = rect(x0, 412 + i * 18, w, 18)
        t.tegn(MG, t.modelleret(trin, STEN, (1, 0.5), 1, kerne=False, bredde=2))
    t.tegn(SU, dvaerg_statue(t, 150, 420, 1.0), dvaerg_statue(t, 650, 420, 1.0, spejl=True))
    t.tegn(FG, f'<path d="M-10 -10 H70 Q50 200 80 460 H-10Z M810 -10 H730 Q750 220 720 460 H810Z" fill="{INK}"/>')
    return t.svg()


# ====================================================================== Dværgesmedjen
@scene
def dvaergesmedjen():
    t = Tegning("Smedjen dybt inde i Jernbjerget", 118)
    t.tegn(BG, stenvaeg(t, 450, fyld=STEN, morkhed=0.5))
    esse = rect(480, 150, 310, 300)
    t.tegn(MG, t.mur(esse, 22, (28, 50), morkhed=0.4), f'<path d="M560 150 V40 H620 V150Z" fill="{INK}"/>')
    aab = el.bue(520, 452, 230, 200)
    t.tegn(MG, t.sti(aab, INK, INK, 2), el.ild(t, 635, 452, 200, 150))
    vaerktoej = ""
    for x, h in ((60, 110), (90, 130), (120, 100)):
        vaerktoej += f'<path d="M{x} 60 V{60 + h}" stroke="{el.TRAE}" stroke-width="6"/><path d="M{x - 10} {60 + h} h20 v14 h-20z" fill="{INK}"/>'
    t.tegn(MG, vaerktoej, el.kaede(170, 40, 170, 180, 12))
    ambolt = Form("M240 380 H400 L380 352 H300 Q250 352 228 366 Q232 376 240 380Z", (228, 352, 400, 380))
    t.tegn(SU, t.modelleret(ambolt, STEN, (1, 0.5), 3, bredde=2.6),
           t.modelleret(form([(290, 380), (350, 380), (360, 452), (280, 452)], blod=False), STEN, (1, 0.3), 3, bredde=2.4))
    t.tegn(SU, f'<path d="M320 352 H380 V344 H320Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>', t.gloed(350, 346, 60, GOLD, 0.8))
    # dværgesmeden
    krop = form([(120, 452), (116, 360), (136, 316), (180, 300), (224, 316), (240, 360), (236, 452)])
    t.tegn(SU, t.modelleret(krop, el.TRAE, (-1, 0.3), 3, bredde=2.6))
    hoved = form([(178 + 30 * math.cos(a / 12 * 6.283), 272 + 30 * math.sin(a / 12 * 6.283)) for a in range(12)])
    t.tegn(SU, t.modelleret(hoved, PAPER2, (-1, 0.3), 2, kerne=False, bredde=2.4))
    skaeg = Form("M150 284 Q178 404 206 284 Q196 296 178 300 Q160 296 150 284Z", (150, 284, 206, 404))
    t.tegn(SU, t.modelleret(skaeg, PAPER, (-1, 0.2), 1, kerne=False, bredde=2.2),
           f'<path d="M162 300 q6 40 4 80 M178 300 v90 M194 300 q-6 40 -4 80" stroke="{INK}" stroke-width="1.4" fill="none"/>',
           f'<path d="M148 262 Q178 226 208 262 Q192 252 178 252 Q164 252 148 262Z" fill="{INK}"/><path d="M162 266 h12 M182 266 h12" stroke="{INK}" stroke-width="3.4"/>'
           f'<circle cx="169" cy="273" r="2.2" fill="{INK}"/><circle cx="187" cy="273" r="2.2" fill="{INK}"/><path d="M178 270 q6 10 0 16 q-4 0 -6 -2" stroke="{INK}" stroke-width="2" fill="none"/>')
    t.tegn(SU, f'<path d="M224 320 L296 262" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>',
           f'<path d="M296 262 L344 316" stroke="{el.TRAE}" stroke-width="7"/>',
           t.modelleret(form([(282, 232), (322, 266), (310, 282), (270, 248)], blod=False), STEN, (1, 0.3), 2, kerne=False, bredde=2.2))
    gnister = "".join(f'<circle cx="{f(350 + t.u(-60, 60))}" cy="{f(330 - t.u(0, 90))}" r="{f(t.u(1, 2.6))}"/>' for _ in range(24))
    t.tegn(LY, f'<g fill="{GOLD}">{gnister}</g>', t.gloed(635, 390, 300, GOLD, 0.5))
    return t.svg()


# ====================================================================== Askeborg
def ruin(t, x, b, h, y=430):
    pts = [(x, y), (x, y - h)]
    n = 6
    for i in range(1, n):
        pts.append((x + b * i / n, y - h * t.u(0.55, 1.0)))
    pts += [(x + b, y - h * t.u(0.5, 0.9)), (x + b, y)]
    fm = form(pts, blod=False)
    ud = t.mur(fm, 18, (24, 42), morkhed=0.3)
    for _ in range(2):
        vx = x + t.u(b * 0.15, b * 0.6)
        vy = y - h * t.u(0.3, 0.5)
        ud += t.sti(el.bue(vx, vy, b * 0.22, h * 0.25), INK, INK, 2)
    return ud


@scene
def askeborg():
    t = Tegning("Ruinbyen Askeborg", 120)
    t.tegn(BG, t.himmel(ASKE, h=330, op=0.55), t.gloed(610, 170, 160, LILLA, 0.7))
    t.tegn(BG, f'<path d="M560 230 L580 140 L590 160 L600 90 L612 160 L626 124 L640 230Z M520 236 Q580 206 660 236Z" fill="{INK}"/>',
           f'<g fill="{LYSLILLA}"><rect x="594" y="150" width="6" height="10"/><rect x="616" y="170" width="6" height="10"/></g>')
    t.tegn(BG, t.lag_land([(-10, 280), (300, 270), (500, 276), (810, 268)], 1, ASKE, kant=1.4, op=0.8))
    t.tegn(MG, ruin(t, 0, 220, 250), ruin(t, 580, 220, 230))
    bue = Form("M290 430 V300 Q290 200 400 200 Q510 200 510 300 V430 H470 V300 Q470 240 400 240 Q330 240 330 300 V430Z", (290, 200, 510, 430))
    t.tegn(MG, t.mur(bue, 18, (20, 36), morkhed=0.3))
    t.tegn(SU, skygge(370, 420, 110), skygge(446, 414, 90, -1), skygge(250, 440, 70))
    t.tegn(SU, krage(110, 186), krage(690, 206, 0.9))
    jord = t.land([(-10, 420), (200, 408), (400, 428), (600, 410), (810, 422)])
    t.tegn(FG, t.sti(jord, ASKE, None), t.prikker(jord, 200, 1.2, op=0.6), t.tone(jord, 1, 10), t.sti(jord, "none", INK, 2))
    t.tegn(FG, t.sten(90, 430, 30, fyld=ASKE), t.sten(640, 426, 26, fyld=ASKE))
    t.tegn(LY, t.taage(370, 50, 0.6, ASKE))
    return t.svg()


# ====================================================================== Kloakken
@scene
def kloakken():
    t = Tegning("Kloakormen under Askeborg", 125)
    t.tegn(BG, f'<rect width="800" height="450" fill="{INK}"/>')
    hvaelv = Form("M60 460 V200 Q60 50 400 50 Q740 50 740 200 V460Z", (60, 50, 740, 460))
    t.tegn(MG, t.mur(hvaelv, 20, (30, 54), fyld=SEPIA, morkhed=0.5))
    t.tegn(MG, t.sti(Form("M300 460 V260 Q300 200 400 200 Q500 200 500 260 V460Z", (300, 200, 500, 460)), INK, INK, 2))
    vand = rect(60, 360, 680, 100)
    t.tegn(MG, t.sti(vand, MOSS, None, op=0.85), t.vand(60, 362, 740, 450, 1.3))
    t.tegn(MG, t.modelleret(rect(60, 340, 220, 20), STEN, (0, 1), 1, kerne=False), t.modelleret(rect(520, 340, 220, 20), STEN, (0, 1), 1, kerne=False))
    ormen = []
    for i in range(9):
        a = i / 8
        cx = 400 + math.sin(a * 2.4) * 70
        cy = 400 - a * 170
        r = 40 - a * 12
        ormen.append((cx, cy, r))
    for cx, cy, r in ormen:
        seg = form([(cx + r * math.cos(k / 12 * 6.283), cy + r * 0.75 * math.sin(k / 12 * 6.283)) for k in range(12)])
        t.tegn(SU, t.modelleret(seg, ASKE, (1, 0.4), 2, kerne=True, bredde=2.2))
    hx, hy, _ = ormen[-1]
    t.tegn(SU, f'<circle cx="{f(hx + 14)}" cy="{f(hy - 4)}" r="20" fill="{BLOOD}" stroke="{INK}" stroke-width="2.4"/>',
           f'<g fill="{PAPER}"><path d="M{f(hx + 2)} {f(hy - 12)} l4 -9 4 9z M{f(hx + 14)} {f(hy - 18)} l4 -9 4 9z M{f(hx + 26)} {f(hy - 10)} l9 -2 -7 7z M{f(hx + 4)} {f(hy + 8)} l2 9 5 -9z"/></g>')
    for x in (130, 610):
        t.tegn(SU, f'<path d="M{x} 340 q10 -14 24 -8 q8 4 12 8 z M{x} 338 q-16 2 -26 10" fill="{INK}" stroke="{INK}" stroke-width="2"/><circle cx="{x + 28}" cy="334" r="1.6" fill="{BLOOD}"/>')
    t.tegn(FG, f'<path d="M-5 -5 H60 V455 H-5Z M740 -5 H805 V455 H740Z" fill="{INK}"/>')
    t.tegn(LY, f'<path d="M340 50 L300 360 H500 L460 50Z" fill="{PAPER}" opacity=".15"/>')
    return t.svg()


# ====================================================================== Spøgelsespigen
@scene
def spoegelsespigen():
    t = Tegning("Spøgelsespigen Ylva i ruinerne", 128)
    t.tegn(BG, t.himmel(ASKE, h=330, op=0.5), t.lag_land([(-10, 300), (400, 290), (810, 302)], 1, ASKE, kant=1.4, op=0.7))
    t.tegn(MG, ruin(t, -10, 220, 330, 440), ruin(t, 590, 220, 320, 440))
    gade = t.sti_vej(400, 470, 400, 300, 440, 120, sving=0)
    t.tegn(MG, t.sti(gade, STEN, INK, 2))
    brosten = ""
    for r in range(8):
        y = 300 + r * 20 + r * r * 1.2
        b = 120 + (440 - 120) * (y - 300) / 170
        x = 400 - b / 2
        while x < 400 + b / 2:
            w = t.u(14, 26) * (0.5 + (y - 300) / 170)
            brosten += f'<path d="M{f(x)} {f(y)} h{f(w - 2)}" stroke="{INK}" stroke-width="1.2"/>'
            x += w
    t.tegn(MG, brosten)
    t.tegn(SU, t.gloed(400, 330, 130, ARCANE, 0.7))
    ylva = form([(370, 420), (376, 350), (388, 322), (412, 322), (424, 350), (430, 420), (418, 410), (408, 422), (398, 408), (388, 422), (378, 410)])
    t.tegn(SU, t.sti(ylva, PAPER, ARCANE, 2.4, op=0.85), t.skraver(ylva, 80, 6, 1, farve=ARCANE, op=0.4))
    hoved = form([(400 + 18 * math.cos(a / 12 * 6.283), 302 + 20 * math.sin(a / 12 * 6.283)) for a in range(12)])
    t.tegn(SU, t.sti(hoved, PAPER, ARCANE, 2.4, op=0.9), f'<path d="M384 290 l8 -12 8 8 8 -8 8 12" stroke="{GOLD}" stroke-width="2.6" fill="none"/>',
           f'<circle cx="394" cy="302" r="2.2" fill="{ARCANE}"/><circle cx="406" cy="302" r="2.2" fill="{ARCANE}"/>',
           f'<path d="M424 350 Q450 340 470 312" stroke="{ARCANE}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    t.tegn(SU, f'<path d="M470 312 V292" stroke="{INK}" stroke-width="2"/><path d="M462 292 h16 v22 h-16z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/><path d="M460 292 l10 -8 10 8z" fill="{INK}"/>',
           t.gloed(470, 304, 50, GOLD, 0.7))
    t.tegn(FG, t.sten(120, 440, 34, fyld=ASKE), t.sten(690, 444, 30, fyld=ASKE))
    return t.svg()


# ====================================================================== Skyggeborgen
@scene
def skyggeborgen():
    t = Tegning("Skyggeborgen", 130)
    t.tegn(BG, t.himmel(LILLA, h=450, op=0.55))
    for rx, ry, op in ((180, 70, 0.6), (270, 104, 0.5), (360, 136, 0.4)):
        t.tegn(BG, f'<ellipse cx="400" cy="120" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="2.2" opacity="{op}" stroke-dasharray="40 14"/>')
    borg = ("M220 300 V200 L240 160 L260 200 V220 H300 V140 L330 60 L360 140 V220 H440 V140 L470 60 L500 140 V220 H540 V200 L560 160 L580 200 V300Z")
    fm = Form(borg, (220, 60, 580, 300))
    t.tegn(MG, t.sti(fm, "#1d1712", None), t.skraver(fm, 80, 5, 1, farve=LYSLILLA, op=0.25, halv=(-1, 0, 0.2)), t.sti(fm, "none", INK, 2.4))
    t.tegn(MG, f'<g fill="{LYSLILLA}"><rect x="322" y="150" width="10" height="18"/><rect x="462" y="150" width="10" height="18"/><rect x="236" y="230" width="8" height="14"/><rect x="556" y="230" width="8" height="14"/><rect x="326" y="196" width="8" height="14"/><rect x="466" y="196" width="8" height="14"/></g>')
    t.tegn(MG, f'<path d="M360 300 V252 Q400 216 440 252 V300Z" fill="{LILLA}" stroke="{INK}" stroke-width="2"/>')
    trappe = form([(370, 300), (430, 300), (470, 460), (330, 460)], blod=False)
    t.tegn(MG, t.sti(trappe, ASKE, INK, 2))
    t.tegn(MG, "".join(f'<path d="M{f(370 - k * 40)} {f(300 + k * 160)} H{f(430 + k * 40)}" stroke="{INK}" stroke-width="1.8"/>' for k in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9)))
    for side in ((-10, 460, 260, 300), (810, 460, 540, 300)):
        x0, y0, x1, y1 = side
        kloft = form([(x0, y0), (x0, y1 + 10), (x1 - (40 if x1 < 400 else -40), y1 + 20), (x1, y0)], blod=False)
        t.tegn(MG, t.sti(kloft, INK, INK, 2))
    t.tegn(SU, fg.placer(fg.vandrer(sværd=False, kant=LYSLILLA), 400, 440, 0.45))
    t.tegn(SU, krage(330, 62, 1.4), krage(470, 60, 1.4))
    for x, y in ((120, 100), (680, 80)):
        t.tegn(SU, t.fugl(x, y, 1.2))
    t.tegn(LY, t.gloed(400, 260, 160, LILLA, 0.7), t.gloed(327, 160, 30, LYSLILLA, 0.6), t.gloed(467, 160, 30, LYSLILLA, 0.6))
    return t.svg()


# ====================================================================== Tronsalen
@scene
def tronsalen():
    t = Tegning("Skyggekongen Vardrak i tronsalen", 136)
    t.tegn(BG, stenvaeg(t, 450, fyld=ASKE, morkhed=0.55))
    for x in (90, 210, 590, 710):
        soejle = rect(x - 24, 100, 48, 350)
        t.tegn(MG, t.modelleret(soejle, STEN, (1 if x > 400 else -1, 0.2), 3, bredde=2.4, vinkel=85),
               f'<path d="M{x - 32} 100 H{x + 32} V84 H{x - 32}Z M{x - 32} 450 H{x + 32} V436 H{x - 32}Z" fill="{INK}"/>')
    tæppe = form([(320, 460), (372, 320), (428, 320), (480, 460)], blod=False)
    t.tegn(MG, t.sti(tæppe, BLOOD, INK, 2), t.skraver(tæppe, 90, 8, 1, op=0.5), f'<path d="M340 460 L380 322 M460 460 L420 322" stroke="{GOLD}" stroke-width="2"/>')
    t.tegn(MG, t.modelleret(rect(330, 300, 140, 22), STEN, (1, 0.5), 2, kerne=False), t.modelleret(rect(344, 282, 112, 20), STEN, (1, 0.5), 2, kerne=False))
    trone = form([(330, 282), (330, 100), (360, 56), (400, 88), (440, 56), (470, 100), (470, 282)], blod=False)
    t.tegn(SU, t.gloed(400, 150, 150, LILLA, 0.9), t.sti(trone, INK, INK, 2), t.kantlys(trone.d, LYSLILLA, 2.4, 0.7))
    t.tegn(SU, f'<path d="M384 150 L400 116 L416 150 L400 184Z" fill="#e8c8f0" stroke="{LILLA}" stroke-width="3"/>', t.gloed(400, 150, 60, "#e8c8f0", 0.8))
    vardrak = Form("M354 282 Q350 220 366 196 Q384 176 400 176 Q416 176 434 196 Q450 220 446 282Z", (350, 176, 450, 282))
    t.tegn(SU, t.sti(vardrak, "#1d1712", LYSLILLA, 2.4), f'<circle cx="400" cy="198" r="18" fill="#1d1712" stroke="{LYSLILLA}" stroke-width="2.4"/>',
           f'<path d="M380 190 L374 156 L386 178 L392 146 L400 176 L408 146 L414 178 L426 156 L420 190Z" fill="{INK}" stroke="{LYSLILLA}" stroke-width="2.4"/>',
           f'<g fill="#e8c8f0"><path d="M390 198 q4 -3 8 0 q-4 2 -8 0z M402 198 q4 -3 8 0 q-4 2 -8 0z"/></g>',
           f'<path d="M446 236 L500 226 M500 150 V320" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M490 150 L500 120 L510 150Z" fill="{INK}"/>')
    t.tegn(SU, skygge(250, 440, 120), skygge(550, 440, 120, -1), skygge(160, 450, 90), skygge(640, 450, 90, -1))
    t.tegn(FG, f'<path d="M-5 432 H805 V455 H-5Z" fill="{INK}"/>')
    return t.svg()


# ====================================================================== Lysets sejr
@scene
def lysets_sejr():
    t = Tegning("Månestenen lyser igen over Vildmose", 150)
    t.tegn(BG, t.himmel(ARCANE, h=360, op=0.55), stjerner(t, 20), el.maane(t, 690, 70, 30))
    t.tegn(BG, t.straaler(400, 220, list(range(180, 361, 15)), 520, 0.03, "#cfe3f5", 0.9))
    t.tegn(BG, t.lag_land([(-10, 320), (200, 300), (400, 312), (600, 296), (810, 314)], 2, SEPIA, kant=2))
    t.tegn(MG, el.hus(t, 30, 338, 130, 70), el.hus(t, 640, 334, 130, 72), el.hus(t, 190, 330, 90, 50, skorsten=False), el.hus(t, 520, 330, 90, 50, skorsten=False))
    lygter = ""
    for i, x in enumerate(range(150, 660, 70)):
        y = 250 + 14 * math.sin(i * 1.3) + abs(x - 400) * -0.03
        lygter += f'<circle cx="{x}" cy="{f(y)}" r="7" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>' + t.gloed(x, y, 24, GOLD, 0.6)
    t.tegn(MG, f'<path d="M120 244 Q260 274 400 256 Q540 274 680 244" stroke="{INK}" stroke-width="1.6" fill="none"/>', lygter)
    t.tegn(SU, t.modelleret(rect(395, 226, 10, 110), el.TRAE, (1, 0), 2, kerne=False, bredde=2))
    t.tegn(SU, t.gloed(400, 216, 170, "#cfe3f5", 0.9), f'<path d="M380 230 Q400 198 420 230" stroke="{GOLD}" stroke-width="3" fill="none"/>',
           f'<circle cx="400" cy="216" r="16" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>')
    for x, y, s, sp in ((250, 340, 0.62, False), (320, 346, 0.6, True), (480, 346, 0.6, False), (550, 340, 0.62, True)):
        t.tegn(SU, fg.placer(fg.kappefigur(kant="#cfe3f5"), x, y, s, spejl=sp),
               f'<path d="M{x - 8} {y - 40} L{x - 30} {y - 70} M{x + 8} {y - 40} L{x + 30} {y - 72}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    t.tegn(FG, t.lag_land([(-10, 420), (300, 404), (520, 418), (810, 402)], 3, SEPIA, kant=2), t.graes(0, 800, 418, 60, 12))
    for cx, cy in ((56, 316), (666, 312)):
        t.tegn(LY, t.gloed(cx, cy, 30, GOLD, 0.6))
    return t.svg()
