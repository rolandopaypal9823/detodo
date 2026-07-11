# -*- coding: utf-8 -*-
"""El ABC del Alto Rendimiento — página de curso estilo 'classroom'.

Director de arte (skill awesome-design):
- ESQUELETO: Mintlify (layout de documentación/aprendizaje: sidebar de navegación +
  panel principal de contenido; item activo resaltado; densidad legible).
- PIEL: NFM (Azul #0c3452, Naranja Acción #ff6602 como ÚNICO acento, Montserrat + Open Sans,
  sombras teñidas de azul, pill buttons, motion ascendente).

Comportamiento tipo plataforma de curso: el sidebar lista los 5 módulos con sus lecciones;
al hacer clic en una lección, su video (Loom/YouTube) se carga en el reproductor principal.
Progreso por módulo y global, "marcar visto", prev/next, y recuerda la última lección vista.

Uso:  python3 build_abc.py   →  index.html (autocontenido; logo embebido en base64)
"""
import os
import re
import json
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_NAVY = os.path.join(HERE, "assets", "logo-navy.png")
LOGO_WHITE = os.path.join(HERE, "assets", "logo-blanco.png")

# ---- Contenido (idéntico al inventario del classroom) -----------------------
# lesson: (título, tipo, id/url, es_apunte📒)   tipo ∈ {loom, yt}
# recurso: (título, tipo, url|None)             tipo ∈ {pdf, yt, ig, book, test, link}
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
        "recursos": [("Entregable N° 2 — Mindset", "pdf", None)],
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

RES_ICON = {"pdf": "📄", "yt": "▶", "ig": "📷", "book": "📕", "test": "🧪", "link": "🔗"}


def yt_id(s):
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{6,})", s)
    return m.group(1) if m else s


def embed_url(kind, ref):
    if kind == "loom":
        return "https://www.loom.com/embed/" + ref
    if kind == "yt":
        return "https://www.youtube.com/embed/" + yt_id(ref)
    return ref


def count_videos(mod):
    return sum(len(s["lessons"]) for s in mod["sections"])


TOTAL_VIDEOS = sum(count_videos(m) for m in MODULES)


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


# ---- construir JSON de lecciones para el JS + HTML del sidebar --------------
def build_data():
    lessons = []       # orden lineal para prev/next
    sidebar_parts = []
    for mi, mod in enumerate(MODULES):
        nvid = count_videos(mod)
        sidebar_parts.append(
            f'<div class="s-mod open" data-mod="{mi}">'
            f'<button class="s-mhead" aria-expanded="true">'
            f'<span class="s-emoji">{mod["emoji"]}</span>'
            f'<span class="s-mtitle">{mod["title"]}</span>'
            f'<span class="s-mprog"><b class="s-seen">0</b>/{nvid}</span>'
            f'<span class="s-chev">⌄</span></button>'
            f'<div class="s-mbody">'
        )
        li = 0
        for sec in mod["sections"]:
            sidebar_parts.append(f'<div class="s-sec">{sec["name"]}</div>')
            for (title, kind, ref, note) in sec["lessons"]:
                lid = f"m{mi}-l{li}"
                li += 1
                emb = embed_url(kind, ref)
                lessons.append({
                    "id": lid, "m": mi, "mtitle": mod["title"], "emoji": mod["emoji"],
                    "sec": sec["name"], "title": title, "type": kind, "embed": emb, "note": note,
                })
                badge = '<span class="s-badge" title="Incluye apunte">📒</span>' if note else ""
                sidebar_parts.append(
                    f'<button class="s-lesson" data-id="{lid}">'
                    f'<span class="s-dot" data-seen="{lid}" title="Marcar como visto"></span>'
                    f'<span class="s-ltitle">{title}{badge}</span></button>'
                )
        sidebar_parts.append("</div></div>")
    return lessons, "".join(sidebar_parts)


def build_resources_js():
    res = []
    for mi, mod in enumerate(MODULES):
        items = []
        for (t, kind, url) in mod.get("recursos", []):
            items.append({"t": t, "icon": RES_ICON.get(kind, "🔗"), "url": url,
                          "locked": url is None})
        res.append(items)
    return res


def build():
    lessons, sidebar_html = build_data()
    resources = build_resources_js()
    logo_white = b64(LOGO_WHITE)

    html = PAGE.format(
        navy="#0c3452", orange="#ff6602",
        logo_white=logo_white,
        n_modules=len(MODULES), n_videos=TOTAL_VIDEOS,
        sidebar=sidebar_html,
        lessons_json=json.dumps(lessons, ensure_ascii=False),
        resources_json=json.dumps(resources, ensure_ascii=False),
    )
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK — {out}  ({len(MODULES)} módulos · {TOTAL_VIDEOS} lecciones)")


PAGE = r"""<!DOCTYPE html>
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
:root{{
  --navy:{navy};--navy2:#123f63;--orange:{orange};--orange-hover:#e65a00;--orange-soft:#fff1e8;
  --ink:#0c3452;--body:#3a4a57;--muted:#6b7a86;--steel:#5b7488;
  --canvas:#fff;--surface:#f5f7f9;--hairline:#e3e8ec;
  --topbar-h:60px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Open Sans',-apple-system,system-ui,sans-serif;background:var(--canvas);color:var(--body);line-height:1.6}}
h1,h2,h3,h4,.font-h{{font-family:'Montserrat',sans-serif}}
a{{color:var(--orange);text-decoration:none}}
::selection{{background:var(--orange-soft)}}
/* ---------- topbar ---------- */
.topbar{{height:var(--topbar-h);background:var(--navy);position:sticky;top:0;z-index:60;display:flex;align-items:center;justify-content:space-between;padding:0 20px;box-shadow:0 1px 0 rgba(255,255,255,.06)}}
.topbar .left{{display:flex;align-items:center;gap:14px;min-width:0}}
.topbar img{{height:28px;display:block}}
.topbar .crumb{{color:#bcd2e2;font-family:'Montserrat';font-weight:700;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.topbar .right{{display:flex;align-items:center;gap:14px}}
.tp-prog{{display:flex;align-items:center;gap:9px}}
.tp-prog .track{{width:120px;height:7px;background:rgba(255,255,255,.16);border-radius:5px;overflow:hidden}}
.tp-prog .track i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),#ff8a3d);transition:width .5s cubic-bezier(.22,1,.36,1)}}
.tp-prog .pct{{color:#fff;font-family:'Montserrat';font-weight:800;font-size:.82rem;min-width:34px;text-align:right}}
.burger{{display:none;background:none;border:1px solid rgba(255,255,255,.22);color:#fff;border-radius:8px;width:38px;height:34px;font-size:1.1rem;cursor:pointer}}
/* ---------- shell ---------- */
.shell{{display:flex;align-items:flex-start}}
/* ---------- sidebar ---------- */
.sidebar{{flex:0 0 306px;width:306px;border-right:1px solid var(--hairline);height:calc(100vh - var(--topbar-h));position:sticky;top:var(--topbar-h);overflow-y:auto;background:var(--canvas);padding:20px 14px 40px}}
.s-head{{padding:6px 8px 16px}}
.s-kicker{{color:var(--orange);font-family:'Montserrat';font-weight:700;font-size:.62rem;letter-spacing:.18em;text-transform:uppercase}}
.s-title{{font-family:'Montserrat';font-weight:800;color:var(--ink);font-size:1.12rem;line-height:1.2;margin:4px 0 12px}}
.s-gprog{{display:flex;align-items:center;gap:9px}}
.s-gprog .track{{flex:1;height:8px;background:var(--surface);border-radius:5px;overflow:hidden;border:1px solid var(--hairline)}}
.s-gprog .track i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),#ff8a3d);transition:width .5s cubic-bezier(.22,1,.36,1)}}
.s-gprog .pct{{font-family:'Montserrat';font-weight:800;color:var(--orange);font-size:.8rem;min-width:34px;text-align:right}}
.s-mod{{margin-top:6px;border-radius:10px}}
.s-mhead{{width:100%;display:flex;align-items:center;gap:10px;background:none;border:none;cursor:pointer;padding:10px 8px;border-radius:9px;font:inherit;color:var(--ink);text-align:left}}
.s-mhead:hover{{background:var(--surface)}}
.s-emoji{{flex:0 0 30px;height:30px;border-radius:8px;background:linear-gradient(145deg,var(--navy),var(--navy2));display:flex;align-items:center;justify-content:center;font-size:1rem}}
.s-mtitle{{flex:1;min-width:0;font-family:'Montserrat';font-weight:700;font-size:.92rem;line-height:1.15}}
.s-mprog{{font-size:.68rem;color:var(--muted);font-weight:700;white-space:nowrap}}
.s-mprog b{{color:var(--ink)}}
.s-chev{{color:var(--muted);font-size:1.1rem;transition:transform .28s cubic-bezier(.22,1,.36,1)}}
.s-mod.open .s-chev{{transform:rotate(180deg)}}
.s-mbody{{display:none;padding:2px 0 8px}}
.s-mod.open .s-mbody{{display:block}}
.s-sec{{font-family:'Montserrat';font-weight:700;color:var(--steel);font-size:.6rem;letter-spacing:.13em;text-transform:uppercase;padding:12px 10px 5px}}
.s-lesson{{width:100%;display:flex;align-items:center;gap:10px;background:none;border:none;cursor:pointer;padding:8px 10px;border-radius:8px;font:inherit;color:var(--body);text-align:left;line-height:1.3;position:relative}}
.s-lesson:hover{{background:var(--surface)}}
.s-lesson.active{{background:var(--orange-soft)}}
.s-lesson.active::before{{content:"";position:absolute;left:0;top:6px;bottom:6px;width:3px;border-radius:3px;background:var(--orange)}}
.s-lesson.active .s-ltitle{{color:var(--ink);font-weight:700}}
.s-dot{{flex:0 0 16px;height:16px;border-radius:50%;border:2px solid #c3d2de;transition:all .2s;display:flex;align-items:center;justify-content:center}}
.s-dot::after{{content:"✓";color:#fff;font-size:.6rem;opacity:0;font-weight:700}}
.s-lesson.seen .s-dot{{background:#12a150;border-color:#12a150}}
.s-lesson.seen .s-dot::after{{opacity:1}}
.s-lesson.seen .s-ltitle{{color:var(--muted)}}
.s-ltitle{{flex:1;min-width:0;font-size:.86rem}}
.s-badge{{margin-left:5px;font-size:.85em}}
/* ---------- main ---------- */
.main{{flex:1;min-width:0}}
.main-inner{{max-width:900px;margin:0 auto;padding:30px 30px 60px}}
.crumbs{{display:flex;align-items:center;gap:8px;font-size:.74rem;color:var(--muted);font-family:'Montserrat';font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:14px;flex-wrap:wrap}}
.crumbs .sep{{opacity:.5}}
.crumbs .c-mod{{color:var(--orange)}}
.player-wrap{{background:var(--navy);border-radius:16px;overflow:hidden;box-shadow:0 1px 3px rgba(12,52,82,.08),0 14px 40px rgba(12,52,82,.12);opacity:0;transform:translateY(14px);transition:opacity .5s cubic-bezier(.22,1,.36,1),transform .5s cubic-bezier(.22,1,.36,1)}}
.player-wrap.in{{opacity:1;transform:none}}
.frame{{position:relative;width:100%;padding-bottom:56.25%;height:0;background:#000}}
.frame iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.lhead{{display:flex;align-items:flex-start;gap:16px;margin:22px 0 4px}}
.lhead h1{{flex:1;min-width:0;font-size:1.72rem;font-weight:800;color:var(--ink);line-height:1.15;letter-spacing:-.01em}}
.ltag{{flex:0 0 auto;font-family:'Montserrat';font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:var(--steel);font-weight:700;border:1px solid var(--hairline);border-radius:999px;padding:5px 12px;margin-top:4px}}
.lactions{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 0 8px}}
.btn-seen{{display:inline-flex;align-items:center;gap:9px;background:var(--orange);color:#fff;border:none;border-radius:999px;font-family:'Montserrat';font-weight:700;font-size:.92rem;padding:12px 24px;cursor:pointer;box-shadow:0 8px 24px rgba(255,102,2,.28);transition:transform .18s,background .18s}}
.btn-seen:hover{{transform:translateY(-1px);background:var(--orange-hover)}}
.btn-seen .ck{{width:19px;height:19px;border-radius:50%;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:.66rem}}
.btn-seen.done{{background:#12a150;box-shadow:0 8px 24px rgba(18,161,80,.25)}}
.btn-seen.done .ck{{background:#fff;color:#12a150}}
.nav-btns{{display:flex;gap:10px;margin-left:auto}}
.nav-btn{{display:inline-flex;align-items:center;gap:7px;background:transparent;border:1.5px solid var(--hairline);color:var(--ink);border-radius:999px;font-family:'Montserrat';font-weight:700;font-size:.84rem;padding:10px 18px;cursor:pointer;transition:border-color .18s,background .18s}}
.nav-btn:hover:not(:disabled){{border-color:var(--navy);background:var(--surface)}}
.nav-btn:disabled{{opacity:.4;cursor:not-allowed}}
/* recursos */
.resources{{margin-top:34px;border-top:1px solid var(--hairline);padding-top:24px}}
.reslabel{{font-family:'Montserrat';font-weight:800;color:var(--ink);font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.reslist{{display:grid;gap:8px}}
.res{{display:flex;align-items:center;gap:12px;padding:13px 15px;border:1px solid var(--hairline);border-radius:12px;color:var(--ink);font-weight:600;font-size:.94rem;background:var(--canvas);transition:border-color .15s,box-shadow .15s,transform .15s}}
a.res:hover{{border-color:#cfe0ec;box-shadow:0 6px 18px rgba(12,52,82,.07);transform:translateY(-1px)}}
.res .ricon{{flex:0 0 34px;height:34px;border-radius:9px;background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:1rem}}
.res .rtx{{flex:1;min-width:0}}
.res .rarrow{{color:var(--orange);font-weight:800;font-size:1.1rem}}
.res-locked{{color:var(--muted);background:var(--surface)}}
.res-locked .rtag{{font-family:'Montserrat';font-size:.58rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border:1px solid var(--hairline);border-radius:999px;padding:4px 9px;font-weight:700}}
/* backdrop mobile */
.backdrop{{display:none;position:fixed;inset:var(--topbar-h) 0 0;background:rgba(12,52,82,.45);z-index:40}}
/* footer */
footer{{background:var(--navy);color:#9db8cc;padding:26px 20px;text-align:center;font-size:.82rem}}
footer .q{{font-family:'Montserrat';font-weight:700;color:#fff;margin-bottom:4px}}
/* responsive */
@media(max-width:940px){{
  .burger{{display:block}}
  .tp-prog .track{{width:80px}}
  .sidebar{{position:fixed;top:var(--topbar-h);left:0;bottom:0;height:auto;z-index:50;transform:translateX(-104%);transition:transform .3s cubic-bezier(.22,1,.36,1);box-shadow:8px 0 30px rgba(12,52,82,.18);width:300px;flex-basis:300px}}
  .sidebar.open{{transform:none}}
  .backdrop.show{{display:block}}
  .main-inner{{padding:22px 18px 50px}}
  .lhead h1{{font-size:1.4rem}}
}}
@media(max-width:560px){{
  .topbar .crumb{{display:none}}
  .nav-btns{{margin-left:0;width:100%}}
  .nav-btn{{flex:1;justify-content:center}}
}}
</style>
</head>
<body>
<div class="topbar">
  <div class="left">
    <button class="burger" id="burger" aria-label="Abrir módulos">☰</button>
    <img src="{logo_white}" alt="NFM — Instituto de Productividad">
    <span class="crumb">El ABC del Alto Rendimiento</span>
  </div>
  <div class="right">
    <div class="tp-prog"><span class="track"><i id="tpbar"></i></span><span class="pct" id="tppct">0%</span></div>
  </div>
</div>

<div class="shell">
  <aside class="sidebar" id="sidebar">
    <div class="s-head">
      <div class="s-kicker">Curso · {n_modules} módulos · {n_videos} lecciones</div>
      <div class="s-title">El ABC del Alto Rendimiento</div>
      <div class="s-gprog"><span class="track"><i id="sbar"></i></span><span class="pct" id="spct">0%</span></div>
    </div>
    {sidebar}
  </aside>
  <div class="backdrop" id="backdrop"></div>

  <main class="main"><div class="main-inner">
    <div class="crumbs" id="crumbs"></div>
    <div class="player-wrap" id="playerWrap"><div class="frame" id="frame"></div></div>
    <div class="lhead"><h1 id="lTitle">—</h1><span class="ltag" id="lTag"></span></div>
    <div class="lactions">
      <button class="btn-seen" id="btnSeen"><span class="ck">✓</span><span id="btnSeenTx">Marcar como visto</span></button>
      <div class="nav-btns">
        <button class="nav-btn" id="prevBtn">← Anterior</button>
        <button class="nav-btn" id="nextBtn">Siguiente →</button>
      </div>
    </div>
    <div class="resources" id="resources"></div>
  </div></main>
</div>

<footer>
  <div class="q">"No es motivación, es ciencia."</div>
  <div>El ABC del Alto Rendimiento · Nico Fernández Miranda · Instituto de Productividad</div>
</footer>

<script>
(function(){{
  var LESSONS={lessons_json};
  var RES={resources_json};
  var TOTAL={n_videos};
  var SEEN_KEY='abc_seen_v2', LAST_KEY='abc_last_v2';
  var seen={{}}; try{{seen=JSON.parse(localStorage.getItem(SEEN_KEY)||'{{}}')}}catch(e){{}}
  var byId={{}}; LESSONS.forEach(function(l){{byId[l.id]=l}});
  var order=LESSONS.map(function(l){{return l.id}});
  var current=null;

  var frame=document.getElementById('frame');
  var pw=document.getElementById('playerWrap');

  function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}}

  function renderResources(mi){{
    var box=document.getElementById('resources');
    var items=RES[mi]||[];
    if(!items.length){{box.innerHTML='';return}}
    var html='<div class="reslabel">📎 Recursos y entregables</div><div class="reslist">';
    items.forEach(function(r){{
      if(r.locked){{
        html+='<div class="res res-locked"><span class="ricon">'+r.icon+'</span><span class="rtx">'+esc(r.t)+'</span><span class="rtag">PDF · en Skool</span></div>';
      }}else{{
        html+='<a class="res" href="'+r.url+'" target="_blank" rel="noopener"><span class="ricon">'+r.icon+'</span><span class="rtx">'+esc(r.t)+'</span><span class="rarrow">→</span></a>';
      }}
    }});
    box.innerHTML=html+'</div>';
  }}

  function select(id, push){{
    var l=byId[id]; if(!l) return;
    current=id;
    // player (lazy: recién al seleccionar)
    pw.classList.remove('in');
    frame.innerHTML='<iframe src="'+l.embed+'" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>';
    void pw.offsetWidth; pw.classList.add('in');
    // meta
    document.getElementById('lTitle').innerHTML=esc(l.title)+(l.note?' <span title="Incluye apunte" style="font-size:.8em">📒</span>':'');
    document.getElementById('lTag').textContent=(l.type==='loom'?'Loom':'YouTube');
    document.getElementById('crumbs').innerHTML=
      '<span class="c-mod">'+l.emoji+' '+esc(l.mtitle)+'</span><span class="sep">›</span><span>'+esc(l.sec)+'</span>';
    renderResources(l.m);
    // sidebar active
    document.querySelectorAll('.s-lesson').forEach(function(b){{b.classList.toggle('active',b.dataset.id===id)}});
    // abrir el módulo del lesson en el sidebar
    var active=document.querySelector('.s-lesson[data-id="'+id+'"]');
    if(active){{var mod=active.closest('.s-mod'); if(mod && !mod.classList.contains('open')){{mod.classList.add('open');mod.querySelector('.s-mhead').setAttribute('aria-expanded','true')}}
      active.scrollIntoView({{block:'nearest'}});}}
    // seen button
    var sb=document.getElementById('btnSeen');
    var done=!!seen[id];
    sb.classList.toggle('done',done);
    document.getElementById('btnSeenTx').textContent=done?'Visto ✓':'Marcar como visto';
    // prev/next
    var idx=order.indexOf(id);
    document.getElementById('prevBtn').disabled=idx<=0;
    document.getElementById('nextBtn').disabled=idx>=order.length-1;
    try{{localStorage.setItem(LAST_KEY,id)}}catch(e){{}}
    if(push!==false){{document.querySelector('.main-inner').scrollIntoView({{block:'start',behavior:'smooth'}});}}
    // cerrar drawer en mobile
    closeDrawer();
  }}

  function save(){{try{{localStorage.setItem(SEEN_KEY,JSON.stringify(seen))}}catch(e){{}}}}
  function refresh(){{
    var done=0;
    document.querySelectorAll('.s-mod').forEach(function(mod){{
      var ls=mod.querySelectorAll('.s-lesson'),c=0;
      ls.forEach(function(b){{var s=!!seen[b.dataset.id];b.classList.toggle('seen',s);if(s)c++}});
      done+=c;
      var sc=mod.querySelector('.s-seen'); if(sc)sc.textContent=c;
    }});
    var pct=TOTAL?Math.round(done/TOTAL*100):0;
    ['sbar','tpbar'].forEach(function(idb){{var b=document.getElementById(idb);if(b)b.style.width=pct+'%'}});
    ['spct','tppct'].forEach(function(idp){{var p=document.getElementById(idp);if(p)p.textContent=pct+'%'}});
  }}
  function toggleSeen(id){{
    if(seen[id])delete seen[id]; else seen[id]=1;
    save();refresh();
    if(id===current){{
      var done=!!seen[id];
      document.getElementById('btnSeen').classList.toggle('done',done);
      document.getElementById('btnSeenTx').textContent=done?'Visto ✓':'Marcar como visto';
    }}
  }}

  // eventos sidebar
  document.querySelectorAll('.s-lesson').forEach(function(b){{
    b.addEventListener('click',function(e){{
      if(e.target.closest('.s-dot')){{toggleSeen(b.dataset.id);e.stopPropagation();return}}
      select(b.dataset.id);
    }});
  }});
  document.querySelectorAll('.s-dot').forEach(function(d){{
    d.addEventListener('click',function(e){{e.stopPropagation();toggleSeen(d.dataset.seen)}});
  }});
  document.querySelectorAll('.s-mhead').forEach(function(h){{
    h.addEventListener('click',function(){{
      var m=h.closest('.s-mod');var op=m.classList.toggle('open');
      h.setAttribute('aria-expanded',op?'true':'false');
    }});
  }});
  // botones main
  document.getElementById('btnSeen').addEventListener('click',function(){{if(current)toggleSeen(current)}});
  document.getElementById('prevBtn').addEventListener('click',function(){{var i=order.indexOf(current);if(i>0)select(order[i-1])}});
  document.getElementById('nextBtn').addEventListener('click',function(){{var i=order.indexOf(current);if(i<order.length-1)select(order[i+1])}});
  // drawer mobile
  var sidebar=document.getElementById('sidebar'),backdrop=document.getElementById('backdrop');
  function closeDrawer(){{sidebar.classList.remove('open');backdrop.classList.remove('show')}}
  document.getElementById('burger').addEventListener('click',function(){{
    var op=sidebar.classList.toggle('open');backdrop.classList.toggle('show',op);
  }});
  backdrop.addEventListener('click',closeDrawer);

  // init: última lección vista o la primera
  refresh();
  var last=null; try{{last=localStorage.getItem(LAST_KEY)}}catch(e){{}}
  select((last&&byId[last])?last:order[0], false);
}})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
