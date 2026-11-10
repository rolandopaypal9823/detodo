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

Hoy está el de Wistia (`tdrkk8cd9a`, 7:51). Para subirlo a vTurb, el MP4 en 1080p se baja de acá:

https://embed-ssl.wistia.com/deliveries/9a5c3207572881c110d212e17b2119248afb4a62/vsl-4-pilares-1080p.mp4

Cuando esté en vTurb: buscá el comentario `VIDEO DEL PASO 2` y reemplazá el `<iframe>` que está adentro de `<div class="nfm-ty__video">` por el código de vTurb. El div le da el formato 16:9.

## Lo que lee de Calendly

- `invitee_first_name` → "¡Felicidades, Rolando!". Sin dato: "¡Felicidades!".
- `assigned_to` → "Confirmá tu llamada con Ayrton por WhatsApp". Sin dato, o un asesor que no está en la lista: "Confirmá tu llamada por WhatsApp".

Asesores en la lista (`ASESORES`, en el script del final): Luciana, Cristina, Pierina, Paula, Matías, Romina, Ayrton y Lucas. Para sumar uno: `nombre:'Nombre'`, con la clave en minúscula y sin tildes.

En Calendly, el evento tiene que tener activado pasar los datos del evento a la página de redirección, como ya está en `gracias-1`.
