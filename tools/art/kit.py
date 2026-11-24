"""Tegneværktøj til fantasy-game-art: træsnit og tusch på ældet pergament.

En scene laves med en Tegning. Alle hjælpefunktioner returnerer SVG-tekst,
som lægges i et af de fem lag med t.tegn(lag, ...).

Grundideen er træsnittets: lyse former med tuschkant, en skraveret
skyggeside og en sort kerneskygge. Skraveringen tegnes som rigtige,
let rystede streger (ikke et gentaget mønster), så den ligner håndarbejde.
"""
import math
import random

INK = "#0d0b09"
PAPER = "#f4ebd9"
PAPER2 = "#e6d6b6"
SEPIA = "#6b5536"
STEN = "#b9aa90"
GOLD = "#c89d54"
BLOOD = "#8a2b2b"
MOSS = "#3b5239"
ARCANE = "#3a5a78"
W, H = 800, 450

LAG = ("background", "midground-architecture", "subject", "foreground-framing", "lighting-overlay")


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


class Form:
    """En lukket figur: SVG-sti + afgrænsningsboks + centrum."""

    def __init__(self, d, bb):
        self.d = d
        self.bb = bb

    @property
    def c(self):
        return ((self.bb[0] + self.bb[2]) / 2, (self.bb[1] + self.bb[3]) / 2)


def glat(pts, lukket=True, t=1.0):
    """Catmull-Rom gennem punkterne → bløde, organiske kurver."""
    n = len(pts)
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    rk = range(n) if lukket else range(n - 1)
    for i in rk:
        p0 = pts[(i - 1) % n] if (lukket or i > 0) else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (lukket or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 6, p1[1] + (p2[1] - p0[1]) * t / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 6, p2[1] - (p3[1] - p1[1]) * t / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + ("Z" if lukket else "")


def kantet(pts, lukket=True):
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    return d + ("Z" if lukket else "")


def form(pts, blod=True):
    return Form(glat(pts) if blod else kantet(pts), bbox(pts))


def rect(x, y, w, h):
    return Form(f"M{f(x)} {f(y)}h{f(w)}v{f(h)}h{f(-w)}Z", (x, y, x + w, y + h))


class Tegning:
    def __init__(self, titel, seed=1):
        self.titel = titel
        self.r = random.Random(seed)
        self.defs = []
        self.n = 0
        self.lag = {k: [] for k in LAG}

    # ------------------------------------------------------------ basis
    def id(self, p="k"):
        self.n += 1
        return f"{p}{self.n}"

    def tegn(self, lag, *dele):
        self.lag[lag].extend(d for d in dele if d)

    def u(self, a, b):
        return self.r.uniform(a, b)

    def sti(self, fm, fyld=PAPER, streg=INK, bredde=2.2, op=None, ekstra=""):
        o = f' opacity="{op}"' if op is not None else ""
        s = f' stroke="{streg}" stroke-width="{bredde}" stroke-linejoin="round"' if streg else ""
        return f'<path d="{fm.d}" fill="{fyld}"{s}{o}{ekstra}/>'

    def klip(self, fm):
        cid = self.id("c")
        self.defs.append(f'<clipPath id="{cid}"><path d="{fm.d}"/></clipPath>')
        return cid

    # ------------------------------------------------------------ skravering
    def _linjer(self, bb, vinkel, afstand, ryst):
        x0, y0, x1, y1 = bb
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        R = math.hypot(x1 - x0, y1 - y0) / 2 + 6
        a = math.radians(vinkel)
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        segs = []
        k = -R + self.u(0, afstand)
        while k <= R:
            px, py = cx + nx * k, cy + ny * k
            a1 = (px - dx * R + self.u(-ryst, ryst), py - dy * R)
            a2 = (px + dx * R, py + dy * R + self.u(-ryst, ryst))
            segs.append(f"M{a1[0]:.0f} {a1[1]:.0f}L{a2[0]:.0f} {a2[1]:.0f}")
            k += afstand * self.u(0.8, 1.2)
        return "".join(segs)

    def skraver(self, fm, vinkel=35, afstand=5, bredde=1.1, farve=INK, op=1, ryst=0.7, halv=None):
        """Skraver en form. halv=(lx, ly, andel) begrænser til skyggesiden."""
        cid = self.klip(fm)
        linjer = f'<path d="{self._linjer(fm.bb, vinkel, afstand, ryst)}" stroke="{farve}" stroke-width="{bredde}" fill="none" opacity="{op}" stroke-linecap="round"/>'
        if halv:
            hid = self.klip(self.halvplan(fm, *halv))
            linjer = f'<g clip-path="url(#{hid})">{linjer}</g>'
        return f'<g clip-path="url(#{cid})">{linjer}</g>'

    def halvplan(self, fm, lx, ly, andel=0.0):
        """Den del af formens boks, der vender væk fra lyset (lys kommer fra -lx,-ly)."""
        cx, cy = fm.c
        L = math.hypot(lx, ly) or 1
        lx, ly = lx / L, ly / L
        r = max(fm.bb[2] - fm.bb[0], fm.bb[3] - fm.bb[1]) / 2
        bx, by = cx + lx * r * andel, cy + ly * r * andel
        px, py = -ly, lx
        S = 2000
        pts = [(bx + px * S, by + py * S), (bx - px * S, by - py * S),
               (bx - px * S + lx * S, by - py * S + ly * S), (bx + px * S + lx * S, by + py * S + ly * S)]
        return Form(kantet(pts), (-S, -S, S, S))

    def tone(self, fm, niveau, vinkel=35, halv=None):
        """Tonevaerdi 1-4: let skravering → tæt krydsskravering."""
        dele = []
        if niveau >= 1:
            dele.append(self.skraver(fm, vinkel, 6.5 if niveau == 1 else 4.2, 1.0, halv=halv))
        if niveau >= 3:
            dele.append(self.skraver(fm, vinkel + 70, 4.8, 1.0, halv=halv))
        if niveau >= 4:
            dele.append(self.skraver(fm, vinkel - 45, 3.6, 0.9, halv=halv))
        return "".join(dele)

    def modelleret(self, fm, fyld=PAPER, lys=(1, 0.55), niveau=2, kerne=True, bredde=2.2, vinkel=35):
        """Træsnitsform: lys flade, skraveret skyggeside, sort kerneskygge, tuschkant."""
        dele = [self.sti(fm, fyld, None)]
        dele.append(self.tone(fm, niveau, vinkel, halv=(lys[0], lys[1], -0.15)))
        if kerne:
            cid = self.klip(fm)
            hid = self.klip(self.halvplan(fm, lys[0], lys[1], 0.62))
            dele.append(f'<g clip-path="url(#{cid})"><g clip-path="url(#{hid})"><path d="{fm.d}" fill="{INK}" opacity=".85"/></g></g>')
        dele.append(self.sti(fm, "none", INK, bredde))
        return "".join(dele)

    def prikker(self, fm, antal, r=1.0, farve=INK, op=0.8):
        x0, y0, x1, y1 = fm.bb
        cid = self.klip(fm)
        c = "".join(f'<circle cx="{f(self.u(x0, x1))}" cy="{f(self.u(y0, y1))}" r="{f(r * self.u(0.6, 1.3))}"/>' for _ in range(antal))
        return f'<g clip-path="url(#{cid})" fill="{farve}" opacity="{op}">{c}</g>'

    # ------------------------------------------------------------ lys
    def gloed(self, cx, cy, r, farve=GOLD, op=0.6):
        gid = self.id("g")
        self.defs.append(f'<radialGradient id="{gid}"><stop offset="0" stop-color="{farve}" stop-opacity="{op}"/>'
                         f'<stop offset=".45" stop-color="{farve}" stop-opacity="{op * 0.45}"/><stop offset="1" stop-color="{farve}" stop-opacity="0"/></radialGradient>')
        return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#{gid})"/>'

    def straaler(self, cx, cy, vinkler, laengde, bredde=0.06, farve=GOLD, op=0.35):
        gid = self.id("s")
        self.defs.append(f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(laengde)}" gradientUnits="userSpaceOnUse">'
                         f'<stop offset="0" stop-color="{farve}" stop-opacity="{op}"/><stop offset="1" stop-color="{farve}" stop-opacity="0"/></radialGradient>')
        d = ""
        for v in vinkler:
            a = math.radians(v)
            b = bredde * self.u(0.6, 1.4)
            p1 = (cx + math.cos(a - b) * laengde, cy + math.sin(a - b) * laengde)
            p2 = (cx + math.cos(a + b) * laengde, cy + math.sin(a + b) * laengde)
            d += f"M{f(cx)} {f(cy)} L{f(p1[0])} {f(p1[1])} L{f(p2[0])} {f(p2[1])}Z "
        return f'<path d="{d}" fill="url(#{gid})"/>'

    def taage(self, y, h, op=0.7, farve=PAPER):
        gid = self.id("t")
        self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{farve}" stop-opacity="0"/>'
                         f'<stop offset=".5" stop-color="{farve}" stop-opacity="{op}"/><stop offset="1" stop-color="{farve}" stop-opacity="0"/></linearGradient>')
        pts = [(x, y + self.u(-h * 0.15, h * 0.15)) for x in range(-20, 840, 60)]
        top = glat(pts, False)
        bund = " ".join(f"L{f(x)} {f(yy + h)}" for x, yy in reversed(pts))
        return f'<path d="{top} {bund}Z" fill="url(#{gid})"/>'

    def himmel(self, top, bund=PAPER, h=330, op=0.55):
        gid = self.id("h")
        self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}" stop-opacity="{op}"/>'
                         f'<stop offset="1" stop-color="{bund}" stop-opacity="0"/></linearGradient>')
        return f'<rect width="{W}" height="{h}" fill="url(#{gid})"/>'

    # ------------------------------------------------------------ landskab
    def kam(self, x0, x1, y0, y1, amp, ru=0.55, dybde=6):
        """Fraktal bjerg-/bakkekam fra (x0,y0) til (x1,y1)."""
        pts = [(x0, y0), (x1, y1)]
        a = amp
        for _ in range(dybde):
            ny = [pts[0]]
            for p, q in zip(pts, pts[1:]):
                m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + self.u(-a, a))
                ny += [m, q]
            pts = ny
            a *= ru
        return pts

    def land(self, kam, bund=H + 10, blod=True):
        top = glat(kam, False) if blod else kantet(kam, False)
        d = f"{top} L{f(kam[-1][0])} {bund} L{f(kam[0][0])} {bund}Z"
        bb = bbox(kam)
        return Form(d, (bb[0], bb[1], bb[2], bund))

    def lag_land(self, kam, niveau=1, fyld=PAPER, blod=True, kant=1.8, vinkel=30, op=1):
        fm = self.land(kam, blod=blod)
        return (f'<g opacity="{op}">' + self.sti(fm, fyld, None) + (self.tone(fm, niveau, vinkel) if niveau else "")
                + f'<path d="{glat(kam, False) if blod else kantet(kam, False)}" fill="none" stroke="{INK}" stroke-width="{kant}"/></g>')

    def graes(self, x0, x1, y, antal, h=12, bredde=1.4, farve=INK, ybund=None):
        d = ""
        for _ in range(antal):
            x = self.u(x0, x1)
            yy = self.u(y, ybund) if ybund else y + self.u(-2, 2)
            for _ in range(self.r.randint(2, 4)):
                hh = h * self.u(0.5, 1.2)
                lean = self.u(-0.5, 0.5) * hh
                d += f"M{f(x)} {f(yy)} q{f(lean * 0.3)} {f(-hh * 0.6)} {f(lean)} {f(-hh)} "
                x += self.u(1.5, 3)
        return f'<path d="{d}" stroke="{farve}" stroke-width="{bredde}" fill="none" stroke-linecap="round"/>'

    def sten(self, cx, cy, r, lys=(1, 0.5), niveau=2, fyld=STEN, fladhed=0.65):
        n = self.r.randint(7, 10)
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n + self.u(-0.25, 0.25)
            rr = r * self.u(0.75, 1.15)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * fladhed))
        pts = [(x, min(y, cy + r * fladhed * 0.6)) for x, y in pts]
        return self.modelleret(form(pts, blod=False), fyld, lys, niveau, bredde=1.8)

    def sky(self, cx, cy, b, h):
        n = max(5, int(b / 28))
        top = [(cx - b / 2 + b * i / (n - 1), cy - h * self.u(0.5, 1.0) * math.sin(math.pi * i / (n - 1)) ** 0.6) for i in range(n)]
        d = f"M{f(cx - b / 2)} {f(cy)}"
        for i in range(1, n):
            p, q = top[i - 1], top[i]
            mx = (p[0] + q[0]) / 2
            d += f" Q{f(mx)} {f(min(p[1], q[1]) - h * 0.45)} {f(q[0])} {f(q[1])}"
        d += f" Q{f(cx)} {f(cy + h * 0.25)} {f(cx - b / 2)} {f(cy)}Z"
        fm = Form(d, (cx - b / 2, cy - h * 1.5, cx + b / 2, cy + h * 0.3))
        return (self.sti(fm, PAPER, None) + self.skraver(fm, 0, 4, 0.9, op=0.7, halv=(0, 1, 0.1))
                + self.sti(fm, "none", INK, 1.6))

    def vand(self, x0, y0, x1, y1, taethed=1.0):
        d = ""
        y = y0 + 3
        while y < y1:
            frac = (y - y0) / max(1, y1 - y0)
            x = x0 + self.u(-30, 10)
            while x < x1:
                ln = self.u(14, 60) * (0.6 + frac)
                d += f"M{f(x)} {f(y + self.u(-0.8, 0.8))} h{f(ln)} "
                x += ln + self.u(8, 40) * (1.4 - frac)
            y += self.u(4, 8) / taethed * (1.3 - frac * 0.6)
        return f'<path d="{d}" stroke="{INK}" stroke-width="1.3" fill="none" stroke-linecap="round"/>'

    # ------------------------------------------------------------ træer
    def gran(self, x, y, h, b=None, fyld=INK, op=1, lys=True):
        b = b or h * 0.38
        lag = max(5, int(h / 14))
        venstre, hoejre = [], []
        for i in range(lag + 1):
            t = i / lag
            yy = y - h + h * t
            bb = b * (0.08 + 0.92 * t) / 2
            venstre.append((x - bb * self.u(0.85, 1.15), yy + self.u(0, 4)))
            venstre.append((x - bb * 0.55, yy + h / lag * 0.55))
            hoejre.append((x + bb * self.u(0.85, 1.15), yy + self.u(0, 4)))
            hoejre.append((x + bb * 0.55, yy + h / lag * 0.55))
        pts = [(x, y - h - h * 0.04)] + hoejre + [(x + b * 0.06, y), (x + b * 0.06, y + h * 0.06), (x - b * 0.06, y + h * 0.06), (x - b * 0.06, y)] + list(reversed(venstre))
        fm = form(pts, blod=False)
        ud = f'<g opacity="{op}">' + self.sti(fm, fyld, INK, 1.2)
        if lys and fyld == INK:
            d = ""
            for i in range(1, lag):
                t = i / lag
                yy = y - h + h * t
                bb = b * (0.08 + 0.92 * t) / 2
                d += f"M{f(x - bb * 0.85)} {f(yy + 2)} q{f(bb * 0.35)} {f(-3)} {f(bb * 0.7)} {f(-1)} "
            ud += f'<path d="{d}" stroke="{PAPER}" stroke-width="1.1" fill="none" opacity=".45"/>'
        return ud + "</g>"

    def gren(self, x, y, vinkel, laengde, bredde, dybde, d):
        a = math.radians(vinkel)
        x2 = x + math.cos(a) * laengde
        y2 = y + math.sin(a) * laengde
        mx = (x + x2) / 2 + self.u(-laengde, laengde) * 0.12
        my = (y + y2) / 2 + self.u(-laengde, laengde) * 0.12
        nx, ny = -math.sin(a), math.cos(a)
        b2 = bredde * 0.62
        d.append(f"M{f(x + nx * bredde / 2)} {f(y + ny * bredde / 2)} Q{f(mx + nx * bredde * 0.4)} {f(my + ny * bredde * 0.4)} {f(x2 + nx * b2 / 2)} {f(y2 + ny * b2 / 2)} "
                 f"L{f(x2 - nx * b2 / 2)} {f(y2 - ny * b2 / 2)} Q{f(mx - nx * bredde * 0.4)} {f(my - ny * bredde * 0.4)} {f(x - nx * bredde / 2)} {f(y - ny * bredde / 2)}Z")
        spidser = []
        if dybde <= 0:
            return [(x2, y2)]
        for _ in range(self.r.choice((2, 2, 3))):
            spidser += self.gren(x2, y2, vinkel + self.u(-38, 38), laengde * self.u(0.6, 0.8), b2, dybde - 1, d)
        return spidser

    def traestamme(self, x, y, h, bredde, dybde=4, spredning=0):
        d = []
        spidser = self.gren(x, y, -90 + spredning, h * 0.42, bredde, dybde, d)
        return d, spidser

    def loevtrae(self, x, y, h, lys=(1, 0.5), kroneskala=1.0, bar=False):
        d, spidser = self.traestamme(x, y, h, h * 0.09, dybde=4 if bar else 3)
        stamme = f'<path d="{" ".join(d)}" fill="{INK}"/>'
        rod = f'<path d="M{f(x - h * 0.09)} {f(y)} q{f(-h * 0.05)} {f(h * 0.03)} {f(-h * 0.1)} {f(h * 0.04)} M{f(x + h * 0.04)} {f(y)} q{f(h * 0.05)} {f(h * 0.02)} {f(h * 0.11)} {f(h * 0.05)}" stroke="{INK}" stroke-width="{f(h * 0.025)}" fill="none" stroke-linecap="round"/>'
        if bar:
            return stamme + rod
        valgte = spidser[:: max(1, len(spidser) // 14)]
        rr = [(sx, sy, h * self.u(0.1, 0.15) * kroneskala) for sx, sy in valgte]
        # først en mørk krone-masse (skyggen inde i kronen), så de belyste løvklumper
        masse = "".join(self.sti(self._loevform(sx + r * 0.25 * lys[0], sy + r * 0.3, r * 1.2), INK, None) for sx, sy, r in rr)
        klumper = "".join(self.buske(sx - r * 0.15 * lys[0], sy - r * 0.2, r, lys) for sx, sy, r in sorted(rr, key=lambda p: -p[1]))
        return masse + stamme + rod + klumper

    def _loevform(self, cx, cy, r):
        """Uregelmæssig løvklump med mange små buler (bladkant)."""
        n = self.r.randint(13, 18)
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n + self.u(-0.1, 0.1)
            rr = r * self.u(0.78, 1.08)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.82))
        d = f"M{f(pts[0][0])} {f(pts[0][1])}"
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            ox, oy = mx - cx, my - cy
            L = math.hypot(ox, oy) or 1
            bule = r * self.u(0.12, 0.26)
            d += f" Q{f(mx + ox / L * bule)} {f(my + oy / L * bule)} {f(q[0])} {f(q[1])}"
        return Form(d + "Z", (cx - r * 1.3, cy - r * 1.2, cx + r * 1.3, cy + r * 1.2))

    def buske(self, cx, cy, r, lys=(1, 0.5), fyld=PAPER, niveau=2):
        fm = self._loevform(cx, cy, r)
        ud = self.modelleret(fm, fyld, lys, niveau, bredde=1.5, vinkel=self.u(25, 55))
        # små bladstreger i den lyse side
        d = ""
        for _ in range(4):
            a = self.u(math.pi * 0.9, math.pi * 1.6)
            px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.5
            d += f"M{f(px)} {f(py)} q{f(r * 0.12)} {f(-r * 0.12)} {f(r * 0.25)} 0 "
        return ud + f'<path d="{d}" stroke="{INK}" stroke-width="1" fill="none" opacity=".7"/>'

    def sti_vej(self, xb, yb, xt, yt, bb, bt, sving=40, n=12):
        """Vej/sti i perspektiv: bred forneden, smal oppe, med et S-sving."""
        venstre, hoejre = [], []
        for i in range(n + 1):
            t = i / n
            cx = xb + (xt - xb) * t + math.sin(t * math.pi * 1.4) * sving * (1 - t)
            cy = yb + (yt - yb) * (1 - (1 - t) ** 1.6)
            b = bb + (bt - bb) * t ** 0.7
            venstre.append((cx - b / 2, cy))
            hoejre.append((cx + b / 2, cy))
        pts = venstre + list(reversed(hoejre))
        return Form(glat(pts), bbox(pts))

    # ------------------------------------------------------------ bygning
    def mur(self, fm, raekke=18, sten_b=(26, 50), lys=(1, 0.5), fyld=STEN, morkhed=0.25):
        """Kampestensmur inden for en form."""
        x0, y0, x1, y1 = fm.bb
        cid = self.klip(fm)
        ud = self.sti(fm, SEPIA, None)
        y = y0
        rk = 0
        while y < y1:
            x = x0 - self.u(0, sten_b[1]) * (rk % 2)
            while x < x1:
                b = self.u(*sten_b)
                pts = [(x + 2 + self.u(-1, 1), y + 2), (x + b - 2, y + 2 + self.u(-1, 1)), (x + b - 2 + self.u(-1, 1), y + raekke - 2), (x + 2, y + raekke - 2 + self.u(-1, 1))]
                sfm = form(pts, blod=False)
                ud += self.sti(sfm, fyld, INK, 1.2)
                if self.r.random() < morkhed:
                    ud += self.skraver(sfm, 40, 3.5, 0.9)
                else:
                    ud += f'<path d="M{f(x + 4)} {f(y + raekke - 4)} h{f(b - 10)}" stroke="{INK}" stroke-width="1" opacity=".6"/>'
                x += b
            y += raekke
            rk += 1
        return f'<g clip-path="url(#{cid})">{ud}</g>' + self.sti(fm, "none", INK, 2.4)

    def planker(self, fm, retning="v", b=22, fyld="#8a6d4a"):
        x0, y0, x1, y1 = fm.bb
        cid = self.klip(fm)
        ud = self.sti(fm, fyld, None)
        d = ""
        if retning == "v":
            x = x0
            while x < x1:
                d += f"M{f(x)} {f(y0)} V{f(y1)} "
                for _ in range(3):
                    yy = self.u(y0, y1)
                    d += f"M{f(x + self.u(3, b - 6))} {f(yy)} q{f(self.u(-2, 2))} {f(self.u(10, 30))} 0 {f(self.u(20, 50))} "
                x += b * self.u(0.85, 1.15)
        else:
            y = y0
            while y < y1:
                d += f"M{f(x0)} {f(y)} H{f(x1)} "
                for _ in range(3):
                    xx = self.u(x0, x1)
                    d += f"M{f(xx)} {f(y + self.u(3, b - 6))} q{f(self.u(10, 30))} {f(self.u(-2, 2))} {f(self.u(20, 50))} 0 "
                y += b * self.u(0.85, 1.15)
        ud += f'<path d="{d}" stroke="{INK}" stroke-width="1.2" fill="none"/>'
        return f'<g clip-path="url(#{cid})">{ud}{self.tone(fm, 1, 60)}</g>' + self.sti(fm, "none", INK, 2.2)

    # ------------------------------------------------------------ figurer
    def fugl(self, x, y, s=1, flap=0.0):
        return (f'<path d="M{f(x - 10 * s)} {f(y - (2 + flap) * s)} q{f(5 * s)} {f(-5 * s)} {f(10 * s)} {f(2 * s)} '
                f'q{f(5 * s)} {f(-7 * s)} {f(10 * s)} {f(-2 * s)}" stroke="{INK}" stroke-width="{f(2 * s)}" fill="none" stroke-linecap="round"/>')

    def kantlys(self, d, farve=GOLD, bredde=2, op=0.8):
        return f'<path d="{d}" fill="none" stroke="{farve}" stroke-width="{bredde}" opacity="{op}" stroke-linejoin="round"/>'

    # ------------------------------------------------------------ samling
    def svg(self, morkhed=0.55):
        self.defs.append(f"""
    <filter id="papir" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".011 .016" numOctaves="4" seed="3"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .42  0 0 0 0 .33  0 0 0 0 .21  0 0 0 .55 -.18"/>
    </filter>
    <filter id="gryn" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .05  0 0 0 0 .04  0 0 0 0 .03  0 0 0 .3 -.09"/>
    </filter>
    <filter id="ru" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="11" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="3"/>
    </filter>
    <radialGradient id="vignet" cx="50%" cy="48%" r="72%">
      <stop offset=".5" stop-color="{INK}" stop-opacity="0"/>
      <stop offset=".85" stop-color="#3a2a17" stop-opacity="{morkhed * 0.6}"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="{morkhed}"/>
    </radialGradient>""")
        hjoerne = ""
        for (x, y, sx, sy) in ((14, 14, 1, 1), (786, 14, -1, 1), (14, 436, 1, -1), (786, 436, -1, -1)):
            hjoerne += (f'<path transform="translate({x} {y}) scale({sx} {sy})" d="M0 22 V0 H22 M6 22 V6 H22 M10 10 l6 6" '
                        f'fill="none" stroke="{INK}" stroke-width="1.6"/>')
        lag = ""
        for k in LAG:
            filt = ' filter="url(#ru)"' if k in ("midground-architecture", "subject", "foreground-framing") else ""
            ekstra = ""
            if k == "background":
                ekstra = f'<rect width="{W}" height="{H}" fill="{PAPER}"/><rect width="{W}" height="{H}" filter="url(#papir)"/>'
            indhold = "".join(self.lag[k])
            if k == "lighting-overlay":
                indhold += (f'<rect width="{W}" height="{H}" filter="url(#gryn)" opacity=".8"/>'
                            f'<rect width="{W}" height="{H}" fill="url(#vignet)"/>'
                            f'<rect x="7" y="7" width="786" height="436" fill="none" stroke="{INK}" stroke-width="3.5"/>'
                            f'<rect x="15" y="15" width="770" height="420" fill="none" stroke="{INK}" stroke-width="1.2"/>' + hjoerne)
            lag += f'\n  <g id="{k}"{filt}>{ekstra}{indhold}</g>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{self.titel}">\n'
                f'  <title>{self.titel}</title>\n  <defs>{"".join(self.defs)}</defs>{lag}\n</svg>\n')
