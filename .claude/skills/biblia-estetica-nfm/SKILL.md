---
name: biblia-estetica-nfm
description: Biblia Estética del Instituto de Productividad / NFM (Nicolás Fernández Miranda) — el sistema de diseño oficial en formato accionable: tokens exactos (azul NFM #0c3452, naranja acción #ff6602, Montserrat + Open Sans + JetBrains Mono), componentes, recetas de código y el logo oficial. Activá SIEMPRE que haya que diseñar, maquetar o mejorar cualquier pieza visual de NFM — landings, páginas de gracias/entrega, emails, dashboards, slides, mockups, infografías, PDFs, artefactos HTML — y también cuando el usuario diga que algo "está feo", "está básico", "que se vea más pro", "ponele la estética", "el azul plano", "que se parezca a la landing", o pida aplicar la marca a una pieza existente. Traé de acá el azul con profundidad (nunca plano), el naranja como único color de activación, la red neuronal de fondo, el shimmer, las cards de vidrio y el logo — antes de elegir un solo color o una sola fuente.
---

# Biblia Estética NFM

El sistema de diseño del Instituto de Productividad. Esto no es inspiración: son los valores
exactos. Si vas a poner un color, una fuente o una sombra en una pieza de NFM, sale de acá.

## La regla de oro

> **Azul serio, naranja para activar, blanco para respirar.**

Dos voltajes. **Azul NFM `#0c3452`** es la base institucional (rigor, profundidad).
**Naranja Acción `#ff6602`** es el ÚNICO color de activación — reservado a CTAs y al acento que
exige atención. El blanco (o el navy profundo) es espacio de respiro, y el respiro es parte de la
marca.

### Los tres no negociables

1. **Un solo naranja.** `#ff6602` es el único color de activación. Nunca un segundo naranja, nunca
   naranja como fondo de página. Es acento, no relleno.
2. **Sombras teñidas de azul.** Nunca negro puro. `rgba(12,52,82,.08)`, no `rgba(0,0,0,.08)`.
3. **El azul nunca va plano.** Un `background:#0c3452` sólido cumple pero se siente barato. Todo
   fondo oscuro grande lleva capas: gradiente + glow radial + calor naranja tenue + borde de luz.
   Es la diferencia entre "correcto" y "caro". Receta exacta en `references/recetas.md`.

## Antes de escribir código, leé la referencia que corresponde

- `references/tokens.md` — paleta completa (los 3 modos: sobre blanco, sobre navy, texto),
  tipografía y escala, radios, sombras, espaciado, motion. **Leelo siempre antes de elegir un
  color o una fuente.** Trae el bloque `:root` listo para pegar.
- `references/componentes.md` — botones, eyebrows, badges, cards (blanca / vidrio / foco), stats,
  paneles, tablas, framer de foto, marquee, cita. HTML + CSS copiable de cada uno.
- `references/recetas.md` — los efectos que hacen que una pieza "se sienta" de NFM: el azul
  elegante, la red neuronal animada, el shimmer, las cards de vidrio, los reveals on scroll, el
  patrón de dos cards lado a lado. Todo con código completo y accesibilidad resuelta.

`assets/biblia-estetica.html` es la referencia viva: abrila cuando dudes de cómo se ve algo.
Es la vara de calidad.

## El logo va siempre

Toda pieza visual de NFM lleva el logo. Están en `assets/`:

| Archivo | Cuándo |
|---|---|
| `assets/logo-nfm-navy.png` | Sobre fondos claros o blancos. Es el default. |
| `assets/logo-nfm-blanco.png` | Sobre fondos oscuros, naranjas o fotos. |

Aspecto ~2.4:1. Ancho mínimo legible ~130px. Clear-space alrededor: mínimo la altura de la "N".
En HTML autocontenido va embebido como data URI base64, nunca como link externo.

## Tipografía

**Montserrat** (900/800, tracking negativo) para títulos · **Open Sans** (400/600) para cuerpo ·
**JetBrains Mono** (500, mayúsculas, tracking `.2em`) para labels y eyebrows.
No se mezclan otras fuentes. Nunca Inter, Roboto, Arial ni system-ui.

## Los tres lienzos

Blanco (respiro y foco) → Tint azul claro `#e7edf2` / glass (secciones alternas) → Navy
(autoridad, cierre, prueba premium). **El ritmo blanco → tint → navy es lo que da profundidad**;
una pieza toda del mismo fondo se siente chata aunque los colores estén bien.

## Qué sí, qué no

**✓ Hacé**
- Naranja solo en CTAs y 1 dato clave por bloque.
- Un único CTA primario por pantalla; el resto ghost (contorno).
- Sombras y overlays teñidos de azul NFM.
- Alternar fondos para dar profundidad.
- Neural y shimmer como acento sutil, de fondo.

**✕ Evitá**
- Un segundo naranja, o gradiente naranja→otro color de protagonista.
- Naranja como fondo de página completa.
- Negro puro en sombras o texto (usá navy / muted).
- Mezclar otras tipografías.
- Saturar: llenar cada pixel, dejar sin respiro.
- Neural o animaciones que compitan con la lectura. Es fondo, nunca protagonista.
- Emojis. NFM no los usa.
- Cajas redondeadas con borde izquierdo de color como acento (el cliché de IA por excelencia).

## Cierre

Antes de entregar cualquier pieza, sacá un screenshot y miralo. Chequeá: ¿el azul tiene
profundidad o quedó plano? ¿hay un solo CTA primario? ¿está el logo? ¿el naranja aparece solo
donde importa? ¿hay respiro? ¿alguna fuente que no sea del sistema?

Esta skill es el sistema. Para *producir* artefactos HTML completos de NFM (canvas, dashboards,
diagramas, landings), combinala con `disenador-visual-nfm`; para la voz del copy, con
`nfm-super-skill`.
