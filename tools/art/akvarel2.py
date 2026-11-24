"""Kapitel 2 (Skyggekongen) malet i blød akvarel-/Bob Ross-stil."""
import math
from akvarel_vaerk import *  # noqa: F401,F403
from akvarel_vaerk import Billede, f
import figurer as fg

S = {}
LYSLILLA = "#c9a0dc"
ASKE = "#9a918a"
MOERK = "#2a2230"


def scene(fn):
    S[fn.__name__.replace("_", "-")] = fn
    return fn


def skygge(x, y, h, spejl=1, op=0.8):
    s = spejl
    d = (f"M{f(x - 18 * s)} {f(y)} Q{f(x - 24 * s)} {f(y - h * 0.5)} {f(x - 8 * s)} {f(y - h * 0.86)} "
         f"Q{f(x)} {f(y - h - 6)} {f(x + 12 * s)} {f(y - h * 0.86)} Q{f(x + 28 * s)} {f(y - h * 0.5)} {f(x + 20 * s)} {f(y)} "
         f"Q{f(x + 10 * s)} {f(y - 18)} {f(x)} {f(y - 4)} Q{f(x - 10 * s)} {f(y - 20)} {f(x - 18 * s)} {f(y)}Z")
    arme = "".join(f"M{f(x + 16 * s)} {f(y - h * 0.62)} q{f(28 * s)} {f(-10 + k * 8)} {f((44 + k * 4) * s)} {f(4 + k * 10)} " for k in range(4))
    return (f'<g opacity="{op}" filter="url(#vask)"><path d="{d}" fill="{MOERK}"/><path d="{arme}" stroke="{MOERK}" stroke-width="4" fill="none" stroke-linecap="round"/></g>'
            f'<circle cx="{f(x - 2 * s)}" cy="{f(y - h * 0.8)}" r="2.5" fill="#e05050"/><circle cx="{f(x + 8 * s)}" cy="{f(y - h * 0.8)}" r="2.5" fill="#e05050"/>')


def ruin(b, x, bb, h, y=440, farve=LYSSTEN):
    pts = [(x, y), (x, y - h)] + [(x + bb * i / 6, y - h * b.u(0.55, 1.0)) for i in range(1, 6)] + [(x + bb, y - h * b.u(0.5, 0.9)), (x + bb, y)]
    d = "M" + " L".join(f"{f(px)} {f(py)}" for px, py in pts) + "Z"
    ud = f'<path d="{d}" fill="{b.lin([(0, farve), (1, "#6a625c")])}" filter="url(#akvarel)"/>'
    for _ in range(2):
        vx, vy = x + b.u(bb * 0.15, bb * 0.6), y - h * b.u(0.3, 0.5)
        ud += b.bue(vx, vy, bb * 0.22, h * 0.25, "#2a2228")
    return ud


# ====================================================================== Månestenen i mørke
@scene
def maanesten_i_moerke():
    b = Billede("Månestenen bliver sort", 101)
    b.mal(b.himmel([(0, "#1e1a34"), (0.5, "#4a3a6a"), (1, "#8a7a9a")]), b.stjerner(30), b.maane(120, 80, 26, "#e8e0f0"))
    b.mal(b.skyer([(330, 90, 260, "#6a5a8a", .5), (620, 130, 220, "#5a4a7a", .5)]))
    b.mal(b.bjerge(270, 260, 60, "#4a4068", sne="#c8c0d8", taage="#6a5a7a"))
    b.mal(b.skovrand(300, hmin=30, hmax=60, mork="#1a1a2a", lys="#3a3a4a", taet=14))
    b.mal(b.bakke([(-10, 340), (200, 322), (420, 330), (620, 316), (810, 332)], top="#3a4a4a", bund="#1a2420", gtop="#5a6a5a"))
    b.mal(b.hytte(50, 372, 140, 76, roeg=False), b.hytte(610, 376, 150, 80, roeg=False))
    b.mal(f'<rect x="394" y="236" width="12" height="190" fill="{VANDYKE}" filter="url(#pensel)"/>')
    b.mal(b.lys(400, 250, 160, "#1a1020", 0.9), b.lys(400, 250, 50, "#a03040", 0.6))
    b.mal(f'<circle cx="400" cy="256" r="20" fill="#1a1020" filter="url(#pensel)"/><path d="M372 250 Q400 212 428 250" stroke="{GUL}" stroke-width="4" fill="none"/>')
    b.mal(skygge(190, 430, 140), skygge(640, 436, 150, -1), skygge(310, 440, 96), skygge(520, 444, 110, -1))
    b.mal(b.land([(-10, 430), (300, 418), (520, 434), (810, 420)], b.lin([(0, "#2a3a30"), (1, "#141c16")])))
    return b.svg()


# ====================================================================== Heden
@scene
def heden():
    b = Billede("Den øde hede med vejviseren", 102)
    b.mal(b.himmel([(0, "#7a8aa8"), (0.6, "#d8ccc0"), (1, "#f0e0c0")]), b.skyer([(420, 70, 300, HVID, .8), (700, 110, 200, "#e8d8d0", .7)]))
    b.mal(b.bjerge(230, 250, 170, "#7a7aa8", x0=-20, x1=380, taage=None))
    b.mal(f'<path d="M560 262 V214 H576 V190 H592 V222 H612 V176 H622 V154 L630 140 L638 154 V206 H660 V196 H682 V262Z" fill="#6a6070" opacity=".7" filter="url(#akvarel)"/>')
    b.mal(b.taage(200, 80, "#ece0cc"))
    b.mal(b.bakke([(-10, 270), (200, 258), (400, 266), (600, 254), (810, 270)], top="#a08a6a", bund="#5a4a3a", gtop="#c8b088"))
    lyng = "".join(f'<circle cx="{f(b.u(0, 800))}" cy="{f(b.u(290, 440))}" r="{f(b.u(2, 5))}" fill="{b.r.choice(("#9a5a7a", "#b06a8a", "#7a4a6a"))}"/>' for _ in range(260))
    b.mal(f'<g filter="url(#pensel)" opacity=".7">{lyng}</g>')
    b.mal(b.sti([(330, 460), (396, 372), (412, 372), (480, 460)], "#d8c8a0"))
    for d in ("M392 376 Q300 330 170 296", "M416 376 Q520 330 650 292", "M404 374 Q408 330 404 276"):
        b.mal(f'<path d="{d}" stroke="#d8c8a0" stroke-width="14" fill="none" stroke-linecap="round" opacity=".85" filter="url(#akvarel)"/>')
    b.mal(f'<rect x="396" y="170" width="14" height="210" fill="{BRUN}" filter="url(#pensel)"/>')
    for (x1, y1, x2, retn) in ((410, 186, 494, 1), (396, 222, 316, -1), (410, 258, 480, 1)):
        b.mal(f'<path d="M{x1} {y1} H{x2} L{x2 + 14 * retn} {y1 + 13} L{x2} {y1 + 26} H{x1}Z" fill="{OKKER}" filter="url(#akvarel)"/>')
    b.mal(b.figur(fg.ravn_siddende(), 404, 170, 0.6))
    b.mal(b.loevtrae(620, 300, 170, bar=True, stamme=PLUM), b.figur(fg.ravn_siddende(), 660, 196, 0.5), b.figur(fg.ravn_siddende(), 586, 214, 0.45))
    b.mal(b.land([(-10, 430), (260, 416), (520, 438), (810, 422)], b.lin([(0, "#7a6a4a"), (1, "#3a2e22")])), b.graes(0, 800, 420, 450, 160, "#c8b088", 12))
    return b.svg()


# ====================================================================== Heksehytten
@scene
def heksehytten():
    b = Billede("Heksens hytte på pæle over mosen", 104)
    H = 330
    b.mal(b.himmel([(0, "#6a8a7a"), (0.6, "#c8d4b8"), (1, "#e8e4c8")]))
    land = "".join(b.loevtrae(x, H, b.u(160, 220), bar=True, stamme="#4a4a3a") for x in (40, 110, 680, 760))
    land += b.taage(250, 90, "#e0e4d0")
    for x1, x2 in ((300, 320), (400, 396), (500, 480)):
        land += f'<path d="M{x1 - 6} 420 L{x2 - 5} 248 L{x2 + 5} 248 L{x1 + 6} 420Z" fill="{VANDYKE}" filter="url(#pensel)"/>'
    land += f'<path d="M280 256 L520 246 L510 150 L290 160Z" fill="{b.lin([(0, VANDYKE), (1, BRUN)], 1, 0)}" filter="url(#akvarel)"/>'
    land += f'<path d="M256 172 L300 90 L420 36 L520 76 L548 166 L420 148Z" fill="{b.lin([(0, "#8a6a3a"), (1, "#4a3a22")])}" filter="url(#akvarel)"/>'
    land += f'<path d="M330 246 V196 Q350 176 370 196 V246Z" fill="{GUL}" filter="url(#pensel)"/>' + b.lys(350, 220, 70, "#ffe08a", 0.7)
    land += f'<rect x="440" y="182" width="40" height="28" fill="#9ad08a" filter="url(#pensel)"/>' + b.lys(460, 196, 50, LYSGRON, 0.6)
    land += f'<g stroke="{VANDYKE}" stroke-width="3" filter="url(#pensel)"><path d="M350 256 L340 400 M370 256 L362 400 M343 290 h22 M342 330 h22 M341 370 h22"/></g>'
    b.mal(f'<g id="hytte">{land}</g>', b.soe(H + 70, "hytte", [(0, "#a8b8a0"), (1, "#3a4a3a")], spejlop=0.45))
    b.mal(b.figur(fg.kappefigur(hat=True, kant=GUL), 350, 246, 0.55))
    b.mal(b.ild(600, 420, 60, 40), f'<path d="M560 400 Q560 430 600 432 Q640 430 640 400Z" fill="{PLUM}" filter="url(#pensel)"/>', b.lys(600, 380, 90, LYSGRON, 0.7))
    b.mal(b.taage(360, 60, "#e8ecdc", 0.7), b.siv(0, 100, 440), b.siv(700, 800, 440))
    return b.svg()


# ====================================================================== Bjergpasset
@scene
def bjergpasset():
    b = Billede("Det sneklædte bjergpas", 110)
    b.mal(b.himmel([(0, "#4f6fa8"), (0.6, "#b8c8e0"), (1, "#eef0f0")]))
    b.mal(b.bjerge(200, 190, 230, "#8a98c8", taage="#e8ecf4"), b.bjerge(280, 270, 130, "#5d6a98", taage="#e0e6f0"))
    b.mal(b.land([(-10, 320), (120, 300), (260, 336), (380, 330), (560, 300), (700, 280), (810, 290)], b.lin([(0, "#8a7a68"), (1, "#4a3e34")])))
    b.mal(f'<path d="M-10 360 Q200 330 380 352 Q520 368 700 330 L810 320 V350 Q620 380 470 386 Q260 396 -10 392Z" fill="#f4f4f8" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M-10 330 L-10 150 L40 130 L110 140 L150 170 L170 330Z" fill="{b.lin([(0, "#6a5a4a"), (1, "#3a3028")], 1, 0)}" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M30 150 Q80 140 130 150 L134 300 Q80 318 26 300Z" fill="{b.lin([(0, "#e8f4fc"), (1, "#a8c8e0")])}" filter="url(#akvarel)"/>', b.lys(80, 230, 90, MAGI, 0.4))
    b.mal(f'<path d="M600 330 Q600 262 650 256 Q700 262 700 330Z" fill="#2a2430" filter="url(#akvarel)"/>')
    b.mal(b.graner([(560, 300, 60, 26), (720, 290, 70, 30), (760, 300, 50, 22)], mork="#1f3a3a", lys="#d8e8f0"))
    b.mal(b.figur(fg.vandrer(sværd=False, kant=HVID), 420, 372, 0.6, farve="#3a3048"))
    b.mal(b.land([(-10, 430), (240, 412), (500, 440), (810, 418)], b.lin([(0, "#f0f2f6"), (1, "#c8d0dc")])))
    sne = "".join(f'<circle cx="{f(b.u(20, 780))}" cy="{f(b.u(20, 420))}" r="{f(b.u(1.5, 3.5))}" fill="#ffffff" opacity=".85"/>' for _ in range(80))
    b.mal(sne)
    return b.svg()


# ====================================================================== Mineskakten
@scene
def mineskakten():
    b = Billede("Den gamle dværgemine", 114)
    b.mal(f'<rect width="800" height="450" fill="{b.rad(400, 225, 500, [(0, "#4a3a2a"), (1, "#1a1410")])}"/>')
    for w, h, bb in ((380, 230, 26), (280, 166, 20), (196, 116, 15), (134, 80, 11), (90, 54, 8)):
        for x, y, bw, bh in ((400 - w, 225 - h, bb, h * 2), (400 + w - bb, 225 - h, bb, h * 2), (400 - w, 225 - h, w * 2, bb * 0.9)):
            b.mal(b.kasse(x, y, bw, bh, BRUN))
    b.mal(f'<path d="M322 271 V179 H478 V271Z" fill="#0e0a08" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M290 460 L388 271 M510 460 L412 271" stroke="#9a9aa0" stroke-width="5" filter="url(#pensel)"/>')
    sveller = "".join(f'<path d="M{f(400 - 120 * k)} {f(271 + 190 * k)} H{f(400 + 120 * k)}" stroke="{BRUN}" stroke-width="{f(3 + 6 * k)}"/>' for k in (0.15, 0.3, 0.5, 0.75, 1.0))
    b.mal(f'<g filter="url(#pensel)">{sveller}</g>')
    b.mal(f'<path d="M520 400 L540 336 H690 L710 400Z" fill="{b.lin([(0, BRUN), (1, VANDYKE)])}" filter="url(#akvarel)"/>',
          f'<path d="M540 336 q30 -26 60 -6 q30 -20 60 -2 q20 -6 30 8z" fill="{STEN}" filter="url(#akvarel)"/>',
          f'<circle cx="560" cy="410" r="16" fill="{PLUM}"/><circle cx="670" cy="410" r="16" fill="{PLUM}"/>')
    b.mal(f'<g fill="{GUL}"><path d="M372 220 q4 -3 8 0 q-4 2 -8 0z M384 220 q4 -3 8 0 q-4 2 -8 0z M410 236 q4 -3 8 0 q-4 2 -8 0z M422 236 q4 -3 8 0 q-4 2 -8 0z"/></g>', b.lys(398, 228, 50, GUL, 0.4))
    b.mal(b.fakkel(100, 360, 60), b.lys(100, 280, 300, "#ffcf7a", 0.5))
    return b.svg()


# ====================================================================== Dværgeporten
@scene
def dvaergeporten():
    b = Billede("Dværgeporten i Jernbjerget", 116)
    b.mal(f'<rect width="800" height="450" fill="{b.lin([(0, "#8a7a6a"), (1, "#4a3e34")])}"/>')
    revner = "".join(f'<path d="M{f(b.u(0, 800))} {f(b.u(0, 420))} l{f(b.u(-40, 40))} {f(b.u(20, 60))} l{f(b.u(-30, 30))} {f(b.u(20, 50))}" stroke="#3a3028" stroke-width="2.4" fill="none" opacity=".6"/>' for _ in range(14))
    b.mal(f'<g filter="url(#pensel)">{revner}</g>', b.skyer([(200, 100, 300, "#a89888", .4), (600, 300, 300, "#6a5a4a", .4)]))
    b.mal(b.bue(250, 412, 300, 360, b.lin([(0, LYSSTEN), (1, STEN)])))
    b.mal(b.bue(276, 412, 248, 330, b.lin([(0, "#6a4a30"), (1, "#3a2818")])))
    b.mal(f'<path d="M400 82 V412 M276 200 H524 M276 300 H524" stroke="#2a1a10" stroke-width="6" filter="url(#pensel)"/>',
          f'<circle cx="380" cy="300" r="9" fill="{GUL}"/><circle cx="420" cy="300" r="9" fill="{GUL}"/>')
    b.mal(f'<g stroke="#ffd77a" stroke-width="3.2" fill="none" stroke-linecap="round" filter="url(#pensel)"><path d="M330 140 l10 -16 10 16 M372 122 v20 l10 -10 M418 124 l10 18 l10 -18 M458 140 l10 -16 l6 16"/>'
          f'<path d="M320 250 h20 M330 240 v20 M460 250 l12 -10 l0 20 M360 172 l8 8 -8 8 M432 172 l-8 8 8 8"/></g>', b.lys(400, 180, 180, "#ffd77a", 0.4))
    b.mal(b.kasse(210, 412, 380, 18, LYSSTEN), b.kasse(230, 430, 340, 20, STEN))
    for x, sp in ((150, False), (650, True)):
        statue = (f'<path d="M-40 0 V-100 Q-40 -150 0 -154 Q40 -150 40 -100 V0Z" fill="#a89a88"/><circle cx="0" cy="-176" r="24" fill="#b8ab98"/>'
                  f'<path d="M-22 -168 Q0 -90 22 -168Z" fill="#d8d0c0"/><path d="M-27 -184 Q0 -222 27 -184Z" fill="#7a6a58"/>'
                  f'<path d="M-26 -194 Q-44 -204 -42 -226 Q-32 -210 -18 -204Z M26 -194 Q44 -204 42 -226 Q32 -210 18 -204Z" fill="#eee6d8"/>'
                  f'<path d="M50 -230 V0" stroke="#4a3a2a" stroke-width="7"/><path d="M50 -210 Q90 -200 90 -170 Q90 -140 50 -134 Q64 -170 50 -210Z" fill="#c8c8d0"/>')
        b.mal(f'<g filter="url(#akvarel)" transform="translate({x} 420) scale({-1 if sp else 1} 1)">{statue}</g>')
    b.mal(b.morke_hjoerner(0.6))
    return b.svg()


# ====================================================================== Dværgesmedjen
@scene
def dvaergesmedjen():
    b = Billede("Smedjen dybt inde i Jernbjerget", 118)
    b.mal(b.interioer(("#a08a7a", "#4a3a30"), tone=("#8a7a6a", "#7a6a5a", "#9a8a7a", "#6a5a4a")))
    b.mal(b.kasse(480, 150, 310, 300, LYSSTEN), f'<rect x="560" y="40" width="60" height="110" fill="#3a3030" filter="url(#akvarel)"/>')
    b.mal(b.bue(520, 452, 230, 200, "#2a1a14"), b.ild(635, 452, 210, 160))
    vaerktoej = "".join(f'<path d="M{x} 60 V{60 + h}" stroke="{BRUN}" stroke-width="6"/><rect x="{x - 10}" y="{60 + h}" width="20" height="14" fill="#6a6a72"/>' for x, h in ((60, 110), (90, 130), (120, 100)))
    b.mal(f'<g filter="url(#pensel)">{vaerktoej}</g>', b.kaede(170, 40, 170, 180))
    b.mal(f'<path d="M240 380 H400 L380 352 H300 Q250 352 228 366 Q232 376 240 380Z" fill="{b.lin([(0, "#9a9aa8"), (1, "#4a4a58")])}" filter="url(#akvarel)"/>',
          f'<path d="M290 380 L350 380 L360 452 L280 452Z" fill="#5a5a68" filter="url(#akvarel)"/>',
          f'<rect x="320" y="344" width="60" height="8" fill="#ffb84a" filter="url(#pensel)"/>', b.lys(350, 346, 70, ILD, 0.8))
    b.mal(f'<path d="M120 452 L116 360 L136 316 L180 300 L224 316 L240 360 L236 452Z" fill="{b.lin([(0, "#8a5a3a"), (1, "#4a3020")], 1, 0)}" filter="url(#akvarel)"/>')
    b.mal(f'<circle cx="178" cy="272" r="30" fill="#e8b898" filter="url(#akvarel)"/>',
          f'<path d="M150 284 Q178 404 206 284 Q196 296 178 300 Q160 296 150 284Z" fill="#e8e0d8" filter="url(#akvarel)"/>',
          f'<path d="M148 262 Q178 226 208 262 Q192 252 178 252 Q164 252 148 262Z" fill="#5a5a62" filter="url(#pensel)"/>',
          f'<path d="M162 268 h12 M182 268 h12" stroke="{VANDYKE}" stroke-width="3" filter="url(#pensel)"/><circle cx="169" cy="274" r="2.2" fill="{PLUM}"/><circle cx="187" cy="274" r="2.2" fill="{PLUM}"/>')
    b.mal(f'<path d="M224 320 L296 262" stroke="#7a4a30" stroke-width="16" stroke-linecap="round" filter="url(#pensel)"/>',
          f'<path d="M296 262 L344 316" stroke="{BRUN}" stroke-width="7"/><path d="M282 232 L322 266 L310 282 L270 248Z" fill="#7a7a88" filter="url(#akvarel)"/>')
    gnister = "".join(f'<circle cx="{f(350 + b.u(-70, 70))}" cy="{f(330 - b.u(0, 100))}" r="{f(b.u(1.2, 3))}"/>' for _ in range(30))
    b.mal(f'<g fill="#ffd77a">{gnister}</g>', b.lys(635, 390, 320, "#ffb84a", 0.5), b.morke_hjoerner(0.6))
    return b.svg()


# ====================================================================== Askeborg
@scene
def askeborg():
    b = Billede("Ruinbyen Askeborg", 120)
    b.mal(b.himmel([(0, "#5a4a6a"), (0.55, "#b8a8a8"), (1, "#d8ccc0")]), b.lys(610, 170, 170, "#8a5aa8", 0.7))
    b.mal(f'<path d="M560 230 L580 140 L590 160 L600 90 L612 160 L626 124 L640 230Z M520 236 Q580 206 660 236Z" fill="#2a2030" filter="url(#akvarel)"/>',
          f'<g fill="{LYSLILLA}"><rect x="594" y="150" width="6" height="10"/><rect x="616" y="170" width="6" height="10"/></g>')
    b.mal(b.taage(220, 80, "#c8bcb8"))
    b.mal(b.land([(-10, 280), (300, 270), (500, 276), (810, 268)], ASKE, op=0.8))
    b.mal(ruin(b, 0, 220, 250, 430), ruin(b, 580, 220, 230, 430))
    b.mal(f'<path d="M290 430 V300 Q290 200 400 200 Q510 200 510 300 V430 H470 V300 Q470 240 400 240 Q330 240 330 300 V430Z" fill="{b.lin([(0, LYSSTEN), (1, "#7a706a")])}" filter="url(#akvarel)"/>')
    b.mal(skygge(370, 420, 110), skygge(446, 414, 90, -1), skygge(250, 440, 70))
    b.mal(b.figur(fg.ravn_siddende(), 110, 186, 0.5), b.figur(fg.ravn_siddende(), 690, 206, 0.45))
    b.mal(b.land([(-10, 420), (200, 408), (400, 428), (600, 410), (810, 422)], b.lin([(0, "#a8a098"), (1, "#5a524c")])))
    b.mal(b.taage(360, 70, "#c8c0b8", 0.7))
    return b.svg()


# ====================================================================== Kloakken
@scene
def kloakken():
    b = Billede("Kloakormen under Askeborg", 125)
    b.mal(f'<rect width="800" height="450" fill="#1a1410"/>')
    b.mal(f'<path d="M60 460 V200 Q60 50 400 50 Q740 50 740 200 V460Z" fill="{b.lin([(0, "#7a6a52"), (1, "#3a3024")])}" filter="url(#akvarel)"/>')
    sten = ""
    for r in range(18):
        y = 50 + r * 22
        x = 60 - (r % 2) * 20
        while x < 740:
            w = b.u(30, 54)
            sten += f'<rect x="{f(x + 2)}" y="{f(y)}" width="{f(w - 4)}" height="18" rx="4" fill="{b.r.choice(("#8a7a62", "#6a5a46", "#9a8a72"))}" opacity=".5"/>'
            x += w
    b.defs.append('<clipPath id="hv"><path d="M60 460 V200 Q60 50 400 50 Q740 50 740 200 V460Z"/></clipPath>')
    b.mal(f'<g clip-path="url(#hv)" filter="url(#akvarel)">{sten}</g>')
    b.mal(f'<path d="M300 460 V260 Q300 200 400 200 Q500 200 500 260 V460Z" fill="#14100c" filter="url(#akvarel)"/>')
    b.mal(f'<rect x="60" y="360" width="680" height="100" fill="{b.lin([(0, "#5a6a4a"), (1, "#2a3424")])}" filter="url(#akvarel)"/>')
    linjer = "".join(f"M{f(b.u(60, 700))} {f(b.u(366, 450))} h{f(b.u(20, 80))} " for _ in range(40))
    b.mal(f'<path d="{linjer}" stroke="#c8d0b0" stroke-width="1.2" opacity=".45" filter="url(#pensel)"/>')
    b.mal(b.kasse(60, 340, 220, 20, LYSSTEN), b.kasse(520, 340, 220, 20, LYSSTEN))
    for i in range(9):
        a = i / 8
        cx, cy, r = 400 + math.sin(a * 2.4) * 70, 400 - a * 170, 40 - a * 12
        b.mal(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r)}" ry="{f(r * 0.75)}" fill="{b.rad(cx - r * 0.3, cy - r * 0.3, r * 1.4, [(0, "#c8bcb0"), (1, "#5a5048")])}" filter="url(#akvarel)"/>')
    hx, hy = 400 + math.sin(2.4) * 70, 230
    b.mal(f'<circle cx="{f(hx + 14)}" cy="{f(hy - 4)}" r="20" fill="#7a2a2a" filter="url(#pensel)"/>',
          f'<g fill="#f8f0e0"><path d="M{f(hx + 2)} {f(hy - 12)} l4 -9 4 9z M{f(hx + 14)} {f(hy - 18)} l4 -9 4 9z M{f(hx + 26)} {f(hy - 10)} l9 -2 -7 7z"/></g>')
    b.mal(f'<path d="M340 50 L300 360 H500 L460 50Z" fill="#fff4dc" opacity=".14" filter="url(#vask)"/>', b.morke_hjoerner(0.6))
    return b.svg()


# ====================================================================== Spøgelsespigen
@scene
def spoegelsespigen():
    b = Billede("Spøgelsespigen Ylva i ruinerne", 128)
    b.mal(b.himmel([(0, "#6a6a8a"), (0.6, "#c8c0c0"), (1, "#e0d8cc")]), b.land([(-10, 300), (400, 290), (810, 302)], ASKE, op=0.7))
    b.mal(ruin(b, -10, 220, 330, 440), ruin(b, 590, 220, 320, 440))
    b.mal(f'<path d="M180 460 L340 300 H460 L620 460Z" fill="{b.lin([(0, "#b8b0a4"), (1, "#8a8278")])}" filter="url(#akvarel)"/>')
    brosten = "".join(f'<path d="M{f(400 - (60 + r * 22) + b.u(0, 30))} {f(304 + r * 20)} h{f(b.u(12, 26))}" stroke="#6a625a" stroke-width="1.6" opacity=".6"/>' for r in range(8) for _ in range(8))
    b.mal(f'<g filter="url(#pensel)">{brosten}</g>')
    b.mal(b.lys(400, 330, 140, MAGI, 0.7))
    b.mal(f'<path d="M370 420 L376 350 L388 322 L412 322 L424 350 L430 420 L418 410 L408 422 L398 408 L388 422 L378 410Z" fill="#eef4fc" opacity=".8" filter="url(#akvarel)"/>',
          f'<circle cx="400" cy="302" r="19" fill="#f4f8fc" opacity=".9" filter="url(#akvarel)"/>',
          f'<path d="M384 290 l8 -12 8 8 8 -8 8 12" stroke="{GUL}" stroke-width="2.6" fill="none"/><circle cx="394" cy="302" r="2.2" fill="{PHTHALO}"/><circle cx="406" cy="302" r="2.2" fill="{PHTHALO}"/>',
          f'<path d="M424 350 Q450 340 470 312" stroke="#c8daf0" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.mal(f'<path d="M470 312 V292" stroke="{VANDYKE}" stroke-width="2"/><rect x="462" y="292" width="16" height="22" fill="{GUL}" filter="url(#pensel)"/>', b.lys(470, 304, 60, "#ffe08a", 0.7))
    b.mal(b.taage(380, 60, "#d8d4d0", 0.6))
    return b.svg()


# ====================================================================== Skyggeborgen
@scene
def skyggeborgen():
    b = Billede("Skyggeborgen", 130)
    b.mal(b.himmel([(0, "#2a1a3a"), (0.5, "#6a4a8a"), (1, "#c8a8c8")]))
    for rx, ry, op in ((180, 70, 0.35), (270, 104, 0.3), (360, 136, 0.25)):
        b.mal(f'<ellipse cx="400" cy="120" rx="{rx}" ry="{ry}" fill="none" stroke="#e8d0f0" stroke-width="10" opacity="{op}" filter="url(#vask)"/>')
    b.mal(b.lys(400, 260, 200, "#a070c0", 0.6))
    borg = "M220 300 V200 L240 160 L260 200 V220 H300 V140 L330 60 L360 140 V220 H440 V140 L470 60 L500 140 V220 H540 V200 L560 160 L580 200 V300Z"
    b.mal(f'<path d="{borg}" fill="{b.lin([(0, "#3a2a4a"), (1, "#14101c")])}" filter="url(#akvarel)"/>')
    b.mal(f'<g fill="{LYSLILLA}" filter="url(#pensel)"><rect x="322" y="150" width="10" height="18"/><rect x="462" y="150" width="10" height="18"/><rect x="236" y="230" width="8" height="14"/><rect x="556" y="230" width="8" height="14"/></g>',
          f'<path d="M360 300 V252 Q400 216 440 252 V300Z" fill="#8a5aa8" filter="url(#pensel)"/>')
    b.mal(f'<path d="M370 300 L430 300 L470 460 L330 460Z" fill="{b.lin([(0, "#8a8090"), (1, "#4a4250")])}" filter="url(#akvarel)"/>')
    b.mal(b.land([(-10, 330), (120, 310), (260, 316), (280, 460)], b.lin([(0, "#2a2030"), (1, "#100c14")])),
          b.land([(520, 460), (540, 316), (680, 310), (810, 330)], b.lin([(0, "#2a2030"), (1, "#100c14")])))
    b.mal(b.figur(fg.vandrer(sværd=False, kant=LYSLILLA), 400, 440, 0.45, farve="#1a1420"))
    b.mal(b.figur(fg.ravn_siddende(), 330, 62, 0.7), b.figur(fg.ravn_siddende(), 470, 60, 0.7), b.fugle([(120, 100, 1.2), (680, 80, 1.1)], "#1a1420"))
    return b.svg()


# ====================================================================== Tronsalen
@scene
def tronsalen():
    b = Billede("Skyggekongen Vardrak i tronsalen", 136)
    b.mal(b.interioer(("#8a7a8a", "#3a2e3a"), tone=("#7a6a7a", "#6a5a6a", "#8a7a8a", "#5a4a5a")))
    for x in (90, 210, 590, 710):
        b.mal(f'<rect x="{x - 24}" y="100" width="48" height="350" fill="{b.lin([(0, "#c8bcc0"), (1, "#6a5e66")], 1, 0) if x < 400 else b.lin([(0, "#6a5e66"), (1, "#c8bcc0")], 1, 0)}" filter="url(#akvarel)"/>',
              b.kasse(x - 32, 84, 64, 16, "#4a3e4a"))
    b.mal(f'<path d="M320 460 L372 320 L428 320 L480 460Z" fill="{b.lin([(0, "#b04050"), (1, "#6a2030")])}" filter="url(#akvarel)"/>')
    b.mal(b.kasse(330, 300, 140, 22, "#8a7a88"), b.kasse(344, 282, 112, 20, "#9a8a98"))
    b.mal(b.lys(400, 150, 180, "#b080d0", 0.9))
    b.mal(f'<path d="M330 282 V100 L360 56 L400 88 L440 56 L470 100 V282Z" fill="#1a1420" filter="url(#akvarel)"/>')
    b.mal(f'<path d="M384 150 L400 116 L416 150 L400 184Z" fill="#f0d8f8" filter="url(#pensel)"/>', b.lys(400, 150, 70, "#f0d8f8", 0.8))
    b.mal(f'<path d="M354 282 Q350 220 366 196 Q384 176 400 176 Q416 176 434 196 Q450 220 446 282Z" fill="#2a2034" filter="url(#akvarel)"/>',
          f'<circle cx="400" cy="198" r="18" fill="#2a2034" filter="url(#pensel)"/>',
          f'<path d="M380 190 L374 156 L386 178 L392 146 L400 176 L408 146 L414 178 L426 156 L420 190Z" fill="#4a3060" filter="url(#pensel)"/>',
          f'<g fill="#f0d8f8"><path d="M390 198 q4 -3 8 0 q-4 2 -8 0z M402 198 q4 -3 8 0 q-4 2 -8 0z"/></g>',
          f'<path d="M446 236 L500 226 M500 150 V320" stroke="#1a1420" stroke-width="6" stroke-linecap="round"/>')
    b.mal(skygge(250, 440, 120), skygge(550, 440, 120, -1), skygge(160, 450, 90), skygge(640, 450, 90, -1))
    b.mal(b.morke_hjoerner(0.7, "#120c18"))
    return b.svg()


# ====================================================================== Lysets sejr
@scene
def lysets_sejr():
    b = Billede("Månestenen lyser igen over Vildmose", 150)
    b.mal(b.himmel([(0, NAT), (0.5, PRUSSIAN), (1, "#8a9ac8")]), b.stjerner(40), b.maane(690, 70, 24))
    rays = "".join(f'<path d="M400 220 L{f(400 + math.cos(math.radians(a - 2)) * 600)} {f(220 + math.sin(math.radians(a - 2)) * 600)} L{f(400 + math.cos(math.radians(a + 2)) * 600)} {f(220 + math.sin(math.radians(a + 2)) * 600)}Z" fill="#e0f0ff" opacity=".22"/>' for a in range(180, 361, 15))
    b.mal(f'<g filter="url(#vask)">{rays}</g>')
    b.mal(b.bjerge(290, 280, 50, "#4a5a88", sne="#e0e8f8", taage="#6a7aa8"))
    b.mal(b.bakke([(-10, 320), (200, 300), (400, 312), (600, 296), (810, 314)], top="#3a5a4a", bund="#1a2e24", gtop="#7a9a8a"))
    b.mal(b.hytte(30, 338, 130, 70), b.hytte(640, 334, 130, 72), b.hytte(190, 330, 90, 50, skorsten=False), b.hytte(520, 330, 90, 50, skorsten=False))
    lygter = ""
    for i, x in enumerate(range(150, 660, 70)):
        y = 250 + 14 * math.sin(i * 1.3)
        lygter += f'<circle cx="{x}" cy="{f(y)}" r="7" fill="{GUL}"/>' + b.lys(x, y, 26, "#ffe08a", 0.7)
    b.mal(f'<path d="M120 244 Q260 274 400 256 Q540 274 680 244" stroke="{VANDYKE}" stroke-width="1.6" fill="none"/>', lygter)
    b.mal(f'<rect x="395" y="226" width="10" height="110" fill="{VANDYKE}" filter="url(#pensel)"/>', b.lys(400, 216, 190, "#e0f0ff", 0.95),
          f'<circle cx="400" cy="216" r="16" fill="#ffffff"/>')
    for x, y, s, sp in ((250, 340, 0.62, False), (320, 346, 0.6, True), (480, 346, 0.6, False), (550, 340, 0.62, True)):
        b.mal(b.figur(fg.kappefigur(kant="#e0f0ff"), x, y, s, spejl=sp, farve="#1e2030"),
              f'<path d="M{x - 8} {y - 40} L{x - 30} {y - 70} M{x + 8} {y - 40} L{x + 30} {y - 72}" stroke="#1e2030" stroke-width="4" stroke-linecap="round"/>')
    b.mal(b.land([(-10, 420), (300, 404), (520, 418), (810, 402)], b.lin([(0, "#2a4a3a"), (1, "#101c16")])), b.graes(0, 800, 405, 450, 140, "#7a9a8a", 12))
    return b.svg()
