#!/usr/bin/env python3
"""Genera guia-seiko-vs-citizen.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-vs-citizen.html"
TITLE = "Seiko vs Citizen: cuál elegir (5 relojes comparados)"
DESC = "Comparamos Seiko y Citizen con cinco modelos de nuestro catálogo: movimiento, cristal, agua y precio, de 229 a 650 €. Cuál te conviene según el uso."
W = [
 ("reloj-seiko-5-sports.html","Seiko 5 Sports (SRPD)","229 €","Automático 4R36","Hardlex","100 m","42,5 mm"),
 ("reloj-citizen-promaster-eco-drive-diver.html","Citizen Promaster Eco-Drive Diver","229 €","Cuarzo solar E168","Mineral","200 m (ISO 6425)","44 mm"),
 ("reloj-citizen-tsuyosa.html","Citizen Tsuyosa","329 €","Automático 8210","Zafiro","50 m","40 mm"),
 ("reloj-seiko-presage-srpb41.html","Seiko Presage SRPB41","350 €","Automático 4R35","Hardlex","50 m","40,5 mm"),
 ("reloj-seiko-alpinist-spb210.html","Seiko Prospex Alpinist SPB210","650 €","Automático 6R35","Zafiro","200 m","39,5 mm"),
]
FAQ = [
 ("¿Es mejor Seiko o Citizen?",
  "Ninguna es mejor en todo. Seiko destaca en automáticos con mucha variedad de estilos; Citizen destaca en la tecnología Eco-Drive solar, que no necesita pila. Depende de si prefieres mecánica o comodidad."),
 ("¿Qué es Eco-Drive de Citizen?",
  "Es un cuarzo que se carga con luz. En el Promaster del catálogo aguanta hasta 6 meses a oscuras tras una carga completa, así que casi no requiere mantenimiento."),
 ("¿Qué Seiko automático es mejor para empezar?",
  "El Seiko 5 Sports (229 €): automático 4R36, 100 m de resistencia al agua y piezas fáciles de encontrar."),
 ("¿Cuál tiene zafiro, Seiko o Citizen?",
  "En nuestro catálogo, el Citizen Tsuyosa (329 €) y el Seiko Alpinist (650 €). El Seiko 5 y el Presage llevan Hardlex, y el Promaster, cristal mineral."),
]
def build():
    rows = "".join(f'<tr><td><a href="/{s}">{n}</a></td><td>{p}</td><td>{m}</td><td>{c}</td><td>{a}</td><td>{d}</td></tr>' for s,n,p,m,c,a,d in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{SLUG}","author":{"@type":"Organization","name":"Calibre & Correa"}},
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
    head = head.replace("guia-relojes-muneca-pequena.html", SLUG)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Seiko vs Citizen: cuál elegir</h1>
  <p>Son las dos marcas japonesas más recomendadas para empezar. Aquí las comparamos con los cinco modelos que tenemos en el catálogo, entre 229 y 650 €, para que veas qué da cada una a cada precio.</p>
  <h2>1. La diferencia de fondo</h2>
  <p>Seiko apuesta por el automático: movimientos mecánicos con estilos muy variados. Citizen aporta, además de automáticos como el 8210 del Tsuyosa, la tecnología solar Eco-Drive: cuarzo que se carga con luz y no necesita cambiar pila. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">qué movimiento elegir</a>.</p>
  <h2>2. Comparativa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Movimiento</th><th>Cristal</th><th>Agua</th><th>Caja</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>3. Qué elegir según el uso</h2>
  <ul>
   <li><strong>Primer automático:</strong> <a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a>, el más barato y con 100 m de agua.</li>
   <li><strong>Cero mantenimiento y agua:</strong> <a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster solar</a>, certificado de buceo, aunque su caja de 44 mm es grande para muñecas finas.</li>
   <li><strong>Zafiro y diseño actual:</strong> <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a>, con brazalete integrado a 329 €.</li>
   <li><strong>Para vestir con color:</strong> <a href="/reloj-seiko-presage-srpb41.html">Seiko Presage SRPB41</a>, dial azul lacado.</li>
   <li><strong>Aventura y mejor reserva de marcha:</strong> <a href="/reloj-seiko-alpinist-spb210.html">Seiko Alpinist</a>, 70 horas y 200 m.</li>
  </ul>
  <h2>4. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a>, por el zafiro y el acabado a 329 €. Si tu presupuesto es de 230 €, el Seiko 5 Sports. Compáralos en el <a href="/comparador.html">comparador</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        m = re.search(r"<url><loc>[^<]*guia-relojes-muneca-pequena\.html</loc>.*?</url>\n", t)
        assert m
        sm.write_text(t[:m.end()] + f'  <url><loc>{BASE}/{SLUG}</loc></url>\n' + t[m.end():], encoding="utf-8"); print("✓ sitemap")
    add = f'<p>¿Dudas entre marcas japonesas? Lee <a href="/{SLUG}">Seiko vs Citizen: cuál elegir</a>.</p>\n'
    for n in ["guia-mejores-relojes-baratos.html","guia-tipos-de-movimiento.html","guia-relojes-automaticos-entrada.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = '<a href="/guia-relojes-muneca-pequena.html">Guía: muñeca pequeña</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko vs Citizen</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
