#!/usr/bin/env python3
"""Genera guia-orient-bambino-vs-seiko-presage.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-orient-bambino-vs-seiko-presage.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-que-es-un-microbrand"
TITLE = "Orient Bambino V5 vs Seiko Presage SRPB41: cuál elegir"
DESC = "Comparamos dos relojes de vestir automáticos japoneses: Orient Bambino Versión 5 (220 €) y Seiko Presage SRPB41 (350 €). Caja, cristal, agua y reserva de marcha."
ROWS = [
 ("Precio","220 €","350 €"),
 ("Movimiento","Automático Orient F6724 (cuerda manual y parada de segundero)","Automático Seiko 4R35"),
 ("Reserva de marcha","40 horas aprox.","41 horas"),
 ("Diámetro de caja","40,5 mm","40,5 mm"),
 ("Grosor","12 mm","11,8 mm"),
 ("Resistencia al agua","30 m","50 m"),
 ("Cristal","Mineral abombado","Hardlex con forma de caja"),
 ("Correa","Piel marrón","Brazalete de acero"),
 ("Fondo","Transparente","Transparente"),
]
FAQ = [
 ("¿Cuál es más barato, el Orient Bambino o el Seiko Presage?",
  "En nuestro catálogo, el Orient Bambino Versión 5 cuesta 220 € y el Seiko Presage SRPB41, 350 €: una diferencia de 130 €."),
 ("¿Qué diferencia hay entre ambos en cristal y resistencia al agua?",
  "Ninguno lleva zafiro. El Orient usa cristal mineral abombado y aguanta 30 m; el Seiko usa Hardlex y llega a 50 m. En ambos casos es agua de salpicaduras, no para nadar."),
 ("¿Cuál es más fácil de ajustar?",
  "El Orient F6724 admite cuerda manual y tiene parada de segundero, lo que ayuda a poner la hora con precisión."),
 ("¿Cuál recomendáis?",
  "Si quieres entrar en lo clásico gastando lo mínimo, el Orient Bambino. Si valoras más el dial azul lacado y el brazalete de acero, el Seiko Presage."),
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
  <h1 style="font-size:2rem;">Orient Bambino V5 vs Seiko Presage SRPB41</h1>
  <p>Dos relojes de vestir automáticos japoneses con la misma caja de 40,5 mm. Los comparamos con los datos de nuestro catálogo para que veas qué te dan los 130 € de diferencia.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-orient-bambino-v5.html">Orient Bambino Versión 5</a></th><th><a href="/reloj-seiko-presage-srpb41.html">Seiko Presage SRPB41</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Orient</h2>
  <p>Cuesta 130 € menos, tiene cristal abombado de aire vintage y su calibre F6724 permite dar cuerda a mano y para el segundero al ajustar la hora. Es la entrada más barata a la relojería clásica del catálogo.</p>
  <h2>3. Dónde gana el Seiko</h2>
  <p>Tiene brazalete de acero, 50 m frente a 30 m y un dial azul con laca de siete capas, poco habitual a este precio. Su corona transmite mejor tacto al dar cuerda.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ninguno lleva zafiro y ninguno es para nadar. Si quieres zafiro en un vestir, mira el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a> o la <a href="/guia-mejores-relojes-vestir.html">guía de relojes de vestir</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Presupuesto ajustado y gusto clásico: Orient Bambino. Dial con carácter y brazalete: Seiko Presage. Puedes verlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Dudas entre dos relojes de vestir japoneses? Lee <a href="/{SLUG}">Orient Bambino vs Seiko Presage</a>.</p>\n'
    for n in ["guia-mejores-relojes-vestir.html","guia-seiko-vs-citizen.html","guia-mejores-relojes-baratos.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: qué es un microbrand</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Orient vs Seiko Presage</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
