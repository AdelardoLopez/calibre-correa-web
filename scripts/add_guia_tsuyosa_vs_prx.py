#!/usr/bin/env python3
"""Genera guia-citizen-tsuyosa-vs-tissot-prx-quartz.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-citizen-tsuyosa-vs-tissot-prx-quartz.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-alpinist-vs-baltic-aquascaphe"
TITLE = "Citizen Tsuyosa vs Tissot PRX Quartz: cuál elegir"
DESC = "Citizen Tsuyosa automático (329 €) vs Tissot PRX Quartz (395 €): ambos con brazalete integrado y zafiro; cambian movimiento, grosor, agua y fondo."
ROWS = [
 ("Precio","329 €","395 €"),
 ("Movimiento","Automático Citizen 8210","Cuarzo suizo ETA F06.115"),
 ("Reserva de marcha","40 horas","No aplica (batería)"),
 ("Diámetro de caja","40 mm","40 x 39,5 mm (tonneau)"),
 ("Grosor","≈ 12 mm","10,4 mm"),
 ("Resistencia al agua","50 m","100 m"),
 ("Cristal","Zafiro con antirreflejante","Zafiro con antirreflejante"),
 ("Correa","Brazalete integrado de acero","Brazalete de acero de liberación rápida"),
 ("Fondo","Transparente","Cerrado"),
]
FAQ = [
 ("¿Cuál es más barato, el Citizen Tsuyosa o el Tissot PRX Quartz?",
  "En nuestro catálogo, el Tsuyosa cuesta 329 € y el PRX Quartz, 395 €: el Citizen es 66 € más barato."),
 ("¿Cuál es automático y cuál de cuarzo?",
  "El Tsuyosa es automático (calibre Citizen 8210) y el PRX es de cuarzo suizo (ETA F06.115). El cuarzo no necesita cuerda, pero requiere cambiar la batería cada varios años."),
 ("¿Cuál aguanta mejor el agua?",
  "El Tissot PRX Quartz, con 100 m frente a los 50 m del Tsuyosa. Con 50 m, el Citizen es justo para nadar, no para bucear."),
 ("¿Cuál es más fino?",
  "El PRX, con 10,4 mm de grosor frente a unos 12 mm del Tsuyosa. Los dos tienen una caja de en torno a 40 mm."),
 ("¿Cuál tiene fondo transparente?",
  "El Citizen Tsuyosa deja ver el movimiento por el fondo transparente. El Tissot PRX Quartz tiene el fondo cerrado."),
 ("¿Cuál recomendáis?",
  "Si te atrae la parte mecánica y quieres pagar menos, el Tsuyosa. Si prefieres un reloj más fino, con más resistencia al agua y sin preocuparte de la cuerda, el PRX Quartz."),
]
def build():
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in ROWS)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":URL,"author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/"guia-relojes-muneca-pequena.html").read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace("guia-relojes-muneca-pequena.html", SLUG).replace("guia-relojes-muneca-pequena", SLUG[:-5])
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Citizen Tsuyosa vs Tissot PRX Quartz</h1>
  <p>Dos relojes con brazalete integrado y cristal de zafiro por menos de 400 €: un automático japonés y un cuarzo suizo. Los comparamos con los datos de nuestro catálogo.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa NJ0151-53M</a></th><th><a href="/reloj-tissot-prx-quartz.html">Tissot PRX Quartz T137.410.11.041.00</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Citizen Tsuyosa</h2>
  <p>Cuesta 66 € menos, es automático y su fondo transparente deja ver el movimiento. Su brazalete integrado en cuña resulta muy cómodo y su acabado se percibe por encima de su gama.</p>
  <h2>3. Dónde gana el Tissot PRX Quartz</h2>
  <p>Es más fino (10,4 mm), llega a 100 m de resistencia al agua y, al ser de cuarzo suizo, ofrece precisión y mantenimiento mínimo. Su brazalete de liberación rápida facilita cambiarlo por una correa. Su diseño tonneau está inspirado en Gérald Genta.</p>
  <h2>4. Automático o cuarzo</h2>
  <p>El automático tiene el atractivo mecánico, pero pide más cuidado y revisiones; el cuarzo solo exige cambiar la batería cada varios años. Si dudas, lee la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Atracción por lo mecánico y presupuesto más ajustado: Tsuyosa. Reloj fino, más resistente al agua y sin complicaciones: PRX Quartz. Más opciones en la <a href="/guia-mejores-relojes-vestir.html">guía de mejores relojes de vestir</a>, o ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if URL not in t:
        m = re.search(rf"<url><loc>{re.escape(BASE)}/{PREV}</loc>.*?</url>\n", t)
        assert m
        sm.write_text(t[:m.end()] + f'  <url><loc>{URL}</loc></url>\n' + t[m.end():], encoding="utf-8"); print("✓ sitemap")
    add = f'<p>¿Citizen Tsuyosa o Tissot PRX Quartz? Lee la <a href="/{SLUG}">comparativa Citizen Tsuyosa vs Tissot PRX Quartz</a>.</p>\n'
    for n in ["guia-mejores-relojes-vestir.html","guia-tipos-de-movimiento.html","guia-cuando-pagar-mas-reloj.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Alpinist vs Aquascaphe</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Tsuyosa vs PRX Quartz</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
