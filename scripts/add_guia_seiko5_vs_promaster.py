#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-citizen-promaster-diver.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-citizen-promaster-diver.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-citizen-tsuyosa-vs-tissot-prx-quartz"
TITLE = "Seiko 5 Sports vs Citizen Promaster Diver: cuál elegir"
DESC = "Seiko 5 Sports automático y Citizen Promaster Eco-Drive Diver cuestan 229 € cada uno: comparamos movimiento, agua (100 m vs 200 m), tamaño y cristal."
ROWS = [
 ("Precio","229 €","229 €"),
 ("Movimiento","Automático Seiko 4R36","Cuarzo solar Citizen Eco-Drive E168"),
 ("Reserva de marcha","41 horas","Hasta 6 meses a oscuras tras carga completa"),
 ("Diámetro de caja","42,5 mm","44 mm"),
 ("Grosor","13,4 mm","12 mm"),
 ("Resistencia al agua","100 m","200 m (certificado ISO 6425)"),
 ("Cristal","Hardlex mineral","Mineral con antirreflejante"),
 ("Correa","Acero / NATO / caucho (según versión)","Poliuretano"),
 ("Fondo","Transparente","Cerrado"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Citizen Promaster Diver?",
  "En nuestro catálogo cuestan lo mismo: 229 € cada uno."),
 ("¿Cuál es automático y cuál solar?",
  "El Seiko 5 Sports es automático (calibre 4R36) y el Citizen Promaster es de cuarzo solar Eco-Drive (E168), que se carga con cualquier luz y no necesita pila ni cuerda."),
 ("¿Cuál aguanta mejor el agua?",
  "El Citizen Promaster: 200 m con certificación ISO 6425 y corona atornillada. El Seiko 5 Sports llega a 100 m, pero su corona no es de rosca y no es un reloj de inmersión certificado."),
 ("¿Cuál es más pequeño?",
  "El Seiko 5 Sports, con 42,5 mm frente a los 44 mm del Citizen. El Citizen es algo más fino (12 mm frente a 13,4 mm). Con muñeca fina, mide antes con la herramienta de talla."),
 ("¿Alguno tiene cristal de zafiro?",
  "Ninguno: el Seiko usa Hardlex mineral y el Citizen, cristal mineral con antirreflejante."),
 ("¿Cuál recomendáis?",
  "Si te atrae lo mecánico y ver el movimiento por el fondo transparente, el Seiko 5 Sports. Si quieres un diver certificado, con más resistencia al agua y sin mantenimiento de pila ni cuerda, el Citizen Promaster."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Citizen Promaster Diver</h1>
  <p>Dos relojes deportivos de buceo al mismo precio, 229 €, con filosofías opuestas: un automático mecánico y un cuarzo solar certificado. Los comparamos con los datos de nuestro catálogo.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports Automático (SRPD)</a></th><th><a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver BN0151-09L</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko 5 Sports</h2>
  <p>Es más pequeño (42,5 mm), tiene movimiento automático propio con fondo transparente y piezas y servicio técnico Seiko fáciles de encontrar. Su punto débil es el cristal Hardlex, que se raya más que un zafiro.</p>
  <h2>3. Dónde gana el Citizen Promaster</h2>
  <p>Llega a 200 m con certificación ISO 6425 y corona atornillada, y no necesita pila ni cuerda porque se carga con cualquier luz. A cambio, su caja de 44 mm es la más grande de la comparativa y el bisel es de aluminio, que se raya con más facilidad que uno cerámico.</p>
  <h2>4. Automático o solar</h2>
  <p>El automático ofrece el atractivo mecánico pero pide cuerda de uso y revisiones; el solar apenas exige mantenimiento. Si dudas, lee la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Primer automático, con estética de buceo y tamaño contenido: Seiko 5 Sports. Reloj de buceo certificado y sin mantenimiento: Citizen Promaster. Más opciones en la <a href="/guia-mejores-relojes-buceo.html">guía de mejores relojes de buceo</a> y en la <a href="/guia-mejores-relojes-baratos.html">de relojes baratos</a>, o ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko 5 Sports o Citizen Promaster Diver? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Citizen Promaster Diver</a>.</p>\n'
    for n in ["guia-mejores-relojes-buceo.html","guia-mejores-relojes-baratos.html","guia-seiko-vs-citizen.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Tsuyosa vs PRX Quartz</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 vs Promaster Diver</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
