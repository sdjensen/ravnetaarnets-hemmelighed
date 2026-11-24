"""Tegner alle scener til spillet som SVG-filer.

Kør fra projektmappen:
    python tools/art/byg.py            # alle scener
    python tools/art/byg.py ravnetaarnet heden   # kun de nævnte

Filerne skrives til tools/art/svg/<navn>.svg og tjekkes for gyldig XML.
Kør derefter eksport.py, som laver JPEG-filerne til spillet i assets/art/scenes/.

Sådan er det bygget op:
    kit.py      – Tegning-klassen: skravering, træsnitsskygger, landskab,
                  træer, sten, mur, lys, papirstruktur og de fem lag
                  (background, midground-architecture, subject,
                  foreground-framing, lighting-overlay)
    figurer.py  – personer og væsner (vandrer, ulv, ravn, trold ...)
    kap1.py, kap2.py – selve scenerne; hver er en funktion med @scene
    akvarel.py, akvarel1.py, akvarel2.py – scener malet i blød akvarel-/
                  Bob Ross-stil (værktøjer i akvarel_vaerk.py); de erstatter
                  træsnitsscenen med samme navn

Ny scene: skriv en funktion med @scene i kap1.py/kap2.py, kør scriptet,
kør eksport.py og sæt billede: "assets/art/scenes/<navn>.jpg" på afsnittet i story.js.
"""
import os
import sys
import xml.dom.minidom

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)

import kap1  # noqa: E402
import kap2  # noqa: E402
import akvarel  # noqa: E402
import akvarel1  # noqa: E402
import akvarel2  # noqa: E402

# akvarel-versioner erstatter træsnitsversionen af samme scene
ALLE = {**kap1.S, **kap2.S, **akvarel.S, **akvarel1.S, **akvarel2.S}

ud = os.path.join(HER, "svg")
os.makedirs(ud, exist_ok=True)

valgte = sys.argv[1:] or list(ALLE)
for navn in valgte:
    svg = ALLE[navn]()
    xml.dom.minidom.parseString(svg.encode("utf-8"))  # fejler ved ugyldig SVG
    with open(os.path.join(ud, navn + ".svg"), "w", encoding="utf-8") as fil:
        fil.write(svg)
    print(f"{navn}.svg  {len(svg) // 1024} KB")
print(f"{len(valgte)} scener skrevet til {ud}")
