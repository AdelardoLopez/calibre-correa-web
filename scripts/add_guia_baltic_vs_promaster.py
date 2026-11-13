#!/usr/bin/env python3
"""Genera guia-nodus-sector-ii-vs-scurfa-diver-one.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-baltic-aquascaphe-vs-citizen-promaster-diver.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-nodus-sector-ii-vs-scurfa-diver-one"
PREV_LABEL = "Guía: Nodus vs Scurfa"
TITLE = "Baltic Aquascaphe MK2 vs Citizen Promaster Eco-Drive Diver"
DESC = "Dos divers de 200 m: Baltic Aquascaphe MK2 (630 €, automático, zafiro) frente a Citizen Promaster Eco-Drive (229 €, cuarzo solar, ISO 6425). Datos del catálogo."
ROWS = [
 ("Precio","630 €","229 €"),
 ("Movimiento","Automático Miyota 9039 (24 rubíes, hacking)","Cuarzo solar Citizen Eco-Drive Calibre E168"),
 ("Reserva de marcha","42 horas","Hasta 6 meses a oscuras tras carga completa"),
 ("Diámetro de caja","39,5 mm","44 mm"),
 ("Grosor","12,9 mm","12 mm"),
 ("Resistencia al agua","200 m","200 m (certificado ISO 6425)"),
 ("Cristal","Zafiro doble domo con antirreflejante","Mineral con tratamiento antirreflejante"),
 ("Correa","Caucho FKM (opción de brazalete de acero)","Poliuretano"),
 ("Fondo","Acero macizo atornillado (cerrado)","Cerrado"),
 ("Dónde se compra","Solo en baltic-watches.com (venta directa)","Enlace de compra de nuestra ficha"),
]
FAQ = [
 ("¿Cuál es más barato, el Baltic Aquascaphe MK2 o el Citizen Promaster Diver?",
  "El Citizen Promaster Eco-Drive Diver: 229 € frente a 630 € del Baltic en nuestro catálogo, 401 € menos."),
 ("¿Cuál resiste más el agua?",
  "Ambos indican 200 m. El Citizen, además, figura con certificación ISO 6425 de buceo en nuestra ficha."),
 ("¿Cuál es mejor para muñecas pequeñas?",
  "El Baltic, con 39,5 mm de caja frente a 44 mm del Citizen. El Citizen es el más grande del catálogo en diámetro."),
 ("¿Cuál tiene cristal de zafiro?",
  "El Baltic Aquascaphe MK2 lleva zafiro de doble domo. El Citizen usa cristal mineral con antirreflejante."),
 ("¿Cuál es automático y cuál no necesita pila?",
  "El Baltic es automático (Miyota 9039, 42 horas de reserva). El Citizen es de cuarzo solar Eco-Drive: se carga con la luz y llega a 6 meses a oscuras tras carga completa."),
 ("¿Cuál recomendáis?",
  "Para un diver automático de diseño vintage, zafiro y caja de 39,5 mm: Baltic, asumiendo la compra directa a la marca. Para un diver certificado, sin pila ni cuerda y mucho más barato: Citizen, aceptando la caja de 44 mm y el cristal mineral."),
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
  <h1 style="font-size:2rem;">Baltic Aquascaphe MK2 vs Citizen Promaster Eco-Drive Diver</h1>
  <p>Dos divers de 200 m con enfoques muy distintos: un automático vintage de microbrand francesa frente a un cuarzo solar certificado ISO 6425. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a></th><th><a href="/reloj-citizen-promaster-eco-drive-diver.html">Citizen Promaster Eco-Drive Diver</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Baltic</h2>
  <p>Es automático, lleva zafiro de doble domo, su caja de 39,5 mm es más manejable y su diseño recuerda a los relojes de buceo de los años 50-60. Como contrapartida, cuesta 401 € más y solo se vende en la web de la marca, de modo que conviene revisar envío, aduanas y servicio técnico antes de comprar.</p>
  <h2>3. Dónde gana el Citizen</h2>
  <p>Cuesta 229 €, tiene certificación ISO 6425, no necesita pila (hasta 6 meses de reserva a oscuras tras carga completa) y es algo más fino, con 12 mm. Como contrapartida, mide 44 mm, usa cristal mineral y su bisel es de aluminio, más propenso a rayarse que uno cerámico.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos resisten 200 m y tienen fondo cerrado. Para entender las implicaciones de comprar a una marca pequeña, lee <a href="/guia-que-es-un-microbrand.html">qué es un microbrand</a>; para más opciones, la <a href="/guia-mejores-relojes-buceo.html">guía de relojes de buceo</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Si priorizas diseño, zafiro y mecánico: Baltic. Si priorizas certificación, comodidad sin mantenimiento y precio: Citizen. También puedes ver el Baltic frente al <a href="/guia-nodus-sector-ii-vs-baltic-aquascaphe.html">Nodus Sector II</a> o el Citizen frente al <a href="/guia-scurfa-diver-one-vs-citizen-promaster-diver.html">Scurfa Diver One</a>, o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Baltic o Citizen? Lee la <a href="/{SLUG}">comparativa Baltic Aquascaphe MK2 vs Citizen Promaster Diver</a>.</p>\n'
    for n in ["guia-nodus-sector-ii-vs-baltic-aquascaphe.html","guia-scurfa-diver-one-vs-citizen-promaster-diver.html","guia-mejores-relojes-buceo.html","guia-seiko-alpinist-vs-baltic-aquascaphe.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Baltic vs Promaster Diver</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
