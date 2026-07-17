# -*- coding: utf-8 -*-
"""Injerta el componente 'Chat con Nico' en la landing existente.

Entrada:  landing.html   (la landing original, sin tocar)
Salida:   index.html      (landing + chat, lista para publicar)

Por qué un injector y no editar a mano: si actualizás la landing, reemplazás
landing.html y volvés a correr  python3 inject_chat.py  para re-injertar el chat.

El chat usa los MISMOS tokens de la landing (--ink, --orange, --hairline, etc.),
así que queda nativo. No colisiona con clases existentes (verificado).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "landing.html")
OUT = os.path.join(HERE, "index.html")

# ------------------------------------------------------------------ CSS
CHAT_CSS = r"""
/* ===================== NOTIFICACIÓN iPhone + CHAT NICO (injertado) ===================== */
.nc-push{position:fixed;top:14px;left:50%;transform:translate(-50%,-160%);z-index:96;width:min(400px,calc(100vw - 24px));background:rgba(255,255,255,.94);backdrop-filter:blur(20px) saturate(160%);-webkit-backdrop-filter:blur(20px) saturate(160%);border:1px solid rgba(12,52,82,.08);border-radius:22px;box-shadow:0 18px 50px rgba(12,52,82,.22);padding:13px 16px;display:flex;gap:12px;align-items:center;cursor:pointer;transition:transform .55s var(--ease)}
.nc-push.show{transform:translate(-50%,0)}
.nc-av{width:42px;height:42px;border-radius:12px;background:var(--ink);color:#fff;font-weight:700;font-size:1.1rem;display:flex;align-items:center;justify-content:center;flex:none;font-family:'Montserrat',sans-serif;overflow:hidden}
.nc-av img{width:100%;height:100%;object-fit:cover}
.nc-tx{flex:1;min-width:0}
.nc-tx .h{display:flex;justify-content:space-between;gap:8px;font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.nc-tx b{display:block;font-size:.92rem;color:var(--ink);margin-top:1px}
.nc-tx small{font-size:.85rem;color:var(--body);display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nc-chat{position:fixed;right:18px;bottom:88px;z-index:96;width:min(380px,calc(100vw - 24px));max-height:min(560px,72vh);background:var(--canvas);border:1px solid var(--hairline);border-radius:24px;box-shadow:var(--shadow-elevated);display:none;flex-direction:column;overflow:hidden}
.nc-chat.open{display:flex;animation:ncpop .4s var(--ease)}
@keyframes ncpop{from{transform:scale(.92);opacity:0}to{transform:none;opacity:1}}
@media(max-width:560px){.nc-chat{right:0;left:0;bottom:0;width:100%;border-radius:24px 24px 0 0;max-height:80vh}}
.nc-head{display:flex;align-items:center;gap:11px;padding:14px 16px;background:var(--ink);color:#fff}
.nc-head .av{width:38px;height:38px;border-radius:50%;background:#fff;color:var(--ink);font-family:'Montserrat',sans-serif;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;overflow:hidden}
.nc-head .av img{width:100%;height:100%;object-fit:cover}
.nc-head b{font-size:.98rem;color:#fff}
.nc-head small{display:block;font-size:.72rem;opacity:.9;color:#fff}
.nc-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#8FF0A6;box-shadow:0 0 0 2px rgba(143,240,166,.35);margin-right:6px;vertical-align:middle}
.nc-head button{margin-left:auto;background:none;border:none;color:#fff;font-size:1.2rem;cursor:pointer;padding:4px 8px;line-height:1}
.nc-body{flex:1;overflow-y:auto;padding:18px 16px;display:flex;flex-direction:column;gap:10px;background:var(--surface-soft)}
.nc-msg{max-width:86%;padding:11px 15px;border-radius:18px;font-size:.92rem;line-height:1.5;animation:ncmsgin .35s var(--ease)}
@keyframes ncmsgin{from{transform:translateY(8px);opacity:0}to{transform:none;opacity:1}}
.nc-msg.nico{background:var(--canvas);border:1px solid var(--hairline);color:var(--body);border-bottom-left-radius:6px;align-self:flex-start}
.nc-msg.nico b{color:var(--ink)}
.nc-msg.me{background:var(--orange);color:#fff;border-bottom-right-radius:6px;align-self:flex-end}
.nc-msg.me b{color:#fff}
.nc-typing{align-self:flex-start;background:var(--canvas);border:1px solid var(--hairline);border-radius:18px;border-bottom-left-radius:6px;padding:13px 16px;display:flex;gap:5px}
.nc-typing i{width:7px;height:7px;border-radius:50%;background:var(--muted);animation:nctp 1.2s infinite}
.nc-typing i:nth-child(2){animation-delay:.18s}.nc-typing i:nth-child(3){animation-delay:.36s}
@keyframes nctp{0%,60%,100%{opacity:.3;transform:none}30%{opacity:1;transform:translateY(-3px)}}
.nc-opts{padding:12px 14px;border-top:1px solid var(--hairline);display:flex;flex-wrap:wrap;gap:8px;background:var(--canvas)}
.nc-opts button{background:var(--orange-soft);border:1px solid rgba(255,102,2,.35);color:var(--orange-hover);border-radius:999px;padding:10px 18px;font-family:'Open Sans',sans-serif;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s}
.nc-opts button:hover{background:var(--orange);color:#fff}
@keyframes ncPageShake{0%,100%{transform:translate3d(0,0,0)}15%{transform:translate3d(-7px,2px,0)}30%{transform:translate3d(7px,-2px,0)}45%{transform:translate3d(-5px,1px,0)}60%{transform:translate3d(5px,-1px,0)}75%{transform:translate3d(-3px,1px,0)}90%{transform:translate3d(3px,0,0)}}
body.nc-shake{animation:ncPageShake .5s cubic-bezier(.36,.07,.19,.97)}
@media(prefers-reduced-motion:reduce){body.nc-shake{animation:none}.nc-push{transition:none}}
"""

# ------------------------------------------------------------------ HTML
CHAT_HTML = r"""
<!-- ===================== CHAT CON NICO (injertado) ===================== -->
<div class="nc-push" id="nc-push" role="button" aria-label="Abrir mensaje de Nico">
  <div class="nc-av" id="nc-push-av">N</div>
  <div class="nc-tx">
    <div class="h"><span>Nico · Instituto de Productividad</span><span>ahora</span></div>
    <b>Nico</b>
    <small id="nc-push-msg">¿Te puedo ser 100% honesto un segundo?</small>
  </div>
</div>
<div class="nc-chat" id="nc-chat" aria-live="polite">
  <div class="nc-head">
    <div class="av" id="nc-chat-av">N</div>
    <div>
      <b>Nico Fernández Miranda</b>
      <small><span class="nc-dot"></span>en línea ahora</small>
    </div>
    <button id="nc-close" aria-label="Cerrar chat">&times;</button>
  </div>
  <div class="nc-body" id="nc-body"></div>
  <div class="nc-opts" id="nc-opts"></div>
</div>
"""

# ------------------------------------------------------------------ JS
CHAT_JS = r"""
(function(){
  /* ═══════════ CONFIG (editá esto) ═══════════ */
  var CHECKOUT_URL = "#oferta";   // dónde manda el CTA final del chat. '#oferta' = baja a la oferta.
                                  //   Cuando tengas el link de Mercado Pago, ponelo acá (ej: "https://mpago.la/...").
  var NICO_AVATAR  = "";          // foto de Nico (URL o dataURI). Vacío = usa la inicial "N".
  var TEST_MODE    = /[?#&]test/.test(location.href);   // ?test acelera los tiempos para probar
  var CHAT_DELAY_MS = 50000;      // espera antes del primer mensaje (producción)
  /* ════════════════════════════════════════════ */

  if(NICO_AVATAR){
    var a1=document.getElementById('nc-push-av'), a2=document.getElementById('nc-chat-av');
    if(a1) a1.innerHTML='<img src="'+NICO_AVATAR+'" alt="Nico">';
    if(a2) a2.innerHTML='<img src="'+NICO_AVATAR+'" alt="Nico">';
  }

  var push=document.getElementById('nc-push'), chat=document.getElementById('nc-chat');
  var body=document.getElementById('nc-body'), opts=document.getElementById('nc-opts');
  if(!push||!chat) return;
  var pushShown=false, chatOpened=false, shakeEnabled=true;

  var PUSH_MSGS=[
    '¿Te puedo ser 100% honesto un segundo? 💬',
    '¿Estás por ahí? 👀',
    'Te dejo esto por acá antes de que te vayas 👇'
  ];
  var FOLLOWUPS=[
    'Hola, hola 👋 Soy Nico. ¿Te puedo hacer una pregunta media incómoda? 💬',
    '¿Estás por ahí? 👀',
    'Te dejo esto por acá 👇 Si sabés lo que tenés que hacer y no lo hacés, esto es para vos. ¿Le damos?'
  ];
  var STEP_GAPS = TEST_MODE ? [3000,5000,5000] : [10000,20000,8000];
  var pushStep=0;
  function modalOpen(){ return !!document.querySelector('.xpop.show, .exit-modal.show'); }
  function showPushStep(){
    if(chatOpened) return;
    if(modalOpen()){ setTimeout(showPushStep, 4000); return; }   /* no pisar los popups de la landing */
    if(pushStep>=2) shakeEnabled=false;
    var m=document.getElementById('nc-push-msg'); if(m) m.innerHTML=PUSH_MSGS[pushStep];
    push.classList.add('show'); pageShake();
    var gap=STEP_GAPS[pushStep]||8000; pushStep++;
    if(pushStep<PUSH_MSGS.length){ setTimeout(showPushStep,gap); }
    else { setTimeout(function(){ if(!chatOpened) seedAndDock(); },gap); }
  }
  function tryPush(){ if(pushShown) return; if(modalOpen()){ return setTimeout(tryPush,10000); } pushShown=true; showPushStep(); }
  setTimeout(tryPush, TEST_MODE ? 3000 : CHAT_DELAY_MS);
  window.addEventListener('scroll',function(){ if(!pushShown && window.scrollY>document.body.scrollHeight*.6) tryPush(); },{passive:true});

  push.addEventListener('click',function(){ push.classList.remove('show'); chatOpen(); });
  var closeBtn=document.getElementById('nc-close'); if(closeBtn) closeBtn.addEventListener('click',chatClose);
  function chatClose(){ chat.classList.remove('open'); }
  function chatOpen(){ shakeEnabled=false; if(chatOpened){ chat.classList.add('open'); return; } chatOpened=true; chat.classList.add('open'); step('intro'); }

  function seedAndDock(){
    if(chatOpened) return;
    chatOpened=true; push.classList.remove('show');
    FOLLOWUPS.forEach(function(txt){ var m=document.createElement('div'); m.className='nc-msg nico'; m.innerHTML=txt; body.appendChild(m); });
    body.scrollTop=1e9; chat.classList.add('open');
    buttons([{t:'Sí, dale 💛',next:'s1'},{t:'Ahora no',next:'no'}]);
  }

  var _shakeT=null;
  function pageShake(){
    if(!shakeEnabled) return;
    document.body.classList.remove('nc-shake'); void document.body.offsetWidth;
    document.body.classList.add('nc-shake');
    if(navigator.vibrate){ try{ navigator.vibrate(35); }catch(e){} }
    clearTimeout(_shakeT); _shakeT=setTimeout(function(){ document.body.classList.remove('nc-shake'); },560);
  }
  function nico(html,cb,delay){
    var t=document.createElement('div'); t.className='nc-typing'; t.innerHTML='<i></i><i></i><i></i>';
    body.appendChild(t); body.scrollTop=1e9;
    setTimeout(function(){ t.remove();
      var m=document.createElement('div'); m.className='nc-msg nico'; m.innerHTML=html;
      body.appendChild(m); body.scrollTop=1e9; pageShake(); if(cb)cb();
    }, delay||1100);
  }
  function me(text){ var m=document.createElement('div'); m.className='nc-msg me'; m.textContent=text; body.appendChild(m); body.scrollTop=1e9; }
  function buttons(list){ opts.innerHTML='';
    list.forEach(function(b){ var el=document.createElement('button'); el.textContent=b.t;
      el.onclick=function(){ me(b.t); opts.innerHTML=''; step(b.next); }; opts.appendChild(el); }); }

  /* Guion (voz de Nico): empatía → dolor → "no es fuerza de voluntad, es ciencia"
     → costo → el ebook → los 6 bonos → oferta → CTA */
  function step(id){
    if(id==='intro'){ nico('Hola, hola 👋 Soy Nico. ¿Te puedo hacer una pregunta media incómoda?', function(){ buttons([{t:'Dale',next:'s1'},{t:'Ahora no',next:'no'}]); }); }
    else if(id==='no'){ nico('Todo bien 💛 Te dejo una sola cosa: si sabés lo que tenés que hacer y no lo hacés, no te falta información… te falta un <b>sistema</b>. Cuando quieras verlo, acá estoy. Un abrazo.', function(){ buttons([{t:'Listo, contame',next:'s1'}]); }); }
    else if(id==='s1'){ nico('Va, y contestate con la mano en el corazón: ¿cuántas veces sabés <b>exactamente</b> lo que tenés que hacer… y aun así terminás scrolleando o dejándolo para después?', function(){ buttons([{t:'Uf… todo el tiempo',next:'s2'},{t:'Me pasa igual',next:'s2'}]); }); }
    else if(id==='s2'){ nico('Spoiler alert: eso no es que seas vago ni indisciplinado. Es <b>química</b>. Tu cerebro elige la recompensa fácil e inmediata (el celular) por encima de la importante. No te falta motivación — te falta entender cómo funciona tu cabeza. <b>No es motivación, es ciencia.</b>', function(){ buttons([{t:'Tal cual me pasa',next:'s3'}]); },1300); }
    else if(id==='s3'){ nico('Y mientras tanto se te va el día en distracciones, dormís peor, rendís a la mitad… y arranca la culpa. Lo peor: no es tu culpa. Las apps las diseñan <b>equipos enteros de ingenieros</b> para ganarle a tu fuerza de voluntad. El partido está armado en tu contra.', function(){ buttons([{t:'Me hace todo el sentido',next:'s4'}]); },1400); }
    else if(id==='s4'){ nico('Por eso escribí <b>Desintoxicación Digital</b>. No es «usá menos el celular». Es un <b>método paso a paso</b> para que entiendas tu dopamina y le pongas un sistema: recuperás foco, sueño y horas de tu día. Sin fuerza de voluntad heroica.', function(){ buttons([{t:'Eso es lo que necesito',next:'s5'}]); },1500); }
    else if(id==='s5'){ nico('Y no vas solo: viene con <b>6 bonos</b> que lo hacen imparable 👇<br>• Reseteo de Dopamina<br>• Bloque de Foco<br>• Masterclass: la neurociencia de la procrastinación<br>• Sueño Blindado<br>• Reto de 7 Días acompañado<br>• Canal exclusivo de WhatsApp', function(){ buttons([{t:'Lo quiero completo',next:'s6'}]); },1600); }
    else if(id==='s6'){ nico('Mirá, hoy te lo llevás <b>con los 6 bonos de regalo</b> y con <b>7 días de garantía total</b>. Es el sistema completo, no más info suelta para sumar a la pila. ¿Le damos?', function(){ buttons([{t:'Sí, lo quiero →',next:'go'},{t:'¿Y si no me sirve?',next:'g'}]); },1400); }
    else if(id==='g'){ nico('Tenés <b>7 días de garantía total</b>: lo probás, lo aplicás, y si no sentís el cambio te devuelvo el 100%. El riesgo lo corro yo, no vos.', function(){ buttons([{t:'Listo, lo quiero →',next:'go'}]); }); }
    else if(id==='go'){ nico('¡Genial! 🎉 Te llevo…', function(){ setTimeout(function(){
      chatClose();
      if(CHECKOUT_URL && CHECKOUT_URL.charAt(0)!=='#'){ window.location.href=CHECKOUT_URL; }
      else { var el=document.querySelector(CHECKOUT_URL||'#oferta'); if(el){ el.scrollIntoView({behavior:'smooth'}); } }
    },900); },700); }
  }
})();
"""


def build():
    with open(SRC, "r", encoding="utf-8") as f:
        html = f.read()

    # limpiar una injección previa (para poder re-correr)
    import re
    html = re.sub(r"\n?/\* =+ NOTIFICACIÓN iPhone \+ CHAT NICO.*?body\.nc-shake\{animation:none\}\.nc-push\{transition:none\}\}\n?",
                  "", html, flags=re.S)
    html = re.sub(r"\n?<!-- =+ CHAT CON NICO \(injertado\) =+ -->.*?</div>\n(?=</body>)",
                  "", html, flags=re.S)

    # 1) CSS antes de </style>
    idx = html.rfind("</style>")
    html = html[:idx] + CHAT_CSS + "\n" + html[idx:]

    # 2) HTML + JS antes de </body>
    idx = html.rfind("</body>")
    block = CHAT_HTML + "\n<script>" + CHAT_JS + "</script>\n"
    html = html[:idx] + block + html[idx:]

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK — injertado en", OUT)


if __name__ == "__main__":
    build()
