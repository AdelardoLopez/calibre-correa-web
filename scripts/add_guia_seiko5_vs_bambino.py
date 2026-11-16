#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-orient-bambino-v5.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-orient-bambino-v5.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-baltic-aquascaphe-vs-citizen-promaster-diver"
PREV_LABEL = "Guía: Baltic vs Promaster Diver"
TITLE = "Seiko 5 Sports vs Orient Bambino V5"
DESC = "Dos automáticos japoneses de entrada: Seiko 5 Sports SRPD (229 €, 100 m, deportivo) frente a Orient Bambino V5 (220 €, 30 m, vestir). Datos del catálogo."
ROWS = [
 ("Precio","229 €","220 €"),
 ("Movimiento","Automático Seiko Calibre 4R36","Automático Orient Calibre F6724 (con cuerda manual y parada de segundero)"),
 ("Reserva de marcha","41 horas","40 horas aprox."),
 ("Diámetro de caja","42,5 mm","40,5 mm"),
 ("Grosor","13,4 mm","12 mm"),
 ("Resistencia al agua","100 m","30 m"),
 ("Cristal","Hardlex mineral","Mineral abombado"),
 ("Correa","Acero inoxidable / NATO / caucho (según versión)","Piel marrón"),
 ("Fondo","Transparente (visible el movimiento)","Transparente (visible el movimiento)"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Orient Bambino V5?",
  "El Orient Bambino V5: 220 € frente a 229 € del Seiko 5 Sports en nuestro catálogo, 9 € menos."),
 ("¿Cuál resiste más el agua?",
  "El Seiko 5 Sports, con 100 m frente a 30 m del Bambino. Con el Bambino conviene evitar nadar o sumergirlo."),
 ("¿Cuál es mejor para muñecas pequeñas?",
  "El Orient Bambino V5, con 40,5 mm de caja y 12 mm de grosor, frente a 42,5 mm y 13,4 mm del Seiko."),
 ("¿Cuál es mejor para vestir?",
  "El Bambino, con cristal abombado, caja PVD oro rosa y correa de piel. El Seiko 5 Sports tiene estética deportiva de buceo."),
 ("¿Tienen cristal de zafiro?",
  "Ninguno. El Seiko usa Hardlex mineral y el Orient, mineral abombado."),
 ("¿Cuál recomendáis?",
  "Para un reloj de uso diario, más resistente al agua y de estilo deportivo: Seiko 5 Sports. Para un reloj de vestir de aire vintage, más pequeño y fino: Orient Bambino V5, asumiendo sus 30 m de resistencia al agua."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Orient Bambino V5</h1>
  <p>Dos automáticos japoneses de entrada con casi el mismo precio y personalidades opuestas: uno deportivo y resistente, el otro de vestir y de aire vintage. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a></th><th><a href="/reloj-orient-bambino-v5.html">Orient Bambino V5</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko 5 Sports</h2>
  <p>Resiste 100 m, así que aguanta lluvia, ducha y baño sin problemas, y ofrece versiones con brazalete de acero, NATO o caucho. Como contrapartida, es más grande (42,5 mm) y más grueso (13,4 mm), y su cristal Hardlex se raya más que un zafiro.</p>
  <h2>3. Dónde gana el Orient Bambino V5</h2>
  <p>Su caja de 40,5 mm y 12 mm, el cristal abombado y el acabado PVD oro rosa le dan un aire clásico muy cuidado, y su calibre F6724 permite dar cuerda a mano y para el segundero al ajustar la hora. Como contrapartida, solo resiste 30 m y la correa de piel de fábrica no es la de mayor calidad.</p>
  <h2>4. Lo que comparten</h2>
  <p>Ambos son automáticos con unas 40 horas de reserva, cristal mineral y fondo transparente. Si dudas entre mecánico y cuarzo, mira la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>; para más opciones, la <a href="/guia-relojes-automaticos-entrada.html">guía de automáticos de entrada</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Si buscas un reloj para todos los días, con agua y estilo deportivo: Seiko 5 Sports. Si buscas un reloj de vestir clásico y discreto: Orient Bambino V5. También puedes ver el Seiko frente al <a href="/guia-seiko-5-sports-vs-citizen-tsuyosa.html">Citizen Tsuyosa</a> o el Orient frente al <a href="/guia-orient-bambino-vs-seiko-presage.html">Seiko Presage</a>, o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko 5 u Orient Bambino? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Orient Bambino V5</a>.</p>\n'
    for n in ["guia-orient-bambino-vs-seiko-presage.html","guia-seiko-5-sports-vs-citizen-tsuyosa.html","guia-relojes-automaticos-entrada.html","reloj-orient-bambino-v5.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 vs Bambino</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
