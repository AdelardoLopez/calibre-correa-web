#!/usr/bin/env python3
"""Genera guia-orient-bambino-vs-citizen-tsuyosa.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-orient-bambino-vs-citizen-tsuyosa.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-5-sports-vs-citizen-tsuyosa"
PREV_LABEL = "Guía: Seiko 5 vs Tsuyosa"
TITLE = "Orient Bambino V5 vs Citizen Tsuyosa"
DESC = "Automáticos de vestir: Orient Bambino V5 (220 €, cristal mineral abombado) frente a Citizen Tsuyosa (329 €, zafiro, brazalete integrado). Datos del catálogo."
ROWS = [
 ("Precio","220 €","329 €"),
 ("Movimiento","Automático Orient Calibre F6724 (cuerda manual y parada de segundero)","Automático Citizen Calibre 8210"),
 ("Reserva de marcha","40 horas aprox.","40 horas"),
 ("Diámetro de caja","40,5 mm","40 mm"),
 ("Grosor","12 mm","≈ 12 mm"),
 ("Resistencia al agua","30 m","50 m"),
 ("Cristal","Mineral abombado","Zafiro con tratamiento antirreflejante"),
 ("Correa","Piel marrón","Brazalete integrado de acero"),
 ("Fondo","Transparente","Transparente"),
]
FAQ = [
 ("¿Cuál es más barato, el Orient Bambino V5 o el Citizen Tsuyosa?",
  "El Orient Bambino V5: 220 € frente a 329 € del Tsuyosa en nuestro catálogo, es decir, 109 € menos."),
 ("¿Cuál lleva cristal de zafiro?",
  "El Citizen Tsuyosa. El Orient Bambino V5 usa cristal mineral abombado, que da un aire vintage pero se raya con más facilidad que el zafiro."),
 ("¿Cuál resiste más el agua?",
  "El Citizen Tsuyosa, con 50 m frente a los 30 m del Bambino. Ninguno está pensado para nadar."),
 ("¿Cuál tiene más reserva de marcha?",
  "Empatan prácticamente: unas 40 horas el Orient y 40 horas el Citizen según nuestras fichas."),
 ("¿Cuál es mejor para vestir?",
  "Ambos son automáticos de vestir. El Bambino tiene un estilo clásico con cristal abombado y acabado PVD oro rosa; el Tsuyosa apuesta por el brazalete integrado y el zafiro. En nuestra valoración de diseño el Tsuyosa puntúa 9 sobre 10 y el Bambino 8."),
 ("¿Cuál es más robusto?",
  "En nuestro catálogo el Citizen Tsuyosa puntúa 6 sobre 10 en robustez y el Orient Bambino 5 sobre 10; ninguno es un reloj de uso deportivo."),
 ("¿Cuál recomendáis?",
  "Si buscas un vestir clásico con encanto vintage y quieres gastar lo mínimo, el Bambino. Si priorizas el zafiro, más resistencia al agua y el brazalete integrado, el Tsuyosa compensa los 109 € de diferencia."),
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
  <h1 style="font-size:2rem;">Orient Bambino V5 vs Citizen Tsuyosa</h1>
  <p>Dos automáticos japoneses de vestir con una diferencia de 109 € entre ellos. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-orient-bambino-v5.html">Orient Bambino V5 RA-AC0001S10A</a></th><th><a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa NJ0151-53M</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Orient Bambino V5</h2>
  <p>Cuesta 220 €, el más barato de esta comparativa. Su cristal abombado le da un aire vintage muy cuidado, el movimiento propio permite parar el segundero para ajustar la hora con precisión y el acabado PVD oro rosa es poco habitual a este precio. Como contrapartida, solo tiene 30 m de resistencia al agua, cristal mineral en lugar de zafiro y una correa de piel de fábrica que muchos usuarios acaban cambiando.</p>
  <h2>3. Dónde gana el Citizen Tsuyosa</h2>
  <p>Lleva cristal de zafiro, 50 m de resistencia al agua y un brazalete integrado en cuña muy cómodo, con proporciones que se perciben por encima de su gama. Como contrapartida, cuesta 109 € más, el brazalete integrado no admite cualquier correa de repuesto y el cierre no tiene micro-ajuste.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos son automáticos con fondo transparente, unas 40 horas de reserva de marcha, cajas de 40 a 40,5 mm y un grosor cercano a 12 mm. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; para más opciones elegantes, la <a href="/guia-mejores-relojes-vestir.html">guía de relojes de vestir</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para un vestir clásico con el menor gasto: Bambino. Para zafiro, más agua y brazalete integrado: Tsuyosa. También puedes comparar el Bambino con el <a href="/guia-orient-bambino-vs-seiko-presage.html">Seiko Presage</a> o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Bambino o Tsuyosa? Lee la <a href="/{SLUG}">comparativa Orient Bambino V5 vs Citizen Tsuyosa</a>.</p>\n'
    for n in ["guia-orient-bambino-vs-seiko-presage.html","guia-mejores-relojes-vestir.html","guia-relojes-automaticos-entrada.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Bambino vs Tsuyosa</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
