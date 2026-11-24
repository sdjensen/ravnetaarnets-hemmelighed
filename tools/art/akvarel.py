"""Scener malet i blød akvarel-/Bob Ross-stil (i stedet for træsnit).

Teknikken: store bløde farvevaske med uskarpe, flydende kanter (feTurbulence +
feDisplacementMap + blur), mørkere farvekant hvor vasken tørrer (alfa minus
sløret alfa), pigmentkorn og et lag med akvarelpapirets struktur. Spejlinger
i søen laves ved at genbruge landskabet spejlvendt og sløret.
"""
import math
import random

S = {}


def scene(fn):
    S[fn.__name__.replace("_", "-")] = fn
    return fn


def f(v):
    return f"{v:.1f}"


class Maleri:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def u(self, a, b):
        return self.r.uniform(a, b)

    def kam(self, x0, x1, y0, y1, amp, ru=0.55, dybde=7):
        pts = [(x0, y0), (x1, y1)]
        a = amp
        for _ in range(dybde):
            ny = [pts[0]]
            for p, q in zip(pts, pts[1:]):
                ny += [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + self.u(-a, a)), q]
            pts = ny
            a *= ru
        return pts

    @staticmethod
    def poly(pts, bund=None):
        d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
        if bund is not None:
            d += f" L{f(pts[-1][0])} {bund} L{f(pts[0][0])} {bund}"
        return d + "Z"

    def sne(self, kam, tykkelse=14, side=1):
        """Sne/lys på de bjergsider, der vender mod lyset (Bob Ross-kniven)."""
        d = ""
        for (x1, y1), (x2, y2) in zip(kam, kam[1:]):
            if (y2 - y1) * side > 0.4 and y1 < 260:
                t = tykkelse * self.u(0.6, 1.3)
                d += f"M{f(x1)} {f(y1)} L{f(x2)} {f(y2)} L{f(x2 - t * 0.3)} {f(y2 + t)} L{f(x1 - t * 0.2)} {f(y1 + t * 0.7)}Z "
        return d

    def gran(self, x, y, h, mork, lys, b=None, lysside=1):
        """Bob Ross' 'happy little tree': stamme + mange korte, nedadhældende penselstrøg."""
        b = b or h * 0.34
        strog_m, strog_l = "", ""
        trin = max(8, int(h / 2.6))
        for i in range(trin):
            t = (i + 1) / trin
            yy = y - h + h * t
            bb = b / 2 * (t ** 0.85) * self.u(0.75, 1.15)
            for s in (-1, 1):
                for _ in range(2):
                    l = bb * self.u(0.55, 1.05)
                    strog_m += f"M{f(x + self.u(-1, 1))} {f(yy)} q{f(s * l * 0.5)} {f(l * 0.05)} {f(s * l)} {f(l * 0.38 + self.u(0, 3))} "
                if s == lysside and self.r.random() < 0.55 and t < 0.92:
                    l = bb * self.u(0.35, 0.8)
                    strog_l += f"M{f(x + s * bb * 0.15)} {f(yy - 1)} q{f(s * l * 0.5)} 0 {f(s * l)} {f(l * 0.32)} "
        bredde = max(1.6, h / 32)
        stamme = f'<path d="M{f(x)} {f(y + h * 0.04)} L{f(x)} {f(y - h)}" stroke="#3b2a20" stroke-width="{f(bredde * 0.8)}" stroke-linecap="round"/>'
        return (stamme + f'<path d="{strog_m}" stroke="{mork}" stroke-width="{f(bredde)}" fill="none" stroke-linecap="round"/>'
                + f'<path d="{strog_l}" stroke="{lys}" stroke-width="{f(bredde * 0.75)}" fill="none" stroke-linecap="round" opacity=".9"/>')

    def busk(self, x, y, r, farver):
        ud = ""
        for farve, n, rr, dy in zip(farver, (26, 16, 8), (1.0, 0.75, 0.5), (0, -0.18, -0.35)):
            for _ in range(n):
                a = self.u(0, math.tau)
                d = self.u(0, r * rr)
                ud += f'<circle cx="{f(x + math.cos(a) * d * 1.4)}" cy="{f(y + r * dy + math.sin(a) * d * 0.6)}" r="{f(self.u(2.5, 6))}" fill="{farve}"/>'
        return ud

    def graes(self, x0, x1, y0, y1, n, farve, h=8):
        d = ""
        for _ in range(n):
            x, y = self.u(x0, x1), self.u(y0, y1)
            d += f"M{f(x)} {f(y)} l{f(self.u(-2, 2))} {f(-h * self.u(0.5, 1.2))} "
        return f'<path d="{d}" stroke="{farve}" stroke-width="1.4" stroke-linecap="round" opacity=".8"/>'


FILTRE = """
  <filter id="vask" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="3" seed="4" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="22" xChannelSelector="R" yChannelSelector="G"/>
    <feGaussianBlur stdDeviation="5"/>
  </filter>
  <filter id="akvarel" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="9" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="9" xChannelSelector="R" yChannelSelector="G" result="flyd"/>
    <feGaussianBlur in="flyd" stdDeviation="1.1" result="blod"/>
    <feGaussianBlur in="SourceAlpha" stdDeviation="3.5" result="ba"/>
    <feDisplacementMap in="SourceAlpha" in2="t" scale="9" xChannelSelector="R" yChannelSelector="G" result="fa"/>
    <feComposite in="fa" in2="ba" operator="arithmetic" k2="1" k3="-0.9" result="rand"/>
    <feFlood flood-color="#2a1d30" flood-opacity=".38"/>
    <feComposite in2="rand" operator="in" result="kant"/>
    <feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="2" seed="2" result="korn"/>
    <feColorMatrix in="korn" type="matrix" values="0 0 0 0 .15  0 0 0 0 .1  0 0 0 0 .15  0 0 0 .5 -.18" result="korn2"/>
    <feComposite in="korn2" in2="flyd" operator="in" result="pigment"/>
    <feMerge><feMergeNode in="blod"/><feMergeNode in="kant"/><feMergeNode in="pigment"/></feMerge>
  </filter>
  <filter id="pensel" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".08" numOctaves="2" seed="6" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="3"/>
    <feGaussianBlur stdDeviation=".45"/>
  </filter>
  <filter id="spejl" x="-5%" y="-5%" width="110%" height="110%">
    <feGaussianBlur stdDeviation="2.5 1.2"/>
  </filter>
  <filter id="papir" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="4" seed="8" result="bump"/>
    <feDiffuseLighting in="bump" surfaceScale="1.6" lighting-color="#fffaf0" result="lys">
      <feDistantLight azimuth="235" elevation="58"/>
    </feDiffuseLighting>
    <feColorMatrix in="lys" type="matrix" values=".98 0 0 0 0  0 .96 0 0 0  0 0 .9 0 0  0 0 0 0 1"/>
  </filter>
  <filter id="gloed" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
"""


# ====================================================================== Ravnetårnet
@scene
def ravnetaarnet():
    m = Maleri(61)
    HORISONT = 312
    ud = []
    defs = FILTRE + """
  <linearGradient id="himmel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2c3d6e"/><stop offset=".32" stop-color="#5f74a8"/>
    <stop offset=".58" stop-color="#d9a7a0"/><stop offset=".78" stop-color="#f4cf8a"/><stop offset="1" stop-color="#fbe8b8"/>
  </linearGradient>
  <radialGradient id="sol" cx="560" cy="250" r="260" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#fffbe6" stop-opacity="1"/><stop offset=".25" stop-color="#fde7a6" stop-opacity=".8"/>
    <stop offset="1" stop-color="#f6c77d" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="taage" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f3e2c8" stop-opacity="0"/><stop offset="1" stop-color="#f3e2c8" stop-opacity=".95"/>
  </linearGradient>
  <linearGradient id="soe" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f3d8a6"/><stop offset=".35" stop-color="#b9a8b8"/><stop offset="1" stop-color="#3d5278"/>
  </linearGradient>
  <linearGradient id="bakke" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6b8a4a"/><stop offset=".5" stop-color="#3e5a32"/><stop offset="1" stop-color="#1f3324"/>
  </linearGradient>
  <linearGradient id="taarnlys" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#5b4b5e"/><stop offset=".45" stop-color="#8a7470"/><stop offset=".75" stop-color="#d6ae7c"/><stop offset="1" stop-color="#e8c48e"/>
  </linearGradient>
  <linearGradient id="forgrund" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4f6d36"/><stop offset="1" stop-color="#1c2a1a"/>
  </linearGradient>
  <clipPath id="vandklip"><rect x="0" y="%d" width="800" height="200"/></clipPath>
""" % HORISONT

    # --- himmel og sol
    ud.append('<rect width="800" height="450" fill="url(#himmel)"/>')
    ud.append('<rect width="800" height="450" fill="url(#sol)"/>')
    skyer = ""
    for cx, cy, b, farve, op in ((150, 90, 260, "#f2c9c0", .75), (420, 60, 300, "#e8b8c2", .6), (690, 120, 220, "#f7d9b8", .8),
                                 (300, 170, 200, "#fbe1c0", .7), (90, 190, 160, "#c99aaf", .5), (640, 40, 180, "#9aa6cf", .5)):
        for _ in range(9):
            skyer += f'<ellipse cx="{f(cx + m.u(-b * 0.45, b * 0.45))}" cy="{f(cy + m.u(-12, 12))}" rx="{f(m.u(30, 70))}" ry="{f(m.u(10, 22))}" fill="{farve}" opacity="{op}"/>'
    ud.append(f'<g filter="url(#vask)">{skyer}</g>')
    ud.append('<circle cx="560" cy="250" r="70" fill="#fffbe8" opacity=".9" filter="url(#gloed)"/>')

    # --- landskabet (genbruges spejlvendt i søen)
    land = []
    # fjerne bjerge
    fjern = m.kam(-20, 820, 210, 200, 150, 0.55)
    land.append(f'<path d="{m.poly(fjern, 330)}" fill="#8f97c4" opacity=".75" filter="url(#akvarel)"/>')
    land.append(f'<path d="{m.sne(fjern, 18, 1)}" fill="#fdf6ec" opacity=".9" filter="url(#pensel)"/>')
    land.append('<rect x="0" y="210" width="800" height="110" fill="url(#taage)"/>')
    # mellemste bjerge
    midt = m.kam(-20, 820, 250, 262, 120, 0.52)
    land.append(f'<path d="{m.poly(midt, 330)}" fill="#5d6a98" opacity=".9" filter="url(#akvarel)"/>')
    land.append(f'<path d="{m.sne(midt, 22, 1)}" fill="#f7efe6" opacity=".95" filter="url(#pensel)"/>')
    land.append(f'<path d="{m.sne(midt, 10, -1)}" fill="#3f4a75" opacity=".45" filter="url(#pensel)"/>')
    land.append('<rect x="0" y="245" width="800" height="75" fill="url(#taage)"/>')
    # fjern skovbræmme langs søen
    rand = ""
    for i in range(90):
        x = -10 + i * 9.2 + m.u(-3, 3)
        rand += m.gran(x, HORISONT + m.u(-2, 3), m.u(16, 34), "#34505a", "#7c9a8a", lysside=1)
    land.append(f'<g opacity=".85" filter="url(#pensel)">{rand}</g>')
    # bakken med tårnet
    bakke = [(380, HORISONT + 2), (420, 296), (470, 276), (520, 268), (580, 270), (630, 284), (690, 302), (740, HORISONT + 2)]
    land.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in bakke)}Z" fill="url(#bakke)" filter="url(#akvarel)"/>')
    land.append(m.graes(420, 720, 280, 308, 140, "#9cbb6a", 5))
    # tårnet
    krop = "M524 272 L532 92 L604 92 L612 272Z"
    land.append(f'<path d="{krop}" fill="url(#taarnlys)" filter="url(#akvarel)"/>')
    sten = ""
    for r in range(14):
        y = 104 + r * 12
        x = 534 + (r % 2) * 9
        while x < 604:
            w = m.u(12, 20)
            sten += f"M{f(x)} {f(y)} h{f(w - 3)} "
            x += w
    land.append(f'<path d="{sten}" stroke="#4a3a40" stroke-width="1" opacity=".35" filter="url(#pensel)"/>')
    tinder = "M528 94 h80 v-18 h-9 v8 h-10 v-8 h-10 v8 h-10 v-8 h-10 v8 h-10 v-8 h-10 v8 h-8 v-8 h-3Z"
    land.append(f'<path d="{tinder}" fill="#7d6a6a" filter="url(#akvarel)"/>')
    land.append('<path d="M520 94 H616 V102 H520Z" fill="#3c2e3a" opacity=".85" filter="url(#pensel)"/>')
    land.append('<path d="M556 168 Q568 140 580 168 V200 H556Z" fill="#ffd77a" filter="url(#pensel)"/>')
    land.append('<circle cx="568" cy="182" r="34" fill="#ffe7a0" opacity=".7" filter="url(#gloed)"/>')
    land.append('<path d="M554 272 V242 Q568 224 582 242 V272Z" fill="#3a2a2a" opacity=".85" filter="url(#pensel)"/>')
    land.append('<path d="M560 198 q-2 -12 8 -14 q8 0 8 5 l7 2 -7 2 q1 6 -4 9z M560 198 l-9 5 10 -2z" fill="#1d1620"/>')
    # efeu
    efeu = "".join(f'<circle cx="{f(m.u(526, 548))}" cy="{f(m.u(160, 268))}" r="{f(m.u(2.5, 5))}" fill="{c}"/>' for c in ["#4f7a3c", "#6f9a4c", "#355a30"] * 12)
    land.append(f'<g opacity=".85" filter="url(#pensel)">{efeu}</g>')
    # små træer på bakken
    for x, h in ((430, 46), (452, 60), (650, 54), (676, 40), (700, 30)):
        land.append(f'<g filter="url(#pensel)">{m.gran(x, 300, h, "#1f3a2e", "#86a75e")}</g>')
    landskab = "".join(land)
    ud.append(f'<g id="landskab">{landskab}</g>')

    # --- søen med spejlinger og Bob Ross' vandlinjer
    ud.append(f'<rect x="0" y="{HORISONT}" width="800" height="140" fill="url(#soe)"/>')
    ud.append(f'<g clip-path="url(#vandklip)" opacity=".6" filter="url(#spejl)"><use href="#landskab" transform="translate(0 {2 * HORISONT}) scale(1 -1)"/></g>')
    ud.append(f'<ellipse cx="560" cy="{HORISONT + 40}" rx="90" ry="22" fill="#fff4cf" opacity=".45" filter="url(#gloed)"/>')
    linjer = ""
    for _ in range(70):
        y = m.u(HORISONT + 4, 420)
        x = m.u(-20, 780)
        linjer += f"M{f(x)} {f(y)} h{f(m.u(20, 120) * (1 + (y - HORISONT) / 90))} "
    ud.append(f'<path d="{linjer}" stroke="#fff8e8" stroke-width="1.3" opacity=".6" stroke-linecap="round" filter="url(#pensel)"/>')
    ud.append(f'<path d="M0 {HORISONT + 1} H800" stroke="#fff8e8" stroke-width="2" opacity=".6" filter="url(#pensel)"/>')

    # --- forgrund: brinker, buske og store glade træer
    venstre = [(-10, 380), (60, 370), (160, 384), (250, 404), (330, 430), (360, 460), (-10, 460)]
    hoejre = [(560, 460), (620, 430), (700, 412), (810, 404), (810, 460)]
    for pts in (venstre, hoejre):
        ud.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in pts)}Z" fill="url(#forgrund)" filter="url(#akvarel)"/>')
    buske = "".join(m.busk(x, y, r, ("#2e4a2a", "#5f8a3e", "#b5c86a")) for x, y, r in
                    ((40, 372, 34), (140, 380, 30), (240, 400, 26), (650, 420, 30), (760, 404, 36)))
    ud.append(f'<g filter="url(#pensel)">{buske}</g>')
    ud.append(m.graes(0, 340, 390, 450, 260, "#c4d27a", 10))
    ud.append(m.graes(570, 800, 416, 450, 160, "#c4d27a", 10))
    store = ""
    for x, y, h, b in ((70, 392, 300, 120), (150, 398, 220, 90), (20, 410, 360, 140), (740, 420, 280, 110), (790, 430, 230, 90)):
        store += m.gran(x, y, h, "#15261f", "#4f7048", b=b, lysside=1 if x < 400 else -1)
    ud.append(f'<g filter="url(#pensel)">{store}</g>')
    # en lille ravn over søen
    ud.append('<path d="M300 150 q8 -8 16 0 q8 -8 16 0 M342 128 q6 -6 12 0 q6 -6 12 0" stroke="#2a2030" stroke-width="2.2" fill="none" stroke-linecap="round"/>')

    # --- papir og lys
    ud.append('<rect width="800" height="450" filter="url(#papir)" style="mix-blend-mode:multiply" opacity=".55"/>')
    ud.append('<rect width="800" height="450" fill="none" stroke="#f8f1e4" stroke-width="18" filter="url(#vask)"/>')

    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 800 450" role="img" aria-label="Ravnetårnet">\n'
            f'<title>Ravnetårnet</title><defs>{defs}</defs>\n' + "\n".join(ud) + "\n</svg>\n")
