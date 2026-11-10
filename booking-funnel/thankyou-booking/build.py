# -*- coding: utf-8 -*-
"""Thank you page del booking funnel (después de agendar en Calendly).

   Arriba quedan los dos bloques que ya funcionan en mba.nicolasfernandezmiranda.com/gracias-1:
     1) el asesor asignado (lee ?assigned_to= y ?invitee_first_name= que manda Calendly)
     2) el video obligatorio antes de la sesión (Wistia)
   Abajo van los bloques nuevos (secciones-nuevas.html):
     3) el fundador: la historia de Nico en 5 escenas, en carrusel
     4) personas que arrancaron donde estás vos: lista de casos (nombre, oficio, frase)
     5) qué incluye el proceso
     6) la escalera: en qué escalón estás
     7) cierre
   Salen fuera el equipo y el quiz de casos de la página vieja.

   Entra : base-gracias-1-ghl.html (el código del widget HTML de gracias-1, tal cual está en GHL)
           secciones-nuevas.html
   Sale  : thankyou-booking.html  → se pega entero en un widget HTML de GHL
   Correr desde esta carpeta:  python3 build.py
"""
import io

base = io.open('base-gracias-1-ghl.html', encoding='utf-8').read()
nuevas = io.open('secciones-nuevas.html', encoding='utf-8').read()

def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, f'{c}x :: {a[:80]}'
    return s.replace(a, b)

# ── nos quedamos con los bloques 1 (asesor) y 2 (video) ──
corte = base.index('<!-- ═══════════════════════════════════════════════════════\n     3) WIDGET — EQUIPO')
s = base[:corte]

s = rep(s, """     PÁGINA THANK YOU — NFM · Instituto de Productividad
     TODO EN UNO (pegar en un solo HTML Widget de Elementor)
     Orden: 1) Closer asignado  2) Video  3) Equipo  4) Casos""",
"""     PÁGINA THANK YOU · BOOKING FUNNEL — NFM · Instituto de Productividad
     TODO EN UNO (pegar en un solo widget HTML de GHL, con los bordes en 0)
     Orden: 1) Asesor asignado  2) Video  3) El fundador  4) Casos  5) Qué incluye  6) Escalera  7) Cierre""")

# ── asesores nuevos: Ayrton y Lucas. Sin foto todavía: sale la inicial en un círculo.
#    Cuando tengas la foto, pegá el link en foto: '' ──
rep_closers = """    matias: {
      nombre: 'Matías',
      role: 'Asesor · Instituto de Productividad',
      foto: 'https://nicolasfernandezmiranda.com/wp-content/uploads/2026/06/image.png',
      mensaje: 'Voy a estar en la sesión con vos para escucharte y ayudarte a encontrar el mejor camino. Nos vemos en breve 🙌'
    }
  };"""
s = rep(s, rep_closers, """    matias: {
      nombre: 'Matías',
      role: 'Asesor · Instituto de Productividad',
      foto: 'https://nicolasfernandezmiranda.com/wp-content/uploads/2026/06/image.png',
      mensaje: 'Voy a estar en la sesión con vos para escucharte y ayudarte a encontrar el mejor camino. Nos vemos en breve 🙌'
    },
    ayrton: {
      nombre: 'Ayrton',
      role: 'Asesor · Instituto de Productividad',
      foto: '',   // ⚠️ falta la foto: pegá acá el link
      mensaje: 'Voy a acompañarte en esta primera charla para entender tu caso y ver cuál es el próximo paso. ¡Te escribo pronto! 🙌'
    },
    lucas: {
      nombre: 'Lucas',
      role: 'Asesor · Instituto de Productividad',
      foto: '',   // ⚠️ falta la foto: pegá acá el link
      mensaje: 'Voy a estar en la sesión con vos para escucharte y ayudarte a encontrar el mejor camino. ¡Hablamos pronto! 👋'
    }
  };""")
s = rep(s, """    paula: 'Paula',
    matias: 'Matías'
  };""", """    paula: 'Paula',
    matias: 'Matías',
    ayrton: 'Ayrton',
    lucas: 'Lucas'
  };""")

# el título del video lee assigned_to sin decodificar dos veces: con el doble encoding de Calendly
# («Luciana%20Fernandez») no encontraba al asesor y quedaba «tu asesor»
s = rep(s, "const assigned = (params.get('assigned_to') || '').toLowerCase().trim();",
        "let assigned = params.get('assigned_to') || '';\n  try { if (/%[0-9A-Fa-f]{2}/.test(assigned)) assigned = decodeURIComponent(assigned); } catch (e) {}\n  assigned = assigned.toLowerCase().trim();")

# ── menos texto arriba ──
# video: fuera la bajada y el recuadro de abajo; queda el título y el video
i = s.index('      <p class="nfm-video__subtitle">'); j = s.index('</p>', i) + len('</p>\n')
s = s[:i] + s[j:]
i = s.index('    <!-- TIP -->'); fin = s.index('  </div>\n</section>', i)
s = s[:i] + s[fin:]
s = rep(s, 'Paso obligatorio · Antes de tu sesión', 'Antes de tu sesión')
# asesor: una línea abajo del título y fuera el recuadro de "Revisá tu WhatsApp"
s = rep(s, "'Ya enviamos un mensaje a tu número para coordinar todo. Conocé a la persona que va a acompañarte en este proceso:'", "'Ya te escribimos para coordinar el horario.'")
s = rep(s, "'En las próximas horas, un asesor del Instituto se va a comunicar con vos por WhatsApp para coordinar todo y conocer tu caso en detalle.'", "'Te escribe por WhatsApp en las próximas horas.'")
s = rep(s, """        Ya enviamos un mensaje a tu número para coordinar todo. Conocé a la persona que va a acompañarte en este proceso:""", """        Ya te escribimos para coordinar el horario.""")
i = s.index('      <div class="nfm-closer__instruction">'); fin = s.index('      <div class="nfm-closer__extra">', i)
s = s[:i] + s[fin:]

out = s.rstrip() + '\n\n\n' + nuevas
io.open('thankyou-booking.html', 'w', encoding='utf-8').write(out)
print('ok thankyou-booking.html', len(out) // 1024, 'KB')
