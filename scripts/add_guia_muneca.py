#!/usr/bin/env python3
"""Genera guia-relojes-muneca-pequena.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-relojes-muneca-pequena.html"
TITLE = "Mejores relojes para muñeca pequeña (38-40 mm)"
DESC = "Relojes de nuestro catálogo de 38 a 40,5 mm y de menos de 13 mm de grosor, ideales para muñeca pequeña o fina. Medidas reales y cuál elegir."
W = [
 ("reloj-hamilton-khaki-field-mechanical.html","Hamilton Khaki Field Mechanical","575 €","38 mm","9,5 mm","El más pequeño y fino de la lista: perfecto para muñeca fina."),
 ("reloj-seiko-alpinist-spb210.html","Seiko Prospex Alpinist SPB210","650 €","39,5 mm","13,2 mm","39,5 mm con 200 m: deportivo sin ser grande."),
 ("reloj-baltic-aquascaphe-mk2.html","Baltic Aquascaphe MK2","630 €","39,5 mm","12,9 mm","Diver vintage de tamaño contenido."),
 ("reloj-tissot-prx-quartz.html","Tissot PRX Cuarzo","395 €","40 x 39,5 mm","10,4 mm","Brazalete integrado y muy fino: asienta bien en muñecas pequeñas."),
 ("reloj-citizen-tsuyosa.html","Citizen Tsuyosa","329 €","40 mm","≈ 12 mm","Buena relación tamaño-precio con zafiro."),
 ("reloj-orient-bambino-v5.html","Orient Bambino Versión 5","220 €","40,5 mm","—","El más barato; clásico de vestir."),
]
FAQ = [
 ("¿Qué tamaño de reloj es mejor para muñeca pequeña?",
  "Como regla general, entre 36 y 40 mm. En nuestro catálogo el más pequeño es el Hamilton Khaki Field (38 mm) y varios llegan a 39,5 o 40 mm."),
 ("¿Importa el grosor además del diámetro?",
  "Sí. Un reloj fino se ve más pequeño en la muñeca. El Hamilton (9,5 mm) y el Tissot PRX (10,4 mm) son los más finos de la lista."),
 ("¿Un reloj de 40 mm es demasiado grande para muñeca pequeña?",
  "No necesariamente: depende también de la distancia entre asas y del diseño. Un brazalete integrado como el del Tissot PRX o el Tsuyosa se ajusta mejor que una caja con asas largas."),
 ("¿Cómo sé qué talla me conviene?",
  "Mide tu muñeca y usa la herramienta de talla de la web para ver el rango de diámetro recomendado."),
]
def build():
    rows = "".join(f'<tr><td><a href="/{s}">{n}</a></td><td>{p}</td><td>{d}</td><td>{g}</td></tr>' for s,n,p,d,g,_ in W)
    picks = "".join(f'<li><a href="/{s}"><strong>{n}</strong></a> ({d}): {v}</li>' for s,n,p,d,g,v in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{SLUG}","author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/"guia-mejores-relojes-regalo-hombre.html").read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace("guia-mejores-relojes-regalo-hombre.html", SLUG)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Mejores relojes para muñeca pequeña</h1>
  <p>Con la muñeca fina, un reloj de 44 mm queda desproporcionado. Esta guía reúne los modelos de nuestro catálogo de entre 38 y 40,5 mm, con su grosor, para que elijas uno que quede bien.</p>
  <h2>1. Diámetro y grosor: qué mirar</h2>
  <p>El diámetro marca el tamaño visible, pero el grosor decide si el reloj se ve "alto" sobre la muñeca. Para muñeca pequeña busca 36–40 mm y, si puedes, menos de 13 mm de grosor. La <a href="/herramienta-talla-reloj.html">herramienta de talla</a> calcula el rango según tu muñeca.</p>
  <h2>2. Comparativa por tamaño</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Caja</th><th>Grosor</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>3. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field Mechanical</a>, el más compacto y fino. Si tu presupuesto es menor, el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a> (329 €).</p>
  <ul>{picks}</ul>
  <p>Compáralos en el <a href="/comparador.html">comparador</a>. También te puede interesar la <a href="/guia-mejores-relojes-regalo-hombre.html">guía de relojes para regalar</a> y la de <a href="/guia-mejores-relojes-vestir.html">relojes de vestir</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        m = re.search(r"<url><loc>[^<]*guia-mejores-relojes-regalo-hombre\.html</loc>.*?</url>\n", t)
        assert m
        sm.write_text(t[:m.end()] + f'  <url><loc>{BASE}/{SLUG}</loc></url>\n' + t[m.end():], encoding="utf-8"); print("✓ sitemap")
    add = f'<p>¿Muñeca pequeña? Mira la <a href="/{SLUG}">guía de relojes de 38 a 40 mm</a>.</p>\n'
    for n in ["guia-mejores-relojes-regalo-hombre.html","guia-mejores-relojes-vestir.html","guia-relojes-automaticos-entrada.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    # herramienta de talla: enlace desde su cabecera
    p = ROOT/"herramienta-talla-reloj.html"; t = p.read_text(encoding="utf-8")
    if SLUG not in t:
        new = re.sub(r'(<div class="section-head"><h1>[^<]*</h1><div class="sub">[^<]*)(</div></div>)',
                     lambda m: m.group(1)+f' <a href="/{SLUG}">Ver relojes para muñeca pequeña</a>.'+m.group(2), t, 1)
        if new != t: p.write_text(new, encoding="utf-8"); print("✓ enlace en herramienta")
    old = '<a href="/guia-mejores-relojes-regalo-hombre.html">Guía: relojes para regalar</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: muñeca pequeña</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
