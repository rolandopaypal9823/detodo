# Clase del miércoles 4 de noviembre · 19:00 hs (Argentina)

Es la del miércoles 21 de octubre con otra fecha. Mismo tema (Neurociencia para el Alto Rendimiento
Profesional), mismo tráiler de Loom, mismos forms de GHL y mismos asientos de USD 5 y USD 9.

## Qué cambió respecto de la del 21

| Qué | Antes (21/10) | Ahora (4/11) |
|---|---|---|
| Fecha | `2026-10-21` · «miércoles 21 de octubre» | `2026-11-04` · «miércoles 4 de noviembre» |
| UTM / edición | `clase-oct21-alto-rendimiento` | `clase-nov04-alto-rendimiento` |
| Referencia de Stripe en el pop-up | `etapa-nivel-oct21` | `etapa-nivel-nov04` |
| Grupo de WhatsApp | `clase-de-neurociencia-21-10` | **pendiente** · hoy dice `go.wha.link/PENDIENTE-GRUPO-4-NOV` |
| Baúl (clase-beneficios.netlify.app) | `/asiento-basic/` y `/premium-htc/` eran del 21 | ahora son del 4/11; lo del 21 pasó a `/clase-21/…` |
| Calendario | `calendario-clase-21-oct` | `calendario-clase-4-nov` · 19:00 a 20:30 (Argentina) |
| Clave anti-duplicados del gate de Zoom | — | `nfm_reg_4nov` |

## Dónde está cada pieza

| Pieza | Archivo |
|---|---|
| Landing con popup | `landing-siempre-on/clase-4-noviembre/index-popup.html` |
| Landing con el form en la página | `landing-siempre-on/clase-4-noviembre/index.html` |
| Thank you de registro con el pop-up de asientos (USD 5 / USD 9) | `nfm-clase-paga/thankyou-oto.html` |
| Thank you de registro sin pop-up (para la pauta) | `nfm-clase-paga/thankyou-registro-sin-popup.html` |
| Thank you de compra (a donde manda Stripe) | `nfm-clase-paga/thankyou-compra-basic.html` · `thankyou-compra-premium.html` |
| Mail de compra | `nfm-clase-paga/mail-compra-basic.html` · `mail-compra-premium.html` |
| Baúl de beneficios | `portal-beneficios/clase-beneficios/` (se sube la carpeta entera a Netlify) |
| Thank you para etapa C (grupo de comunidad) | `landing-siempre-on/clase-4-noviembre/thank-you-comunidad.html` |
| Gate de Zoom | `landing-siempre-on/clase-4-noviembre/zoom-gate/index.html` |
| Mails de registro (bienvenida, 24 h, 30 min) | `landing-siempre-on/clase-4-noviembre/mails/` |
| Calendario (.ics y Google) | `landing-siempre-on/clase-4-noviembre/calendario-clase-4-nov.*` |
| QR del Calendly para la clase | `qr/qr-calendly-clase0411*` (`utm_source=clase0411`) |

## Antes de publicar

1. **El grupo de WhatsApp.** Cuando esté, va en la thank you (con y sin pop-up), las de compra, los mails y
   el calendario: en todos los lugares que hoy dicen `PENDIENTE-GRUPO-4-NOV`. No se publica antes.
2. **Los links de pago.** Siguen los del 21: USD 5 → `buy.stripe.com/7sY8wIa9904W0BQ46DcbC0a` y USD 9 →
   `buy.stripe.com/28E9AM1CDaJAacq1YvcbC0b`. Si en Stripe dicen «clase del 21» en el nombre o en la descripción,
   hay que cambiarlo ahí o crear links nuevos.
3. **Subir el baúl** (la carpeta `clase-beneficios` entera) a Netlify, para que lo del 21 quede en `/clase-21/`.
4. **El link de Zoom** del gate sigue siendo el de siempre (`us06web.zoom.us/j/82405076014`).

## El video de Loom

El mismo de la del 21. El embed lleva `hideEmbedTopBar`, `hide_owner`, `hide_share`, `hide_title` y `hide_speed`.
La velocidad 1x se fija en Loom (Settings → Audience). Si los subtítulos se muestran, revisá la transcripción.

## En GHL

Igual que siempre: el bloque entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ» va en el custom code; el pixel va en
Settings → Tracking Code → HEAD (sólo `PageView`).
