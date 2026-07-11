# El ABC del Alto Rendimiento — página del curso (upsell)

Página de entrega estilo **Skool**, con la marca de Nico (NFM), para el upsell **El ABC del Alto Rendimiento**.

## Qué es

- **5 módulos** desplegables (accordion): Mindset · Hábitos · Ejercicio y Alimentación · Concentración · Memoria.
- **34 lecciones en video** (33 Looms + 1 bonus de YouTube), embebidas: cada lección abre su reproductor **dentro de la misma página**.
- **Carga lazy:** el iframe de cada video se inyecta recién al abrir la lección, así la página carga liviana aunque haya 34 videos.
- **Progreso** por módulo y global, con marca de "visto" por lección, guardado en el dispositivo (localStorage).
- **Recursos y entregables** por módulo (links a YouTube, Instagram, tests, libro, extensiones).

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La página lista para publicar (autocontenida: el logo va embebido en base64). |
| `build_abc.py` | Generador. Editás el contenido (módulos, lecciones, links) acá y corrés `python3 build_abc.py`. |
| `assets/` | Logos de origen (ya van embebidos en el HTML; la carpeta queda como respaldo). |

## Cómo editar

Todo el contenido está en la lista `MODULES` de `build_abc.py`. Cada lección es
`("Título", "loom"|"yt", "id_o_url", incluye_apunte📒)`. Después:

```
python3 build_abc.py   # regenera index.html
```

## Deploy

Es una sola página autocontenida. Igual que el reto: subís la carpeta `upsell-abc` a Netlify
(o servís solo `index.html` donde quieras). Sugerencia de dominio: `abc-alto-rendimiento-nfm.netlify.app`.

## Notas

- **Videos embebidos:** los Looms se embeben con `loom.com/embed/{id}` y el bonus con `youtube.com/embed/{id}`.
  Para que se vean, los Looms deben estar con visibilidad pública o "cualquiera con el link".
- **Entregables PDF de Skool:** los "Entregable N°..." viven dentro de Skool y no tienen link público,
  así que en la página aparecen marcados como *PDF · en Skool* (sin descarga directa). Si querés que se
  puedan descargar desde acá, hay que subir esos PDF a algún lado (Netlify, Drive público) y pasarme el link.
- **Módulos:** el pedido decía "4 módulos" pero el contenido entregado tiene 5. Están los 5. Si querés
  dejarlo en 4, decime cuáles fusiono/saco y lo ajusto en `build_abc.py`.
