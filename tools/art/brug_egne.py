"""Sætter dine egne billeder (fx fra Gemini) ind i historien.

Læg billederne i assets/art/egne/ med samme navn som scenen, fx
    assets/art/egne/graaskoven.jpg   (eller .png / .jpeg / .webp)
og kør fra projektmappen:
    python tools/art/brug_egne.py

Scriptet retter stierne i story.js, så afsnittene bruger dit billede i stedet
for det tegnede. Scener uden eget billede beholder det tegnede. Fjerner du
et eget billede igen, skifter afsnittet automatisk tilbage.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")  # så ✔ og ↩ også virker i Windows-terminalen

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.normpath(os.path.join(HER, "..", ".."))
EGNE = os.path.join(ROD, "assets", "art", "egne")
STORY = os.path.join(ROD, "story.js")
ENDELSER = (".jpg", ".jpeg", ".png", ".webp")

egne = {}
for fil in sorted(os.listdir(EGNE)) if os.path.isdir(EGNE) else []:
    navn, ext = os.path.splitext(fil)
    if ext.lower() in ENDELSER:
        egne[navn] = f"assets/art/egne/{fil}"

tekst = open(STORY, encoding="utf-8").read()
SCENER = os.path.join(ROD, "assets", "art", "scenes")
tegnede = set(os.path.splitext(f)[0] for f in os.listdir(SCENER) if f.endswith(".jpg")) if os.path.isdir(SCENER) else set()
# alle scener = de tegnede + dem, der kun findes som egne billeder i historien
alle = tegnede | set(os.path.splitext(os.path.basename(p))[0] for p in re.findall(r'(?:billede|forsidebillede): "(assets/art/[^"]+)"', tekst))
brugt, tilbage, venter = set(), set(), set()


def skift(m):
    sti = m.group(1)
    navn = os.path.splitext(os.path.basename(sti))[0]
    if navn in egne:
        brugt.add(navn)
        return m.group(0).replace(sti, egne[navn])
    if sti.startswith("assets/art/egne/"):
        if navn in tegnede:
            tilbage.add(navn)
            return m.group(0).replace(sti, f"assets/art/scenes/{navn}.jpg")
        venter.add(navn)  # ingen tegnet version – vises, når billedet er gemt
    return m.group(0)


ny = re.sub(r'(?:billede|forsidebillede): "(assets/art/[^"]+)"', skift, tekst)
if ny != tekst:
    open(STORY, "w", encoding="utf-8").write(ny)

print(f"Egne billeder i brug: {len(brugt)} af {len(alle)} scener")
for n in sorted(brugt):
    print(f"  ✔ {n}")
for n in sorted(tilbage):
    print(f"  ↩ {n} (eget billede fjernet – bruger det tegnede igen)")
ukendte = sorted(set(egne) - alle - brugt)
for n in ukendte:
    print(f"  ? {egne[n]} matcher ingen scene – tjek filnavnet")
for n in sorted(venter):
    print(f"  … {n} venter på dit billede (assets/art/egne/{n}.jpg) – afsnittet vises uden billede indtil da")
mangler = sorted(alle - brugt)
if mangler:
    print(f"Mangler stadig ({len(mangler)}): {', '.join(mangler)}")
