# Hoja membretada + tarjeta invitación — Instituto de Productividad (teatro)

Piezas impresas para la charla de Nico en el teatro. Se generan con `python3 build.py`
(requiere `pip install playwright segno pillow` y un Chromium; en la nube ya está en `/opt/pw-browsers`).

## Archivos en `output/`

| Archivo | Qué es |
|---|---|
| `hoja-membretada-idp-carta.pdf` | Hoja Carta (21,59 × 27,94 cm), lisa. Esquina superior izquierda libre para pegar la tarjeta. |
| `hoja-membretada-idp-carta-renglones.pdf` | Misma hoja con renglones suaves cada 8,5 mm para que el público escriba. |
| `hoja-membretada-idp-a4.pdf` / `-a4-renglones.pdf` | Versiones A4 (21 × 29,7 cm). |
| `hoja-membretada-idp-*-bn.pdf` | Las mismas cuatro hojas en blanco y negro (logo negro, acentos gris, renglones gris claro). |
| `tarjeta-invitacion-idp-90x50-v1.pdf` | Tarjeta 90 × 50 mm con QR. Texto: "Gracias por venir". |
| `tarjeta-invitacion-idp-90x50-v2.pdf` | Ídem. Texto: "Espero que disfrutes la función." |
| `tarjeta-invitacion-idp-90x50-v2-bn.pdf` | v2 en blanco y negro, mismo diseño (fondo negro). |
| `tarjeta-invitacion-idp-90x50-v2-bn-blanco.pdf` | v2 en blanco y negro con fondo blanco (menos tinta, impresora común). |
| `tarjeta-invitacion-idp-plancha-carta-*.pdf` | 10 tarjetas en una Carta con marcas de corte, una plancha por versión y tema. |
| `qr-idp-tsl-teatro.svg` / `.png` | El QR solo (azul NFM sobre blanco), por si hace falta en otra pieza. |
| `mockup-hoja-con-tarjeta.png` | Preview de cómo queda la tarjeta pegada en la hoja. |

## Datos (editables arriba de `build.py`)

- QR → `https://mba.nicolasfernandezmiranda.com/idp-tsl?utm_source=teatro`
- Pie de hoja → CTA a `mba.nicolasfernandezmiranda.com/idp` + Instagram `@nicofernandezmiranda` y `@institutodeproductividad`
- Marca → azul NFM `#0c3452`, naranja acción `#ff6602`, Montserrat / Open Sans / JetBrains Mono (manual de marca NFM).
- Logo → logo oficial NFM (navy sobre blanco en la hoja, blanco sobre azul en la tarjeta) + wordmark "Instituto de Productividad".
