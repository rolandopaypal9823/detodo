# Masterclass del martes 27 de octubre · Comunidad Productiva

Landing de registro y thank you page de la clase gratuita **Neurociencia de la productividad**, armadas con la estrategia v2 (`Contexto_Masterclass_Comunidad_27-10/01_estrategia_comunicacion_v2.md`).

| Archivo | Qué es |
|---|---|
| `index.html` | Landing de registro, variante popup. Cualquier botón abre el registro: una pregunta de etapa y el form de GHL. |
| `thankyou.html` | Thank you page: grupo de WhatsApp, calendario y la pregunta "¿Qué es lo que siempre te queda para después?". |
| `calendario-masterclass-27-oct.md` / `.ics` | Link de Google Calendar y archivo para iPhone/Outlook, para el grupo o los mails. |

En GHL va lo que está entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ». El pixel de la landing va en Settings → Tracking Code → HEAD, como siempre. El de la thank you ya viene adentro del custom code.

## La landing, de arriba abajo

Sigue los tres tiempos del núcleo: espejo, mecanismo y la clase.

1. **Hero:** "¿Terminás la semana sin energía y con tus cosas igual que el lunes?", el eco del anuncio C2. Debajo, el título de la clase y la bajada de la estrategia.
2. **Prensa:** la misma cinta de logos de las clases anteriores.
3. **Espejo:** el domingo a la noche, con el texto de C2 y el dato de 0 a 2 horas por semana para tus cosas.
4. **Mecanismo:** los tres datos (23 minutos por interrupción, el plan escrito y la semana perfecta que no existe).
5. **En la clase vas a ver:** las 5 promesas, una por anuncio.
6. **Para quién es:** trabajás, estudiás, tenés hijos o un proyecto propio, y cumplís con todos menos con vos.
7. **Quién es Nico:** versión corta.
8. **Cierre** con botón y fecha.

No lleva precio ni menciona la Comunidad: la venta se hace en la clase. Tampoco usa frases de leads con nombre.

## El registro

- Una sola pregunta, la de etapa A, B o C, de un clic y obligatoria. Al elegir, pasa directo al form. El form es el mismo para todos.
- Al form le llegan `etapa`, `clase_fecha=2026-10-27`, `edicion=masterclass-oct27-comunidad` y todas las UTM. Si el lead llega sin UTM, se cargan `utm_source=directo` y `utm_campaign=masterclass-oct27-comunidad`.
- La etapa queda guardada en el navegador para la thank you page.
- **Un cambio en las opciones:** la opción A decía "la cabeza que no se apaga" y ahora dice **"la mente que no se apaga"**, por la regla de nunca usar "cabeza". Las otras dos están igual que el 7/10. Si la imagen de esa opción tiene el texto escrito adentro, también hay que cambiarla.
- Se sacaron la pregunta del equipo, la de "a qué te dedicás" y el form aparte de Comunidad para la etapa C.

## Antes de publicar

1. **Form de GHL.** El ID que quedó (`kLh5onxCgHdGDA10c8NU`) es el del form de las clases anteriores, y su redirección manda a la thank you del 21. Duplicalo para esta masterclass, poné la redirección a la thank you nueva y pegá el ID nuevo en los dos lugares: el iframe (`data-src` y `data-form-id`) y `CONFIG.FORM_ID`. Revisá también la conversión por la API de Conversiones y los workflows (tags, mensajes de WhatsApp).
2. **Grupo de WhatsApp.** Cargalo en `CONFIG.WA` de la thank you. Mientras esté vacío, la página muestra una barra naranja de aviso y el botón no manda a ningún lado.
3. **Hora.** Quedó a las 19:00 (Argentina). Si cambia, tocá `HORA_CLASE` en la landing y en la thank you. El contador, las fechas, la hora local y el calendario de la thank you se recalculan solos. El `.md` y el `.ics` de esta carpeta hay que regenerarlos.
4. **La respuesta del paso 3.** Necesita una URL que la reciba: un webhook de Zapier o Make, un Inbound Webhook de GHL o un Apps Script. Va en `CONFIG.RESPUESTA_WEBHOOK`. Mientras esté vacío, la página agradece igual pero la respuesta no se guarda.
   - La página manda: clase, respuesta, etapa, email, teléfono, nombre, UTM, página y fecha.
   - Email, teléfono y nombre salen de la URL, así que en GHL activá que la redirección pase los datos del contacto (`email`, `phone`, `name`).
5. **Fotos.** Usan las mismas URLs de nicolasfernandezmiranda.com: la del TED en el hero y la del libro en "Quién es Nico".

## Lo que queda afuera hasta que se defina

- **Asiento premium en la thank you.** No está. Si se suma, que no compita con la Comunidad: grabación y workbook alcanzan.
- **Psicólogos, nutricionistas y coaches** (anuncio C5). No se mencionan hasta confirmar que están en la oferta.
- **Caso de éxito y escasez** (USD 35 hasta 1.000 personas). Son de la clase y de la página de pago, no de esta landing.
