#!/usr/bin/env python3
"""Cloudflare sirve /pagina (sin .html) y redirige /pagina.html. Este script deja canonical, og:url,
twitter:url, JSON-LD y sitemap apuntando a la URL real sin .html (index -> raíz). Idempotente.
Ejecutar tras crear páginas nuevas con los scripts add_guia_*.py."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
HOST = "https://calibre-correa.adelardo.workers.dev"
SKIP = {"googleaa8b9c4981793855.html"}
PAT = re.compile(re.escape(HOST) + r"/([a-z0-9-]+)\.html")
def repl(m):
    return HOST + "/" if m.group(1) == "index" else f"{HOST}/{m.group(1)}"
n = 0
for p in list(ROOT.glob("*.html")) + [ROOT/"sitemap.xml", ROOT/"robots.txt"]:
    if p.name in SKIP or not p.exists(): continue
    t = p.read_text(encoding="utf-8")
    t2 = PAT.sub(repl, t)
    if t2 != t: p.write_text(t2, encoding="utf-8"); n += 1
print(f"✓ {n} archivos actualizados")
