#!/usr/bin/env python3
"""Genera guia-nodus-sector-ii-vs-baltic-aquascaphe.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-nodus-sector-ii-vs-baltic-aquascaphe.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-relojes-con-cristal-de-zafiro"
TITLE = "Nodus Sector II Dive GMT vs Baltic Aquascaphe Mk2"
DESC = "Dos automáticos de microbrand con zafiro: Nodus Sector II GMT (480 €, 100 m) frente a Baltic Aquascaphe Mk2 (630 €, 200 m). Comparamos datos de nuestro catálogo."
ROWS = [
 ("Precio","480 €","630 €"),
 ("Movimiento","Automático Seiko (TMI) NH34 con función GMT","Automático Miyota 9039 (24 rubíes, hacking)"),
 ("Reserva de marcha","Unas 41 horas","42 horas"),
 ("Diámetro de caja","40 mm","39,5 mm"),
 ("Grosor","11,9 mm","12,9 mm"),
 ("Resistencia al agua","100 m","200 m"),
 ("Cristal","Zafiro","Zafiro doble domo con antirreflejante"),
 ("Correa","Brazalete de acero estilo Oyster con módulo NodeX","Caucho FKM (opción de brazalete de acero)"),
 ("Fondo","No indicado en nuestra ficha","Acero macizo atornillado (cerrado)"),
 ("Venta","Web de Nodus, envío desde EE. UU.","Solo en baltic-watches.com"),
]
FAQ = [
 ("¿Cuál es más barato, el Nodus Sector II o el Baltic Aquascaphe Mk2?",
  "El Nodus Sector II Dive GMT: 480 € frente a 630 € del Baltic en nuestro catálogo, es decir, 150 € menos."),
 ("¿Cuál aguanta mejor el agua?",
  "El Baltic Aquascaphe Mk2, con 200 m frente a los 100 m del Nodus. Los 100 m del Nodus bastan para nadar, según nuestra ficha."),
 ("¿Cuál tiene función GMT?",
  "El Nodus Sector II Dive GMT, que lleva una aguja dedicada para una segunda zona horaria. El Baltic no la tiene."),
 ("¿Cuál es más fino?",
  "El Nodus, con 11,9 mm frente a los 12,9 mm del Baltic. El Baltic es medio milímetro más pequeño de diámetro (39,5 mm frente a 40 mm)."),
 ("¿Los dos tienen cristal de zafiro?",
  "Sí. El Nodus lleva zafiro y el Baltic zafiro de doble domo con antirreflejante."),
 ("¿Dónde se compran?",
  "Ambos se venden directamente en la web de su marca, sin intermediarios. El Nodus se envía desde EE. UU. y, según nuestra ficha, el Baltic solo se vende en baltic-watches.com; en ambos casos pueden aplicarse aduanas e impuestos según el destino, y el servicio técnico depende de la propia marca."),
 ("¿Cuál recomendáis?",
  "Si viajas o trabajas con dos husos horarios y quieres la caja más fina, el Nodus. Si priorizas más resistencia al agua (200 m) y un diseño de buceo de inspiración clásica, el Baltic."),
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
  <h1 style="font-size:2rem;">Nodus Sector II Dive GMT vs Baltic Aquascaphe Mk2</h1>
  <p>Dos automáticos de microbrand con cristal de zafiro y estética de buceo, separados por 150 €. Los comparamos con los datos de nuestro catálogo.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-nodus-sector-ii-dive-gmt.html">Nodus Sector II Dive GMT</a></th><th><a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe Mk2</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Nodus Sector II</h2>
  <p>Cuesta 150 € menos, añade una segunda zona horaria con su movimiento GMT, es 1 mm más fino (11,9 mm) y su brazalete de acero incluye un módulo de ajuste NodeX para afinar el tamaño sin herramientas. Como contrapartida, sus 100 m quedan por debajo de los 200 m del Baltic.</p>
  <h2>3. Dónde gana el Baltic Aquascaphe Mk2</h2>
  <p>Duplica la resistencia al agua (200 m), es algo más compacto en diámetro (39,5 mm), lleva zafiro de doble domo y su movimiento Miyota 9039 tiene parada de segundero. No ofrece función GMT y cuesta más.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos se compran directamente a la marca, sin devolución tipo Amazon, con posibles aduanas fuera de la UE y con servicio técnico que depende de la propia marca. Si el concepto te es nuevo, lee <a href="/guia-que-es-un-microbrand.html">qué es un microbrand</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para viajar o trabajar con dos husos horarios: Nodus. Para más margen frente al agua y un diseño de inspiración clásica: Baltic. Más opciones en la <a href="/guia-relojes-con-cristal-de-zafiro.html">guía de relojes con zafiro</a> y en la <a href="/guia-mejores-relojes-buceo.html">de relojes de buceo</a>, o ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Nodus o Baltic? Lee la <a href="/{SLUG}">comparativa Nodus Sector II Dive GMT vs Baltic Aquascaphe Mk2</a>.</p>\n'
    for n in ["guia-que-es-un-microbrand.html","guia-mejores-relojes-buceo.html","guia-seiko-alpinist-vs-baltic-aquascaphe.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: relojes con zafiro</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Nodus vs Baltic</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
