# Portal de beneficios de la clase

Un solo sitio en Netlify. Dos páginas, una por asiento:

| Asiento | URL | Qué tiene |
|---|---|---|
| Básico · USD 1 | `clase-beneficios.netlify.app/asiento-basic` | La clase: workbook + grabación (con contador hasta que estén) |
| Hackea tu Productividad · USD 5 | `clase-beneficios.netlify.app/premium-htc` | Lo mismo + el ebook de «Hackea tu Cerebro» + el curso El ABC del Alto Rendimiento |

La raíz (`/`) no lista nada: dice que el acceso llegó por mail. Y `robots.txt` pide no indexar.

## Deploy

Arrastrar la carpeta `portal-beneficios` entera a Netlify (Sites → Add new site → Deploy manually),
o conectarla al repo con *publish directory* = `portal-beneficios`. Nombre del sitio: `clase-beneficios`.
Las URLs salen solas de la estructura de carpetas (`asiento-basic/index.html` → `/asiento-basic`).

## Cuando estén el workbook y la grabación

Editar `CFG` en `gen-portal.py` — `WORKBOOK_URL` y `GRABACION_URL` — y correr
`python3 portal-beneficios/gen-portal.py` desde la raíz del repo. Mientras estén vacíos, después
de la fecha el portal dice «lo estamos subiendo» en vez de mostrar un botón que no lleva a ningún lado.

Para probar el estado «ya disponible» sin esperar: agregar `?nfm_now=2026-10-08T12:01:00-03:00` a la URL.

## Ojo

Estas páginas no tienen contraseña: quien tenga el link, entra. Es el mismo criterio que el curso ABC.
Si algún día hace falta cerrarlas, lo más simple es la protección por contraseña de Netlify (plan pago) o
mover los archivos pesados a links que caduquen.
