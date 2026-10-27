#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-hamilton-khaki-field.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-hamilton-khaki-field.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-orient-bambino-vs-seiko-presage"
TITLE = "Seiko 5 Sports vs Hamilton Khaki Field Mechanical: cuál elegir"
DESC = "Comparamos el Seiko 5 Sports SRPD (229 €, automático) y el Hamilton Khaki Field Mechanical (575 €, cuerda manual): caja, cristal, agua y reserva de marcha."
ROWS = [
 ("Precio","229 €","575 €"),
 ("Movimiento","Automático Seiko 4R36","Manual (cuerda a mano) Hamilton H-50"),
 ("Reserva de marcha","41 horas","80 horas"),
 ("Diámetro de caja","42,5 mm","38 mm"),
 ("Grosor","13,4 mm","9,5 mm"),
 ("Resistencia al agua","100 m","50 m"),
 ("Cristal","Hardlex mineral","Zafiro"),
 ("Correa","Acero / NATO / caucho (según versión)","NATO de tela verde"),
 ("Fondo","Transparente","Cerrado"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Hamilton Khaki Field?",
  "En nuestro catálogo, el Seiko 5 Sports cuesta 229 € y el Hamilton Khaki Field Mechanical, 575 €: una diferencia de 346 €."),
 ("¿Cuál es automático y cuál de cuerda manual?",
  "El Seiko 5 Sports es automático (calibre 4R36) y se carga con el movimiento de la muñeca. El Hamilton es de cuerda manual (calibre H-50): hay que darle cuerda con la corona."),
 ("¿Cuál aguanta mejor el agua?",
  "El Seiko 5 Sports, con 100 m frente a los 50 m del Hamilton. Ninguno de los dos es un reloj de inmersión certificado."),
 ("¿Cuál tiene cristal de zafiro?",
  "El Hamilton Khaki Field Mechanical. El Seiko 5 Sports lleva Hardlex mineral, que se raya con más facilidad."),
 ("¿Cuál recomendáis?",
  "Si quieres tu primer automático con buena resistencia al agua y gastando poco, el Seiko 5 Sports. Si prefieres una caja fina de 38 mm, zafiro, 80 horas de reserva y no te importa darle cuerda, el Hamilton."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Hamilton Khaki Field Mechanical</h1>
  <p>Dos relojes de campo y uso diario con filosofías distintas: un automático japonés de 229 € y un manual suizo de 575 €. Los comparamos con los datos de nuestro catálogo.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports (SRPD)</a></th><th><a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field Mechanical</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko</h2>
  <p>Cuesta 346 € menos, es automático (no hay que darle cuerda a diario) y llega a 100 m de resistencia al agua. Además, las piezas y el servicio técnico de Seiko son fáciles de encontrar.</p>
  <h2>3. Dónde gana el Hamilton</h2>
  <p>Tiene cristal de zafiro, una reserva de marcha de 80 horas y una caja más fina (9,5 mm frente a 13,4 mm) y compacta, de 38 mm. Es una buena opción si tienes una muñeca pequeña; mira también la <a href="/guia-relojes-muneca-pequena.html">guía de relojes para muñeca pequeña</a>.</p>
  <h2>4. Automático o manual</h2>
  <p>El automático se carga solo mientras lo llevas puesto; el manual pide un gesto diario con la corona. Hay quien lo considera parte del encanto y quien lo ve una molestia. Si dudas, lee la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Primer automático, uso intenso y presupuesto contenido: Seiko 5 Sports. Caja pequeña, zafiro y gusto por lo manual: Hamilton. Puedes verlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko 5 Sports o Hamilton Khaki Field? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Hamilton Khaki Field</a>.</p>\n'
    for n in ["guia-relojes-automaticos-entrada.html","guia-tipos-de-movimiento.html","guia-relojes-muneca-pequena.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Orient vs Seiko Presage</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 Sports vs Hamilton</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
