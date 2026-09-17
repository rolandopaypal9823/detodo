# -*- coding: utf-8 -*-
"""Arma la thank you page con el pop-up del OTO.

   Entra  : nfm-clase-paga/thankyou-base.html  (la thank you que ya está al aire)
   Sale   : nfm-clase-paga/thankyou-oto.html

   La base no se toca: el pop-up se inyecta en tres puntos marcados, así que
   cuando cambie la thank you alcanza con reemplazar la base y volver a correr
   esto. Correr desde la raíz del repo:  python3 nfm-clase-paga/gen-thankyou-oto.py
"""
import io

BASE = 'nfm-clase-paga/thankyou-base.html'
DST  = 'nfm-clase-paga/thankyou-oto.html'

# ══════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════
CSS = """
/* ════════════════════════════════════════════════════════════════
   OTO · el pop-up de la oferta única
   No tiene X y no se cierra clickeando afuera ni con Escape: las
   únicas tres salidas son los dos botones de pago y el link gris de
   abajo. Eso es a propósito — es una decisión, no un banner.
   ════════════════════════════════════════════════════════════════ */
.oto{ position:fixed; inset:0; z-index:99999;
  display:flex; align-items:center; justify-content:center; padding:20px;
  background:rgba(4,14,24,.88); -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px);
  /* Oculto con visibility y no con display:none, a propósito: los botones de
     Stripe viven dentro de un iframe y necesitan que el nodo tenga layout para
     medirse. Con display:none aparecen con 0 de alto la primera vez. */
  visibility:hidden; opacity:0; pointer-events:none;
  transition:opacity .32s var(--nfm-ease), visibility 0s .32s; }
.oto[data-open]{ visibility:visible; opacity:1; pointer-events:auto;
  transition:opacity .32s var(--nfm-ease); }
.oto *, .oto *::before, .oto *::after{ box-sizing:border-box; }
body[data-oto-open]{ overflow:hidden; }

.oto__box{ width:100%; max-width:860px; max-height:92vh; overflow-y:auto;
  border-radius:var(--nfm-r-lg); padding:30px 34px 0;
  font-family:var(--nfm-font-b); text-align:center; color:#fff;
  background:linear-gradient(180deg,#143A5C 0%,#0B2942 100%);
  border:1px solid rgba(255,255,255,.10); box-shadow:0 40px 110px rgba(0,0,0,.6); }
.oto[data-open] .oto__box{ animation:oto-in .42s var(--nfm-ease) both; }
@keyframes oto-in{ from{ opacity:0; transform:translateY(22px) scale(.975) } to{ opacity:1; transform:none } }

.oto__eyebrow{ display:inline-block; font-family:var(--nfm-font-h); font-size:.66rem; font-weight:700;
  letter-spacing:.16em; text-transform:uppercase; color:var(--nfm-orange);
  border:1px solid rgba(255,102,2,.35); border-radius:50px; padding:6px 15px; margin:0 0 14px; }
.oto__box h2{ font-family:var(--nfm-font-h); font-size:clamp(1.35rem,3.2vw,1.8rem); font-weight:700;
  line-height:1.2; letter-spacing:-.02em; margin:0 0 10px; color:#fff; }
.oto__box h2 em{ font-style:normal; color:var(--nfm-orange); }
.oto__lead{ font-size:.97rem; color:rgba(255,255,255,.66); line-height:1.55; margin:0 auto 22px; max-width:40em; }
.oto__lead strong{ color:#fff; font-weight:600; }

/* ── las dos tarjetas ── */
.oto__packs{ display:grid; grid-template-columns:1fr 1fr; gap:16px; text-align:left; }
.oto__pack{ position:relative; display:flex; flex-direction:column; padding:24px 22px 22px;
  border-radius:var(--nfm-r-lg); background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.09);
  transition:transform .25s var(--nfm-ease), border-color .25s var(--nfm-ease); }
.oto__pack:hover{ transform:translateY(-3px); border-color:rgba(255,102,2,.4); }
.oto__pack--hot{ border-color:rgba(255,102,2,.45); background:rgba(255,102,2,.07);
  box-shadow:0 18px 46px rgba(255,102,2,.14); }
.oto__badge{ position:absolute; top:0; left:50%; transform:translate(-50%,-50%);
  background:var(--nfm-orange); color:#fff; white-space:nowrap;
  font-family:var(--nfm-font-h); font-size:.6rem; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; padding:7px 15px; border-radius:50px;
  box-shadow:0 8px 22px var(--nfm-orange-glow); }
.oto__name{ font-family:var(--nfm-font-h); font-size:.66rem; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color:rgba(255,255,255,.66); margin:0 0 8px; line-height:1.5; }
.oto__pack--hot .oto__name{ color:var(--nfm-orange); }
.oto__price{ font-family:var(--nfm-font-h); font-size:2.1rem; font-weight:700; line-height:1;
  letter-spacing:-.03em; color:#fff; margin:0 0 16px; }
.oto__list{ list-style:none; padding:0; margin:0 0 20px; flex:1; }
.oto__list li{ position:relative; padding:0 0 11px 24px; font-size:.9rem; line-height:1.55;
  color:rgba(255,255,255,.66); }
.oto__list li:last-child{ padding-bottom:0; }
.oto__list li::before{ content:''; position:absolute; left:0; top:6px; width:13px; height:7px;
  border-left:2px solid var(--nfm-orange); border-bottom:2px solid var(--nfm-orange);
  transform:rotate(-45deg); border-radius:1px; }
.oto__list b{ color:#fff; font-weight:600; }

/* ── el botón de Stripe ──
   Se dibuja adentro de un iframe propio, así que su color y su texto se
   configuran en el panel de Stripe, no acá. Lo único que controlamos es el
   hueco: se reserva el alto para que la tarjeta no salte cuando carga. */
.oto__buy{ min-height:52px; display:flex; flex-direction:column; justify-content:center; }
.oto__buy stripe-buy-button{ display:block; width:100%; }
.oto__buyerr{ display:none; font-size:.8rem; line-height:1.5; text-align:center;
  color:rgba(255,255,255,.42); margin:0; }
.oto__buy[data-fallo] .oto__buyerr{ display:block; }

/* ── el pie: pago + la salida ──
   Queda pegado abajo de la caja. Con listas largas o pantallas bajas el
   contenido scrollea por detrás, pero la salida nunca se esconde: quitarle
   la X al pop-up no es lo mismo que esconder la puerta. */
.oto__foot{ position:sticky; bottom:0; margin:0 -34px; padding:16px 34px 20px;
  background:#0B2942; border-top:1px solid rgba(255,255,255,.09); }
.oto__pay{ font-size:.78rem; color:rgba(255,255,255,.42); margin:0; line-height:1.5; }
.oto__no{ display:inline-block; margin:10px 0 0; padding:6px 4px; background:none; border:none;
  font-family:var(--nfm-font-b); font-size:.84rem; color:rgba(255,255,255,.42);
  text-decoration:underline; text-underline-offset:3px; cursor:pointer; line-height:1.5; }
.oto__no:hover{ color:rgba(255,255,255,.66); }

@media (max-width:720px){
  .oto{ padding:12px; align-items:flex-start; }
  .oto__box{ padding:26px 18px 0; max-height:96vh; margin:8px 0; }
  .oto__foot{ margin:0 -18px; padding:14px 18px 18px; }
  /* Apiladas, el de USD 5 caía debajo del pliegue: había que scrollear adentro
     del pop-up para encontrar el que queremos vender. Va primero. */
  .oto__packs{ grid-template-columns:1fr; gap:28px; padding-top:14px; }
  .oto__pack--hot{ order:-1; }
  .oto__pack{ padding:24px 20px 22px; }
  .oto__price{ font-size:2rem; }
  .oto__eyebrow{ margin-bottom:12px; }
  .oto__box h2{ font-size:1.24rem; line-height:1.26; }
  .oto__lead{ font-size:.9rem; margin-bottom:18px; }
  .oto__list li{ font-size:.88rem; }
}
@media (prefers-reduced-motion:reduce){
  .oto, .oto[data-open] .oto__box{ transition:none; animation:none; }
  .oto__pack:hover{ transform:none; }
}
"""

# ══════════════════════════════════════════════════════════════════════════
#  HTML
# ══════════════════════════════════════════════════════════════════════════
HTML = """
  <!-- ═══════════ OTO · pop-up de la oferta única ═══════════ -->
  <div class="oto" id="oto" role="dialog" aria-modal="true" aria-labelledby="oto-t" aria-hidden="true">
    <div class="oto__box">

      <span class="oto__eyebrow">Sólo aparece esta vez</span>
      <h2 id="oto-t">Tu lugar ya está reservado.<br>Antes de entrar al grupo, <em>elegí con qué asiento la hacés.</em></h2>
      <p class="oto__lead">Esto es opcional y <strong>no vuelve a aparecer</strong>. La clase gratis la tenés igual, elijas lo que elijas.</p>

      <div class="oto__packs">

        <!-- USD 1 -->
        <div class="oto__pack">
          <p class="oto__name">Asiento Premium Básico</p>
          <p class="oto__price">USD 1</p>
          <ul class="oto__list">
            <li><b>Workbook con el resumen de la clase</b> y los accionables concretos, para que no dependas de tus apuntes.</li>
            <li><b>La grabación, tuya para siempre.</b> Si ese día se te cruza algo, la ves después.</li>
          </ul>
          <div class="oto__buy" data-oto-buy="1">
            <stripe-buy-button
              buy-button-id="{{BTN_1}}"
              publishable-key="{{PK}}">
            </stripe-buy-button>
            <p class="oto__buyerr">No se pudo cargar el botón de pago. Recargá la página e intentá de nuevo.</p>
          </div>
        </div>

        <!-- USD 5 -->
        <div class="oto__pack oto__pack--hot">
          <span class="oto__badge">Recomendado</span>
          <p class="oto__name">Asiento Premium · Hackea tu Productividad</p>
          <p class="oto__price">USD 5</p>
          <ul class="oto__list">
            <li><b>Todo lo del Básico</b> — workbook y grabación de la clase.</li>
            <li><b>Sesión de 60 minutos de preguntas y respuestas</b> con Nicolás Fernández Miranda y Soledad Funes, psicóloga experta en TDA/H. <b>Tenés a los dos expertos ahí</b> para contestar preguntas sobre tu caso.</li>
            <li><b>Workbook, grabación y material de apoyo</b> de esa sesión.</li>
          </ul>
          <div class="oto__buy" data-oto-buy="5">
            <stripe-buy-button
              buy-button-id="{{BTN_5}}"
              publishable-key="{{PK}}">
            </stripe-buy-button>
            <p class="oto__buyerr">No se pudo cargar el botón de pago. Recargá la página e intentá de nuevo.</p>
          </div>
        </div>

      </div>

      <div class="oto__foot">
        <p class="oto__pay">Pago seguro con Stripe. El acceso te llega al mail en el momento.</p>
        <button class="oto__no" data-oto-no>Solo quiero unirme a la clase gratis, sin la grabación y sin el workbook.</button>
      </div>

    </div>
  </div>
"""

# ══════════════════════════════════════════════════════════════════════════
#  JS
# ══════════════════════════════════════════════════════════════════════════
JS = """
<!-- Stripe Buy Button · dibuja los dos botones de pago del pop-up -->
<script async src="https://js.stripe.com/v3/buy-button.js"></script>

<script>
/* ════════════════════════════════════════════════════════════════════════
   OTO · el pop-up de la thank you
   ────────────────────────────────────────────────────────────────────────
   Se muestra una vez por sesión y se cierra por una de tres salidas: pagar
   el Básico, pagar el de Hackea tu Productividad, o el link gris. No hay X,
   no cierra clickeando afuera y Escape no hace nada. Para volver a verlo
   mientras se prueba: agregar ?oto=1 a la URL.

   ⚠️ Los botones de pago son de Stripe y viven adentro de un iframe propio:
      el clic NO llega hasta acá, así que el evento Purchase lo tiene que
      mandar la página de gracias de cada compra, no esta página.
   ════════════════════════════════════════════════════════════════════════ */
(function(){
'use strict';

var OTO = {
  DELAY: 900,                    /* que la página pinte antes de taparla */
  CLAVE: 'nfm_oto_visto',
  ESPERA_STRIPE: 7000            /* si en 7s no cargó, se avisa en vez de dejar el hueco vacío */
};

var box = document.getElementById('oto');
if(!box) return;

function forzado(){ return /[?&]oto=1/.test(window.location.search); }
function visto(){ try{ return sessionStorage.getItem(OTO.CLAVE) === '1'; }catch(e){ return false; } }
function marcar(){ try{ sessionStorage.setItem(OTO.CLAVE,'1'); }catch(e){} }
function track(ev,d){ try{ if(window.fbq) fbq('track',ev,d||{}); }catch(e){} }

function abrir(){
  box.setAttribute('data-open','');
  box.removeAttribute('aria-hidden');
  document.body.setAttribute('data-oto-open','');
  track('ViewContent', {content_name:'oto_thankyou'});
}
function cerrar(){
  box.removeAttribute('data-open');
  box.setAttribute('aria-hidden','true');
  document.body.removeAttribute('data-oto-open');
  marcar();
}

/* Acá NO hay un listener sobre los botones de pago, y no es un olvido: el
   botón de Stripe se dibuja adentro de un iframe, y ni el clic ni el
   pointerdown salen de ahí. Tampoco hace falta — al pagar, Stripe se lleva a
   la persona a su checkout. Si vuelve con el botón Atrás sin haber pagado, el
   pop-up le aparece de nuevo, que es lo que queremos. */

/* La salida */
var no = box.querySelector('[data-oto-no]');
if(no) no.addEventListener('click', function(){
  track('Lead', {content_name:'oto_rechazado'});
  cerrar();
});

/* Sin X, sin click afuera, sin Escape. Y el foco no se escapa de la caja
   mientras está abierta: con teclado o con lector de pantalla las opciones
   siguen siendo las mismas tres. */
box.addEventListener('click', function(e){ e.stopPropagation(); });
document.addEventListener('keydown', function(e){
  if(!box.hasAttribute('data-open')) return;
  if(e.key === 'Escape'){ e.preventDefault(); return; }
  if(e.key !== 'Tab') return;
  var f = box.querySelectorAll('button, [href], input, select, textarea, stripe-buy-button, [tabindex]:not([tabindex="-1"])');
  if(!f.length) return;
  var primero = f[0], ultimo = f[f.length-1];
  if(e.shiftKey && document.activeElement === primero){ e.preventDefault(); ultimo.focus(); }
  else if(!e.shiftKey && document.activeElement === ultimo){ e.preventDefault(); primero.focus(); }
}, true);

/* Si Stripe no carga (bloqueador, red caída, script caído), el hueco queda
   vacío y la persona no entiende por qué no puede pagar. Se avisa. */
if(window.customElements && customElements.whenDefined){
  var listo = false;
  customElements.whenDefined('stripe-buy-button').then(function(){ listo = true; });
  setTimeout(function(){
    if(listo) return;
    var h = box.querySelectorAll('.oto__buy');
    for(var j=0;j<h.length;j++) h[j].setAttribute('data-fallo','');
  }, OTO.ESPERA_STRIPE);
}

if(forzado() || !visto()) setTimeout(abrir, OTO.DELAY);
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════════════
#  Stripe · IDs de los botones
#  ⚠️ ESTO ES PLATA REAL: la clave es pk_live. Si los dos IDs quedan
#     cruzados, el Básico cobra 5 y el otro cobra 1. Confirmar contra el
#     panel de Stripe antes de publicar — es lo único que hay que mirar acá.
# ══════════════════════════════════════════════════════════════════════════
STRIPE = {
  'PK'    : 'pk_live_51QoqTa4EXY0lpTArqfyGuVkqUNbebcUt7y7KvitbwxsqAs2IxR7aL9jKsiFnyHnvHGqT8hsK81iiz5ZADFP2TNsL00Ci0loiug',
  'BTN_1' : 'buy_btn_1UFhJo4EXY0lpTArVIiU2xPY',   # Asiento Premium Básico · USD 1
  'BTN_5' : 'buy_btn_1UFhOE4EXY0lpTArJSRUYiGI',   # Asiento Premium Hackea tu Productividad · USD 5
}

# ══════════════════════════════════════════════════════════════════════════
#  Montaje
# ══════════════════════════════════════════════════════════════════════════
def main():
    s = io.open(BASE, encoding='utf-8').read()

    anclas = [
      ('</style>\n\n\n<div class="nfm-thx">',  CSS + '</style>\n\n\n<div class="nfm-thx">'),
      ('</div><!-- /.nfm-thx -->',             '</div><!-- /.nfm-thx -->\n' + HTML),
      ('<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->',
       JS + '<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->'),
    ]
    for viejo, nuevo in anclas:
        if s.count(viejo) != 1:
            raise SystemExit('Ancla que no aparece exactamente una vez en la base: ' + viejo[:60])
        s = s.replace(viejo, nuevo)

    for k, v in STRIPE.items():
        s = s.replace('{{' + k + '}}', v)

    sobran = [t for t in ('{{PK}}','{{BTN_1}}','{{BTN_5}}') if t in s]
    if sobran:
        raise SystemExit('Quedaron tokens sin reemplazar: ' + ', '.join(sobran))

    io.open(DST, 'w', encoding='utf-8').write(s)
    print('escrito', DST, len(s), 'bytes')

main()
