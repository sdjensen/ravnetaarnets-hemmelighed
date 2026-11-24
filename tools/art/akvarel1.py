"""Kapitel 1 malet i blød akvarel-/Bob Ross-stil."""
import math
from akvarel_vaerk import *  # noqa: F401,F403
from akvarel_vaerk import Billede, f
import figurer as fg

S = {}


def scene(fn):
    S[fn.__name__.replace("_", "-")] = fn
    return fn


# ====================================================================== Vildmose
@scene
def vildmose_landsby():
    b = Billede("Landsbyen Vildmose i måneskin", 1)
    b.mal(b.himmel([(0, NAT), (0.45, PRUSSIAN), (0.8, "#8f8fb8"), (1, "#d9c3b8")]), b.stjerner(50), b.maane(640, 90, 34))
    b.mal(b.skyer([(200, 120, 260, "#8f97c4", .5), (480, 70, 200, "#b8b0cc", .45)]))
    b.mal(b.bjerge(250, 240, 90, "#5d6a98", sne="#e8e6f0", taage="#b8b4cc"))
    b.mal(b.skovrand(300, hmin=24, hmax=50, mork="#1f3040", lys="#4f6a78", taet=12))
    b.mal(b.bakke([(-10, 330), (200, 312), (420, 322), (620, 306), (810, 320)], top="#4f6a5a", bund="#1f3326", gtop="#8aa08a"))
    b.mal(b.hytte(80, 368, 130, 70), b.hytte(310, 342, 100, 54, skorsten=False), b.hytte(570, 376, 150, 80))
    b.mal(b.sti([(300, 460), (380, 330), (400, 326), (520, 460)], "#c8b896"))
    hegn = "".join(f'<path d="M{x} {f(398 + (x - 230) * 0.1)} v-34" stroke="{VANDYKE}" stroke-width="4" stroke-linecap="round"/>' for x in range(230, 330, 22))
    b.mal(f'<g filter="url(#pensel)">{hegn}<path d="M226 378 L332 386 M226 366 L332 374" stroke="{VANDYKE}" stroke-width="2.4"/></g>')
    b.mal(b.figur(fg.kappefigur(kant="#f4cf8a"), 470, 404, 0.9), f'<path d="M490 330 L494 404" stroke="{VANDYKE}" stroke-width="3.5"/>',
          b.lys(497, 340, 50, "#ffd77a", 0.9), f'<rect x="489" y="332" width="14" height="16" fill="{GUL}" filter="url(#pensel)"/>')
    b.mal(b.loevtrae(40, 450, 320, bar=True, stamme=PLUM), b.buske([(720, 430, 40), (640, 440, 28), (160, 440, 30)], ("#1f3326", "#3f5a46", "#7f9a7a")))
    b.mal(b.graes(0, 800, 410, 450, 200, "#8aa08a", 10))
    return b.svg()


# ====================================================================== Kroen
@scene
def den_sorte_gryde():
    b = Billede("Kroen Den Sorte Gryde", 41)
    b.mal(b.interioer())
    b.mal(b.kasse(-5, -5, 810, 42, VANDYKE), b.kasse(110, 37, 26, 365, BRUN), b.kasse(420, 37, 26, 365, BRUN))
    urter = "".join(f'<path d="M{x} 40 v{14 + i % 2 * 8}" stroke="{VANDYKE}" stroke-width="1.5"/><path d="M{x - 9} {54 + i % 2 * 8} q9 -6 18 0 l-9 {40 + i % 3 * 6}z" fill="{SAP}"/>' for i, x in enumerate(range(170, 380, 34)))
    b.mal(f'<g filter="url(#pensel)">{urter}</g>')
    b.mal(b.kasse(160, 196, 230, 12, BRUN))
    flasker = "".join(f'<path d="M{x} 196 v-26 q0 -8 6 -12 v-10 h6 v10 q6 4 6 12 v26z" fill="{(SAP, ALIZARIN, BRUN, PHTHALO)[i % 4]}"/>' for i, x in enumerate(range(176, 380, 30)))
    b.mal(f'<g filter="url(#pensel)">{flasker}</g>', f'<path d="M300 40 V96" stroke="{VANDYKE}" stroke-width="2"/>',
          f'<path d="M286 96 h28 l-4 34 h-20z" fill="{GUL}" filter="url(#pensel)"/>', b.lys(300, 114, 110, "#ffd77a", 0.7))
    b.mal(b.kasse(520, 150, 270, 260, LYSSTEN), b.bue(560, 410, 190, 200, PLUM), b.ild(655, 410, 130, 90))
    b.mal(f'<path d="M607 330 Q607 370 655 372 Q703 370 703 330Z" fill="{PLUM}" filter="url(#pensel)"/>', b.kaede(655, 230, 655, 330))
    b.mal(b.gulv(404), b.bord(170, 330, 300))
    b.mal(b.kasse(250, 296, 30, 34, BRUN), f'<path d="M280 304 q14 0 14 12 q0 10 -14 10" fill="none" stroke="{VANDYKE}" stroke-width="3"/>')
    b.mal(f'<g filter="url(#pensel)"><rect x="340" y="314" width="16" height="16" rx="2" fill="{HVID}" transform="rotate(12 348 322)"/><rect x="372" y="318" width="16" height="16" rx="2" fill="{HVID}" transform="rotate(-8 380 326)"/></g>')
    b.mal(b.figur(fg.kappefigur(kant=GUL), 120, 452, 1.55, farve="#3a2a3a"),
          f'<path d="M108 312 q6 -4 12 0 M128 312 q6 -4 12 0" stroke="{GUL}" stroke-width="2.4" fill="none"/>')
    b.mal(b.figur(fg.kappefigur(kant=ILD), 500, 452, 1.15, spejl=True, farve="#5a3a3a"))
    b.mal(b.lys(655, 360, 260, "#ffcf7a", 0.45), b.morke_hjoerner(0.6))
    return b.svg()


# ====================================================================== Gråskoven
@scene
def graaskoven():
    b = Billede("Gråskoven", 24)
    b.mal(b.himmel([(0, "#9fb0a0"), (0.6, "#d8dcc0"), (1, "#c9c8a0")]))
    b.mal(b.lys(420, 60, 300, "#fff4cf", 0.8))
    for i in range(16):
        x = 30 + i * 50 + b.u(-15, 15)
        b.mal(f'<g opacity="{f(b.u(0.25, 0.4))}" filter="url(#vask)">{b.gran(x, 330, b.u(170, 250), "#6a7a6a", "#9aaa8a")}</g>')
    b.mal(b.taage(220, 120, "#e8e4c8"))
    for x, y, h in ((150, 340, 240), (270, 336, 180), (530, 340, 250), (660, 332, 200), (380, 326, 140)):
        b.mal(b.loevtrae(x, y, h, farver=("#2f4a32", "#5f8a4a", "#a8c27a")))
    b.mal(b.bakke([(-10, 340), (200, 326), (400, 334), (600, 322), (810, 336)], top="#7a9a5a", bund="#2f4a2c"))
    b.mal(b.sti([(300, 460), (396, 336), (414, 336), (560, 460)], "#d8c094"))
    rays = "".join(f'<path d="M{f(380 + i * 22)} -10 L{f(300 + i * 40)} 460 L{f(340 + i * 40)} 460 L{f(396 + i * 22)} -10Z" fill="#fff4cf" opacity=".18"/>' for i in range(4))
    b.mal(f'<g filter="url(#vask)">{rays}</g>')
    b.mal(b.loevtrae(620, 392, 230, farver=("#2a4030", "#4f7a3c", "#9cbb6a")))
    b.mal(b.figur(fg.gammel_mand(kant=GUL), 572, 394, 0.95, spejl=True, farve="#4a3a3a"))
    for x, bb in ((40, 74), (765, 84)):
        stamme = f"M{f(x - bb / 2)} -10 H{f(x + bb / 2)} L{f(x + bb * 0.45)} 300 L{f(x + bb * 0.75)} 460 L{f(x - bb * 0.75)} 460 L{f(x - bb * 0.45)} 300Z"
        b.mal(f'<path d="{stamme}" fill="{b.lin([(0, VANDYKE), (1, BRUN)], 1, 0)}" filter="url(#akvarel)"/>')
    b.mal(b.buske([(110, 440, 40), (200, 450, 30), (680, 440, 40), (600, 452, 26)]), b.graes(0, 800, 400, 450, 220, LYSGRON, 9))
    return b.svg()


# ====================================================================== Stencirklen
@scene
def stencirklen():
    b = Billede("Stencirklen med sværdet i stenen", 30)
    b.mal(b.himmel([(0, "#3d5a8a"), (0.5, "#9ab0c8"), (1, "#e8e0c8")]))
    b.mal(b.skovrand(250, hmin=110, hmax=170, mork="#2a4038", lys="#5f7a5a", taet=24, op=0.9))
    b.mal(b.taage(180, 90, "#e8e6d8"))
    b.mal(b.bakke([(-10, 260), (200, 250), (400, 256), (600, 248), (810, 260)], top="#8aaa6a", bund="#3a5a32"))
    for x, y, bb, h in ((110, 360, 70, 150), (230, 312, 52, 112), (338, 290, 40, 82), (462, 290, 40, 82), (570, 312, 52, 112), (690, 360, 70, 150)):
        pts = [(x - bb / 2, y), (x - bb * 0.45, y - h * 0.7), (x - bb * 0.2, y - h), (x + bb * 0.25, y - h * 0.94), (x + bb * 0.5, y - h * 0.6), (x + bb / 2, y)]
        d = "M" + " L".join(f"{f(px + b.u(-3, 3))} {f(py + b.u(-3, 3))}" for px, py in pts) + "Z"
        lys = b.lin([(0, LYSSTEN), (1, "#6a6470")], 1 if x < 400 else -1, 0) if x < 400 else b.lin([(0, "#6a6470"), (1, LYSSTEN)], 1, 0)
        b.mal(f'<path d="{d}" fill="{lys}" filter="url(#akvarel)"/>',
              f'<path d="M{f(x - bb / 2)} {f(y)} q{f(bb * 0.25)} -18 {f(bb * 0.55)} -6 q-8 8 -{f(bb * 0.55)} 6z" fill="{SAP}" filter="url(#pensel)"/>')
    b.mal(f'<path d="M330 392 L346 344 H454 L470 392Z" fill="{b.lin([(0, LYSSTEN), (1, STEN)])}" filter="url(#akvarel)"/>')
    b.mal(b.lys(400, 250, 180, MAGI, 0.7), b.lys(400, 250, 60, "#ffffff", 0.8))
    b.mal(f'<g filter="url(#pensel)"><path d="M394 344 V220 L400 206 L406 220 V344Z" fill="#eef4f8"/><path d="M376 222 H424 V230 H376Z M396 222 V186 H404 V222Z" fill="{PLUM}"/><circle cx="400" cy="180" r="8" fill="{GUL}"/></g>')
    b.mal(b.graes(0, 800, 290, 440, 260, "#b5c86a", 9))
    b.mal(b.graner([(20, 470, 380, 160), (790, 470, 400, 170)]))
    return b.svg()


# ====================================================================== Ulvene
@scene
def ulvene():
    b = Billede("Ulvene i Gråskoven", 52)
    b.mal(b.himmel([(0, "#3a2a4a"), (0.5, "#8a5a6a"), (1, "#e0a888")]), b.maane(650, 70, 24, "#fde8c8"))
    b.mal(b.skovrand(280, hmin=160, hmax=250, mork="#1a2420", lys="#3a4a40", taet=22, op=0.95))
    b.mal(b.skovrand(300, hmin=90, hmax=140, mork="#141c18", lys="#34443a", taet=28, op=1))
    b.mal(b.lys(630, 230, 30, "#ffd77a", 0.9))
    b.mal(b.bakke([(-10, 330), (200, 316), (400, 326), (600, 312), (810, 328)], top="#6a7a5a", bund="#2a3426", gtop="#a0a888"))
    b.mal(b.figur(fg.ulv(), 220, 404, 0.78, farve="#3a3440"), b.figur(fg.ulv(), 600, 410, 0.66, spejl=True, farve="#4a4250"))
    torn = ""
    for sx, retn in ((0, 1), (800, -1)):
        for k in range(3):
            y0 = 380 + k * 22
            torn += f"M{sx} {y0} Q{sx + retn * 100} {y0 - 70} {sx + retn * 210} {y0 - 10} "
    b.mal(f'<path d="{torn}" stroke="{VANDYKE}" stroke-width="3.5" fill="none" stroke-linecap="round" filter="url(#pensel)"/>')
    b.mal(b.lys(400, 340, 320, "#c05050", 0.25), b.graes(0, 800, 400, 450, 160, "#b0a878", 10))
    return b.svg()


# ====================================================================== Floden
@scene
def soelvaa_faergen():
    b = Billede("Færgemanden ved floden Sølvå", 9)
    H = 230
    b.mal(b.himmel([(0, "#5f86c0"), (0.6, "#bcd0e0"), (1, "#f4e0b8")]))
    b.mal(b.skyer([(180, 80, 260, HVID, .9), (600, 60, 220, "#f8e8d8", .8), (420, 140, 180, HVID, .6)]))
    land = b.bjerge(190, 180, 70, "#7a8ab8", taage="#e8e4d8") + b.skovrand(H, hmin=30, hmax=70, mork="#2a4a3a", lys="#7a9a6a", taet=14)
    b.mal(f'<g id="landskab">{land}</g>', b.soe(H, "landskab", [(0, "#e0e4d8"), (0.4, "#8aa8c8"), (1, "#3d5a7a")]))
    b.mal(f'<path d="M240 318 H560 L530 344 H270Z" fill="{b.lin([(0, BRUN), (1, VANDYKE)])}" filter="url(#akvarel)"/>')
    b.mal(b.figur(fg.kappefigur(kant=HVID), 450, 318, 1.15, farve="#3a3048"))
    b.mal(f'<path d="M380 120 L600 400" stroke="{VANDYKE}" stroke-width="6" stroke-linecap="round" filter="url(#pensel)"/>')
    b.mal(f'<path d="M300 318 V278" stroke="{VANDYKE}" stroke-width="3"/><rect x="290" y="252" width="20" height="26" fill="{GUL}" filter="url(#pensel)"/>', b.lys(300, 265, 60, "#ffe7a0", 0.8))
    b.mal(b.land([(-10, 405), (200, 396), (400, 414), (600, 400), (810, 408)], b.lin([(0, "#6a8a4a"), (1, "#2f4a2c")])))
    b.mal(b.siv(10, 140, 424), b.siv(660, 800, 424), b.buske([(80, 420, 30), (720, 418, 34)]))
    return b.svg()


# ====================================================================== Troldebroen
@scene
def troldebroen():
    b = Billede("Trolden på stenbroen", 21)
    b.mal(b.himmel([(0, "#4f6fa8"), (0.6, "#c8d4e0"), (1, "#f0e4c8")]), b.skyer([(600, 70, 260, HVID, .85), (180, 110, 200, HVID, .7)]))
    b.mal(b.bjerge(200, 190, 70, "#7a8ab8", taage="#e8e4d8"), b.skovrand(226, hmin=30, hmax=60, taet=16))
    b.mal(b.soe(300, None, [(0, "#a8c0d0"), (1, "#3d5a7a")]))
    bro = "M-10 214 H810 V344 H650 Q646 262 400 258 Q154 262 150 344 H-10Z"
    b.mal(f'<path d="{bro}" fill="{b.lin([(0, LYSSTEN), (1, STEN)])}" filter="url(#akvarel)"/>')
    sten = ""
    for r in range(7):
        y = 222 + r * 18
        x = -10 - (r % 2) * 20
        while x < 810:
            w = b.u(30, 50)
            sten += f'<rect x="{f(x + 2)}" y="{f(y)}" width="{f(w - 4)}" height="14" rx="4" fill="{b.r.choice(("#b8ab98", "#a89a88", "#c8bca8"))}" opacity=".6"/>'
            x += w
    b.mal(f'<g filter="url(#akvarel)" clip-path="url(#brok)">{sten}</g>')
    b.defs.append(f'<clipPath id="brok"><path d="{bro}"/></clipPath>')
    b.mal(f'<path d="M150 344 Q154 262 400 258 Q646 262 650 344Z" fill="{b.lin([(0, "#2a2a3a"), (1, "#4a5a6a")])}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M-10 206 H810 V222 H-10Z" fill="{LYSSTEN}" filter="url(#akvarel)"/>')
    b.mal(b.figur(fg.trold(fyld="#6b6a52"), 560, 214, 1.05, farve="#4a4a3a"))
    b.mal(f'<path d="M646 200 Q690 180 712 140" stroke="#6b6a52" stroke-width="22" fill="none" stroke-linecap="round" filter="url(#pensel)"/>',
          f'<path d="M700 156 L738 52 Q756 34 774 58 L726 166Z" fill="{BRUN}" filter="url(#akvarel)"/>')
    b.mal(b.land([(-10, 420), (160, 406), (300, 440), (320, 460)], b.lin([(0, SAP), (1, MORKGRON)])),
          b.land([(480, 460), (560, 420), (700, 404), (810, 412)], b.lin([(0, SAP), (1, MORKGRON)])))
    b.mal(b.buske([(110, 420, 34), (700, 410, 40)]), b.graes(0, 260, 420, 450, 60, LYSGRON), b.graes(560, 800, 410, 450, 60, LYSGRON))
    return b.svg()


# ====================================================================== Ravnesumpen
@scene
def ravnesumpen():
    b = Billede("Ravnesumpen med de blå lys", 55)
    H = 280
    b.mal(b.himmel([(0, "#3a4a6a"), (0.6, "#9aa8b8"), (1, "#d8dcd0")]))
    land = f'<path d="M560 {H} L574 100 H622 L636 {H}Z M566 100 H628 V82 H566Z" fill="#3a3a4a" opacity=".7" filter="url(#akvarel)"/>'
    land += b.skovrand(H, hmin=20, hmax=40, mork="#3a4a4a", lys="#6a7a6a", taet=14, op=0.7)
    for x, h in ((110, 200), (250, 160), (470, 190), (660, 230), (740, 140)):
        birk = f'<path d="M{x - 5} {H + 120} L{x - 3} {H + 120 - h} L{x + 3} {H + 120 - h} L{x + 5} {H + 120}Z" fill="#ece6dc"/>'
        birk += "".join(f'<path d="M{x - 5} {f(H + 120 - h * b.u(0.05, 0.95))} h{f(b.u(4, 9))}" stroke="{PLUM}" stroke-width="{f(b.u(2, 4))}"/>' for _ in range(6))
        birk += f'<path d="M{x} {f(H + 120 - h * 0.7)} q20 -14 36 -10 M{x} {f(H + 120 - h * 0.8)} q-16 -12 -30 -6" stroke="{PLUM}" stroke-width="2.5" fill="none"/>'
        land += f'<g filter="url(#pensel)">{birk}</g>'
    b.mal(f'<g id="land">{land}</g>', b.soe(H + 120, "land", [(0, "#a8b4b8"), (1, "#3a4a5a")], spejlop=0.4))
    b.mal(b.taage(H - 60, 100, "#e0e4e0"), f'<rect x="0" y="{H}" width="800" height="120" fill="#c8d0c8" opacity=".55" filter="url(#vask)"/>')
    b.mal(b.taage(H + 20, 80, "#e8ecea", 0.8))
    for x, y, h in ((110, 400, 220), (250, 400, 170), (470, 400, 200), (660, 400, 240)):
        birk = f'<path d="M{x - 6} {y} L{x - 3} {y - h} L{x + 3} {y - h} L{x + 6} {y}Z" fill="#f2ece2"/>'
        birk += "".join(f'<path d="M{x - 6} {f(y - h * b.u(0.05, 0.95))} h{f(b.u(5, 10))}" stroke="{PLUM}" stroke-width="{f(b.u(2, 4))}"/>' for _ in range(7))
        birk += f'<path d="M{x} {f(y - h * 0.7)} q22 -14 40 -10 M{x} {f(y - h * 0.82)} q-18 -12 -32 -6" stroke="{PLUM}" stroke-width="3" fill="none"/>'
        b.mal(f'<g filter="url(#pensel)">{birk}</g>')
    for cx, cy in ((330, 252), (400, 230), (560, 272), (300, 302), (620, 220)):
        b.mal(b.lys(cx, cy, 40, MAGI, 0.95), f'<circle cx="{cx}" cy="{cy}" r="4" fill="#ffffff"/>')
    b.mal(b.siv(0, 120, 440), b.siv(680, 800, 440))
    return b.svg()


# ====================================================================== Kælderen
@scene
def kaelderen():
    b = Billede("Fangen i tårnets kælder", 68)
    b.mal(b.interioer(("#9a8a7a", "#4a3a30"), tone=("#8a7a6a", "#7a6a5a", "#a09080", "#6a5a4a")))
    b.mal(f'<rect x="340" y="20" width="120" height="50" fill="{PLUM}" filter="url(#pensel)"/>',
          f'<path d="M362 20 V70 M386 20 V70 M410 20 V70 M434 20 V70" stroke="{STEN}" stroke-width="5" filter="url(#pensel)"/>')
    b.mal(f'<path d="M340 70 L230 420 H570 L460 70Z" fill="#fff4dc" opacity=".35" filter="url(#vask)"/>')
    b.mal(b.gulv(412, "#7a6a50"), b.graes(150, 650, 412, 430, 120, OKKER, 6))
    b.mal(b.kaede(340, 190, 362, 300), b.kaede(460, 190, 438, 300))
    b.mal(b.figur(fg.kappefigur(kant=HVID), 400, 414, 1.25, farve="#5a4a5a"))
    b.mal(f'<path d="M366 300 L384 330 M434 300 L416 330" stroke="#5a4a5a" stroke-width="9" stroke-linecap="round" filter="url(#pensel)"/>')
    for x in (130, 640):
        b.mal(f'<path d="M{x} 404 q10 -14 24 -8 q8 4 12 8z M{x} 402 q-16 2 -26 10" fill="{PLUM}" stroke="{PLUM}" stroke-width="2" filter="url(#pensel)"/><circle cx="{x + 28}" cy="398" r="1.8" fill="{BLOD}"/>')
    b.mal(b.lys(400, 330, 200, "#fff4dc", 0.35), b.morke_hjoerner(0.85, "#1a1410"))
    return b.svg()


# ====================================================================== Skeletvagten
@scene
def skeletvagten():
    b = Billede("Skeletvagten på vindeltrappen", 66)
    b.mal(b.interioer(("#c8a880", "#6a5040")))
    b.mal(b.bue(210, 460, 380, 430, "#2a2030"))
    for i in range(7):
        y = 450 - i * 30
        x0 = 230 + i * 34
        b.mal(b.kasse(x0, y - 30, 560 - x0, 30, b.lin([(0, LYSSTEN), (1, STEN)]), op=0.95))
    b.mal(b.fakkel(130, 250), b.lys(130, 170, 260, "#ffcf7a", 0.5))
    b.mal(b.figur(fg.skelet(), 406, 360, 0.9, farve="#3a2a2a"))
    b.mal(b.lys(408, 228, 30, BLOD, 0.6), b.morke_hjoerner(0.7))
    return b.svg()


# ====================================================================== Morvaks kammer
@scene
def morvaks_kammer():
    b = Billede("Troldmanden Morvaks kammer", 29)
    b.mal(b.interioer(("#b8a0a8", "#5a4a5a"), tone=("#a890a0", "#9a8292", "#b8a0b0", "#8a7484")))
    b.mal(b.vindue(310, 30, 180, 180, (PRUSSIAN, "#7a8ac0"), PLUM, rund=True), b.maane(430, 100, 20))
    b.mal(b.reol(20, 40, 160, 370), b.reol(620, 40, 160, 370))
    b.mal(b.gulv(410, "#6a4a40"))
    b.mal(f'<path d="M190 420 V250 Q190 214 214 214 H316 Q340 214 340 250 V420Z" fill="{b.lin([(0, ALIZARIN), (1, BLOD)])}" filter="url(#akvarel)"/>')
    b.mal(b.figur(fg.kappefigur(hat=True, kant=MAGI), 266, 404, 1.45, farve="#2e2a4a"))
    b.mal(f'<path d="M248 290 q18 60 36 0 q-6 60 -18 80 q-12 -20 -18 -80z" fill="{HVID}" filter="url(#pensel)"/>')
    b.mal(b.bord(420, 330, 180, "#6a4a3a"))
    b.mal(b.lys(510, 314, 140, MAGI, 0.9), f'<circle cx="510" cy="314" r="12" fill="#e0f0ff" filter="url(#pensel)"/>',
          f'<path d="M490 330 q20 -36 40 0" stroke="{GUL}" stroke-width="3" fill="none"/>')
    b.mal(f'<rect x="570" y="292" width="12" height="38" fill="{HVID}" filter="url(#pensel)"/>', b.ild(576, 292, 10, 18))
    b.mal(b.figur(fg.ravn_siddende(), 700, 40, 0.8, spejl=True))
    b.mal(b.morke_hjoerner(0.6, "#1a1426"))
    return b.svg()


# ====================================================================== Hjemkomsten
@scene
def hjemkomsten():
    b = Billede("Hjemkomsten til Vildmose", 100)
    b.mal(b.himmel([(0, "#6a8ac0"), (0.45, "#f0b8a0"), (0.75, "#fcd88a"), (1, "#fff0c8")]))
    b.mal(b.lys(400, 300, 300, "#fff4c0", 1), f'<circle cx="400" cy="300" r="70" fill="#fff8d8" filter="url(#gloed)"/>')
    b.mal(b.skyer([(170, 160, 240, "#f8c8b0", .8), (640, 140, 260, "#f8d8c0", .8), (420, 80, 200, "#e8b8c0", .6)]))
    b.mal(b.bjerge(270, 260, 60, "#9a8ab8", taage="#fce4c0"))
    b.mal(b.bakke([(-10, 330), (200, 300), (400, 318), (600, 296), (810, 316)], top="#8aaa5a", bund="#3a5a32"))
    b.mal(b.hytte(70, 340, 120, 64), b.hytte(600, 330, 130, 70), b.hytte(230, 326, 80, 46, skorsten=False))
    b.mal(b.figur(fg.vandrer(sværd=False, kant=GUL), 360, 318, 0.9, farve="#3a2a3a"), b.figur(fg.kappefigur(kant=GUL), 450, 318, 0.82, farve="#5a3a4a"))
    b.mal(f'<path d="M402 318 V236 H410 V318Z" fill="{VANDYKE}" filter="url(#pensel)"/>', b.lys(406, 228, 60, MAGI, 0.9),
          f'<circle cx="406" cy="228" r="11" fill="#e0f0ff" filter="url(#pensel)"/>')
    b.mal(b.land([(-10, 420), (300, 404), (520, 420), (810, 400)], b.lin([(0, SAP), (1, MORKGRON)])), b.graes(0, 800, 405, 450, 200, LYSGRON, 12))
    b.mal(b.buske([(60, 420, 36), (740, 404, 40)]), b.fugle([(140, 90, 1.4), (180, 70, 1), (620, 60, 1.2), (660, 86, 0.9)]))
    return b.svg()


# ====================================================================== Værkstedet
@scene
def alkymistvaerkstedet():
    b = Billede("Troldmandens værksted med nissen i buret", 46)
    b.mal(b.interioer(("#c8b8a0", "#6a5a50")))
    b.mal(b.bue(40, 270, 110, 200, b.lin([(0, PRUSSIAN), (1, HIMMELBLAA)])), b.maane(104, 120, 12))
    b.mal(f'<path d="M95 70 V270 M40 170 H150" stroke="{VANDYKE}" stroke-width="5" filter="url(#pensel)"/>')
    for y in (120, 210):
        b.mal(b.kasse(440, y, 340, 12, BRUN))
    for i, x in enumerate(range(462, 770, 44)):
        b.mal(b.kolbe(x, 104, 9 + i % 3 * 3, (SAP, PHTHALO, ALIZARIN, GUL)[i % 4]))
    b.mal(b.kasse(574, 162, 26, 48, ALIZARIN), b.bord(200, 330, 560))
    b.mal(b.kolbe(300, 300, 24, SAP), b.kolbe(420, 306, 18, PHTHALO), b.kolbe(660, 298, 26, ALIZARIN))
    b.mal(f'<path d="M300 258 Q320 200 380 210 Q420 220 420 270 M660 252 Q680 220 720 240 L730 300" stroke="#8a8a90" stroke-width="4" fill="none" filter="url(#pensel)"/>')
    b.mal(f'<path d="M250 0 V44" stroke="{VANDYKE}" stroke-width="3"/>', b.lys(250, 140, 120, LYSGRON, 0.6))
    b.mal(f'<g filter="url(#pensel)">{fg.placer(fg.nisse(), 250, 150, 1.0)}</g>'.replace("#0d0b09", PLUM))
    b.mal(f'<g stroke="#5a4a3a" stroke-width="3" fill="none" filter="url(#pensel)"><path d="M190 190 V90 Q190 40 250 40 Q310 40 310 90 V190"/>'
          f'<path d="M210 190 V64 M230 190 V48 M250 190 V44 M270 190 V48 M290 190 V64"/><path d="M186 190 H314 M190 110 H310" stroke-width="5"/></g>')
    b.mal(b.morke_hjoerner(0.55))
    return b.svg()


# ====================================================================== Marnas hytte
@scene
def marnas_hytte():
    b = Billede("Fiskerkonen Marnas hytte", 19)
    b.mal(b.interioer(("#c8a070", "#6a4a30"), sten=False))
    planker = "".join(f"M{x} 0 V420 " for x in range(0, 800, 32))
    b.mal(f'<path d="{planker}" stroke="{VANDYKE}" stroke-width="2" opacity=".5" filter="url(#pensel)"/>')
    b.mal(b.vindue(600, 80, 120, 100, (HIMMELBLAA, "#b8d0e0")))
    net = "".join(f"M{380 + i * 12} 30 L{420 + i * 6} 170 " for i in range(16)) + "".join(f"M{380 + j * 3} {30 + j * 10} H{560 - j * 3} " for j in range(14))
    b.mal(f'<path d="{net}" stroke="{VANDYKE}" stroke-width="1.2" opacity=".7" filter="url(#pensel)"/>')
    fisk = "".join(f'<path d="M{x} 30 v20" stroke="{VANDYKE}" stroke-width="1.5"/><path d="M{x - 8} 50 q8 -6 16 0 q-2 22 -8 42 q-6 -20 -8 -42z" fill="{LYSSTEN}"/>' for x in (230, 270, 310))
    b.mal(f'<g filter="url(#pensel)">{fisk}</g>')
    b.mal(b.kasse(30, 170, 250, 250, LYSSTEN), b.bue(70, 420, 170, 170, PLUM), b.ild(155, 420, 120, 80))
    b.mal(f'<path d="M110 340 Q110 380 155 382 Q200 380 200 340Z" fill="{PLUM}" filter="url(#pensel)"/>', b.kaede(155, 230, 155, 340))
    b.mal(b.gulv(416), b.bord(330, 360, 220))
    b.mal(f'<path d="M400 360 Q430 336 460 360Z" fill="{HVID}" filter="url(#pensel)"/>',
          f'<path d="M418 336 c-6 -10 6 -18 0 -30 M434 332 c-6 -10 6 -18 0 -30" stroke="{HVID}" stroke-width="3" fill="none" opacity=".7" filter="url(#vask)"/>')
    b.mal(f'<path d="M590 452 L594 380 L606 330 L624 306 L660 300 L690 314 L706 352 L714 452Z" fill="{b.lin([(0, "#4f7a5a"), (1, "#2f4a3a")])}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M624 340 L676 338 L690 452 L612 452Z" fill="{HVID}" opacity=".9" filter="url(#akvarel)"/>')
    b.mal(f'<circle cx="650" cy="272" r="25" fill="#f0c8a8" filter="url(#akvarel)"/>',
          f'<path d="M624 270 Q622 236 650 232 Q680 236 678 270 Q666 252 650 252 Q634 252 624 270Z" fill="{ALIZARIN}" filter="url(#pensel)"/>',
          f'<path d="M640 274 h6 M656 274 h6 M644 290 q6 3 12 0" stroke="{VANDYKE}" stroke-width="2" fill="none" filter="url(#pensel)"/>')
    b.mal(f'<path d="M612 350 Q570 352 548 330" stroke="#3f6a4a" stroke-width="13" stroke-linecap="round" fill="none" filter="url(#pensel)"/>',
          f'<path d="M546 330 L500 276" stroke="{VANDYKE}" stroke-width="4" stroke-linecap="round"/>')
    b.mal(b.lys(155, 380, 260, "#ffcf7a", 0.5), b.morke_hjoerner(0.55))
    return b.svg()


# ====================================================================== Ulvehulen
@scene
def ulvehulen():
    b = Billede("Ulvehulen under det væltede træ", 56)
    b.mal(b.himmel([(0, "#8ab0c0"), (1, "#e8e4c8")], 260))
    b.mal(b.skovrand(200, hmin=60, hmax=110, mork="#2a4a3a", lys="#7a9a6a", taet=18, op=0.8))
    b.mal(b.bakke([(-10, 210), (400, 196), (810, 210)], top="#8aaa6a", bund="#5a7a4a", graes=False))
    hule = "M-10 460 V170 Q120 100 400 110 Q680 100 810 170 V460 H700 Q690 260 400 236 Q110 260 100 460Z"
    b.mal(f'<path d="{hule}" fill="{b.lin([(0, "#4a3a2a"), (1, "#2a1e16")])}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M-10 120 L400 86 L810 116 V150 L400 120 L-10 156Z" fill="{b.lin([(0, BRUN), (1, VANDYKE)])}" filter="url(#akvarel)"/>')
    roedder = "".join(f'<path d="M{x} {f(118 + abs(x - 400) * 0.06)} q{f(b.u(-12, 12))} {f(b.u(30, 60))} {f(b.u(-6, 6))} {f(b.u(70, 140))}" stroke="{VANDYKE}" stroke-width="{f(b.u(2.5, 5))}" fill="none" stroke-linecap="round"/>' for x in range(150, 660, 40))
    b.mal(f'<g filter="url(#pensel)">{roedder}</g>')
    b.mal(f'<path d="M100 460 Q110 360 400 340 Q690 360 700 460Z" fill="{b.lin([(0, OKKER), (1, BRUN)])}" filter="url(#akvarel)"/>')
    b.mal(b.lys(400, 300, 320, "#fff0c8", 0.35))
    b.mal(b.figur(fg.ulv(snerren=False), 250, 418, 0.36, farve="#6a6070"), b.figur(fg.ulv(snerren=False), 360, 430, 0.3, spejl=True, farve="#7a7080"),
          b.figur(fg.ulv(snerren=False), 190, 438, 0.28, farve="#5a5060"))
    b.mal(f'<circle cx="520" cy="384" r="14" fill="{HVID}" filter="url(#pensel)"/><circle cx="515" cy="382" r="3" fill="{PLUM}"/><circle cx="525" cy="382" r="3" fill="{PLUM}"/>',
          f'<path d="M534 392 L590 388 L640 408 L630 426 L580 414 L530 406Z" fill="#9aa0a8" filter="url(#akvarel)"/>',
          f'<path d="M584 420 q10 -12 22 0 q-2 16 -22 0z" fill="{GUL}" filter="url(#pensel)"/>')
    return b.svg()


# ====================================================================== Ravnens angreb
@scene
def ravnens_angreb():
    b = Billede("Ravnen Korvus angriber", 92)
    b.mal(b.himmel([(0, "#4a3a6a"), (0.45, "#c06a70"), (0.8, "#f4b880"), (1, "#fce0b0")]))
    b.mal(b.lys(600, 300, 260, "#ffd8a0", 0.8), b.skyer([(160, 120, 260, "#e8a0a0", .7), (640, 260, 220, "#f8c8a0", .7), (450, 70, 200, "#a07090", .6)]))
    b.mal(b.bjerge(320, 300, 50, "#7a6a9a", sne=None, taage="#f8d0a8"))
    b.mal(f'<path d="M90 320 L104 200 H132 L146 320Z M96 200 H140 V186 H96Z" fill="#3a2a40" opacity=".8" filter="url(#akvarel)"/>', b.lys(118, 240, 20, GUL, 0.9))
    b.mal(b.bakke([(-10, 360), (200, 336), (420, 352), (640, 340), (810, 356)], top="#8a8a5a", bund="#3a4a2a"))
    b.mal(b.figur(fg.ravn_flyvende(), 500, 160, 0.95, farve="#1e1826"))
    b.mal(b.figur(fg.vandrer(kant=GUL), 250, 360, 1.25, farve="#2e2436"))
    b.mal(b.lys(244, 290, 50, MAGI, 0.9), f'<circle cx="244" cy="290" r="7" fill="#e0f0ff"/>')
    b.mal(b.land([(-10, 430), (300, 418), (600, 436), (810, 420)], b.lin([(0, "#5a6a3a"), (1, "#2a3420")])),
          b.loevtrae(760, 440, 260, bar=True, stamme=PLUM), b.graes(0, 800, 420, 450, 160, "#c8c080", 12))
    return b.svg()


# ====================================================================== Den mørke fremmede
@scene
def den_moerke_fremmede():
    b = Billede("Den mørke fremmede i krohjørnet", 42)
    b.mal(b.interioer(("#b89a78", "#5a4232")), b.kasse(-5, -5, 810, 60, VANDYKE))
    b.mal(f'<path d="M250 330 L240 200 L290 110 L360 70 L420 66 L480 74 L550 110 L600 200 L590 330Z" fill="{b.lin([(0, "#3a3040"), (1, "#1e1a24")])}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M480 74 L550 110 L600 200 L590 330" stroke="{ILD}" stroke-width="4" fill="none" opacity=".6" filter="url(#vask)"/>')
    b.mal(f'<path d="M360 150 L420 118 L480 150 L470 220 L420 238 L370 220Z" fill="#14101a" filter="url(#akvarel)"/>')
    b.mal(f'<g fill="{GUL}" filter="url(#pensel)"><path d="M384 170 q10 -6 20 0 q-10 5 -20 0z M436 170 q10 -6 20 0 q-10 5 -20 0z"/></g>', b.lys(420, 170, 50, GUL, 0.4),
          f'<path d="M394 204 Q420 218 446 204" stroke="#f0d8b0" stroke-width="2.2" fill="none" opacity=".7"/>')
    b.mal(b.gulv(320, BRUN))
    b.mal(f'<path d="M150 340 L430 336 L446 410 L130 418Z" fill="#f0e2c0" filter="url(#akvarel)"/>',
          f'<g filter="url(#pensel)"><path d="M270 400 L276 352 H292 L298 400Z M268 352 h32 v-8 h-32z" fill="{PLUM}"/>'
          f'<path d="M170 392 q40 -20 80 -6 t80 -10 q30 -8 60 6" stroke="{ALIZARIN}" stroke-width="2" fill="none" stroke-dasharray="6 4"/></g>')
    b.mal(f'<path d="M520 340 Q540 300 580 304" stroke="#2a2430" stroke-width="26" stroke-linecap="round" fill="none" filter="url(#pensel)"/>')
    b.mal(b.kasse(560, 288, 50, 48, BRUN), f'<rect x="660" y="280" width="14" height="56" fill="{HVID}" filter="url(#pensel)"/>', b.ild(667, 280, 12, 22))
    b.mal(b.lys(667, 270, 300, "#ffcf7a", 0.5), b.morke_hjoerner(0.7))
    return b.svg()


# ====================================================================== Skattekammeret
@scene
def skattekammeret():
    b = Billede("Morvaks skattekammer", 87)
    b.mal(b.interioer(("#b8a080", "#5a4632")))
    b.mal(f'<circle cx="160" cy="190" r="58" fill="{b.rad(140, 170, 80, [(0, "#7aa06a"), (1, "#2f4a32")])}" filter="url(#akvarel)"/>',
          f'<circle cx="160" cy="190" r="16" fill="{GUL}" filter="url(#pensel)"/>')
    for (x1, y1, x2, y2) in ((590, 110, 720, 270), (720, 110, 590, 270)):
        b.mal(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#d8dce0" stroke-width="6" stroke-linecap="round" filter="url(#pensel)"/>')
    b.mal(b.fakkel(470, 220, 50), b.lys(470, 150, 200, "#ffcf7a", 0.5))
    for cx, cy, bb in ((180, 460, 180), (620, 460, 170), (400, 470, 120)):
        b.mal(f'<path d="M{cx - bb} {cy} Q{cx - bb * 0.6} {cy - bb * 0.4} {cx} {cy - bb * 0.55} Q{cx + bb * 0.6} {cy - bb * 0.4} {cx + bb} {cy}Z" fill="{b.lin([(0, "#fce08a"), (1, "#c8902a")])}" filter="url(#akvarel)"/>')
        mont = "".join(f'<ellipse cx="{f(cx + b.u(-bb * 0.7, bb * 0.7))}" cy="{f(cy - b.u(5, bb * 0.3))}" rx="8" ry="3.5" fill="#fff0b0"/>' for _ in range(16))
        b.mal(f'<g filter="url(#pensel)" opacity=".85">{mont}</g>')
    b.mal(b.kasse(300, 330, 200, 80, BRUN), f'<path d="M300 330 Q300 270 400 268 Q500 270 500 330Z" fill="{b.lin([(0, BRUN), (1, VANDYKE)])}" filter="url(#akvarel)"/>',
          f'<path d="M300 352 H500 M332 330 V410 M468 330 V410" stroke="{VANDYKE}" stroke-width="6" filter="url(#pensel)"/>', f'<rect x="388" y="346" width="24" height="24" fill="{GUL}" filter="url(#pensel)"/>')
    b.mal(b.lys(400, 380, 260, "#ffe08a", 0.45), b.morke_hjoerner(0.6))
    return b.svg()


# ====================================================================== Edderkoppekløften
@scene
def edderkoppekloeften():
    b = Billede("Kæmpeedderkoppen i kløften", 32)
    b.mal(b.himmel([(0, "#e8ecf0"), (1, "#c8c0b0")]), b.lys(400, 0, 300, "#ffffff", 0.9))
    b.mal(f'<path d="M-10 -10 L330 -10 L300 80 L320 160 L290 240 L330 320 L300 400 L340 460 L-10 460Z" fill="{b.lin([(0, "#3a3028"), (1, "#8a7a68")], 1, 0)}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M810 -10 L470 -10 L500 90 L476 170 L510 250 L470 330 L500 400 L460 460 L810 460Z" fill="{b.lin([(0, "#7a6a58"), (1, "#2a221c")], 1, 0)}" filter="url(#akvarel)"/>')
    spind = ""
    for cx, cy, r in ((330, 90, 70), (482, 300, 80), (120, 380, 60)):
        for k in range(8):
            a = k * math.pi / 4
            spind += f"M{cx} {cy} L{f(cx + math.cos(a) * r)} {f(cy + math.sin(a) * r)} "
        for ring in (0.3, 0.55, 0.8):
            spind += f"M{f(cx + r * ring)} {cy} " + " ".join(f"L{f(cx + math.cos(k * math.pi / 4) * r * ring)} {f(cy + math.sin(k * math.pi / 4) * r * ring)}" for k in range(1, 9)) + " "
    b.mal(f'<path d="{spind}" stroke="#f8f4ec" stroke-width="1.2" fill="none" opacity=".8"/>')
    b.mal(b.figur(fg.edderkop(), 400, 300, 1.0, farve="#1e1820"))
    b.mal(f'<path d="M610 100 V170" stroke="#f8f4ec" stroke-width="1.5"/><path d="M592 186 L610 166 L628 186 L632 230 L610 270 L588 230Z" fill="#f4eee4" filter="url(#akvarel)"/>')
    b.mal(b.land([(-10, 420), (200, 404), (400, 430), (600, 408), (810, 420)], b.lin([(0, "#4a4038"), (1, "#1a1612")])))
    b.mal(b.lys(400, 148, 40, BLOD, 0.7))
    return b.svg()
