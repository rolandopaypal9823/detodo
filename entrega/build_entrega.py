# -*- coding: utf-8 -*-
"""Genera la PÁGINA DE ENTREGA de Desintoxicación Digital (post-compra).

Estética tomada de la Masterclass de Neurociencia (Montserrat/Open Sans + JetBrains Mono,
eyebrow pill, título con shimmer, glow naranja, esquinas de marco, botones con brillo,
reveals) PERO sobre FONDO BLANCO (no navy).

Uso:  python3 build_entrega.py  →  index.html
"""
import os
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", ".claude", "skills", "nfm-super-skill", "assets", "logo-nfm-navy.png")

NAVY = "#0c3452"
ORANGE = "#ff6602"

MAIN = {
    "img": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/WhatsApp-Image-2026-07-11-at-9.59.28-AM.jpeg",
    "title": "Ebook Desintoxicación Digital",
    "desc": "El plan completo, un paso por día, para recuperar tu cerebro del celular. Empezá por acá.",
    "cta": "Descargar el ebook (PDF)",
    "href": "https://nicolasfernandezmiranda.com/wp-content/uploads/2026/07/Desintoxicacion_Digital_7dias.pdf",
}

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


def sh(label):
    """Botón naranja con brillo (shine)."""
    return f'<span class="shine"></span><span class="lbl">{label}</span>'


def bono_card(i, bo):
    if bo.get("special") == "reto":
        actions = (
            '<div class="bo-actions">'
            f'<a class="btn btn-o btn-sm" href="{RETO_MAIL}" target="_blank" rel="noopener">{sh("📧 Por mail")}</a>'
            f'<a class="btn btn-o btn-sm" href="{RETO_IG}" target="_blank" rel="noopener">{sh("📱 Por Instagram")}</a>'
            '</div>'
            '<p class="bo-note">¿No se te activa el de Instagram? Mandá la palabra <b>RETO7</b> en el chat.</p>'
        )
    else:
        actions = f'<a class="btn btn-o btn-sm" href="{bo["href"]}" target="_blank" rel="noopener">{sh(bo["cta"])}</a>'
    delay = f'd{min(i + 1, 5)}'
    return f'''<article class="bono fade-up {delay}">
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
    bonos_html = "\n".join(bono_card(i, b) for i, b in enumerate(BONOS))
    html = PAGE.format(navy=NAVY, orange=ORANGE, logo=logo, main=MAIN, bonos=bonos_html)
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
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Open+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--navy:{navy};--navy2:#123f63;--orange:{orange};--orange-hi:#ff8124;--orange-hover:#e65a00;
--ink:#0c3452;--body:#3a4a57;--muted:#6b7a86;--mono:#8598a8;--hair:#e6ebf0;--surface:#f5f7f9;--canvas:#fff;
--glow:rgba(255,102,2,.28);--shadow:0 1px 3px rgba(12,52,82,.07),0 12px 34px rgba(12,52,82,.08);
--ease:cubic-bezier(.16,1,.3,1)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:'Open Sans',-apple-system,system-ui,sans-serif;color:var(--body);background:var(--canvas);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
h1,h2,h3{{font-family:'Montserrat',sans-serif;color:var(--ink);letter-spacing:-.01em;line-height:1.15}}
img{{max-width:100%;display:block}}
a{{color:var(--orange)}}
::selection{{background:var(--orange);color:#fff}}
.wrap{{max-width:940px;margin:0 auto;padding:0 22px}}
.mono{{font-family:'JetBrains Mono',monospace}}
/* reveal (CSS puro, siempre termina visible) */
.fade-up{{opacity:0;transform:translateY(24px);animation:fadeUp .8s var(--ease) forwards}}
.d1{{animation-delay:.05s}}.d2{{animation-delay:.13s}}.d3{{animation-delay:.21s}}.d4{{animation-delay:.29s}}.d5{{animation-delay:.37s}}
@keyframes fadeUp{{to{{opacity:1;transform:none}}}}
@media(prefers-reduced-motion:reduce){{.fade-up{{animation:none;opacity:1;transform:none}}.shimmer{{animation:none}}}}
/* topbar */
.topbar{{border-bottom:1px solid var(--hair);padding:16px 0}}
.topbar .in{{display:flex;align-items:center;gap:14px;justify-content:center}}
.topbar img{{height:30px}}
.topbar .tag{{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mono);font-weight:500;border-left:1px solid var(--hair);padding-left:14px}}
@media(max-width:520px){{.topbar .tag{{display:none}}}}
/* hero */
.hero{{text-align:center;padding:52px 0 34px;position:relative;overflow:hidden}}
.hero::before{{content:"";position:absolute;top:-60px;left:50%;transform:translateX(-50%);width:680px;height:400px;max-width:120vw;background:radial-gradient(circle,rgba(255,102,2,.13),transparent 66%);pointer-events:none}}
.hero>*{{position:relative;z-index:1}}
.eyebrow{{display:inline-flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--muted);background:var(--surface);border:1px solid var(--hair);padding:8px 16px;border-radius:100px;margin-bottom:22px}}
.eyebrow .dot{{width:7px;height:7px;border-radius:50%;background:var(--orange);animation:pulse 2.4s infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(255,102,2,.5)}}70%{{box-shadow:0 0 0 8px rgba(255,102,2,0)}}100%{{box-shadow:0 0 0 0 rgba(255,102,2,0)}}}}
.check{{width:64px;height:64px;border-radius:50%;background:var(--orange);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;box-shadow:0 16px 40px -8px var(--glow)}}
.check svg{{width:32px;height:32px}}
.hero h1{{font-family:'Montserrat',sans-serif;font-weight:900;font-size:clamp(30px,5.6vw,54px);line-height:1.04;letter-spacing:-.02em;max-width:16ch;margin:0 auto}}
.shimmer{{background:linear-gradient(100deg,var(--orange) 20%,var(--orange-hi) 42%,#ffd0ad 50%,var(--orange-hi) 58%,var(--orange) 80%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shimmer 5.5s linear infinite}}
@keyframes shimmer{{to{{background-position:200% center}}}}
.hero p{{color:var(--body);max-width:56ch;margin:16px auto 0;font-size:1.06rem}}
/* botón con brillo */
.btn{{position:relative;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;gap:9px;font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;border:none;border-radius:100px;cursor:pointer;text-decoration:none;transition:transform .18s var(--ease),box-shadow .3s,background .2s}}
.btn .lbl,.btn .shine{{position:relative;z-index:2}}
.btn .lbl{{display:inline-flex;align-items:center;gap:9px}}
.btn .shine{{position:absolute;inset:0;z-index:1;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.5) 50%,transparent 70%);transform:translateX(-120%)}}
.btn-o{{background:var(--orange);color:#fff;padding:15px 30px;box-shadow:0 14px 32px -12px var(--glow)}}
.btn-o:hover{{background:var(--orange-hi);transform:translateY(-2px);box-shadow:0 20px 44px -12px var(--glow)}}
.btn-o:hover .shine{{animation:shine 1.05s var(--ease)}}
.btn-sm{{padding:12px 24px;font-size:.94rem}}
@keyframes shine{{to{{transform:translateX(120%)}}}}
/* main */
main{{padding:36px 0 64px}}
.kicker{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange);margin-bottom:14px}}
.feat{{position:relative;background:var(--canvas);border:1px solid var(--hair);border-radius:20px;overflow:hidden;box-shadow:0 24px 60px -24px rgba(12,52,82,.28);display:grid;grid-template-columns:300px 1fr;margin-bottom:44px}}
.feat::before{{content:"";position:absolute;inset:-1px;border-radius:20px;background:radial-gradient(70% 60% at 50% 0%,var(--glow),transparent 70%);z-index:-1;filter:blur(16px);opacity:.85}}
.feat-media{{position:relative;background:var(--surface);min-height:100%}}
.feat-media img{{width:100%;height:100%;object-fit:cover}}
.corner{{position:absolute;width:20px;height:20px;border:2px solid var(--orange);opacity:.8;z-index:2}}
.corner.tl{{top:10px;left:10px;border-right:0;border-bottom:0;border-radius:7px 0 0 0}}
.corner.tr{{top:10px;right:10px;border-left:0;border-bottom:0;border-radius:0 7px 0 0}}
.corner.bl{{bottom:10px;left:10px;border-right:0;border-top:0;border-radius:0 0 0 7px}}
.corner.br{{bottom:10px;right:10px;border-left:0;border-top:0;border-radius:0 0 7px 0}}
.feat-body{{padding:32px 34px;display:flex;flex-direction:column;justify-content:center}}
.feat-body h2{{font-size:1.55rem;font-weight:800;margin:2px 0 8px}}
.feat-body p{{margin-bottom:22px}}
.feat .btn{{align-self:flex-start;font-size:1.05rem;padding:16px 32px}}
@media(max-width:640px){{.feat{{grid-template-columns:1fr}}.feat-media{{aspect-ratio:16/10}}}}
/* tip */
.tip{{display:flex;gap:12px;align-items:flex-start;background:#fff7f1;border:1px solid #ffe0c7;border-radius:14px;padding:15px 18px;margin:0 0 34px;font-size:.94rem;color:#8a4212}}
.tip b{{color:#7a3a10}}
/* bonos */
.sec-head{{text-align:center;margin-bottom:26px}}
.sec-head .kicker{{margin-bottom:8px}}
.sec-head h2{{font-size:clamp(1.4rem,3.4vw,2rem);font-weight:800}}
.sec-head p{{color:var(--muted);margin-top:8px}}
.bonos-grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:640px){{.bonos-grid{{grid-template-columns:1fr}}}}
.bono{{background:var(--canvas);border:1px solid var(--hair);border-radius:16px;padding:22px;display:flex;gap:16px;box-shadow:var(--shadow);transition:transform .18s var(--ease),box-shadow .2s,border-color .2s}}
.bono:hover{{transform:translateY(-3px);box-shadow:0 18px 44px rgba(12,52,82,.13);border-color:#d7e2ec}}
.bo-ico{{flex:0 0 52px;height:52px;border-radius:14px;background:linear-gradient(145deg,var(--navy),var(--navy2));display:flex;align-items:center;justify-content:center;font-size:1.5rem;box-shadow:0 8px 20px rgba(12,52,82,.22)}}
.bo-body{{flex:1;min-width:0}}
.bo-tag{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;color:var(--orange)}}
.bono h3{{font-size:1.08rem;font-weight:800;margin:5px 0 6px;line-height:1.2}}
.bo-desc{{font-size:.92rem;color:var(--body);margin-bottom:16px}}
.bo-actions{{display:flex;gap:10px;flex-wrap:wrap}}
.bo-note{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.02em;color:var(--mono);margin-top:12px;background:var(--surface);border:1px solid var(--hair);border-radius:10px;padding:9px 12px}}
.bo-note b{{color:var(--ink)}}
/* footer */
footer{{border-top:1px solid var(--hair);text-align:center;padding:30px 20px;font-size:.86rem;color:var(--muted)}}
footer .q{{font-family:'Montserrat',sans-serif;font-weight:700;color:var(--ink);margin-bottom:6px}}
footer .mono{{color:var(--mono);font-size:.72rem;letter-spacing:.06em;margin-top:8px}}
</style>
</head>
<body>
<div class="topbar"><div class="in">
  <img src="{logo}" alt="NFM — Instituto de Productividad">
  <span class="tag">Instituto de Productividad</span>
</div></div>

<header class="hero"><div class="wrap">
  <span class="eyebrow fade-up"><span class="dot"></span>Compra confirmada · Acceso inmediato</span>
  <div class="check fade-up d1"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  <h1 class="fade-up d1">¡Listo! Ya es todo <span class="shimmer">tuyo</span></h1>
  <p class="fade-up d2">Gracias por dar el paso 💛 Acá abajo tenés tu ebook y los 6 bonos, listos para descargar y usar. Te sugiero empezar por el ebook.</p>
</div></header>

<main><div class="wrap">

  <div class="tip fade-up">💡 <div><b>Guardá esta página en favoritos.</b> Desde acá vas a poder volver a descargar todo cuando quieras. Los archivos abren en una pestaña nueva.</div></div>

  <div class="kicker fade-up">Tu producto principal</div>
  <div class="feat fade-up d1">
    <div class="feat-media">
      <img src="{main[img]}" alt="Ebook Desintoxicación Digital">
      <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
    </div>
    <div class="feat-body">
      <h2>{main[title]}</h2>
      <p>{main[desc]}</p>
      <a class="btn btn-o" href="{main[href]}" target="_blank" rel="noopener"><span class="shine"></span><span class="lbl">⬇ {main[cta]}</span></a>
    </div>
  </div>

  <div class="sec-head fade-up">
    <div class="kicker">Incluido en tu compra</div>
    <h2>🎁 Tus 6 bonos de regalo</h2>
    <p>Todo lo que suma al ebook para que el cambio sea imparable.</p>
  </div>
  <div class="bonos-grid">
{bonos}
  </div>

</div></main>

<footer><div class="wrap">
  <div class="q">"No es motivación, es ciencia."</div>
  <div>Desintoxicación Digital · Nico Fernández Miranda</div>
  <div class="mono">INSTITUTO DE PRODUCTIVIDAD</div>
</div></footer>
</body>
</html>
"""

if __name__ == "__main__":
    build()
