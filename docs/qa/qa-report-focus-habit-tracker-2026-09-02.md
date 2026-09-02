# QA — Focus Habit Tracker

- **Fecha:** 2026-09-02
- **Rama:** `claude/habits-management-mvp-iu9gyi` (base: `main`)
- **Modo:** diff-aware sobre la rama, tier Standard (arregla critical + high + medium)
- **Target:** app estática servida en `http://localhost:8471` desde `focus-habit-tracker/`
- **Framework:** vanilla JS + HTML/CSS, sin build. PWA con service worker.
- **Navegador:** Chromium 151 vía Playwright

## Resumen

| | Baseline | Final |
|---|---|---|
| **Health score** | **92** | **96** |
| Issues abiertos | 3 | 0 |
| Tests del repo | 0 | 48 |
| Primer pintado | 12 454 ms | 74 ms |

3 issues encontrados, 3 arreglados y verificados. Ninguno diferido por no poder
arreglarse. La app no tenía tests propios en el repo: ahora tiene 48.

**PR summary:** QA encontró 3 issues, arregló 3, health score 92 → 96.

## Top 3 arreglados

### ISSUE-001 — La app tardaba 12 s en pintar si Google Fonts no respondía
- **Severidad:** high · **Categoría:** performance · **Estado:** verified
- **Commit:** `b74f7b4` · **Archivos:** `index.html`, `css/styles.css`, `sw.js`

La hoja de estilos de Google Fonts estaba en el `<head>` como render-blocking.
En cualquier red que no la alcance (móvil lenta, offline, o redes donde Google
está bloqueado) el navegador espera el timeout de conexión antes de dibujar:
pantalla en blanco.

**Medición:** 12 454 ms hasta DOMContentLoaded, contra 63 ms cortando esa única
petición. El service worker no podía compensarlo porque esa hoja nunca estuvo
en el precache, lo cual contradecía la promesa de la propia PWA ("abre al
instante").

**Arreglo:** el `<link>` pasa a `media="print"` + swap a `media="all"` en
`onload`, con `<noscript>` de respaldo. Los stacks tipográficos suman fuentes
de sistema reales en vez de caer a la genérica `sans-serif`.

**Verificación:** 12 454 ms → **48 ms** (260×), sin errores de consola y sin
cambio visual en la pantalla de bienvenida.

### ISSUE-002 — Un nombre de hábito largo rompía el layout en mobile
- **Severidad:** medium · **Categoría:** visual · **Estado:** verified
- **Commit:** `0b57a88` · **Archivos:** `css/styles.css`

Un nombre sin espacios (o una URL pegada) hacía que la fila de "Hábitos de hoy"
midiera **750 px dentro de un viewport de 375 px**: scroll horizontal en toda
la página. En una PWA pensada para el celular, es la pantalla principal rota.

**Causa raíz:** los ítems flex arrancan en `min-width: auto`, o sea que no
achican por debajo de su contenido. `.today-item .habit-title` no tenía
`min-width: 0` ni `overflow-wrap`. La lista del modal ya lo tenía resuelto;
esta no.

**Verificación:** 375 px de contenido en 375 px de viewport, cero desbordes.

### ISSUE-003 — La fila de stats se pasaba 5 px del viewport en mobile
- **Severidad:** medium · **Categoría:** visual · **Estado:** verified
- **Commit:** `f36f24b` · **Archivos:** `css/styles.css`, `sw.js`

`.stat-card` llegaba a 380 px en un viewport de 375 px. Misma causa raíz que
ISSUE-002 un nivel más arriba: los hijos de grid también arrancan en
`min-width: auto`, y la barra de anticipación del hito, con su `min-width:
130px` fijo, empujaba la columna.

**Verificación:** `scrollWidth` 375 px, cero elementos desbordados.

## Lo que se probó y pasó limpio

| Área | Resultado |
|---|---|
| XSS en nombre de usuario y de hábito | Escapado correctamente, no ejecuta |
| Validación de formularios | Nombre vacío rechazado; meta limitada a 1–31 |
| Rutas `#/inicio`, `#/habitos`, `#/objetivos` | Cargan sin errores JS |
| Ruta inválida (`#/noexiste`) | Manejada, no deja la vista vacía |
| Estados vacíos | Presentes en Inicio y en el Panel |
| "Solo se marca hoy" | Solo las celdas de hoy son interactivas |
| Congelador de racha | Se consume solo, avisa y persiste |
| Celebraciones | Hito abre modal, día perfecto es inline |

## Consola

1 error: `net::ERR_CONNECTION_RESET` al pedir Google Fonts. Es del **entorno**
(el proxy de este contenedor bloquea `fonts.googleapis.com`), no del código:
en una red normal la petición resuelve. Tras ISSUE-001 ya no bloquea el render.

## Diferido (cosmético, tier Standard no lo arregla)

- **Labels apretados en la card de racha a 375 px.** "RACHA DE DÍAS" y el
  estado ("6 DÍAS EN JUEGO · HOY: 0 MARCADOS") cortan en 2–3 líneas. Se lee,
  pero queda tosco. Candidato para `/design-review`.
- **Accesibilidad no auditada a fondo en esta pasada.** El score la asume en
  100 sin evidencia nueva; sesiones previas agregaron focus trap y contraste
  AA, pero no se corrió un audit completo. Candidato para una pasada dedicada.

## Tests agregados al repo

Antes de este QA los 48 tests vivían en un directorio temporal fuera del repo
y se perdían al apagarse el contenedor.

| Suite | Casos | Corre con |
|---|---|---|
| `test/streak.test.mjs` | 20 | `npm test` |
| `test/month-close.test.mjs` | 12 | `npm test` |
| `test/render.test.mjs` | 4 | `npm test` (regresión de ISSUE-001) |
| `test/e2e/app.e2e.mjs` | 12 | `npm run test:e2e` (regresión de ISSUE-002) |

Runner: `node --test`, incorporado en Node 18+. Cero dependencias para los
unitarios. El E2E se saltea solo si Playwright no está instalado.

Los dos tests de regresión se verificaron contra el código viejo: fallan sin
el arreglo, pasan con él.

## Nota de proceso

El commit `0b57a88` (ISSUE-002) incluye además dos correcciones del propio
E2E: anidar la suite mobile (como suite hermana, el `after()` de la primera
cerraba el navegador y cancelaba la segunda) y sacar la dependencia de la
fecha del test de celda congelada. Debieron ir en un commit aparte; quedaron
juntas por estar en el mismo archivo.
