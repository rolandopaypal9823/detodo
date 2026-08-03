# Componentes · Biblia Estética NFM

HTML + CSS copiable. Todo asume el bloque `:root` de `tokens.md`.

---

## Botones

Regla: **un solo CTA primario por pantalla**. El resto, ghost.

```css
.btn{display:inline-flex;align-items:center;gap:9px;justify-content:center;
  font-family:'Montserrat',sans-serif;font-weight:800;font-size:16px;
  padding:15px 28px;border-radius:12px;border:none;cursor:pointer;text-decoration:none;
  line-height:1.1;transition:transform .16s var(--ease),box-shadow .16s,background .16s}
.btn-primary{background:var(--orange);color:#fff;box-shadow:var(--shadow-cta)}
.btn-primary:hover{transform:translateY(-2px);background:var(--orange-hover);
  box-shadow:0 14px 34px rgba(255,102,2,.4)}
/* ghost sobre blanco */
.btn-ghost{background:transparent;color:var(--navy);border:2px solid rgba(12,52,82,.2)}
.btn-ghost:hover{border-color:var(--navy)}
/* ghost sobre navy */
.btn-ghost-d{background:rgba(255,255,255,.05);color:#fff;border:2px solid rgba(255,255,255,.46)}
.btn-ghost-d:hover{border-color:#fff;background:rgba(255,255,255,.11)}
/* tamaños */
.btn-sm{font-size:13px;padding:10px 18px;border-radius:10px}
.btn-lg{font-size:18px;padding:18px 34px}
/* la flecha se mueve en hover */
.btn .arw{font-size:1.1em;transition:transform .2s}
.btn:hover .arw{transform:translateX(3px)}
```

```html
<a class="btn btn-primary" href="#">Agendá tu entrevista <span class="arw">→</span></a>
<a class="btn btn-ghost" href="#">Conocer más</a>
```

---

## Eyebrow (label de sección)

```css
.eyebrow{display:inline-flex;align-items:center;gap:8px;
  font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.2em;
  font-size:11px;font-weight:500;color:var(--orange-text);background:var(--orange-wash);
  border:1px solid rgba(255,102,2,.22);padding:7px 14px;border-radius:100px;margin-bottom:18px}
/* sobre navy */
.dark .eyebrow{color:#ffd0ac;background:rgba(255,102,2,.14);border-color:rgba(255,255,255,.14)}
```

Variante con punto pulsante (para estados "en vivo", "listo", "disponible"):

```css
.eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--orange);
  box-shadow:0 0 0 0 rgba(255,102,2,.55);animation:pulse 2.6s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 9px rgba(255,102,2,0)}100%{box-shadow:0 0 0 0 rgba(255,102,2,0)}}
```

## Badge

```css
.badge{display:inline-flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;
  font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;
  color:var(--orange-text);background:var(--orange-wash);
  border:1px solid rgba(255,102,2,.22);padding:5px 12px;border-radius:100px}
```

---

## Cards

### Sobre blanco

```css
.card{background:#fff;border:1px solid var(--hair);border-radius:var(--radius);
  padding:24px;box-shadow:var(--shadow-card)}
.card h4{font-family:'Montserrat';font-weight:800;font-size:16px;color:var(--navy);margin-bottom:6px}
.card p{font-size:13.5px;color:var(--muted);line-height:1.55}
/* número grande naranja de la card */
.card .mk{font-family:'Montserrat';font-weight:900;font-size:20px;color:var(--orange);
  display:block;margin-bottom:8px}
```

### Sobre navy (vidrio)

```css
.card--navy{background:rgba(255,255,255,.045);border:1px solid var(--hair-d);
  border-radius:var(--radius);padding:24px;
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07), 0 18px 44px -22px rgba(0,0,0,.6)}
.card--navy h4{color:#fff}
.card--navy p{color:var(--niebla)}
```

### Card foco

**Una sola por pantalla.** Borde naranja + calor radial. Es la que querés que elijan.

```css
/* sobre blanco */
.card--focus{border:2px solid var(--orange);
  box-shadow:0 20px 46px -18px rgba(255,102,2,.28)}
/* sobre navy */
.card--focus-d{border-color:rgba(255,102,2,.42);
  background:radial-gradient(100% 60% at 50% 0%,rgba(255,102,2,.10),transparent 62%),
             rgba(255,255,255,.045);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07), 0 22px 52px -24px rgba(255,102,2,.34)}
```

---

## Paneles

```css
.panel{border-radius:16px;padding:26px;border:1px solid var(--hair)}
.panel.white{background:#fff}
.panel.tint{background:var(--blue-light)}
.panel.navy{background:var(--navy);color:var(--hueso);border-color:var(--hair-d)}
.panel .plabel{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--mono-grey);margin-bottom:14px}
.panel.navy .plabel{color:var(--niebla-2)}
```

---

## Stats / prueba

```css
.stat{text-align:center}
.stat .n{font-family:'Montserrat';font-weight:900;font-size:clamp(26px,4vw,38px);
  color:var(--navy);line-height:1}
.stat .n .u{color:var(--orange)}   /* la unidad va naranja: "8.8/10", "+10 países" */
.stat .l{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-top:8px}
.dark .stat .n{color:#fff} .dark .stat .l{color:var(--niebla)}
```

```html
<div class="stat"><div class="n">8.8<span class="u">/10</span></div><div class="l">Acompañamiento</div></div>
```

---

## FRAMER (marco de foto)

Marca las esquinas con el ángulo naranja. Sirve como marco de imagen real **y** como placeholder
elegante cuando el asset todavía no existe.

```css
.framer{position:relative;aspect-ratio:16/10;border-radius:16px;overflow:hidden;
  background:linear-gradient(150deg,#eef3f7,#dae5ee);border:1px solid var(--hair);
  display:flex;align-items:center;justify-content:center;
  color:var(--mono-grey);font-family:'JetBrains Mono';font-size:11px;
  letter-spacing:.12em;text-transform:uppercase}
.framer::before,.framer::after{content:"";position:absolute;width:24px;height:24px;
  border:2.5px solid var(--orange);opacity:.85}
.framer::before{top:12px;left:12px;border-right:0;border-bottom:0;border-radius:8px 0 0 0}
.framer::after{bottom:12px;right:12px;border-left:0;border-top:0;border-radius:0 0 8px 0}
.framer.on-navy{background:linear-gradient(150deg,#0e3350,#0a2942);
  color:var(--niebla-2);border-color:var(--hair-d)}
```

---

## Marquee (cinta de conceptos)

```css
.marq{overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.marq__row{display:flex;width:max-content;animation:mq 26s linear infinite}
.mq-i{font-family:'JetBrains Mono';font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--mono-grey);white-space:nowrap;display:inline-flex;align-items:center;
  gap:16px;padding:0 16px}
.mq-i::after{content:"";width:5px;height:5px;border-radius:50%;background:var(--orange);opacity:.75}
@keyframes mq{to{transform:translateX(-50%)}}
```

El contenido va **duplicado** en dos divs hermanos dentro de `.marq__row`, si no el loop salta.

---

## Cita

```css
.quote{max-width:760px;margin:0 auto;text-align:center}
.quote .mark{font-family:'Montserrat';font-weight:900;font-size:60px;
  color:var(--orange);opacity:.5;line-height:.6;margin-bottom:14px}
.quote blockquote{font-family:'Montserrat';font-weight:700;
  font-size:clamp(17px,2.5vw,23px);line-height:1.4;color:#fff;letter-spacing:-.01em}
.quote cite{display:block;margin-top:16px;font-style:normal;
  font-family:'JetBrains Mono';font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--niebla-2)}
```

---

## Tabla de datos

```css
.tk-table{width:100%;border-collapse:collapse;font-size:13.5px}
.tk-table th,.tk-table td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--hair)}
.tk-table th{font-family:'JetBrains Mono';font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--mono-grey);font-weight:500}
.tk-table td code{background:var(--blue-light);padding:2px 7px;border-radius:6px;color:var(--navy)}
```

---

## Grid utilitario

```css
.grid{display:grid;gap:18px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:820px){.g3,.g4{grid-template-columns:repeat(2,1fr)}.g2{grid-template-columns:1fr}}
@media(max-width:520px){.g3,.g4{grid-template-columns:1fr}}
```
