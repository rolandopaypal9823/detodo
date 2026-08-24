# Export a .pptx

Dos versiones del mismo deck, según qué necesites:

| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `El-mapa-del-1-pct-EDITABLE.pptx` | Formas y textos **nativos** de PowerPoint | Querés cambiar el copy o mover cosas |
| `El-mapa-del-1-pct.pptx` | Cada slide como **imagen** a 2x | Querés fidelidad exacta al HTML |

Ambos: 11 slides en 16:9 (13,33" × 7,5" = 1920×1080) y **con las notas del
presentador** cargadas en el panel de notas.

## La versión EDITABLE

159 cuadros de texto y 319 formas, todo seleccionable y movible. Las únicas
imágenes son las dos ilustraciones de Mini Nico (una ilustración no puede ser
una forma nativa).

Se ve *parecida* al HTML, no idéntica: los mockups (WhatsApp, formulario,
calendario, habit tracker) están reconstruidos con rectángulos y texto en vez
de replicar el CSS. A cambio, podés editar cada palabra.

Tipografías: Montserrat y Open Sans. Si no las tenés instaladas, PowerPoint
sustituye y el espaciado cambia un poco — instalalas desde Google Fonts.

Falta pegar el **QR** en el slide 10 (hay un recuadro blanco que dice
"Pegá acá el QR").

### Regenerarla

```bash
cd deck-1pct/export
npm install pptxgenjs
node build-nativo.js
```

Las ilustraciones salen de `img/`.

## La versión por imágenes

```bash
cd deck-1pct/export
npm install playwright pptxgenjs
node capture.js     # 11 PNG + meta.json (notas) desde el HTML
node build.js       # arma El-mapa-del-1-pct.pptx
```

Los PNG intermedios no se versionan. Para cambiar copy acá se edita
`../deck-mapa-1-pct.html` y se vuelve a exportar.
