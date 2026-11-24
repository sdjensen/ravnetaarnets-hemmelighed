"""Gør dine egne billeder i assets/art/egne/ mindre, så spillet loader hurtigt.

Originalerne gemmes først i tools/art/originaler/ (rør dem ikke), og de
komprimerede versioner (1200 px brede, JPEG kvalitet 82) skrives ind i
assets/art/egne/. Køres scriptet igen, laves de altid ud fra originalerne –
kvaliteten falder altså ikke af at køre det flere gange. Nye billeder, du
lægger i egne/, kommer automatisk med.

Kræver Pillow (én gang):  pip install pillow
Kør fra projektmappen:    python tools/art/komprimer.py
Kør derefter:             python tools/art/brug_egne.py
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow mangler – installér det med:  pip install pillow")

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.normpath(os.path.join(HER, "..", ".."))
EGNE = os.path.join(ROD, "assets", "art", "egne")
ORIG = os.path.join(HER, "originaler")
BREDDE = 1200
KVALITET = 82
ENDELSER = (".jpg", ".jpeg", ".png", ".webp")

os.makedirs(ORIG, exist_ok=True)

# 1) gem originaler (kun dem, der ikke allerede er gemt)
for fil in os.listdir(EGNE):
    navn, ext = os.path.splitext(fil)
    if ext.lower() in ENDELSER and not any(os.path.exists(os.path.join(ORIG, navn + e)) for e in ENDELSER):
        shutil.copy2(os.path.join(EGNE, fil), os.path.join(ORIG, fil))

# 2) skalér og komprimér ud fra originalerne
foer = efter = antal = 0
for fil in sorted(os.listdir(ORIG)):
    navn, ext = os.path.splitext(fil)
    if ext.lower() not in ENDELSER:
        continue
    with Image.open(os.path.join(ORIG, fil)) as img:
        img = img.convert("RGB")
        if img.width > BREDDE:
            img = img.resize((BREDDE, round(img.height * BREDDE / img.width)), Image.LANCZOS)
        for gammel in os.listdir(EGNE):  # kun én fil pr. scene (fx hvis originalen var .png)
            if os.path.splitext(gammel)[0] == navn:
                os.remove(os.path.join(EGNE, gammel))
        maal = os.path.join(EGNE, navn + ".jpg")
        img.save(maal, "JPEG", quality=KVALITET, optimize=True, progressive=True)
    foer += os.path.getsize(os.path.join(ORIG, fil))
    efter += os.path.getsize(maal)
    antal += 1

print(f"{antal} billeder komprimeret: {foer / 1e6:.1f} MB → {efter / 1e6:.1f} MB")
print("Kør nu: python tools/art/brug_egne.py")
