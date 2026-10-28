# Clase del miércoles 4 de noviembre · 19:00 hs (Argentina)

**Neurociencia para el Alto Rendimiento Profesional.** Es el mismo webinar del 21/10 con otra fecha. Mismo diseño, misma historia de Nico, mismos casos, mismo quiz y la misma oferta de asientos (USD 5 y USD 9).

## Landings de registro (esta carpeta)

| Archivo | Cómo se registra la gente |
|---|---|
| `index-popup.html` | **Con popup.** Cualquier botón abre el quiz y el form en un popup. Se cierra sólo con la X. |
| `index.html` | Con el quiz y el form en la página. Los botones bajan hasta ahí. |

Salen de las del 21 con `build-desde-clase-21.py`. Si se cambia algo en las del 21, se corre de nuevo desde la raíz del repo: `python3 landing-siempre-on/clase-04-noviembre/build-desde-clase-21.py`.

Qué cambió respecto de la del 21:

1. **Fecha y UTM:** la fecha es `2026-11-04` y la UTM `clase-nov04-alto-rendimiento`. Esa UTM va en el `utm_campaign` de los leads sin UTM, en `edicion` y en `clase_fecha` del form. El contador, la píldora, los textos y la hora local se arman solos con esa fecha.
2. **Pixel de Meta adentro del bloque** que se pega en GHL, así viaja con el pegado. Si además está en Settings → Tracking Code → HEAD, el del bloque no se dispara y Meta no cuenta dos veces. La conversión (Lead) la sigue mandando GHL por la API de Conversiones.
3. **Opción A del quiz:** dice "la mente que no se apaga" en lugar de "la cabeza", por la regla de marca. Si la imagen de esa opción tiene el texto escrito, también hay que cambiarla.

Los forms de GHL son los mismos del 21: "Form AGOSTO NUEVO" para las etapas A y B, y "FORM PARA COMUNIDAD" para la C. Su redirección tiene que ir a la thank you de registro (`nfm-clase-paga/thankyou-oto.html` o la versión sin popup).

## Lo demás que se actualizó para el 4/11

| Pieza | Archivo | Qué cambió |
|---|---|---|
| Thank you de registro con asientos | `nfm-clase-paga/thankyou-oto.html` | Fecha, UTM, grupo `clase-de-neurociencia-04-11` (también escrito directo en el botón) y la referencia de Stripe, que ahora termina en `-nov04`. |
| Thank you de registro sin asientos | `nfm-clase-paga/thankyou-registro-sin-popup.html` | La misma, sin el popup (`gen-thankyou-sin-popup.py`). |
| Thank you de compra USD 5 y USD 9 | `nfm-clase-paga/thankyou-compra-{basic,premium}.html` | Fecha y grupo del 4/11 (`gen-thankyou-compra.py`). |
| Mails de compra | `nfm-clase-paga/mail-compra-{basic,premium}.html` | "Miércoles 4 de noviembre" y el grupo del 4/11 (`gen-mail-compra.py`). |
| Portal de beneficios | `portal-beneficios/clase-beneficios/` | `/asiento-basic/` y `/premium-htc/` son ahora de la clase del 4/11. Lo del 21 quedó en `/clase-21/…` y lo del 7 sigue en `/clase-7/…`. Las páginas nuevas llevan abajo los links a las dos clases anteriores. |
| Mails de grabación del 21 | `nfm-clase-paga/mail-grabacion-21oct-{basic,premium}.html` | Ahora mandan a `/clase-21/…`. |
| Calendario | `calendario-clase-04-nov.md` / `.ics` | Link de Google Calendar y archivo para iPhone/Outlook, con la puerta al Zoom y el grupo del 4/11. |

Los links de pago de Stripe (USD 5 y USD 9) son los mismos del 21.

## Antes de publicar

1. **Subir el portal** a Netlify: la carpeta `clase-beneficios` entera, así quedan las rutas `/clase-21/` y `/clase-7/`. Subilo antes de que entre la primera compra del 4/11.
2. **La puerta al Zoom** (`zoom-nfm.netlify.app`): actualizar el link de Zoom y la clave anti-duplicados para esta clase. El calendario manda ahí.
3. **El tráiler de Loom:** es el mismo del 21. Recordá que la velocidad 1x se fija en Loom → Settings → Audience.

## Después de la clase

Cargar el workbook (link de Drive) y la grabación (código de Loom) en la edición del 4/11 de `portal-beneficios/gen-portal.py`, correrlo y subir la carpeta. El portal pasa a "ya disponible" el jueves 5 a las 12:00.
