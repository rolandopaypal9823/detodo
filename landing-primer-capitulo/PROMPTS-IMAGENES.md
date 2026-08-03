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

## ⚠️ Regla dura: la tapa no se toca

Los modelos de imagen, si les das una foto con una cara, **la vuelven a dibujar**. Te devuelven un
Nico que no es Nico: otra nariz, otros ojos, otra edad, el bigote distinto, los anteojos cambiados.
Es el error más común y el que arruina la pieza.

La tapa —foto de Nico, ilustración, rayos, tipografía, logos de la editorial— es un **asset cerrado**
que se copia tal cual. Lo único que el modelo puede hacer es **acomodar el dispositivo**: rotarlo,
escalarlo, iluminarlo y ponerle sombra. Nada de lo que está adentro de la pantalla se regenera.

Los dos prompts ya traen esa instrucción en mayúsculas. Igual, **mirá la cara antes de dar por buena
cada imagen**. Si cambió aunque sea un poco, mandá el re-roll de más abajo.

---

## PROMPT A — Primer capítulo (card izquierda)

```
ABSOLUTE RULE — THE COVER IS A LOCKED ASSET. The attached image contains a photograph of a real
person (the author). Copy the book cover from the attached image pixel-for-pixel: the photograph of
the man, his FACE, his facial features, his expression, his eyes, his eyebrows, his nose, his
moustache and beard, his glasses, his hair, his skin tone, his tattoo and his t-shirt, plus the
illustration, the lightning shapes, every word of the cover typography and the publisher logos.
DO NOT redraw, regenerate, re-render, restyle, retouch, beautify, smooth, re-age, reproportion or
swap the man's face. DO NOT change his expression. DO NOT redesign, re-letter or re-illustrate the
cover. Treat everything inside the screen as an untouchable photographic paste-in.
The ONLY thing you may do with the device is reposition it: rotate it, rescale it, light it and
give it a shadow, as a single rigid object. Any change to the man's face is a failed result.

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

Avoid: ANY alteration of the author's face or of the cover artwork, AI-retouched or "prettified"
skin, a different-looking person, a redrawn illustration, re-typeset cover text, any text other
than the two strings above, watermarks, extra logos, hands, people, desks, plants, background
gradients, framed drop shadows, glossy 3D bevels, plastic reflections, misspelled Spanish, and
missing accents — "CAPÍTULO" must keep its Í.
```

## PROMPT B — Libro completo (card derecha)

```
Same device, same cover, same lighting, same scale and same treatment as the previous image —
this is its twin for a side-by-side layout.

ABSOLUTE RULE — THE COVER IS A LOCKED ASSET, exactly as in the previous image. Copy the book cover
from the attached image pixel-for-pixel: the photograph of the real man (the author), his FACE, his
facial features, his expression, his eyes, his eyebrows, his nose, his moustache and beard, his
glasses, his hair, his skin tone, his tattoo and his t-shirt, plus the illustration, the lightning
shapes, every word of the cover typography and the publisher logos. DO NOT redraw, regenerate,
re-render, restyle, retouch, beautify, smooth, re-age, reproportion or swap the man's face. DO NOT
change his expression. DO NOT redesign, re-letter or re-illustrate the cover. Treat everything
inside the screen as an untouchable photographic paste-in. The ONLY thing you may do with the
device is reposition it: rotate it, rescale it, light it and give it a shadow, as a single rigid
object. His face must be identical to the previous image and to the reference.

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

Avoid: ANY alteration of the author's face or of the cover artwork, AI-retouched or "prettified"
skin, a different-looking person, a face that does not match the previous image, a redrawn
illustration, re-typeset cover text, any text other than the two strings above, watermarks, extra
logos, hands, people, desks, plants, background gradients, framed drop shadows, glossy 3D bevels,
plastic reflections, misspelled Spanish, and missing accents — "EDICIÓN" must keep its Ó.
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

## Si le cambió la cara a Nico

Es el fallo más probable. Re-roll, pegando esto en la misma conversación:

```
The author's face changed. Regenerate keeping the composition, rotation, lighting, shadow and badge
exactly as they are, but restore the book cover to be pixel-identical to the attached reference: the
same photograph of the same real man, same face, same features, same expression, same moustache and
beard, same glasses, same hair, same skin tone, same tattoo, same t-shirt, same illustration, same
typography. Do not redraw or retouch his face in any way — copy it, do not interpret it.
```

Si a la segunda o tercera sigue cambiándola, no insistas: el modelo no la está copiando, la está
volviendo a dibujar. Salida segura:

- Generá la imagen **con la pantalla vacía** (agregá: *"leave the tablet screen empty, a plain dark
  screen, no cover artwork"*), y después **pegás la tapa original encima** en Canva/Photoshop, con
  la misma rotación. La tapa queda intacta porque nunca pasó por el modelo.
- O usá la foto del ebook tal cual, recortada en PNG con fondo transparente, sin generar nada. La
  landing igual se ve bien: el cartel de "Primer capítulo" y "Libro completo" ya lo dicen los
  títulos de cada card.

## Si el modelo rompe los acentos

Pasa seguido con `Í` y `Ó`. Dos salidas:

1. Re-generá pidiendo: *"Regenerate keeping everything identical, but fix the typography: the text
   must read exactly PRIMER CAPÍTULO with an accented Í. Do not change composition or lighting."*
2. O generá las imágenes **sin cartel** (borrá el bloque "Graphic overlay") y dejá que el texto lo
   ponga la landing: el título de cada card ya dice "Primer capítulo en PDF" y "El libro completo".
   Es la opción más segura y la que mejor se ve en mobile.
