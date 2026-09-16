# Lead relay → FunnelChat (sin n8n)

Una sola función de Netlify (`netlify/functions/lead.js`), desplegada en
`https://funnelchat-webhook-agenda-hecha.netlify.app`, con **dos endpoints** que
alimentan **dos flujos distintos** de FunnelChat:

| Endpoint | Quién le pega | Flujo de FunnelChat | Plantilla |
|---|---|---|---|
| `/lead` | Thank You Page de Calendly (agenda hecha) | Agenda | Confirmación de entrevista |
| `/webinar` | Workflow de GoHighLevel (form de registro a la clase) | Webinar | **Bienvenida a la clase** |

- El **flujo 1 (agenda)** está en producción y no cambió: ver más abajo.
- El **flujo 2 (webinar)** es el nuevo: [saltá directo a la sección](#flujo-2--registro-al-webinar--whatsapp-de-bienvenida).

---

## Flujo 1 — Agenda hecha (Calendly) → `/lead`

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

### Setup (una vez, ~15 min)

#### Paso 0 — Averiguá cómo se llama el parámetro del teléfono

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

#### Paso 1 — FunnelChat: creá el webhook entrante

En FunnelChat, nueva automatización con disparador **Webhook entrante**
(Inbound Webhook). Te va a dar una URL tipo `https://api.funnelchat.../hooks/abc123`.
Copiala. Esa URL es un secreto: no la pegues en el HTML de la página.

#### Paso 2 — Netlify: subí la función

Con el CLI, parado en esta carpeta:

```bash
npx netlify-cli deploy --prod
```

O desde netlify.com → Add new site → Import from GitHub, con
*Base directory* = `funnelchat-webhook`.

Te queda un endpoint: `https://TU-SITIO.netlify.app/lead`

#### Paso 3 — Netlify: cargá la URL secreta

Site settings → **Environment variables** → agregá:

| Key | Value |
|---|---|
| `FUNNELCHAT_WEBHOOK_URL` | la URL del Paso 1 |

Después **redeploy** (las variables solo se leen al desplegar).

#### Paso 4 — Thank You Page: pegá el snippet

Copiá `snippet-thx-page.html` en un widget HTML de Elementor, reemplazando
`TU-SITIO` por tu subdominio real. Va al final de la página, no importa dónde.

#### Paso 5 — FunnelChat: mapeá y mandá

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

### Probar

#### Sin tocar FunnelChat (modo debug)

Te devuelve qué parseó, sin enviar nada:

```bash
curl "https://TU-SITIO.netlify.app/lead?debug=1&invitee_full_name=Juan%20Perez&invitee_email=juan@mail.com&answer_1=%2B5491123456789"
```

Fijate que `telefono` salga bien normalizado. Si sale vacío, mirá el objeto
`params` de la respuesta: ahí está el nombre real del campo, y lo agregás a la
lista del `pick(...)` en `lead.js`.

#### De punta a punta

```bash
curl -X POST https://TU-SITIO.netlify.app/lead \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Prueba Test","email":"prueba@test.com","telefono":"+5491100000000"}'
```

Esperás `{"ok":true,"funnelchat_status":200}` y el WhatsApp llegando al número.

---

### Si algo falla

| Síntoma | Causa | Solución |
|---|---|---|
| `"FUNNELCHAT_WEBHOOK_URL no configurada"` | Falta la variable o no hiciste redeploy | Paso 3 + redeploy |
| `"Falta email y teléfono"` | La URL no traía params | Revisá el redirect de Calendly: en el event type, *Confirmation page* → **Redirect to an external site** con "Pass event details to your redirected page" activado |
| `funnelchat_status: 404` | La URL del webhook está mal | Recopiala del Paso 1 |
| `telefono` vacío pero el resto bien | El param tiene otro nombre | Miralo en `params` y agregalo al `pick(...)` |
| Llega dos veces el WhatsApp | Alguien abrió la página en dos pestañas | El `sessionStorage` cubre el refresh; para blindarlo, deduplicá en FunnelChat por número |


---

## Flujo 2 — Registro al webinar → WhatsApp de bienvenida

```
Landing (form GHL kLh5onxCgHdGDA10c8NU)
   │  la persona se registra: nombre, email, TELÉFONO (+ quiz oculto: etapa, equipo, nivel, califica…)
   ▼
GoHighLevel · Workflow "Form Submitted" ── acción Webhook (POST) ──▶ Netlify /webinar
                                                                        │ normaliza teléfono y nombre,
                                                                        │ agrega fecha/título/grupo de la clase
                                                                        ▼
                                                    FunnelChat · flujo con disparador
                                                    "Integración con terceros" (webhook)
                                                                        │
                                                                        ▼
                                                    acción: enviar PLANTILLA API
                                                    "Bienvenida a la clase" al {{telefono}}
```

**¿Por qué desde el workflow de GHL y no desde la thank you page?** El form de la
landing es un iframe de GoHighLevel: la página no puede leer el teléfono que la
persona escribió adentro. GHL sí lo tiene, y el workflow dispara aunque la persona
cierre la pestaña antes de llegar a la thank you. Es el único lugar confiable para
"coger el dato de teléfono".

**¿Por qué pasa por Netlify y no de GHL directo a FunnelChat?** Porque el webhook
de GHL manda el teléfono como lo cargó la persona (`+54 9 11 2345-6789`, sin +,
con espacios), el nombre repartido en tres campos, y todo el contacto anidado en
`customData`. La función lo deja limpio (`+5491123456789`, `primer_nombre`,
`clase_texto`, `grupo_whatsapp`) para que en FunnelChat mapees variables y listo.
Además la URL del webhook de FunnelChat queda guardada en Netlify, no en GHL.

### Setup (una vez, ~20 min)

#### Paso 1 — FunnelChat: creá el flujo de bienvenida

1. **Plantilla.** Plantillas API de WhatsApp → nueva plantilla, categoría *Utilidad*
   (es una confirmación de registro, no marketing: se aprueba más rápido y no la
   frenan). Nombre sugerido: `bienvenida_clase`. Cuerpo sugerido, con las variables
   en el orden que después vas a mapear:

   ```
   Hola {{1}} 👋 ¡Ya tenés tu lugar reservado en la clase en vivo
   *{{2}}* con Nico Fernández Miranda!

   📅 {{3}}, {{4}} · por Zoom.

   El acceso lo mandamos por este grupo. Unite ahora así no te lo perdés:
   {{5}}

   Cualquier duda, respondé este mensaje.
   ```

   | Variable | Campo del payload | Ejemplo |
   |---|---|---|
   | `{{1}}` | `primer_nombre` | Juan |
   | `{{2}}` | `clase_titulo` | Neurociencia para el Alto Rendimiento Profesional |
   | `{{3}}` | `clase_texto` | martes 22 de septiembre |
   | `{{4}}` | `clase_hora` | 19:00 h (Argentina) |
   | `{{5}}` | `grupo_whatsapp` | https://chat.whatsapp.com/… |

   Enviala a aprobar y esperá el visto bueno de Meta (minutos a unas horas).

2. **Flujo.** Nuevo flujo → disparador **Integración con terceros** (webhook
   entrante). FunnelChat te da una URL secreta tipo `https://…/hooks/xxxx`.
   Copiala: es la que va a Netlify en el Paso 2. **No la pegues en GHL ni en
   ninguna página.**

3. **Mapeo.** Cuando en el Paso 4 le mandes la primera prueba, FunnelChat te va a
   mostrar el JSON recibido (ver más abajo). Mapeá `telefono` al número del
   contacto y `nombre` / `email` a los datos del contacto.

4. **Acción.** Agregá la acción de enviar plantilla → `bienvenida_clase` y
   completá las 5 variables con los campos de la tabla de arriba.

5. *(Opcional)* Antes de la acción, una condición `califica` = `no` → salir del
   flujo, si no querés escribirle a los que eligieron C en el quiz (la thank you
   page tampoco les muestra el grupo). O directamente activá `WEBINAR_SOLO_CALIFICA`
   en Netlify (Paso 2) y la función no los manda.

6. *(Opcional)* Etiquetá al contacto con la `edicion` (`clase-sep22-alto-rendimiento`)
   para después mandar recordatorios o tandas sólo a esa clase.

#### Paso 2 — Netlify: variables de entorno y redeploy

Es el **mismo sitio** que ya tenés (`funnelchat-webhook-agenda-hecha`), no hace
falta crear otro. Site configuration → Environment variables → agregá:

| Key | Obligatoria | Value |
|---|---|---|
| `FUNNELCHAT_WEBHOOK_URL_WEBINAR` | **sí** | la URL del webhook del flujo de bienvenida (Paso 1.2) |
| `WEBINAR_CLASE_TITULO` | no | `Neurociencia para el Alto Rendimiento Profesional` |
| `WEBINAR_CLASE_HORA` | no | `19:00 h (Argentina)` |
| `WEBINAR_GRUPO_WHATSAPP` | no | link de invitación del grupo de la clase (`https://chat.whatsapp.com/…`) |
| `WEBINAR_TOKEN` | no | una clave cualquiera; si la ponés, GHL tiene que mandarla en la URL (`?token=…`) |
| `WEBINAR_SOLO_CALIFICA` | no | `1` para no escribirles a los que eligieron C en el quiz |

`FUNNELCHAT_WEBHOOK_URL` (la del flujo de agenda) **queda como está**.

Después desplegá de nuevo, parado en esta carpeta y con el sitio ya linkeado:

```bash
npx netlify-cli deploy --prod
```

(Si el CLI no lo reconoce como el sitio existente: `npx netlify-cli link` y elegí
`funnelchat-webhook-agenda-hecha`.) Las variables se leen al desplegar: si las
cambiás después, Deploys → **Trigger deploy**.

> Cuando cambie la clase (nuevo martes, nuevo grupo), no hay que tocar código:
> actualizás `WEBINAR_GRUPO_WHATSAPP` (y el título/hora si cambian) y hacés
> Trigger deploy. La fecha (`clase_fecha`) ya llega desde el form, por el campo
> oculto que carga la landing.

#### Paso 3 — GoHighLevel: workflow con acción Webhook

Automation → Workflows → **Create workflow**:

1. **Trigger:** `Form Submitted` → filtro *Form is* → el form de la landing
   (`kLh5onxCgHdGDA10c8NU`, "Form AGOSTO NUEVO"). Si en el futuro hay más forms
   de clases, agregalos al mismo filtro o hacé un workflow por form.
2. **Acción:** `Webhook`
   - Method: **POST**
   - URL: `https://funnelchat-webhook-agenda-hecha.netlify.app/webinar`
     (si pusiste `WEBINAR_TOKEN`: `…/webinar?token=LA-CLAVE`)
   - Custom Data / Body: pegá el contenido de **`ghl-webhook-body.json`** (está en
     esta carpeta). Son los campos del contacto con los merge tags de GHL,
     incluidos los custom fields del quiz (`etapa`, `equipo`, `nivel`, `califica`,
     `dedicacion`, `clase_fecha`, `edicion`). Si alguno de esos custom fields no
     existe en tu cuenta, GHL manda el tag vacío y no pasa nada.

   Si tu plan de GHL sólo deja mandar el webhook "con todos los datos del
   contacto" (sin custom data), también sirve: la función acepta el payload
   completo de GHL, aplana `customData`/`contact`, y lee `phone`, `first_name`,
   `last_name`, `email` y los custom fields tal como GHL los manda.
3. **Publish** el workflow.

Recomendado: como segunda acción, `Add Tag` → `wa-bienvenida-enviada`, para
poder auditar en GHL quién pasó por acá.

#### Paso 4 — Probar

**Sin tocar FunnelChat (modo debug)** — te devuelve qué parseó, sin enviar nada:

```bash
curl -X POST "https://funnelchat-webhook-agenda-hecha.netlify.app/webinar?debug=1" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Juan","last_name":"Pérez","email":"juan@mail.com","phone":"+54 9 11 2345-6789","etapa":"A","equipo":"B","califica":"si","clase_fecha":"2026-09-22"}'
```

Fijate que salga `"telefono": "+5491123456789"`, `"primer_nombre": "Juan"` y
`"clase_texto": "martes 22 de septiembre"`.

**De punta a punta** (a tu propio número; esto manda el WhatsApp de verdad y le
muestra el JSON al flujo de FunnelChat para que puedas mapear):

```bash
curl -X POST https://funnelchat-webhook-agenda-hecha.netlify.app/webinar \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Prueba","email":"prueba@test.com","phone":"+549TUNUMERO","clase_fecha":"2026-09-22","califica":"si"}'
```

Esperás `{"ok":true,"flujo":"webinar","funnelchat_status":200,…}` y el WhatsApp
llegando. Después, una prueba real: registrate en la landing con tu número y
mirá en GHL → Workflow → *Execution logs* que el webhook respondió 200.

**Prueba local del código** (sin red, para cuando toques `lead.js`):

```bash
node test/local.js
```

### Qué recibe FunnelChat en `/webinar`

```json
{
  "nombre": "Juan Pérez",
  "primer_nombre": "Juan",
  "email": "juan@mail.com",
  "telefono": "+5491123456789",
  "telefono_sin_plus": "5491123456789",
  "clase_fecha": "2026-09-22",
  "clase_texto": "martes 22 de septiembre",
  "clase_titulo": "Neurociencia para el Alto Rendimiento Profesional",
  "clase_hora": "19:00 h (Argentina)",
  "grupo_whatsapp": "https://chat.whatsapp.com/…",
  "edicion": "clase-sep22-alto-rendimiento",
  "etapa": "A", "equipo": "B", "nivel": "alto", "califica": "si",
  "dedicacion": "Dirijo una pyme",
  "utm_source": "ig", "utm_medium": "", "utm_campaign": "…", "utm_content": "",
  "ghl_contact_id": "abc123",
  "origen": "webinar-registro",
  "fecha": "2026-09-16T21:00:00.000Z",
  "params": { "...todo lo que mandó GHL, por si querés mapear otro campo..." }
}
```

### Si algo falla (webinar)

| Síntoma | Causa | Solución |
|---|---|---|
| `"FUNNELCHAT_WEBHOOK_URL_WEBINAR no configurada"` | Falta la variable o no hiciste redeploy | Paso 2 + Trigger deploy |
| `"token inválido"` (401) | Pusiste `WEBINAR_TOKEN` y la URL del workflow no lo lleva | Agregá `?token=…` a la URL en GHL, o borrá la variable |
| `"skipped": true, "El registro no trae teléfono"` | El body del webhook no manda `phone` | Revisá el Custom Data del Paso 3: tiene que estar `"phone": "{{contact.phone}}"` |
| `telefono` sin `+` | La persona lo cargó sin código de país | En GHL, en el form, activá el campo de teléfono con selector de país para que lo guarde en E.164 |
| El workflow no dispara | El filtro del trigger apunta a otro form | Trigger → *Form is* → `kLh5onxCgHdGDA10c8NU` |
| Llega el WhatsApp pero sin nombre/fecha | Variables de la plantilla sin mapear | Paso 1.4: cada `{{n}}` con su campo |
| `funnelchat_status: 404` | La URL del webhook está mal | Recopiala del flujo en FunnelChat |
| Le llega a los que eligieron C | `WEBINAR_SOLO_CALIFICA` no está en `1` | Ponela, o la condición del Paso 1.5 |
