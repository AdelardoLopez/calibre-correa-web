#!/usr/bin/env python3
"""Genera guia-que-es-un-microbrand.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-que-es-un-microbrand.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-vs-citizen"
TITLE = "Qué es un microbrand y si merece la pena (con 3 ejemplos)"
DESC = "Qué son los relojes microbrand, qué ventajas y riesgos tienen y tres ejemplos de nuestro catálogo: Baltic, Scurfa y Nodus, de 345 a 630 €."
W = [
 ("reloj-scurfa-diver-one-d1-500.html","Scurfa Diver One D1-500","345 €","Reino Unido","Cuarzo suizo ETA","500 m","12 meses"),
 ("reloj-nodus-sector-ii-dive-gmt.html","Nodus Sector II Dive GMT","480 €","EE. UU. (Los Ángeles)","Automático Seiko NH34 GMT","100 m","Directa con la marca"),
 ("reloj-baltic-aquascaphe-mk2.html","Baltic Aquascaphe MK2","630 €","Francia","Automático Miyota 9039","200 m","Directa con la marca"),
]
FAQ = [
 ("¿Qué es un microbrand?",
  "Es una marca de relojes pequeña e independiente que diseña sus modelos y los vende sobre todo directamente en su web, sin pasar por distribuidores. Suele montar movimientos de proveedores como Seiko, Miyota o ETA."),
 ("¿Merece la pena comprar un reloj microbrand?",
  "Sí, si te importa el diseño y la relación calidad-precio: a menudo ofrecen zafiro, buena resistencia al agua y acabados por encima de su precio. El riesgo está en la postventa, que depende de una marca pequeña."),
 ("¿Qué riesgos tiene comprar a un microbrand?",
  "Devoluciones más complicadas que en Amazon, envíos desde fuera de la UE con posibles aduanas e impuestos, y un servicio técnico que depende de la propia marca."),
 ("¿Los microbrands llevan movimientos propios?",
  "Normalmente no: usan calibres comerciales, como el Miyota 9039 del Baltic, el Seiko NH34 del Nodus o el cuarzo suizo ETA del Scurfa. Eso facilita encontrar quien los repare."),
]
def build():
    rows = "".join(f'<tr><td><a href="/{s}">{n}</a></td><td>{p}</td><td>{o}</td><td>{m}</td><td>{a}</td></tr>' for s,n,p,o,m,a,g in W)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in FAQ)
    ld = [
     {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,"inLanguage":"es","mainEntityOfPage":URL,"author":{"@type":"Organization","name":"Calibre & Correa"}},
     {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in ld)
    t = (ROOT/(PREV+".html")).read_text(encoding="utf-8")
    head, rest = t.split('<article class="guide">')
    head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
    for pat in ('name="description"','property="og:description"','name="twitter:description"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
    for pat in ('property="og:title"','name="twitter:title"'):
        head = re.sub(rf'(<meta {pat} content=")[^"]*(")', lambda m: m.group(1)+TITLE+" | Calibre &amp; Correa"+m.group(2), head)
    head = head.replace(f"{BASE}/{PREV}.html", URL).replace(f"{BASE}/{PREV}", URL)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", head, flags=re.S)
    head = head.replace("</head>", ld_html+"</head>")
    tail = rest.split("</article>",1)[1]
    body = f'''<article class="guide">
  <h1 style="font-size:2rem;">Qué es un microbrand y si merece la pena</h1>
  <p>Un microbrand es una marca de relojes pequeña e independiente que vende directamente al cliente. Suelen ofrecer más reloj por el dinero, con diseño cuidado, zafiro y buena resistencia al agua, a cambio de una postventa menos cómoda. Aquí tienes tres ejemplos de nuestro catálogo.</p>
  <h2>1. Ventajas de un microbrand</h2>
  <p>Al vender sin intermediarios, parte del precio va a la caja, el cristal y el diseño y no al margen de la tienda. Por eso encuentras zafiro, bisel de cerámica o 200-500 m de agua por 345-630 €. Y el diseño suele tener personalidad propia, a menudo inspirado en relojes históricos.</p>
  <h2>2. Riesgos que conviene conocer</h2>
  <p>Las devoluciones no son tan fáciles como en Amazon, los envíos desde fuera de la UE pueden llevar aduanas e impuestos, y el servicio técnico depende de la propia marca. Los tres de este catálogo usan calibres comerciales (Miyota, Seiko NH34, ETA), así que casi cualquier relojero puede repararlos.</p>
  <h2>3. Tres microbrands del catálogo</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Reloj</th><th>Precio</th><th>Origen</th><th>Movimiento</th><th>Agua</th></tr></thead><tbody>{rows}</tbody></table></div>
  <ul>
   <li><a href="/reloj-scurfa-diver-one-d1-500.html"><strong>Scurfa Diver One D1-500</strong></a>: 500 m, bisel de cerámica y cuarzo suizo. Es el más resistente y el más barato; solo se vende en la web de la marca.</li>
   <li><a href="/reloj-nodus-sector-ii-dive-gmt.html"><strong>Nodus Sector II Dive GMT</strong></a>: GMT automático con zafiro y brazalete de acero con ajuste NodeX.</li>
   <li><a href="/reloj-baltic-aquascaphe-mk2.html"><strong>Baltic Aquascaphe MK2</strong></a>: diver vintage de 39,5 mm con zafiro de doble domo y Miyota 9039.</li>
  </ul>
  <h2>4. Nuestra recomendación</h2>
  <p>Si quieres probar un microbrand sin arriesgar mucho: el <a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a>, por tamaño, zafiro y automático con parada de segundero. Si quieres lo más resistente por menos dinero, el Scurfa. Compáralos en el <a href="/comparador.html">comparador</a> o mira toda la <a href="/categoria-microbrands.html">categoría de microbrands</a>.</p>
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
    add = f'<p>¿Te atrae una marca independiente? Lee <a href="/{SLUG}">qué es un microbrand y si merece la pena</a>.</p>\n'
    for n in ["guia-cuando-pagar-mas-reloj.html","guia-mejores-relojes-buceo.html","guia-seiko-vs-citizen.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    p = ROOT/"categoria-microbrands.html"; t = p.read_text(encoding="utf-8")
    if SLUG not in t:
        new = re.sub(r'(<div class="section-head"><h1>[^<]*</h1><div class="sub">[^<]*)(</div></div>)',
                     lambda m: m.group(1)+f' <a href="/{SLUG}">Qué es un microbrand</a>.'+m.group(2), t, 1)
        if new != t: p.write_text(new, encoding="utf-8"); print("✓ enlace en categoria-microbrands")
    old = f'<a href="/{PREV}.html">Guía: Seiko vs Citizen</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: qué es un microbrand</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
