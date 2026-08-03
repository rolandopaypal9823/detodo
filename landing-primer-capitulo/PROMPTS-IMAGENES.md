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

## ⚠️ Leé esto primero: por qué te cambia la cara de Nico

**No es un problema de prompt.** Un modelo de imagen no recorta ni copia: **sintetiza cada pixel de
cero**. Cuando le pedís "acomodá la tablet, iluminala, ponele sombra", está generando una imagen
nueva entera — y la cara de Nico entra en esa generación. Vuelve a dibujarla siempre. A veces te la
devuelve parecida y zafás; a veces te devuelve a otra persona.

Escribir la regla más fuerte, en mayúsculas y repetida, **baja la probabilidad pero no la elimina**.
No hay redacción que la lleve a cero, porque le estás pidiendo justamente lo que rompe la cara.

La única forma de garantía es que **la tapa nunca pase por el modelo**.

### Las tres vías, de más segura a más riesgosa

| | Vía | Fidelidad de la cara | Trabajo |
|---|---|---|---|
| **1** | **El script `armar-mockups.py`** — sin IA, manipulación de pixeles | **100%, garantizada** | 1 comando |
| **2** | IA con **pantalla vacía** + pegás la tapa encima | 100% (la tapa no se genera) | 10 min en Canva |
| **3** | IA generando todo (Prompts A y B) | **no garantizada** | rápido, pero re-rolls |

Si ya probaste la 3 y te la sigue cambiando: **no insistas, andá a la 1**.

---

## VÍA 1 — El script (recomendada)

Cero IA. Recorta el fondo, rota el dispositivo, le pone el cartel y la sombra. La tapa se mueve
como un bloque de pixeles: **es imposible que la cara cambie, porque nadie la vuelve a dibujar.**

```bash
cd landing-primer-capitulo
python3 armar-mockups.py /ruta/a/la/foto-del-ebook.png
```

Te deja las dos imágenes en `assets/` con los nombres exactos que la landing espera. Listo.

Detalles:

- Necesita Pillow: `pip install Pillow`.
- Si la foto ya viene con fondo transparente: `--no-recorte`.
- Si queda un halo blanco alrededor del dispositivo: subí el umbral, `--tolerancia 48`.
- El recorte va por *flood fill* desde los bordes, así que **el blanco que esté dentro de la tapa no
  se toca** — solo se saca el fondo que rodea al dispositivo.
- Para el tipo exacto de los carteles: `--font /ruta/Montserrat-Black.ttf`. Sin eso usa la fuente
  bold del sistema y avisa.

---

## VÍA 2 — IA con la pantalla vacía

Si querés la luz y la sombra de un render de IA pero sin arriesgar la cara: generás la tablet
**vacía** y después le pegás la tapa encima en Canva/Photoshop, con la misma inclinación.

Prompt:

```
Use the attached image only as a reference for the DEVICE SHAPE (the tablet's silhouette, bezel,
thickness and proportions). Do NOT reproduce the artwork on the screen.

Render the tablet with a COMPLETELY EMPTY SCREEN: a flat, uniform, pure magenta screen (#FF00FF),
edge to edge, with no image, no text, no logo, no reflection and no gradient on it. The magenta area
must be perfectly flat and uniform so it can be used as a chroma key.

Square 1:1 on a FULLY TRANSPARENT background (real alpha channel — no backdrop, no floor, no scene).
The tablet floats upright and centered, rotated about 6 degrees clockwise, subtle three-quarter
perspective, occupying about 62% of the frame height, nothing cropped.

Lighting: cool studio key light from the upper left; deep navy rim light (#0c3452) along the right
edge; warm orange accent (#ff6602) grazing the lower-right corner. Soft semi-transparent contact
shadow under the device that fades out completely — never a hard black blob. Light the bezel and the
body, never the screen area.

Avoid: any artwork, text, person, face, logo or reflection on the screen; gradients or highlights
over the magenta; backgrounds; hands; desks.
```

Para la segunda imagen, cambiá **clockwise** por **counter-clockwise**.

Después, en Canva: ponés la tapa original arriba, la rotás los mismos 6°, la ajustás al rectángulo
magenta y le sumás el cartel. La cara nunca pasó por el modelo.

---

## VÍA 3 — IA generando todo

Los dos prompts de abajo traen la regla de la cara lo más dura que se puede escribir. Aun así,
**la fidelidad no está garantizada** (ver arriba). Usalos si querés probar rápido, y mirá la cara
antes de dar por buena cada imagen.

Si tu herramienta tiene **edición con máscara** (el pincel de "seleccioná el área a editar"),
usala: pintá **solo el fondo alrededor del dispositivo** y dejá la pantalla fuera de la selección.
Lo que queda fuera de la máscara no se regenera — y ahí sí la cara está protegida de verdad.

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

**Un solo re-roll.** Si a la segunda te la vuelve a cambiar, dejá de pelearla: el modelo no la está
copiando, la está volviendo a dibujar, y va a seguir haciéndolo. Andá a la **Vía 1** (el script) o a
la **Vía 2** (pantalla vacía). Ahí el problema desaparece por construcción, no por suerte.

## Si el modelo rompe los acentos

Pasa seguido con `Í` y `Ó`. Dos salidas:

1. Re-generá pidiendo: *"Regenerate keeping everything identical, but fix the typography: the text
   must read exactly PRIMER CAPÍTULO with an accented Í. Do not change composition or lighting."*
2. O generá las imágenes **sin cartel** (borrá el bloque "Graphic overlay") y dejá que el texto lo
   ponga la landing: el título de cada card ya dice "Primer capítulo en PDF" y "El libro completo".
   Es la opción más segura y la que mejor se ve en mobile.
