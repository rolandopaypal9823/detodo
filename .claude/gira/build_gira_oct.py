# -*- coding: utf-8 -*-
# Arma hackea-tu-cerebro-gira-oct2026.html: sistema visual de la landing de webinars
# (rama claude/nueva-landing-form-7ajo0h, landing-siempre-on/clase-6-octubre/index.html)
# + funciones, motor y pixel de hackea-tu-cerebro-gira-2026.html.
# Antes de correrlo: git show origin/claude/nueva-landing-form-7ajo0h:landing-siempre-on/clase-6-octubre/index.html > <ruta de W>
import io, re
W = io.open('/tmp/claude-0/-home-user-detodo/9d0166ff-9878-57c8-9b0f-5de407c74f9b/scratchpad/webinar/index.html', encoding='utf-8').read().split('\n')
G = io.open('/home/user/detodo/hackea-tu-cerebro-gira-2026.html', encoding='utf-8').read()
GL = G.split('\n')

def entre(lineas, ini, fin):
    """bloque desde la linea que contiene ini hasta antes de la que contiene fin"""
    a = next(i for i, l in enumerate(lineas) if ini in l)
    b = next(i for i, l in enumerate(lineas) if fin in l and i > a)
    return lineas[a:b]

# ── CSS de la landing de webinars (sistema visual), sin quiz, escenas ni testimonios en video
css_w = entre(W, '/* ════════════════', '</style>')
txt = '\n'.join(css_w)
for ini, fin in [('/* ═══ QUIZ + FORM ═══ */', '/* ═══ NICO · ESCENAS ═══ */'),
                 ('/* ═══ NICO · ESCENAS ═══ */', '/* ═══ QUÉ VAS A DESCUBRIR ═══ */'),
                 ('/* ═══ TESTIMONIOS ═══ */', '.nfm-insight{')]:
    i = txt.index(ini); j = txt.index(fin, i); txt = txt[:i] + txt[j:]
txt = txt.replace('Clase del martes 6 de octubre · Sistema visual NFM', 'Gira Hackea tu Cerebro · octubre · Sistema visual de la landing de webinars')
txt = txt.replace('EVENTO EN VIVO · NEUROCIENCIA PARA EL ALTO RENDIMIENTO PROFESIONAL', 'HACKEA TU CEREBRO · FUNCIÓN EN VIVO')
# reglas responsive de bloques que ya no estan
txt = re.sub(r'\n\s*\.nfm-quiz\{[^\n]*', '', txt)
txt = re.sub(r'\n\s*\.nfm-scene\{[^\n]*', '', txt)
txt = txt.replace('@media (max-width:900px){ .nfm-tst__grid{ grid-template-columns:1fr; max-width:560px; } }\n', '')
txt = txt.replace('.nfm-eq, .nfm-reg, .nfm-nico, .nfm-learn, .nfm-tst{ padding:64px 0; }', '.nfm-eq, .nfm-fx, .nfm-learn, .nfm-who, .nfm-faq{ padding:64px 0; }')

# ── CSS de la gira que la de webinars no tiene: funciones, numeros y preguntas
fx = '\n'.join(entre(GL, 'FUNCIONES  (ocupa el lugar del formulario)', 'EL SHOW / MECANISMO'))
# el reset de la landing de webinars (.nfm-page p{margin:0}) le gana a estos margenes: van con !important
for regla in ('margin:0 auto 44px', 'margin:32px auto 0', 'margin:0 0 8px', 'margin:0 0 20px'):
    assert fx.count(regla + ';') == 1, regla
    fx = fx.replace(regla + ';', regla + ' !important;')
stats = '\n'.join(entre(GL, '.nfm-stats{', '.nfm-insight{'))
faq = '\n'.join(entre(GL, '.nfm-faq{', '/* ════════════════ CTA FINAL'))
extra = '''
/* ═══ FUNCIONES (de la landing de la gira) ═══ */
''' + fx.split('\n', 1)[1] + '''
/* ═══ QUIÉN ESTÁ EN ESCENA ═══ */
.nfm-who{ padding:96px 0; background:linear-gradient(180deg,#0C3452 0%,#081F33 100%); color:#fff; }
.nfm-who__grid{ display:grid; grid-template-columns:0.9fr 1.1fr; gap:48px; align-items:center; max-width:1000px; margin:0 auto 44px; }
.nfm-who__photo{ border-radius:var(--nfm-r-lg); overflow:hidden; border:1px solid var(--nfm-hair); aspect-ratio:4/5; background:var(--nfm-navy-1); }
.nfm-who__photo img{ width:100% !important; height:100% !important; object-fit:cover; object-position:center 30%; }
.nfm-who h2{ font-family:var(--nfm-font-h); font-size:clamp(1.7rem,3.4vw,2.5rem); font-weight:700; letter-spacing:-0.02em; line-height:1.15; margin:0 0 14px; color:#fff; }
.nfm-who p{ font-size:1.06rem; color:var(--nfm-tl); line-height:1.6; max-width:30em; }
.nfm-who p em{ color:var(--nfm-orange); font-style:normal; font-weight:600; }
''' + stats + '''
/* ═══ PREGUNTAS FRECUENTES (de la landing de la gira) ═══ */
''' + faq + '''
@media (max-width:1024px){ .nfm-fx__grid{ grid-template-columns:1fr 1fr; } }
@media (max-width:768px){
  .nfm-fx__grid{ grid-template-columns:1fr; }
  .nfm-stats{ grid-template-columns:1fr; gap:10px; max-width:460px; }
  .nfm-stat{ display:flex; align-items:center; gap:16px; text-align:left; padding:16px 20px; }
  .nfm-stat b{ flex:0 0 auto; font-size:1.55rem; margin:0; }
  .nfm-stat span{ font-size:0.9rem; }
  .nfm-who__grid{ grid-template-columns:1fr; gap:24px; text-align:center; }
  .nfm-who__photo{ aspect-ratio:4/3; max-width:420px; width:100%; margin:0 auto; }
  .nfm-who .nfm-eyebrow, .nfm-who h2, .nfm-who p{ text-align:center; margin-left:auto; margin-right:auto; }
  .nfm-faq__item summary{ padding:18px 20px; font-size:0.94rem; }
  .nfm-faq__item p{ padding:0 20px 20px; font-size:0.92rem; }
}
'''
css = txt + extra

# ── HEAD: el de la gira (titulo, meta, pixel)
head = G[:G.index('<!-- ═══════════ DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL ═══════════ -->')]

# ── logos de prensa: los mismos de la landing de webinars
logos = '\n'.join(entre(W, '<div class="nfm-marquee__set">', '<div class="nfm-marquee__set" aria-hidden="true">')[1:-1])

# ── iconos de la lista (los de la landing de webinars)
ICO = {
 'foco': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/><path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3"/></svg>',
 'energia': '<svg viewBox="0 0 24 24"><rect x="2.5" y="7" width="17" height="10" rx="2.5"/><path d="M19.5 10.5h1.5a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-1.5"/><path d="M12 8.5l-2.5 4h4L11 16"/></svg>',
 'habitos': '<svg viewBox="0 0 24 24"><path d="M3 21h18M5 21V10M10 21V10M14 21V10M19 21V10M2.5 10L12 3l9.5 7z"/></svg>',
 'manana': '<svg viewBox="0 0 24 24"><circle cx="6" cy="5.5" r="2.2"/><circle cx="18" cy="5.5" r="2.2"/><circle cx="12" cy="18.5" r="2.2"/><path d="M6 7.7v1.8a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4V7.7M12 13.5v2.8"/></svg>',
}
FOTO = 'https://assets.cdn.filesafe.space/qSngYAz0JpogeHnqp5cS/media/6abebcf18807113c2d2770f2.jpeg'   # foto de Nico solo, en la galeria de GHL
FLECHA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

def item(ico, titulo, texto):
    return ('      <div class="nfm-map__item"><div class="nfm-map__ico" aria-hidden="true">%s</div>'
            '<div class="nfm-map__txt"><h4><b>%s</b> %s</h4></div></div>' % (ICO[ico], titulo, texto))

body = '''<div class="nfm-page">

<!-- ═══ NAV · contador a la próxima función ═══ -->
<nav class="nfm-nav" id="nfm-nav">
  <div class="nfm-container nfm-nav__inner">
    <div class="nfm-nav__cd" aria-label="Cuenta regresiva para la próxima función">
      <span class="nfm-nav__cd-lbl">La próxima función empieza en</span>
      <div class="nfm-nav__cd-t">
        <span><b id="nfm-cd-days">00</b><i>días</i></span>
        <span><b id="nfm-cd-hours">00</b><i>hs</i></span>
        <span><b id="nfm-cd-min">00</b><i>min</i></span>
        <span><b id="nfm-cd-sec">00</b><i>seg</i></span>
      </div>
    </div>
  </div>
</nav>

<!-- ═══ HERO ═══ -->
<section class="nfm-hero" id="nfm-hero">
  <div class="nfm-hero__card">
    <div class="nfm-hero__bg">
      <img src="https://cdn.shopify.com/s/files/1/0968/8865/1849/files/IMG_9766_1.jpg?v=1773009489&width=1600" alt="Nicolás Fernández Miranda en escena" loading="eager">
    </div>
    <div class="nfm-hero__inner">
      <span class="nfm-hero__tag"><span class="nfm-dot"></span> Función en vivo · Gira 2026</span>
      <h1 class="nfm-hero__title">Hackea tu Cerebro <em>en vivo</em></h1>
      <p class="nfm-hero__event">Una noche para entender cómo funciona tu cerebro y usarlo a tu favor.</p>
      <p class="nfm-hero__sub">90 minutos de neurociencia contada con humor, para aplicar al día siguiente.</p>
      <p class="nfm-hero__with">con Nico Fernández Miranda</p>
      <p class="nfm-hero__pill" id="nfm-hero-pill">Próxima función: <span id="nfm-next-city">Villa María</span> · <span id="nfm-next-date">Sáb 24 OCT</span> · <span id="nfm-next-venue">Teatro Verdi</span></p>
      <div class="nfm-hero__cta-wrap">
        <button class="nfm-btn" data-scroll-to="nfm-funciones">ELEGIR MI FUNCIÓN ''' + FLECHA + '''</button>
      </div>
    </div>
  </div>
</section>

<!-- ═══ PRENSA ═══ -->
<section class="nfm-proof" aria-label="Su trabajo fue destacado en">
  <div class="nfm-proof__label">Su trabajo fue destacado en</div>
  <div class="nfm-marquee">
    <div class="nfm-marquee__track">
      <div class="nfm-marquee__set">
''' + logos + '''
      </div>
      <div class="nfm-marquee__set" aria-hidden="true">
''' + logos + '''
      </div>
    </div>
  </div>
</section>

<!-- ═══ FUNCIONES · arriba a propósito: el que ya viene decidido compra sin scrollear ═══ -->
<section class="nfm-fx" id="nfm-funciones">
  <div class="nfm-fx__particles" id="nfm-fx-particles"></div>
  <div class="nfm-container">
    <h2 class="nfm-fx__title nfm-reveal">Elegí tu función. <span>Y asegurá tu lugar.</span></h2>
    <p class="nfm-fx__sub nfm-reveal nfm-d1">Después del éxito de CABA, San Rafael, Mendoza y San Juan, la gira llega a:</p>
    <!-- las tarjetas se generan solas desde el bloque FUNCIONES del script -->
    <div class="nfm-fx__grid nfm-reveal nfm-d1" id="nfm-fx-grid"></div>
    <p class="nfm-fx__note nfm-reveal nfm-d2">Cada botón te lleva a la ticketera oficial de esa función.</p>
  </div>
</section>

<!-- ═══ LO QUE ESTE SHOW DESARMA ═══ -->
<section class="nfm-eq">
  <div class="nfm-container nfm-narrow">
    <span class="nfm-eyebrow nfm-reveal">Lo que este show desarma</span>
    <h2 class="nfm-reveal nfm-d1">Probaste de todo.<br><em>Faltaba una pieza.</em></h2>
    <div class="nfm-eq__board nfm-reveal nfm-d2" aria-label="Lo que ya probaste">
      <ul class="nfm-eq__list">
        <li><s>Más fuerza de voluntad</s></li>
        <li><s>Otra app de productividad</s></li>
        <li><s>Levantarte a las 5&nbsp;am</s></li>
        <li><s>El tercer café de la tarde</s></li>
        <li><s>Arrancar el hábito otra vez el lunes</s></li>
      </ul>
      <div class="nfm-eq__sum">
        <span class="nfm-eq__blur" aria-hidden="true">Lo que falta</span>
        <span class="nfm-eq__grp"><span class="nfm-eq__op">=</span><span>días que te rinden</span><span class="nfm-eq__mark nfm-eq__mark--yes" aria-label="correcto">✓</span></span>
      </div>
    </div>
    <p class="nfm-eq__cap nfm-reveal nfm-d3"><strong>¿Cuál es la pieza?</strong><br>La vas a ver en escena: cómo funciona tu cerebro y cómo usarlo a tu favor.</p>
  </div>
</section>

<!-- ═══ QUÉ TE LLEVÁS ═══ -->
<section class="nfm-learn">
  <div class="nfm-container">
    <div class="nfm-learn__head nfm-reveal">
      <span class="nfm-eyebrow">La noche</span>
      <h2>Salís del teatro con el manual</h2>
    </div>
    <div class="nfm-map nfm-reveal nfm-d1">
''' + '\n'.join([
    item('foco', 'Foco a demanda:', 'qué enciende y qué apaga tu atención.'),
    item('energia', 'Energía para todo el día:', 'por qué a las tres de la tarde te caés, y qué hacer.'),
    item('habitos', 'Hábitos que se sostienen:', 'cómo armar uno que no dependa de la motivación del lunes.'),
    item('manana', 'Un primer paso para mañana:', 'algo concreto para aplicar apenas te despertás.'),
]) + '''
    </div>
    <div class="nfm-learn__cta nfm-reveal nfm-d2">
      <button class="nfm-btn" data-scroll-to="nfm-funciones">ELEGIR MI FUNCIÓN ''' + FLECHA + '''</button>
    </div>
  </div>
</section>

<!-- ═══ QUIÉN ESTÁ EN ESCENA ═══ -->
<section class="nfm-who">
  <div class="nfm-container">
    <div class="nfm-who__grid">
      <!-- Foto de Nico solo (galeria de GHL). Para cambiarla, reemplaza el link del src. -->
      <div class="nfm-who__photo nfm-reveal"><img src="''' + FOTO + '''" alt="Nicolás Fernández Miranda" loading="lazy"></div>
      <div class="nfm-reveal nfm-d1">
        <span class="nfm-eyebrow nfm-eyebrow--solid">Quién está en escena</span>
        <h2>Nicolás Fernández Miranda</h2>
        <p>Contador y magíster en neurociencias. Escribió <em>Hackea tu cerebro</em>, el libro del que sale el show.</p>
      </div>
    </div>
    <div class="nfm-stats">
      <div class="nfm-stat nfm-reveal nfm-d1"><b>+15.000</b><span>personas ya lo vieron en vivo</span></div>
      <div class="nfm-stat nfm-reveal nfm-d2"><b>Bestseller</b><span>“Hackea tu cerebro”, de Ediciones Lea</span></div>
      <div class="nfm-stat nfm-reveal nfm-d3"><b>+1M</b><span>de seguidores en redes</span></div>
    </div>
  </div>
</section>

<!-- ═══ PREGUNTAS FRECUENTES ═══ -->
<section class="nfm-faq">
  <div class="nfm-container">
    <div class="nfm-faq__head nfm-reveal">
      <span class="nfm-eyebrow">Dudas típicas</span>
      <h2>Preguntas frecuentes</h2>
    </div>
    <div class="nfm-faq__list nfm-reveal nfm-d1">
      <details class="nfm-faq__item"><summary>¿Cuánto dura el show?</summary><p>Unos 90 minutos.</p></details>
      <details class="nfm-faq__item"><summary>¿Es una charla técnica?</summary><p>Es un show en vivo y con humor. Nico explica la neurociencia en palabras simples, para que la uses al día siguiente.</p></details>
      <details class="nfm-faq__item"><summary>¿Necesito haber leído el libro?</summary><p>Te sirve igual. El show sale del libro y va más allá: si lo leíste vas a ver cosas nuevas, y si no, entendés todo desde cero.</p></details>
      <details class="nfm-faq__item"><summary>¿Puedo comprar en la puerta?</summary><p>Si quedan entradas, sí, pero a precio full. Te conviene comprar antes en la ticketera de tu función.</p></details>
      <details class="nfm-faq__item"><summary>¿Pueden ir menores?</summary><p>Sí, es apto para todo público.</p></details>
    </div>
  </div>
</section>

<!-- ═══ CIERRE ═══ -->
<section class="nfm-final">
  <div class="nfm-container nfm-mid">
    <h2 class="nfm-reveal">Tu cerebro es tu activo más valioso. <em>Invertí una noche en entenderlo.</em></h2>
    <div class="nfm-reveal nfm-d1">
      <button class="nfm-btn" data-scroll-to="nfm-funciones">ELEGIR MI FUNCIÓN ''' + FLECHA + '''</button>
    </div>
    <div class="nfm-reveal nfm-d2"><p class="nfm-final__date"><span class="nfm-dot"></span><span id="nfm-final-cities">Villa María · Córdoba · CABA</span></p></div>
  </div>
</section>

<footer class="nfm-footer"><div class="nfm-container"><p>© 2026 Nicolás Fernández Miranda · Instituto de Productividad · Todos los derechos reservados.</p></div></footer>

<div class="nfm-sticky" id="nfm-sticky"><button class="nfm-btn" data-scroll-to="nfm-funciones">Elegir mi función</button></div>

</div><!-- /.nfm-page -->
'''

# ── MOTOR: el de la gira (funciones, contador, pixel), adaptado a la barra de arriba
motor = G[G.index('<script>\n/* ════════════════════════════════════════════════════════════════════════════════\n   NFM · MOTOR DE LA LANDING DE GIRA'):G.index('<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->')]
def rep(a, b):
    global motor
    assert motor.count(a) == 1, a[:70]
    motor = motor.replace(a, b)
rep('''    var cd = document.querySelector('.nfm-cd'), lb = document.querySelector('.nfm-cd-label'),
        fe = document.querySelector('.nfm-hero__date');
    if(cd) cd.style.display='none'; if(lb) lb.style.display='none'; if(fe) fe.style.display='none';''',
    '''    var nv = document.getElementById('nfm-nav'), pl = document.getElementById('nfm-hero-pill');
    if(nv) nv.style.display='none'; if(pl) pl.style.display='none';''')
rep('''    if(diff <= 0){
      document.querySelector('.nfm-page').classList.add('nfm-is-live');
      return;
    }''', '''    if(diff <= 0){
      var lbl = document.querySelector('.nfm-nav__cd-lbl'), t = document.querySelector('.nfm-nav__cd-t');
      if(lbl) lbl.textContent = 'La función es hoy · quedan las últimas entradas';
      if(t) t.style.display = 'none';
      return;
    }''')
rep("makeParticles('nfm-particles', 22);\n", '')
rep("""  var nav = document.getElementById('nfm-nav'), sticky = document.getElementById('nfm-sticky');
  window.addEventListener('scroll', function(){
    if(nav)    nav.classList.toggle('nfm-nav--scrolled', window.scrollY > 60);
    if(sticky) sticky.classList.toggle('nfm-sticky--show', window.scrollY > 700);
  }, {passive:true});""", """  var nav = document.getElementById('nfm-nav'), sticky = document.getElementById('nfm-sticky');
  var heroBtn = document.querySelector('.nfm-hero__cta-wrap .nfm-btn'), fx = document.getElementById('nfm-fx-grid');
  function seVe(el){ if(!el) return false; var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; }
  function actualizar(){
    if(nav) nav.classList.toggle('nfm-nav--scrolled', window.scrollY > 60);
    /* la barra de abajo aparece cuando no se ve ni el boton del hero ni las funciones:
       en un celular chico el boton queda a mano desde el primer segundo */
    if(sticky) sticky.classList.toggle('nfm-sticky--show', !seVe(heroBtn) && !seVe(fx));
  }
  window.addEventListener('scroll', actualizar, {passive:true});
  window.addEventListener('resize', actualizar);
  actualizar();""")

html = head + '''<!-- ═══════════ DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL ═══════════ -->

<style>
''' + css + '''
</style>

''' + body + '\n' + motor + '<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->\n</body>\n</html>\n'
io.open('/home/user/detodo/hackea-tu-cerebro-gira-oct2026.html', 'w', encoding='utf-8').write(html)
print(len(html), 'bytes')
