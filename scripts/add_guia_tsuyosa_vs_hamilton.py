#!/usr/bin/env python3
"""Genera guia-citizen-tsuyosa-vs-hamilton-khaki-field.html (idempotente) y la enlaza en sitemap, guías y footer."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BASE = "https://calibre-correa.adelardo.workers.dev"
SLUG = "guia-citizen-tsuyosa-vs-hamilton-khaki-field.html"
URL = f"{BASE}/{SLUG[:-5]}"
PREV = "guia-seiko-5-sports-vs-orient-bambino-v5"
PREV_LABEL = "Guía: Seiko 5 vs Bambino"
TITLE = "Citizen Tsuyosa vs Hamilton Khaki Field Mechanical"
DESC = "Citizen Tsuyosa (329 €, automático, brazalete integrado) frente a Hamilton Khaki Field Mechanical (575 €, cuerda manual, 80 h de reserva). Datos del catálogo."
ROWS = [
 ("Precio","329 €","575 €"),
 ("Movimiento","Automático Citizen Calibre 8210","Manual (cuerda a mano) Hamilton Calibre H-50"),
 ("Reserva de marcha","40 horas","80 horas"),
 ("Diámetro de caja","40 mm","38 mm"),
 ("Grosor","≈ 12 mm","9,5 mm"),
 ("Resistencia al agua","50 m","50 m"),
 ("Cristal","Zafiro con tratamiento antirreflejante","Zafiro"),
 ("Correa","Brazalete integrado de acero","NATO de tela verde"),
 ("Fondo","Transparente (visible el movimiento)","Cerrado"),
]
FAQ = [
 ("¿Cuál es más barato, el Citizen Tsuyosa o el Hamilton Khaki Field Mechanical?",
  "El Citizen Tsuyosa: 329 € frente a 575 € del Hamilton en nuestro catálogo, 246 € menos."),
 ("¿Cuál tiene más reserva de marcha?",
  "El Hamilton, con 80 horas frente a 40 del Tsuyosa. Eso sí, el Hamilton es de cuerda manual y hay que darle cuerda a mano."),
 ("¿Cuál es automático?",
  "El Citizen Tsuyosa. El Hamilton Khaki Field Mechanical es de cuerda manual, sin rotor."),
 ("¿Cuál es más fino y pequeño?",
  "El Hamilton, con 38 mm de caja y 9,5 mm de grosor, frente a 40 mm y unos 12 mm del Tsuyosa."),
 ("¿Tienen cristal de zafiro?",
  "Sí, los dos. El Tsuyosa añade tratamiento antirreflejante."),
 ("¿Cuál resiste más el agua?",
  "Empatan: 50 m los dos, suficiente para salpicaduras y lluvia pero justo para nadar."),
 ("¿Cuál recomendáis?",
  "Para un automático de estilo urbano con brazalete integrado y fondo transparente: Citizen Tsuyosa. Para un reloj de campo fino, de diseño militar atemporal y con mucha reserva de marcha, aceptando darle cuerda a mano: Hamilton Khaki Field Mechanical."),
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
  <h1 style="font-size:2rem;">Citizen Tsuyosa vs Hamilton Khaki Field Mechanical</h1>
  <p>Dos relojes de estilos muy distintos con cristal de zafiro y 50 m de resistencia al agua: un automático de brazalete integrado frente a un reloj de campo de cuerda manual. Los comparamos con los datos de nuestro catálogo, sin pruebas propias en la muñeca: las fichas se basan en las especificaciones de cada marca y en reseñas publicadas.</p>
  <h2>1. Comparativa directa</h2>
  <div style="overflow-x:auto;"><table class="guide-table"><thead><tr><th></th><th><a href="/reloj-citizen-tsuyosa.html">Citizen Tsuyosa</a></th><th><a href="/reloj-hamilton-khaki-field-mechanical.html">Hamilton Khaki Field Mechanical</a></th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>2. Dónde gana el Citizen Tsuyosa</h2>
  <p>Es más barato (329 €) y es automático, así que no hay que darle cuerda a diario. Su brazalete integrado de acero es poco habitual a este precio y muy cómodo por su diseño en cuña, y el fondo transparente deja ver el movimiento. Como contrapartida, tiene 40 horas de reserva, el brazalete no admite cualquier correa de repuesto y el cierre no tiene micro-ajuste.</p>
  <h2>3. Dónde gana el Hamilton Khaki Field Mechanical</h2>
  <p>Ofrece 80 horas de reserva de marcha, una caja más pequeña y fina (38 mm y 9,5 mm) y un diseño militar atemporal de un fabricante suizo del grupo Swatch. Como contrapartida, cuesta 246 € más, hay que darle cuerda a mano cada día o dos y el fondo cerrado no deja ver el movimiento.</p>
  <h2>4. Lo que comparten</h2>
  <p>Cristal de zafiro y 50 m de resistencia al agua: sirven para el día a día, pero no para nadar con regularidad. Si dudas entre automático y manual, mira la <a href="/guia-tipos-de-movimiento.html">guía de tipos de movimiento</a>; para más opciones con zafiro, la <a href="/guia-relojes-con-cristal-de-zafiro.html">guía de relojes con cristal de zafiro</a>.</p>
  <h2>5. Nuestra recomendación</h2>
  <p>Si quieres un automático con personalidad urbana y brazalete integrado: Citizen Tsuyosa. Si prefieres un reloj de campo fino y clásico, y no te importa darle cuerda: Hamilton Khaki Field Mechanical. También puedes ver el Hamilton frente al <a href="/guia-seiko-5-sports-vs-hamilton-khaki-field.html">Seiko 5 Sports</a> o el Tsuyosa frente al <a href="/guia-orient-bambino-vs-citizen-tsuyosa.html">Orient Bambino</a>, o ponerlos lado a lado en el <a href="/comparador.html">comparador</a>.</p>
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
    add = f'<p>¿Citizen Tsuyosa u Hamilton Khaki Field? Lee la <a href="/{SLUG}">comparativa Citizen Tsuyosa vs Hamilton Khaki Field Mechanical</a>.</p>\n'
    for n in ["guia-seiko-5-sports-vs-hamilton-khaki-field.html","guia-orient-bambino-vs-citizen-tsuyosa.html","reloj-citizen-tsuyosa.html","reloj-hamilton-khaki-field-mechanical.html"]:
        p = ROOT/n; t = p.read_text(encoding="utf-8")
        if SLUG in t: continue
        p.write_text(t.replace("</article>", add+"</article>",1), encoding="utf-8"); print("✓ enlace en", n)
    old = f'<a href="/{PREV}.html">{PREV_LABEL}</a>'
    newf = old + f'\n      <a href="/{SLUG}">Guía: Tsuyosa vs Hamilton</a>'
    for p in ROOT.glob("*.html"):
        t = p.read_text(encoding="utf-8")
        if old in t and SLUG+'">Guía' not in t:
            p.write_text(t.replace(old,newf),encoding="utf-8")
if __name__ == "__main__": main()
