# No estás roto — El combustible de tu cerebro

Juego interactivo (estilo Mario 2D) para Instagram sobre TDA y neurodiversidad.
Entregable de un solo archivo: `index.html` (autocontenido, sin dependencias).

## La idea

Se educa con la analogía de la **camioneta** que dio Soledad Funes: tu cerebro no
está roto, funciona distinto. El problema es el combustible que le cargás.

- **Nivel 1 — combustible equivocado:** "esforzate más", todo junto y en la cabeza,
  "sos un vago". La camioneta se ahoga, larga humo y no puede esquivar los obstáculos
  (entregas, reuniones, pendientes con deadline). Se queda sin combustible.
- **Puente:** *No sos vos, es el combustible.*
- **Nivel 2 — combustible correcto:** un solo foco por vez, el primer paso chiquito,
  cambiar la creencia. La misma camioneta ahora salta los mismos obstáculos.
- **Cierre:** reflexión + invitación a la clase del **martes 28 de julio, 19 hs (Arg)**
  con CTA a WhatsApp.

Contenido apoyado en la clase de Soledad Funes (deck del Día de la Neurodiversidad y
el TDA) y en la voz de marca NFM.

## Cómo se usa

Abrí `index.html` en cualquier navegador. Se juega tocando la pantalla para saltar.
Funciona en celular (portrait, ideal para Instagram) y en escritorio.

Para compartir: subilo a cualquier hosting estático (GitHub Pages, tu dominio,
link en bio) y pasá el link. Al final, el botón lleva al grupo de WhatsApp:
`https://go.wha.link/clase-28-7-neurociencia`

## Editar

Todo vive en `index.html`. Lo más probable de tocar:

- **Link de WhatsApp:** buscá `go.wha.link` (aparece en el botón `.wa`).
- **Fecha / hora / nombre de la clase:** están en la sección `data-s="final"`.
- **Los 3 combustibles** (equivocado / correcto): en las secciones `data-s="load1"`
  y `data-s="load2"`, y los mensajes del juego en las constantes `capsWrong` /
  `capsRight` del script.
- **Obstáculos:** constante `OBST` (`ENTREGA`, `REUNIÓN`, `PENDIENTES`).

Las fuentes NFM (Montserrat / Open Sans / JetBrains Mono) y el logo van embebidos en
base64, así que el archivo anda offline y en cualquier lado sin pedir nada externo.
