# -*- coding: utf-8 -*-
"""Genera el portal de beneficios de la clase, una edición por clase.

   Clase del 7 de octubre · portal-beneficios/clase-7-oct/ → clase-beneficios.netlify.app
     /asiento-basic   → USD 1 · la clase (workbook + grabación)
     /premium-htc     → USD 5 · lo mismo + el ebook + el curso ABC
   Clase del 14 de octubre · un sitio por asiento (cada carpeta se sube sola):
     asiento-basic-14.netlify.app    → USD 1
     asiento-premium-14.netlify.app  → USD 5

   Las dos salen de la misma plantilla: cambia el contenido, no el esqueleto.
   Correr desde la raíz del repo:  python3 portal-beneficios/gen-portal.py
"""
import io, os

RAIZ = 'portal-beneficios'

# ══════════════════════════════════════════════════════════════════════════
#  CONFIG · lo único que hay que tocar cuando cambie algo
# ══════════════════════════════════════════════════════════════════════════
COMUN = {
  # Lo del asiento de USD 5
  'LIBRO_URL' : 'https://drive.google.com/file/d/1M2AGlaIzwFDei7b2NeBQmLqcf6LtA4PY/view?usp=sharing',
  'ABC_URL'   : 'https://abc-altorendimiento-nfm.netlify.app/',
  'LOGO'      : 'https://nicolasfernandezmiranda.com/wp-content/uploads/2026/01/nuevo-logo-nfm-1.png',
}
BASIC   = { 'titulo':'Asiento Premium Básico', 'eyebrow':'Asiento Premium Básico', 'premium':False }
PREMIUM = { 'titulo':'Asiento Premium · Hackea tu Productividad', 'eyebrow':'Asiento Premium · Hackea tu Productividad', 'premium':True }

# Por edición: el día, cuándo aparece lo de la clase (hora Argentina) y los links.
# Links vacíos = todavía no está: el portal dice «lo estamos subiendo», nunca un botón roto.
# GRABACION_LOOM = el código del video de Loom (lo que va después de /embed/): la grabación
# se ve adentro del portal. Si no hay Loom, GRABACION_URL es un link común.
EDICIONES = [
  { # clase del miércoles 7 · un sitio con dos rutas: clase-beneficios.netlify.app/asiento-basic y /premium-htc
    'carpeta'        : 'portal-beneficios/clase-7-oct',
    'un_sitio'       : True,
    'CLASE'          : '2026-10-07',
    'LISTO'          : '2026-10-07T21:00:00-03:00',
    'WORKBOOK_URL'   : 'https://drive.google.com/file/d/1b4-HRL0BZKePblPdMzSFNwBjEF4OGj4N/view?usp=sharing',
    'GRABACION_LOOM' : '323726c4dd324cb9af2d8eaffbb4b220',
    'GRABACION_URL'  : '',
    'paginas'        : { 'asiento-basic': BASIC, 'premium-htc': PREMIUM },
  },
  { # clase del miércoles 14 · un sitio por asiento
    'carpeta'        : 'portal-beneficios',
    'un_sitio'       : False,
    'CLASE'          : '2026-10-14',
    'LISTO'          : '2026-10-15T12:00:00-03:00',
    'WORKBOOK_URL'   : '',
    'GRABACION_LOOM' : '',
    'GRABACION_URL'  : '',
    'paginas'        : { 'asiento-basic-14': BASIC, 'asiento-premium-14': PREMIUM },
  },
]
CFG = {}   # la edición que se está generando (la llena main)
LOOM_PARAMS = 'hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true&hide_speed=true'

# ══════════════════════════════════════════════════════════════════════════
#  PLANTILLA
# ══════════════════════════════════════════════════════════════════════════
CSS = """
:root{
  --navy-deep:#081F33; --navy:#0C3452; --navy-1:#0E2E4A; --navy-2:#143A5C;
  --orange:#FF6602; --orange-hover:#FF8033; --orange-glow:rgba(255,102,2,.30); --green:#22C55E;
  --tl:rgba(255,255,255,.87); --tm:rgba(255,255,255,.62); --ts:rgba(255,255,255,.42); --hair:rgba(255,255,255,.09);
  --fh:'Space Grotesk',sans-serif; --fb:'DM Sans',sans-serif; --r:14px; --r-lg:22px;
  --ease:cubic-bezier(.22,1,.36,1);
}
*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; background:#081F33; }
body{ font-family:var(--fb); color:#fff; line-height:1.6; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; overflow-x:hidden;
  background:radial-gradient(800px 420px at 50% -5%, rgba(255,102,2,.14), transparent 62%), linear-gradient(180deg,#0C3452 0%,#081F33 38%,#081F33 100%); min-height:100vh; }
p{ margin:0; } img{ max-width:100%; height:auto; display:block; } a{ color:inherit; text-decoration:none; }
.wrap{ max-width:720px; margin:0 auto; padding:0 22px; }

.nav{ padding:18px 0; border-bottom:1px solid var(--hair); }
.nav .wrap{ display:flex; justify-content:center; }
.nav img{ height:64px; width:auto; }

.hero{ padding:46px 0 26px; text-align:center; }
.eyebrow{ display:inline-block; font-family:var(--fh); font-size:.68rem; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--orange);
  border:1px solid rgba(255,102,2,.4); padding:6px 14px; border-radius:50px; margin:0 0 16px; }
h1{ font-family:var(--fh); font-size:clamp(1.7rem,4vw,2.3rem); font-weight:700; line-height:1.14; letter-spacing:-.02em; margin:0 0 12px; text-wrap:balance; }
h1 .acc{ color:var(--orange); }
.hero .sub{ font-size:1.02rem; color:var(--tm); max-width:34em; margin:0 auto; }

.cards{ display:flex; flex-direction:column; gap:18px; padding:8px 0 56px; }
.card{ background:rgba(255,255,255,.04); border:1px solid var(--hair); border-radius:var(--r-lg); padding:28px; position:relative; overflow:hidden; }
.card--hot{ border-color:rgba(255,102,2,.42); background:rgba(255,102,2,.06); }
.card__k{ font-family:var(--fh); font-size:.66rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:var(--orange); margin:0 0 8px; }
.card h2{ font-family:var(--fh); font-size:clamp(1.25rem,2.6vw,1.55rem); font-weight:700; line-height:1.2; letter-spacing:-.015em; margin:0 0 8px; }
.card .txt{ font-size:.98rem; color:var(--tm); line-height:1.6; max-width:40em; }
.card .txt b{ color:#fff; font-weight:600; }

/* el estado «listo» esconde la nota previa */
.card[data-listo] .cd-nota{ display:none; }

/* los ítems de la clase */
.items{ list-style:none; padding:0; margin:22px 0 0; display:flex; flex-direction:column; gap:10px; }
.item{ display:flex; align-items:center; gap:14px; padding:16px 18px; border-radius:var(--r); background:rgba(0,0,0,.18); border:1px solid var(--hair); }
.item__ic{ flex:0 0 40px; width:40px; height:40px; border-radius:10px; background:rgba(255,102,2,.12); border:1px solid rgba(255,102,2,.28); display:flex; align-items:center; justify-content:center; }
.item__ic svg{ width:20px; height:20px; color:var(--orange); }
.item__t{ flex:1; min-width:0; }
.item__t b{ display:block; font-family:var(--fh); font-size:1rem; font-weight:700; }
.item__t span{ display:block; font-size:.88rem; color:var(--tm); line-height:1.45; }
.item__st{ flex:0 0 auto; font-family:var(--fh); font-size:.68rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:var(--ts);
  border:1px solid var(--hair); border-radius:50px; padding:7px 12px; white-space:nowrap; }
.item__st--pronto{ color:var(--tm); }
.item{ flex-wrap:wrap; }
.item__video{ flex:0 0 100%; margin-top:4px; }
.item__video[hidden]{ display:none; }
.vbox{ position:relative; width:100%; height:0; padding-bottom:56.25%; border-radius:12px; overflow:hidden; background:#000; box-shadow:0 0 0 1px var(--hair); }
.vbox iframe{ position:absolute; top:0; left:0; width:100%; height:100%; border:0; display:block; }
.item .btn{ flex:0 0 auto; }
.item [data-cuando-listo]{ display:none; }
.card[data-listo] .item [data-cuando-listo]{ display:inline-flex; }
.card[data-listo] .item [data-antes]{ display:none; }

/* botones */
.btn{ display:inline-flex; align-items:center; justify-content:center; gap:9px; font-family:var(--fh); font-size:.98rem; font-weight:700; line-height:1.2;
  color:#fff; background:var(--orange); border:1.5px solid transparent; border-radius:50px; padding:14px 22px; cursor:pointer; white-space:nowrap;
  box-shadow:0 8px 24px var(--orange-glow); transition:transform .22s var(--ease), background .22s var(--ease), box-shadow .22s var(--ease); }
.btn:hover{ background:var(--orange-hover); transform:translateY(-2px); box-shadow:0 12px 32px var(--orange-glow); }
.btn svg{ width:16px; height:16px; flex:0 0 16px; transition:transform .22s var(--ease); }
.btn:hover svg{ transform:translateX(3px); }
.btn--sm{ font-size:.86rem; padding:11px 16px; }
.btn--w{ width:100%; margin-top:18px; }
.card .btn--w{ display:flex; }

.foot{ padding:26px 0 40px; border-top:1px solid var(--hair); text-align:center; }
.foot p{ font-size:.82rem; color:var(--ts); line-height:1.6; }
.foot p+p{ margin-top:6px; }

@media (max-width:600px){
  .nav img{ height:54px; }
  .hero{ padding:34px 0 20px; }
  .card{ padding:22px 18px; }
  .cd{ gap:7px; }
  .cd div{ padding:12px 4px 9px; }
  .item{ flex-wrap:wrap; gap:12px; padding:14px; }
  .item__t{ flex:1 1 160px; }
  .item__st, .item .btn{ margin-left:54px; }
  .item__ic + .item__t + .item__st, .item__ic + .item__t + .btn{ margin-left:0; }
}
@media (prefers-reduced-motion:reduce){ .btn, .btn svg{ transition:none; } }
"""

ICO_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>'
ICO_PLAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9l5 3-5 3z" fill="currentColor" stroke="none"/></svg>'
ICO_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
ICO_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M6 11l6 6 6-6M4 20h16"/></svg>'

def item(key, ico, titulo, bajada, loom=''):
    video = (f"""
          <div class="item__video" data-video="{key}" hidden><div class="vbox"><iframe data-src="https://www.loom.com/embed/{loom}?{LOOM_PARAMS}" title="{titulo} de la clase" frameborder="0" allow="fullscreen; picture-in-picture" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div></div>"""
             if loom else '')
    return f"""
        <li class="item" data-item="{key}">
          <div class="item__ic">{ico}</div>
          <div class="item__t"><b>{titulo}</b><span>{bajada}</span></div>
          <span class="item__st" data-antes>Después de la clase</span>
          <a class="btn btn--sm" data-cuando-listo data-link="{key}" href="#" target="_blank" rel="noopener">Abrir {ICO_ARROW}</a>
          <span class="item__st item__st--pronto" data-cuando-listo data-sinlink="{key}">Lo estamos subiendo · volvé en un rato</span>{video}
        </li>"""

def pagina(slug, pg):
    premium = pg['premium']
    extra = ''
    if premium:
        extra = f"""
      <!-- EL LIBRO -->
      <section class="card card--hot">
        <p class="card__k">Incluido en tu asiento</p>
        <h2>Hackea tu Cerebro · versión ebook</h2>
        <p class="txt">El libro completo, el mismo que está en librerías. Es tuyo: descargalo y guardalo donde quieras.</p>
        <a class="btn btn--w" href="{CFG['LIBRO_URL']}" target="_blank" rel="noopener">Descargar el libro {ICO_DL}</a>
      </section>

      <!-- EL ABC -->
      <section class="card">
        <p class="card__k">Incluido en tu asiento</p>
        <h2>El ABC del Alto Rendimiento</h2>
        <p class="txt">El curso completo en video: <b>6 módulos</b> — mindset, hábitos, sueño y descanso, ejercicio y alimentación, concentración y memoria. Entrá cuando quieras, el acceso no vence.</p>
        <a class="btn btn--w" href="{CFG['ABC_URL']}" target="_blank" rel="noopener">Entrar al curso {ICO_ARROW}</a>
      </section>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{pg['titulo']} · Tus beneficios · Nicolás Fernández Miranda</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

  <nav class="nav"><div class="wrap"><a href="https://nicolasfernandezmiranda.com" aria-label="Nicolás Fernández Miranda"><img src="{CFG['LOGO']}" alt="Nicolás Fernández Miranda"></a></div></nav>

  <header class="hero">
    <div class="wrap">
      <span class="eyebrow">{pg['eyebrow']}</span>
      <h1>Tu asiento está <span class="acc">confirmado.</span></h1>
      <p class="sub" data-sub>Acá está todo lo que incluye tu asiento.</p>
    </div>
  </header>

  <main class="wrap cards">

    <!-- LA CLASE -->
    <section class="card" id="clase">
      <p class="card__k">Tu clase</p>
      <h2 data-fecha="claseLarga">—</h2>
      <p class="txt cd-nota">El <b>workbook</b> con el resumen y los accionables, y la <b>grabación completa</b>, van a estar acá <b>después de la clase del <span data-fecha="claseDia"></span></b>.</p>
      <p class="txt" data-cuando-listo-txt hidden>Ya está disponible lo de la clase. Si algo todavía no aparece, lo estamos subiendo.</p>

      <ul class="items">{item('workbook', ICO_DOC, 'Workbook', 'Resumen de la clase y accionables concretos, en formato de hacer.')}{item('grabacion', ICO_PLAY, 'Grabación', 'La clase completa, tuya para siempre.', CFG['GRABACION_LOOM'])}
      </ul>
    </section>
{extra}
  </main>

  <footer class="foot">
    <div class="wrap">
      <p>Si algo no carga, respondé el mail con el que te llegó este acceso y lo resolvemos.</p>
      <p>© Nicolás Fernández Miranda · Instituto de Productividad</p>
    </div>
  </footer>

<script>
(function(){{
'use strict';
var CFG = {{
  CLASE: '{CFG['CLASE']}',
  LISTO: '{CFG['LISTO']}',
  LINKS: {{ workbook: '{CFG['WORKBOOK_URL']}', grabacion: '{CFG['GRABACION_URL']}' }},
  LOOM:  {{ grabacion: '{CFG['GRABACION_LOOM']}' }}
}};
var DIAS=['domingo','lunes','martes','miércoles','jueves','viernes','sábado'];
var MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
function pad(n){{ return n<10?'0'+n:''+n; }}
function qs(k){{ var m=new RegExp('[?&]'+k+'=([^&#]*)').exec(location.search); return m?decodeURIComponent(m[1]):null; }}
/* ?nfm_now=2026-10-15T12:01:00-03:00 simula otra hora, para probar el estado «listo» */
function ahora(){{ var s=qs('nfm_now'); if(s){{ var t=Date.parse(s); if(!isNaN(t)) return t; }} return Date.now(); }}

/* fechas en hora Argentina, se lea desde donde se lea */
var OFF=-3;
function arg(ts){{ var d=new Date(ts+OFF*3600000); return {{dow:d.getUTCDay(),dia:d.getUTCDate(),mes:d.getUTCMonth(),hh:d.getUTCHours(),mm:d.getUTCMinutes()}}; }}
var pC=CFG.CLASE.split('-'), tsClase=Date.UTC(+pC[0],+pC[1]-1,+pC[2],12-OFF);
var tsListo=Date.parse(CFG.LISTO);
var c=arg(tsClase);
var F={{
  claseLarga: DIAS[c.dow].charAt(0).toUpperCase()+DIAS[c.dow].slice(1)+' '+c.dia+' de '+MESES[c.mes],
  claseDia: DIAS[c.dow]
}};
[].forEach.call(document.querySelectorAll('[data-fecha]'), function(e){{ var k=e.getAttribute('data-fecha'); if(F[k]) e.textContent=F[k]; }});

/* El cambio de estado a la hora configurada (LISTO). No se muestra ninguna
   hora: la página sólo dice «después de la clase». */
var card=document.getElementById('clase');
function listo(){{
  card.setAttribute('data-listo','');
  var t=card.querySelector('[data-cuando-listo-txt]'); if(t) t.hidden=false;
  var sub=document.querySelector('[data-sub]'); if(sub) sub.textContent='Acá está todo lo que incluye tu asiento.';
  var todo=true;
  ['workbook','grabacion'].forEach(function(k){{
    var url=(CFG.LINKS[k]||'').trim(), loom=((CFG.LOOM||{{}})[k]||'').trim();
    var a=card.querySelector('[data-link="'+k+'"]'), s=card.querySelector('[data-sinlink="'+k+'"]'), v=card.querySelector('[data-video="'+k+'"]');
    if(loom && v){{   /* el video se ve acá mismo: sin botón */
      var f=v.querySelector('iframe'); if(f && !f.getAttribute('src')) f.setAttribute('src', f.getAttribute('data-src'));
      v.hidden=false; if(a) a.style.display='none'; if(s) s.style.display='none';
    }}
    else if(url){{ a.setAttribute('href',url); if(s) s.style.display='none'; }}
    else {{ todo=false; if(a) a.style.display='none'; }}
  }});
  if(todo && t) t.textContent='Ya están el workbook y la grabación completa de la clase.';
}}
function tick(){{
  var r=tsListo-ahora();
  if(r<=0){{ listo(); return; }}
  setTimeout(tick, Math.min(r, 60000));   /* vuelve a mirar cada minuto, o justo cuando llega */
}}
tick();
}})();
</script>
</body>
</html>
"""

RAIZ_HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex, nofollow">
<title>Beneficios de la clase · Nicolás Fernández Miranda</title>
<style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#081F33;color:#fff;font-family:'DM Sans',system-ui,sans-serif;text-align:center;padding:24px}}
p{{max-width:30em;line-height:1.6;color:rgba(255,255,255,.7)}} b{{color:#fff}}</style></head>
<body><p><b>Tu acceso está en el mail.</b><br>Abrí el link que te mandamos después de la compra: ahí están tus beneficios.</p></body></html>
"""

ROBOTS = "User-agent: *\nDisallow: /\n"

README = """# Baúl de beneficios · clase del miércoles 14 de octubre

Dos sitios en Netlify, uno por asiento. Cada carpeta se sube sola (Add new site → Deploy manually → arrastrar la carpeta):

| Carpeta | Sitio en Netlify | Asiento |
|---|---|---|
| `asiento-basic-14/` | `asiento-basic-14.netlify.app` | Básico · USD 1 — workbook + grabación |
| `asiento-premium-14/` | `asiento-premium-14.netlify.app` | Hackea tu Productividad · USD 5 — lo mismo + ebook + curso ABC |

El nombre del sitio en Netlify tiene que ser exactamente ese: las thank you de compra y los mails apuntan ahí.

## Cuando estén el workbook y la grabación

Editar `CFG` en `gen-portal.py` — `WORKBOOK_URL` y `GRABACION_URL` — correr
`python3 portal-beneficios/gen-portal.py` desde la raíz del repo, y volver a subir las dos carpetas.
La página no muestra ninguna hora (dice «después de la clase del miércoles»); por dentro cambia de estado en `LISTO`
(jueves 15 a las 12:00, hora Argentina). Sin links cargados, a esa hora dice «lo estamos subiendo», nunca un botón roto.

Para probar el estado «ya disponible» sin esperar: agregar `?nfm_now=2026-10-15T12:01:00-03:00` a la URL.

## Ojo

Sin contraseña: quien tenga el link entra. Llevan noindex y robots.txt para que no las levante Google.
"""

README_7 = """# Baúl de beneficios · clase del miércoles 7 de octubre

Un solo sitio en Netlify (`clase-beneficios.netlify.app`) con dos páginas, como se subió para el 7:

| Ruta | Asiento |
|---|---|
| `/asiento-basic` | Básico · USD 1 — workbook + grabación |
| `/premium-htc` | Hackea tu Productividad · USD 5 — lo mismo + ebook + curso ABC |

Para actualizarlo: Netlify → el sitio → Deploys → arrastrar la carpeta `clase-7-oct` entera.
(Si en vez de un sitio subiste cada asiento como sitio aparte, arrastrá `asiento-basic` y `premium-htc`
cada una a su sitio: las dos páginas funcionan solas.)

Ya está todo cargado: workbook (Drive) y grabación (Loom, se ve adentro del portal).
"""

def main():
    global CFG
    for ed in EDICIONES:
        CFG = dict(COMUN, **ed)
        raiz = ed['carpeta']; os.makedirs(raiz, exist_ok=True)
        for slug, pg in ed['paginas'].items():
            d = os.path.join(raiz, slug); os.makedirs(d, exist_ok=True)
            out = pagina(slug, pg)
            io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
            io.open(os.path.join(d, 'robots.txt'), 'w', encoding='utf-8').write(ROBOTS)
            print('escrito', os.path.join(d, 'index.html'), len(out), 'bytes')
        if ed['un_sitio']:
            io.open(os.path.join(raiz, 'index.html'), 'w', encoding='utf-8').write(RAIZ_HTML)
            io.open(os.path.join(raiz, 'robots.txt'), 'w', encoding='utf-8').write(ROBOTS)
            io.open(os.path.join(raiz, 'README.md'), 'w', encoding='utf-8').write(README_7)
        else:
            io.open(os.path.join(raiz, 'README.md'), 'w', encoding='utf-8').write(README)
        faltan = [k for k in ('WORKBOOK_URL','GRABACION') if not (CFG.get(k) or CFG.get(k+'_URL') or CFG.get(k+'_LOOM'))]
        if faltan: print('   ⚠️  clase', ed['CLASE'], '· sin link todavía:', ', '.join(faltan), '— después de LISTO dirá «lo estamos subiendo».')

main()
