# Prompts para GPT-image — las dos imágenes de la landing

Dos imágenes gemelas del ebook, una para cada card. Tienen que verse como un **set**:
mismo tamaño de dispositivo, misma luz, mismo tratamiento. Lo único que cambia es la
inclinación (convergen hacia el centro) y el cartel.

| Imagen | Card | Archivo final | Cartel |
|---|---|---|---|
| A | izquierda (el regalo) | `assets/ebook-primer-capitulo.png` | `PRIMER CAPÍTULO` (naranja) |
| B | derecha (la venta) | `assets/ebook-libro-completo.png` | `LIBRO COMPLETO` (blanco) |

## Cómo usarlos

1. Adjuntá **la foto del ebook** (la tablet con la tapa de *Hackea tu cerebro*) como referencia.
2. Pegá el Prompt A. Pedí salida **1024×1024, PNG con fondo transparente**.
3. En la **misma conversación**, pegá el Prompt B (así hereda luz y escala del primero).
4. Guardá los PNG en `assets/` con los nombres exactos de la tabla. La landing los toma sola.

> El fondo transparente no es opcional: las cards son de vidrio sobre azul con gradiente.
> Un PNG con fondo sólido va a dibujar un rectángulo y arruina el efecto.

> El **botón va en HTML**, no dentro de la imagen: es clickeable, se ve nítido en cualquier
> pantalla y se puede medir. Si igual querés uno pintado en la imagen, al final está el add-on.

---

## PROMPT A — Primer capítulo (card izquierda)

```
Use the attached image as the exact reference for the device and the book cover: same tablet,
same cover artwork, same illustration, same colors, same cover typography. Reproduce the cover
faithfully — do not redesign it, do not re-letter it, do not re-illustrate it.

Square 1:1 product hero shot on a FULLY TRANSPARENT background (real alpha channel — no backdrop,
no floor, no room, no scene, no color fill).

Composition: the tablet floats upright and centered, rotated about 6 degrees clockwise (top edge
leaning to the right), in a subtle three-quarter perspective. It occupies roughly 62% of the frame
height, with clear headroom above and below. Nothing is cropped.

Lighting: cool studio key light from the upper left; a deep navy rim light (#0c3452) along the
right edge; a warm orange accent light (#ff6602) grazing the lower-right corner of the device.
Crisp, believable screen reflection. Soft semi-transparent contact shadow under the device that
fades out completely — never a hard black blob.

Graphic overlay, rendered as clean vector-sharp type in a heavy geometric sans (Montserrat Black
style), ALL CAPS. Render the Spanish text EXACTLY as written, accents included:
- A bold badge pinned over the upper-left corner of the tablet, rotated about -8 degrees,
  solid orange #ff6602, white text: "PRIMER CAPÍTULO"
- Centered below the device, small monospaced caps with wide letter-spacing, white: "PDF · GRATIS"

Style: premium editorial tech mockup. High contrast, clean, generous negative space. Palette
limited to the cover's own colors plus navy #0c3452, orange #ff6602 and white.

Avoid: any text other than the two strings above, watermarks, extra logos, hands, people, desks,
plants, background gradients, framed drop shadows, glossy 3D bevels, plastic reflections,
misspelled Spanish, and missing accents — "CAPÍTULO" must keep its Í.
```

## PROMPT B — Libro completo (card derecha)

```
Same device, same cover, same lighting, same scale and same treatment as the previous image —
this is its twin for a side-by-side layout. Use the attached image again as the exact reference
for the tablet and the book cover; reproduce the cover faithfully, do not redesign or re-letter it.

Square 1:1 product hero shot on a FULLY TRANSPARENT background (real alpha channel — no backdrop,
no floor, no scene, no color fill).

Only two things change from the previous image:
1. The tablet is rotated about 6 degrees COUNTER-CLOCKWISE (top edge leaning to the left), so that
   placed to the right of its twin the two devices converge toward each other.
2. The badge pinned over the upper-left corner of the tablet is solid WHITE with deep navy #0c3452
   text and a thin orange #ff6602 outline, rotated about -8 degrees, reading exactly:
   "LIBRO COMPLETO"

Centered below the device, small monospaced caps with wide letter-spacing, white, exactly:
"EDICIÓN COMPLETA"

Keep everything else identical: same device size in frame, same upper-left key light, same navy rim
light on the right edge, same orange accent grazing the lower-right corner, same soft transparent
contact shadow, same heavy geometric sans (Montserrat Black style) in ALL CAPS.

Style: premium editorial tech mockup. High contrast, clean, generous negative space. Palette limited
to the cover's own colors plus navy #0c3452, orange #ff6602 and white.

Avoid: any text other than the two strings above, watermarks, extra logos, hands, people, desks,
plants, background gradients, framed drop shadows, glossy 3D bevels, plastic reflections,
misspelled Spanish, and missing accents — "EDICIÓN" must keep its Ó.
```

---

## Add-on opcional — botón pintado dentro de la imagen

Si querés que la imagen ya traiga el botón dibujado, agregá este párrafo al final del prompt
(y en la landing sacá o dejá el botón real según cómo se vea):

```
Also include, centered below the device, a rounded rectangle button (12px-style radius) filled with
solid orange #ff6602, with a soft orange glow beneath it, and white ALL CAPS text in a heavy
geometric sans reading exactly: "DESCARGAR PRIMER CAPÍTULO"   <-- imagen A
                              "CONSEGUIR LIBRO COMPLETO"      <-- imagen B
```

Para la imagen B, si el botón va pintado, usalo **blanco con texto navy** en lugar de naranja: en el
sistema NFM el naranja es el único color de activación y no debe competir consigo mismo en la misma
pantalla.

---

## Si el modelo rompe los acentos

Pasa seguido con `Í` y `Ó`. Dos salidas:

1. Re-generá pidiendo: *"Regenerate keeping everything identical, but fix the typography: the text
   must read exactly PRIMER CAPÍTULO with an accented Í. Do not change composition or lighting."*
2. O generá las imágenes **sin cartel** (borrá el bloque "Graphic overlay") y dejá que el texto lo
   ponga la landing: el título de cada card ya dice "Primer capítulo en PDF" y "El libro completo".
   Es la opción más segura y la que mejor se ve en mobile.
