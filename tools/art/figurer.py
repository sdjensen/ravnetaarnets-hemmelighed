"""Figurer og væsner til scenerne. Hver funktion returnerer SVG-tekst,
tegnet omkring (0,0) = fødderne/bunden i midten, og placeres med
translate/scale. Silhuetter i tusch med kantlys, så de står ud fra
mørke baggrunde."""
from kit import INK, PAPER, PAPER2, SEPIA, STEN, GOLD, BLOOD, MOSS, ARCANE, f


def placer(svg, x, y, s=1.0, spejl=False):
    sx = -s if spejl else s
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(s)})">{svg}</g>'


def _kant(d, farve=GOLD, b=1.6, op=0.85):
    return f'<path d="{d}" fill="none" stroke="{farve}" stroke-width="{b}" opacity="{op}" stroke-linejoin="round" stroke-linecap="round"/>'


# ------------------------------------------------------------------ mennesker
def vandrer(kant=GOLD, sværd=True, kappe=INK):
    """Helten: kappeklædt vandrer, set fra siden, vendt mod højre (højde ca. 100)."""
    krop = ("M-14 0 L-10 -18 Q-20 -40 -16 -62 Q-12 -78 -2 -82 Q-6 -92 2 -98 Q12 -102 16 -92 Q20 -84 12 -78 "
            "Q20 -66 18 -44 L22 -20 Q18 -8 20 0 L8 0 L4 -24 L-2 -24 L-4 0Z")
    ud = f'<path d="{krop}" fill="{kappe}"/>'
    ud += f'<path d="M-2 -82 Q-10 -60 -12 -30 M4 -70 Q2 -50 4 -30" stroke="{PAPER}" stroke-width="1" opacity=".35" fill="none"/>'
    if sværd:
        ud += f'<path d="M14 -60 L34 -66" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        ud += f'<path d="M30 -64 L58 -112" stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/><path d="M30 -64 L58 -112" stroke="{INK}" stroke-width="1.2"/>'
        ud += f'<path d="M24 -60 L38 -70" stroke="{INK}" stroke-width="4"/>'
    ud += _kant("M12 -78 Q20 -66 18 -44 L22 -20 Q18 -8 20 0", kant) + _kant("M2 -98 Q12 -102 16 -92 Q20 -84 12 -78", kant)
    return ud


def gammel_mand(kant=PAPER):
    """Siddende gammel mand med skæg og hætte."""
    d = ("M-30 0 Q-34 -24 -26 -40 Q-18 -56 -4 -60 Q-10 -70 -4 -80 Q6 -88 16 -80 Q22 -72 16 -62 "
         "Q28 -56 32 -40 L40 -22 Q46 -10 44 0Z")
    ud = f'<path d="{d}" fill="{INK}"/>'
    ud += f'<path d="M12 -70 Q22 -58 16 -40 Q8 -50 6 -62Z" fill="{PAPER}" opacity=".9"/>'
    ud += f'<path d="M14 -66 l8 2 -6 4" fill="{INK}"/>'
    ud += f'<path d="M40 -22 L58 -70" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
    ud += _kant("M16 -80 Q22 -72 16 -62 Q28 -56 32 -40 L40 -22", kant, 1.4, .6)
    return ud


def kappefigur(hat=False, fyld=INK, kant=GOLD, h=1.0):
    """Stående figur i lang kjortel/kappe (kone, færgemand, heks...)."""
    d = "M-22 0 Q-24 -40 -16 -66 Q-10 -84 0 -86 Q10 -84 16 -66 Q24 -40 22 0Z"
    ud = f'<path d="{d}" fill="{fyld}"/>'
    ud += f'<path d="M-12 -86 Q0 -110 12 -86 Q6 -78 0 -78 Q-6 -78 -12 -86Z" fill="{fyld}"/>'
    if hat:
        ud += f'<path d="M-22 -90 H22 L10 -94 L2 -130 L-8 -96Z" fill="{fyld}"/>'
    ud += _kant("M0 -86 Q10 -84 16 -66 Q24 -40 22 0", kant, 1.6, .8)
    return ud


# ------------------------------------------------------------------ dyr
def ulv(snerren=True):
    """Ulv i profil mod højre, ca. 240 lang, fødder ved y=0."""
    # slank ulv med lange ben, spids snude, store ører og busket hale
    d = ("M-168 -96 Q-150 -112 -120 -104 Q-104 -112 -90 -114 C-50 -126 20 -124 64 -122 Q92 -128 106 -146 "
         "L108 -186 L124 -156 L134 -184 L140 -152 Q156 -150 166 -140 L204 -130 Q212 -126 208 -120 L184 -116 "
         "L200 -104 Q186 -98 168 -104 Q152 -102 142 -94 Q128 -82 122 -60 L128 -6 L136 0 L114 0 L108 -54 "
         "Q72 -64 20 -62 Q-24 -60 -56 -68 L-50 -6 L-42 0 L-64 0 L-72 -62 Q-90 -70 -100 -88 Q-130 -82 -168 -96Z")
    ud = f'<path d="{d}" fill="{INK}"/>'
    ud += f'<path d="M86 -64 L92 -4 L98 0 L78 0 L74 -62Z M-34 -64 L-26 -4 L-20 0 L-40 0 L-46 -64Z" fill="{INK}" opacity=".85"/>'
    pels = "M-160 -100 l-10 -6 M-150 -96 l-8 6 M-60 -122 l-6 -9 M-20 -126 l-2 -9 M20 -124 l2 -9 M60 -122 l6 -8 M100 -140 l10 -4"
    ud += f'<path d="{pels}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    ud += _kant("M-120 -104 Q-104 -112 -90 -114 C-50 -126 20 -124 64 -122 Q92 -128 106 -146", PAPER, 1.4, .55)
    ud += f'<path d="M-60 -112 q50 -10 110 -6 M-50 -96 q40 -6 90 -2 M116 -92 q-4 20 -2 34" stroke="{PAPER}" stroke-width="1.1" fill="none" opacity=".3"/>'
    ud += f'<path d="M146 -140 q7 -4 14 0 q-7 3 -14 0z" fill="{GOLD}"/><circle cx="153" cy="-139" r="1.6" fill="{BLOOD}"/>'
    if snerren:
        ud += f'<path d="M184 -116 l3 7 3 -7 M192 -115 l3 6 3 -6 M174 -104 l3 -6 3 6 M184 -104 l3 -5 3 5" fill="{PAPER}"/>'
    return ud


def ravn_siddende():
    """Siddende ravn mod højre, ca. 60 høj."""
    d = ("M-26 0 L-4 -8 Q-14 -26 -6 -42 Q2 -56 16 -54 Q30 -52 30 -40 L46 -36 L30 -32 Q34 -20 24 -10 L20 0 L14 0 L14 -8 L6 -6 L4 0 L-2 0 Z")
    return (f'<path d="{d}" fill="{INK}"/><circle cx="20" cy="-44" r="2.4" fill="{BLOOD}"/>'
            + _kant("M-6 -42 Q2 -56 16 -54 Q30 -52 30 -40", PAPER, 1.2, .5))


def ravn_flyvende(spaend=1.0):
    """Ravn i dyk med udbredte vinger, centreret om kroppen."""
    v = ("M0 0 Q-60 -30 -120 -100 Q-150 -130 -200 -140 L-170 -112 L-210 -110 L-176 -88 L-214 -80 L-174 -64 L-206 -50 L-160 -40 Q-100 -10 -40 20Z")
    h = ("M30 0 Q90 -40 150 -110 Q180 -140 230 -150 L200 -120 L240 -116 L204 -96 L244 -86 L202 -70 L236 -56 L188 -46 Q130 -10 70 24Z")
    krop = "M-40 20 Q0 -10 30 0 Q70 24 60 60 Q40 90 0 100 L-30 140 L-10 100 Q-50 80 -50 50Z"
    hoved = "M-14 -4 Q0 -40 26 -36 Q46 -30 42 -6 Q30 6 10 6Z M38 -22 L84 -10 L40 -6Z"
    ud = f'<path d="{v} {h} {krop} {hoved}" fill="{INK}"/>'
    fjer = ("M-160 -40 Q-100 -14 -40 6 M-176 -88 Q-110 -60 -50 -10 M190 -46 Q130 -12 70 12 M204 -96 Q140 -60 60 -6")
    ud += f'<path d="{fjer}" stroke="{PAPER}" stroke-width="1.3" fill="none" opacity=".35"/>'
    ud += f'<circle cx="26" cy="-20" r="5" fill="{BLOOD}"/>'
    ud += f'<path d="M-14 100 l-8 24 M-2 100 l2 26 M10 98 l12 22" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    return ud


def edderkop():
    ud = f'<path d="M0 -150 V-260" stroke="{INK}" stroke-width="1.5"/>'
    ben = ""
    for s in (1, -1):
        for (a, b, c) in (((-24, -150), (-80, -190), (-110, -130)), ((-28, -140), (-100, -140), (-130, -70)),
                          ((-26, -128), (-90, -90), (-110, -10)), ((-20, -116), (-60, -60), (-60, 10))):
            ben += f"M{a[0] * s} {a[1]} Q{b[0] * s} {b[1]} {c[0] * s} {c[1]} "
    ud += f'<path d="{ben}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    ud += f'<path d="{ben}" stroke="{PAPER}" stroke-width="1" fill="none" opacity=".35"/>'
    ud += f'<ellipse cx="0" cy="-90" rx="46" ry="58" fill="{INK}"/><circle cx="0" cy="-152" r="28" fill="{INK}"/>'
    ud += f'<path d="M-10 -110 h20 l-10 14z M-10 -80 h20 l-10 -14z" fill="{BLOOD}"/>'
    ud += f'<g fill="{BLOOD}"><circle cx="-10" cy="-158" r="4"/><circle cx="10" cy="-158" r="4"/><circle cx="-16" cy="-166" r="2.5"/><circle cx="16" cy="-166" r="2.5"/></g>'
    ud += f'<path d="M-8 -130 l-4 12 M8 -130 l4 12" stroke="{PAPER}" stroke-width="3" stroke-linecap="round"/>'
    ud += _kant("M-30 -140 Q0 -186 30 -140", PAPER, 1.2, .5)
    return ud


def skelet():
    knogle = PAPER
    ud = f'<path d="M-16 -150 Q-16 -182 10 -184 Q36 -182 36 -150 Q36 -132 24 -128 V-118 H-4 V-128 Q-16 -132 -16 -150Z" fill="{knogle}" stroke="{INK}" stroke-width="2"/>'
    ud += f'<g fill="{INK}"><ellipse cx="2" cy="-154" rx="7" ry="8"/><ellipse cx="20" cy="-154" rx="7" ry="8"/><path d="M8 -142 l3 8 3 -8z"/></g>'
    ud += f'<path d="M0 -122 v6 M6 -122 v6 M12 -122 v6 M18 -122 v6" stroke="{INK}" stroke-width="1.5"/>'
    ud += f'<g fill="{BLOOD}"><circle cx="2" cy="-153" r="2"/><circle cx="20" cy="-153" r="2"/></g>'
    lem = "M10 -116 V-20 M-12 -94 Q10 -104 32 -94 M-14 -80 Q10 -90 34 -80 M-12 -66 Q10 -76 32 -66 M-8 -54 Q10 -62 28 -54 " \
          "M-8 -104 L-36 -64 L-44 -20 M28 -104 L60 -76 L96 -90 M10 -20 L-12 30 L-16 60 M10 -20 L36 20 L48 60"
    ud += f'<path d="{lem}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    ud += f'<path d="{lem}" stroke="{knogle}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    ud += f'<path d="M-14 -104 H34 V-44 H-14Z" fill="{BLOOD}" opacity=".5"/>'
    ud += f'<path d="M94 -90 L150 -128 Q158 -130 154 -122 L102 -84Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    return f'<g transform="translate(0 -60)">{ud}</g>'


def trold(fyld=INK, ojne=GOLD, t=None):
    """Troldehoved og skuldre (til at kigge op over noget), bund ved y=0.
    Med en Tegning t bliver kroppen skraveret og modelleret som sten."""
    krop = "M-90 0 Q-100 -80 -60 -118 Q-20 -150 30 -140 Q80 -128 92 -80 Q100 -40 90 0Z"
    if t is not None:
        from kit import Form
        ud = t.modelleret(Form(krop, (-100, -150, 100, 0)), "#7a7560", (1, 0.4), 3, bredde=3)
        ud += f'<path d="M-70 -60 q10 -8 22 -2 M40 -30 q12 -6 20 4 M-40 -20 q8 -6 16 0" stroke="{INK}" stroke-width="2" fill="none"/>'
        fyld = "#7a7560"
    else:
        ud = f'<path d="{krop}" fill="{fyld}"/>'
    ud += f'<path d="M-50 -110 L-84 -146 L-40 -124Z M60 -112 L100 -140 L56 -120Z" fill="{fyld}" stroke="{INK}" stroke-width="2.5"/>'
    ud += f'<g fill="{ojne}"><ellipse cx="-22" cy="-98" rx="10" ry="6"/><ellipse cx="28" cy="-98" rx="10" ry="6"/></g>'
    ud += f'<g fill="{INK}"><circle cx="-20" cy="-98" r="3"/><circle cx="26" cy="-98" r="3"/></g>'
    ud += f'<path d="M-36 -110 l20 4 M42 -110 l-20 4" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    ud += f'<path d="M-4 -92 Q-12 -58 4 -50 Q22 -52 14 -90Z" fill="{fyld}" stroke="{PAPER}" stroke-width="1.4" stroke-opacity=".45"/>'
    ud += f'<path d="M-36 -44 Q4 -24 44 -44 L38 -32 Q4 -14 -30 -32Z" fill="{PAPER}"/>'
    ud += f'<path d="M-24 -42 l5 12 5 -12 M26 -42 l5 12 5 -12" fill="{INK}"/>'
    ud += f'<path d="M-6 -20 q-6 20 4 34 M10 -22 q8 18 -2 34 M-20 -26 q-10 14 -6 28" stroke="{MOSS}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    ud += _kant("M-60 -118 Q-20 -150 30 -140 Q80 -128 92 -80", PAPER, 1.4, .4)
    return ud


def nisse():
    ud = f'<path d="M-22 40 Q-26 6 -10 -6 Q0 -10 10 -6 Q26 6 22 40Z" fill="{MOSS}" stroke="{INK}" stroke-width="2.5"/>'
    ud += f'<circle cx="0" cy="-22" r="20" fill="{MOSS}" stroke="{INK}" stroke-width="2.5"/>'
    ud += f'<path d="M-14 -36 L-22 -58 L-6 -40Z M14 -36 L22 -58 L6 -40Z" fill="{INK}"/>'
    ud += f'<path d="M-24 -24 L-38 -30 L-22 -16Z M24 -24 L38 -30 L22 -16Z" fill="{MOSS}" stroke="{INK}" stroke-width="2"/>'
    ud += f'<ellipse cx="-8" cy="-24" rx="6" ry="7" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/><ellipse cx="8" cy="-24" rx="6" ry="7" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>'
    ud += f'<circle cx="-7" cy="-23" r="2.5" fill="{INK}"/><circle cx="9" cy="-23" r="2.5" fill="{INK}"/>'
    ud += f'<path d="M-10 -10 Q0 -4 10 -10" stroke="{INK}" stroke-width="2" fill="none"/>'
    ud += f'<path d="M-20 10 L-34 -6 M20 10 L34 -6" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    ud += f'<path d="M18 34 Q44 40 40 18 Q38 8 46 6" stroke="{INK}" stroke-width="3" fill="none"/><path d="M44 2 l6 4 -6 4z" fill="{INK}"/>'
    return ud
