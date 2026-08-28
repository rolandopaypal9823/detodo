# Landing "Hackear tu vida" — 13 variantes por QR

Una sola pagina que cambia por completo segun el numero de QR que venga en la URL.

```
https://tudominio.com/          -> pagina general del libro
https://tudominio.com/?qr=1     -> contenido del QR 1
https://tudominio.com/?qr=7     -> contenido del QR 7
https://tudominio.com/?qr=13    -> contenido del QR 13
```

Si el parametro falta, no es un numero o esta fuera de 1-13, se muestra la pagina general.

## Archivos

| Archivo | Que es |
|---|---|
| `index.html` | La landing completa (HTML + estilos + los 13 contenidos, todo en un archivo) |
| `codigos.html` | Lista los 13 enlaces listos para pegar en el generador de QR. Escribis el dominio y te arma las 13 URLs |
| `assets/logo.svg` | El logo. Mientras no este, la pagina muestra el wordmark "NFM" de respaldo |

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

## Publicar

Son archivos estaticos, sin build ni dependencias (solo Google Fonts). Se sube la
carpeta tal cual a cualquier hosting estatico: Netlify, Vercel, Cloudflare Pages,
GitHub Pages o el hosting propio.
