#!/usr/bin/env python3
"""Genera guia-scurfa-diver-one-vs-citizen-promaster-diver.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-scurfa-diver-one-vs-citizen-promaster-diver.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-nodus-sector-ii-vs-baltic-aquascaphe"
TITLE = "Scurfa Diver One D1-500 vs Citizen Promaster Eco-Drive Diver"
DESC = "Dos divers de cuarzo: Scurfa Diver One D1-500 (345 €, 500 m, zafiro) frente a Citizen Promaster Eco-Drive (229 €, 200 m, solar). Datos de nuestro catálogo."
ROWS = [
 ("Precio","345 €","229 €"),
 ("Movimiento","Cuarzo suizo ETA F06.412 (HeavyDrive y PreciDrive)","Cuarzo solar Citizen Eco-Drive Calibre E168"),
 ("Energía","Pila (autonomía no indicada por la marca)","Luz: hasta 6 meses a oscuras tras carga completa"),
 ("Diámetro de caja","40 mm","44 mm"),
 ("Grosor","14,4 mm","12 mm"),
 ("Resistencia al agua","500 m","200 m (certificado ISO 6425)"),
 ("Cristal","Zafiro abombado con antirreflejante azul en la cara interior","Mineral con tratamiento antirreflejante"),
 ("Correa","Caucho de 20 mm","Poliuretano"),
 ("Venta","Solo en la web de Scurfa, envío desde Reino Unido","Enlace de compra en Amazon desde nuestra ficha"),
]
FAQ = [
 ("¿Cuál es más barato, el Scurfa Diver One o el Citizen Promaster?",
  "El Citizen Promaster Eco-Drive Diver: 229 € frente a 345 € del Scurfa en nuestro catálogo, es decir, 116 € menos."),
 ("¿Cuál resiste más el agua?",
  "El Scurfa Diver One D1-500, con 500 m frente a 200 m. El Citizen Promaster cuenta con certificación ISO 6425 de buceo, según nuestra ficha."),
 ("¿Cuál necesita cambiar la pila?",
  "El Scurfa lleva una pila convencional. El Citizen es solar Eco-Drive y se carga con cualquier luz, con hasta 6 meses de reserva a oscuras tras carga completa."),
 ("¿Cuál es mejor para muñecas pequeñas?",
  "El Scurfa tiene menos diámetro (40 mm frente a 44 mm), pero es más grueso (14,4 mm frente a 12 mm) y mide 47,7 mm entre asas. Conviene probar ambas medidas con nuestra herramienta de talla."),
 ("¿Cuál lleva cristal de zafiro?",
  "El Scurfa, con zafiro abombado. El Citizen usa cristal mineral con tratamiento antirreflejante."),
 ("¿Dónde se compran?",
  "El Scurfa se vende solo en la web de la marca, con envío desde Reino Unido y posibles aduanas e impuestos; en la fecha de nuestra ficha figuraba como a la espera de stock. El Citizen tiene enlace de compra en Amazon desde su ficha."),
 ("¿Cuál recomendáis?",
  "Si quieres el mayor margen de resistencia, zafiro y una caja de 40 mm, el Scurfa. Si prefieres no cambiar nunca la pila, la certificación ISO 6425 y el precio más bajo, el Citizen."),
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
  <h1 style="font-size:2rem;">Scurfa Diver One D1-500 vs Citizen Promaster Eco-Drive Diver</h1>
  <p>Dos relojes de buceo de cuarzo con enfoque de herramienta, separados por 116 €. Los comparamos con los datos de nuestro catálogo. Aún no hemos tenido el Scurfa en la muñeca: su ficha se basa en las especificaciones oficiales de la marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-scurfa-diver-one-d1-500.html">Scurfa Diver One D1-500</a></th><th><a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Scurfa Diver One</h2>
  <p>Triplica la resistencia al agua del Citizen (500 m frente a 200 m), lleva zafiro abombado y bisel de cerámica de 120 clics, y su caja de 40 mm es más compacta en diámetro que los 44 mm del Citizen. Como contrapartida, es más grueso (14,4 mm), usa pila y cuesta 116 € más.</p>
  <h2>3. Dónde gana el Citizen Promaster</h2>
  <p>Es solar: no necesita pila. Tiene certificación ISO 6425, corona atornillada, es más fino (12 mm) y cuesta 229 €. Como contrapartida, su cristal es mineral, su bisel de aluminio se raya con más facilidad y sus 44 mm no son aptos para muñecas finas.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos son de cuarzo, de uso robusto y con puntuación de robustez alta en nuestro catálogo (9 sobre 10). Si dudas entre cuarzo y mecánico, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; si el concepto de marca pequeña es nuevo, <a href="/guia-que-es-un-microbrand.html">qué es un microbrand</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para máxima resistencia y zafiro: Scurfa. Para olvidarte de la pila y gastar menos: Citizen. Más opciones en la <a href="/guia-mejores-relojes-buceo.html">guía de relojes de buceo</a> y en la <a href="/guia-relojes-muneca-pequena.html">de muñeca pequeña</a>, o ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Scurfa o Citizen? Lee la <a href="/{SLUG}">comparativa Scurfa Diver One D1-500 vs Citizen Promaster Eco-Drive Diver</a>.</p>\n'
    for n in ["guia-que-es-un-microbrand.html","guia-mejores-relojes-buceo.html","guia-seiko-5-sports-vs-citizen-promaster-diver.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Nodus vs Baltic</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Scurfa vs Promaster</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
