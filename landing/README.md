# Landing "Hackear tu vida" — 13 variantes por QR

Una sola pagina que cambia por completo segun el numero de QR que venga en la URL.

```
https://nicolasfernandezmiranda.com/HTV/          -> pagina general del libro
https://nicolasfernandezmiranda.com/HTV/?qr=1     -> contenido del QR 1
https://nicolasfernandezmiranda.com/HTV/?qr=7     -> contenido del QR 7
https://nicolasfernandezmiranda.com/HTV/?qr=13    -> contenido del QR 13
```

La landing se sube a la carpeta `/HTV/` del dominio.

Si el parametro falta, no es un numero o esta fuera de 1-13, se muestra la pagina general.

## Archivos

| Archivo | Que es |
|---|---|
| `index.html` | La landing completa (HTML + estilos + los 13 contenidos, todo en un archivo) |
| `codigos.html` | Lista los 13 enlaces listos para pegar en el generador de QR. Escribis el dominio y te arma las 13 URLs |
| `assets/logo.svg` | El logo. Mientras no este, la pagina muestra el wordmark "NFM" de respaldo |
| `qr/negro/` | Los 13 QR en negro sobre blanco, en SVG y PNG |
| `qr/azul-nfm/` | Los mismos 13 QR en azul NFM `#0c3452` sobre blanco |
| `qr/hoja-de-control.html` | Hoja imprimible con los 13 codigos y su enlace debajo, para revisar y pasarle al diseniador del libro |
| `qr/enlaces.json` | Los 13 enlaces en JSON, por si hace falta procesarlos |

## Cargar el contenido de un QR

Todo esta en el bloque `CONTENIDOS` dentro de `index.html`. Por defecto los 13 estan
en estado `proximamente`, que es el recuadro "Contenido disponible proximamente".

Para publicar uno, agregalo debajo del comentario `A PARTIR DE ACA SE EDITA CADA QR`:

```js
CONTENIDOS[1] = {
  etiqueta: "QR 01 - CAPITULO 1",
  titulo:   "Titulo del contenido",
  bajada:   ["Primer parrafo.", "Segundo parrafo."],
  estado:   "publicado",
  bloques:  [
    { titulo: "Video", texto: "Descripcion." },
    { titulo: "Ejercicio", texto: "Descripcion." }
  ],
  cta: { texto: "Ver el material", url: "https://..." }
};
```

Con `estado: "publicado"` desaparece el recuadro de proximamente y aparecen los
bloques y el boton naranja. Con `estado: "proximamente"` (o si no tocas nada)
se ve el recuadro.

El titulo del libro y el nombre del autor estan en las constantes `LIBRO` y `AUTOR`,
arriba de todo del script: se cambian en un solo lugar.

## Logo

Dejar el archivo en `assets/logo.svg` (tambien sirve `.png` cambiando la ruta en el
`<img>` de la cabecera). Se muestra a 46px de alto. Como el fondo es azul oscuro,
tiene que ser la version en blanco / clara del logo.

## Los codigos QR

Ya estan generados los 13, apuntando a `https://nicolasfernandezmiranda.com/HTV/?qr=N`.

- **Para la imprenta: usar los SVG.** Son vectoriales, no pierden definicion a ningun tamano.
- Los PNG son de 1230x1230 px, para pantalla o pruebas.
- **Tamano minimo impreso: 2 cm de lado.** Recomendado entre 2,5 y 3 cm.
- El margen blanco (zona de silencio) ya viene incluido: no recortarlo ni pegar nada contra el borde.
- Correccion de errores **nivel Q**: se leen con hasta un 25% de la superficie tapada o daniada.
- Los 26 archivos fueron verificados uno por uno: los 26 decodifican a la URL correcta.

Si cambia el dominio o la ruta, se regeneran con:

```bash
pip install segno
python3 -c "
import segno
for i in range(1,14):
    q = segno.make(f'https://nicolasfernandezmiranda.com/HTV/?qr={i}', error='q')
    q.save(f'qr/negro/qr-{i:02d}.svg', scale=10, border=4)
"
```

## Publicar

Son archivos estaticos, sin build ni dependencias (solo Google Fonts). Se sube la
carpeta tal cual a cualquier hosting estatico: Netlify, Vercel, Cloudflare Pages,
GitHub Pages o el hosting propio.
