# Puente GoHighLevel → Doppler (sin n8n)

Función de Netlify que recibe el webhook de un formulario de GoHighLevel y
suscribe el contacto a una lista de **Doppler Email Marketing**. Los mails los
manda después una **Automatización de Doppler** con disparador
"Al suscribirse a una lista".

```
Form GHL → Workflow GHL → Webhook → Netlify Function → API Doppler (lista) → Automatización Doppler → mails
```

## 1. Deploy en Netlify

Conectá este repo a Netlify (o `netlify deploy --prod` con la CLI). No hay build:
`publish = public`, `functions = netlify/functions`.

Endpoint final: `https://TU-SITIO.netlify.app/api/ghl-doppler`

## 2. Variables de entorno

Site configuration → Environment variables:

| Variable | Obligatoria | Qué es |
|---|---|---|
| `DOPPLER_API_KEY` | sí | API key de Doppler (Panel de control → Integraciones y API → API Key) |
| `DOPPLER_ACCOUNT` | sí | el **email** de tu cuenta de Doppler (es el `accountName` de la API) |
| `DOPPLER_LIST_ID` | sí | id numérico de la lista destino (se ve en la URL de la lista en Doppler) |
| `WEBHOOK_SECRET` | recomendada | token propio; GHL lo manda como `?key=...` o header `x-webhook-token` |
| `DOPPLER_FIELD_MAP` | no | JSON `{"campo_del_lead":"CAMPO_DOPPLER"}`, ej. `{"phone":"PHONE"}` |
| `ALLOWED_LIST_IDS` | no | ids extra permitidos, separados por coma, para usar `?list=` |

`FIRSTNAME` y `LASTNAME` se mandan siempre que vengan en el payload; cualquier
otro campo tiene que existir antes en Doppler (Suscriptores → Campos) y
declararse en `DOPPLER_FIELD_MAP`. Si Doppler rechaza un campo, la función
reintenta sola mandando solo el email, así el lead nunca se pierde.

## 3. Configurar el webhook en GoHighLevel

Workflow → Trigger `Form Submitted` → acción **Webhook**:

- Método: `POST`
- URL: `https://TU-SITIO.netlify.app/api/ghl-doppler?key=EL_MISMO_WEBHOOK_SECRET`
- Body: JSON con al menos `email`, y opcionalmente `first_name`, `last_name`, `phone`.

El parser acepta el payload plano o anidado (`contact`, `customData`) y también
`full_name` / `nombre` / `apellido`.

## 4. Configurar la automatización en Doppler

Automation → **Al suscribirse a una lista** → elegí la lista de `DOPPLER_LIST_ID`
→ armá la secuencia de emails (bienvenida, +1 día, +3 días…) → **Activar**.
Todo contacto que entre por este endpoint arranca la secuencia solo.

## 5. Probar

```bash
curl -X POST "https://TU-SITIO.netlify.app/api/ghl-doppler?key=WEBHOOK_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"email":"prueba@tudominio.com","first_name":"Juan","last_name":"Perez"}'
```

Respuesta esperada: `{"ok":true,"email":"prueba@tudominio.com","listId":"...","dopplerStatus":201}`

Códigos: `401` token mal, `400` JSON o email inválido, `422` Doppler rechazó el
dato, `502` Doppler caído o con error (GHL puede reintentar). Los detalles quedan
en Netlify → Functions → Logs.

## Referencia de la API usada

```
POST https://restapi.fromdoppler.com/accounts/{cuenta}/lists/{listId}/subscribers
Authorization: token {API_KEY}
Content-Type: application/json

{ "email": "juan@test.com",
  "fields": [ {"name":"FIRSTNAME","value":"Juan"}, {"name":"LASTNAME","value":"Perez"} ] }
```
