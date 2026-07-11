# Reto de 7 Días — Detox Digital (bonus del e-book)

Bonus del paquete del e-book de Desintoxicación Digital, en la voz de **Nico (NFM)**.
La persona elige recibirlo por **email** o por **Instagram (ManyChat)**.

## Archivos

| Archivo | Qué es |
|---|---|
| `emails-html/` | **Mails HTML cortos y visuales** (bienvenida + días 1–7): logo de Nico + título + spoiler + botón "Ir al Día N". **Esta es la forma de envío por mail.** |
| `manychat.md` | **Mensajes cortos de ManyChat** (bienvenida + 7 días): título + mini spoiler + link al día. |
| `sitio/` | **Sitio web del reto** (índice + 7 páginas, una por día). Listo para subir a Netlify. |
| `build_sitio.py` | Generador del sitio. Editar los textos acá y correr `python3 build_sitio.py`. |
| `build_emails.py` | Generador de los mails HTML. Editar `SITE` (dominio) acá y correr `python3 build_emails.py`. |
| `emails.md` | Versión **largo / texto plano** de los mails (por si alguna vez querés mandar el reto completo por mail sin el sitio). No es la vía principal. |
| `reto-7-dias-concepto.md` | Versión 1 del concepto (borrador inicial). |

## Cómo funciona el embudo

Email o ManyChat → **mensaje corto con botón** → **página del día en el sitio** (reto completo + checklist) → **CTA final → «Hackea tu Cerebro»** (Circle, con UTMs).

## Mails HTML (`emails-html/`)

- 8 archivos: `bienvenida.html` + `dia1.html` … `dia7.html`.
- Súper cortos y visuales: header navy con el logo de Nico, título del día, una línea de spoiler y un botón naranja **"Ir al Día N →"** que lleva a la página del día en el sitio. Mismo concepto que ManyChat.
- HTML de email real (tablas + estilos inline + fuentes web-safe + botón bulletproof): se ven bien en Gmail, Outlook, Apple Mail, etc.
- **Para cargarlos:** pegá el HTML de cada archivo en tu ESP (Mailchimp/Brevo/etc. tienen "pegar código HTML"). El botón y el logo apuntan a `SITE` (variable en `build_emails.py`); poné ahí tu dominio real y regenerá.
- El logo se sirve desde el sitio (`SITE/assets/logo-blanco.png`), así que se ve una vez que el sitio está en Netlify.

## Tracking / UTMs

El CTA final de cada día del sitio apunta a **Hackea tu Cerebro** con UTMs, para que midas de dónde viene cada visita:

```
https://comunidadproductiva.circle.so/hackea-tu-cerebro?utm_source=ebook&utm_medium=reto-7-dias&utm_content=diaN
```

- `utm_source=ebook` · `utm_medium=reto-7-dias` · `utm_content=dia1..dia7` (el día específico).
- Se genera solo en `build_sitio.py` (función `producto_link`).

## Deploy del sitio en Netlify

1. Arrastrar la carpeta `sitio/` completa a Netlify (o `netlify deploy --dir=sitio --prod`).
2. Cada día queda en `/dia1`, `/dia2` … `/dia7` (son carpetas con `index.html`, funcionan sin configuración).
3. Poner el dominio definitivo (ej. `retode7dias.netlify.app`) y actualizarlo en `manychat.md`.

## El sitio incluye

- Marca NFM completa: Azul `#0c3452`, Naranja Acción `#ff6602`, Montserrat + Open Sans, logo en header y footer.
- Barra de progreso de los 7 días (con día actual animado) y animaciones de aparición al scrollear.
- **Checklist interactivo** por día: la persona tilda cada paso y queda guardado en su dispositivo (localStorage). Al completar todo aparece un banner de festejo.
- **Día 4:** widget de respiración 4-4-6 guiada (círculo animado con las fases y contador de ciclos).
- **Día 7:** confeti + cartel "FELICITACIONES, completaste el reto" + campo para escribir *"después de estos 7 días, ¿qué cambió / cómo te sentiste / qué lograste?"* (se autoguarda) + invitación a sacar captura y etiquetar a Nico en Instagram.

## El "acompañado" sin humo

En la landing se promete un reto *acompañado*. Para que sea coherente sin inventar contadores falsos ni "1.234 personas online", el acompañamiento se sostiene con tres cosas **reales**:

1. **Nico te escribe todos los días** (email o DM): ese es el acompañamiento principal y es literal.
2. La frase que usamos en todos los mensajes: *"el reto está abierto todo el año y cada semana arranca gente nueva"* — describe cómo funciona el sistema, sin cifras inventadas.
3. La invitación a **subir historias etiquetando a Nico** (día 0, la franja de comunidad del sitio y el día 7) hace visible a la gente que realmente está haciendo el reto — la prueba social se genera sola y es verificable.

## Pendientes antes de lanzar

- [ ] **Dominio del sitio**: poné el dominio real de Netlify en `SITE` (`build_emails.py`) y en `manychat.md`, y regenerá los mails (`python3 build_emails.py`). ✅ El link del producto (Hackea tu Cerebro) ya está con UTMs.
- [ ] Confirmar handle de Instagram (`@nicofernandezmiranda`) en `manychat.md` y `build_sitio.py`.
- [ ] Palabra clave de ManyChat (sugerida: **RETO**).
- [ ] Hora de envío de los mails (sugerida: 7:30 am hora local).
