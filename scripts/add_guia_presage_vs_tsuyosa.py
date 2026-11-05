#!/usr/bin/env python3
"""Genera guia-scurfa-diver-one-vs-citizen-promaster-diver.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-presage-srpb41-vs-citizen-tsuyosa.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-scurfa-diver-one-vs-citizen-promaster-diver"
TITLE = "Seiko Presage Cocktail Time SRPB41 vs Citizen Tsuyosa"
DESC = "Automáticos de vestir: Seiko Presage SRPB41 (350 €, dial azul, Hardlex) frente a Citizen Tsuyosa (329 €, zafiro, brazalete integrado). Datos del catálogo."
ROWS = [
 ("Precio","350 €","329 €"),
 ("Movimiento","Automático Seiko Calibre 4R35","Automático Citizen Calibre 8210"),
 ("Reserva de marcha","41 horas","40 horas"),
 ("Diámetro de caja","40,5 mm","40 mm"),
 ("Grosor","11,8 mm","≈ 12 mm"),
 ("Resistencia al agua","50 m","50 m"),
 ("Cristal","Hardlex con forma de caja","Zafiro con tratamiento antirreflejante"),
 ("Correa","Brazalete de acero","Brazalete integrado de acero"),
 ("Fondo","Transparente","Transparente"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko Presage SRPB41 o el Citizen Tsuyosa?",
  "El Citizen Tsuyosa: 329 € frente a 350 € del Presage en nuestro catálogo, es decir, 21 € menos."),
 ("¿Cuál lleva cristal de zafiro?",
  "El Citizen Tsuyosa. El Seiko Presage SRPB41 usa Hardlex, un cristal tratado más resistente que el mineral común pero que se raya más que el zafiro."),
 ("¿Cuál resiste más el agua?",
  "Empatan: ambos indican 50 m, suficiente para salpicaduras y lluvia pero no para nadar con confianza."),
 ("¿Cuál tiene más reserva de marcha?",
  "Prácticamente igual: 41 horas el Seiko y 40 horas el Citizen según nuestras fichas."),
 ("¿Cuál es mejor para el trabajo y la oficina?",
  "Ambos están pensados para vestir. El Presage destaca por su dial azul texturizado con laca de siete capas; el Tsuyosa por el brazalete integrado y el zafiro. En nuestra valoración de diseño el Tsuyosa y el Presage puntúan ambos 9 sobre 10."),
 ("¿Cuál es más robusto?",
  "En nuestro catálogo el Citizen Tsuyosa puntúa 6 sobre 10 en robustez y el Seiko Presage también 6 sobre 10; ninguno es un reloj de uso deportivo intensivo."),
 ("¿Cuál recomendáis?",
  "Si buscas un dial que llame la atención y una corona con buen tacto, el Presage. Si priorizas el zafiro, el brazalete integrado y pagar algo menos, el Tsuyosa."),
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
  <h1 style="font-size:2rem;">Seiko Presage Cocktail Time SRPB41 vs Citizen Tsuyosa</h1>
  <p>Dos automáticos japoneses de vestir con precios casi iguales, separados por 21 €. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-presage-srpb41.html">Seiko Presage Cocktail Time SRPB41</a></th><th><a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa NJ0151-53M</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko Presage</h2>
  <p>Su dial azul texturizado con siete capas de laca es poco habitual a este precio, y la corona tiene mucho par de apriete. Es la puerta de entrada a la línea Presage de Seiko. Como contrapartida, usa Hardlex en lugar de zafiro, tiene la reserva de marcha más ajustada de nuestras comparativas (41 horas) y cuesta 21 € más.</p>
  <h2>3. Dónde gana el Citizen Tsuyosa</h2>
  <p>Lleva cristal de zafiro, brazalete integrado en cuña muy cómodo y proporciones que se perciben por encima de su gama. Es algo más barato (329 €). Como contrapartida, el brazalete integrado no admite cualquier correa de repuesto y el cierre no tiene micro-ajuste.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos son automáticos con fondo transparente, 50 m de resistencia al agua y unos 40 mm de caja, con un grosor cercano a 12 mm. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; para más opciones elegantes, la <a href="/guia-mejores-relojes-vestir.html">guía de relojes de vestir</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para un dial con carácter: Presage. Para zafiro y brazalete integrado: Tsuyosa. Si tu presupuesto es menor, mira la <a href="/guia-orient-bambino-vs-seiko-presage.html">comparativa Orient Bambino vs Seiko Presage</a>, y ponlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Presage o Tsuyosa? Lee la <a href="/{SLUG}">comparativa Seiko Presage SRPB41 vs Citizen Tsuyosa</a>.</p>\n'
    for n in ["guia-mejores-relojes-vestir.html","guia-orient-bambino-vs-seiko-presage.html","guia-citizen-tsuyosa-vs-tissot-prx-quartz.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Scurfa vs Promaster</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Presage vs Tsuyosa</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
