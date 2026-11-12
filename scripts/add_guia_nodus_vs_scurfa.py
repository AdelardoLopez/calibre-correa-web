#!/usr/bin/env python3
"""Genera guia-nodus-sector-ii-vs-scurfa-diver-one.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-nodus-sector-ii-vs-scurfa-diver-one.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-orient-bambino-vs-citizen-tsuyosa"
PREV_LABEL = "Guía: Bambino vs Tsuyosa"
TITLE = "Nodus Sector II Dive GMT vs Scurfa Diver One D1-500"
DESC = "Dos divers de microbrand: Nodus Sector II Dive GMT (480 €, automático GMT, 100 m) frente a Scurfa Diver One D1-500 (345 €, cuarzo suizo, 500 m). Datos del catálogo."
ROWS = [
 ("Precio","480 €","345 €"),
 ("Movimiento","Automático Seiko (TMI) NH34 con función GMT","Cuarzo suizo ETA F06.412 (HeavyDrive y PreciDrive)"),
 ("Reserva de marcha","Unas 41 horas (según el calibre NH34)","Cuarzo con pila (autonomía no indicada por la marca)"),
 ("Diámetro de caja","40 mm","40 mm"),
 ("Grosor","11,9 mm","14,4 mm"),
 ("Resistencia al agua","100 m","500 m"),
 ("Cristal","Zafiro","Zafiro abombado con antirreflejante azul en la cara interior"),
 ("Correa","Brazalete de acero estilo Oyster con módulo de ajuste NodeX","Caucho de 20 mm"),
 ("Origen","Ensamblado en Los Ángeles (EE. UU.)","Marca británica, venta directa"),
 ("Garantía","No indicada en nuestra ficha","12 meses"),
]
FAQ = [
 ("¿Cuál es más barato, el Nodus Sector II Dive GMT o el Scurfa Diver One?",
  "El Scurfa Diver One D1-500: 345 € frente a 480 € del Nodus en nuestro catálogo, 135 € menos."),
 ("¿Cuál resiste más el agua?",
  "El Scurfa, con 500 m frente a los 100 m del Nodus. Los 100 m del Nodus son suficientes para nadar; los 500 m del Scurfa dan un margen muy superior."),
 ("¿Cuál tiene función GMT?",
  "El Nodus Sector II Dive GMT, con aguja dedicada para una segunda zona horaria. El Scurfa Diver One D1-500 no la incluye según su ficha."),
 ("¿Cuál es mecánico y cuál de cuarzo?",
  "El Nodus es automático (calibre Seiko NH34) y el Scurfa es de cuarzo suizo ETA F06.412, que no necesita más mantenimiento que cambiar la pila."),
 ("¿Cuál es más fino?",
  "El Nodus, con 11,9 mm frente a 14,4 mm del Scurfa. Ambos tienen caja de 40 mm."),
 ("¿Cuál recomendáis?",
  "Para viajar con dos husos horarios y un movimiento mecánico: Nodus. Para un diver de herramienta de cuarzo con 500 m y menos precio: Scurfa. Recuerda que ambos se venden directamente en la web de cada marca, con envío desde el extranjero."),
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
  <h1 style="font-size:2rem;">Nodus Sector II Dive GMT vs Scurfa Diver One D1-500</h1>
  <p>Dos divers de microbrand con caja de 40 mm y zafiro, pero con filosofías opuestas: automático con GMT frente a cuarzo de 500 m. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-nodus-sector-ii-dive-gmt.html">Nodus Sector II Dive GMT</a></th><th><a href="/reloj-scurfa-diver-one-d1-500.html">Scurfa Diver One D1-500 Original</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Nodus</h2>
  <p>Es automático, incluye una aguja GMT para una segunda zona horaria y es más fino (11,9 mm), con brazalete de acero y módulo de ajuste NodeX. Como contrapartida, cuesta 135 € más, solo llega a 100 m y su calibre NH34 tiene la precisión típica de la familia NH.</p>
  <h2>3. Dónde gana el Scurfa</h2>
  <p>Cuesta 345 €, resiste 500 m, lleva bisel de cerámica y cuarzo suizo que no requiere más mantenimiento que cambiar la pila. Como contrapartida, es de cuarzo, mide 14,4 mm de grosor con 47,7 mm entre asas y no tiene GMT.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos tienen caja de 40 mm, cristal de zafiro y se venden directamente en la web de la marca con envío desde el extranjero, de modo que conviene revisar aduanas, impuestos y servicio técnico antes de comprar. Para entender qué implica ese modelo, lee <a href="/guia-que-es-un-microbrand.html">qué es un microbrand</a>; para más opciones de agua, la <a href="/guia-mejores-relojes-buceo.html">guía de relojes de buceo</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Si viajas o quieres mecánico con GMT: Nodus. Si buscas un diver de herramienta con el máximo margen de agua y menos gasto: Scurfa. También puedes ver el Nodus frente al <a href="/guia-nodus-sector-ii-vs-baltic-aquascaphe.html">Baltic Aquascaphe</a> o el Scurfa frente al <a href="/guia-scurfa-diver-one-vs-citizen-promaster-diver.html">Citizen Promaster Diver</a>, o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Nodus o Scurfa? Lee la <a href="/{SLUG}">comparativa Nodus Sector II Dive GMT vs Scurfa Diver One</a>.</p>\n'
    for n in ["guia-nodus-sector-ii-vs-baltic-aquascaphe.html","guia-scurfa-diver-one-vs-citizen-promaster-diver.html","guia-mejores-relojes-buceo.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Nodus vs Scurfa</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
