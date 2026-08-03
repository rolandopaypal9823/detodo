# NFM — Landing Madre · "El Viaje del Alto Rendimiento"

Entregable: **`landing-madre.html`** (single-file, sin dependencias salvo Google Fonts + Calendly).

Experiencia interactiva gamificada de ~3 min (misma **estructura de juego paso a paso** que la landing
de referencia de FlowScale), adaptada al nicho de NFM con la metáfora eje **"tu cerebro es el motor de
tu alto rendimiento"**. No vende directo: **califica/descalifica en silencio** y ramifica el cierre.

## Estructura (motor de 7 escenas + HUD "Nivel X/6") — 3 mini-juegos interactivos (CSS 3D, sin librerías)

| Nivel | Metáfora / pantalla | Qué hace la persona |
|---|---|---|
| **0 · Inicio** | Hero + demo de la batería drenándose | "Empezar el viaje" |
| **1 · La cabina** 🎮 | Cockpit 3D: girás la llave, el motor arranca **en reserva**, y **mantenés apretado el acelerador** → más esfuerzo = la batería se vacía más rápido | La lección del One Belief, en el cuerpo |
| **2 · El tablero** | Encuesta de 3 preguntas | **Califica / descalifica** |
| **3 · El enjambre** 🎮 | Juego imposible: tocás notificaciones para cerrarlas y **por cada una aparecen dos** → la energía se agota igual | "La voluntad pierde siempre; el sistema gana" → llamada + chat de Nico |
| **4 · La ruta** 🎮 | Carretera 3D: manejás y parás en las 4 estaciones (Energía · Foco · Sistema · Identidad) | Recorre el método |
| **5 · La bifurcación** | Dos rutas en 3D: reserva vs sistema | Compromiso |
| **6 · La recompensa** | **Ramifica según si calificó** (sin nombrarlo) | Cierre |

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
Probado end-to-end en Chromium en los **dos finales**: sin errores de JS, los 3 juegos se juegan
(encender+acelerar, enjambre hasta el final, 4 estaciones), el popup de Calendly abre y el ruteo
call/ebook funciona. Tracking incluye eventos de juego: `game[cabina:encender/leccion]`,
`game[enjambre]{cerradas,aparecieron}`, `game[ruta]{estacion}`. `?test` acelera todos los timings.
