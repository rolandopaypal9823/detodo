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
| `elementor.html` | **La version para pegar en Elementor.** Es la que hay que usar si la pagina se monta en WordPress |
| `index.html` | La misma landing como archivo suelto, para hosting estatico o para abrirla y probarla en local |
| `codigos.html` | Lista los 13 enlaces listos para pegar en el generador de QR. Escribis el dominio y te arma las 13 URLs |
| `assets/logo.svg` | El logo. Mientras no este, la pagina muestra el wordmark "NFM" de respaldo |
| `qr/negro/` | Los 13 QR en negro sobre blanco, en SVG y PNG |
| `qr/azul-nfm/` | Los mismos 13 QR en azul NFM `#0c3452` sobre blanco |
| `qr/hoja-de-control.html` | Hoja imprimible con los 13 codigos y su enlace debajo, para revisar y pasarle al diseniador del libro |
| `qr/enlaces.json` | Los 13 enlaces en JSON, por si hace falta procesarlos |

## Montarla en Elementor

Usar `elementor.html`, no `index.html`.

1. En la pagina, poner un widget **HTML**.
2. Pegar adentro **todo** el contenido de `elementor.html`, reemplazando lo que hubiera.
3. En el contenedor que envuelve al widget: ancho **Completo** y padding en 0.
4. En la pagina: layout **Lienzo de Elementor** o **Ancho completo**.

Por que no sirve pegar `index.html` en Elementor: ese archivo es un documento
completo, con `<html>`, `<head>` y `<body>`. WordPress descarta esas etiquetas
pero deja el CSS suelto, asi que la regla `body{background:azul; color:blanco}`
no llega a pintar el fondo (el tema ya tiene el suyo) pero si pinta el texto de
blanco. Queda texto blanco sobre fondo blanco y ademas se desconfigura el resto
del sitio.

`elementor.html` esta hecho para eso: no lleva `<html>/<head>/<body>`, todo el
CSS esta encerrado en `#htv-app` (no toca ni un estilo del resto de la pagina) y
el bloque se estira solo a todo el ancho de la pantalla aunque el contenedor de
Elementor sea angosto. Si NO se quiere a todo el ancho, se borran las 5 lineas
marcadas como `ANCHO COMPLETO` arriba del CSS.

El logo se toma de `/wp-content/uploads/logo-nfm-blanco.svg`. Subir el logo a la
biblioteca de medios de WordPress y ajustar esa ruta en el `<img>`. Mientras
tanto se ve el wordmark "NFM" de respaldo.

## Cargar el contenido de un QR

Todo esta en el bloque `CONTENIDOS`. Esta igual en `elementor.html` y en
`index.html`: hay que editarlo en el archivo que se este usando. Por defecto los 13 estan
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
