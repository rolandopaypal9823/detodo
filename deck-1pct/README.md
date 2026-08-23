# Deck · "El mapa del 1%"

Slides del roadmap del lead para el cierre de la clase **"Escalá tu vida, no tu cansancio"**
(Instituto de Productividad · NFM).

## Archivos

| Archivo | Qué es |
|---|---|
| `deck-mapa-1-pct.html` | **El deck.** Un solo HTML autocontenido. Se abre con doble clic en cualquier navegador. |
| `whatsapp-confirmacion.html` | El mock de WhatsApp suelto, por si hace falta exportarlo a PNG para otro uso. |
| `assets/WhatsApp-Confirmacion.png` | Ese mismo mock ya exportado (1080×1350, @2x). |
| `assets/` | Acá van los screenshots que faltan (ver abajo). |

## Cómo se usa en vivo

- `→` / `barra espaciadora` / clic: avanzar · `←`: volver · `Home`: al principio
- `F`: pantalla completa (usar esto antes de compartir pantalla en Zoom)
- El cursor se esconde solo a los 3 segundos
- Refrescar no pierde el lugar: guarda el slide actual en `localStorage`
- Contador abajo a la derecha: `07 / 12`

**Ritmo:** 15-20 segundos por paso, tono "mirá lo simple que es". El único slide donde
conviene frenar y leer despacio es el **calificador** (slide 10), que es el que filtra.

## Orden de los 12 slides

1. Portada
2. Intro del mapa (todo apagado menos la estación 1)
3-9. Los 8 nodos (el nodo 8 tiene dos beats: puerta grande → puerta chica)
10. Calificador ("esto es para vos si…" / "no agendes si…")
11. CTA con el QR
12. Cierre (mapa entero encendido)

## Cómo se desbloquea el mapa

El mapa no se muestra entero de golpe. Funciona así:

- **Slide 2 (intro)** es el único que muestra el camino completo, todo apagado salvo la
  estación 1. Es el beat de "ocho pasos, mirá lo simple que es".
- **A partir de ahí** solo se ven las estaciones recorridas, la actual y **la siguiente**.
  El sendero punteado se asoma un tramo corto más y corta.
- Una **cámara** hace zoom sobre el tramo revelado y se va abriendo sola a medida que el
  camino crece. Al principio dos estaciones ocupan toda la pantalla; al final entran las ocho.
- El **cierre** vuelve a mostrar todo, ya recorrido.

Si alguna vez querés que el intro también arranque cerrado, en el array `SLIDES` sacale
`showAll:true` a la línea del `intro`.

## Pantallas del producto: ya están dibujadas

Las pantallas reales (formulario, calendario, página de gracias, autodiagnóstico, habit
tracker, insight) están **reconstruidas en HTML** dentro del deck, en el objeto `MOCKS`.
Se ven nítidas proyectadas y no dependen de ningún archivo.

Si preferís el screenshot real, poné el PNG en `assets/` con el nombre de la tabla y
**reemplaza solo al mockup** — no hay que tocar código.

| Archivo | Nodo | Hoy se ve |
|---|---|---|
| `SCREENSHOT-formulario.png` | 3 | mockup del form de Calendly |
| `SCREENSHOT-calendario.png` | 3 | mockup del calendario de Calendly |
| `SCREENSHOT-pagina-gracias.png` | 4 | mockup de la página de gracias |
| `SCREENSHOT-autodiagnostico.png` | 5 | mockup del autodiagnóstico |
| `SCREENSHOT-habit-tracker.png` | 6 | mockup de la sección del tracker |
| `SCREENSHOT-insight.png` | 6 | mockup del reporte de insight |

Hay un mockup extra ya hecho y sin usar: `loading` ("Estamos construyendo tu sistema…").
Para meterlo, cambiá el `mock2` de algún nodo por `"loading"`.

## Assets que sí faltan

| Archivo | Qué tiene que mostrar | Formato ideal |
|---|---|---|
| `SCREENSHOT-qr.png` | El QR real (o el botón/link del chat). Se usa en el nodo 2 y en el slide del CTA. | cuadrado, ≥1000×1000 |
| `mini-nico-videollamada.png` | Ilustración de Mini Nico en videollamada (nodo 7). | fondo blanco o transparente |
| `mini-nico-marker.png` | Recorte de Mini Nico con **fondo transparente**. Es el marcador que camina por el mapa. | PNG transparente, ~600px de alto |

Mientras `mini-nico-marker.png` no esté, el marcador es un pin naranja con las iniciales
"MN". Apenas aparezca el PNG, lo reemplaza solo.

## Editar los textos

Todo el contenido de los 8 pasos vive en el array `STATIONS`, arriba de todo del `<script>`
en `deck-mapa-1-pct.html`. Se cambian `title` y `copy` sin tocar nada del layout.
Las coordenadas del sendero están aparte, en `GEO`.
