#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-citizen-promaster-diver.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-relojes-con-cristal-de-zafiro.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-5-sports-vs-citizen-promaster-diver"
TITLE = "Relojes con cristal de zafiro: opciones desde 329 €"
DESC = "Siete relojes de nuestro catálogo con cristal de zafiro, de 329 € a 650 €: movimiento, tamaño y agua de cada uno, y qué cristal llevan los que no lo tienen."
ROWS = [
 ("Citizen Tsuyosa NJ0151-53M","329 €","Automático 8210","40 mm","50 m","Zafiro antirreflejante"),
 ("Scurfa Diver One D1-500","345 €","Cuarzo suizo ETA F06.412","40 mm","500 m","Zafiro abombado"),
 ("Tissot PRX Cuarzo","395 €","Cuarzo suizo ETA F06.115","40 x 39,5 mm","100 m","Zafiro antirreflejante"),
 ("Nodus Sector II Dive GMT","480 €","Automático NH34 GMT","40 mm","100 m","Zafiro"),
 ("Hamilton Khaki Field Mechanical","575 €","Manual H-50","38 mm","50 m","Zafiro"),
 ("Baltic Aquascaphe MK2","630 €","Automático Miyota 9039","39,5 mm","200 m","Zafiro doble domo antirreflejante"),
 ("Seiko Prospex Alpinist SPB210","650 €","Automático 6R35","39,5 mm","200 m","Zafiro antirreflejante"),
]
NOSAFIRO = "Seiko 5 Sports (Hardlex, 229 €), Citizen Promaster Eco-Drive Diver (mineral, 229 €), Seiko Presage SRPB41 (Hardlex, 350 €) y Orient Bambino V5 (mineral abombado, 220 €)"
FAQ = [
 ("¿Cuál es el reloj con zafiro más barato del catálogo?",
  "El Citizen Tsuyosa NJ0151-53M, con 329 €. Le sigue el Scurfa Diver One D1-500 (345 €) y el Tissot PRX Cuarzo (395 €)."),
 ("¿Qué relojes del catálogo no tienen zafiro?",
  "Cuatro: "+NOSAFIRO+"."),
 ("¿Para qué sirve el zafiro?",
  "Es mucho más resistente al rayado que el cristal mineral o el Hardlex, así que el reloj conserva mejor la esfera visible con el uso diario. No es irrompible: un golpe fuerte sí puede romperlo."),
 ("¿Hay algún automático con zafiro por menos de 400 €?",
  "Sí, el Citizen Tsuyosa (329 €, calibre 8210, 40 mm). Si prefieres un buceador, el Nodus Sector II Dive GMT sube a 480 € e incluye función GMT."),
 ("¿Cuál con zafiro aguanta más agua?",
  "El Scurfa Diver One D1-500, con 500 m. Entre los automáticos, el Baltic Aquascaphe MK2 y el Seiko Alpinist SPB210 llegan a 200 m."),
 ("¿Cuál recomendáis?",
  "Para vestir a buen precio, el Citizen Tsuyosa. Para uso diario con mucha estanqueidad, el Baltic Aquascaphe MK2. Para quien quiere cuerda manual y formato pequeño, el Hamilton Khaki Field Mechanical."),
]
def build():
    rows = "".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in ROWS)
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
  <h1 style="font-size:2rem;">Relojes con cristal de zafiro: cuáles elegir</h1>
  <p>El zafiro es el cristal más resistente al rayado que se monta en relojes de este rango de precio. De los once modelos de nuestro catálogo, siete lo llevan; aquí los tienes ordenados por precio.</p>
  <h2>1. Los siete con zafiro</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th>Modelo</th><th>Precio</th><th>Movimiento</th><th>Caja</th><th>Agua</th><th>Cristal</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Los que no lo llevan</h2>
  <p>Son {NOSAFIRO}. Son opciones válidas y más baratas (220-350 €), pero su cristal se raya con más facilidad.</p>
  <h2>3. Qué elegir según el uso</h2>
  <p>Para vestir, el <a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a> o el <a href="/reloj-tissot-prx-quartz.html">Tissot PRX Cuarzo</a>. Para agua, el <a href="/reloj-scurfa-diver-one-d1-500.html">Scurfa Diver One</a> (500 m) o el <a href="/reloj-baltic-aquascaphe-mk2.html">Baltic Aquascaphe MK2</a> (200 m). Para campo y diario, el <a href="/reloj-seiko-alpinist-spb210.html">Seiko Alpinist SPB210</a> o el <a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field</a>. El <a href="/reloj-nodus-sector-ii-dive-gmt.html">Nodus Sector II Dive GMT</a> añade función GMT.</p>
  <h2>4. Más guías</h2>
  <p>Si buscas ahorrar, mira la <a href="/guia-mejores-relojes-baratos.html">guía de relojes baratos</a>; si dudas entre pagar más, la <a href="/guia-cuando-pagar-mas-reloj.html">guía de cuándo pagar más</a>. También puedes usar el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Te importa el cristal? Mira los <a href="/{SLUG}">relojes con cristal de zafiro de nuestro catálogo</a>.</p>\n'
    for n in ["guia-cuando-pagar-mas-reloj.html","guia-mejores-relojes-vestir.html","guia-mejores-relojes-buceo.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">Guía: Seiko 5 vs Promaster Diver</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: relojes con zafiro</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
