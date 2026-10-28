# Baúl de beneficios · clase-beneficios.netlify.app

Un solo sitio. Se sube arrastrando la carpeta `clase-beneficios` entera a Netlify (el sitio → Deploys).

| Ruta | Qué es |
|---|---|
| `/asiento-basic/` | Clase del miércoles 4 de noviembre · USD 5 — workbook + grabación |
| `/premium-htc/` | Clase del miércoles 4 de noviembre · USD 9 — lo mismo + ebook + curso ABC |
| `/clase-21/asiento-basic/` | Clase del 21/10 · lo que compraron entonces (workbook + grabación cargados) |
| `/clase-21/premium-htc/` | Clase del 21/10 · lo mismo + ebook + curso ABC |
| `/clase-7/asiento-basic/` | Clase del 7/10 · workbook + grabación cargados |
| `/clase-7/premium-htc/` | Clase del 7/10 · lo mismo + ebook + curso ABC |

Las páginas de la clase del 4/11 llevan abajo un aviso con los links a `/clase-21/…` y `/clase-7/…`, porque los mails
de las clases anteriores mandan a las rutas de arriba.

## Cuando estén el workbook y la grabación del 4/11

Editar la edición del 4/11 en `gen-portal.py` (`WORKBOOK_URL` y `GRABACION_LOOM`), correr
`python3 portal-beneficios/gen-portal.py` desde la raíz del repo y volver a subir la carpeta.
La página no muestra ninguna hora (dice «después de la clase del miércoles»); por dentro cambia de estado el
jueves 5 de noviembre a las 12:00. Sin links cargados, a esa hora dice «lo estamos subiendo», nunca un botón roto.

Para probar el estado «ya disponible» sin esperar: agregar `?nfm_now=2026-11-05T12:01:00-03:00` a la URL.

## Ojo

Sin contraseña: quien tenga el link entra. Llevan noindex y robots.txt para que no las levante Google.
