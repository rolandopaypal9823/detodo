# Lead relay → FunnelChat (sin n8n)

Cuando alguien agenda, Calendly redirige a la Thank You Page dejando sus datos
en los parámetros de la URL. Este relay los agarra de ahí y se los pasa a
FunnelChat para que dispare la plantilla de WhatsApp.

```
Calendly ──redirige con params──▶ THX page ──POST──▶ Netlify /lead ──POST──▶ Webhook
  (nombre, email, teléfono)        (snippet)        (normaliza)      entrante FunnelChat
                                                                            │
                                                                    plantilla WhatsApp
```

**¿Por qué la función en el medio y no la página directo a FunnelChat?**
Dos motivos: el navegador bloquea el POST directo por CORS, y la URL de tu
webhook quedaría a la vista en el HTML público de la página.

---

## Setup (una vez, ~15 min)

### Paso 0 — Averiguá cómo se llama el parámetro del teléfono

Este es el único paso que hay que hacer con los ojos. Agendá una entrevista de
prueba con un teléfono real, y cuando caigas en la Thank You Page **copiá la URL
completa**. Vas a ver algo así:

```
https://.../gracias?invitee_full_name=Juan%20Perez
                   &invitee_email=juan@mail.com
                   &answer_1=%2B5491123456789      ← acá está el teléfono
                   &invitee_uuid=...
```

**En el Calendly del Instituto ya está verificado: el teléfono viene en `answer_1`**
(y `text_reminder_number` llega vacío). Otros setups posibles:

| Cómo pediste el teléfono en Calendly | Parámetro |
|---|---|
| Pregunta personalizada ← **el caso del Instituto** | `answer_1`, `answer_2`… según el orden |
| Campo nativo de recordatorio por SMS | `text_reminder_number` |
| Campo de teléfono en el booking | `invitee_phone` |

Otro dato ya verificado: **`invitee_full_name` llega VACÍO**. El nombre hay que
armarlo con `invitee_first_name` + `invitee_last_name` — la función ya lo hace.

**No hace falta que aciertes**: la función ya prueba los tres, y si igual no lo
encuentra busca por forma (cualquier valor de 8 a 15 dígitos que no sea un email
ni un nombre). Además reenvía **todos** los params bajo la clave `params`, así
que en FunnelChat siempre lo vas a poder mapear a mano.

### Paso 1 — FunnelChat: creá el webhook entrante

En FunnelChat, nueva automatización con disparador **Webhook entrante**
(Inbound Webhook). Te va a dar una URL tipo `https://api.funnelchat.../hooks/abc123`.
Copiala. Esa URL es un secreto: no la pegues en el HTML de la página.

### Paso 2 — Netlify: subí la función

Con el CLI, parado en esta carpeta:

```bash
npx netlify-cli deploy --prod
```

O desde netlify.com → Add new site → Import from GitHub, con
*Base directory* = `funnelchat-webhook`.

Te queda un endpoint: `https://TU-SITIO.netlify.app/lead`

### Paso 3 — Netlify: cargá la URL secreta

Site settings → **Environment variables** → agregá:

| Key | Value |
|---|---|
| `FUNNELCHAT_WEBHOOK_URL` | la URL del Paso 1 |

Después **redeploy** (las variables solo se leen al desplegar).

### Paso 4 — Thank You Page: pegá el snippet

Copiá `snippet-thx-page.html` en un widget HTML de Elementor, reemplazando
`TU-SITIO` por tu subdominio real. Va al final de la página, no importa dónde.

### Paso 5 — FunnelChat: mapeá y mandá

En la automatización, el webhook entrante te va a mostrar el JSON que recibió:

```json
{
  "nombre": "Juan Perez",
  "email": "juan@mail.com",
  "telefono": "+5491123456789",
  "origen": "thx-agendamiento",
  "fecha": "2026-08-24T15:04:05.000Z",
  "params": { "...todo lo que vino en la URL..." }
}
```

Mapeá `telefono` al contacto, `nombre` a la variable de la plantilla, y agregá
la acción de enviar el template. Listo.

---

## Probar

### Sin tocar FunnelChat (modo debug)

Te devuelve qué parseó, sin enviar nada:

```bash
curl "https://TU-SITIO.netlify.app/lead?debug=1&invitee_full_name=Juan%20Perez&invitee_email=juan@mail.com&answer_1=%2B5491123456789"
```

Fijate que `telefono` salga bien normalizado. Si sale vacío, mirá el objeto
`params` de la respuesta: ahí está el nombre real del campo, y lo agregás a la
lista del `pick(...)` en `lead.js`.

### De punta a punta

```bash
curl -X POST https://TU-SITIO.netlify.app/lead \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Prueba Test","email":"prueba@test.com","telefono":"+5491100000000"}'
```

Esperás `{"ok":true,"funnelchat_status":200}` y el WhatsApp llegando al número.

---

## Si algo falla

| Síntoma | Causa | Solución |
|---|---|---|
| `"FUNNELCHAT_WEBHOOK_URL no configurada"` | Falta la variable o no hiciste redeploy | Paso 3 + redeploy |
| `"Falta email y teléfono"` | La URL no traía params | Revisá el redirect de Calendly: en el event type, *Confirmation page* → **Redirect to an external site** con "Pass event details to your redirected page" activado |
| `funnelchat_status: 404` | La URL del webhook está mal | Recopiala del Paso 1 |
| `telefono` vacío pero el resto bien | El param tiene otro nombre | Miralo en `params` y agregalo al `pick(...)` |
| Llega dos veces el WhatsApp | Alguien abrió la página en dos pestañas | El `sessionStorage` cubre el refresh; para blindarlo, deduplicá en FunnelChat por número |
