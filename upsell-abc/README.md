# El ABC del Alto Rendimiento — página del curso (upsell)

Página de entrega tipo **plataforma de curso** (classroom), con la marca de Nico (NFM), para el upsell **El ABC del Alto Rendimiento**.

## Diseño (skill awesome-design)

- **Esqueleto:** layout de **Mintlify** (documentación/aprendizaje) → **sidebar de navegación fijo** con los módulos y lecciones + **panel principal** donde se carga la lección elegida. Es el patrón de las plataformas de curso profesionales (y del classroom de Skool).
- **Piel:** identidad **NFM en su versión OSCURA** (estética de la Masterclass de Neurociencia) — fondo abismo `#06192b` con **red neuronal animada** (canvas), Naranja Acción `#ff6602` como único acento, Montserrat + Open Sans + **JetBrains Mono** para etiquetas, marco de video con **glow y esquinas** naranjas.

## Qué es

- **6 módulos** (Mindset · Hábitos · Sueño y Descanso · Ejercicio y Alimentación · Concentración · Memoria) con secciones, en el sidebar colapsable.
- **41 lecciones en video** (Looms + 1 bonus de YouTube). Clic en una lección → su video se carga en el **reproductor principal** (no todo a la vez).
- **Carga lazy:** el iframe se inyecta al seleccionar la lección, así la página vuela.
- **Progreso** por módulo y global (barra en el sidebar y en el topbar), con "marcar visto" por lección, guardado en el dispositivo (localStorage). **Recuerda la última lección vista.**
- **Prev / Siguiente**, breadcrumb (módulo › sección), y **drawer** en mobile.
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
- **⚠️ Entregables PDF (links firmados de Skool):** los 6 PDF (`Entregable N°...` + Planillas Hábitos) usan
  links firmados de `files.skool.com` que **caducan ~21/04/2026** (parámetro `Expires`). Después de esa fecha
  dejan de funcionar y hay que **regenerarlos desde Skool** y volver a pegarlos en `build_abc.py` (campo `recursos`),
  o —mejor a largo plazo— subir los PDF a un hosting propio (Netlify/Drive) y usar ese link permanente.
- **Fondo neuronal:** el canvas se desactiva solo si el usuario tiene `prefers-reduced-motion` (accesibilidad).
