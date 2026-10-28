#!/usr/bin/env python3
"""Genera guia-seiko-alpinist-vs-baltic-aquascaphe.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-alpinist-vs-baltic-aquascaphe.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-5-sports-vs-hamilton-khaki-field"
TITLE = "Seiko Alpinist SPB210 vs Baltic Aquascaphe Mk2: cuál elegir"
DESC = "Seiko Prospex Alpinist SPB210 (650 €) vs Baltic Aquascaphe Mk2 (630 €): ambos automáticos de 39,5 mm, zafiro y 200 m; cambian reserva de marcha, fondo y compra."
ROWS = [
 ("Precio","650 €","630 €"),
 ("Movimiento","Automático Seiko 6R35 (con cuerda manual)","Automático Miyota 9039 (24 rubíes, hacking)"),
 ("Reserva de marcha","70 horas","42 horas"),
 ("Diámetro de caja","39,5 mm","39,5 mm"),
 ("Grosor","13,2 mm","12,9 mm"),
 ("Resistencia al agua","200 m","200 m"),
 ("Cristal","Zafiro con antirreflejante","Zafiro doble domo con antirreflejante"),
 ("Correa","Piel marrón","Caucho FKM (opción de brazalete de acero)"),
 ("Fondo","Transparente","Acero macizo atornillado (cerrado)"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko Alpinist o el Baltic Aquascaphe?",
  "En nuestro catálogo, el Alpinist SPB210 cuesta 650 € y el Aquascaphe Mk2, 630 €: solo 20 € de diferencia, así que el precio no decide."),
 ("¿Cuál tiene más reserva de marcha?",
  "El Seiko Alpinist, con 70 horas frente a las 42 del Baltic. Es una diferencia notable si lo dejas parado un fin de semana."),
 ("¿Cuál tiene brújula?",
  "El Seiko Alpinist, con un bisel interior giratorio con brújula. El Baltic Aquascaphe es un reloj de buceo de estilo clásico, sin esa función."),
 ("¿Los dos aguantan 200 m?",
  "Sí, ambos tienen 200 m de resistencia al agua. El Baltic viene con correa de caucho FKM; el Alpinist, con piel, que no es la mejor opción para nadar o bucear."),
 ("¿Dónde se compra cada uno?",
  "El Aquascaphe solo se vende en la web de la marca (baltic-watches.com), con lo que implica en envíos, aduanas fuera de la UE y servicio técnico. El Seiko es más fácil de encontrar y tiene servicio técnico Seiko."),
 ("¿Cuál recomendáis?",
  "Si vas a la montaña y quieres brújula y 70 horas de reserva, el Alpinist. Si prefieres un diseño de buceo vintage, caucho y apoyar a un microbrand, el Baltic."),
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
  <h1 style="font-size:2rem;">Seiko Alpinist SPB210 vs Baltic Aquascaphe Mk2</h1>
  <p>Dos automáticos de 39,5 mm con zafiro y 200 m de resistencia al agua, a solo 20 € de distancia. Uno es un clásico japonés de montaña; el otro, un microbrand de inspiración buceo vintage. Los comparamos con los datos de nuestro catálogo.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-alpinist-spb210.html">Seiko Alpinist SPB210</a></th><th><a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe Mk2</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko Alpinist</h2>
  <p>Tiene 70 horas de reserva de marcha frente a 42, y un bisel interior giratorio con brújula, una función útil al aire libre. El 6R35 admite además cuerda manual. Y es más fácil de comprar y de llevar a servicio técnico.</p>
  <h2>3. Dónde gana el Baltic Aquascaphe</h2>
  <p>Su cristal de zafiro de doble domo y su diseño inspirado en los relojes de buceo de los años 50-60 son lo más comentado. Es algo más fino (12,9 mm frente a 13,2 mm), trae caucho FKM más adecuado para el agua y el Miyota 9039 incluye parada de segundero. Cuesta 20 € menos.</p>
  <h2>4. Comprar a un gran fabricante o a un microbrand</h2>
  <p>El Baltic se vende solo en la web de la marca: sin devolución tipo Amazon ni tienda física, con posibles costes de envío y aduanas fuera de la UE, y con servicio técnico dependiente de la propia marca. Si dudas, lee la <a href="/guia-que-es-un-microbrand.html">guía sobre qué es un microbrand</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Senderismo, montaña y reserva de marcha larga: Alpinist. Estética de buceo clásico, caucho y ganas de salirte de las marcas grandes: Baltic. Para más opciones de agua, mira la <a href="/guia-mejores-relojes-buceo.html">guía de mejores relojes de buceo</a> o ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko Alpinist o Baltic Aquascaphe? Lee la <a href="/{SLUG}">comparativa Seiko Alpinist SPB210 vs Baltic Aquascaphe Mk2</a>.</p>\n'
    for n in ["guia-mejores-relojes-buceo.html","guia-que-es-un-microbrand.html","guia-cuando-pagar-mas-reloj.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Seiko 5 Sports vs Hamilton</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Alpinist vs Aquascaphe</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
