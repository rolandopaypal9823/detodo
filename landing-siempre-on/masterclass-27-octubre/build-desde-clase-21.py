# Landing de la masterclass del 27/10 con la MISMA estructura que la del 21 (index-popup.html):
# hero → prensa + tráiler → (la semana, en vez de la ecuación) → historia de Nico → qué vas a aprender
# → casos de éxito → cierre → popup. El popup va directo al form: sin pregunta de etapa.
import re
SRC = '/home/user/detodo/landing-siempre-on/clase-21-octubre/index-popup.html'
DST = '/home/user/detodo/landing-siempre-on/masterclass-27-octubre/index.html'
s = open(SRC, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

def cut(a, b, nuevo):
    """reemplaza desde a (incluido) hasta b (excluido)"""
    global s
    i = s.index(a); j = s.index(b, i)
    assert s.count(a) == 1
    s = s[:i] + nuevo + s[j:]

# ── head ──
rep('<title>Dejá de pagar el sobreprecio de ser "productivo" · Neurociencia para el Alto Rendimiento Profesional · Evento en vivo con Nico Fernández Miranda</title>',
    '<title>Neurociencia aplicada: cómo dejar de procrastinar, concentrarte y cumplir lo que planificás · Clase gratuita en vivo con Nico Fernández Miranda</title>')
rep('<meta name="description" content="Evento en vivo: Neurociencia para el Alto Rendimiento Profesional, con Nico Fernández Miranda. Para líderes, empresarios y profesionales que ya construyeron algo y están pagando el costo de sostenerlo.">',
    '<meta name="description" content="Clase gratuita en vivo con Nico Fernández Miranda: cómo usar la neurociencia para concentrarte, dejar de procrastinar y cumplir lo que planificás.">')
rep('''<!-- VARIANTE POPUP · el quiz + form no está en la página: se abre en un popup al tocar cualquier botón.
     El popup se cierra SÓLO con la X (no con clic afuera ni con Escape). Para test A/B contra index.html. -->''',
    '''<!-- MASTERCLASS DEL MARTES 27/10 · misma estructura que la landing de la clase del 21 (variante popup).
     Cualquier botón abre el popup con el form de GHL directo, sin preguntas antes: registro en masa.
     El popup se cierra SÓLO con la X (no con clic afuera ni con Escape). -->''')
rep('''   NFM · EVENTO EN VIVO · NEUROCIENCIA PARA EL ALTO RENDIMIENTO PROFESIONAL
   Clase del miércoles 21 de octubre · Sistema visual NFM''',
    '''   NFM · CLASE GRATUITA EN VIVO · NEUROCIENCIA DE LA PRODUCTIVIDAD
   Masterclass del martes 27 de octubre · Sistema visual NFM''')

# ── CSS: la ecuación se reemplaza por "la semana" ──
cut('/* ═══ ECUACIÓN ═══ */', '/* ═══ QUIZ + FORM ═══ */', '''/* ═══ LA SEMANA · espejo corto + el dato + el mecanismo en una línea ═══ */
.nfm-eq{ background:var(--nfm-white); padding:84px 0; text-align:center; }
.nfm-eq .nfm-container{ display:flex; flex-direction:column; align-items:center; }
.nfm-eq h2{ width:100%; text-align:center !important; font-family:var(--nfm-font-h); font-size:clamp(1.5rem,3vw,2.1rem); font-weight:700; color:var(--nfm-ink); letter-spacing:-0.02em; line-height:1.15; margin:0 0 32px; text-wrap:balance; }
.nfm-eq h2 em{ color:var(--nfm-orange); font-style:normal; }
.nfm-week{ width:100%; max-width:560px; margin:0 auto !important; text-align:left; background:var(--nfm-gray-50); border:1px solid var(--nfm-gray-200); border-radius:var(--nfm-r-lg); padding:26px 26px 22px; box-shadow:0 20px 60px rgba(12,52,82,0.08); }
.nfm-week__lbl{ font-family:var(--nfm-font-h); font-size:0.7rem; font-weight:600; letter-spacing:0.16em; text-transform:uppercase; color:var(--nfm-ink-mute); margin:0 0 16px !important; }
.nfm-week__row{ display:grid; grid-template-columns:6.4rem minmax(0,1fr) 3.4rem; align-items:center; gap:12px; margin:0 0 12px; font-family:var(--nfm-font-h); font-size:0.98rem; font-weight:600; color:var(--nfm-ink); }
.nfm-week__row:last-of-type{ margin-bottom:0; }
.nfm-week__bar{ height:14px; border-radius:7px; background:var(--nfm-gray-200); overflow:hidden; }
.nfm-week__bar i{ display:block; height:100%; border-radius:7px; background:var(--nfm-navy); }
.nfm-week__h{ text-align:right; font-weight:700; font-variant-numeric:tabular-nums; }
.nfm-week__row--you, .nfm-week__row--you .nfm-week__h{ color:var(--nfm-orange); }
.nfm-week__row--you .nfm-week__bar i{ background:var(--nfm-orange); }
.nfm-eq__cap{ margin:26px auto 0 !important; font-family:var(--nfm-font-h); font-size:1.05rem; color:var(--nfm-ink-mute); max-width:34em; line-height:1.5; text-align:center !important; text-wrap:balance; }
.nfm-eq__cap strong{ color:var(--nfm-ink); font-weight:700; }

''')
rep('''  .nfm-eq__board{ padding:26px 16px; }
  .nfm-eq__list li{ font-size:1rem; padding:9px 0; } .nfm-eq__list li s{ text-decoration-thickness:2px; } .nfm-eq__sum{ font-size:1.18rem; gap:8px 10px; } .nfm-eq__grp{ gap:10px; }''',
    '''  .nfm-week{ padding:22px 18px 20px; } .nfm-week__row{ grid-template-columns:5.6rem minmax(0,1fr) 3rem; gap:10px; font-size:0.92rem; }''')
rep(' .nfm-eq__list li{ font-size:0.94rem; } .nfm-eq__sum{ font-size:1.1rem; } }', ' }')
# el popup ya no tiene quiz: el form ocupa todo el panel
rep('.nfm-modal .nfm-quiz{ box-shadow:none; padding:24px; text-align:left; margin:0 auto; }',
    '.nfm-modal .nfm-quiz{ box-shadow:none; padding:0; border:none; background:none; text-align:left; margin:0 auto; }')
rep('  .nfm-modal .nfm-quiz{ padding:12px; }\n', '')

# ── HERO ──
rep('<span class="nfm-hero__tag"><span class="nfm-dot"></span> Evento en vivo</span>',
    '<span class="nfm-hero__tag"><span class="nfm-dot"></span> Clase gratuita en vivo</span>')
rep('<h1 class="nfm-hero__title">Dejá de pagar el <em>sobreprecio</em> de ser "productivo".</h1>',
    '<h1 class="nfm-hero__title">Neurociencia aplicada: cómo <em>dejar de procrastinar</em>, concentrarte y cumplir lo que planificás</h1>')
rep('<p class="nfm-hero__event">Neurociencia para el Alto Rendimiento Profesional</p>',
    '<p class="nfm-hero__event">¿Terminás la semana sin energía y con tus cosas igual que el lunes?</p>')
rep('<p class="nfm-hero__sub">Seguí escalando sin pagarlo con tu sueño, tu salud ni tiempo con tu familia.</p>',
    '<p class="nfm-hero__sub">Qué hace tu cerebro para que tus cosas siempre queden para después, y cómo planificar una semana que puedas sostener.</p>')
rep('<span data-nfm-fecha="pill">Mié 21 oct · 19:00 hs (Arg) · Zoom</span>', '<span data-nfm-fecha="pill">Mar 27 oct · 19:00 hs (Arg) · Zoom</span>')

# ── LA ECUACIÓN → LA SEMANA (corto) ──
cut('<!-- ═══ LA ECUACIÓN ═══ -->', '<!-- ═══ QUIZ + REGISTRO ═══ -->', '''<!-- ═══ LA SEMANA · espejo + dato (anuncio C2) + mecanismo en una línea ═══ -->
<section class="nfm-eq">
  <div class="nfm-container nfm-narrow">
    <span class="nfm-eyebrow nfm-reveal">La escena se repite</span>
    <h2 class="nfm-reveal nfm-d1">Cumpliste con todos.<br><em>Tus cosas quedaron en cero.</em></h2>
    <div class="nfm-week nfm-reveal nfm-d2" aria-label="Una semana cualquiera: 50 horas de trabajo y entre 0 y 2 horas para tus cosas">
      <p class="nfm-week__lbl">Una semana cualquiera</p>
      <div class="nfm-week__row"><span>Trabajo</span><span class="nfm-week__bar"><i style="width:100%"></i></span><span class="nfm-week__h">50 h</span></div>
      <div class="nfm-week__row nfm-week__row--you"><span>Tus cosas</span><span class="nfm-week__bar"><i style="width:4%"></i></span><span class="nfm-week__h">0–2 h</span></div>
    </div>
    <p class="nfm-eq__cap nfm-reveal nfm-d3"><strong>Tu cerebro tarda hasta 23 minutos en volver a lo tuyo después de cada interrupción.</strong><br>Lo vemos en vivo el <span data-nfm-fecha="diaYNumero">martes 27</span>: cómo concentrarte, dejar de procrastinar y cumplir lo que planificás.</p>
  </div>
</section>

''')
# "lo tuyo" está vetado
rep('en volver a lo tuyo después de cada interrupción.', 'en volver a concentrarse después de cada interrupción.')

# ── NICO · las escenas quedan igual; sólo el encabezado y el cierre ──
rep('<span class="nfm-eyebrow">Quién da el evento</span>', '<span class="nfm-eyebrow">Quién da la clase</span>')
rep('''<p><strong>Este <span data-nfm-fecha="larga">miércoles 21 de octubre</span> te va a mostrar cómo usar la neurociencia para escalar tus resultados y avanzar en lo importante de tu vida sin pagar el costo en tu bienestar ni en el tiempo con tu familia. Y sostener lo que ya lograste.</strong></p>''',
    '''<p><strong>Este <span data-nfm-fecha="larga">martes 27 de octubre</span> te va a mostrar, con lo que dice la neurociencia, cómo planificar tu semana para que tus cosas dejen de quedar para después.</strong></p>''')

# ── QUÉ VAS A APRENDER · las 5 promesas, una por anuncio ──
rep('<span class="nfm-eyebrow">Contenido del evento</span>', '<span class="nfm-eyebrow">Contenido de la clase</span>')
rep('<h2>Qué vas a aprender el <span data-nfm-fecha="abr">21 de Oct.</span> en Vivo</h2>', '<h2>Qué vas a aprender el <span data-nfm-fecha="abr">27 de Oct.</span> en Vivo</h2>')
items = [
  ('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9.5 2.5h5"/>', 'Las interrupciones:', 'por qué cada una te cuesta hasta 23 minutos y cuántas horas se te van por semana sin que te des cuenta.'),
  ('<rect x="5" y="3.5" width="14" height="17" rx="2.5"/><path d="M9 8.5h6M9 12.5h6M9 16.5h3.5"/>', 'El plan escrito:', 'dónde se esconden las horas que perdés cada vez que te sentás a trabajar sin uno.'),
  ('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14.5h3"/>', 'Tu semana:', 'cómo planificarla para que tus cosas dejen de quedar para lo último.'),
  ('<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>', 'Cuando la semana se desarma:', 'qué hacer para no abandonar todo otra vez.'),
  ('<circle cx="8" cy="8.5" r="3"/><circle cx="16.5" cy="8.5" r="3"/><path d="M2.5 19.5a5.5 5.5 0 0 1 11 0M11.5 19.5a5.5 5.5 0 0 1 10 0"/>', 'Hacerlo acompañado:', 'por qué tu cerebro rinde distinto cuando hacés las cosas junto a otras personas.'),
]
nuevo = ''.join(f'      <div class="nfm-map__item"><div class="nfm-map__ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ico}</svg></div><div class="nfm-map__txt"><h4><b>{t}</b> {d}</h4></div></div>\n' for ico, t, d in items)
i = s.index('    <div class="nfm-map nfm-reveal nfm-d1">\n') + len('    <div class="nfm-map nfm-reveal nfm-d1">\n')
j = s.index('    </div>\n    <div class="nfm-learn__cta', i)
assert s[i:j].count('nfm-map__item') == 7
s = s[:i] + nuevo + s[j:]

# ── CIERRE ──
rep('<h2 class="nfm-reveal">El <span data-nfm-fecha="corta">21 de octubre</span> vas a ver <em>la variable que no estás mirando.</em></h2>',
    '<h2 class="nfm-reveal">El <span data-nfm-fecha="corta">27 de octubre</span> vas a ver cómo usar la neurociencia para <em>concentrarte y dejar de procrastinar.</em></h2>')
rep('<span data-nfm-fecha="completa">Miércoles 21 de octubre · 19:00 hs (Argentina) · En vivo por Zoom</span>',
    '<span data-nfm-fecha="completa">Martes 27 de octubre · 19:00 hs (Argentina) · En vivo por Zoom</span>')

# ── POPUP: directo al form, sin preguntas ──
cut('    <h2 class="nfm-reg__title" id="nfm-modal-title">', '</div>\n\n</div><!-- /.nfm-page -->', '''    <h2 class="nfm-reg__title" id="nfm-modal-title">Reservá tu lugar <span>en la clase.</span></h2>
    <div class="nfm-quiz" id="nfm-quiz">
      <!-- FORM DE GHL · "Form Webinar Comunidad". El src se arma por JS al abrir el popup: lleva las UTM y la clase.
           Si se cambia de form, el ID va acá (data-src, id, data-layout-iframe-id, data-form-id) y en CONFIG.FORM_ID. -->
      <div class="nfm-reg__form" id="nfm-form-principal">
        <iframe
          data-src="https://api.leadconnectorhq.com/widget/form/ib4zw3gRec1D9D3kxyUv"
          id="inline-ib4zw3gRec1D9D3kxyUv"
          data-layout="{'id':'INLINE'}" data-trigger-type="alwaysShow" data-trigger-value=""
          data-activation-type="alwaysActivated" data-activation-value=""
          data-deactivation-type="neverDeactivate" data-deactivation-value=""
          data-form-name="Form Webinar Comunidad" data-height="1366"
          data-layout-iframe-id="inline-ib4zw3gRec1D9D3kxyUv" data-form-id="ib4zw3gRec1D9D3kxyUv"
          data-cookie-consent="true" data-cookie-consent-provider="auto"
          title="Form Webinar Comunidad" style="width:100%;height:100%;border:none;border-radius:15px"></iframe>
      </div>
    </div>
  </div>
''')

# ── JS ──
rep('''   CONFIG · versión FIJA para la clase del 21 de octubre''', '''   CONFIG · masterclass del martes 27 de octubre
   ⚠️ Hora a confirmar: si cambia, tocá sólo HORA_CLASE / MINUTOS_CLASE.''')
rep('''  FECHA: '2026-10-21',                       // miércoles 21 de octubre
  UTM_CLASE: 'clase-oct21-alto-rendimiento', // etiqueta de campaña para leads sin UTM
  HORA_CLASE: 19, MINUTOS_CLASE: 0, OFFSET_ARG: -3,
  FORM_ID: 'kLh5onxCgHdGDA10c8NU', FORM_ALTO_MINIMO: 729,                 // form principal · etapa A o B
  FORM_COMUNIDAD_ID: 'w6wTjXjcIScDip8GuVBr', FORM_COMUNIDAD_ALTO_MINIMO: 620 // form para comunidad · etapa C''',
    '''  FECHA: '2026-10-27',                        // martes 27 de octubre
  UTM_CLASE: 'masterclass-oct27-comunidad',   // va en utm_campaign (si el lead llega sin UTM) y en edicion
  HORA_CLASE: 19, MINUTOS_CLASE: 0, OFFSET_ARG: -3,
  FORM_ID: 'ib4zw3gRec1D9D3kxyUv', FORM_ALTO_MINIMO: 1366  // "Form Webinar Comunidad" · alto = data-height del embed''')
cut('/* ─── QUIZ ───', '/* ─── fotos de las escenas', '''/* ─── FORM ───
   Sin preguntas antes: al abrir el popup se carga el form con las UTM, la fecha y la edición en la URL.
   La clase queda en sessionStorage para la thank you page. */
function cargarForm(){
  var ifr=document.getElementById('inline-'+CONFIG.FORM_ID); if(!ifr) return;
  var pasar=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','utm_id','fbclid','gclid','ttclid','ad_id','adset_id','campaign_id','ref'];
  var p=[], i, v, tieneSource=false, tieneCampaign=false;
  for(i=0;i<pasar.length;i++){ v=qs(pasar[i]); if(v){ p.push(encodeURIComponent(pasar[i])+'='+encodeURIComponent(v)); if(pasar[i]==='utm_source') tieneSource=true; if(pasar[i]==='utm_campaign') tieneCampaign=true; } }
  if(!tieneSource) p.push('utm_source=directo');
  if(!tieneCampaign) p.push('utm_campaign='+encodeURIComponent(CONFIG.UTM_CLASE));
  p.push('clase_fecha='+CONFIG.FECHA);
  p.push('edicion='+encodeURIComponent(CONFIG.UTM_CLASE));
  var base=ifr.getAttribute('data-src')||('https://api.leadconnectorhq.com/widget/form/'+CONFIG.FORM_ID);
  var url=base+(base.indexOf('?')===-1?'?':'&')+p.join('&');
  if(ifr.getAttribute('src')!==url){ ifr.src=url; ifr.style.minHeight=CONFIG.FORM_ALTO_MINIMO+'px'; }
  try{
    window.sessionStorage.setItem('nfm_clase', CONFIG.UTM_CLASE);
    window.sessionStorage.setItem('nfm_clase_fecha', CONFIG.FECHA);
  }catch(err){}
}

''')
rep('''  calentarForm(CONFIG.FORM_ID);
  var primero=modal.querySelector('.nfm-quiz__step.nfm-on .nfm-opt, .nfm-quiz__step.nfm-on input, .nfm-quiz__step.nfm-on iframe');''',
    '''  cargarForm();
  var primero=modal.querySelector('iframe');''')
# precarga: el form se calienta apenas carga la página, así el popup abre rápido
rep('''/* ─── fotos de las escenas''', '''/* ─── PRECARGA ───
   Cuando la página termina de cargar, el form se carga en el iframe del popup (oculto), así al tocar
   cualquier botón ya está listo. Cuenta como una "vista" del form en las estadísticas de GHL. */
window.addEventListener('load', function(){ setTimeout(cargarForm, 1200); });

/* ─── fotos de las escenas''')

# ── controles ──
for viejo in ['21 de oct', 'iércoles 21', 'Mié 21', 'oct21', 'class="nfm-opt', 'class="nfm-alerta"', 'w6wTjXjcIScDip8GuVBr', 'sobreprecio', 'calentarForm(', 'resp.etapa', 'cabeza']:
    assert viejo not in s, viejo
open(DST, 'w', encoding='utf-8').write(s)
t = re.sub(r'<(script|style)[\s\S]*?</\1>', '', s); t = re.sub(r'<[^>]+>', ' ', t)
for w in ['tuyo', 'cabeza', 'comprá']:
    if w in t.lower(): print('OJO', w)
print('ok', len(s)//1024, 'KB')
