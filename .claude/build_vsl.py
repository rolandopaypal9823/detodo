#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las dos versiones de la VSL landing del Instituto (A y B: mismo
cuerpo, distinto video de vturb) a partir de instituto-booking.html.

Ademas del video, aplica la limpieza de copy (sin conceptos repetidos ni
subtitulos de relleno), suma la historia de Nico y el widget "El camino"
(Punto A → Punto B → La Escalera → Como accedes), y ajusta el celular.
Las fotos del camino viven en /vsl-assets (sacadas del deck "Escala tu vida").
"""
import io, os, re

BASE = "/home/user/detodo"
SCR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tsl-assets")
ORIGEN = os.path.join(BASE, "instituto-booking.html")
HISTORIA = io.open(os.path.join(SCR, "historia.html"), encoding="utf-8").read()
CAMINO   = io.open(os.path.join(SCR, "camino.html"), encoding="utf-8").read()
# el widget de la historia usaba la misma pildora de fondo naranja que la landing; va plana como el resto
HISTORIA = re.sub(r"^\.nfmh-eyebrow\{[^\n]*\n",
    ".nfmh-eyebrow{display:inline-block;font-family:'JetBrains Mono',monospace;text-transform:uppercase;"
    "letter-spacing:.22em;font-size:11px;font-weight:500;color:var(--nfmh-orange-text);margin-bottom:16px}\n",
    HISTORIA, flags=re.M)
assert "border-radius:100px" not in HISTORIA

# ─────────────────────────────────────────────── titular (se elige aparte)
# Mientras no se elija, queda el titular actual de la landing.
TITULO = 'Dejá de pagar el sobreprecio de ser <span class="shimmer">“productivo”</span>.'
SUB    = ('Recuperá tu tiempo, tu claridad mental y avanzá en lo tuyo — con un '
          '<b>sistema con base en neurociencia</b>, no con más disciplina.')
TITLE_TAG = 'Instituto de Productividad · Dejá de pagar el sobreprecio de ser productivo'
META_DESC = ('Recuperá tu tiempo, tu claridad mental y avanzá en lo tuyo con un sistema con base en '
             'neurociencia, no con más disciplina. Mirá el video y aplicá a tu entrevista de admisión.')

VTURB_CUENTA = "82529694-4445-4a28-9435-65713f4bcce6"
VERSIONES = [
    ("instituto-vsl-a.html", "A", "6aad0c7e4524b264a54cbbb3"),
    ("instituto-vsl-b.html", "B", "6aac5b499de2f947efaa1453"),
]


def reemplazar(s, viejo, nuevo, etq, veces=1):
    n = s.count(viejo)
    assert n == veces, "%s: esperaba %d, hay %d" % (etq, veces, n)
    return s.replace(viejo, nuevo)


def cortar(s, desde, hasta, etq, incluir_hasta=True):
    """Borra desde el marcador `desde` hasta el marcador `hasta` (inclusive)."""
    i = s.index(desde)
    j = s.index(hasta, i)
    if incluir_hasta:
        j += len(hasta)
    assert s.count(desde) == 1, etq
    return s[:i] + s[j:]


def construir(version, vturb_id):
    s = io.open(ORIGEN, encoding="utf-8").read()

    # ═══════════════════════════════════════════ 1) VIDEO: Loom → vturb
    bloque_video_viejo = s[s.index('        <div class="video-frame" id="vslFrame">'):
                           s.index('    <div class="hero-cta fade-up d4" id="aplicar">')]
    bloque_video_nuevo = (
        '        <!-- VSL · vturb. Para cambiar el video: reemplazá el ID en las DOS lineas marcadas -->\n'
        '        <div class="video-vturb" id="vslFrame">\n'
        '          <span class="corner tl"></span><span class="corner tr"></span>\n'
        '          <span class="corner bl"></span><span class="corner br"></span>\n'
        '          <vturb-smartplayer id="vid-%(id)s" style="display: block; margin: 0 auto; width: 100%%;">'          # ← ID
        '<div class="vturb-player-placeholder" style="position: relative; width: 100%%; padding: 56.25%% 0 0; z-index: 0; background-color: black;"></div>'
        '</vturb-smartplayer>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '    <script>\n'
        '    (function(){ var s=document.createElement("script");\n'
        '      s.src="https://scripts.converteai.net/%(cuenta)s/players/%(id)s/v4/player.js";'   # ← ID
        ' s.async=!0; document.head.appendChild(s); })();\n'
        '    </script>\n\n'
    ) % {"id": vturb_id, "cuenta": VTURB_CUENTA}
    s = s.replace(bloque_video_viejo, bloque_video_nuevo)
    assert 'class="video-bar"' not in s and 'vsl-ph' not in s.split('</style>')[1]

    # CSS del video: el contenedor nuevo y fuera lo que ya no existe
    s = reemplazar(s,
        ".video-frame{position:relative;width:100%;padding-top:56.25%}",
        ".video-vturb{position:relative;width:100%}\n"
        ".video-vturb vturb-smartplayer{position:relative;z-index:1}",
        "css video-frame")
    s = reemplazar(s,
        ".corner{position:absolute;width:18px;height:18px;border:2px solid var(--nfm-orange);opacity:.75;z-index:3}",
        ".corner{position:absolute;width:18px;height:18px;border:2px solid var(--nfm-orange);opacity:.75;z-index:3;pointer-events:none}",
        "css corner")
    for sel in (".vsl-ph", ".video-bar", ".fs-btn", ".hero h1 .word", ".hero h1 .ltr", ".hero h1.lit"):
        s = re.sub(r"^" + re.escape(sel) + r"[^\n]*\n", "", s, flags=re.M)
    s = reemplazar(s, "  .hero h1 .ltr{opacity:1;transform:none;filter:none}\n", "", "css ltr reduced-motion")

    # JS del video viejo: CONFIG, funciones y arranque
    s = cortar(s,
        "  // Video VSL. Pegá la URL de EMBED",
        "hide_title=true\",\n",
        "config VIDEO_EMBED_URL")
    s = reemplazar(s,
        "  // Base de datos (mismo endpoint que la landing madre para unificar leads).",
        "  // Etiqueta de esta version: viaja al survey como utm_content para saber\n"
        "  // que VSL genero cada lead.\n"
        "  VERSION: \"vsl-%s\",\n\n"
        "  // Base de datos (mismo endpoint que la landing madre para unificar leads)." % version.lower(),
        "config VERSION")
    s = cortar(s,
        "/* ---------- Testimonios / casos (click-to-play YouTube) ---------- */",
        "/* ---------- UTM / Sheets ---------- */",
        "js video viejo", incluir_hasta=False)
    s = reemplazar(s,
        "window.addEventListener('DOMContentLoaded',()=>{ initVSL(); fillPhotos(); });",
        "window.addEventListener('DOMContentLoaded',()=>{ fillPhotos(); });",
        "init")
    s = reemplazar(s,
        "  var full=url+sep+'utm_source='+encodeURIComponent(getUTM());",
        "  var full=url+sep+'utm_source='+encodeURIComponent(getUTM())+'&utm_content='+encodeURIComponent(CONFIG.VERSION||'');",
        "survey utm_content")

    # el titulo letra por letra: en celular retrasaba la lectura del titular
    s = cortar(s,
        '  /* ----- Título del hero letra por letra',
        '}catch(err){ if(window.console) console.warn("hero type:", err); }\n',
        "js letra por letra")
    assert "heroTitle" in s   # el h1 sigue ahi, sin animacion

    # ═══════════════════════════════════════════ 2) TITULAR (si ya se eligio)
    if TITULO:
        s = reemplazar(s,
            'No te falta información. Te falta un método que trabaje <span class="shimmer">a favor de tu cerebro</span>.',
            TITULO, "titular")
    if SUB:
        s = reemplazar(s,
            'En el <b>Instituto de Productividad</b> no sumamos más apps, más cursos ni más fuerza de voluntad. Entendemos cómo funciona tu cerebro y armamos un sistema a tu medida —para que rendir deje de ser pelearte con vos mismo. <b>Neurociencia aplicada, no más disciplina.</b>',
            SUB, "subtitulo")

    s = reemplazar(s,
        '<title>Instituto de Productividad · Mirá el video y aplicá</title>',
        '<title>' + TITLE_TAG + '</title>', "title")
    s = reemplazar(s,
        '<meta name="description" content="No te falta información: te falta un método que trabaje a favor de tu cerebro. La razón neurológica por la que tu cerebro cumple con todo el mundo y deja tus objetivos para después — y qué hace el Instituto de Productividad para cambiarlo. Aplicá a tu entrevista de admisión.">',
        '<meta name="description" content="' + META_DESC + '">', "meta description")

    # ═══════════════════════════════════════════ 3) EL CAMINO (reemplaza al espejo) + HISTORIA DE NICO
    # El espejo ("Seamos honestos") queda absorbido por el Punto A: la persona se
    # identifica una sola vez, y de ahi sale directo al mecanismo.
    i = s.index("<!-- ESPEJO · Seamos honestos (secretos en la ducha) -->\n")
    j = s.index("</section>\n", i) + len("</section>\n")
    s = s[:i] + CAMINO.rstrip() + "\n" + s[j:]
    for sel in (".ducha", ".think", ".ducha-close", "@media(max-width:640px){.ducha", "/* ---------- ESPEJO"):
        s = re.sub(r"^" + re.escape(sel) + r"[^\n]*\n", "", s, flags=re.M)
    assert ".ducha" not in s and "Seamos honestos" not in s.split("<!-- FOOTER -->")[0]

    s = reemplazar(s,
        "<!-- AVAL UNIVERSITARIO (3er widget · el diferencial arriba) -->",
        HISTORIA.rstrip() + "\n\n<!-- AVAL UNIVERSITARIO (3er widget · el diferencial arriba) -->",
        "historia")

    # ═══════════════════════════════════════════ 4) LIMPIEZA DE COPY
    # Aval: cuatro capas de titulo diciendo lo mismo → quedan dos
    s = reemplazar(s,
        '    <p class="lead-2 center" style="max-width:62ch;margin-left:auto;margin-right:auto">Antes de contarte nada más: esto es lo que separa al Instituto de "un curso más".</p>\n',
        "", "aval lead")
    s = reemplazar(s,
        '        <span class="feat-badge">★ El diferencial · Respaldo académico</span>\n',
        "", "aval badge")
    s = reemplazar(s,
        'No es una constancia por asistir. La versión <b>Platinum</b> se certifica de forma conjunta con la <b>Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy (UNJu)</b>: un trayecto de 250 horas con evaluación y un trabajo final aplicado a tu propia vida o negocio. Se gana, no se regala — y por eso pesa distinto en tu CV, tu LinkedIn y frente a quien sea.',
        'No es una constancia por asistir. La versión <b>Platinum</b> se certifica junto con la <b>Facultad de Ciencias Económicas de la Universidad Nacional de Jujuy (UNJu)</b>. Se gana, no se regala, y por eso pesa distinto en tu CV y frente a quien sea.',
        "aval lead card")
    s = reemplazar(s,
        '<li>Trayecto de 250 horas certificado por la Facultad, con evaluación y trabajo final</li>',
        '<li>250 horas con evaluación y un trabajo final aplicado a tu propia vida o negocio</li>',
        "aval li")

    # La razon real / Para quien / Que incluye: fuera enteras. El camino (Punto A → B →
    # escalera → como accedes) cuenta lo mismo una sola vez y de manera visual.
    s = cortar(s, "<!-- QUÉ ES / PARA QUIÉN -->\n", "</section>\n", "seccion que es")
    s = cortar(s, "<!-- QUÉ INCLUYE -->\n", "</section>\n", "seccion incluye")
    for sel in (".split", ".forwho", ".fw", ".bcard", ".incl-grid", ".ic", ".incl-note",
                ".photo-slot--sm", '[data-img="coach"]', "@media(max-width:640px){.incl-grid--duo"):
        # borra la regla de esa clase y sus derivadas (.bcard, .bcards, .bcard__ph...) pero no .icons ni .fwd
        s = re.sub(r"^" + re.escape(sel) + r"(?:s|__[a-z-]+|--[a-z-]+)?(?=[\s{:.,\[])[^\n]*\n", "", s, flags=re.M)
    for linea in ("  .incl-grid{grid-template-columns:repeat(2,1fr)}\n", "  .bcards{grid-template-columns:repeat(2,1fr)}\n",
                  "  .split{grid-template-columns:1fr;gap:32px}\n", "  .incl-grid{grid-template-columns:1fr}\n",
                  "  .bcards{grid-template-columns:1fr;max-width:420px;margin-left:auto;margin-right:auto}\n"):
        s = reemplazar(s, linea, "", "css responsive " + linea.strip()[:24])
    s = reemplazar(s, '      <a href="#incluye">Qué incluye</a>\n', "", "footer link incluye")
    s = reemplazar(s, '      <a href="#espejo">Seamos honestos</a>\n', '      <a href="#camino">El camino</a>\n', "footer link espejo")

    # Fotos: las cuatro de "que incluye" ya no se usan; entran las del camino (una por lugar)
    s = cortar(s, "  // Recuadro 5 · Comunidad (foto grupal)\n", "  // Recuadro 1 · Aval", "img viejas", incluir_hasta=False)
    s = reemplazar(s,
        "/* ===== FOTOS REALES DE LOS RECUADROS =====\n   Subí cada foto a tu WordPress (Medios) y pegá el link https entre comillas.\n   Podés poner VARIAS por recuadro y se arma un collage solo (hasta 4). */\n",
        "/* ===== FOTOS REALES =====\n   Subí cada foto a la biblioteca de medios y pegá el link https entre comillas.\n"
        "   Las del camino están en la carpeta vsl-assets (sacadas del deck de Nico): un link por lugar.\n"
        "   El aval admite VARIAS y arma un collage solo (hasta 4). */\n",
        "img comentario")
    s = reemplazar(s,
        '    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275ecb6db2520210e7a.jpg"\n  ],\n};\n',
        '    "https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6a6b6275ecb6db2520210e7a.jpg"\n  ],\n\n'
        "  // ── El camino (un link por lugar) ──\n"
        '  camino_a:   "vsl-assets/a-podio.jpg",                 // Punto A · Mini Nico en el podio, agotado\n'
        '  camino_b:   "vsl-assets/b-arriba-de-la-pared.jpg",    // Punto B · Mini Nico arriba de la pared, con el mate\n'
        '  escalera_1: "vsl-assets/escalera-1-parales.jpg",      // 01 · los dos parales (Mente y Cuerpo)\n'
        '  escalera_2: "vsl-assets/escalera-2-peldano.jpg",      // 02 · el peldaño (Competencias)\n'
        '  escalera_3: "vsl-assets/escalera-3-completa.jpg",     // 03 · la escalera completa, tocando la X\n'
        '  // (las 4 fotos de los pilares siguen en la carpeta, con nombre acceso-*.jpg, por si vuelven)\n'
        "};\n",
        "img camino")

    # Metodo y equipo: leads mas cortos, sin re-explicar el titulo
    s = reemplazar(s,
        '<p class="lead-2">Acá tenés <b>un profesional por cada frente</b>: coach dedicada, psicólogos, nutricionistas y coaches de alto rendimiento. No es Nico solo: es un equipo que te ve, te sigue y no te deja aflojar. Con nombre y cara, incluso quien te va a atender en la primera charla.</p>',
        '<p class="lead-2">No es Nico solo. Un profesional por cada frente, <b>con nombre y cara</b>.</p>',
        "equipo lead")

    # Casos: menos palabras, y las 14 entrevistas quedan a un toque en vez de estirar la pagina
    s = reemplazar(s,
        'Respondé 3 preguntas rápidas y te muestro tres alumnos que se parecen a vos — mismo perfil, mismo dolor, mismo punto donde estás hoy. Y si preferís, más abajo están <b>todas</b> las entrevistas completas.',
        'Respondé 3 preguntas y te muestro tres alumnos que arrancaron donde estás vos. Si preferís, abajo están <b>todas</b> las entrevistas.',
        "casos sub")
    s = reemplazar(s,
        '<p>Sus historias coinciden con tu perfil y el patrón que más te resuena. Mirá los videos para ver cómo lo transformaron.</p>',
        '<p>Mirá cómo lo resolvieron.</p>',
        "casos result p")
    s = reemplazar(s,
        '<p>Sin recortes ni selección: todas las entrevistas, con nombre, cara y oficio. Elegí la que quieras.</p>\n      </div>\n      <div class="nfm-cases__grid nfm-cases__grid--all" id="nfm-cases-allgrid"></div>',
        '<p>Sin recortes: todas las entrevistas, con nombre, cara y oficio.</p>\n        <button type="button" class="nfm-cases__btn nfm-cases__btn--ghost" id="nfm-cases-vertodos" onclick="nfmCasesVerTodos()">Ver todas las entrevistas</button>\n      </div>\n      <div class="nfm-cases__grid nfm-cases__grid--all" id="nfm-cases-allgrid"></div>',
        "casos ver todos")
    s = reemplazar(s,
        "  .nfm-cases__grid--all { margin-bottom: 0; }",
        "  .nfm-cases__grid--all { margin-bottom: 0; }\n"
        "  /* las 14 entrevistas arrancan plegadas: en celular estiraban la pagina 6000px antes del cierre */\n"
        "  .nfm-cases__all:not(.is-open) .nfm-cases__grid--all { display: none; }\n"
        "  .nfm-cases__btn--ghost { background: transparent; color: var(--navy); border: 1.5px solid rgba(12, 52, 82, 0.28); box-shadow: none; margin-top: 4px; }\n"
        "  .nfm-cases__btn--ghost:hover:not(:disabled) { background: rgba(12, 52, 82, 0.05); box-shadow: none; }\n"
        "  .nfm-cases__btn { min-height: 46px; }",
        "casos css plegado")
    s = reemplazar(s,
        "  function renderAll(){\n    var grid=document.getElementById('nfm-cases-allgrid');\n    if(grid) grid.innerHTML = casos.map(cardHTML).join('');\n  }",
        "  function renderAll(){\n    var grid=document.getElementById('nfm-cases-allgrid');\n    if(grid) grid.innerHTML = casos.map(cardHTML).join('');\n"
        "    var b=document.getElementById('nfm-cases-vertodos');\n    if(b) b.textContent='Ver las '+casos.length+' entrevistas';\n  }\n"
        "  window.nfmCasesVerTodos = function(){\n    var all=document.querySelector('.nfm-cases__all'); if(!all) return;\n"
        "    all.classList.add('is-open');\n    var b=document.getElementById('nfm-cases-vertodos'); if(b) b.style.display='none';\n  };",
        "casos js ver todos")

    # Cierre: el segundo parrafo era relleno que repetia el hero
    s = reemplazar(s,
        '<p>Si no hacés algo distinto, en uno, dos o tres años vas a seguir en el mismo lugar. Y eso se traduce en concreto: <b>potencial que sabés que podés dar y no estás dando</b>, oportunidades que pasan de largo, calidad de vida, ingresos, tiempo con tu familia, tu salud.</p><p>Todos pasamos por un punto de quiebre. <b>No tenemos por qué pasarlo solos.</b> Para eso está el Instituto de Productividad: para acompañarte en el proceso, con evidencia de cómo funciona tu cerebro y un método basado en neurociencia.</p>',
        '<p>Si no hacés algo distinto, en uno, dos o tres años vas a estar en el mismo lugar. Y eso tiene un precio concreto: <b>potencial que sabés que tenés y no estás dando</b>, oportunidades que pasan de largo, tiempo con tu familia, tu salud.</p>',
        "cierre")

    # ═══════════════════════════════════════════ 4b) FUERA EL EQUIPO
    # En una VSL para trafico frio es un bloque mas entre el video y el boton;
    # el equipo vive en la thank you page, que es donde importa quien te atiende.
    s = cortar(s,
        '<!-- ============================================================\n     EQUIPO QUE TE ACOMPAÑA (6 miembros) — widget integrado',
        '</section>\n', "seccion equipo")
    s = reemplazar(s, '      <a href="#nfm-equipo">Equipo</a>\n', '', "footer link equipo")
    s = re.sub(r"^\s*\.nfm-team[^\n]*\n", "", s, flags=re.M)
    s = re.sub(r"^/\* ---------- EQUIPO \(widget integrado\) ---------- \*/\n", "", s, flags=re.M)
    s = re.sub(r"^/\* \.nfm-team hereda[^\n]*\n", "", s, flags=re.M)

    # ═══════════════════════════════════════════ 4c) FUERA EL METODO
    # Los 5 pilares explicaban que areas toca el sistema, algo que la VSL ya
    # cuenta; era el bloque que menos empujaba hacia el boton.
    s = cortar(s, '<!-- ENFOQUE INTEGRAL / PILARES -->\n', '</section>\n', "seccion metodo")
    s = cortar(s, '/* ---------- ENFOQUE INTEGRAL / PILARES ---------- */\n',
                  '.pill p{font-size:13px;color:var(--muted);line-height:1.5}\n', "css pilares")

    # Un solo numero de alumnos en toda la pagina: el mismo que respalda la escalera
    s = reemplazar(s,
        '<div class="stat"><div class="n">+2.000</div><div class="l">Alumnos acompañados</div></div>',
        '<div class="stat"><div class="n">+800</div><div class="l">Alumnos acompañados</div></div>',
        "trust +800")

    # ═══════════════════════════════════════════ 4c-ter) FUERA EL H1: EL TITULO VA EN EL VIDEO DE VTURB
    # Nico lo agrega como overlay del propio video; en la landing repetirlo era ruido.
    s = reemplazar(s,
        '    <h1 id="heroTitle" style="max-width:24ch;margin-left:auto;margin-right:auto">' + TITULO + '</h1>\n',
        "", "hero h1")
    s = re.sub(r"^\.hero h1(?=[\s{.])[^\n]*\n", "", s, flags=re.M)

    # ═══════════════════════════════════════════ 4c-bis) FUERA EL CIERRE DE LA PAGINA
    # Repetia la pregunta del camino con otras palabras. El unico CTA de cierre
    # queda el del camino, y el link del pie pasa a abrir el panel.
    s = cortar(s, "<!-- CTA FINAL / AGENDAR -->\n", "</section>\n", "seccion cierre")
    s = reemplazar(s, '      <a href="#agendar">Agendar entrevista</a>\n',
        '      <a href="#" onclick="agdOpen(\'pie\');return false">Agendar entrevista</a>\n', "footer link agendar")
    s = re.sub(r"^\.apply(?=[\s{:.])[^\n]*\n", "", s, flags=re.M)
    s = re.sub(r"^\.section--navy\.apply[^\n]*\n", "", s, flags=re.M)
    s = reemplazar(s, "  .apply .btn-lg,.nfm-cases__btn{width:100%;max-width:340px}\n",
        "  .nfm-cases__btn{width:100%;max-width:340px}\n", "css celular apply")
    s = reemplazar(s, ".section--navy .h2,.section--navy.apply h2{color:#fff}\n",
        ".section--navy .h2{color:#fff}\n", "css navy h2")
    s = reemplazar(s, ".section--navy .h2 .hl,.section--navy.apply h2 .hl{color:var(--nfm-orange)}\n",
        ".section--navy .h2 .hl{color:var(--nfm-orange)}\n", "css navy hl")

    # ═══════════════════════════════════════════ 4d) MENOS RUIDO ARRIBA
    # Fuera la cinta que gira (marquee) y la pildora del hero: el titulo y el video
    # ya dicen que es. Los rotulos de seccion quedan como texto mono plano, sin pildora.
    s = cortar(s, '    <div class="marquee fade-up d5" aria-hidden="true">\n', "      </div>\n    </div>\n", "marquee html")
    for sel in (".marquee", ".mq-item", "@keyframes marq", "/* ---------- MARQUEE ---------- */"):
        s = re.sub(r"^" + re.escape(sel) + r"[^\n]*\n", "", s, flags=re.M)
    s = reemplazar(s, '    <span class="eyebrow fade-up d1">Alto rendimiento con base en neurociencia</span>\n', "", "hero eyebrow")
    s = re.sub(r"^\.eyebrow\{[^\n]*\n",
        ".eyebrow{display:inline-block;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.22em;"
        "font-size:11px;font-weight:500;color:var(--nfm-orange-text);margin-bottom:16px}\n", s, flags=re.M)
    s = re.sub(r"^\.eyebrow\.on-blue\{[^\n]*\n", ".eyebrow.on-blue{color:#ffd0ac}\n", s, flags=re.M)
    s = re.sub(r"^\.section--navy \.eyebrow\{[^\n]*\n", ".section--navy .eyebrow{color:#ffd0ac}\n", s, flags=re.M)
    assert 'class="marquee' not in s and ".marquee" not in s and "mq-item" not in s
    assert "border-radius:100px" not in re.search(r"^\.eyebrow\{[^\n]*", s, flags=re.M).group(0)

    # ═══════════════════════════════════════════ 5) CELULAR
    s = reemplazar(s,
        "  .topbar__cta .lbl-full{display:none}\n  .topbar__cta .lbl-short{display:inline}\n}",
        "  .topbar__cta .lbl-full{display:none}\n  .topbar__cta .lbl-short{display:inline}\n"
        "  .btn-sm{min-height:44px;padding:12px 18px}   /* el boton fijo de arriba media 37px */\n"
        "  .feat-legal{font-size:12px}\n}",
        "css celular")
    # el boton de rehacer el test media 35px
    s = reemplazar(s,
        "  .nfm-cases__retake {\n    background: transparent;",
        "  .nfm-cases__retake {\n    min-height: 44px;\n    background: transparent;",
        "retake 44px")

    # ═══════════════════════════════════════════ 6) ROTULO
    s = reemplazar(s,
        "   LANDING · INSTITUTO DE PRODUCTIVIDAD\n",
        "   LANDING · INSTITUTO DE PRODUCTIVIDAD · VSL · VERSIÓN %s\n"
        "   (generada por .claude/build_vsl.py — la A y la B solo cambian el video)\n" % version,
        "rotulo")

    # controles finales
    for prohibido in ("loadVSL", "initVSL", "goFullscreen", "VIDEO_EMBED_URL", "loom.com", "nfm-adm", "Valent", "nfm-team", "nfm-equipo", 'id="metodo"', ".pillars", ".pill{",
                      'id="espejo"', 'id="quees"', 'id="incluye"', 'id="agendar"', 'class="marquee', ".bcard", ".ducha",
                      "urgencia prestada", "Recuadro 2", "Cuatro pilares", "nfmc-pilar", ".apply{", "section apply", "agendarBtn",
                      'id="heroTitle"', ".hero h1{"):
        assert prohibido not in s, "quedo " + prohibido
    assert s.count(vturb_id) == 2, "el ID de vturb tiene que aparecer exactamente 2 veces"
    assert s.count('id="camino"') == 1 and s.count("data-foto=") == 5 and s.count("vsl-assets/") == 5
    assert "+2.000" not in s and s.count("+800") == 1 and s.count("más de 800 personas") == 1
    assert s.index('id="camino"') < s.index('id="historia-nico"') < s.index('id="aval"') < s.index('id="nfm-casos"')
    return s


if __name__ == "__main__":
    for fname, ver, vid in VERSIONES:
        html = construir(ver, vid)
        io.open(os.path.join(BASE, fname), "w", encoding="utf-8").write(html)
        print("%-24s version %s · vturb %s · %d bytes" % (fname, ver, vid, len(html)))
