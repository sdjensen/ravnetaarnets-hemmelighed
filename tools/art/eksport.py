"""Eksporterer alle scener fra SVG til JPEG (1200×675), så de loader hurtigt i spillet.

Kræver: Chrome installeret og at projektmappen serveres lokalt, fx
    python -m http.server 8123
Kør så fra projektmappen:
    python tools/art/eksport.py            # alle scener
    python tools/art/eksport.py heden      # kun de nævnte

Chrome åbner en lille side (uden vindue), der tegner hver SVG på et lærred og
skriver JPEG-data ind i siden; scriptet læser siden og gemmer .jpg-filerne
ved siden af .svg-filerne i assets/art/scenes/.
"""
import base64
import json
import os
import re
import subprocess
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.normpath(os.path.join(HER, "..", ".."))
SCENER = os.path.join(ROD, "assets", "art", "scenes")
SVG = os.path.join(HER, "svg")
PORT = os.environ.get("PORT", "8123")
KVALITET = 0.8
CHROME = next((p for p in (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium") if os.path.exists(p) or "/" not in p and "\\" not in p), None)

navne = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(SVG) if f.endswith(".svg"))

side = f"""<!doctype html><meta charset="utf-8"><body><script>
const navne = {json.dumps(navne)};
(async () => {{
  for (const n of navne) {{
    const img = new Image();
    img.src = '/tools/art/svg/' + n + '.svg';
    await img.decode();
    const c = document.createElement('canvas');
    c.width = 1200; c.height = 675;
    const g = c.getContext('2d');
    g.drawImage(img, 0, 0, 1200, 675);
    const pre = document.createElement('pre');
    pre.id = 'j-' + n;
    pre.textContent = c.toDataURL('image/jpeg', {KVALITET}).split(',')[1];
    document.body.appendChild(pre);
  }}
  document.title = 'faerdig';
}})();
</script>"""
sti = os.path.join(HER, "_eksport.html")
with open(sti, "w", encoding="utf-8") as f:
    f.write(side)

try:
    ud = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=120000",
                         "--dump-dom", f"http://localhost:{PORT}/tools/art/_eksport.html"],
                        capture_output=True, text=True, timeout=600).stdout
finally:
    os.remove(sti)

fundet = dict(re.findall(r'<pre id="j-([^"]+)">([A-Za-z0-9+/=]+)</pre>', ud))
for n in navne:
    if n not in fundet:
        print(f"MANGLER: {n}")
        continue
    data = base64.b64decode(fundet[n])
    with open(os.path.join(SCENER, n + ".jpg"), "wb") as f:
        f.write(data)
    print(f"{n}.jpg  {len(data) // 1024} KB")
print(f"{len(fundet)}/{len(navne)} scener eksporteret")
