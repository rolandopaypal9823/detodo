# Thank you del booking funnel

`thankyou-booking.html` se pega entero en un widget HTML de GHL (bordes en 0, que ocupe toda la página), en el paso de gracias del Booking Funnel.

## Qué tiene, de arriba abajo

1. **El asesor asignado**, como en `gracias-1`: "¡Felicitaciones, Nombre! Te va a contactar Lucas por WhatsApp". Lee `assigned_to` e `invitee_first_name` que manda Calendly.
2. **El video** antes de la sesión (el mismo Wistia).
3. **Nico:** su historia en 5 líneas, sin fotos.
4. **Estuvieron donde estás vos:** 12 frases de alumnos, con nombre y oficio.
5. **Qué incluye:** 6 ítems, sin explicación.
6. **¿En qué escalón estás?:** la escalera, con las bases abajo y el resto bloqueado.

Corta y sin fotos nuevas. Se sacaron el equipo, el quiz de casos y los textos de apoyo de `gracias-1`.

## Asesores

Están Luciana, Cristina, Pierina, Paula, Matías, **Ayrton** y **Lucas**. Ayrton y Lucas van sin foto: sale la inicial en un círculo naranja.

Si `assigned_to` trae un nombre que no está en la lista, o viene vacío, la página muestra la versión genérica ("un asesor del Instituto").

## Cómo se arma

`python3 build.py` desde esta carpeta. Toma `base-gracias-1-ghl.html` (el código de `gracias-1` tal cual está en GHL), deja los bloques 1 y 2, suma Ayrton y Lucas y pega `secciones-nuevas.html` abajo.
