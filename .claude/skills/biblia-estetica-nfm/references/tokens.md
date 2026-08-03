# Tokens · Biblia Estética NFM

Valores exactos. No inventar variantes, no "aproximar" un hex.

---

## Paleta

### Marca

| Nombre | Hex | Uso |
|---|---|---|
| Naranja Acción | `#ff6602` | CTAs, acentos, activación. El único color de activación. |
| Naranja bright | `#ff8124` | Shimmer / gradiente sutil. Nunca solo. |
| Naranja texto | `#d95400` | Texto chico naranja **sobre blanco** (contraste AA). |
| Naranja wash | `#fff7f2` | Fondo de acento muy lavado (badges, eyebrows sobre claro). |
| Azul NFM | `#0c3452` | Ink + superficies oscuras. El azul institucional. |
| Azul profundo | `#061d30` | Fondos dark, base de sombras. |
| Azul intermedio | `#16466d` | Superficies dark secundarias, glow superior. |
| Azul claro / tint | `#e7edf2` | Cards y secciones claras alternas. |
| Blanco | `#ffffff` | Respiro. Es identidad, no relleno. |

> `#ff6602` sobre blanco NO pasa AA en texto chico. Para texto chico naranja usá `#d95400`.
> Para un botón naranja con texto blanco, `#ff6602` está bien (texto grande y bold).

### Texto sobre claro

| Nombre | Hex | Uso |
|---|---|---|
| Ink | `#0c3452` | Texto principal |
| Muted | `#33536b` | Texto secundario |
| Mono-grey | `#7a93a6` | Metadatos / labels |
| Mono-grey soft | `#9db0bf` | Terciario |

### Texto y bordes sobre navy

| Nombre | Hex | Uso |
|---|---|---|
| Hueso | `#f3f7fb` | Texto principal sobre navy |
| Niebla | `#9fb6c8` | Secundario sobre navy |
| Niebla 2 | `#6f8aa1` | Terciario sobre navy |
| Hairline dark | `rgba(255,255,255,.12)` | Bordes sobre navy |

### Bordes sobre claro

| Nombre | Valor |
|---|---|
| hair | `rgba(12,52,82,.10)` |
| hair-2 | `rgba(12,52,82,.16)` |

---

## Tipografía

```
Montserrat      → títulos. Pesos 800/900. Tracking negativo (-.01 a -.022em).
Open Sans       → cuerpo. Pesos 400/600/700. Line-height 1.6.
JetBrains Mono  → labels, eyebrows, metadatos. Peso 500, MAYÚSCULAS, letter-spacing .16–.2em.
```

Import:

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Open+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Escala

| Rol | Fuente | Tamaño | Tracking |
|---|---|---|---|
| Display XL | Montserrat 900 | `clamp(34px,6vw,64px)` | `-.02em` |
| Display LG | Montserrat 800 | `clamp(26px,4vw,40px)` | `-.015em` |
| Heading | Montserrat 800 | 24px | `-.01em` |
| Card title | Montserrat 800 | 16–23px | `-.01em` |
| Lead | Open Sans 400 | `clamp(16px,2vw,19px)` | — |
| Body | Open Sans 400 | 16px (13.5px en cards) | — |
| Mono / eyebrow | JetBrains Mono 500 | 10–12px | `.16–.2em` |

Ancho de línea: títulos `max-width:16ch`, lead `max-width:52–66ch`. Nunca líneas de 120 caracteres.

---

## Sistema

| Token | Valor | Uso |
|---|---|---|
| radius sm / md / lg / xl | `8 / 12 / 16 / 24px` | inputs → botones → cards → destacados |
| pill | `999px` | badges, eyebrows |
| shadow-card | `0 1px 3px rgba(12,52,82,.08), 0 8px 24px rgba(12,52,82,.06)` | cards sobre claro |
| shadow-cta | `0 8px 24px rgba(255,102,2,.28)` | glow del CTA naranja |
| shadow-elev | `0 12px 40px rgba(12,52,82,.12)` | elementos elevados |
| espaciado | base `4px` | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 |
| section padding | `88px` desktop / `62px` mobile | vertical |
| content max-width | `1080–1120px` | ancho de contenido |

## Motion

| Token | Valor |
|---|---|
| ease | `cubic-bezier(.16,1,.3,1)` |
| spring | `cubic-bezier(.34,1.56,.64,1)` |
| micro (hover, toggles) | `160–320ms` |
| entrada de sección | `600–900ms` |
| patrón de entrada | `fade + translate-Y ascendente` (18px) |
| shimmer | `5.5s linear infinite` |

Todo movimiento se apaga bajo `@media (prefers-reduced-motion: reduce)`.

---

## Bloque `:root` — copiar y pegar

```css
/* Sistema de diseño · Instituto de Productividad (NFM) */
:root{
  /* Marca */
  --orange:#ff6602; --orange-hi:#ff8124; --orange-hover:#e65a00;
  --orange-text:#d95400; --orange-wash:#fff7f2;
  --navy:#0c3452; --navy-deep:#061d30; --navy-lift:#16466d;
  /* Superficies claras */
  --white:#ffffff; --blue-light:#e7edf2;
  --hair:rgba(12,52,82,.10); --hair-2:rgba(12,52,82,.16);
  /* Texto sobre claro */
  --ink:#0c3452; --muted:#33536b; --mono-grey:#7a93a6; --mono-grey-soft:#9db0bf;
  /* Texto/bordes sobre navy */
  --hueso:#f3f7fb; --niebla:#9fb6c8; --niebla-2:#6f8aa1; --hair-d:rgba(255,255,255,.12);
  /* Sistema */
  --radius:16px;
  --ease:cubic-bezier(.16,1,.3,1);
  --spring:cubic-bezier(.34,1.56,.64,1);
  --shadow-card:0 1px 3px rgba(12,52,82,.08),0 8px 24px rgba(12,52,82,.06);
  --shadow-cta:0 8px 24px rgba(255,102,2,.28);
  --shadow-elev:0 12px 40px rgba(12,52,82,.12);
  --maxw:1080px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Open Sans',sans-serif;color:var(--ink);background:var(--white);
  line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:'Montserrat',sans-serif}
.mono{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.2em}
::selection{background:var(--orange);color:#fff}
```
