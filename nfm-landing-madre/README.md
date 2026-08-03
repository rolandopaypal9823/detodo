# NFM — Landing Madre · "El Viaje del Alto Rendimiento"

Entregable: **`landing-madre.html`** (single-file, sin dependencias salvo Google Fonts + Calendly).

Experiencia interactiva gamificada de ~3 min (misma **estructura de juego paso a paso** que la landing
de referencia de FlowScale), adaptada al nicho de NFM con la metáfora eje **"tu cerebro es el motor de
tu alto rendimiento"**. No vende directo: **califica/descalifica en silencio** y ramifica el cierre.

## Estructura (motor de 7 escenas + HUD "Nivel X/6")

| Nivel | Metáfora / pantalla | Qué hace la persona |
|---|---|---|
| **0 · Inicio** | Hero + demo de la batería del cerebro drenándose (apps en 2° plano) | "Empezar el viaje" |
| **1 · El motor** | Enciende el motor → ve que está en reserva → por qué (apps en 2° plano) | Instala el One Belief |
| **2 · El tablero** | Encuesta de 3 preguntas (profesión · dolor · momento) | **Califica / descalifica** |
| **3 · El mensaje** | Llamada entrante + chat de Nico (estilo WhatsApp) | No es info, es sistema + acompañamiento |
| **4 · La travesía** | 4 estaciones/pilares: Energía · Foco · Sistema · Identidad | Recorre el método |
| **5 · La decisión** | Dos caminos: seguir en reserva vs operar a favor del cerebro | Compromiso |
| **6 · La recompensa** | **Ramifica según si calificó** | Cierre |

## Ramificación del cierre (Nivel 6)
- **Califica** → invitación a **agendar entrevista** (popup de Calendly, cierra solo con la X).
- **No califica** → **ebook de Desintoxicación Digital**.
- **Siempre** → botón **"Unite a mi próxima clase online"**.

**Regla de calificación** (`qualifies()`): descalifica si es **estudiante** o eligió **"prefiero lo
gratuito"**; todos los demás califican → call.

## Configuración (arriba del `<script>`, en `CFG`)
- `EBOOK_URL` → `mba.nicolasfernandezmiranda.com/ebook`
- `CLASE_URL` → `mba.nicolasfernandezmiranda.com/webinar`
- `CALENDLY_URL` → entrevista de admisión (UTMs: `utm_source=landing-madre`)
- `TRACK_ENDPOINT` → el mismo Google Sheet que el test (eventos con `source: "landing-madre"`)
- `?test` en la URL → colapsa los timings de animación (para revisar rápido)

## Contenido como datos (editable sin tocar la mecánica)
- `SURVEY` → las 3 preguntas de la encuesta.
- `PILARES` → las 4 estaciones del método.
- El guion del chat de Nico está en `chatRun()`.
- El "feel" de juego: `shake()`+vibración, glows pulsantes, `countTo()`, transiciones `wipeTo()`.

## Verificación
Probado end-to-end en Chromium en los **dos finales**: sin errores de JS, las 7 escenas avanzan, la
encuesta califica/descalifica bien, el popup de Calendly abre, y el ruteo call/ebook funciona. Tracking:
`load → start_viaje → nivel×6 → answers → call → decision → result → cta_click`. *(En el sandbox no
cargan Google Fonts ni Calendly; el logo va embebido. En producción cargan normal.)*
