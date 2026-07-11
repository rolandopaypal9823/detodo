# -*- coding: utf-8 -*-
"""Genera el sitio del Reto de 7 Días (voz NFM, marca Instituto de Productividad).

Uso:  python3 build_sitio.py
Salida: sitio/index.html + sitio/dia1..dia7/index.html
Netlify: arrastrar la carpeta `sitio` al deploy. Cada día queda en /dia1 ... /dia7.
"""
import os
from string import Template

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitio")

IG = "@nicofernandezmiranda"
LINK_PRODUCTO = "#LINK-PRODUCTO"  # TODO: reemplazar por el link real del producto

COMMUNITY = (
    "No estás haciendo esto solo: el reto está abierto todo el año y <strong>cada semana arranca "
    "gente nueva</strong>. Subí tu avance a historias y etiquetá a <strong>" + IG + "</strong> "
    "— me gusta ver quién está del otro lado."
)

DAYS = [
    {
        "n": 1,
        "emoji": "🧠",
        "title": "El número que casi nadie se anima a mirar",
        "subtitle": "Hoy no cambiás nada. Solo medís. Y medir ya es intervenir.",
        "brain_title": "El sesgo de anclaje",
        "brain": [
            "El tiempo que <strong>creés</strong> que pasás en el celular casi nunca coincide con el real. Un caso real: un chico juraba usar el celular 90 minutos por día. La medición mostró <strong>4 horas 20 minutos</strong>. Y solo ver el dato —sin sermones de nadie— hizo que él mismo pidiera cortar antes.",
            "¿Por qué funciona? La autoobservación activa tu <strong>corteza prefrontal</strong> (la parte que planifica y decide) y le baja el volumen a la reacción automática. Como un médico: primero el análisis, después el tratamiento.",
        ],
        "steps": [
            ("Abrí tu medidor de tiempo", "Tiempo en Pantalla (iPhone) o Bienestar Digital (Android)."),
            ("Anotá los minutos totales de ayer", "Y tus 3 apps más usadas."),
            ("Anotá tu sueño y tu energía", "A qué hora te dormiste anoche y con cuánta energía amaneciste, del 1 al 10."),
            ("No cambies nada hoy", "En serio. Ese número es tu punto A: el día 7 lo vas a comparar."),
        ],
        "planb": "¿Día complicado? Anotá solo el número total. Con eso alcanza.",
        "familia": "Cada uno mira su propio número y lo comparte. Regla de oro: cero juicio. Hoy son solo datos.",
        "cta_line": "Esto de hoy es una herramienta de la caja. Si querés integrar más herramientas y entender de verdad cómo funciona tu cerebro para rendir mejor en cada área de tu vida:",
        "teaser": "Mañana escribís tus propias reglas del juego (y justo por eso se van a cumplir).",
    },
    {
        "n": 2,
        "emoji": "📝",
        "title": "Reglas que sí se cumplen",
        "subtitle": "Las «dietas de pantalla» duran 3 días porque las reglas las escribe otro. Hoy las escribís vos.",
        "brain_title": "Autonomía e identidad",
        "brain": [
            "Cuando la regla la elegís vos, tu cerebro la procesa como <strong>autonomía</strong> y el compromiso sube. Cuando te la imponen, la procesa como amenaza y busca la trampa. Eso dice la teoría de la autodeterminación.",
            "Y el nivel dos, donde está lo copado: los hábitos que duran no salen de «voy a tratar de usar menos el celular». Salen de un cambio de <strong>identidad</strong>: «soy una persona que cuida su foco». Primero la identidad, después las acciones.",
        ],
        "steps": [
            ("Escribí 3 reglas propias, en positivo", "Ejemplos: comidas sin pantallas · el celular carga fuera de la habitación desde las 21:00 · primero mi prioridad del día, después las redes."),
            ("Pegalas donde las veas", "En papel y a la vista: heladera, escritorio, espejo."),
            ("Declaralo experimento", "Son 7 días, no una condena. Lo que no funcione se ajusta el día 7."),
        ],
        "planb": "Una sola regla: comidas sin pantallas. Es la que más cambia el ambiente.",
        "familia": "Cada uno propone reglas —los chicos también, sobre todo los chicos—. Consensúen 5, fírmenlo como contrato y péguenlo en la heladera. Cuando ellos proponen, cumplen.",
        "cta_line": "Autonomía, identidad, hábitos: todo esto tiene una lógica hermosa dentro de tu cabeza. Si querés el mapa completo de cómo funciona tu cerebro:",
        "teaser": "Mañana: 15 minutos de configuración que valen toda la semana.",
    },
    {
        "n": 3,
        "emoji": "🔕",
        "title": "El teléfono pasa a ser árbitro",
        "subtitle": "La forma más efectiva de cambiar un hábito no es la fuerza de voluntad: es cambiar el entorno.",
        "brain_title": "Batería mental y fatiga de decisión",
        "brain": [
            "Tu cerebro es como la <strong>batería del celular</strong>: aunque no estés usando ninguna app, las que quedan abiertas en segundo plano la consumen igual. Las notificaciones son exactamente eso: apps en segundo plano de tu atención.",
            "Cada «¿entro o no entro?» gasta batería mental — se llama <strong>fatiga de decisión</strong>. Por eso a la noche, ya sin nafta, caés en el scroll. Hoy no vas a resistir más fuerte: vas a sacar el freno de mano.",
        ],
        "steps": [
            ("Apagá las notificaciones no humanas", "Redes y noticias: off. Dejá solo las personas que te escriben directo. (Esto solo ya es el 80% del resultado.)"),
            ("Límite diario a tus 2 apps top", "45–60 minutos a las del día 1. Cuando salte el límite, el que dice «se acabó» es el teléfono, no vos."),
            ("«No molestar» de 22:00 a 7:00", "Automático, todos los días."),
            ("Escondé la tentación", "Las apps golosas, a la última pantalla y fuera de la vista."),
        ],
        "planb": "Solo el paso 1 (notificaciones). Es el 80% del resultado.",
        "familia": "Mismos pasos en los dispositivos de los chicos, más una estación de carga fuera de los dormitorios. La frase que funciona: «dejamos que el teléfono haga de árbitro, así no discutimos nosotros».",
        "cta_line": "¿Por qué una sola notificación te puede costar 20 minutos de foco? La respuesta completa —y qué hacer con ella— está acá:",
        "teaser": "Mañana: por qué Messi duerme 11 horas por día (y qué tiene que ver con tu celular).",
    },
    {
        "n": 4,
        "emoji": "😴",
        "title": "Dormir de verdad",
        "subtitle": "Messi duerme hasta 11 horas. Federer dormía 10. No es casualidad: es estrategia.",
        "brain_title": "Melatonina vs. cortisol",
        "brain": [
            "La luz de la pantalla suprime tu <strong>melatonina</strong> (la hormona que te duerme) y el contenido excitante sube tu <strong>cortisol</strong> (la hormona de alerta). Doble golpe: tardás más en dormirte y dormís peor.",
            "En el sueño profundo y el REM tu cerebro consolida lo que aprendiste y regula tus emociones. Dormir mal no te hace flojo al otro día: te deja el envase a media carga. La práctica <strong>más el descanso</strong> hacen al maestro.",
        ],
        "steps": [
            ("3 horas antes de dormir", "Última cafeína o bebida excitante."),
            ("2 horas antes", "Cena liviana y pantallas al mínimo."),
            ("1 hora antes: corte digital total", "El celular carga fuera de la habitación (tu regla del día 2 😉). Lectura tranquila o música suave."),
            ("En la cama: respiración 4-4-6", "Inhalás 4 segundos, sostenés 4, exhalás 6. Diez ciclos. Practicá acá abajo 👇"),
        ],
        "special": "breathing",
        "planb": "Solo el corte de la última hora más la respiración. Con eso la noche ya cambia.",
        "familia": "El corte digital es de todos: los chicos copian lo que ven, no lo que se les dice. Lectura compartida en el último rato = jugada perfecta.",
        "cta_line": "Sueño, memoria, emociones, energía: es todo un mismo sistema. Si querés entender cómo se conecta y cómo optimizarlo:",
        "teaser": "Mañana: eso que sentís cuando soltás el celular no es aburrimiento. Es otra cosa.",
    },
    {
        "n": 5,
        "emoji": "⚡",
        "title": "Eso que sentís no es aburrimiento",
        "subtitle": "Es craving. Tiene nombre, tiene explicación y es 100% reversible.",
        "brain_title": "Dopamina rápida vs. dopamina de logro",
        "brain": [
            "Tu sistema de dopamina se acostumbró a recompensas rápidas —scroll, likes, videos de 15 segundos— y ahora las recompensas lentas le saben a poco. Ese vacío raro al soltar el celular es <strong>craving</strong>, no aburrimiento.",
            "La salida no es sacar el estímulo y dejar el hueco: es <strong>reemplazar la recompensa</strong>. Crear, moverte, terminar algo con las manos. Y si el reemplazo es movimiento, tu cerebro genera BDNF: literalmente fertilizante para las neuronas. Se llama neuroplasticidad, y juega para vos.",
        ],
        "steps": [
            ("Armá tu menú anti-scroll", "5 actividades que te gusten de verdad y no tengan pantalla: cocinar algo rico, salir a caminar, dibujar, la guitarra, llamar a alguien que querés."),
            ("Dejalo a la vista", "Pegado en la heladera o de fondo de pantalla."),
            ("Usalo hoy: 20 minutos mínimo", "Cuando aparezca el impulso de scrollear, elegí una del menú. Los primeros 5 minutos cuestan; después el cerebro agarra ritmo."),
        ],
        "planb": "Una sola actividad, 10 minutos. Lo que importa es que el cerebro pruebe la otra recompensa.",
        "familia": "Armá la caja anti-aburrimiento: 8–12 actividades listas para usar, a la altura de los chicos. Y para salir de la pantalla, transición 5-3-1: aviso a los 5 minutos, elegir actividad a los 3, cierre amable al minuto final.",
        "cta_line": "Dopamina rápida versus dopamina de logro: este capítulo de tu cabeza explica mucho más que el scroll. Está completo acá:",
        "teaser": "Mañana no hay listas ni configuración. Mañana toca la mejor parte del reto.",
    },
    {
        "n": 6,
        "emoji": "☕",
        "title": "Dos horas en modo avión",
        "subtitle": "Vos, no el celular. Hoy toca la mejor parte del reto.",
        "brain_title": "Desprendimiento psicológico",
        "brain": [
            "Desconectarse de verdad no es tener el celular boca abajo «por las dudas»: es no tenerlo. Los rituales predecibles —mismo día, misma hora, misma actividad— le bajan la ansiedad al cerebro y generan <strong>expectativa positiva</strong>: ese «ya viene mi momento».",
            "Y hay algo más profundo: la conexión cara a cara activa circuitos de recompensa que ninguna app puede imitar. <strong>Ninguna.</strong>",
        ],
        "steps": [
            ("Elegí un bloque de 1 a 2 horas", "Hoy o mañana. Sábado a la tarde funciona bárbaro."),
            ("Elegí la actividad", "Cocinar algo especial, juego de mesa, caminata larga, un café con alguien que querés."),
            ("Celulares a la estación de carga", "Todos. El tuyo primero."),
            ("Al final, puntualo del 1 al 10", "¿Cuánto lo disfrutaste? Anotalo: ese dato vale oro para mañana."),
        ],
        "planb": "30 minutos con una persona (o con vos mismo) y cero pantallas. Cuenta igual.",
        "familia": "Pónganle nombre al ritual («los sábados sin cables»), asignen roles —quién cocina, quién elige la música— y al final voten qué hacen la semana que viene. La repetición lo convierte en tradición.",
        "cta_line": "¿Por qué la conexión humana recarga justo lo que el scroll gasta? La respuesta está acá:",
        "teaser": "Mañana: día 7. Tu punto A contra tu punto B. Y una sorpresa 🏆",
    },
    {
        "n": 7,
        "emoji": "🏆",
        "title": "El efecto compuesto",
        "subtitle": "1,01³⁶⁵ = 37,78. Un 1% de mejora por día es un 3.700% en un año. Esta semana hiciste bastante más que un 1%.",
        "brain_title": "Dopamina de logro",
        "brain": [
            "Comparar tu punto A con tu punto B activa la <strong>dopamina de logro</strong>: la que consolida hábitos. Celebrar con datos no es un mimo — es enseñarle al cerebro «esto vale la pena, repitámoslo».",
            "Esta semana no aprendiste «trucos para usar menos el celular». Aprendiste que cuando entendés cómo funciona tu cerebro, dejás de pelear contra vos y empezás a jugar a tu favor.",
        ],
        "steps": [
            ("Compará tus minutos: día 1 vs. hoy", "La meta de una primera semana es 20–30% menos. Cualquier baja cuenta."),
            ("Compará tu energía al despertar", "¿Subió respecto del lunes?"),
            ("Declará 2 herramientas permanentes", "¿El árbitro? ¿El 3-2-1? ¿El menú anti-scroll? Las que mejor te funcionaron, se quedan."),
            ("Ajustá 1 regla", "La que quedó poco realista. Esto es un sistema vivo, no un examen."),
        ],
        "special": "final",
        "planb": "¿No anotaste el día 1? No pasa nada: escribí cómo te sentís hoy comparado con la semana pasada. Eso también es un dato.",
        "familia": "Revisión juntos: celebren 2 logros concretos de cada uno y ajusten una regla en equipo. Sin sermones: solo «mirá lo que logramos».",
        "cta_line": "Si querés integrar aún más herramientas y conocer correctamente cómo funciona tu cerebro para rendir mejor en cada área de tu vida —tu foco, tus hábitos, tu descanso, tu energía, tu trabajo— el siguiente paso está acá:",
        "teaser": "",
    },
]

CSS = """
:root{--navy:#0c3452;--navy2:#123f63;--orange:#ff6602;--bg:#f4f7fa;--ink:#22384a;--muted:#5a7086;--card:#ffffff}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Open Sans',Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65}
h1,h2,h3,.kicker,.daynum{font-family:'Montserrat',Arial,sans-serif}
a{color:var(--orange)}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
/* ---------- header/hero ---------- */
.topbar{background:var(--navy);padding:14px 0}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px}
.topbar img{height:34px;display:block}
.topbar a.home{font-family:'Montserrat';font-weight:700;font-size:.72rem;letter-spacing:.14em;color:#bcd2e2;text-decoration:none;text-transform:uppercase}
.topbar a.home:hover{color:#fff}
.hero{background:linear-gradient(150deg,var(--navy) 0%,var(--navy2) 60%,#0e4a75 100%);color:#fff;padding:52px 0 84px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-90px;top:-90px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,102,2,.28),transparent 70%)}
.kicker{color:var(--orange);font-weight:700;font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;margin-bottom:14px;animation:fadeUp .7s ease both}
.daynum{font-size:4.4rem;font-weight:800;line-height:1;letter-spacing:-.02em;animation:fadeUp .7s .08s ease both}
.daynum .emoji{font-size:3rem;vertical-align:middle;margin-left:10px}
.hero h1{font-size:1.85rem;font-weight:800;margin:14px 0 10px;max-width:600px;animation:fadeUp .7s .16s ease both}
.hero p.sub{color:#c8d9e6;font-size:1.06rem;max-width:580px;animation:fadeUp .7s .24s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
/* ---------- progress ---------- */
.progress{margin-top:-34px;position:relative;z-index:2}
.progress .row{background:var(--card);border-radius:16px;box-shadow:0 10px 30px rgba(12,52,82,.14);padding:18px 22px;display:flex;align-items:center;justify-content:space-between;gap:6px}
.pstep{display:flex;flex-direction:column;align-items:center;gap:5px;text-decoration:none;flex:1}
.pstep .dot{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Montserrat';font-weight:700;font-size:.85rem;background:#e4ecf3;color:var(--muted);transition:transform .25s}
.pstep:hover .dot{transform:scale(1.12)}
.pstep.done .dot{background:var(--navy);color:#fff}
.pstep.now .dot{background:var(--orange);color:#fff;box-shadow:0 0 0 0 rgba(255,102,2,.5);animation:pulse 1.8s infinite}
.pstep span{font-size:.62rem;letter-spacing:.08em;color:var(--muted);text-transform:uppercase;font-weight:600}
.pstep.now span{color:var(--orange)}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(255,102,2,.45)}70%{box-shadow:0 0 0 12px rgba(255,102,2,0)}100%{box-shadow:0 0 0 0 rgba(255,102,2,0)}}
/* ---------- cards ---------- */
main{padding:36px 0 10px}
.card{background:var(--card);border-radius:16px;box-shadow:0 4px 18px rgba(12,52,82,.07);padding:28px;margin-bottom:22px;opacity:0;transform:translateY(24px);transition:opacity .6s ease,transform .6s ease}
.card.in{opacity:1;transform:none}
.label{display:flex;align-items:center;gap:8px;font-family:'Montserrat';font-weight:800;font-size:.76rem;letter-spacing:.18em;text-transform:uppercase;color:var(--orange);margin-bottom:12px}
.label::before{content:"▸";font-size:1rem}
.card h2{font-size:1.3rem;font-weight:800;color:var(--navy);margin-bottom:12px}
.card p{margin-bottom:12px;color:var(--ink)}
.card p:last-child{margin-bottom:0}
/* checklist */
.check{list-style:none}
.check li{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #edf2f6;cursor:pointer}
.check li:last-child{border-bottom:none}
.check input{display:none}
.check .box{flex:0 0 26px;height:26px;border-radius:8px;border:2px solid #c3d2de;margin-top:2px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:.85rem;transition:all .25s}
.check li.on .box{background:var(--orange);border-color:var(--orange);transform:scale(1.05)}
.check .t strong{display:block;font-family:'Montserrat';font-weight:700;color:var(--navy);font-size:1rem}
.check li.on .t strong{text-decoration:line-through;color:var(--muted)}
.check .t small{color:var(--muted);font-size:.9rem;line-height:1.5;display:block;margin-top:2px}
.done-banner{display:none;margin-top:16px;background:#fff3ea;border:1.5px solid var(--orange);color:#a34104;border-radius:12px;padding:14px 18px;font-weight:600;animation:fadeUp .5s ease both}
.done-banner.show{display:block}
/* duo cards */
.duo{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-bottom:22px}
@media(max-width:640px){.duo{grid-template-columns:1fr}}
.duo .card{margin-bottom:0}
.mini h3{font-family:'Montserrat';font-weight:800;font-size:.95rem;color:var(--navy);margin-bottom:8px}
.mini p{font-size:.95rem;color:var(--ink)}
/* community */
.community{background:#e8f0f7;border-left:4px solid var(--navy);border-radius:12px;padding:18px 22px;font-size:.95rem;margin-bottom:22px;opacity:0;transform:translateY(24px);transition:opacity .6s,transform .6s}
.community.in{opacity:1;transform:none}
/* cta */
.cta{background:linear-gradient(140deg,var(--navy),var(--navy2));color:#fff;text-align:center;padding:36px 28px}
.cta p{color:#d3e2ee;max-width:540px;margin:0 auto 20px}
.btn{display:inline-block;background:var(--orange);color:#fff;text-decoration:none;font-family:'Montserrat';font-weight:800;font-size:1rem;letter-spacing:.03em;padding:16px 34px;border-radius:50px;box-shadow:0 8px 22px rgba(255,102,2,.4);transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(255,102,2,.5)}
.cta small{display:block;margin-top:14px;color:#9db8cc;font-size:.8rem}
/* teaser */
.teaser{display:flex;align-items:center;gap:14px;background:var(--card);border:1.5px dashed #c3d2de}
.teaser .arrow{font-size:1.6rem;color:var(--orange);font-weight:800}
.teaser p{color:var(--muted);font-size:.98rem}
.teaser p strong{color:var(--navy)}
/* breathing widget */
.breath{text-align:center;padding:34px 28px}
.breath .circle{width:150px;height:150px;margin:22px auto;border-radius:50%;background:radial-gradient(circle at 34% 30%,#1a5b8f,var(--navy));display:flex;align-items:center;justify-content:center;color:#fff;font-family:'Montserrat';font-weight:700;transition:transform 4s ease-in-out;box-shadow:0 0 0 14px rgba(12,52,82,.08),0 0 0 28px rgba(12,52,82,.04)}
.breath .phase{font-size:1.05rem;color:var(--navy);font-weight:700;font-family:'Montserrat';min-height:1.6em}
.breath .cycles{color:var(--muted);font-size:.9rem;margin-top:6px}
.btn2{background:var(--navy);color:#fff;border:none;font-family:'Montserrat';font-weight:700;font-size:.95rem;padding:13px 30px;border-radius:50px;cursor:pointer;margin-top:16px;transition:background .2s}
.btn2:hover{background:var(--navy2)}
/* final (día 7) */
.congrats{background:linear-gradient(140deg,var(--orange),#ff8a3d);color:#fff;text-align:center;padding:38px 28px;position:relative;overflow:hidden}
.congrats h2{color:#fff;font-size:1.5rem;margin:8px 0 6px}
.congrats .medal{font-size:3rem}
.congrats p{color:#fff3ea}
.reflect textarea{width:100%;min-height:150px;border:2px solid #c3d2de;border-radius:12px;padding:16px;font-family:'Open Sans';font-size:1rem;color:var(--ink);resize:vertical;margin:6px 0 12px}
.reflect textarea:focus{outline:none;border-color:var(--orange)}
.share{background:#fff8f3;border:1.5px solid #ffd9bd;border-radius:12px;padding:16px 20px;font-size:.95rem;margin-top:8px}
.saved{display:none;color:#0a7a3d;font-weight:600;font-size:.9rem;margin-left:12px}
.saved.show{display:inline}
/* confetti */
.confetti{position:fixed;top:-14px;border-radius:3px;z-index:99;pointer-events:none;animation:fall linear forwards}
@keyframes fall{to{transform:translateY(105vh) rotate(720deg);opacity:.2}}
/* footer */
footer{background:var(--navy);color:#9db8cc;margin-top:44px;padding:34px 0;text-align:center;font-size:.85rem}
footer img{height:30px;margin-bottom:14px;opacity:.95}
footer .q{font-family:'Montserrat';font-weight:700;color:#fff;font-size:1rem;margin-bottom:6px}
/* index grid */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:26px 0}
@media(max-width:640px){.grid{grid-template-columns:1fr}}
.daycard{background:var(--card);border-radius:16px;box-shadow:0 4px 18px rgba(12,52,82,.07);padding:22px;text-decoration:none;color:var(--ink);display:block;transition:transform .2s,box-shadow .2s;opacity:0;transform:translateY(24px)}
.daycard.in{opacity:1;transform:none;transition:opacity .6s,transform .6s}
.daycard:hover{transform:translateY(-4px);box-shadow:0 12px 26px rgba(12,52,82,.14)}
.daycard .dn{font-family:'Montserrat';font-weight:800;color:var(--orange);font-size:.78rem;letter-spacing:.18em;text-transform:uppercase}
.daycard h3{font-family:'Montserrat';font-weight:800;color:var(--navy);font-size:1.05rem;margin:6px 0}
.daycard p{font-size:.9rem;color:var(--muted)}
@media(max-width:640px){.daynum{font-size:3.2rem}.hero h1{font-size:1.45rem}.pstep span{display:none}.card{padding:22px}}
"""

JS_COMMON = """
// reveal on scroll
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.card,.community,.daycard').forEach(function(el){io.observe(el)});
// checklist + localStorage
var KEY='reto7_dia'+(window.DIA||0);
var items=document.querySelectorAll('.check li');
if(items.length){
  var saved=[];try{saved=JSON.parse(localStorage.getItem(KEY)||'[]')}catch(e){}
  items.forEach(function(li,i){
    if(saved.indexOf(i)>-1){li.classList.add('on');li.querySelector('.box').textContent='✓'}
    li.addEventListener('click',function(){
      li.classList.toggle('on');
      li.querySelector('.box').textContent=li.classList.contains('on')?'✓':'';
      var on=[];items.forEach(function(x,j){if(x.classList.contains('on'))on.push(j)});
      try{localStorage.setItem(KEY,JSON.stringify(on))}catch(e){}
      check();
    });
  });
  function check(){
    var all=true;items.forEach(function(x){if(!x.classList.contains('on'))all=false});
    var b=document.getElementById('doneBanner');
    if(b){b.classList.toggle('show',all)}
  }
  check();
}
"""

JS_BREATH = """
// respiración 4-4-6
(function(){
  var btn=document.getElementById('bStart'),c=document.getElementById('bCircle'),
      ph=document.getElementById('bPhase'),cy=document.getElementById('bCycles'),
      running=false,cycle=0,timer=null;
  function phase(name,secs,scale){
    ph.textContent=name+' — '+secs+' segundos';
    c.style.transitionDuration=secs+'s';
    c.style.transform='scale('+scale+')';
  }
  function loop(){
    if(cycle>=10){ph.textContent='Listo. Así se le habla al cuerpo 💤';cy.textContent='10 ciclos completados';btn.textContent='Repetir';running=false;return}
    cycle++;cy.textContent='Ciclo '+cycle+' de 10';
    phase('Inhalá',4,1.35);
    timer=setTimeout(function(){
      phase('Sostené',4,1.35);
      timer=setTimeout(function(){
        phase('Exhalá',6,1);
        timer=setTimeout(loop,6000);
      },4000);
    },4000);
  }
  btn.addEventListener('click',function(){
    if(running){clearTimeout(timer);running=false;btn.textContent='Empezar';ph.textContent='';cy.textContent='';c.style.transform='scale(1)';cycle=0;return}
    running=true;cycle=0;btn.textContent='Parar';loop();
  });
})();
"""

JS_FINAL = """
// confetti
(function(){
  var colors=['#ff6602','#0c3452','#ffb37e','#4d84ab','#ffffff'];
  for(var i=0;i<90;i++){
    var d=document.createElement('div');d.className='confetti';
    d.style.left=Math.random()*100+'vw';
    d.style.width=(6+Math.random()*7)+'px';d.style.height=(8+Math.random()*10)+'px';
    d.style.background=colors[i%colors.length];
    d.style.animationDuration=(3.5+Math.random()*4)+'s';
    d.style.animationDelay=(Math.random()*2.5)+'s';
    document.body.appendChild(d);
    (function(el){setTimeout(function(){el.remove()},11000)})(d);
  }
})();
// reflexión con guardado local
(function(){
  var ta=document.getElementById('reflect'),ok=document.getElementById('savedTag');
  if(!ta)return;
  try{ta.value=localStorage.getItem('reto7_reflexion')||''}catch(e){}
  var t;ta.addEventListener('input',function(){
    clearTimeout(t);t=setTimeout(function(){
      try{localStorage.setItem('reto7_reflexion',ta.value)}catch(e){}
      ok.classList.add('show');setTimeout(function(){ok.classList.remove('show')},1600);
    },500);
  });
})();
"""

PAGE = Template("""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>$page_title</title>
<meta name="description" content="$description">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>$css</style>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <img src="$root/assets/logo-blanco.png" alt="NFM — Instituto de Productividad">
    <a class="home" href="$root/">Reto 7 Días · Detox Digital</a>
  </div>
</div>
$body
<footer>
  <div class="wrap">
    <img src="$root/assets/logo-blanco.png" alt="NFM">
    <div class="q">"No es motivación, es ciencia."</div>
    <div>Reto de 7 Días de Desintoxicación Digital · Nico Fernández Miranda · Instituto de Productividad</div>
  </div>
</footer>
<script>window.DIA=$dia;$js</script>
</body>
</html>
""")


def progress_html(current, root):
    out = ['<div class="progress"><div class="wrap"><div class="row">']
    for d in range(1, 8):
        cls = "now" if d == current else ("done" if d < current else "")
        out.append(
            '<a class="pstep %s" href="%s/dia%d/"><div class="dot">%s</div><span>Día %d</span></a>'
            % (cls, root, d, "✓" if d < current else str(d), d)
        )
    out.append("</div></div></div>")
    return "".join(out)


def steps_html(steps):
    lis = []
    for title, detail in steps:
        lis.append(
            '<li><div class="box"></div><div class="t"><strong>%s</strong><small>%s</small></div></li>'
            % (title, detail)
        )
    return '<ul class="check">%s</ul>' % "".join(lis)


def day_body(d, root):
    n = d["n"]
    parts = []
    parts.append(
        f'''<div class="hero"><div class="wrap">
  <div class="kicker">Reto de 7 días · Detox digital</div>
  <div class="daynum">Día {n}<span class="emoji">{d["emoji"]}</span></div>
  <h1>{d["title"]}</h1>
  <p class="sub">{d["subtitle"]}</p>
</div></div>'''
    )
    parts.append(progress_html(n, root))
    parts.append('<main><div class="wrap">')

    if d.get("special") == "final":
        parts.append(
            '''<div class="card congrats"><div class="medal">🏆</div>
<h2>FELICITACIONES</h2>
<p>Completaste el <strong>Reto de 7 Días de Desintoxicación Digital</strong>.<br>Siete días, siete herramientas. Eso ya es efecto compuesto.</p>
</div>'''
        )

    brain_ps = "".join("<p>%s</p>" % p for p in d["brain"])
    parts.append(
        f'''<div class="card"><div class="label">El dato del cerebro</div>
<h2>{d["brain_title"]}</h2>{brain_ps}</div>'''
    )

    parts.append(
        f'''<div class="card"><div class="label">Tu reto de hoy</div>
<h2>Tocá cada paso cuando lo completes</h2>
{steps_html(d["steps"])}
<div class="done-banner" id="doneBanner">🔥 Reto del día completado. Así se construye el 1% diario.</div>
</div>'''
    )

    if d.get("special") == "breathing":
        parts.append(
            '''<div class="card breath"><div class="label">Probalo ahora</div>
<h2>Respiración 4-4-6 guiada</h2>
<p>Seguí el círculo: se agranda cuando inhalás, se queda cuando sostenés, se achica cuando exhalás.</p>
<div class="circle" id="bCircle">4-4-6</div>
<div class="phase" id="bPhase"></div>
<div class="cycles" id="bCycles"></div>
<button class="btn2" id="bStart">Empezar</button>
</div>'''
        )

    if d.get("special") == "final":
        parts.append(
            f'''<div class="card reflect"><div class="label">Tu resultado en tus palabras</div>
<h2>Después de estos 7 días…</h2>
<p>¿Qué cambió? ¿Cómo te sentiste? ¿Qué lograste? Escribilo acá — lo que escribís queda guardado en tu dispositivo.</p>
<textarea id="reflect" placeholder="Ej.: bajé de 4 horas a 2:40 por día, me dormí antes toda la semana, y el sábado pasé una tarde entera sin mirar el celular…"></textarea>
<span class="saved" id="savedTag">✓ Guardado</span>
<div class="share">📸 <strong>Si te copa, sacale una captura a esto</strong> (o a tus números de Tiempo en Pantalla) y <strong>etiquetame en Instagram ({IG})</strong>. Me encantaría ver personalmente tus resultados, conocer a los que están terminando el reto esta semana, y ver si puedo ayudarte con algo más.</div>
</div>'''
        )

    parts.append(
        f'''<div class="duo">
<div class="card mini"><h3>🅱️ Plan B (día complicado)</h3><p>{d["planb"]}</p></div>
<div class="card mini"><h3>👨‍👩‍👧 Si lo hacés en familia</h3><p>{d["familia"]}</p></div>
</div>'''
    )

    parts.append(f'<div class="community">🧠 {COMMUNITY}</div>')

    parts.append(
        f'''<div class="card cta"><div class="label" style="justify-content:center">El siguiente nivel</div>
<p>{d["cta_line"]}</p>
<a class="btn" href="{LINK_PRODUCTO}">Quiero conocer mi cerebro →</a>
<small>Sin apuro: el reto ya es tuyo y las herramientas también.</small>
</div>'''
    )

    if d["teaser"]:
        parts.append(
            f'''<div class="card teaser"><div class="arrow">↗</div>
<p><strong>Mañana, Día {n + 1}:</strong> {d["teaser"]}</p></div>'''
        )

    parts.append("</div></main>")
    return "".join(parts)


def index_body(root):
    cards = []
    for d in DAYS:
        spoiler = d["subtitle"]
        cards.append(
            f'''<a class="daycard" href="{root}/dia{d["n"]}/">
<div class="dn">Día {d["n"]} {d["emoji"]}</div><h3>{d["title"]}</h3><p>{spoiler}</p></a>'''
        )
    return f'''<div class="hero"><div class="wrap">
  <div class="kicker">Bonus del e-book · Un mensaje por día</div>
  <div class="daynum" style="font-size:3rem">Reto de 7 Días 🧠</div>
  <h1>Desintoxicación digital, acompañado</h1>
  <p class="sub">Siete días, siete herramientas. Cada día: un dato de cómo funciona tu cerebro + un accionable de 10 a 20 minutos. No es motivación, es ciencia.</p>
</div></div>
<main style="margin-top:-34px;position:relative;z-index:2"><div class="wrap">
<div class="grid">{"".join(cards)}</div>
<div class="community">🧠 {COMMUNITY}</div>
</div></main>'''


def build():
    # días
    for d in DAYS:
        root = ".."
        html = PAGE.substitute(
            page_title=f"Día {d['n']} — {d['title']} · Reto 7 Días Detox Digital",
            description=d["subtitle"].replace('"', "'"),
            css=CSS,
            root=root,
            body=day_body(d, root),
            dia=d["n"],
            js=JS_COMMON
            + (JS_BREATH if d.get("special") == "breathing" else "")
            + (JS_FINAL if d.get("special") == "final" else ""),
        )
        out = os.path.join(BASE, f"dia{d['n']}")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
    # index
    html = PAGE.substitute(
        page_title="Reto de 7 Días — Detox Digital · NFM",
        description="Siete días, siete herramientas para desintoxicarte de las pantallas. No es motivación, es ciencia.",
        css=CSS,
        root=".",
        body=index_body("."),
        dia=0,
        js=JS_COMMON,
    )
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("OK — generado en", BASE)


if __name__ == "__main__":
    build()
