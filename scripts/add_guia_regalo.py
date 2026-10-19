#!/usr/bin/env python3
"""Genera guia-mejores-relojes-regalo-hombre.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-mejores-relojes-regalo-hombre.html"
TITLE = "Mejores relojes para regalar a un hombre (2026)"
DESC = "Qué reloj regalar según el presupuesto: de 229 a 650 €, con modelos de nuestro catálogo, qué mirar al regalar un reloj y cuál elegir en cada caso."
W = [
 ("reloj-seiko-5-sports.html","Seiko 5 Sports (SRPD)","229 €","Hasta 250 €","Automático deportivo que aguanta 100 m. Acierto seguro si no conoces sus gustos."),
 ("reloj-citizen-tsuyosa.html","Citizen Tsuyosa","329 €","250–400 €","Brazalete integrado y zafiro por poco más de 300 €. El regalo que parece de más precio."),
 ("reloj-seiko-presage-srpb41.html","Seiko Presage Cocktail Time SRPB41","350 €","250–400 €","Dial azul lacado: llama la atención y vale para vestir."),
 ("reloj-tissot-prx-quartz.html","Tissot PRX Cuarzo","395 €","250–400 €","Marca suiza reconocida y cero mantenimiento: ideal si no quieres que se pare."),
 ("reloj-hamilton-khaki-field-mechanical.html","Hamilton Khaki Field Mechanical","575 €","400–700 €","Suizo, 80 horas de reserva y 38 mm. Para quien aprecia la mecánica."),
 ("reloj-seiko-alpinist-spb210.html","Seiko Prospex Alpinist SPB210","650 €","400–700 €","El más premium: zafiro, 200 m y bisel interior con brújula. Para aventureros."),
]
FAQ = [
 ("¿Qué reloj regalar a un hombre si no sé sus gustos?",
  "Uno versátil y de tamaño medio: el Seiko 5 Sports (229 €) por precio, o el Citizen Tsuyosa (329 €) si quieres cristal de zafiro y un diseño que sirve tanto con camisa como con vaqueros."),
 ("¿Cuánto gastar en un reloj de regalo?",
  "Entre 230 y 400 € ya hay relojes con buen movimiento y buenos acabados. Por encima de 500 € se paga sobre todo marca, zafiro y reserva de marcha más larga."),
 ("¿Automático o cuarzo para regalar?",
  "El automático gusta más a quien disfruta de la mecánica, pero necesita ponerse en hora si se para. El cuarzo (como el Tissot PRX) o el solar no piden mantenimiento diario."),
 ("¿Cómo acertar con la talla?",
  "Mira el reloj que ya usa o su muñeca: de 38 a 40 mm sirve a casi todo el mundo. Puedes comprobarlo con la herramienta de talla de la web."),
]
def build():
    rows = "".join(f'<tr><td><a href="/{s}">{n}</a></td><td>{p}</td><td>{b}</td></tr>' for s,n,p,b,_ in W)
    picks = "".join(f'<li><a href="/{s}"><strong>{n}</strong></a> ({p}): {v}</li>' for s,n,p,b,v in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":f"{BASE}/{SLUG}","author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/"guia-mejores-relojes-baratos.html").read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace("guia-mejores-relojes-baratos.html", SLUG)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Mejores relojes para regalar a un hombre en 2026</h1>
  <p>Un reloj es un regalo que se usa cada día y dura años. Esta guía te ayuda a elegir según el presupuesto, con seis modelos de nuestro catálogo entre 229 y 650 €.</p>
  <h2>1. Qué mirar antes de regalar un reloj</h2>
  <p>Tres cosas importan más que la marca: el uso (diario, vestir o aventura), el tamaño (38–40 mm sirve a casi todos; usa la <a href="/herramienta-talla-reloj.html">herramienta de talla</a> si dudas) y el mantenimiento (un automático se para si no se lleva; un cuarzo o solar, no).</p>
  <h2>2. Comparativa por presupuesto</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Tramo</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>3. Nuestra recomendación</h2>
  <p>Si solo quieres una respuesta: el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a> (329 €). Tiene zafiro, brazalete integrado y automático, y entra en un presupuesto de regalo razonable. Si quieres gastar menos, el <a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a> (229 €).</p>
  <ul>{picks}</ul>
  <p>Compáralos en el <a href="/comparador.html">comparador</a>. Si buscas algo más barato, mira la <a href="/guia-mejores-relojes-baratos.html">guía de relojes por menos de 250€</a>; para vestir, la <a href="/guia-mejores-relojes-vestir.html">guía de relojes de vestir</a>.</p>
  <h2>Preguntas frecuentes</h2>
  {faq_html}
</article>'''
    return head + body + tail

def main():
    (ROOT/SLUG).write_text(build(), encoding="utf-8"); print("✓", SLUG)
    sm = ROOT/"sitemap.xml"; t = sm.read_text(encoding="utf-8")
    if SLUG not in t:
        m = re.search(r"<url><loc>[^<]*guia-mejores-relojes-baratos\.html</loc>.*?</url>\n", t)
        assert m
        sm.write_text(t[:m.end()] + f'  <url><loc>{BASE}/{SLUG}</loc></url>\n' + t[m.end():], encoding="utf-8"); print("✓ sitemap")
    add = f'<p>¿Buscas un regalo? Mira la <a href="/{SLUG}">guía de relojes para regalar a un hombre</a>.</p>\n'
    for n in ["guia-mejores-relojes-baratos.html","guia-mejores-relojes-vestir.html","guia-cuando-pagar-mas-reloj.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        t = t.replace("</article>", add+"</article>",1)
        p.write_text(t, encoding="utf-8"); print("✓ enlace en", n)
    old = '<a href="/guia-mejores-relojes-baratos.html">Guía: relojes por menos de 250€</a>'
    new = old + f'\n      <a href="/{SLUG}">Guía: relojes para regalar</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,new),encoding="utf-8")
if __name__ == "__main__": main()
