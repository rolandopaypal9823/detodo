# Export a .pptx

`El-mapa-del-1-pct.pptx` — los 11 slides del deck, en 16:9 (13,33" × 7,5" = 1920×1080),
cada uno como imagen a doble resolución y **con las notas del presentador cargadas en
el panel de notas de PowerPoint / Keynote / Google Slides**.

Los slides son imágenes: se ven exactamente igual que el HTML (mapa, Mini Nico, mockups,
tipografías) pero el texto no se edita desde PowerPoint. Para cambiar copy se edita
`../deck-mapa-1-pct.html` y se vuelve a exportar.

## Volver a exportar

```bash
cd deck-1pct/export
npm install playwright pptxgenjs
node capture.js     # 11 PNG + meta.json (notas) desde el HTML
node build.js       # arma El-mapa-del-1-pct.pptx
```

Los PNG intermedios no se versionan.
