#!/usr/bin/env python3
"""Genera guia-seiko-5-sports-vs-seiko-presage-srpb41.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-seiko-5-sports-vs-seiko-presage-srpb41.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-citizen-tsuyosa-vs-hamilton-khaki-field"
PREV_LABEL = "Guía: Tsuyosa vs Hamilton"
TITLE = "Seiko 5 Sports vs Seiko Presage SRPB41"
DESC = "Seiko 5 Sports (229 €, 100 m, caja de 42,5 mm) frente a Seiko Presage SRPB41 (350 €, dial azul de vestir, 50 m). Datos del catálogo."
ROWS = [
 ("Precio","229 €","350 €"),
 ("Movimiento","Automático Seiko Calibre 4R36","Automático Seiko Calibre 4R35"),
 ("Reserva de marcha","41 horas","41 horas"),
 ("Diámetro de caja","42,5 mm","40,5 mm"),
 ("Grosor","13,4 mm","11,8 mm"),
 ("Resistencia al agua","100 m","50 m"),
 ("Cristal","Hardlex mineral","Hardlex con forma de caja"),
 ("Correa","Acero inoxidable / NATO / caucho (según versión)","Brazalete de acero"),
 ("Fondo","Transparente (visible el movimiento)","Transparente (visible el movimiento)"),
]
FAQ = [
 ("¿Cuál es más barato, el Seiko 5 Sports o el Seiko Presage SRPB41?",
  "El Seiko 5 Sports: 229 € frente a 350 € del Presage SRPB41 en nuestro catálogo, 121 € menos."),
 ("¿Cuál resiste más el agua?",
  "El Seiko 5 Sports, con 100 m frente a 50 m del Presage. El Presage sirve para el día a día, pero no para nadar con confianza."),
 ("¿Cuál es más fino y pequeño?",
  "El Presage SRPB41, con 40,5 mm de caja y 11,8 mm de grosor, frente a 42,5 mm y 13,4 mm del Seiko 5 Sports."),
 ("¿Tienen cristal de zafiro?",
  "No, ninguno de los dos: ambos llevan cristal Hardlex, el mineral endurecido de Seiko."),
 ("¿Tienen la misma reserva de marcha?",
  "Sí: 41 horas los dos, con los calibres automáticos 4R36 (Seiko 5 Sports) y 4R35 (Presage)."),
 ("¿Cuál es más elegante?",
  "El Presage SRPB41, con dial azul texturizado y brazalete de acero pensado para vestir. El Seiko 5 Sports tiene una estética deportiva de buceo."),
 ("¿Cuál recomendáis?",
  "Para un automático deportivo, más resistente al agua y barato: Seiko 5 Sports. Para un reloj de vestir con dial llamativo, más fino y con aire elegante, aceptando 50 m y pagar 121 € más: Seiko Presage SRPB41."),
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
  <h1 style="font-size:2rem;">Seiko 5 Sports vs Seiko Presage SRPB41</h1>
  <p>Dos automáticos de la misma marca, con el mismo tipo de calibre, cristal Hardlex y 41 horas de reserva, pero con personalidades opuestas: un deportivo de uso diario frente a un reloj de vestir con dial azul. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-seiko-5-sports.html">Seiko 5 Sports</a></th><th><a href="/reloj-seiko-presage-srpb41.html">Seiko Presage SRPB41</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Seiko 5 Sports</h2>
  <p>Es más barato (229 €) y resiste más el agua (100 m frente a 50 m), así que admite mejor el uso diario y el baño. Tiene correa a elegir según versión y piezas y servicio técnico Seiko fáciles de encontrar. Como contrapartida, es más grande y grueso (42,5 mm y 13,4 mm), su cristal Hardlex se raya más que un zafiro y su corona no es de rosca.</p>
  <h2>3. Dónde gana el Seiko Presage SRPB41</h2>
  <p>Es más fino y compacto (40,5 mm y 11,8 mm), con un dial azul texturizado de siete capas de laca poco habitual a este precio y un diseño de vestir que no resulta aburrido. Como contrapartida, cuesta 121 € más, solo ofrece 50 m de resistencia al agua y, pese a ser gama Presage, lleva Hardlex y no zafiro.</p>
  <h2>4. Lo que comparten</h2>
  <p>Movimiento automático Seiko de la familia 4R, 41 horas de reserva, cristal Hardlex y fondo transparente. Si quieres cristal de zafiro, mira la <a href="/guia-relojes-con-cristal-de-zafiro.html">guía de relojes con cristal de zafiro</a>; para entender qué significa automático, la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Si quieres un automático deportivo, resistente y económico: Seiko 5 Sports. Si buscas un reloj de vestir con dial llamativo y caja más fina: Seiko Presage SRPB41. También puedes ver el Seiko 5 frente al <a href="/guia-seiko-5-sports-vs-orient-bambino-v5.html">Orient Bambino V5</a> o el Presage frente al <a href="/guia-seiko-presage-srpb41-vs-citizen-tsuyosa.html">Citizen Tsuyosa</a>, o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿¿Seiko 5 Sports o Seiko Presage SRPB41? Lee la <a href="/{SLUG}">comparativa Seiko 5 Sports vs Seiko Presage SRPB41</a>.</p>\n'
    for n in ["guia-seiko-5-sports-vs-orient-bambino-v5.html","guia-seiko-presage-srpb41-vs-citizen-tsuyosa.html","reloj-seiko-5-sports.html","reloj-seiko-presage-srpb41.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Seiko 5 vs Presage</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
