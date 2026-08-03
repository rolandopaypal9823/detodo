# Recetas · Biblia Estética NFM

Los efectos que hacen que una pieza *se sienta* del Instituto. Código completo, listo para pegar.

---

## 1. El azul elegante (el más importante)

Mismo hex, distinto tratamiento. `background:#0c3452` a secas cumple pero se ve chato y barato.
Todo fondo oscuro grande lleva **cuatro capas**: glow superior + calor naranja tenue + gradiente
base + borde de luz.

```css
.navy-elegante{
  position:relative;
  background:
    radial-gradient(120% 90% at 18% 12%, rgba(23,70,109,.6), transparent 55%),   /* glow superior */
    radial-gradient(90% 80% at 88% 106%, rgba(255,102,2,.07), transparent 60%),  /* calor naranja */
    linear-gradient(180deg, #0e3352 0%, #0c3452 45%, #061d30 100%);              /* base */
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06);                               /* borde de luz */
}
```

### Para una página entera

No uses `background-attachment:fixed` en `body`: pinta solo el alto del viewport y el resto de la
página queda **en blanco**. Usá una capa fija propia:

```html
<body>
  <div class="bg" aria-hidden="true"></div>
  <canvas id="neuralbg" aria-hidden="true"></canvas>
  <div id="neural-mask" aria-hidden="true"></div>
  <div class="page"> ... contenido ... </div>
</body>
```

```css
body{background:#061d30}                      /* fallback sólido */
.bg{position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(120% 90% at 18% 0%, rgba(23,70,109,.62), transparent 55%),
    radial-gradient(90% 70% at 88% 104%, rgba(255,102,2,.09), transparent 60%),
    linear-gradient(180deg,#0e3352 0%,#0c3452 42%,#061d30 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
#neuralbg{position:fixed;inset:0;z-index:1;pointer-events:none}
#neural-mask{position:fixed;inset:0;z-index:2;pointer-events:none;
  background:radial-gradient(120% 88% at 50% 4%,transparent 34%,rgba(6,29,48,.86) 100%)}
.page{position:relative;z-index:3}
```

---

## 2. Red neuronal animada

Constelación sutil de fondo. **Es fondo, nunca protagonista**: alfas bajos + la máscara radial
hacen que el texto siempre gane. Se apaga sola si el usuario pidió menos movimiento.

```js
function neural(canvas,opt){
  if(!canvas) return;
  var ctx=canvas.getContext('2d'), dpr=Math.min(window.devicePixelRatio||1,2);
  var w,h,nodes=[],LINK=opt.link||132;
  function size(){var r=canvas.getBoundingClientRect();w=Math.max(1,r.width);h=Math.max(1,r.height);
    canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);build();}
  function build(){var n=Math.max(12,Math.min(70,Math.round(w*h/22000)));nodes=[];
    for(var i=0;i<n;i++){nodes.push({x:Math.random()*w,y:Math.random()*h,
      vx:(Math.random()-.5)*.16,vy:(Math.random()-.5)*.16,r:Math.random()*1.5+.8});}}
  function step(){requestAnimationFrame(step);ctx.clearRect(0,0,w,h);
    for(var i=0;i<nodes.length;i++){var nd=nodes[i];nd.x+=nd.vx;nd.y+=nd.vy;
      if(nd.x<0||nd.x>w)nd.vx*=-1;if(nd.y<0||nd.y>h)nd.vy*=-1;}
    for(var a=0;a<nodes.length;a++){for(var b=a+1;b<nodes.length;b++){var A=nodes[a],B=nodes[b];
      var d=Math.hypot(A.x-B.x,A.y-B.y);
      if(d<LINK){ctx.strokeStyle=opt.edge+(opt.edgeA*(1-d/LINK)).toFixed(3)+')';
        ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(A.x,A.y);ctx.lineTo(B.x,B.y);ctx.stroke();}}}
    for(var k=0;k<nodes.length;k++){var N=nodes[k];ctx.fillStyle=opt.node;ctx.beginPath();
      ctx.arc(N.x,N.y,N.r,0,6.2832);ctx.fill();}}
  window.addEventListener('resize',size);size();step();
}
var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduce){
  // DARK · sobre azul
  neural(document.getElementById('neuralbg'),
    {edge:'rgba(122,182,225,',edgeA:0.18,node:'rgba(150,196,232,0.36)',link:132});
  // LIGHT · sobre blanco
  // neural(el, {edge:'rgba(12,52,82,',edgeA:0.14,node:'rgba(12,52,82,0.30)',link:120});
}
```

Densidad: el divisor `w*h/22000` es el dial. Más chico = más nodos. Por encima de ~90 nodos
empieza a competir con la lectura.

---

## 3. Shimmer (texto que brilla)

Para 2–4 palabras dentro de un H1. Nunca un párrafo entero.

```css
.shimmer{background:linear-gradient(100deg,#ff6602 18%,#ff8124 40%,#fff 50%,#ff8124 60%,#ff6602 82%);
  background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;
  animation:shim 5.5s linear infinite}
@keyframes shim{to{background-position:200% center}}
```

```html
<h1>Tu primer capítulo <span class="shimmer">ya es tuyo</span>.</h1>
```

---

## 4. Reveals on scroll

Fade + translate-Y ascendente, escalonado. **Crítico:** ocultá los elementos solo si el JS corrió.
Si escribís `.rv{opacity:0}` a secas y el JS falla o el `IntersectionObserver` no dispara, la
página queda en blanco.

```css
.js .rv{opacity:0;transform:translateY(18px);
  transition:opacity .8s var(--ease),transform .8s var(--ease)}
.js .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rv{opacity:1!important;transform:none!important}}
```

```js
(function(){
  var els=[].slice.call(document.querySelectorAll('.rv'));
  if(reduce||!('IntersectionObserver' in window)) return;   // sin soporte → todo visible
  document.documentElement.classList.add('js');
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){var el=en.target;
        setTimeout(function(){el.classList.add('in')},(el.dataset.d||0)*1);
        io.unobserve(el);}
    });
  },{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el,i){el.dataset.d=(i%3)*90;io.observe(el);});
})();
```

---

## 5. Cards de vidrio sobre navy

```css
.card{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.12);
  border-radius:20px;padding:26px;
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07), 0 18px 44px -22px rgba(0,0,0,.6);
  transition:transform .3s var(--ease),border-color .3s var(--ease),box-shadow .3s var(--ease)}
.card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.22)}
```

El `inset 0 1px 0 rgba(255,255,255,.07)` es el borde de luz superior. Sin eso la card de vidrio se
ve sucia; con eso se ve de cristal.

---

## 6. Patrón "dos caminos" (regalo + venta)

Dos cards lado a lado cuando hay que ofrecer dos acciones sin que compitan. Es el patrón de las
páginas de entrega: izquierda lo gratis, derecha lo pago.

Reglas:
- La **izquierda** (lo que el usuario vino a buscar) lleva el CTA **naranja lleno**.
- La **derecha** (la venta) lleva CTA **ghost blanco** + **borde naranja en la card** (card foco).
  Así pesa visualmente sin romper la regla del único naranja de activación.
- Numerá los pasos con un label mono: `01 EMPEZÁ ACÁ` / `02 SI TE RESUENA`. Convierte dos opciones
  sueltas en una secuencia.
- Cada card cierra con una nota mono chiquita bajo el botón que dice qué pasa al clickear
  (`PDF · DESCARGA INMEDIATA`, `TE LLEVA A LA PÁGINA DEL LIBRO`). Baja la fricción del click.

```css
.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:stretch}
.card{display:flex;flex-direction:column}
.card .spacer{flex:1}          /* empuja el botón al piso: los CTAs quedan alineados */
@media(max-width:860px){.cards{grid-template-columns:1fr;gap:18px}}
```

El `.spacer` con `flex:1` es lo que hace que los dos botones queden a la misma altura aunque los
textos midan distinto. Sin eso, las cards se ven desprolijas.

---

## 7. Slot de imagen con placeholder

Para que la pieza se vea terminada aunque el asset todavía no exista.

```html
<div class="shot">
  <img src="assets/mockup.png" alt="..."
       onerror="this.closest('.shot').classList.add('is-empty')">
  <div class="ph">Imagen<br>Mockup del producto</div>
</div>
```

```css
.shot{position:relative;aspect-ratio:1/1;max-height:330px;border-radius:14px;overflow:hidden;
  display:flex;align-items:center;justify-content:center;
  background:radial-gradient(72% 62% at 50% 44%,rgba(23,70,109,.55),transparent 70%)}
.shot img{width:auto;height:100%;max-width:100%;object-fit:contain;
  filter:drop-shadow(0 26px 42px rgba(0,0,0,.5));transition:transform .45s var(--ease)}
.card:hover .shot img{transform:translateY(-6px) scale(1.02)}
.shot .ph{display:none;position:absolute;inset:14px;border-radius:12px;
  border:1px dashed rgba(255,255,255,.18);align-items:center;justify-content:center;
  text-align:center;padding:20px;font-family:'JetBrains Mono',monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--niebla-2);line-height:1.9}
.shot .ph::before,.shot .ph::after{content:"";position:absolute;width:22px;height:22px;
  border:2.5px solid var(--orange);opacity:.85}
.shot .ph::before{top:10px;left:10px;border-right:0;border-bottom:0;border-radius:8px 0 0 0}
.shot .ph::after{bottom:10px;right:10px;border-left:0;border-top:0;border-radius:0 0 8px 0}
.shot.is-empty img{display:none}
.shot.is-empty .ph{display:flex}
```

Los mockups de producto van en **PNG con fondo transparente**. Un PNG con fondo sólido dibuja un
rectángulo sobre el navy con gradiente y arruina el efecto.

---

## 8. Pieza que se va a pegar en WordPress: scopeala

Si el HTML termina dentro de un bloque de WordPress / Elementor, **el CSS sin scope pierde**.
Un `h1{color:#fff}` tiene especificidad (0,0,1) y cualquier regla del tema tipo
`.entry-content h1` (0,1,1) le gana: el título sale del color del tema. Y peor: un
`*{margin:0;padding:0}` global le rompe el espaciado a **toda la página del sitio**.

Regla: **todo bajo una clase raíz** (`.nfm-lp`), y `!important` en las propiedades visualmente
críticas (color, background, font).

```html
<div class="nfm-lp">…toda la pieza…</div>
```

```css
.nfm-lp{ /* tokens + tipografía + color base */ }
.nfm-lp *{box-sizing:border-box;margin:0;padding:0;
  font-family:'Open Sans',sans-serif !important}
.nfm-lp h1{color:#fff !important;background:none !important;padding:0 !important}
.nfm-lp img{border:0 !important}          /* muchos temas le ponen borde a las img */
.nfm-lp a{text-decoration:none !important}
```

Cuatro trampas que aparecen sí o sí:

1. **La fuente no se hereda si el tema la declara directo.** `.entry-content p{font-family:Georgia}`
   le gana a la heredada del wrapper, porque una declaración directa siempre vence a la herencia.
   Por eso la base va en `.nfm-lp *` con `!important`, y las excepciones (Montserrat, Mono) tienen
   más especificidad.
2. **Los inline tienen que heredar tamaño.** Si el tema pone `.entry-content span{font-size:19px}`,
   te destroza el shimmer y las negritas. Fijalo:
   ```css
   .nfm-lp .shimmer,.nfm-lp b,.nfm-lp strong,.nfm-lp .arw{
     font-size:inherit !important;line-height:inherit !important;font-family:inherit !important}
   ```
3. **`background:` shorthand resetea `background-clip`.** El shimmer se ve como un bloque de color
   sólido. Usá `background-image:` y ponele `!important` al clip:
   ```css
   .nfm-lp .shimmer{background-image:linear-gradient(…) !important;
     -webkit-background-clip:text !important;background-clip:text !important;
     -webkit-text-fill-color:transparent !important}
   ```
4. **Nada de `position:fixed` en los fondos.** Embebido, un fondo fijo tapa el header y el footer del
   sitio. Van `absolute` dentro del wrapper (que es `position:relative`), así el fondo queda confinado
   a la pieza y scrollea con el contenido.

**Probalo antes de entregar.** Envolvé la pieza en un tema hostil simulado y sacá screenshot:

```css
/* tema falso: si tu pieza sobrevive a esto, sobrevive a cualquier WordPress */
.entry-content h1,.entry-content h2{color:#222 !important;font-family:Georgia;background:#fafafa;padding:10px}
.entry-content p,.entry-content span,.entry-content div{color:#555;font-family:Georgia;font-size:19px}
.entry-content a{color:#0645ad;text-decoration:underline}
.entry-content img{border:4px solid #f0c}
```

Chequeá que el header y el footer del tema queden intactos: si se movieron, tu reset se escapó.

---

## 9. Accesibilidad — el bloque que va siempre

```css
@media(prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
  .rv{opacity:1!important;transform:none!important}
}
```

Y el guard de JS correspondiente:

```js
var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduce){ /* neural, parallax, autoplay */ }
```

---

## 10. Logo embebido en HTML autocontenido

```bash
base64 -w0 logo-nfm-blanco.png
```

```html
<img class="logo" src="data:image/png;base64,iVBORw0KGgo..." alt="Nico Fernández Miranda">
```

Si el PNG pesa mucho, bajalo a ~400px de ancho y cuantizalo a 16 colores (el logo es plano, no
pierde nada y pasa de ~70KB a ~6KB):

```python
from PIL import Image
im = Image.open('logo-nfm-blanco.png').convert('RGBA')
w,h = im.size
im.resize((400, round(400*h/w)), Image.LANCZOS)\
  .quantize(colors=16, method=Image.FASTOCTREE)\
  .save('logo-opt.png', optimize=True)
```

---

## 11. Verificación visual antes de entregar

Chromium está preinstalado en el entorno remoto (`/opt/pw-browsers/chromium`). No corras
`playwright install`.

```python
import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w=1440, h=900, full=True):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page(viewport={"width":w,"height":h}, device_scale_factor=2)
        await pg.goto(url); await pg.wait_for_timeout(1500)
        H = await pg.evaluate("document.body.scrollHeight"); y = 0
        while y < H:                       # pasada de scroll: dispara los reveals
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(220); y += h*0.7
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
asyncio.run(main(*sys.argv[1:]))
```

Sacá el screenshot **desktop 1440 y mobile 390**, y miralos con tus propios ojos. Chequeá en ese
orden: ¿el fondo cubre toda la página o se corta? ¿los títulos blancos se leen? ¿los reveals
quedaron invisibles? ¿el azul tiene profundidad? ¿hay un solo CTA primario? ¿está el logo?
