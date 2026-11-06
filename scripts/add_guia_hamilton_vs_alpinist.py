#!/usr/bin/env python3
"""Genera guia-hamilton-khaki-field-vs-seiko-alpinist.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-hamilton-khaki-field-vs-seiko-alpinist.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-presage-srpb41-vs-citizen-tsuyosa"
TITLE = "Hamilton Khaki Field Mechanical vs Seiko Alpinist SPB210"
DESC = "Dos relojes de campo: Hamilton Khaki Field Mechanical (575 €, cuerda manual, 80 h) frente a Seiko Alpinist SPB210 (650 €, automático, 200 m). Datos del catálogo."
ROWS = [
 ("Precio","575 €","650 €"),
 ("Movimiento","Manual (cuerda a mano) Hamilton Calibre H-50","Automático Seiko Calibre 6R35 (con cuerda manual)"),
 ("Reserva de marcha","80 horas","70 horas"),
 ("Diámetro de caja","38 mm","39,5 mm"),
 ("Grosor","9,5 mm","13,2 mm"),
 ("Resistencia al agua","50 m","200 m"),
 ("Cristal","Zafiro","Zafiro con antirreflejante"),
 ("Correa","NATO de tela verde","Piel marrón"),
 ("Fondo","Cerrado","Transparente"),
]
FAQ = [
 ("¿Cuál es más barato, el Hamilton Khaki Field Mechanical o el Seiko Alpinist SPB210?",
  "El Hamilton: 575 € frente a 650 € del Alpinist en nuestro catálogo, es decir, 75 € menos."),
 ("¿Cuál tiene más reserva de marcha?",
  "El Hamilton, con 80 horas frente a las 70 horas del Seiko según nuestras fichas."),
 ("¿Cuál es automático?",
  "El Seiko Alpinist SPB210 (calibre 6R35, que además admite cuerda manual). El Hamilton Khaki Field Mechanical es de cuerda manual: hay que darle cuerda a mano."),
 ("¿Cuál resiste más el agua?",
  "El Seiko Alpinist, con 200 m frente a 50 m del Hamilton. El Hamilton aguanta salpicaduras y lluvia, pero no está pensado para nadar."),
 ("¿Cuál es más fino y discreto bajo el puño?",
  "El Hamilton: 9,5 mm de grosor y 38 mm de diámetro frente a 13,2 mm y 39,5 mm del Alpinist."),
 ("¿Cuál recomendáis?",
  "Si buscas un reloj de campo fino, ligero y con la mayor reserva de marcha, el Hamilton. Si quieres automático, 200 m de resistencia y bisel interior con brújula para montaña, el Alpinist."),
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
  <h1 style="font-size:2rem;">Hamilton Khaki Field Mechanical vs Seiko Alpinist SPB210</h1>
  <p>Dos relojes de inspiración militar y de montaña con 75 € de diferencia, pero con filosofías distintas. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field Mechanical H69439931</a></th><th><a href="/reloj-seiko-alpinist-spb210.html">Seiko Prospex Alpinist SPB210</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Hamilton Khaki Field</h2>
  <p>Es el más fino (9,5 mm) y el más compacto (38 mm), con 80 horas de reserva de marcha y diseño militar atemporal de la relojería suiza. Cuesta 75 € menos. Como contrapartida, es de cuerda manual, solo resiste 50 m y su fondo cerrado no deja ver el movimiento.</p>
  <h2>3. Dónde gana el Seiko Alpinist</h2>
  <p>Es automático (con cuerda manual opcional), resiste 200 m, tiene fondo transparente y un bisel interior giratorio con brújula, una función útil en senderismo. Como contrapartida, es el más caro de nuestras recomendaciones y sus 13,2 mm de grosor se notan bajo el puño de una camisa; además, la correa de piel no es la mejor para el agua.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos llevan cristal de zafiro, cajas de menos de 40 mm y un aire de reloj de campo. Si dudas entre cuerda manual y automático, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; para otro cara a cara con el Alpinist, la <a href="/guia-seiko-alpinist-vs-baltic-aquascaphe.html">comparativa con el Baltic Aquascaphe</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para el día a día, un reloj fino y la ceremonia de darle cuerda: Hamilton. Para montaña, agua y comodidad sin dar cuerda: Alpinist. Si prefieres un automático más económico, mira la <a href="/guia-seiko-5-sports-vs-hamilton-khaki-field.html">comparativa Seiko 5 Sports vs Hamilton Khaki Field</a>, y ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Hamilton o Alpinist? Lee la <a href="/{SLUG}">comparativa Hamilton Khaki Field vs Seiko Alpinist</a>.</p>\n'
    for n in ["guia-seiko-5-sports-vs-hamilton-khaki-field.html","guia-seiko-alpinist-vs-baltic-aquascaphe.html","guia-tipos-de-movimiento.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Presage vs Tsuyosa</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Hamilton vs Alpinist</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
