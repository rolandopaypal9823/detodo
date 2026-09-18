#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las dos versiones de la VSL landing del Instituto (A y B: mismo
cuerpo, distinto video de vturb) a partir de instituto-booking.html.

Ademas del video, aplica la limpieza de copy (sin conceptos repetidos ni
subtitulos de relleno), suma la historia de Nico y ajusta el celular.
"""
import io, os, re

BASE = "/home/user/detodo"
SCR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tsl-assets")
ORIGEN = os.path.join(BASE, "instituto-booking.html")
HISTORIA = io.open(os.path.join(SCR, "historia.html"), encoding="utf-8").read()

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

    # ═══════════════════════════════════════════ 3) HISTORIA DE NICO
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

    # La razon real: el segundo parrafo repetia el hero; queda la imagen del entrenador
    s = reemplazar(s,
        '<p class="lead-2">La salida no es más información —eso ya lo tenés—. Es entender cómo decide tu cerebro y darle la estructura que le falta: un sistema a tu medida y un equipo que sostiene el proceso con vos. Un entrenador no te enseña a hacer sentadillas: hace que el martes a las 7 estés entrenando. <b>Eso es el Instituto.</b></p>',
        '<p class="lead-2">Un entrenador no te enseña a hacer sentadillas: hace que el martes a las 7 estés entrenando. <b>Eso es el Instituto.</b></p>',
        "razon real p2")
    # Para quien: la tarjeta del medio repetia el parrafo de al lado
    s = reemplazar(s,
        '          <div class="fw"><span class="mono">◆ Es para vos si…</span><h3>Cumplís con todos, y tu proyecto no se mueve</h3><p>Sos impecable con los compromisos que tenés con otros, pero el objetivo que es tuyo lleva años en la misma lista. No te falta capacidad: te falta jerarquía.</p></div>\n',
        "", "para quien card 2")

    # Que incluye: lead de relleno y dos tarjetas que repetian al equipo y a los modulos
    s = reemplazar(s,
        '<p class="lead-2">Todo lo que ponemos del otro lado —dentro de nuestros procesos— para que esta vez tus objetivos sí avancen. Un profesional por cada frente, no un PDF y suerte.</p>',
        '<p class="lead-2">Un profesional por cada frente, no un PDF y suerte.</p>',
        "incluye lead")
    s = reemplazar(s,
        '<h3>Biblioteca de +20 módulos</h3>\n          <p>El método completo, ordenado y secuencial. Píldoras cortas y accionables, no teoría.</p>',
        '<h3>Biblioteca de +20 módulos y herramientas</h3>\n          <p>El método completo en píldoras cortas y accionables. Más el Habit Tracker y el Second Brain para sacarte la carga de la cabeza.</p>',
        "incluye card 02")
    s = cortar(s,
        '    <!-- Beneficios sin foto (se quedan como tarjetas de ícono) -->\n',
        '      <div class="ic"><span class="mk">06</span><div><h3>Método y sistemas listos para usar</h3><p>Biblioteca de módulos accionables + Habit Tracker y Second Brain para sacarte la carga de la cabeza. Copiás, adaptás, aplicás.</p></div></div>\n    </div>\n',
        "incluye ic cards")

    # Metodo y equipo: leads mas cortos, sin re-explicar el titulo
    s = reemplazar(s,
        'Service, aceite, gomas: rendir sostenido no es apretar más fuerte, es que todo el sistema funcione. Por eso el método toca las cinco áreas —no una técnica suelta.',
        'Service, aceite, gomas: no es apretar más fuerte, es que todo el sistema funcione. Por eso el método toca cinco áreas, no una técnica suelta.',
        "metodo lead")
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

    # ═══════════════════════════════════════════ 5) CELULAR
    s = reemplazar(s,
        "  .topbar__cta .lbl-full{display:none}\n  .topbar__cta .lbl-short{display:inline}\n}",
        "  .topbar__cta .lbl-full{display:none}\n  .topbar__cta .lbl-short{display:inline}\n"
        "  .btn-sm{min-height:44px;padding:12px 18px}   /* el boton fijo de arriba media 37px */\n"
        "  .feat-legal{font-size:12px}\n}",
        "css celular")
    # que incluye y equipo: en celular pasaban 2.000 y 3.400px apilados a una columna
    s = reemplazar(s,
        "  .bcards{grid-template-columns:1fr;max-width:420px;margin-left:auto;margin-right:auto}\n",
        "  /* que incluye: dos columnas */\n"
        "  .bcards{grid-template-columns:1fr 1fr;gap:12px}\n"
        "  .bcard__body{padding:12px 12px 14px}\n"
        "  .bcard__body h3{font-size:14px;margin:5px 0 5px}\n"
        "  .bcard__body p{font-size:12.5px}\n"
        "",
        "css celular columnas")
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
    for prohibido in ("loadVSL", "initVSL", "goFullscreen", "VIDEO_EMBED_URL", "loom.com", "nfm-adm", "Valent", "nfm-team", "nfm-equipo"):
        assert prohibido not in s, "quedo " + prohibido
    assert s.count(vturb_id) == 2, "el ID de vturb tiene que aparecer exactamente 2 veces"
    return s


if __name__ == "__main__":
    for fname, ver, vid in VERSIONES:
        html = construir(ver, vid)
        io.open(os.path.join(BASE, fname), "w", encoding="utf-8").write(html)
        print("%-24s version %s · vturb %s · %d bytes" % (fname, ver, vid, len(html)))
