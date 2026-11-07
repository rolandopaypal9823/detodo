# Thank you del booking funnel

`thankyou-booking.html` se pega entero en un widget HTML de GHL (bordes en 0, que ocupe toda la página), en el paso de gracias del Booking Funnel.

## Qué tiene, de arriba abajo

1. **El asesor asignado.** Igual que en `gracias-1`: "¡Felicitaciones, Nombre! Te va a contactar Lucas por WhatsApp", con foto y mensaje. Lee `assigned_to` e `invitee_first_name` de la URL, que los manda Calendly al redirigir. En Calendly, el evento tiene que tener activado pasar los datos del evento a la página de redirección, como ya está en `gracias-1`.
2. **El video obligatorio** antes de la sesión (el mismo Wistia de `gracias-1`).
3. **El fundador:** la historia de Nico en 5 escenas, en carrusel (como en `/webinar-cp`, con el texto un poco más largo, como en el webinar).
4. **Personas que estuvieron en tu mismo punto de partida:** los 14 alumnos de `/idp`, con nombre, oficio y una frase.
5. **Qué incluye el proceso:** coach 1 a 1, biblioteca de módulos, llamadas grupales, comunidad + mastermind presencial, equipo multidisciplinario y sistemas listos para usar (textos de `/idp`).
6. **La escalera:** "¿En qué escalón estás hoy?", con las bases abajo y el resto bloqueado, como la slide de la clase de la Comunidad.
7. **Cierre.**

Se sacaron el bloque del equipo y el quiz de casos de `gracias-1`.

## Asesores

Están Luciana, Cristina, Pierina, Paula, Matías, **Ayrton** y **Lucas**. Ayrton y Lucas todavía no tienen foto: sale la inicial en un círculo naranja. Para ponerla, pegá el link en `foto: ''` de cada uno (en `build.py` o directo en el HTML).

Si `assigned_to` trae un nombre que no está en la lista, o viene vacío, la página muestra la versión genérica ("un asesor del Instituto").

## Cómo se arma

`python3 build.py` desde esta carpeta. Toma `base-gracias-1-ghl.html` (el código de `gracias-1` tal cual está en GHL), deja los bloques 1 y 2, suma Ayrton y Lucas y pega `secciones-nuevas.html` abajo.
