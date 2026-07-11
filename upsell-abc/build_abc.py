# -*- coding: utf-8 -*-
"""Genera la página del curso 'El ABC del Alto Rendimiento' (upsell), estilo Skool, marca NFM.

- Módulos desplegables (accordion) con secciones y lecciones.
- Cada lección abre un reproductor embebido (Loom/YouTube) INLINE, con carga lazy
  (el iframe se inyecta recién al abrir la lección → la página carga liviana).
- Progreso por módulo + global, guardado en el dispositivo (localStorage).
- Recursos/entregables por módulo (links externos; los PDF de Skool quedan señalados).

Uso:  python3 build_abc.py   →   index.html (autocontenido; el logo va embebido en base64)
Deploy: subir la carpeta upsell-abc a Netlify (o servirla donde sea).
"""
import os
import re
import json
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "assets", "logo-blanco.png")

NAVY = "#0c3452"
NAVY2 = "#123f63"
ORANGE = "#ff6602"

# ----------------------------------------------------------------------------
# CONTENIDO — 5 módulos, en el orden del classroom.
# lesson: (título, tipo, id/url, es_apunte📒)   tipo ∈ {loom, yt}
# recurso: (título, tipo, url|None)             tipo ∈ {pdf, yt, ig, book, test, link}
# ----------------------------------------------------------------------------
MODULES = [
    {
        "emoji": "🧠", "title": "Mindset",
        "tagline": "La mentalidad que sostiene todo lo demás.",
        "sections": [
            {"name": "Mentalidad de crecimiento", "lessons": [
                ("La importancia del Mindset", "loom", "80a07d9f14444d5abf6e73471a1191c5", True),
                ("El lenguaje no es inocente", "loom", "5cae3c64ec744a49b177f2354782855b", True),
            ]},
            {"name": "Tips", "lessons": [
                ("El Observador", "loom", "8f6c57e9bda34b88b818753bfc8dd20f", True),
                ("Parálisis por análisis", "loom", "2bb1130d54c54567a639b1b4205b171c", False),
            ]},
        ],
        "recursos": [
            ("Entregable N° 2 — Mindset", "pdf", None),
        ],
    },
    {
        "emoji": "🔁", "title": "Hábitos",
        "tagline": "Tus acciones definen tu futuro.",
        "sections": [
            {"name": "Introducción", "lessons": [
                ("Tus acciones definen tu futuro", "loom", "42eb232d7ea84e3a99caaf2ff6aa3181", False),
            ]},
            {"name": "¿Cómo se forman los hábitos?", "lessons": [
                ("¿Por qué se forman los hábitos?", "loom", "33c174cfc47e41ea80eb92529241255c", False),
                ("Señal · Rutina · Recompensa", "loom", "4b72a1950eb947fb90160bb85b883c2b", False),
            ]},
            {"name": "Y ahora..?", "lessons": [
                ("¿Cómo mantener los hábitos?", "loom", "fafe046896ac4253b0d769a67e2bf1e3", False),
                ("Vision Board", "loom", "c54a1b7d94a04c03a1f4ec7d4c7f4cce", True),
            ]},
        ],
        "recursos": [
            ("Planillas Hábitos", "pdf", None),
            ("Cómo crear imágenes con IA", "yt", "https://www.youtube.com/watch?v=Azvtojs11Tg"),
        ],
    },
    {
        "emoji": "🍎", "title": "Ejercicio y Alimentación",
        "tagline": "El cuerpo es el envase del cerebro.",
        "sections": [
            {"name": "Alimentación", "lessons": [
                ("Alimentación y productividad", "loom", "352b83cc02c84fcb88cc523276c0eefb", False),
                ("El método de la glucosa", "loom", "c4495b75439f4479bab97226fcb585df", False),
                ("¿Y cómo funciona?", "loom", "536f1445d7524b6c8e2ef57c8a0a63de", False),
                ("¿Cuáles son los efectos?", "loom", "d698af731108472cbf82dda5214e592f", False),
                ("¿Cómo disminuirlos?", "loom", "954de4db93f347d5bff728bd9facc244", False),
            ]},
            {"name": "Ejercicio", "lessons": [
                ("No todo es lectura!", "loom", "456683ba632d4d3085f4275a76afc463", False),
                ("A moverse", "loom", "9d7294088dbe4b118908c4e92e39b81c", False),
            ]},
        ],
        "recursos": [
            ("Entregable N° 7 — Ejercicio y Alimentación", "pdf", None),
            ("Instagram · La diosa de la glucosa", "ig", "https://www.instagram.com/glucosegoddess/"),
            ("Instagram · Dr. Marcelo Suárez", "ig", "https://www.instagram.com/doctormarcelosuarez/"),
            ("Libro · La Revolución de la Glucosa", "book", "https://www.mercadolibre.com.ar/"),
        ],
    },
    {
        "emoji": "🎯", "title": "Concentración",
        "tagline": "Entrená el foco como se entrena un músculo.",
        "sections": [
            {"name": "Concentración", "lessons": [
                ("Contribución marginal", "loom", "05ed09cc04254ad78fe1c78712b4ec71", False),
            ]},
            {"name": "Componentes de la concentración", "lessons": [
                ("¿De qué me sirve saber esto?", "loom", "990d98e9747a4b8f902099d194a9ec88", False),
                ("El estado de alerta", "loom", "64645f53e1f0486da8597e2207a25e29", False),
                ("¿Cómo gestionar tu estado de alerta?", "loom", "9a21d3ba57614c91bb52aa4024c79cc8", False),
                ("¿Y si estás exaltado?", "loom", "921dbc6026654579865ee7b19feb3daf", False),
                ("La orientación", "loom", "2fc80854caa348d0aa9d1b77b5279e6c", True),
                ("La capacidad ejecutiva", "loom", "dd531748927c4267a6d64e9f29492913", False),
            ]},
            {"name": "Tips", "lessons": [
                ("Perlitas de la concentración", "loom", "e8160959aeb1452889fdb7271f58dd53", False),
            ]},
        ],
        "recursos": [
            ("Test ciclo circadiano", "test", "https://www.um.es/cronobiologia/"),
            ("Test de cronotipo", "test", "https://sleepdoctor.com/sleep-quizzes/chronotype-quiz/"),
            ("Cómo bloquear aplicaciones (Android)", "yt", "https://www.youtube.com/watch?v=c8_S1T8_tPo"),
            ("Tiempo en pantalla (iPhone)", "yt", "https://www.youtube.com/watch?v=t_UfArksQJg"),
            ("StayFocusd · extensión de Chrome", "link", "https://chromewebstore.google.com/detail/laankejkbhbdhmipfmgcngdelahlfoji"),
            ("Pantalla en blanco y negro (iPhone)", "yt", "https://www.youtube.com/watch?v=tFCufew50Oo"),
            ("Pantalla en blanco y negro (Android)", "yt", "https://www.youtube.com/watch?v=jp9r64-JkBw"),
            ("Entregable N° 3 — Concentración", "pdf", None),
        ],
    },
    {
        "emoji": "💾", "title": "Memoria",
        "tagline": "La metahabilidad: aprender a recordar.",
        "sections": [
            {"name": "Memoria", "lessons": [
                ("Metahabilidad", "loom", "69b46cdb65b34c7f8d50689974181ba1", False),
                ("La memoria se entrena", "loom", "6d64e9ab5572453fb52cb3db23d5fb55", False),
            ]},
            {"name": "Subprocesos", "lessons": [
                ("¿Qué es la memoria?", "loom", "a196bed22d63418c9881856c16341f01", False),
                ("La codificación de la información", "loom", "fe71f6d4121d4ee1b309c3f0bdfc620a", False),
                ("El almacenamiento de la información", "loom", "0e9f21d7c01044b6b059af682ce9f36d", False),
                ("La evocación de la información", "loom", "468a299434754ed0928fe46a4c8caca8", False),
            ]},
            {"name": "Tips", "lessons": [
                ("La regla de oro", "loom", "f0057f60aa22430aa4712f6b84e05adc", False),
                ("Cómo recordar el nombre de las personas", "loom", "894af9366bff4bdab11fb359580099d0", True),
                ("Técnicas de memorización", "loom", "6322ab4094384d7284d9537e7b58b238", True),
                ("Bonus · técnica de memoria", "yt", "TMIpkQvy2tM", False),
            ]},
        ],
        "recursos": [
            ("El mágico número 7 (inglés · PDF)", "pdf",
             "https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf"),
            ("El mágico número 7 (español)", "link", "https://www.academia.edu/"),
            ("La curva del olvido", "yt", "https://www.youtube.com/watch?v=hrGbwutALpA"),
            ("Entregable N° 4 — Memoria", "pdf", None),
        ],
    },
]

RES_ICON = {"pdf": "📄", "yt": "▶️", "ig": "📷", "book": "📕", "test": "🧪", "link": "🔗"}


def yt_id(url_or_id):
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{6,})", url_or_id)
    return m.group(1) if m else url_or_id


def embed_url(kind, ref):
    if kind == "loom":
        return "https://www.loom.com/embed/" + ref
    if kind == "yt":
        return "https://www.youtube.com/embed/" + yt_id(ref)
    return ref


def count_videos(mod):
    return sum(len(s["lessons"]) for s in mod["sections"])


TOTAL_VIDEOS = sum(count_videos(m) for m in MODULES)


def render_lessons(mi, mod):
    """Devuelve (html, lista_de_ids) de las lecciones del módulo."""
    out = []
    ids = []
    li = 0
    for sec in mod["sections"]:
        out.append(f'<div class="seclabel">{sec["name"]}</div>')
        for (title, kind, ref, note) in sec["lessons"]:
            lid = f"m{mi}-l{li}"
            ids.append(lid)
            li += 1
            emb = embed_url(kind, ref)
            badge = '<span class="badge" title="Incluye apunte">📒</span>' if note else ""
            tag = "Loom" if kind == "loom" else "YouTube"
            out.append(f'''<div class="lesson" id="{lid}">
  <div class="lrow">
    <button class="lopen" aria-expanded="false" aria-controls="{lid}-p">
      <span class="play" aria-hidden="true"></span>
      <span class="ltitle">{title}{badge}</span>
      <span class="ltag">{tag}</span>
    </button>
    <button class="lseen" data-id="{lid}" title="Marcar como visto" aria-label="Marcar como visto"><span>✓</span></button>
  </div>
  <div class="player" id="{lid}-p" data-embed="{emb}"></div>
</div>''')
    return "\n".join(out), ids


def render_resources(mod):
    if not mod.get("recursos"):
        return ""
    items = []
    for (t, kind, url) in mod["recursos"]:
        icon = RES_ICON.get(kind, "🔗")
        if url:
            items.append(
                f'<a class="res" href="{url}" target="_blank" rel="noopener">'
                f'<span class="ricon">{icon}</span><span>{t}</span>'
                f'<span class="rarrow">→</span></a>'
            )
        else:
            # PDF alojado en Skool: sin link público directo
            items.append(
                f'<div class="res res-locked" title="Se descarga dentro de la lección en Skool">'
                f'<span class="ricon">{icon}</span><span>{t}</span>'
                f'<span class="rtag">PDF · en Skool</span></div>'
            )
    return (
        '<div class="resources"><div class="reslabel">📎 Recursos y entregables</div>'
        + "".join(items) + "</div>"
    )


def render_module(mi, mod):
    lessons_html, ids = render_lessons(mi, mod)
    resources_html = render_resources(mod)
    nvid = count_videos(mod)
    open_cls = " open" if mi == 0 else ""
    aria = "true" if mi == 0 else "false"
    return f'''<section class="module{open_cls}" data-ids='{json.dumps(ids)}'>
  <button class="mhead" aria-expanded="{aria}">
    <span class="micon">{mod["emoji"]}</span>
    <span class="mtitles">
      <span class="mkicker">Módulo {mi + 1}</span>
      <span class="mtitle">{mod["title"]}</span>
      <span class="mtagline">{mod["tagline"]}</span>
    </span>
    <span class="mmeta">
      <span class="mcount"><b class="seen-count">0</b>/{nvid}</span>
      <span class="mbar"><i></i></span>
    </span>
    <span class="mchev" aria-hidden="true">⌄</span>
  </button>
  <div class="mbody">
    <div class="lessons">
      {lessons_html}
    </div>
    {resources_html}
  </div>
</section>'''


def build():
    with open(LOGO_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("ascii")
    logo_uri = "data:image/png;base64," + logo_b64

    modules_html = "\n".join(render_module(i, m) for i, m in enumerate(MODULES))

    html = PAGE.format(
        navy=NAVY, navy2=NAVY2, orange=ORANGE,
        logo=logo_uri,
        n_modules=len(MODULES),
        n_videos=TOTAL_VIDEOS,
        modules=modules_html,
    )
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK — {out}  ({len(MODULES)} módulos · {TOTAL_VIDEOS} videos)")


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>El ABC del Alto Rendimiento · NFM</title>
<meta name="description" content="Curso El ABC del Alto Rendimiento — Mindset, Hábitos, Ejercicio y Alimentación, Concentración y Memoria. Por Nico Fernández Miranda.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--navy:{navy};--navy2:{navy2};--orange:{orange};--bg:#eef3f7;--ink:#22384a;--muted:#5a7086;--card:#fff;--line:#e7eef4}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Open Sans',Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}}
h1,h2,h3,.mkicker,.mtitle,.micon,.brand,.stat b{{font-family:'Montserrat',Arial,sans-serif}}
.wrap{{max-width:840px;margin:0 auto;padding:0 18px}}
/* topbar */
.topbar{{background:var(--navy);padding:14px 0;position:sticky;top:0;z-index:50;box-shadow:0 2px 12px rgba(12,52,82,.18)}}
.topbar .wrap{{display:flex;align-items:center;justify-content:space-between;gap:12px}}
.topbar img{{height:32px;display:block}}
.topbar .brand{{color:#bcd2e2;font-weight:700;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase}}
/* hero */
.hero{{background:linear-gradient(150deg,var(--navy),var(--navy2) 60%,#0e4a75);color:#fff;padding:44px 0 40px;position:relative;overflow:hidden}}
.hero::after{{content:"";position:absolute;right:-80px;top:-80px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(255,102,2,.25),transparent 70%)}}
.hero .kicker{{color:var(--orange);font-weight:700;font-size:.76rem;letter-spacing:.2em;text-transform:uppercase;margin-bottom:12px}}
.hero h1{{font-size:2.3rem;font-weight:800;line-height:1.05;letter-spacing:-.02em;max-width:620px}}
.hero p{{color:#c8d9e6;margin-top:12px;max-width:560px;font-size:1.05rem}}
.stats{{display:flex;gap:26px;margin-top:22px;flex-wrap:wrap}}
.stat{{display:flex;flex-direction:column}}
.stat b{{font-size:1.5rem;font-weight:800;color:#fff;line-height:1}}
.stat span{{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:#9db8cc;margin-top:4px}}
/* progreso global */
.gprog{{background:var(--card);border-radius:14px;box-shadow:0 8px 26px rgba(12,52,82,.12);padding:16px 20px;margin-top:-26px;position:relative;z-index:5;display:flex;align-items:center;gap:16px}}
.gprog .lbl{{font-family:'Montserrat';font-weight:700;color:var(--navy);font-size:.9rem;white-space:nowrap}}
.gprog .track{{flex:1;height:10px;background:#e4ecf3;border-radius:6px;overflow:hidden}}
.gprog .track i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),#ff8a3d);border-radius:6px;transition:width .5s ease}}
.gprog .pct{{font-family:'Montserrat';font-weight:800;color:var(--orange);font-size:1rem;min-width:42px;text-align:right}}
/* modules */
main{{padding:26px 0 10px}}
.module{{background:var(--card);border-radius:16px;box-shadow:0 4px 18px rgba(12,52,82,.08);margin-bottom:16px;overflow:hidden;border:1px solid var(--line)}}
.mhead{{width:100%;background:none;border:none;cursor:pointer;display:flex;align-items:center;gap:16px;padding:18px 20px;text-align:left;font:inherit;color:inherit}}
.mhead:hover{{background:#f7fafc}}
.micon{{flex:0 0 52px;height:52px;border-radius:14px;background:linear-gradient(145deg,var(--navy),var(--navy2));display:flex;align-items:center;justify-content:center;font-size:1.6rem}}
.mtitles{{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}}
.mkicker{{color:var(--orange);font-weight:700;font-size:.66rem;letter-spacing:.16em;text-transform:uppercase}}
.mtitle{{font-size:1.18rem;font-weight:800;color:var(--navy);line-height:1.2}}
.mtagline{{color:var(--muted);font-size:.86rem}}
.mmeta{{display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex:0 0 auto}}
.mcount{{font-size:.78rem;color:var(--muted);font-weight:600}}
.mcount b{{color:var(--navy)}}
.mbar{{width:74px;height:6px;background:#e4ecf3;border-radius:4px;overflow:hidden;display:block}}
.mbar i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),#ff8a3d);transition:width .4s}}
.mchev{{flex:0 0 auto;color:var(--muted);font-size:1.5rem;transition:transform .3s;line-height:1}}
.module.open .mchev{{transform:rotate(180deg)}}
.mbody{{display:none;padding:6px 20px 22px}}
.module.open .mbody{{display:block}}
/* secciones + lecciones */
.seclabel{{font-family:'Montserrat';font-weight:700;color:var(--navy);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;margin:16px 0 8px;padding-left:2px;opacity:.8}}
.lesson{{border:1px solid var(--line);border-radius:12px;margin-bottom:8px;overflow:hidden;background:#fbfdff}}
.lrow{{display:flex;align-items:stretch}}
.lopen{{flex:1;min-width:0;display:flex;align-items:center;gap:12px;background:none;border:none;cursor:pointer;padding:13px 14px;text-align:left;font:inherit;color:var(--ink)}}
.lopen:hover{{background:#f2f7fb}}
.play{{flex:0 0 30px;height:30px;border-radius:50%;background:var(--navy);position:relative;transition:background .2s,transform .2s}}
.play::after{{content:"";position:absolute;top:50%;left:54%;transform:translate(-50%,-50%);border-style:solid;border-width:6px 0 6px 10px;border-color:transparent transparent transparent #fff}}
.lesson.open .play{{background:var(--orange)}}
.lesson.open .play::after{{border-width:0;width:9px;height:9px;background:#fff;left:50%;border-radius:1px}}
.lopen:hover .play{{transform:scale(1.08)}}
.ltitle{{flex:1;min-width:0;font-weight:600;font-size:.98rem}}
.badge{{margin-left:6px}}
.ltag{{flex:0 0 auto;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;border:1px solid var(--line);border-radius:20px;padding:3px 9px}}
.lseen{{flex:0 0 46px;background:none;border:none;border-left:1px solid var(--line);cursor:pointer;color:#c3d2de;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:color .2s,background .2s}}
.lseen span{{width:24px;height:24px;border-radius:50%;border:2px solid currentColor;display:flex;align-items:center;justify-content:center;font-size:.8rem;line-height:1}}
.lseen:hover{{color:var(--orange)}}
.lesson.seen .lseen{{color:#12a150}}
.lesson.seen .lseen span{{background:#12a150;border-color:#12a150;color:#fff}}
.lesson.seen .ltitle{{color:var(--muted)}}
.player{{display:none;background:#000}}
.lesson.open .player{{display:block}}
.player .frame{{position:relative;width:100%;padding-bottom:56.25%;height:0}}
.player iframe{{position:absolute;top:0;left:0;width:100%;height:100%;border:0}}
/* recursos */
.resources{{margin-top:18px;background:#f4f8fb;border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.reslabel{{font-family:'Montserrat';font-weight:700;color:var(--navy);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}}
.res{{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:9px;text-decoration:none;color:var(--ink);font-size:.92rem;font-weight:600;transition:background .15s;border:1px solid transparent}}
a.res:hover{{background:#fff;border-color:var(--line)}}
.ricon{{flex:0 0 auto;font-size:1.05rem}}
.res span:nth-child(2){{flex:1;min-width:0}}
.rarrow{{color:var(--orange);font-weight:800}}
.res-locked{{color:var(--muted);cursor:default}}
.rtag{{font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:20px;padding:3px 9px;font-weight:700}}
/* footer */
footer{{background:var(--navy);color:#9db8cc;margin-top:34px;padding:30px 0;text-align:center;font-size:.85rem}}
footer img{{height:28px;margin-bottom:12px;opacity:.95}}
footer .q{{font-family:'Montserrat';font-weight:700;color:#fff;font-size:1rem;margin-bottom:6px}}
@media(max-width:640px){{
  .hero h1{{font-size:1.7rem}}
  .mtagline{{display:none}}
  .mmeta .mcount{{display:none}}
  .ltag{{display:none}}
  .micon{{flex-basis:44px;height:44px;font-size:1.3rem}}
}}
</style>
</head>
<body>
<div class="topbar"><div class="wrap">
  <img src="{logo}" alt="NFM — Instituto de Productividad">
  <span class="brand">Alto Rendimiento</span>
</div></div>

<header class="hero"><div class="wrap">
  <div class="kicker">Curso · Acceso completo</div>
  <h1>El ABC del Alto Rendimiento</h1>
  <p>Los cimientos de cómo funciona tu cerebro, en 5 módulos. Ciencia bajada a lo práctico, con Nico de guía. No es motivación, es ciencia.</p>
  <div class="stats">
    <div class="stat"><b>{n_modules}</b><span>Módulos</span></div>
    <div class="stat"><b>{n_videos}</b><span>Lecciones</span></div>
    <div class="stat"><b>∞</b><span>Acceso</span></div>
  </div>
</div></header>

<div class="wrap">
  <div class="gprog">
    <span class="lbl">Tu progreso</span>
    <span class="track"><i id="gbar"></i></span>
    <span class="pct" id="gpct">0%</span>
  </div>
</div>

<main><div class="wrap">
{modules}
</div></main>

<footer><div class="wrap">
  <img src="{logo}" alt="NFM">
  <div class="q">"No es motivación, es ciencia."</div>
  <div>El ABC del Alto Rendimiento · Nico Fernández Miranda · Instituto de Productividad</div>
</div></footer>

<script>
(function(){{
  var SEEN_KEY='abc_seen';
  var seen={{}};
  try{{seen=JSON.parse(localStorage.getItem(SEEN_KEY)||'{{}}')}}catch(e){{}}
  var TOTAL={n_videos};

  // ---- acordeón de módulos ----
  document.querySelectorAll('.mhead').forEach(function(h){{
    h.addEventListener('click',function(){{
      var m=h.closest('.module');
      var open=m.classList.toggle('open');
      h.setAttribute('aria-expanded',open?'true':'false');
    }});
  }});

  // ---- abrir lección + embeber lazy ----
  document.querySelectorAll('.lopen').forEach(function(b){{
    b.addEventListener('click',function(){{
      var lesson=b.closest('.lesson');
      var player=lesson.querySelector('.player');
      var open=lesson.classList.toggle('open');
      b.setAttribute('aria-expanded',open?'true':'false');
      if(open && !player.dataset.loaded){{
        var src=player.dataset.embed;
        player.innerHTML='<div class="frame"><iframe src="'+src+'" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>';
        player.dataset.loaded='1';
      }}
    }});
  }});

  // ---- marcar visto ----
  function save(){{try{{localStorage.setItem(SEEN_KEY,JSON.stringify(seen))}}catch(e){{}}}}
  function refresh(){{
    var done=0;
    document.querySelectorAll('.module').forEach(function(m){{
      var ids=[];try{{ids=JSON.parse(m.dataset.ids||'[]')}}catch(e){{}}
      var c=0;ids.forEach(function(id){{if(seen[id])c++}});
      done+=c;
      var bar=m.querySelector('.mbar i'),cnt=m.querySelector('.seen-count');
      if(bar)bar.style.width=(ids.length?Math.round(c/ids.length*100):0)+'%';
      if(cnt)cnt.textContent=c;
    }});
    var pct=TOTAL?Math.round(done/TOTAL*100):0;
    var gb=document.getElementById('gbar'),gp=document.getElementById('gpct');
    if(gb)gb.style.width=pct+'%';
    if(gp)gp.textContent=pct+'%';
  }}
  document.querySelectorAll('.lseen').forEach(function(s){{
    var id=s.dataset.id;
    if(seen[id])s.closest('.lesson').classList.add('seen');
    s.addEventListener('click',function(){{
      var lesson=s.closest('.lesson');
      if(seen[id]){{delete seen[id];lesson.classList.remove('seen')}}
      else{{seen[id]=1;lesson.classList.add('seen')}}
      save();refresh();
    }});
  }});
  refresh();
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
