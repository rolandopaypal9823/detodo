---
name: awesome-design
description: Director de arte para NFM. Biblioteca de 74 sistemas de diseño de marcas de referencia (Apple, Linear, Stripe, Vercel, Notion, Ferrari, Framer, etc.) MÁS la ficha de marca propia de NFM. Su lógica central NO es copiar una marca: es elegir qué marca de referencia tiene el mejor diseño para lo que el usuario pide (un dashboard → Linear/Vercel; una landing de venta → Stripe/Framer; algo premium → Apple/Ferrari), tomar prestada su ESTRUCTURA, jerarquía, transiciones y animaciones, y RE-PINTAR todo con la identidad visual NFM (Azul #0c3452, Naranja Acción #ff6602, Montserrat + Open Sans). Activá esta skill SIEMPRE que el usuario pida construir o diseñar una página, landing, dashboard, componente, app, email, presentación o cualquier interfaz/asset visual para NFM o el Instituto de Productividad; cuando pida algo "al estilo de" una marca; cuando pida sugerencias de en qué marca inspirarse; o cuando nombre una marca del índice junto a una tarea de diseño/frontend. Por defecto, todo output visual sale con identidad NFM salvo que el usuario diga explícitamente lo contrario.
---

# Awesome DESIGN.md — Director de arte NFM

Esta skill combina dos cosas:

1. **74 fichas `DESIGN.md` de marcas de referencia** (`design-md/<marca>/DESIGN.md`) — sistemas de diseño reales documentados con tokens de color, tipografía, espaciado, radios, sombras, componentes y carácter.
2. **La ficha de marca propia de NFM** (`design-md/_nfm/DESIGN.md`) — los tokens oficiales del Instituto de Productividad.

Un `DESIGN.md` (concepto de Google Stitch) es un documento plain-text que un agente lee para generar UI consistente con un lenguaje visual.

## La lógica central (leé esto antes de cada tarea)

El objetivo NO es clonar una marca. El flujo es de **director de arte**:

> **Marca de referencia = el ESQUELETO (estructura, jerarquía, layout, transiciones, animaciones, criterio de UX).
> NFM = la PIEL (colores, tipografía, voz, motifs).**

Para cada pedido de diseño, seguí estos 4 pasos:

### Paso 1 — Identificar qué tipo de cosa se pide
Dashboard, landing de venta, hero, pricing, email, formulario, blog/artículo, app premium, presentación, etc.

### Paso 2 — Elegir la(s) marca(s) de referencia con mejor diseño para ESO
Usá el **mapa de decisión** de abajo. Si el usuario no nombró una marca, **eligila vos con criterio y decíselo**: "Para un dashboard me voy a inspirar en la estructura de Linear, que es la referencia para data-dense; lo repinto con la identidad NFM." Si el usuario nombró una marca, respetala.
Podés combinar dos: estructura de una, motion de otra.

### Paso 3 — Leer las fichas relevantes
Leé SIEMPRE `design-md/_nfm/DESIGN.md` (la piel) **y** la(s) ficha(s) de la marca de referencia elegida (el esqueleto). No trabajes de memoria: los tokens están en los archivos.

### Paso 4 — Construir = esqueleto de la referencia + piel NFM
- Tomá de la referencia: el layout, la jerarquía tipográfica (escalas/proporciones), el espaciado, el ritmo, las transiciones y micro-animaciones, los patrones de componente.
- Reemplazá TODOS los valores de marca por los de NFM: colores → tokens NFM; fuentes → Montserrat (titulares) + Open Sans (cuerpo); CTAs → naranja #ff6602; sombras → teñidas de azul.
- Aplicá las `hard_rules` de la ficha NFM sin excepción (un solo naranja, naranja como acento nunca como fondo, blanco como respiro, etc.).
- Cuando sume, incorporá los motifs NFM (Vector de Crecimiento ascendente en scroll-reveals y flechas, encuadres FRAMER, texturas sutiles sobre azul).

Resultado: algo que tiene el nivel de ejecución de una marca top, pero inconfundiblemente NFM.

## Mapa de decisión — qué marca para qué pedido

| Lo que pide el usuario | Inspirarse en (esqueleto) | Por qué |
|---|---|---|
| **Dashboard / panel / data-dense / SaaS interno** | linear.app, vercel, posthog, sentry, supabase | Densidad de datos legible, jerarquía clara, dark mode prolijo |
| **Landing de venta / lanzamiento / página de oferta** | stripe, framer, lovable, runwayml | Conversión, secciones de prueba, ritmo de scroll, CTAs |
| **Hero impactante / above-the-fold premium** | apple, ferrari, lamborghini, spacex, tesla | Aspiracional, fotografía + tipografía grande, lujo |
| **Pricing / planes / comparativa** | stripe, notion, cal, superhuman | Tablas de planes claras, destaque del plan recomendado |
| **Email / newsletter** | superhuman, resend, intercom | Tipografía de email, limpieza, legibilidad |
| **Blog / artículo / contenido largo** | theverge, wired, mintlify, notion | Lectura cómoda, jerarquía editorial |
| **App / producto mobile-first** | airbnb, uber, revolut, wise | UX consumer, cards, flujos |
| **Documentación / academia / curso** | mintlify, notion, stripe (docs) | Navegación, estructura de conocimiento |
| **Producto AI / herramienta tech** | claude, cohere, mistral.ai, x.ai, ollama, cursor | Estética AI moderna, sobria |
| **Pieza institucional / autoridad / keynote** | apple, ibm, hashicorp, meta | Seriedad corporativa, peso de marca |
| **Algo creativo / bold / editorial** | spotify, nike, pinterest, figma | Color, energía, expresividad |
| **Onboarding / wizard / formularios** | cal, airtable, zapier, slack | Flujos paso a paso, claridad |

Si el pedido no encaja claro en una fila, elegí la marca cuyo *carácter* (descrito en su ficha) mejor calce con el objetivo, y justificá la elección en una línea al usuario.

## Identidad NFM — resumen operativo (la fuente de verdad está en `design-md/_nfm/DESIGN.md`)

- **Colores:** Azul NFM `#0c3452` (texto/fondos institucionales), Naranja Acción `#ff6602` (ÚNICO color de activación: CTAs y acentos), Blanco `#ffffff` (respiro/foco).
- **Tipografía:** Titulares = **Montserrat Bold** (Title Case o MAYÚSCULAS). Cuerpo = **Open Sans Regular**.
- **Motion:** con intención, sugerir progreso ascendente; ease-out expresivo; scroll-reveals que "suben".
- **Reglas duras:** un solo naranja; naranja es acento, no fondo; sombras teñidas de azul (no negro); blanco es activo de marca; no mezclar otras fuentes.
- **Voz:** español rioplatense, anti-hype, anti-vendehumo, científico pero conversacional.

## Estructura de archivos

```
design-md/
  _nfm/DESIGN.md          ← la PIEL: identidad NFM (leer SIEMPRE)
  <marca>/DESIGN.md       ← el ESQUELETO: 74 marcas de referencia
  <marca>/README.md
```

## Índice de marcas de referencia (74)

**Consumer / marketplace:** airbnb, uber, pinterest, spotify, starbucks, nike, shopify
**AI / dev tools:** claude, cohere, cursor, lovable, mintlify, mistral.ai, minimax, ollama, opencode.ai, replicate, runwayml, together.ai, x.ai, voltagent, warp, raycast, composio, clay
**Fintech / cripto:** stripe, binance, coinbase, kraken, mastercard, revolut, wise, cal
**SaaS / productividad:** linear.app, notion, figma, framer, miro, intercom, slack, superhuman, sanity, webflow, expo, posthog, sentry, resend, zapier
**Infra / data:** vercel, supabase, mongodb, clickhouse, hashicorp, nvidia, ibm, hp, dell-1996
**Automoción / hardware / premium:** tesla, bmw, bmw-m, ferrari, lamborghini, bugatti, renault, apple, meta
**Media / gaming / telco:** theverge, wired, playstation, nintendo-2001, spacex, vodafone, elevenlabs

## Nota de propiedad intelectual

Las fichas de marcas de terceros son referencia de diseño (tokens y patrones). En los entregables finales NO se reproducen logos, nombres ni copy de esas marcas: se toma el *cómo está construido*, y la identidad visible siempre es NFM. Las fichas provienen del repo MIT `awesome-design-md` (VoltAgent); ver `LICENSE`.
