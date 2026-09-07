# -*- coding: utf-8 -*-
"""Genera las dos versiones de la thank you con el pop-up (OTO).
   Las dos salen del mismo cuerpo: lo único que cambia es el bloque de tema.
   Así no se desincronizan cuando toquemos el copy."""
import io, os

BASE = 'nfm-clase-paga/thankyou-base.html'
s = io.open(BASE, encoding='utf-8').read()

# ══════════════════════════════════════════════════════════════════════════
#  CSS · estructura (idéntica en las dos versiones)
# ══════════════════════════════════════════════════════════════════════════
CSS_COMUN = """
/* ════════════════════════════════════════════════════════════════
   OTO · el pop-up de la oferta única
   No tiene X y no se cierra clickeando afuera ni con Escape: las
   únicas tres salidas son los dos botones y el link gris de abajo.
   Eso es a propósito — es una decisión, no un banner.
   ════════════════════════════════════════════════════════════════ */
.oto{ position:fixed; inset:0; z-index:99999; display:none;
  align-items:center; justify-content:center; padding:20px;
  background:rgba(4,14,24,.88); -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px); }
.oto[data-open]{ display:flex; }
.oto *, .oto *::before, .oto *::after{ box-sizing:border-box; }
body[data-oto-open]{ overflow:hidden; }

.oto__box{ width:100%; max-width:840px; max-height:92vh; overflow-y:auto;
  border-radius:var(--nfm-r-lg); padding:30px 34px 0;
  font-family:var(--nfm-font-b); text-align:center;
  animation:oto-in .42s var(--nfm-ease) both;
  background:var(--oto-bg); color:var(--oto-fg);
  border:1px solid var(--oto-edge); box-shadow:var(--oto-shadow); }
@keyframes oto-in{ from{ opacity:0; transform:translateY(24px) scale(.97) } to{ opacity:1; transform:none } }

.oto__eyebrow{ display:inline-block; font-family:var(--nfm-font-h); font-size:.66rem; font-weight:700;
  letter-spacing:.16em; text-transform:uppercase; color:var(--nfm-orange);
  border:1px solid rgba(255,102,2,.35); border-radius:50px; padding:6px 15px; margin:0 0 14px; }
.oto__box h2{ font-family:var(--nfm-font-h); font-size:clamp(1.35rem,3.2vw,1.8rem); font-weight:700;
  line-height:1.2; letter-spacing:-.02em; margin:0 0 10px; color:var(--oto-fg); }
.oto__box h2 em{ font-style:normal; color:var(--nfm-orange); }
.oto__lead{ font-size:.97rem; color:var(--oto-muted); line-height:1.55; margin:0 auto 22px; max-width:40em; }
.oto__lead strong{ color:var(--oto-fg); font-weight:600; }

/* ── las dos tarjetas ── */
.oto__packs{ display:grid; grid-template-columns:1fr 1fr; gap:16px; text-align:left; }
.oto__pack{ position:relative; display:flex; flex-direction:column; padding:24px 22px 22px;
  border-radius:var(--nfm-r-lg); background:var(--oto-card); border:1px solid var(--oto-card-edge);
  transition:transform .25s var(--nfm-ease), border-color .25s var(--nfm-ease), box-shadow .25s var(--nfm-ease); }
.oto__pack:hover{ transform:translateY(-3px); border-color:rgba(255,102,2,.4); }
.oto__pack--hot{ border-color:rgba(255,102,2,.45); background:var(--oto-card-hot);
  box-shadow:0 18px 46px rgba(255,102,2,.14); }
.oto__badge{ position:absolute; top:0; left:50%; transform:translate(-50%,-50%);
  background:var(--nfm-orange); color:#fff; white-space:nowrap;
  font-family:var(--nfm-font-h); font-size:.6rem; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; padding:7px 15px; border-radius:50px;
  box-shadow:0 8px 22px var(--nfm-orange-glow); }
.oto__name{ font-family:var(--nfm-font-h); font-size:.68rem; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color:var(--oto-muted); margin:0 0 8px; }
.oto__pack--hot .oto__name{ color:var(--nfm-orange); }
.oto__price{ font-family:var(--nfm-font-h); font-size:2.1rem; font-weight:700; line-height:1;
  letter-spacing:-.03em; color:var(--oto-fg); margin:0 0 16px; }
.oto__price span{ font-size:.9rem; font-weight:600; color:var(--oto-muted); letter-spacing:0; }
.oto__list{ list-style:none; padding:0; margin:0 0 20px; flex:1; }
.oto__list li{ position:relative; padding:0 0 11px 24px; font-size:.9rem; line-height:1.55;
  color:var(--oto-muted); }
.oto__list li:last-child{ padding-bottom:0; }
.oto__list li::before{ content:''; position:absolute; left:0; top:7px; width:14px; height:8px;
  border-left:2px solid var(--nfm-orange); border-bottom:2px solid var(--nfm-orange);
  transform:rotate(-45deg); border-radius:1px; }
.oto__list b{ color:var(--oto-fg); font-weight:600; }
.oto__list em{ font-style:normal; color:var(--oto-fg); font-weight:600; }

.oto__cta{ display:block; width:100%; text-align:center; cursor:pointer;
  font-family:var(--nfm-font-h); font-size:1rem; font-weight:700; border-radius:50px;
  padding:15px 20px; border:none; transition:transform .22s var(--nfm-ease), box-shadow .22s var(--nfm-ease), background .22s var(--nfm-ease); }
.oto__cta--ghost{ background:transparent; color:var(--oto-fg); border:1.5px solid var(--oto-ghost-edge); }
.oto__cta--ghost:hover{ border-color:var(--nfm-orange); color:var(--nfm-orange); transform:translateY(-2px); }
.oto__cta--full{ background:var(--nfm-orange); color:#fff; box-shadow:0 10px 30px var(--nfm-orange-glow); }
.oto__cta--full:hover{ background:var(--nfm-orange-hover); transform:translateY(-2px);
  box-shadow:0 14px 38px var(--nfm-orange-glow); }

/* El pie se queda pegado al fondo de la caja. Con listas largas o pantallas
   bajas, el contenido scrollea por detrás pero la salida nunca se esconde:
   quitarle la X al pop-up no es lo mismo que esconder la puerta. */
.oto__foot{ position:sticky; bottom:0; margin:0 -34px; padding:16px 34px 20px;
  background:var(--oto-foot); border-top:1px solid var(--oto-card-edge); }
.oto__pay{ font-size:.78rem; color:var(--oto-faint); margin:0; line-height:1.5; }

/* ── la salida, deliberadamente apagada ── */
.oto__no{ display:inline-block; margin:10px 0 0; padding:6px 4px; background:none; border:none;
  font-family:var(--nfm-font-b); font-size:.84rem; color:var(--oto-faint);
  text-decoration:underline; text-underline-offset:3px; cursor:pointer; line-height:1.5; }
.oto__no:hover{ color:var(--oto-muted); }

@media (max-width:720px){
  .oto{ padding:12px; align-items:flex-start; }
  .oto__box{ padding:26px 18px 0; max-height:96vh; margin:8px 0; }
  .oto__foot{ margin:0 -18px; padding:14px 18px 18px; }
  /* En celular las tarjetas se apilan, y apiladas el de USD 5 quedaba abajo
     del pliegue: había que scrollear adentro del pop-up para encontrar el que
     queremos vender. Se invierte el orden — el recomendado va primero. */
  .oto__packs{ grid-template-columns:1fr; gap:28px; padding-top:14px; }
  .oto__pack--hot{ order:-1; }
  .oto__pack{ padding:24px 20px 22px; }
  .oto__price{ font-size:2rem; }
  /* Cabecera más compacta: en celular cada línea del encabezado es una línea
     menos de la tarjeta que queremos que se vea. */
  .oto__eyebrow{ margin-bottom:12px; }
  .oto__box h2{ font-size:1.24rem; line-height:1.26; }
  .oto__lead{ font-size:.9rem; margin-bottom:18px; }
  .oto__list li{ font-size:.88rem; }
}
@media (prefers-reduced-motion:reduce){
  .oto__box{ animation:none; }
  .oto__pack:hover, .oto__cta:hover{ transform:none; }
}
"""

TEMAS = {
 'navy': """
/* ── Tema NAVY · la caja es una pieza más del sistema oscuro ── */
.oto{ --oto-bg:linear-gradient(180deg,#123category 0%,#0B2942 100%);
  --oto-fg:#fff; --oto-muted:rgba(255,255,255,.66); --oto-faint:rgba(255,255,255,.42);
  --oto-edge:rgba(255,255,255,.10); --oto-shadow:0 40px 110px rgba(0,0,0,.6);
  --oto-card:rgba(255,255,255,.04); --oto-card-edge:rgba(255,255,255,.09);
  --oto-card-hot:rgba(255,102,2,.07); --oto-ghost-edge:rgba(255,255,255,.28);
  --oto-foot:#0B2942; }
""".replace('#123category', '#143A5C'),
 'blanco': """
/* ── Tema BLANCO · la caja corta con la página y se lee como un documento ── */
.oto{ --oto-bg:radial-gradient(620px 280px at 50% 0%, rgba(255,102,2,.06), transparent 70%), #fff;
  --oto-fg:#0C3452; --oto-muted:#51647A; --oto-faint:#8A98A8;
  --oto-edge:rgba(12,52,82,.10); --oto-shadow:0 40px 110px rgba(0,0,0,.5);
  --oto-card:#F5F8FB; --oto-card-edge:#E2E8F0;
  --oto-card-hot:#FFF7F2; --oto-ghost-edge:rgba(12,52,82,.22);
  --oto-foot:#fff; }
"""}

# ══════════════════════════════════════════════════════════════════════════
#  HTML del pop-up
# ══════════════════════════════════════════════════════════════════════════
HTML = """
  <!-- ═══════════ OTO · pop-up de la oferta única ═══════════ -->
  <div class="oto" id="oto" role="dialog" aria-modal="true" aria-labelledby="oto-t">
    <div class="oto__box">

      <span class="oto__eyebrow">Sólo aparece esta vez</span>
      <h2 id="oto-t">Tu lugar ya está reservado.<br>Antes de entrar al grupo, <em>elegí cómo la querés hacer.</em></h2>
      <p class="oto__lead">Esto es opcional y <strong>no vuelve a aparecer</strong>. La clase gratis la tenés igual, elijas lo que elijas.</p>

      <div class="oto__packs">

        <!-- USD 1 -->
        <div class="oto__pack">
          <p class="oto__name">Pack básico</p>
          <p class="oto__price">USD 1</p>
          <ul class="oto__list">
            <li><b>Workbook con el resumen de la clase</b> y los accionables concretos, para que no dependas de tus apuntes.</li>
            <li><b>La grabación, tuya para siempre.</b> Si ese día se te cruza algo, la ves después.</li>
          </ul>
          <button class="oto__cta oto__cta--ghost" data-oto-buy="1">Lo quiero por USD 1</button>
        </div>

        <!-- USD 5 -->
        <div class="oto__pack oto__pack--hot">
          <span class="oto__badge">Recomendado</span>
          <p class="oto__name">Pack Hackea tu Productividad</p>
          <p class="oto__price">USD 5</p>
          <ul class="oto__list">
            <li><b>Todo lo del pack básico</b> — workbook y grabación de la clase.</li>
            <li><b>Clase privada en vivo · <span data-oto-fecha>lunes 14 de septiembre</span>, <span data-oto-hora>19:00</span> hs (Argentina) · 2 horas.</b><br>
                <em>«Domina tus funciones ejecutivas para bajar el estrés y rendir mejor»</em>, con Nicolás Fernández Miranda y Soledad Funes, psicóloga experta en TDA/H.</li>
            <li>Workbook, grabación y <b>material de apoyo</b> de esa clase.</li>
            <li>Videos: <b>cómo armar una rutina</b> que cuide tu salud mental y tu cerebro.</li>
          </ul>
          <button class="oto__cta oto__cta--full" data-oto-buy="5">Lo quiero por USD 5</button>
        </div>

      </div>

      <div class="oto__foot">
        <p class="oto__pay">Pago seguro con Stripe o Mercado Pago. El acceso te llega al mail en el momento.</p>
        <button class="oto__no" data-oto-no>Solo quiero unirme a la clase gratis, sin la grabación y sin el workbook.</button>
      </div>

    </div>
  </div>
"""

# ══════════════════════════════════════════════════════════════════════════
#  JS del pop-up
# ══════════════════════════════════════════════════════════════════════════
JS = """
<script>
/* ════════════════════════════════════════════════════════════════════════
   OTO · el pop-up de la thank you
   ────────────────────────────────────────────────────────────────────────
   Se muestra una sola vez por sesión y sólo se cierra por una de las tres
   salidas: comprar el de 1, comprar el de 5, o el link gris. No hay X, no
   cierra clickeando afuera y Escape no hace nada — es una decisión, no un
   banner. Para volver a verlo mientras se prueba: agregar ?oto=1 a la URL.
   ════════════════════════════════════════════════════════════════════════ */
(function(){
'use strict';

var OTO = {
  /* La clase privada. Va a mano porque no es la clase semanal: si se mueve,
     se cambia acá y en ningún otro lado. */
  PRIVADA: { fecha:'2026-09-14', hora:'19:00' },

  /* Links de checkout. Reemplazar por los de Stripe / Mercado Pago. */
  LINKS: { '1':'{{CHECKOUT_1}}', '5':'{{CHECKOUT_5}}' },

  DELAY: 900,          /* que la página pinte antes de taparla */
  CLAVE: 'nfm_oto_visto'
};

var DIAS  = ['domingo','lunes','martes','miércoles','jueves','viernes','sábado'];
var MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
             'septiembre','octubre','noviembre','diciembre'];

var box = document.getElementById('oto');
if(!box) return;

function forzado(){ return /[?&]oto=1/.test(window.location.search); }
function visto(){ try{ return sessionStorage.getItem(OTO.CLAVE) === '1'; }catch(e){ return false; } }
function marcar(){ try{ sessionStorage.setItem(OTO.CLAVE,'1'); }catch(e){} }
function track(ev,d){ try{ if(window.fbq) fbq('track',ev,d||{}); }catch(e){} }

/* — la fecha de la clase privada, escrita — */
(function(){
  var p = OTO.PRIVADA.fecha.split('-');
  /* mediodía UTC: así el día no se corre por zona horaria */
  var d = new Date(Date.UTC(+p[0], +p[1]-1, +p[2], 12));
  var txt = DIAS[d.getUTCDay()] + ' ' + d.getUTCDate() + ' de ' + MESES[d.getUTCMonth()];
  var e = box.querySelector('[data-oto-fecha]'); if(e) e.textContent = txt;
  var h = box.querySelector('[data-oto-hora]');  if(h) h.textContent = OTO.PRIVADA.hora;
})();

function abrir(){
  box.setAttribute('data-open','');
  document.body.setAttribute('data-oto-open','');
  track('ViewContent', {content_name:'oto_thankyou'});
  var f = box.querySelector('[data-oto-buy="5"]');
  if(f) try{ f.focus({preventScroll:true}); }catch(e){ f.focus(); }
}
function cerrar(){
  box.removeAttribute('data-open');
  document.body.removeAttribute('data-oto-open');
  marcar();
}

/* Comprar. El link se abre en la misma pestaña: la compra es el paso
   siguiente, no una rama paralela. Si el token no está reemplazado, no se
   navega a ningún lado — mejor que mandar a una URL rota. */
var botones = box.querySelectorAll('[data-oto-buy]');
for(var i=0;i<botones.length;i++){
  botones[i].addEventListener('click', function(){
    var pack = this.getAttribute('data-oto-buy');
    var url  = OTO.LINKS[pack] || '';
    track('InitiateCheckout', {content_name:'oto_pack_'+pack, value:+pack, currency:'USD'});
    marcar();
    if(/^\\{\\{/.test(url) || !url){
      if(window.console && console.warn) console.warn('[NFM] Falta el link de checkout del pack de USD '+pack);
      return;
    }
    window.location.href = url;
  });
}

/* La salida */
var no = box.querySelector('[data-oto-no]');
if(no) no.addEventListener('click', function(){
  track('Lead', {content_name:'oto_rechazado'});
  cerrar();
});

/* Sin X, sin click afuera, sin Escape. Y el foco no se escapa de la caja
   mientras está abierta: con lector de pantalla o con Tab, las opciones
   siguen siendo las mismas tres. */
box.addEventListener('click', function(e){ e.stopPropagation(); });
document.addEventListener('keydown', function(e){
  if(!box.hasAttribute('data-open')) return;
  if(e.key === 'Escape'){ e.preventDefault(); return; }
  if(e.key !== 'Tab') return;
  var f = box.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  if(!f.length) return;
  var primero = f[0], ultimo = f[f.length-1];
  if(e.shiftKey && document.activeElement === primero){ e.preventDefault(); ultimo.focus(); }
  else if(!e.shiftKey && document.activeElement === ultimo){ e.preventDefault(); primero.focus(); }
}, true);

if(forzado() || !visto()) setTimeout(abrir, OTO.DELAY);
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════════════
#  Montaje
# ══════════════════════════════════════════════════════════════════════════
for tema, css_tema in TEMAS.items():
    out = s
    assert out.count('</style>\n\n\n<div class="nfm-thx">') == 1
    out = out.replace('</style>\n\n\n<div class="nfm-thx">',
                      CSS_COMUN + css_tema + '</style>\n\n\n<div class="nfm-thx">')
    assert out.count('</div><!-- /.nfm-thx -->') == 1
    out = out.replace('</div><!-- /.nfm-thx -->', '</div><!-- /.nfm-thx -->\n' + HTML)
    assert out.count('<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->') == 1
    out = out.replace('<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->',
                      JS + '<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->')
    dst = 'nfm-clase-paga/thankyou-oto-%s.html' % tema
    io.open(dst,'w',encoding='utf-8').write(out)
    print('escrito', dst, len(out))
