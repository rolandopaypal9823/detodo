# Export a .pptx

Dos versiones del mismo deck. **La editable es la recomendada.**

| Archivo | Fondo | Textos | Cuándo |
|---|---|---|---|
| `El-mapa-del-1-pct-EDITABLE.pptx` | imagen fiel al HTML | **41 cuadros editables** | Casi siempre |
| `El-mapa-del-1-pct.pptx` | imagen fiel | dentro de la imagen | Solo si no vas a tocar nada |

Ambos: 11 slides en 16:9 (13,33" × 7,5" = 1920×1080) y con las notas del
presentador en el panel de notas.

## Cómo está armada la editable

Es un híbrido a propósito. Cada slide tiene:

- **Un fondo**: el render real del HTML a doble resolución — el mapa, el
  sendero, Mini Nico, los mockups de Calendly y WhatsApp, las viñetas. Todo
  eso es imagen y **no se puede romper sin querer**.
- **Encima, solo los textos de copy** como cuadros de texto nativos, ubicados
  en las coordenadas exactas medidas del navegador, con su tipografía, cuerpo,
  color, interlineado y los tramos en naranja respetados.

Así podés reescribir cualquier frase sin que se desarme el diseño. Lo que
está dentro del fondo (números y etiquetas del mapa, textos de los mockups,
el contador de página) no se edita acá: eso se cambia en el HTML.

Tipografías: Montserrat y Open Sans. Instalalas desde Google Fonts o
PowerPoint sustituye y el espaciado se corre un poco.

Falta pegar el **QR** en el slide 10 (hay un hueco esperándolo).

## Regenerar

```bash
cd deck-1pct/export
npm install playwright pptxgenjs

node capturar.js        # 11 fondos sin texto + textos.json con posiciones
node build-hibrido.js   # arma El-mapa-del-1-pct-EDITABLE.pptx
```

`capturar.js` decide qué es editable en la constante `EDITABLES`: son
selectores CSS del HTML. Si querés que un texto más pase a ser editable,
agregás su selector ahí.

### La otra versión (todo imagen)

```bash
node capture.js && node build.js
```

Los PNG intermedios y `textos.json` no se versionan.
