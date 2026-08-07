# HANDOFF — Dashboard NFM · v1.0 (fusión NFM VIP + Flowscale)

Documento único de traspaso: **qué está instalado**, qué hace cada cosa y **qué necesita para funcionar en vivo**.

App: `index.html` (un solo archivo) · Backend: `netlify/functions/*.mjs`

---

## 0) Qué es esta versión

Es la fusión de los dos dashboards que existían por separado:

- **Dashboard NFM VIP** (`dashboard nico`) — el más completo en funciones: Meta orgánico y anuncios multi-marca, Stories, Mi YouTube, Email, Resumen ejecutivo, Bandeja de DMs, Cerebro IA con la voz NFM, Estudio visual.
- **Dashboard Flowscale** (`flowscalevip_5`) — el más cuidado en experiencia: configuración inicial, secciones plegables, menú a medida, objetivos de seguidores, FlowScore y control de gasto de las APIs.

**La base es el NFM VIP** (tiene todas las funciones del otro y varias más) y encima se le montó la capa de experiencia de Flowscale. No se sacó nada.

### Lo que se sumó respecto al dashboard NFM VIP

| Novedad | Qué resuelve |
|---|---|
| **Configuración inicial** (asistente de 5 pasos) | Pregunta tu nombre, tu marca, tu logo, qué querés lograr y qué secciones vas a usar. Solo la primera vez; se rehace desde ⚙ Configuración. |
| **Saludo por hora del día** | La portada saluda con tu nombre: "Buen día, Nico" / "Buenas tardes" / "Buenas noches", con las mismas fórmulas que usa Claude. Debajo, el pulso: cuándo publicaste por última vez, seguidores ganados, FlowScore y a qué distancia estás de tu meta. |
| **Secciones plegables** | El problema no era que faltara información: sobraba toda junta. Cada bloque con título es un desplegable. El primero de cada vista viene abierto (el resumen), el resto cerrados con un renglón de contexto ("10 filas", "4 métricas"). Lo que abrís se recuerda. Botones *Abrir todo* / *Cerrar todo*, y se puede apagar entero desde ⚙ Configuración. |
| **Menú a medida** | Lo que no usás desaparece del menú (secciones y marcas). No se borra nada. |
| **🎯 Objetivos** | A cuántos seguidores querés llegar y para cuándo. Mira TUS piezas reales, ve cuáles trajeron seguidores, y calcula cuántas piezas como esas te faltan y a qué ritmo semanal. Barra de progreso, veredicto de si el tiempo alcanza y la tabla de las 10 piezas para replicar. **No usa IA ni gasta un peso.** |
| **⚡ FlowScore** | Un número de 1 a 100 comparándote contra vos mismo: alcance, conexión, conversión y constancia (25 puntos cada uno). Tu mitad más reciente contra la anterior. Sin promedios de industria ni IA. |
| **Control de gasto de Apify** | Estimador de costo antes de cada búsqueda + contador de saldo + los tres controles que definen la factura (cuántas piezas, desde cuándo, con o sin transcripción). |
| **Control de gasto de IA** | Contador de insights y preguntas de chat con costo estimado, en ⚙ Configuración. |
| **Tendencias y Estudio visual, recuperados** | Las dos vistas estaban escritas y funcionando pero habían quedado sin entrada en el menú ni caso en el router. Vuelven a estar. |
| **`netlify/functions/` (bien escrito)** | La carpeta se llamaba `netlify/fuctions` mientras el `netlify.toml` apuntaba a `netlify/functions`: **ninguna función se estaba deployando**. Corregido. |

### Correcciones de legibilidad (tema oscuro)

Cuando el dashboard pasó a tema oscuro, el token `--nfm-azul` cambió de significado:
antes era el navy de fondo, ahora es el color de **texto claro**. Varias reglas que
lo usaban como fondo, o que tenían colores fijos del tema claro, quedaron ilegibles.
Se corrigieron todas, verificadas con un auditor de contraste automático que recorre
las 21 vistas, los modales, los 5 pasos del setup y los flotantes que sólo aparecen
al pasar el mouse:

- **Tooltip del gráfico de crecimiento** — `background: var(--nfm-azul)` con texto
  blanco: blanco sobre casi blanco. Ahora va con superficie oscura explícita.
- **`.insight-body strong`** — pintado con el color de superficie. Correcto dentro de
  la tarjeta `.insight` (que va invertida), invisible cuando el mismo bloque se usa
  dentro de una `.data-card` oscura. Ahora hereda, y sólo se invierte dentro de `.insight`.
- **Colores del embudo** (`#2563eb` / `#7c3aed` / `#16a34a`), del calendario por formato,
  y los verdes/rojos de comparación — todos eran versiones oscuras pensadas para fondo
  blanco. Se subieron a su versión clara, manteniendo el significado.
- Chapita de fase, chapita T1/T2, pie del sidebar, "→ ACCIONABLES" dentro de la tarjeta
  clara, y los puntitos de Facebook y LinkedIn en el menú.

### Cambios en el backend

- **`ig-competitor.mjs`** — la transcripción iba **siempre** en `true` aunque nadie la mirara (es la parte más lenta y cara del scrapeo); ahora la pide el dashboard. Se agregó el filtro por rango (`onlyPostsNewerThan`) y el `limit` que el front ya podía mandar pero no mandaba.
- **`data.mjs`** — ahora guarda también `setup` y `goal`, para que al re-deployar una versión nueva el dashboard siga siendo el tuyo.
- **`meta-stories.mjs` / `meta-stories-cron.mjs`** — el archivo de stories guardaba el
  **link** que devuelve Meta, no la imagen. Esos links van firmados y vencen a las pocas
  horas, así que el archivo histórico se llenaba de imágenes rotas. Ahora la imagen se
  **descarga y se guarda en Netlify Blobs**, y se sirve desde `/api/meta-stories?img=<id>`
  con caché permanente. Además el cron diario ahora recorre **todas** las cuentas de IG
  configuradas (`META_IG_USER_ID` + las de cada marca), no sólo la de por defecto.

---

## 1) Cómo poner esto online

1. Subí **la carpeta completa** a Netlify (**app.netlify.com/drop**, arrastrar y soltar).
2. `netlify.toml` ya está: `publish = "."`, `functions = "netlify/functions"`.
3. Cargá las **variables de entorno** que quieras (§2) en Netlify → Site settings → Environment variables.
4. **Re-deploy** cada vez que agregues o cambies una variable.
5. Para verificar qué keys tomó el sitio: `https://TU-SITIO/api/whoami`.

> **Regla de oro:** todas las keys van SOLO en Netlify (env vars), nunca en el navegador. Todo es **read-only**: lee, nunca modifica. Nunca pegues un token en el chat.

Para la versión paso a paso pensada para alguien que no programa, ver `INSTRUCCIONES.md`.

---

## 2) Variables de entorno

| Variable | Activa | De dónde sale |
|---|---|---|
| `ANTHROPIC_API_KEY` | Toda la **IA**: insights con schema de confianza, chat, diagnóstico ejecutivo y de email | console.anthropic.com |
| `YOUTUBE_API_KEY` | **Competidores de YouTube** (gratis) | Google Cloud → YouTube Data API v3 |
| `APIFY_API_TOKEN` | **Competidores de Instagram** + transcripción de reels (pago por uso) | apify.com → Settings → Integrations |
| `META_ACCESS_TOKEN` | Todo **Meta**: anuncios, orgánico, stories | System User token ("Nunca" vence) |
| `META_IG_USER_ID` | Orgánico de IG de la cuenta por defecto | Graph API / Business |
| `META_IG_USER_ID_INSTITUTO` / `_HTC` / `_DOBLECLICK` | Orgánico de las otras marcas | ídem |
| `META_AD_ACCOUNT_ID` | **Anuncios** de la cuenta por defecto | `act_...` |
| `META_AD_ACCOUNT_ID_INSTITUTO` (etc.) | Anuncios de otra cuenta publicitaria | `act_...` |
| `META_API_VERSION` | Versión de la Graph API (default `v21.0`) | — |
| `KIT_API_SECRET` | **Email → Kit (ConvertKit)** | Kit → Settings → Advanced → API Secret |
| `DOPPLER_API_KEY` + `DOPPLER_ACCOUNT` | **Email → Doppler** (account = tu email de login) | Doppler → API |
| `YT_OAUTH_CLIENT_ID` + `_SECRET` + `_REFRESH_TOKEN` | **Mi YouTube** (analytics del canal propio) | ver §5 |
| `GEMINI_API_KEY` | **Estudio visual** (generar imágenes) | aistudio.google.com |
| `NFM_DATA_TOKEN` | Protege la nube con una contraseña | la inventás vos |
| `SITE_LABEL` | Etiqueta del sitio en `whoami` | — |

**Sufijos por marca:** en mayúsculas y sin guiones → `NICO`, `INSTITUTO`, `HTC`, `DOBLECLICK`. Si una marca no tiene su variable, cae a la genérica.

Ninguna es obligatoria: sin ninguna key, toda la analítica sobre tus CSV funciona igual.

---

## 3) Funcionalidades instaladas

✅ **funciona ya** (solo con tus CSV/XLSX/.numbers) · 🔑 **necesita la env var** correspondiente.

### Arranque y navegación
- ✅ **Configuración inicial** de 5 pasos la primera vez.
- ✅ **Saludo personalizado** por hora del día en la portada.
- ✅ **Secciones plegables** con memoria de lo que abriste.
- ✅ **Menú a medida**: prendés y apagás secciones y marcas.

### Carga de datos
- ✅ Multi-marca × multi-red (Nico, Instituto, Hackeá tu Cerebro, Doble Click × IG/Stories/YT/FB/LinkedIn/TikTok).
- ✅ **Cuentas manuales** (agregás marcas propias con sus redes).
- ✅ Importador **CSV / XLSX / .numbers** (Mac) con autodetección de cuenta.
- ✅ Filtro temporal + ocultar colabs · guardado local + nube.
- 🔑 **Sync orgánico de Meta** (`META_*`) — trae posts de IG sin CSV, multi-marca.

### Análisis de contenido (todo ✅)
- Resumen general + por marca + por red (KPIs, top/peores, por formato, por horario, por duración).
- **⚡ FlowScore** de 1 a 100 comparándote contra vos mismo.
- **🎯 Objetivos**: proyección de seguidores sobre data propia.
- **📈 Tendencias**: comparación de períodos, seguidores acumulados y views por semana.
- **Toda pieza es clickeable** → detalle con preview embebido (IG y YouTube).
- Embudo TOF/MOF/BOF con veredicto honesto + CTA detectado.
- Calendario, Reporte mensual (+PDF), Categorías/hashtags.
- Análisis del CTA "comentá X" con nivel de confianza (descarta los de 1 solo uso).
- Gráficos de crecimiento (seguidores IG + suscriptores YT) con hover.

### Inteligencia artificial (🔑 `ANTHROPIC_API_KEY`)
- **Insight IA on-demand**: primero ves el análisis automático **gratis**; el botón "Análisis con Claude" es lo único que consume, y el resultado queda cacheado por scope + filtro (no se re-pide al navegar).
- Schema de confianza (🟢/🔴/⚠️ + Alta/Media/Baja): nunca escala datos de una sola pieza.
- **Chat lateral** con streaming, con el contexto de métricas cacheado del lado de Anthropic (prompt caching).
- **Cerebro IA** (voz/avatar/oferta) — copia selectiva por documento y por tarjeta.
- Resumen ejecutivo (embudo + inversión + costos por objetivo + diagnóstico con criterio Meta Ads).
- **Contador de gasto** en ⚙ Configuración.

### Anuncios (🔑 `META_*`)
- Dashboard multi-marca: campaña/conjunto/anuncio, gasto/ROAS/CPC/CTR/frecuencia, alerta de fatiga, preview del anuncio embebido, costos por objetivo.

### Competidores
- 🔑 **Instagram** (Apify): top piezas por intención + transcripción opcional + guardar copy al Cerebro. **Con estimador de costo, contador de saldo y tres controles de gasto.** Las búsquedas se guardan (local + nube).
- 🔑 **YouTube** (gratis): top videos + guardar títulos al Cerebro. Persistente y desplegable.
- ✅ Manual + transcripción por DownSub.

### Email / Newsletter (🔑 `KIT_*` / `DOPPLER_*`)
- Kit + Doppler: suscriptores, crecimiento de la base, campañas (aperturas/clicks/bajas), diagnóstico IA.

### Stories (🔑 `META_*`)
- **Captura visual** de stories activas (24h) → archivo histórico.
- **Automática:** tarea programada `meta-stories-cron` captura 1×/día; el dashboard trae el archivo de la nube.

### Mi YouTube (🔑 `YT_OAUTH_*`)
- Analytics de tu propio canal (views, watch time, subs ganados/netos) + gráfico + tabla diaria. Read-only.

### Estudio visual (🔑 `GEMINI_API_KEY`)
- Generá miniaturas y creatividades a partir de una idea escrita, con la identidad de la marca.

### Bandeja de oportunidades (✅ 100% local, sin IA)
- Subís el export de DMs de Instagram (JSON) → detecta **sin responder**, categoriza (🔥 lead caliente, ⚠️ queja, 🤝 colab, 🎙️ prensa, ❓ consulta, 💛 fan) y prioriza. Los DMs **no se suben a ningún lado**.

### Extras (✅)
- Nombre + logo editables · tema oscuro premium · PDF de cualquier vista · Radar de noticias (RSS, gratis).

---

## 4) Funciones Netlify instaladas

| Archivo | Endpoint | Qué hace |
|---|---|---|
| `claude-insight.mjs` | `/api/claude-insight` | Insights IA (schema de confianza; lee el Cerebro) |
| `claude-chat.mjs` | `/api/claude-chat` | Chat IA con streaming |
| `data.mjs` | `/api/data` | Nube: files + competidores + Cerebro + setup + objetivo |
| `feeds.mjs` | `/api/feeds` | Radar de noticias (RSS) |
| `youtube.mjs` | `/api/youtube` | Competidores YouTube |
| `ig-competitor.mjs` | `/api/ig-competitor` | Competidores IG (formatos, límite, rango y transcripción elegibles) |
| `meta-sync.mjs` | `/api/meta-sync` | Orgánico IG multi-marca |
| `meta-ads.mjs` | `/api/meta-ads` | Anuncios multi-marca |
| `meta-ad-preview.mjs` | `/api/meta-ad-preview` | Preview embebido de un anuncio |
| `meta-stories.mjs` | `/api/meta-stories` | Captura stories + archivo en la nube |
| `meta-stories-cron.mjs` | (scheduled `0 9 * * *`) | Captura stories automática 1×/día |
| `yt-analytics.mjs` | `/api/yt-analytics` | YouTube Analytics del canal propio (OAuth) |
| `email-stats.mjs` | `/api/email-stats` | Email Kit + Doppler |
| `gemini-image.mjs` | `/api/gemini-image` | Estudio visual |
| `whoami.mjs` | `/api/whoami` | Diagnóstico: qué keys están cargadas |
| `yt-transcript.mjs` | `/api/yt-transcript` | (sin uso — se usa DownSub manual) |

---

## 5) Setup de "Mi YouTube" (OAuth, una sola vez)

Es el único que necesita OAuth. Para sacar el **refresh token** sin escribir código:

1. **Google Cloud Console** → mismo proyecto que `YOUTUBE_API_KEY` (o uno nuevo) → habilitá **"YouTube Analytics API"**.
2. **Credenciales → Crear → ID de cliente OAuth** → tipo **"Aplicación web"** → en *URIs de redireccionamiento autorizados* agregá `https://developers.google.com/oauthplayground`. Guardá el **Client ID** y el **Client Secret**.
3. Andá a **developers.google.com/oauthplayground** → ⚙ (arriba a la derecha) → tildá **"Use your own OAuth credentials"** → pegá Client ID + Secret.
4. En "Step 1", en el campo de scope pegá `https://www.googleapis.com/auth/yt-analytics.readonly` → **Authorize APIs** → logueate **con la cuenta dueña del canal** → aceptá.
5. "Step 2" → **Exchange authorization code for tokens** → copiá el **Refresh token**.
6. En Netlify cargá `YT_OAUTH_CLIENT_ID`, `YT_OAUTH_CLIENT_SECRET`, `YT_OAUTH_REFRESH_TOKEN` → re-deploy.

> El scope es **solo lectura**. El refresh token no vence salvo que revoques el acceso.

---

## 6) Dónde tocar cada cosa en `index.html`

Es un solo archivo con todo el JS global: buscar por nombre de función alcanza.

| Bloque | Dónde |
|---|---|
| Estado y persistencia | `const state = {…}`, `loadState()`, `saveState()` |
| Parsers (Meta / YouTube / LinkedIn) | `normalizeMetaRows`, `normalizeYouTubeRows`, `parseLinkedInWorkbook` |
| Router de vistas | `render()` (original) y el envoltorio `window.render` de la capa v1.0 |
| Capa v1.0 (lo que vino de Flowscale) | comentario `v1.0 · CAPA FLOWSCALE`, al final del script |
| Saludo | `saludoActual()`, `renderSaludo()`, tablas `SALUDOS` / `SALUDO_SUB` |
| Secciones del menú | tabla `SECCIONES`, `seccionActiva()`, `applySectionVisibility()` |
| Plegables | `foldify()`, `FOLD_SIEMPRE_ABIERTO` |
| Objetivos | `goalProjection()`, `renderObjetivos()` |
| FlowScore | `flowScore()`, `renderFlowScore()` |
| Gasto de Apify | `igCostEstimate()`, `igSpendTotals()`, `renderIgCostControls()` |
| Gasto de IA | `logAIUsage()`, `aiUsageTotals()` |
| Configuración inicial | `openSetup()`, `renderSetup()`, `setupFinish()` |

**Nota sobre el orden de evaluación:** el dashboard hace un primer `render()` antes de llegar a la capa v1.0. Las vistas que usan cosas de esa capa lo chequean con `window.__v1Listo`. Si agregás una función nueva ahí que se llame desde una vista vieja, hacé lo mismo.

---

## 7) Qué quedó afuera a propósito

Del dashboard Flowscale no se trajo:

- **Import de email por CSV con mapeo manual de columnas.** Acá el módulo de Email se conecta directo a Kit o Doppler por API, que es mejor: no hay que exportar nada a mano. Si alguna vez hace falta soportar un proveedor sin API, ese import es el punto de partida.
- **Cuentas dinámicas como único modelo.** Flowscale reemplazaba las marcas fijas por cuentas creadas a mano. Acá conviven las dos: las cuatro marcas NFM cableadas (con toda su lógica de detección automática al importar un CSV) **más** las cuentas manuales. Lo que se sumó es poder ocultar del menú las marcas que no uses.

---

*Todo read-only. Las funciones que dependen de una key muestran un mensaje claro si falta configurarla — nada se rompe si una env var no está.*
