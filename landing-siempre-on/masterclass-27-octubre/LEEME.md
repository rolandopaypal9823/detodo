# Masterclass del martes 27 de octubre · Comunidad Productiva

Landing de registro y thank you page de la clase gratuita **Cómo usar la neurociencia para concentrarte y dejar de procrastinar**, armadas con la estrategia v2 (`Contexto_Masterclass_Comunidad_27-10/01_estrategia_comunicacion_v2.md`).

| Archivo | Qué es |
|---|---|
| `index.html` | Landing de registro, variante popup. Cualquier botón abre el form de GHL directo. |
| `thankyou.html` | Thank you page: grupo de WhatsApp, calendario y la pregunta "¿Qué es lo que siempre te queda para después?". |
| `calendario-masterclass-27-oct.md` / `.ics` | Link de Google Calendar y archivo para iPhone/Outlook, para el grupo o los mails. |

En GHL va lo que está entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ». El pixel de la landing va en Settings → Tracking Code → HEAD, como siempre. El de la thank you ya viene adentro del custom code.

## Los dos títulos

- **Título de la landing:** "Neurociencia aplicada: cómo dejar de procrastinar, concentrarte y cumplir lo que planificás". Va en el hero y en el título de la pestaña.
- **Nombre de la clase:** "Cómo usar la neurociencia para concentrarte y dejar de procrastinar". Va en la thank you page, en el calendario, en el grupo de WhatsApp, en los recordatorios y en los anuncios. En la landing aparece en el cierre.

## La landing, de arriba abajo

Es la misma estructura que la landing de la clase del 21 (`../clase-21-octubre/index-popup.html`), con el mismo diseño. Cambian el tema, la explicación y la fecha.

1. **Cuenta regresiva y hero:** el título de la landing, "Neurociencia aplicada: cómo dejar de procrastinar, concentrarte y cumplir lo que planificás". Debajo, la pregunta del anuncio C2 ("¿Terminás la semana sin energía y con tus cosas igual que el lunes?"), una bajada corta y la fecha.
2. **Prensa y tráiler:** la misma cinta de logos y el mismo video de Loom.
3. **La semana**, en el lugar de la ecuación. Es corta:
   - el título "Cumpliste con todos. Tus cosas quedaron en cero.";
   - el cuadro "Una semana cualquiera": trabajo 50 h y tus cosas 0 a 2 h, los datos del anuncio C2;
   - el mecanismo en una línea: los 23 minutos por interrupción.
4. **Quién da la clase:** la historia de Nico en cinco escenas, igual que siempre. Sólo cambia la última línea, que habla del martes 27.
5. **Qué vas a aprender:** las 5 promesas, una por anuncio.
6. **Casos de éxito:** los mismos cuatro videos de siempre.
7. **Cierre** con botón y fecha.

No lleva precio ni menciona la Comunidad: la venta se hace en la clase.

## El registro

- **Sin preguntas.** Cualquier botón abre el popup con el form de GHL directo, para que el registro sea lo más rápido posible.
- El form se precarga cuando termina de cargar la página, así el popup abre listo.
- Al form le llegan `clase_fecha=2026-10-27`, `edicion=masterclass-oct27-comunidad` y todas las UTM. Si el lead llega sin UTM, se cargan `utm_source=directo` y `utm_campaign=masterclass-oct27-comunidad`.
- Sin la pregunta de etapa no hay forma de separar A, B y C en este registro.

## Antes de publicar

1. **Form de GHL.** El ID que quedó (`kLh5onxCgHdGDA10c8NU`) es el del form de las clases anteriores, y su redirección manda a la thank you del 21. Duplicalo para esta masterclass, poné la redirección a la thank you nueva y pegá el ID nuevo en los dos lugares: el iframe (`data-src`, `id`, `data-layout-iframe-id` y `data-form-id`) y `CONFIG.FORM_ID`. Revisá también la conversión por la API de Conversiones y los workflows (tags, mensajes de WhatsApp).
2. **Grupo de WhatsApp.** Ya está cargado en `CONFIG.WA` de la thank you (https://go.wha.link/clase-de-neurociencia-27-10) y en el calendario.
3. **Hora.** Quedó a las 19:00 (Argentina). Si cambia, tocá `HORA_CLASE` en la landing y en la thank you. El contador, las fechas, la hora local y el calendario de la thank you se recalculan solos. El `.md` y el `.ics` de esta carpeta hay que regenerarlos.
4. **La respuesta del paso 3.** Necesita una URL que la reciba: un webhook de Zapier o Make, un Inbound Webhook de GHL o un Apps Script. Va en `CONFIG.RESPUESTA_WEBHOOK`. Mientras esté vacío, la página agradece igual pero la respuesta no se guarda.
   - La página manda: clase, respuesta, email, teléfono, nombre, UTM, página y fecha.
   - Email, teléfono y nombre salen de la URL, así que en GHL activá que la redirección pase los datos del contacto (`email`, `phone`, `name`).
5. **Fotos y videos.** Son los mismos de la landing del 21: las fotos de nicolasfernandezmiranda.com, el tráiler de Loom y los casos en YouTube.

## Lo que queda afuera hasta que se defina

- **Asiento premium en la thank you.** No está. Si se suma, que no compita con la Comunidad: grabación y workbook alcanzan.
- **Psicólogos, nutricionistas y coaches** (anuncio C5). No se mencionan hasta confirmar que están en la oferta.
- **Escasez** (USD 35 hasta 1.000 personas). Es de la clase y de la página de pago, no de esta landing.
