# Thank you del booking funnel

`thankyou-booking.html` se pega entero en un widget HTML de GHL (bordes en 0, que ocupe toda la página), en el paso de gracias del Booking Funnel.

1. **¡Felicitaciones, Nombre!** y 3 pasos:
   - Paso 1 · Completado: agendar tu sesión.
   - Paso 2 · Ahora: confirmar tu sesión con el asesor por WhatsApp.
   - Paso 3: mirar el material que le compartimos por WhatsApp.
2. **Personas que ya pasaron por el Instituto de Productividad:** 12 alumnos con la miniatura de su entrevista de YouTube, la frase, el nombre y el oficio. Cada tarjeta abre el video en YouTube.

## Lo que lee de Calendly

- `invitee_first_name` → "¡Felicitaciones, Rolando!". Sin dato: "¡Felicitaciones!".
- `assigned_to` → "Confirmar tu sesión con Ayrton por WhatsApp". Sin dato, o un asesor que no está en la lista: "Confirmar tu sesión por WhatsApp".

Asesores en la lista (`ASESORES`, en el script del final): Luciana, Cristina, Pierina, Paula, Matías, Romina, Ayrton y Lucas. Para sumar uno: `nombre:'Nombre'`, con la clave en minúscula y sin tildes.

En Calendly, el evento tiene que tener activado pasar los datos del evento a la página de redirección, como ya está en `gracias-1`.
