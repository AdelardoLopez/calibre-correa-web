#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-tissot-prx-quartz.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-tissot-prx-quartz.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-hamilton-khaki-field-vs-seiko-alpinist"
PREV_LABEL = "Guía: Hamilton vs Alpinist"
TITLE = "Seiko 5 Sports vs Tissot PRX Quartz"
DESC = "Seiko 5 Sports SRPD (229 €, automático) frente a Tissot PRX Cuarzo (395 €, zafiro y brazalete). Precio, medidas, cristal y mantenimiento con datos del catálogo."
ROWS = [
 ("Precio","229 €","395 €"),
 ("Movimiento","Automático Seiko Calibre 4R36","Cuarzo suizo ETA F06.115"),
 ("Reserva de marcha","41 horas","No aplica (batería)"),
 ("Diámetro de caja","42,5 mm","40 x 39,5 mm (tonneau)"),
 ("Grosor","13,4 mm","10,4 mm"),
 ("Resistencia al agua","100 m","100 m"),
 ("Cristal","Hardlex mineral","Zafiro con tratamiento antirreflejante"),
 ("Correa","Acero inoxidable / NATO / caucho (según versión)","Brazalete de acero de liberación rápida"),
 ("Fondo","Transparente (visible el movimiento)","Cerrado"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Tissot PRX Quartz?",
  "El Seiko 5 Sports: 229 € frente a 395 € del PRX en nuestro catálogo, es decir, 166 € menos."),
 ("¿Cuál es automático?",
  "El Seiko 5 Sports (calibre 4R36, 41 horas de reserva). El Tissot PRX de esta comparativa es de cuarzo y funciona con batería."),
 ("¿Cuál resiste más el agua?",
  "Empatan: ambos indican 100 m de resistencia al agua según nuestras fichas."),
 ("¿Cuál tiene cristal de zafiro?",
  "El Tissot PRX, con zafiro y tratamiento antirreflejante. El Seiko 5 Sports lleva cristal Hardlex mineral, que se raya más fácilmente."),
 ("¿Cuál es más fino y cómodo bajo el puño?",
  "El Tissot PRX: 10,4 mm de grosor y 40 mm de caja frente a 13,4 mm y 42,5 mm del Seiko."),
 ("¿Cuál recomendáis?",
  "Si quieres un primer automático barato con fondo transparente, el Seiko 5 Sports. Si priorizas el diseño, el zafiro, el brazalete y la precisión del cuarzo, el Tissot PRX."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Tissot PRX Quartz</h1>
  <p>Dos relojes de 100 m con 166 € de diferencia y planteamientos opuestos: un automático japonés de entrada frente a un cuarzo suizo de diseño. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports Automático (SRPD)</a></th><th><a href="/reloj-tissot-prx-quartz.html">Tissot PRX Cuarzo T137.410.11.041.00</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko 5 Sports</h2>
  <p>Es 166 € más barato, lleva movimiento automático propio (sin batería) y su fondo transparente deja ver el calibre 4R36. Además, hay versiones con acero, NATO o caucho. Como contrapartida, su cristal Hardlex se raya más que un zafiro, es más grueso (13,4 mm) y su precisión es de gama de entrada.</p>
  <h2>3. Dónde gana el Tissot PRX</h2>
  <p>Tiene cristal de zafiro con antirreflejante, una caja más fina (10,4 mm) y compacta, brazalete de liberación rápida y la precisión del cuarzo con mantenimiento mínimo; su diseño tonneau es el motivo de compra más repetido en las reseñas. Como contrapartida, cuesta 395 €, necesita cambio de batería cada pocos años y no tiene movimiento mecánico.</p>
  <h2>4. Lo que comparten</h2>
  <p>Los dos indican 100 m de resistencia al agua y sirven como reloj de diario. Si dudas entre mecánico y cuarzo, lee <a href="/guia-tipos-de-movimiento.html">los tipos de movimiento</a>; para otra comparativa del PRX, la de <a href="/guia-citizen-tsuyosa-vs-tissot-prx-quartz.html">Citizen Tsuyosa vs Tissot PRX Quartz</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Para tu primer automático al mejor precio: Seiko 5 Sports. Para un reloj fino, con zafiro y sin preocuparte de darle cuerda: Tissot PRX. Más opciones en <a href="/guia-relojes-automaticos-entrada.html">automáticos de entrada</a>, y puedes ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Seiko 5 Sports o Tissot PRX? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Tissot PRX Quartz</a>.</p>\n'
    for n in ["guia-citizen-tsuyosa-vs-tissot-prx-quartz.html","guia-seiko-5-sports-vs-citizen-promaster-diver.html","guia-relojes-automaticos-entrada.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 vs PRX</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
