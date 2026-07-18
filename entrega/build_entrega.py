# -*- coding: utf-8 -*-
"""Genera la PÁGINA DE ENTREGA de Desintoxicación Digital (post-compra).

Muestra el producto principal (ebook) + los 6 bonos con su acceso (PDF / web /
WhatsApp / mail / Instagram). Marca NFM, autocontenida (logo embebido en base64).

Uso:  python3 build_entrega.py  →  index.html
Deploy: subir la carpeta entrega a Netlify. Se enlaza desde el checkout / mail de compra.
"""
import os
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", ".claude", "skills", "nfm-super-skill", "assets", "logo-nfm-blanco.png")

NAVY = "#0c3452"
ORANGE = "#ff6602"

# ---- Producto principal ----
MAIN = {
    "img": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/WhatsApp-Image-2026-07-11-at-9.59.28-AM.jpeg",
    "title": "Ebook Desintoxicación Digital",
    "desc": "El plan completo, un paso por día, para recuperar tu cerebro del celular. Empezá por acá.",
    "cta": "Descargar el ebook (PDF)",
    "href": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/Desintoxicacion_Digital_7dias.pdf",
}

# ---- 6 bonos (en el orden del value stack de la landing) ----
BONOS = [
    {"emoji": "🔄", "tag": "Bono 1", "title": "Reseteo de Dopamina",
     "desc": "La guía para hacer un reset de dopamina sin sufrir.",
     "cta": "Descargar PDF",
     "href": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/Reset-de-Dopamina-NFM.pdf"},
    {"emoji": "🌙", "tag": "Bono 2", "title": "Sueño Blindado",
     "desc": "El checklist para volver a dormir de verdad.",
     "cta": "Descargar PDF",
     "href": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/Sueno_blindado.pdf"},
    {"emoji": "🎯", "tag": "Bono 3", "title": "Bloque de Foco",
     "desc": "El método de 30 minutos para recuperar la concentración que creías perdida.",
     "cta": "Descargar PDF",
     "href": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/Modo-Foco-NFM.pdf"},
    {"emoji": "🎬", "tag": "Bono 4", "title": "Masterclass: la neurociencia de la procrastinación",
     "desc": "Nico te explica en video por qué postergás y cómo cortarlo.",
     "cta": "Ver la masterclass →",
     "href": "https://masterclass-nfm.netlify.app/"},
    {"emoji": "📅", "tag": "Bono 5", "title": "Reto de 7 Días acompañado",
     "desc": "Un mensaje por día que te lleva de la mano toda la semana. Elegí cómo recibirlo:",
     "special": "reto"},
    {"emoji": "💬", "tag": "Bono 6", "title": "Canal Exclusivo de WhatsApp",
     "desc": "Herramientas basadas en neurociencia, nuevas todas las semanas.",
     "cta": "Unirme al canal →",
     "href": "https://whatsapp.com/channel/0029Vb7jL3UAe5VmLhH5jk3L"},
]

RETO_MAIL = "https://www.dopplerpages.com/contacto-C19B6/Form1-90085"
RETO_IG = "https://ig.me/m/nicofernandezmiranda?ref=reto7dias"


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def bono_card(bo):
    if bo.get("special") == "reto":
        actions = (
            '<div class="bo-actions">'
            f'<a class="btn btn-o" href="{RETO_MAIL}" target="_blank" rel="noopener">📧 Por mail</a>'
            f'<a class="btn btn-o" href="{RETO_IG}" target="_blank" rel="noopener">📱 Por Instagram</a>'
            '</div>'
            '<p class="bo-note">¿No se te activa el de Instagram? Mandá la palabra <b>RETO7</b> en el chat.</p>'
        )
    else:
        actions = f'<a class="btn btn-o" href="{bo["href"]}" target="_blank" rel="noopener">{bo["cta"]}</a>'
    return f'''<article class="bono">
  <div class="bo-ico">{bo["emoji"]}</div>
  <div class="bo-body">
    <span class="bo-tag">{bo["tag"]}</span>
    <h3>{bo["title"]}</h3>
    <p class="bo-desc">{bo["desc"]}</p>
    {actions}
  </div>
</article>'''


def build():
    logo = b64(LOGO)
    bonos_html = "\n".join(bono_card(b) for b in BONOS)
    html = PAGE.format(navy=NAVY, orange=ORANGE, logo=logo,
                       main=MAIN, bonos=bonos_html)
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK —", out)


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>¡Ya es tuyo! · Desintoxicación Digital · NFM</title>
<meta name="description" content="Tu acceso a Desintoxicación Digital + los 6 bonos de regalo. Descargá todo acá.">
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎉</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--navy:{navy};--navy2:#123f63;--orange:{orange};--orange-hover:#e65a00;--orange-soft:#fff1e8;
--ink:#0c3452;--body:#3a4a57;--muted:#6b7a86;--hairline:#e3e8ec;--surface:#f5f7f9;--canvas:#fff;
--shadow:0 1px 3px rgba(12,52,82,.08),0 10px 30px rgba(12,52,82,.08);--ease:cubic-bezier(.22,1,.36,1)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Open Sans',-apple-system,system-ui,sans-serif;color:var(--body);background:var(--surface);line-height:1.6}}
h1,h2,h3{{font-family:'Montserrat',sans-serif;color:var(--ink);letter-spacing:-.01em;line-height:1.15}}
img{{max-width:100%;display:block}}
a{{color:var(--orange)}}
.wrap{{max-width:920px;margin:0 auto;padding:0 20px}}
/* topbar */
.topbar{{background:var(--navy);padding:15px 0}}
.topbar img{{height:30px;margin:0 auto;display:block}}
/* hero */
.hero{{background:linear-gradient(160deg,var(--navy),var(--navy2) 70%,#0e4a75);color:#fff;text-align:center;padding:46px 0 40px;position:relative;overflow:hidden}}
.hero::after{{content:"";position:absolute;right:-90px;top:-90px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(255,102,2,.28),transparent 70%)}}
.hero .check{{width:60px;height:60px;border-radius:50%;background:var(--orange);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;box-shadow:0 12px 30px rgba(255,102,2,.4);position:relative;z-index:1}}
.hero .check svg{{width:30px;height:30px}}
.hero h1{{color:#fff;font-size:clamp(1.7rem,4.6vw,2.5rem);font-weight:800;max-width:18ch;margin:0 auto;position:relative;z-index:1}}
.hero p{{color:#c8d9e6;max-width:56ch;margin:14px auto 0;font-size:1.05rem;position:relative;z-index:1}}
/* main product */
main{{padding:34px 0 60px}}
.kicker{{font-family:'Montserrat';font-weight:700;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin-bottom:12px}}
.feat{{background:var(--canvas);border:2px solid var(--orange);border-radius:20px;overflow:hidden;box-shadow:0 20px 50px -18px rgba(255,102,2,.35);display:grid;grid-template-columns:300px 1fr;margin-bottom:40px}}
.feat-media{{background:var(--surface);position:relative;min-height:100%}}
.feat-media img{{width:100%;height:100%;object-fit:cover}}
.feat-body{{padding:30px 32px;display:flex;flex-direction:column;justify-content:center}}
.feat-body h2{{font-size:1.5rem;margin:2px 0 8px}}
.feat-body p{{margin-bottom:20px}}
@media(max-width:640px){{.feat{{grid-template-columns:1fr}}.feat-media{{aspect-ratio:16/10}}}}
/* buttons */
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-family:'Montserrat';font-weight:700;font-size:.98rem;border-radius:999px;padding:14px 26px;text-decoration:none;transition:transform .18s var(--ease),box-shadow .25s,background .2s;cursor:pointer;border:none}}
.btn-o{{background:var(--orange);color:#fff;box-shadow:0 10px 26px rgba(255,102,2,.3)}}
.btn-o:hover{{background:var(--orange-hover);transform:translateY(-2px);box-shadow:0 14px 32px rgba(255,102,2,.42)}}
.feat .btn{{align-self:flex-start;font-size:1.05rem;padding:16px 32px}}
/* bonos */
.sec-head{{text-align:center;margin-bottom:26px}}
.sec-head h2{{font-size:clamp(1.4rem,3.4vw,2rem);font-weight:800}}
.sec-head p{{color:var(--muted);margin-top:8px}}
.bonos-grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:640px){{.bonos-grid{{grid-template-columns:1fr}}}}
.bono{{background:var(--canvas);border:1px solid var(--hairline);border-radius:16px;padding:22px;display:flex;gap:16px;box-shadow:var(--shadow);transition:transform .18s var(--ease),box-shadow .2s}}
.bono:hover{{transform:translateY(-3px);box-shadow:0 16px 40px rgba(12,52,82,.12)}}
.bo-ico{{flex:0 0 52px;height:52px;border-radius:14px;background:linear-gradient(145deg,var(--navy),var(--navy2));display:flex;align-items:center;justify-content:center;font-size:1.5rem}}
.bo-body{{flex:1;min-width:0}}
.bo-tag{{font-family:'Montserrat';font-weight:700;font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;color:var(--orange)}}
.bono h3{{font-size:1.08rem;font-weight:800;margin:5px 0 6px;line-height:1.2}}
.bo-desc{{font-size:.92rem;color:var(--body);margin-bottom:16px}}
.bono .btn{{padding:12px 22px;font-size:.92rem}}
.bo-actions{{display:flex;gap:10px;flex-wrap:wrap}}
.bo-note{{font-size:.82rem;color:var(--muted);margin-top:12px;background:var(--surface);border-radius:10px;padding:9px 12px}}
.bo-note b{{color:var(--ink)}}
/* tip */
.tip{{display:flex;gap:12px;align-items:flex-start;background:var(--orange-soft);border:1px solid #ffd9bd;border-radius:14px;padding:16px 18px;margin:0 0 34px;font-size:.95rem;color:#8a4212}}
.tip b{{color:#7a3a10}}
/* footer */
footer{{background:var(--navy);color:#9db8cc;text-align:center;padding:32px 20px;font-size:.86rem}}
footer .q{{font-family:'Montserrat';font-weight:700;color:#fff;margin-bottom:6px}}
footer a{{color:#ffb37e}}
</style>
</head>
<body>
<div class="topbar"><img src="{logo}" alt="NFM — Instituto de Productividad"></div>

<header class="hero"><div class="wrap">
  <div class="check"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  <h1>¡Listo! Ya es todo tuyo</h1>
  <p>Gracias por dar el paso 💛 Acá abajo tenés tu ebook y los 6 bonos, listos para descargar y usar. Te sugiero empezar por el ebook.</p>
</div></header>

<main><div class="wrap">

  <div class="tip">💡 <div><b>Guardá esta página en favoritos.</b> Desde acá vas a poder volver a descargar todo cuando quieras. Los archivos abren en una pestaña nueva.</div></div>

  <div class="kicker">Tu producto principal</div>
  <div class="feat">
    <div class="feat-media"><img src="{main[img]}" alt="Ebook Desintoxicación Digital"></div>
    <div class="feat-body">
      <h2>{main[title]}</h2>
      <p>{main[desc]}</p>
      <a class="btn btn-o" href="{main[href]}" target="_blank" rel="noopener">⬇ {main[cta]}</a>
    </div>
  </div>

  <div class="sec-head">
    <h2>🎁 Tus 6 bonos de regalo</h2>
    <p>Todo lo que suma al ebook para que el cambio sea imparable.</p>
  </div>
  <div class="bonos-grid">
{bonos}
  </div>

</div></main>

<footer><div class="wrap">
  <div class="q">"No es motivación, es ciencia."</div>
  <div>Desintoxicación Digital · Nico Fernández Miranda · Instituto de Productividad</div>
</div></footer>
</body>
</html>
"""

if __name__ == "__main__":
    build()
