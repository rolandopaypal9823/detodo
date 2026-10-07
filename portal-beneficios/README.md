# Baúl de beneficios · clase del miércoles 14 de octubre

Dos sitios en Netlify, uno por asiento. Cada carpeta se sube sola (Add new site → Deploy manually → arrastrar la carpeta):

| Carpeta | Sitio en Netlify | Asiento |
|---|---|---|
| `asiento-basic-14/` | `asiento-basic-14.netlify.app` | Básico · USD 1 — workbook + grabación |
| `asiento-premium-14/` | `asiento-premium-14.netlify.app` | Hackea tu Productividad · USD 5 — lo mismo + ebook + curso ABC |

El nombre del sitio en Netlify tiene que ser exactamente ese: las thank you de compra y los mails apuntan ahí.

## Cuando estén el workbook y la grabación

Editar `CFG` en `gen-portal.py` — `WORKBOOK_URL` y `GRABACION_URL` — correr
`python3 portal-beneficios/gen-portal.py` desde la raíz del repo, y volver a subir las dos carpetas.
La página no muestra ninguna hora (dice «después de la clase del miércoles»); por dentro cambia de estado en `LISTO`
(jueves 15 a las 12:00, hora Argentina). Sin links cargados, a esa hora dice «lo estamos subiendo», nunca un botón roto.

Para probar el estado «ya disponible» sin esperar: agregar `?nfm_now=2026-10-15T12:01:00-03:00` a la URL.

## Ojo

Sin contraseña: quien tenga el link entra. Llevan noindex y robots.txt para que no las levante Google.
