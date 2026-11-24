"""Fælles malerværktøj til akvarel-/Bob Ross-scenerne.

Billede samler defs og malingslag. Alle metoder returnerer SVG-tekst, som
lægges på lærredet med b.mal(...). Bløde kanter kommer fra filtrene i
akvarel.FILTRE: "vask" (meget blød), "akvarel" (flydende kant + mørk tørkant
+ pigmentkorn), "pensel" (let rysten), "gloed" (lys) og "spejl" (vandspejling).
"""
import math
from akvarel import Maleri, FILTRE, f
import figurer as fg

# Bob Ross-paletten (omtrent)
PRUSSIAN = "#2c3d6e"
PHTHALO = "#2f5f7a"
HIMMELBLAA = "#6f86b8"
ALIZARIN = "#b0505a"
ROSA = "#e8b8c2"
GUL = "#f4cf8a"
LYSGUL = "#fbe8b8"
SAP = "#4f7a3c"
MORKGRON = "#1f3a2e"
LYSGRON = "#9cbb6a"
GRANMORK = "#15261f"
VANDYKE = "#4a3426"
BRUN = "#7a5a3e"
OKKER = "#c9a26a"
HVID = "#fbf4e6"
LILLA = "#6a5a8e"
NAT = "#24304f"
PLUM = "#2b2230"
STEN = "#9a8f86"
LYSSTEN = "#c8bba8"
ILD = "#f2a03a"
BLOD = "#8a2b2b"
MAGI = "#7fb3e6"
SKYGGE = "#5a3a6e"


class Billede(Maleri):
    def __init__(self, titel, seed):
        super().__init__(seed)
        self.titel = titel
        self.defs = [FILTRE]
        self.dele = []
        self.n = 0

    def id(self, p="g"):
        self.n += 1
        return f"{p}{self.n}"

    def mal(self, *dele):
        self.dele.extend(d for d in dele if d)

    # ------------------------------------------------------------ farveforløb
    def lin(self, stops, x2=0, y2=1):
        gid = self.id("l")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in self._st(stops))
        self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return f"url(#{gid})"

    def rad(self, cx, cy, r, stops):
        gid = self.id("r")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in self._st(stops))
        self.defs.append(f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" gradientUnits="userSpaceOnUse">{st}</radialGradient>')
        return f"url(#{gid})"

    @staticmethod
    def _st(stops):
        return [(s[0], s[1], s[2] if len(s) > 2 else 1) for s in stops]

    # ------------------------------------------------------------ himmel og lys
    def himmel(self, stops, h=450):
        return f'<rect width="800" height="{h}" fill="{self.lin(stops)}"/>'

    def lys(self, cx, cy, r, farve, op=0.9):
        return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{self.rad(cx, cy, r, [(0, farve, op), (0.4, farve, op * 0.5), (1, farve, 0)])}"/>'

    def skyer(self, liste):
        ud = ""
        for cx, cy, b, farve, op in liste:
            for _ in range(9):
                ud += (f'<ellipse cx="{f(cx + self.u(-b * 0.45, b * 0.45))}" cy="{f(cy + self.u(-12, 12))}" '
                       f'rx="{f(self.u(30, 70))}" ry="{f(self.u(10, 22))}" fill="{farve}" opacity="{op}"/>')
        return f'<g filter="url(#vask)">{ud}</g>'

    def stjerner(self, n=30, ymax=200, farve=HVID):
        return "".join(f'<circle cx="{f(self.u(20, 780))}" cy="{f(self.u(15, ymax))}" r="{f(self.u(0.6, 1.8))}" fill="{farve}" opacity="{f(self.u(0.5, 1))}"/>' for _ in range(n))

    def maane(self, cx, cy, r, farve="#fdf6e0"):
        return (self.lys(cx, cy, r * 3, farve, 0.6) + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{farve}" filter="url(#pensel)"/>'
                + f'<circle cx="{f(cx - r * 0.3)}" cy="{f(cy - r * 0.2)}" r="{f(r * 0.25)}" fill="#e6dcc0" opacity=".7"/>')

    # ------------------------------------------------------------ landskab
    def bjerge(self, y0, y1, amp, farve, sne=HVID, sneop=0.9, op=0.9, x0=-20, x1=820, taage=None, ru=0.53):
        kam = self.kam(x0, x1, y0, y1, amp, ru)
        # dale under grundlinjen skjules alligevel af tågen; så får vi altid tinder opad
        grund = max(y0, y1)
        kam = [(x, grund - abs(grund - y) if y > grund else y) for x, y in kam]
        ud = f'<path d="{self.poly(kam, 460)}" fill="{farve}" opacity="{op}" filter="url(#akvarel)"/>'
        if sne:
            ud += f'<path d="{self.sne(kam, 18, 1)}" fill="{sne}" opacity="{sneop}" filter="url(#pensel)"/>'
            ud += f'<path d="{self.sne(kam, 12, -1)}" fill="{PLUM}" opacity=".25" filter="url(#pensel)"/>'
        if taage:
            ud += self.taage(min(y0, y1) - 10, 120, taage)
        return ud

    def taage(self, y, h, farve=LYSGUL, op=0.95):
        return f'<rect x="-20" y="{f(y)}" width="840" height="{f(h)}" fill="{self.lin([(0, farve, 0), (1, farve, op)])}"/>'

    def land(self, pts, fyld, filt="akvarel", op=1, bund=460):
        d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + f" L{f(pts[-1][0])} {bund} L{f(pts[0][0])} {bund}Z"
        return f'<path d="{d}" fill="{fyld}" opacity="{op}" filter="url(#{filt})"/>'

    def bakke(self, pts, top=SAP, bund=MORKGRON, graes=True, gtop=None):
        ud = self.land(pts, self.lin([(0, top), (1, bund)]))
        if graes:
            ys = [p[1] for p in pts]
            ud += self.graes(pts[0][0], pts[-1][0], min(ys) + 6, min(ys) + 60, 140, gtop or LYSGRON, 6)
        return ud

    def skovrand(self, y, x0=-10, x1=810, hmin=14, hmax=32, mork="#34505a", lys="#7c9a8a", op=0.85, taet=9.0):
        ud = ""
        x = x0
        while x < x1:
            ud += self.gran(x + self.u(-3, 3), y + self.u(-2, 3), self.u(hmin, hmax), mork, lys)
            x += taet * self.u(0.8, 1.2)
        return f'<g opacity="{op}" filter="url(#pensel)">{ud}</g>'

    def graner(self, liste, mork=GRANMORK, lys="#4f7048"):
        ud = "".join(self.gran(x, y, h, mork, lys, b=b, lysside=1 if x < 400 else -1) for x, y, h, b in liste)
        return f'<g filter="url(#pensel)">{ud}</g>'

    def loevtrae(self, x, y, h, farver=(MORKGRON, SAP, LYSGRON), bar=False, stamme=VANDYKE, lysside=1):
        ud = f'<path d="M{f(x - h * 0.035)} {f(y)} Q{f(x - h * 0.02)} {f(y - h * 0.4)} {f(x)} {f(y - h * 0.7)} Q{f(x + h * 0.02)} {f(y - h * 0.4)} {f(x + h * 0.035)} {f(y)}Z" fill="{stamme}"/>'
        grene = ""
        for _ in range(7 if bar else 4):
            gy = y - h * self.u(0.35, 0.75)
            s = self.r.choice((-1, 1))
            l = h * self.u(0.15, 0.35)
            grene += f"M{f(x)} {f(gy)} q{f(s * l * 0.5)} {f(-l * 0.3)} {f(s * l)} {f(-l * 0.6)} "
            if bar:
                grene += f"M{f(x + s * l * 0.6)} {f(gy - l * 0.35)} l{f(s * l * 0.3)} {f(-l * 0.35)} "
        ud += f'<path d="{grene}" stroke="{stamme}" stroke-width="{f(max(1.5, h / 60))}" fill="none" stroke-linecap="round"/>'
        if not bar:
            cx, cy, rx, ry = x, y - h * 0.68, h * 0.34, h * 0.3
            for farve, n, rr, ox in zip(farver, (70, 45, 26), (1.0, 0.8, 0.55), (0, 0.15, 0.3)):
                for _ in range(n):
                    a = self.u(0, math.tau)
                    d = self.u(0, 1) ** 0.6
                    px = cx + math.cos(a) * d * rx * rr - ox * rx * lysside
                    py = cy + math.sin(a) * d * ry * rr - ox * ry
                    ud += f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(self.u(h * 0.02, h * 0.05))}" fill="{farve}"/>'
        return f'<g filter="url(#pensel)">{ud}</g>'

    def buske(self, liste, farver=("#2e4a2a", "#5f8a3e", "#b5c86a")):
        return f'<g filter="url(#pensel)">{"".join(self.busk(x, y, r, farver) for x, y, r in liste)}</g>'

    def sti(self, pts, fyld=OKKER, op=0.85):
        d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
        return f'<path d="{d}" fill="{fyld}" opacity="{op}" filter="url(#akvarel)"/>'

    def soe(self, horisont, gruppe, stops, spejlop=0.55, linjer=70):
        klip = self.id("v")
        self.defs.append(f'<clipPath id="{klip}"><rect x="0" y="{horisont}" width="800" height="{460 - horisont}"/></clipPath>')
        ud = f'<rect x="0" y="{horisont}" width="800" height="{460 - horisont}" fill="{self.lin(stops)}"/>'
        if gruppe:
            ud += f'<g clip-path="url(#{klip})" opacity="{spejlop}" filter="url(#spejl)"><use href="#{gruppe}" transform="translate(0 {2 * horisont}) scale(1 -1)"/></g>'
        d = ""
        for _ in range(linjer):
            y = self.u(horisont + 4, 440)
            d += f"M{f(self.u(-20, 780))} {f(y)} h{f(self.u(20, 110) * (1 + (y - horisont) / 90))} "
        ud += f'<path d="{d}" stroke="{HVID}" stroke-width="1.3" opacity=".55" stroke-linecap="round" filter="url(#pensel)"/>'
        ud += f'<path d="M0 {horisont + 1} H800" stroke="{HVID}" stroke-width="2" opacity=".55" filter="url(#pensel)"/>'
        return ud

    def siv(self, x0, x1, y, h=70, farve="#3e4a2a", top="#6a4a2a"):
        d, toppe = "", ""
        x = x0
        while x < x1:
            hh = h * self.u(0.5, 1.2)
            dx = self.u(-8, 8)
            d += f"M{f(x)} {f(y)} q{f(dx * 0.3)} {f(-hh * 0.5)} {f(dx)} {f(-hh)} "
            if self.r.random() < 0.3:
                toppe += f'<ellipse cx="{f(x + dx * 0.9)}" cy="{f(y - hh * 0.85)}" rx="3.5" ry="11" fill="{top}"/>'
            x += self.u(5, 10)
        return f'<g filter="url(#pensel)"><path d="{d}" stroke="{farve}" stroke-width="2.2" fill="none" stroke-linecap="round"/>{toppe}</g>'

    # ------------------------------------------------------------ bygninger
    def hytte(self, x, y, b, h, vaeg=BRUN, tag=VANDYKE, vindue=True, skorsten=True, roeg=True, lysside=1):
        """Bob Ross-hytte med plankevægge, skrå tag og varmt vindue. (x,y)=nederste venstre hjørne."""
        ud = f'<path d="M{f(x)} {f(y)} V{f(y - h)} H{f(x + b)} V{f(y)}Z" fill="{self.lin([(0, vaeg), (1, VANDYKE)], 1, 0) if lysside < 0 else self.lin([(0, VANDYKE), (1, vaeg)], 1, 0)}" filter="url(#akvarel)"/>'
        planker = "".join(f"M{f(x + 3)} {f(y - h + i * h / 6)} H{f(x + b - 3)} " for i in range(1, 6))
        ud += f'<path d="{planker}" stroke="{VANDYKE}" stroke-width="1.2" opacity=".5" filter="url(#pensel)"/>'
        tagpts = f"M{f(x - b * 0.1)} {f(y - h + 4)} L{f(x + b * 0.5)} {f(y - h - h * 0.75)} L{f(x + b * 1.1)} {f(y - h + 4)}Z"
        ud += f'<path d="{tagpts}" fill="{tag}" filter="url(#akvarel)"/>'
        ud += f'<path d="M{f(x + b * 0.5)} {f(y - h - h * 0.75)} L{f(x + b * (1.1 if lysside > 0 else -0.1))} {f(y - h + 4)}" stroke="{OKKER}" stroke-width="3" opacity=".7" filter="url(#pensel)"/>'
        if vindue:
            ud += f'<rect x="{f(x + b * 0.15)}" y="{f(y - h * 0.62)}" width="{f(b * 0.22)}" height="{f(h * 0.28)}" fill="{GUL}" filter="url(#pensel)"/>'
            ud += self.lys(x + b * 0.26, y - h * 0.48, b * 0.35, "#ffe7a0", 0.6)
        ud += f'<rect x="{f(x + b * 0.55)}" y="{f(y - h * 0.55)}" width="{f(b * 0.2)}" height="{f(h * 0.55)}" fill="{VANDYKE}" opacity=".9" filter="url(#pensel)"/>'
        if skorsten:
            sx = x + b * 0.72
            ud += f'<rect x="{f(sx)}" y="{f(y - h - h * 0.7)}" width="{f(b * 0.1)}" height="{f(h * 0.4)}" fill="{STEN}" filter="url(#pensel)"/>'
            if roeg:
                ud += f'<path d="M{f(sx + b * 0.05)} {f(y - h - h * 0.72)} c-10 -14 12 -24 0 -40 s14 -26 0 -44" stroke="{LYSSTEN}" stroke-width="7" fill="none" opacity=".5" filter="url(#vask)"/>'
        return ud

    # ------------------------------------------------------------ interiør
    def interioer(self, vaeg=("#d9b88a", "#8a6a4a"), sten=True, raekke=24, tone=("#b89870", "#a88a64", "#c8a97e", "#9a7c58")):
        ud = f'<rect width="800" height="450" fill="{self.lin([(0, vaeg[0]), (1, vaeg[1])])}"/>'
        if sten:
            s = ""
            for r in range(int(450 / raekke) + 1):
                y = r * raekke
                x = -self.u(0, 40) * (r % 2)
                while x < 800:
                    w = self.u(34, 64)
                    s += f'<rect x="{f(x + 2)}" y="{f(y + 2)}" width="{f(w - 4)}" height="{raekke - 4}" rx="5" fill="{self.r.choice(tone)}" opacity="{f(self.u(0.35, 0.7))}"/>'
                    x += w
            ud += f'<g filter="url(#akvarel)">{s}</g>'
        return ud

    def morke_hjoerner(self, op=0.75, farve="#2a1a12"):
        return f'<rect width="800" height="450" fill="{self.rad(400, 240, 520, [(0.35, farve, 0), (1, farve, op)])}"/>'

    def gulv(self, y, farve=BRUN):
        ud = f'<rect x="0" y="{y}" width="800" height="{460 - y}" fill="{self.lin([(0, farve), (1, VANDYKE)])}" filter="url(#akvarel)"/>'
        d = ""
        yy = y + 14
        while yy < 450:
            d += f"M0 {f(yy)} H800 "
            yy += 14 + (yy - y) * 0.25
        return ud + f'<path d="{d}" stroke="{VANDYKE}" stroke-width="1.4" opacity=".45" filter="url(#pensel)"/>'

    def ild(self, x, y, b, h):
        ud = self.lys(x, y - h * 0.4, max(b, h) * 2.2, ILD, 0.55)
        for farve, s in ((BLOD, 1.0), (ILD, 0.75), ("#ffe9a8", 0.45)):
            pts = f"M{f(x - b / 2 * s)} {f(y)} "
            n = 5
            for i in range(n):
                tx = x - b / 2 * s + b * s * (i + 0.5) / n
                th = h * s * self.u(0.55, 1.0) * (1 - abs(i - 2) / 6)
                pts += f"Q{f(tx - b * s / n * 0.5)} {f(y - th * 0.5)} {f(tx)} {f(y - th)} Q{f(tx + b * s / n * 0.5)} {f(y - th * 0.5)} {f(tx + b * s / n * 0.5)} {f(y - th * 0.3)} "
            pts += f"L{f(x + b / 2 * s)} {f(y)}Z"
            ud += f'<path d="{pts}" fill="{farve}" filter="url(#pensel)"/>'
        return ud

    def bue(self, x, y, b, h, fyld, filt="akvarel", op=1):
        r = b / 2
        return f'<path d="M{f(x)} {f(y)} V{f(y - h + r)} A{f(r)} {f(r)} 0 0 1 {f(x + b)} {f(y - h + r)} V{f(y)}Z" fill="{fyld}" opacity="{op}" filter="url(#{filt})"/>'

    def kasse(self, x, y, b, h, fyld, kant=VANDYKE, filt="akvarel", op=1):
        return f'<rect x="{f(x)}" y="{f(y)}" width="{f(b)}" height="{f(h)}" fill="{fyld}" opacity="{op}" filter="url(#{filt})"/>' + \
               f'<rect x="{f(x)}" y="{f(y)}" width="{f(b)}" height="{f(h)}" fill="none" stroke="{kant}" stroke-width="1.4" opacity=".5" filter="url(#pensel)"/>'

    def bord(self, x, y, b, fyld=BRUN):
        return (self.kasse(x, y, b, 12, fyld) + self.kasse(x + b * 0.05, y + 12, b * 0.05, 64, VANDYKE) + self.kasse(x + b * 0.9, y + 12, b * 0.05, 64, VANDYKE))

    def reol(self, x, y, b, h, hylder=4):
        ud = self.kasse(x, y, b, h, VANDYKE)
        farver = (ALIZARIN, SAP, PRUSSIAN, OKKER, "#8a5a7a", LYSSTEN, BLOD)
        hh = h / hylder
        for i in range(hylder):
            yb = y + hh * (i + 1) - 6
            bx = x + 8
            boeger = ""
            while bx < x + b - 14:
                bb = self.u(7, 14)
                bh = hh * self.u(0.55, 0.85)
                boeger += f'<rect x="{f(bx)}" y="{f(yb - bh)}" width="{f(bb)}" height="{f(bh)}" fill="{self.r.choice(farver)}"/>'
                bx += bb + 1.5
            ud += f'<g filter="url(#pensel)">{boeger}</g><rect x="{f(x)}" y="{f(yb)}" width="{f(b)}" height="6" fill="{PLUM}" filter="url(#pensel)"/>'
        return ud

    def vindue(self, x, y, b, h, himmel=(PRUSSIAN, HIMMELBLAA), ramme=VANDYKE, rund=False):
        if rund:
            r = b / 2
            ud = f'<circle cx="{f(x + r)}" cy="{f(y + r)}" r="{f(r)}" fill="{self.lin([(0, himmel[0]), (1, himmel[1])])}" filter="url(#akvarel)"/>'
            ud += f'<circle cx="{f(x + r)}" cy="{f(y + r)}" r="{f(r)}" fill="none" stroke="{ramme}" stroke-width="10" filter="url(#pensel)"/>'
            return ud + f'<path d="M{f(x + r)} {f(y)} V{f(y + b)} M{f(x)} {f(y + r)} H{f(x + b)}" stroke="{ramme}" stroke-width="6" filter="url(#pensel)"/>'
        ud = f'<rect x="{f(x)}" y="{f(y)}" width="{f(b)}" height="{f(h)}" fill="{self.lin([(0, himmel[0]), (1, himmel[1])])}" filter="url(#akvarel)"/>'
        return ud + f'<path d="M{f(x)} {f(y)} h{f(b)} v{f(h)} h{f(-b)}Z M{f(x + b / 2)} {f(y)} V{f(y + h)} M{f(x)} {f(y + h / 2)} H{f(x + b)}" stroke="{ramme}" stroke-width="6" fill="none" filter="url(#pensel)"/>'

    def kaede(self, x0, y0, x1, y1, farve="#5a5560"):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 10))
        ud = ""
        for i in range(n):
            cx, cy = x0 + (x1 - x0) * (i + 0.5) / n, y0 + (y1 - y0) * (i + 0.5) / n
            rx, ry = (5.5, 3) if i % 2 else (2.5, 5)
            ud += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{rx}" ry="{ry}" fill="none" stroke="{farve}" stroke-width="2.2"/>'
        return f'<g filter="url(#pensel)">{ud}</g>'

    def fakkel(self, x, y, h=60):
        return (f'<path d="M{f(x - 5)} {f(y)} L{f(x - 7)} {f(y - h)} H{f(x + 7)} L{f(x + 5)} {f(y)}Z" fill="{VANDYKE}" filter="url(#pensel)"/>'
                + self.ild(x, y - h, 20, 36))

    def kolbe(self, x, y, r, farve):
        return (f'<path d="M{f(x - 5)} {f(y - r - 16)} h10 v16 A{f(r)} {f(r)} 0 1 1 {f(x - 5)} {f(y - r)}Z" fill="#e8eef0" opacity=".85" filter="url(#pensel)"/>'
                f'<circle cx="{f(x)}" cy="{f(y + r * 0.15)}" r="{f(r * 0.8)}" fill="{farve}" opacity=".9" filter="url(#pensel)"/>' + self.lys(x, y, r * 2.4, farve, 0.45))

    # ------------------------------------------------------------ figurer
    def figur(self, svg, x, y, s=1.0, spejl=False, farve=PLUM, op=0.95):
        """Genbrug figurerne fra figurer.py, men i akvarelfarver og bløde kanter."""
        svg = svg.replace("#0d0b09", farve).replace("#f4ebd9", "#f6ecd8")
        return f'<g opacity="{op}" filter="url(#pensel)">{fg.placer(svg, x, y, s, spejl)}</g>'

    def fugle(self, liste, farve=PLUM):
        d = "".join(f"M{f(x - 10 * s)} {f(y)} q{f(5 * s)} {f(-6 * s)} {f(10 * s)} 0 q{f(5 * s)} {f(-6 * s)} {f(10 * s)} 0 " for x, y, s in liste)
        return f'<path d="{d}" stroke="{farve}" stroke-width="2" fill="none" stroke-linecap="round"/>'

    # ------------------------------------------------------------ samling
    def svg(self, ramme=True, papirop=0.55):
        slut = f'<rect width="800" height="450" filter="url(#papir)" style="mix-blend-mode:multiply" opacity="{papirop}"/>'
        if ramme:
            slut += '<rect width="800" height="450" fill="none" stroke="#f8f1e4" stroke-width="18" filter="url(#vask)"/>'
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" '
                f'aria-label="{self.titel}">\n<title>{self.titel}</title><defs>{"".join(self.defs)}</defs>\n'
                + "\n".join(self.dele) + "\n" + slut + "\n</svg>\n")
