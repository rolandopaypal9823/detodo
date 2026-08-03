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
    ├── logo-nfm-navy.png       ← logo oficial navy (por si hace falta sobre claro)
    ├── ebook-primer-capitulo.png   ← FALTA: generalo con el Prompt A
    └── ebook-libro-completo.png    ← FALTA: generalo con el Prompt B
```

Mientras las dos imágenes del ebook no existan, cada card muestra un marco FRAMER limpio con el
label de qué va ahí. No se rompe nada: podés publicarla igual y sumar las imágenes después.

**La forma rápida y segura de generarlas** (sin IA, la tapa queda pixel a pixel):

```bash
pip install Pillow
python3 armar-mockups.py /ruta/a/la/foto-del-ebook.png
```

Deja las dos en `assets/` con los nombres correctos. Detalle y alternativas con IA en
`PROMPTS-IMAGENES.md`.

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
`landing-autocontenida.html` en un bloque HTML a página completa. El logo ya viene embebido en
base64; solo tenés que subir las dos imágenes del ebook a la Biblioteca de medios y reemplazar
`assets/ebook-primer-capitulo.png` y `assets/ebook-libro-completo.png` por las URLs que te da
WordPress.

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
