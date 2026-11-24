"""Genbrugelige byggeklodser til scenerne: huse, ild, møbler, måne m.m.
Alle tager en Tegning t som første argument og returnerer SVG-tekst."""
import math
from kit import Form, form, rect, glat, kantet, f, INK, PAPER, PAPER2, SEPIA, STEN, GOLD, BLOOD, MOSS, ARCANE

TRAE = "#8a6d4a"


def maane(t, cx, cy, r, glorie=True):
    ud = (t.gloed(cx, cy, r * 2.6, PAPER, 0.9) + t.gloed(cx, cy, r * 1.6, GOLD, 0.35)) if glorie else ""
    m = form([(cx + r * math.cos(a / 20 * 2 * math.pi), cy + r * math.sin(a / 20 * 2 * math.pi)) for a in range(20)])
    ud += t.sti(m, PAPER, INK, 2) + t.skraver(m, 20, 5, 0.8, op=0.4, halv=(1, 0.3, 0.25))
    for _ in range(4):
        kx, ky, kr = cx + t.u(-r * 0.5, r * 0.4), cy + t.u(-r * 0.5, r * 0.5), r * t.u(0.08, 0.18)
        k = form([(kx + kr * math.cos(a), ky + kr * 0.8 * math.sin(a)) for a in [i * 0.8 for i in range(8)]])
        ud += t.sti(k, "none", INK, 1, op=0.5)
    return ud


def halvmaane(t, cx, cy, r):
    ud = t.gloed(cx, cy, r * 2.2, PAPER, 0.7)
    d = f"M{f(cx)} {f(cy - r)} A{f(r)} {f(r)} 0 1 0 {f(cx)} {f(cy + r)} A{f(r * 0.7)} {f(r)} 0 1 1 {f(cx)} {f(cy - r)}Z"
    return ud + f'<path d="{d}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'


def ild(t, x, y, b, h, gloed=True):
    """Flammer stående på (x,y), bredde b, højde h."""
    ud = t.gloed(x, y - h * 0.4, max(b, h) * 1.6, GOLD, 0.6) if gloed else ""
    for farve, s in ((BLOOD, 1.0), (GOLD, 0.72), (PAPER, 0.42)):
        pts = [(x - b / 2 * s, y)]
        n = 5
        for i in range(n):
            tx = x - b / 2 * s + b * s * (i + 0.5) / n
            th = h * s * t.u(0.55, 1.0) * (1 - abs(i - (n - 1) / 2) / n * 0.8)
            pts += [(tx - b * s / n * 0.3, y - th * 0.45), (tx + t.u(-3, 3), y - th), (tx + b * s / n * 0.3, y - th * 0.45)]
        pts.append((x + b / 2 * s, y))
        ud += f'<path d="{glat(pts)}" fill="{farve}" stroke="{INK if farve == BLOOD else "none"}" stroke-width="1.5"/>'
    gnister = "".join(f'<circle cx="{f(x + t.u(-b, b))}" cy="{f(y - h - t.u(0, h))}" r="{f(t.u(1, 2.2))}"/>' for _ in range(8))
    return ud + f'<g fill="{GOLD}">{gnister}</g>'


def hus(t, x, y, b, h, lys=(1, 0.5), vindue=True, skorsten=True, roeg=True):
    """Bindingsværkshus med stråtag. (x,y) = nederste venstre hjørne."""
    ud = ""
    vaeg = rect(x, y - h, b, h)
    ud += t.sti(vaeg, PAPER, None) + t.tone(vaeg, 1, 60, halv=(lys[0], 0, 0.15))
    bjaelker = f"M{f(x)} {f(y - h * 0.5)} H{f(x + b)} M{f(x + b * 0.33)} {f(y - h)} V{f(y)} M{f(x + b * 0.66)} {f(y - h)} V{f(y)} " \
               f"M{f(x)} {f(y - h)} L{f(x + b * 0.33)} {f(y - h * 0.5)} M{f(x + b)} {f(y - h)} L{f(x + b * 0.66)} {f(y - h * 0.5)}"
    ud += f'<path d="{bjaelker}" stroke="{INK}" stroke-width="3.2" fill="none"/>' + t.sti(vaeg, "none", INK, 2.4)
    if vindue:
        ud += f'<rect x="{f(x + b * 0.08)}" y="{f(y - h * 0.44)}" width="{f(b * 0.2)}" height="{f(h * 0.3)}" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
        ud += f'<path d="M{f(x + b * 0.18)} {f(y - h * 0.44)} v{f(h * 0.3)} M{f(x + b * 0.08)} {f(y - h * 0.29)} h{f(b * 0.2)}" stroke="{INK}" stroke-width="1.5"/>'
    ud += f'<path d="M{f(x + b * 0.4)} {f(y)} V{f(y - h * 0.42)} H{f(x + b * 0.58)} V{f(y)}Z" fill="{SEPIA}" stroke="{INK}" stroke-width="2"/>'
    # stråtag
    tag = [(x - b * 0.12, y - h + 4), (x + b * 0.08, y - h - h * 0.55), (x + b * 0.5, y - h - h * 0.95),
           (x + b * 0.92, y - h - h * 0.55), (x + b * 1.12, y - h + 4), (x + b * 0.5, y - h - 6)]
    tf = form(tag)
    ud += t.sti(tf, SEPIA, None) + t.skraver(tf, 80, 3.2, 1.2) + t.skraver(tf, 100, 7, 0.8, farve=PAPER, op=0.5)
    ud += t.skraver(tf, 20, 4, 1, halv=(lys[0], 0.2, 0.1)) + t.sti(tf, "none", INK, 2.4)
    if skorsten:
        sx = x + b * 0.72
        ud += f'<path d="M{f(sx)} {f(y - h - h * 0.5)} V{f(y - h - h * 0.95)} H{f(sx + b * 0.1)} V{f(y - h - h * 0.62)}Z" fill="{STEN}" stroke="{INK}" stroke-width="2"/>'
        if roeg:
            rx, ry = sx + b * 0.05, y - h - h
            ud += f'<path d="M{f(rx)} {f(ry)} c-12 -14 12 -24 0 -40 s14 -26 0 -44 s12 -20 4 -36" stroke="{INK}" stroke-width="2" fill="none" opacity=".6"/>'
    return ud


def bord(t, x, y, b, tyk=12):
    top = rect(x, y, b, tyk)
    ud = t.planker(top, "h", tyk, TRAE)
    for bx in (x + b * 0.06, x + b * 0.88):
        ben = rect(bx, y + tyk, b * 0.06, 60)
        ud += t.modelleret(ben, TRAE, (1, 0), 2, kerne=False, bredde=1.8)
    return ud


def reol(t, x, y, b, h, hylder=3):
    ud = t.modelleret(rect(x, y, b, h), SEPIA, (1, 0.3), 3, kerne=False, bredde=2.5)
    farver = (BLOOD, PAPER2, MOSS, ARCANE, PAPER, SEPIA, GOLD)
    hh = h / hylder
    for i in range(hylder):
        yb = y + hh * (i + 1) - 6
        bx = x + 8
        while bx < x + b - 14:
            bb = t.u(7, 15)
            bh = hh * t.u(0.55, 0.82)
            if t.r.random() < 0.12:
                bx += bb
                continue
            bog = rect(bx, yb - bh, bb, bh)
            ud += t.sti(bog, t.r.choice(farver), INK, 1.3)
            ud += f'<path d="M{f(bx + 2)} {f(yb - bh * 0.8)} h{f(bb - 4)} M{f(bx + 2)} {f(yb - bh * 0.25)} h{f(bb - 4)}" stroke="{INK}" stroke-width="1"/>'
            bx += bb + 1
        ud += f'<path d="M{f(x)} {f(yb)} H{f(x + b)} V{f(yb + 6)} H{f(x)}Z" fill="{INK}"/>'
    return ud


def bue(x, y, b, h):
    """Rundbuet åbning som Form; (x,y) = nederste venstre hjørne."""
    r = b / 2
    d = f"M{f(x)} {f(y)} V{f(y - h + r)} A{f(r)} {f(r)} 0 0 1 {f(x + b)} {f(y - h + r)} V{f(y)}Z"
    return Form(d, (x, y - h, x + b, y))


def kolbe(t, x, y, r, farve, hals=18):
    d = (f"M{f(x - 5)} {f(y - r - hals)} h10 v{hals} Q{f(x + r)} {f(y - r + 4)} {f(x + r)} {f(y)} "
         f"A{f(r)} {f(r)} 0 1 1 {f(x - r)} {f(y)} Q{f(x - r)} {f(y - r + 4)} {f(x - 5)} {f(y - r)}Z")
    vaeske = f"M{f(x - r + 3)} {f(y + 2)} Q{f(x)} {f(y - 4)} {f(x + r - 3)} {f(y + 2)} A{f(r - 3)} {f(r - 3)} 0 0 1 {f(x - r + 3)} {f(y + 2)}Z"
    return (f'<path d="{d}" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/><path d="{vaeske}" fill="{farve}"/>'
            f'<path d="M{f(x - r * 0.5)} {f(y - r * 0.4)} q4 -6 10 -6" stroke="{PAPER}" stroke-width="2" fill="none"/>'
            + t.gloed(x, y, r * 2.2, farve, 0.4))


def gryde(t, x, y, b):
    d = f"M{f(x - b / 2)} {f(y - b * 0.45)} Q{f(x - b / 2)} {f(y)} {f(x)} {f(y)} Q{f(x + b / 2)} {f(y)} {f(x + b / 2)} {f(y - b * 0.45)}Z"
    fm = Form(d, (x - b / 2, y - b * 0.45, x + b / 2, y))
    return (t.modelleret(fm, INK, (1, 0.4), 0, kerne=False) +
            f'<path d="M{f(x - b / 2 - 4)} {f(y - b * 0.45)} H{f(x + b / 2 + 4)}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{f(x - b * 0.35)} {f(y - b * 0.2)} q{f(b * 0.1)} {f(b * 0.08)} {f(b * 0.25)} {f(b * 0.1)}" stroke="{PAPER}" stroke-width="1.5" fill="none" opacity=".5"/>')


def damp(x, y, n=3, h=40):
    d = "".join(f"M{f(x + i * 10 - n * 5)} {f(y)} c-8 -10 8 -18 0 -{h * 0.5:.0f} s8 -16 0 -{h * 0.5:.0f} " for i in range(n))
    return f'<path d="{d}" stroke="{INK}" stroke-width="1.6" fill="none" opacity=".55"/>'


def kaede(x0, y0, x1, y1, led=10):
    n = max(2, int(math.hypot(x1 - x0, y1 - y0) / led))
    ud = ""
    for i in range(n):
        cx = x0 + (x1 - x0) * (i + 0.5) / n
        cy = y0 + (y1 - y0) * (i + 0.5) / n
        rx, ry = (led * 0.55, led * 0.3) if i % 2 else (led * 0.25, led * 0.5)
        ud += f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    return ud


def spind(cx, cy, r, op=0.8):
    d = ""
    for k in range(8):
        a = k * math.pi / 4
        d += f"M{f(cx)} {f(cy)} L{f(cx + math.cos(a) * r)} {f(cy + math.sin(a) * r)} "
    for ring in (0.25, 0.45, 0.65, 0.85):
        pts = [(cx + math.cos(k * math.pi / 4) * r * ring, cy + math.sin(k * math.pi / 4) * r * ring) for k in range(8)]
        d += f"M{f(pts[0][0])} {f(pts[0][1])}"
        for i in range(8):
            p, q = pts[i], pts[(i + 1) % 8]
            mx, my = (p[0] + q[0]) / 2 * 0.94 + cx * 0.06, (p[1] + q[1]) / 2 * 0.94 + cy * 0.06
            d += f" Q{f(mx)} {f(my)} {f(q[0])} {f(q[1])}"
        d += " "
    return f'<path d="{d}" stroke="{PAPER}" stroke-width="1.2" fill="none" opacity="{op}"/>'


def fakkel(t, x, y, h=60):
    return (f'<path d="M{f(x - 5)} {f(y)} L{f(x - 7)} {f(y - h)} H{f(x + 7)} L{f(x + 5)} {f(y)}Z" fill="{INK}"/>'
            f'<path d="M{f(x - 9)} {f(y - h)} H{f(x + 9)} L{f(x + 6)} {f(y - h - 8)} H{f(x - 6)}Z" fill="{SEPIA}" stroke="{INK}" stroke-width="1.5"/>'
            + ild(t, x, y - h - 6, 18, 34))
