# Landing · Entrega del 1er capítulo de «Hackea tu cerebro»

Rehecha con el sistema de diseño **Biblia Estética NFM**: azul con profundidad (nunca plano),
naranja como único color de activación, Montserrat + Open Sans + JetBrains Mono, logo arriba y
abajo, red neuronal de fondo.

## Qué cambió respecto de la versión anterior

| Antes | Ahora |
|---|---|
| Azul plano `#0c3452` de fondo | Azul con capas: gradiente + glow superior + calor naranja + borde de luz |
| Dos titulares gigantes en mayúsculas apilados | Un H1 con jerarquía + lead corto |
| Dos botones naranjas idénticos, uno arriba del otro | Dos cards lado a lado (regalo / venta), con un solo CTA primario |
| Sin imagen | Un mockup del ebook por card |
| Logo suelto | Logo en header y footer, con regla naranja |
| Sin movimiento | Red neuronal, shimmer, reveals — todos desactivables por `prefers-reduced-motion` |

## Archivos

```
landing-primer-capitulo/
├── index.html                  ← la landing (referencia assets/ por separado)
├── landing-autocontenida.html  ← misma landing en 1 solo archivo (logo embebido)
├── armar-mockups.py            ← arma las 2 imágenes SIN IA (la cara de Nico no se toca)
├── PROMPTS-IMAGENES.md         ← los 2 prompts de GPT-image para las imágenes
└── assets/
    ├── logo-nfm-blanco.png     ← logo oficial (versión negativa, para fondo oscuro)
    └── logo-nfm-navy.png       ← logo oficial navy (por si hace falta sobre claro)
```

## Las imágenes: ya están resueltas

Las dos cards usan **la foto del libro que ya está en WordPress**, por URL absoluta. No hay nada
que generar ni que subir.

Y los carteles —"PRIMER CAPÍTULO · PDF" y "LIBRO COMPLETO"— **son texto HTML**, no están quemados
en la imagen. Eso significa: nítidos en cualquier pantalla, se cambian escribiendo (buscá
`class="sello"`), y ningún modelo de IA le toca la cara a Nico.

Como la foto viene con fondo blanco y las cards son azul oscuro, el libro va apoyado sobre una
**placa clara** con `mix-blend-mode: multiply`, que funde ese fondo con la placa. Se lee como un
product shot de estudio. Los dos libros están rotados ±2.5° para converger hacia el centro.

Si algún día querés los mockups recortados en PNG transparente, `armar-mockups.py` los arma sin
IA a partir de la foto (ver `PROMPTS-IMAGENES.md`). No hace falta para publicar.

## Links que usa

| Dónde | URL |
|---|---|
| Botón "Descargar primer capítulo" | `https://nicolasfernandezmiranda.com/wp-content/uploads/2026/03/HTC-1-CAP.pdf` |
| Botón "Conseguir libro completo" | `https://comunidadproductiva.circle.so/hackea-tu-cerebro?utm_source=1ercap` |

Para cambiarlos, buscá `href=` en `index.html`. Son los dos únicos.

## Cómo publicarla

**Opción A — página HTML directa.** Subís la carpeta entera. `index.html` referencia `assets/`
con rutas relativas, así que funciona en cualquier hosting sin tocar nada.

**Opción B — dentro de WordPress (Elementor / bloque HTML).** Copiá todo el contenido de
`landing-autocontenida.html` en un bloque HTML a página completa. No hay que tocar nada: el logo
va embebido en base64 y la foto del libro, el PDF y el link de compra son URLs absolutas.

## Detalles técnicos

- Un solo archivo, sin dependencias salvo Google Fonts.
- Responsive: las cards se apilan por debajo de 860px.
- `prefers-reduced-motion: reduce` apaga la red neuronal, el shimmer y los reveals.
- Los reveals solo se activan si el JS corrió (`<html class="js">`): si el JS falla, todo el
  contenido queda visible igual.
- `noindex, follow` en el `<meta robots>` — es una página de entrega, no tiene que rankear.

## Qué medir

Es la página donde se define si el regalo se convierte en venta. Los dos números:

1. **Descargas del PDF** (clicks en el CTA naranja) sobre visitas.
2. **Clicks al libro completo** sobre descargas — el `utm_source=1ercap` ya viene puesto en el link,
   así que la venta atribuida a esta landing se ve directo en Circle.
