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

## Orden de los 11 slides

1. Portada
2. Intro del mapa — las 3 estaciones apagadas, Mini Nico en "estás acá"
3-4. **Paso 01 · Tu 1%** — el link del chat / 90 segundos de preguntas
5-6. **Paso 02 · Pasa solo** — tu asesor te escribe / se desbloquean tus recursos
7-8. **Paso 03 · La decisión** — la llamada / la puerta (grande + chica)
9. Calificador
10. CTA con el QR
11. Cierre

El mapa tiene **3 estaciones**, no ocho. Cada una se despliega en 2 sub-momentos que
cambian el panel de abajo sin que el mapa avance — los puntitos al lado del "PASO 0X"
muestran en cuál de los dos estás. Así el camino *se ve* corto, que es lo que hace que
agendar se sienta chico.

El punto de partida ("estás acá") es un punto chico, no una estación: no es un paso del
camino, es dónde está parado hoy.

## Cómo funciona el mapa

Es **un solo componente**. Avanzar no lo redibuja: solo cambia el estado de cada estación
(apagada / recorrida / actual), estira el camino naranja y desliza a Mini Nico. El naranja
solo crece: una estación recorrida nunca vuelve a apagarse.

Una cámara encuadra el mapa entero y lo ajusta sola al alto de la banda, así que si algún
día agregás o sacás una estación en `PT` + `STATIONS`, se reacomoda sin tocar el layout.

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
