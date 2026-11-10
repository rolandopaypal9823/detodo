# Thank you del booking funnel

`thankyou-booking.html` se pega entero en un widget HTML de GHL (bordes en 0, que ocupe toda la página), en el paso de gracias del Booking Funnel.

1. **¡Felicidades, Nombre!** Tu entrevista ya está agendada. Y 3 pasos:
   - Paso 1 · Listo: agendaste tu entrevista.
   - Paso 2 · Obligatorio para confirmar tu entrevista: el video de los 4 pilares de nuestros programas.
   - Paso 3: confirmá tu llamada por WhatsApp.
2. **Conocé casos de éxito del Instituto de Productividad:**
   - Así lo viven los alumnos en el último Mastermind presencial (video de Loom).
   - 12 entrevistas de alumnos en YouTube. Cada tarjeta abre el video.

## El video del paso 2

Está en vTurb (`vid-6af299dc5821dd130fe5d308`). El MP4 original en 1080p, por si hace falta otra vez:
https://embed-ssl.wistia.com/deliveries/9a5c3207572881c110d212e17b2119248afb4a62/vsl-4-pilares-1080p.mp4

El cartel del autoplay sale en portugués ("Seu vídeo já começou · Clique para ouvir"). Se cambia en vTurb, en la configuración del player.

## Webhook de FunnelChat

Al entrar con los datos de Calendly, la página manda un POST (JSON) a `FUNNELCHAT_WEBHOOK` (en el script) para que FunnelChat mande el video de presesión por WhatsApp. Se manda una sola vez por agendamiento, aunque la persona recargue. Si se entra sin datos de Calendly, no se manda nada.

Campos para mapear:

| Campo | Ejemplo |
|---|---|
| `telefono` | `5491100000000` (solo números, con código de país) |
| `telefono_original` | `+54 9 11 0000-0000` |
| `nombre` / `apellido` / `nombre_completo` | `Prueba` / `Booking` / `Prueba Booking` |
| `email` | `prueba@example.com` |
| `asesor` / `asesor_completo` | `Ayrton` |
| `fecha` / `hora` | `jueves 12 de noviembre` / `15:00` |
| `inicio` | `2026-11-12T15:00:00-03:00` |
| `tipo_de_evento` | nombre del evento de Calendly |
| `evento` | siempre `entrevista_agendada` |

Además va todo lo que mande Calendly con su nombre original (`answer_1`, `utm_source`, `invitee_uuid`…).

El teléfono sale de `text_reminder_number` (el recordatorio por SMS de Calendly). Si no viene, toma la primera respuesta (`answer_1` a `answer_10`) que sea un número. Para que llegue, el evento de Calendly tiene que pedir el teléfono, ya sea con el recordatorio por SMS o con una pregunta.

## Lo que lee de Calendly

- `invitee_first_name` → "¡Felicidades, Rolando!". Sin dato: "¡Felicidades!".
- `assigned_to` → "Confirmá tu llamada con Ayrton por WhatsApp". Sin dato, o un asesor que no está en la lista: "Confirmá tu llamada por WhatsApp".

Asesores en la lista (`ASESORES`, en el script del final): Luciana, Cristina, Pierina, Paula, Matías, Romina, Ayrton y Lucas. Para sumar uno: `nombre:'Nombre'`, con la clave en minúscula y sin tildes.

En Calendly, el evento tiene que tener activado pasar los datos del evento a la página de redirección, como ya está en `gracias-1`.
