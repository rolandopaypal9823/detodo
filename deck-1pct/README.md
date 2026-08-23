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

## Assets que faltan

Poné los archivos con **exactamente estos nombres** dentro de `assets/`. El deck los toma
solo, sin tocar código. Mientras no estén, se ve un recuadro punteado con el nombre del
archivo (el deck igual queda presentable para ensayar).

| Archivo | Qué tiene que mostrar | Formato ideal |
|---|---|---|
| `SCREENSHOT-qr.png` | El QR real (o el botón/link del chat). Se usa en el nodo 2 y en el slide del CTA. | cuadrado, ≥1000×1000 |
| `SCREENSHOT-formulario.png` | El formulario de agenda, con una o dos preguntas visibles. | vertical o cuadrado |
| `SCREENSHOT-pagina-gracias.png` | La página de gracias con el material de preparación. | apaisado |
| `SCREENSHOT-autodiagnostico.png` | El autodiagnóstico (test-presesion.netlify.app). | vertical |
| `SCREENSHOT-habit-tracker.png` | El habit tracker, idealmente el reporte semanal/mensual. | apaisado |
| `mini-nico-videollamada.png` | Ilustración de Mini Nico en videollamada (nodo 7). | fondo blanco o transparente |
| `mini-nico-marker.png` | Recorte de Mini Nico con **fondo transparente**, medio cuerpo o figura entera. Es el marcador que camina por el mapa. | PNG transparente, ~600px de alto |

Sobre los screenshots: alcanza con capturas de pantalla comunes. Recortá el navegador
(barra de direcciones, pestañas, favoritos) y dejá solo la pantalla. No hace falta que
tengan el mismo tamaño entre sí: cada uno se ajusta solo dentro de su marco.

Mientras `mini-nico-marker.png` no esté, el marcador es un pin naranja con las iniciales
"MN". Apenas aparezca el PNG, lo reemplaza solo.

## Editar los textos

Todo el contenido de los 8 pasos vive en el array `STATIONS`, arriba de todo del `<script>`
en `deck-mapa-1-pct.html`. Se cambian `title` y `copy` sin tocar nada del layout.
Las coordenadas del sendero están aparte, en `GEO`.
