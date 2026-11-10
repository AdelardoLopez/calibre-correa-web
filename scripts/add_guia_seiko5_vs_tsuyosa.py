#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-citizen-tsuyosa.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-citizen-tsuyosa.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-5-sports-vs-tissot-prx-quartz"
PREV_LABEL = "Guía: Seiko 5 vs PRX"
TITLE = "Seiko 5 Sports vs Citizen Tsuyosa"
DESC = "Seiko 5 Sports SRPD (229 €) frente a Citizen Tsuyosa NJ0151-53M (329 €), ambos automáticos. Agua, cristal, medidas y reserva de marcha con datos del catálogo."
ROWS = [
 ("Precio","229 €","329 €"),
 ("Movimiento","Automático Seiko Calibre 4R36","Automático Citizen Calibre 8210"),
 ("Reserva de marcha","41 horas","40 horas"),
 ("Diámetro de caja","42,5 mm","40 mm"),
 ("Grosor","13,4 mm","≈ 12 mm"),
 ("Resistencia al agua","100 m","50 m"),
 ("Cristal","Hardlex mineral","Zafiro con tratamiento antirreflejante"),
 ("Correa","Acero inoxidable / NATO / caucho (según versión)","Brazalete integrado de acero"),
 ("Fondo","Transparente (visible el movimiento)","Transparente (visible el movimiento)"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Citizen Tsuyosa?",
  "El Seiko 5 Sports: 229 € frente a 329 € del Tsuyosa en nuestro catálogo, es decir, 100 € menos."),
 ("¿Cuál resiste más el agua?",
  "El Seiko 5 Sports, con 100 m frente a 50 m del Tsuyosa. Con 50 m el Tsuyosa vale para salpicaduras y nadar con calma, pero no para bucear."),
 ("¿Cuál tiene cristal de zafiro?",
  "El Citizen Tsuyosa, con antirreflejante. El Seiko 5 Sports lleva cristal Hardlex mineral, que se raya con más facilidad."),
 ("¿Cuál es más pequeño y cómodo?",
  "El Citizen Tsuyosa: 40 mm de caja y unos 12 mm de grosor, frente a 42,5 mm y 13,4 mm del Seiko."),
 ("¿Los dos son automáticos?",
  "Sí. El Seiko usa el calibre 4R36 (41 horas de reserva) y el Citizen el 8210 (40 horas); ambos tienen fondo transparente."),
 ("¿Cuál recomendáis?",
  "Si quieres el automático más barato y con más resistencia al agua, el Seiko 5 Sports. Si priorizas zafiro, caja más compacta y un brazalete integrado de diseño, el Citizen Tsuyosa."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Citizen Tsuyosa</h1>
  <p>Dos automáticos japoneses de entrada con 100 € de diferencia y enfoques distintos: un deportivo clásico frente a un reloj de brazalete integrado. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports Automático (SRPD)</a></th><th><a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa Automático NJ0151-53M</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko 5 Sports</h2>
  <p>Es 100 € más barato y duplica la resistencia al agua (100 m frente a 50 m). Hay piezas y servicio técnico Seiko fáciles de encontrar y versiones con acero, NATO o caucho. Como contrapartida, su cristal Hardlex se raya más que un zafiro, es más grande y grueso (42,5 mm y 13,4 mm) y su precisión es de gama de entrada.</p>
  <h2>3. Dónde gana el Citizen Tsuyosa</h2>
  <p>Tiene cristal de zafiro con antirreflejante, una caja de 40 mm y unos 12 mm de grosor, y un brazalete integrado que las reseñas destacan por su acabado a este precio. Como contrapartida, cuesta 329 €, solo resiste 50 m, el brazalete no admite cualquier correa de repuesto y el cierre no tiene micro-ajuste.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos son automáticos con unas 40 horas de reserva y fondo transparente. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; para el Tsuyosa frente a otro modelo, mira <a href="/guia-seiko-presage-srpb41-vs-citizen-tsuyosa.html">Presage SRPB41 vs Citizen Tsuyosa</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para uso deportivo, agua y el mejor precio: Seiko 5 Sports. Para oficina y diario, con zafiro y un diseño más personal: Citizen Tsuyosa. Más opciones en <a href="/guia-relojes-automaticos-entrada.html">automáticos de entrada</a>, y puedes ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko 5 Sports o Citizen Tsuyosa? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Citizen Tsuyosa</a>.</p>\n'
    for n in ["guia-seiko-presage-srpb41-vs-citizen-tsuyosa.html","guia-seiko-5-sports-vs-tissot-prx-quartz.html","guia-relojes-automaticos-entrada.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 vs Tsuyosa</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
