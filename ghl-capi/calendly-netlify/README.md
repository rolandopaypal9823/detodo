# Puente Calendly -> GHL (Netlify Function)

Cuando alguien agenda en Calendly, esta funcion verifica que el webhook sea
realmente de Calendly y te deja elegir uno de dos caminos hacia GHL.

## Modo A (recomendado): sin token de GHL

La funcion reenvia, por **POST**, un JSON limpio a la URL del trigger
"Inbound Webhook" de un workflow tuyo en GHL. Adentro del workflow, GHL
mismo busca o crea el contacto por email y sigue con el tag / Meta CAPI.
No necesitas Private Integration token ni Location ID.

Payload que reenvia:
```json
{
  "event": "invitee.created",
  "email": "juan@test.com",
  "phone": "+5491155551234",
  "firstName": "Juan",
  "lastName": "Perez Lopez",
  "startTime": "2026-09-15T18:00:00.000000Z",
  "source": "Calendly"
}
```

### Armar el workflow en GHL

1. Workflows > Create Workflow > vacio.
2. Trigger: **Inbound Webhook** (a veces figura como "Webhook"). Guarda y copia
   la URL que te da: esa va en `GHL_INBOUND_WEBHOOK_URL`.
3. Mandale un POST de prueba a esa URL con el JSON de arriba (podes usar el
   propio Test Events / Postman / curl). GHL usa ese payload de ejemplo para
   generar los merge fields `{{trigger.body.email}}`, `{{trigger.body.phone}}`, etc.
4. Accion 1: **Find/Create Contact** (o el nombre equivalente en tu version
   de GHL) > Email: `{{trigger.body.email}}` > Phone: `{{trigger.body.phone}}`
   > First name / Last name desde el trigger.
5. Accion 2 (opcional): **Add Tag** > `agendo` si `{{trigger.body.event}}` es
   `invitee.created`, o `cancelo_agenda` si es `invitee.canceled`. Usa un
   If/Else si tu version no deja condicionar el valor del tag directamente.
6. Accion 3: **Meta conversion API** > Integration > Funnel Event >
   Facebook Event Name: `Schedule` > Custom Mapping ON > FBCLID:
   `{{contact.fbclid}}` (ya viene guardado en el contacto desde el registro).

Con esto, un solo workflow reemplaza los dos pasos (tag + workflow de CAPI)
del diseno anterior.

## Modo B (respaldo): con token de GHL

Si tu plan de GHL no tiene el trigger "Inbound Webhook", dejá
`GHL_INBOUND_WEBHOOK_URL` vacio y completa en cambio `GHL_API_TOKEN` y
`GHL_LOCATION_ID`. La funcion hace el upsert del contacto y le pone el tag
ella misma, llamando a la API de GHL. Ahi si necesitas:

1. **Token**: Settings > Private Integrations > New > scopes `contacts.readonly`
   y `contacts.write`. Copia el token (empieza con `pit-`).
2. **Location ID**: Settings > Business Profile > copia el Location ID.
3. Workflow "CAPI Agenda": Trigger `Contact Tag added: agendo` > Accion
   Meta conversion API con evento `Schedule` y FBCLID `{{contact.fbclid}}`.

## Deploy en Netlify sin GitHub (Netlify CLI)

Arrastrar el zip a la pantalla de "Deploy manually" de Netlify **no funciona
para esta funcion**: esa via solo publica archivos estaticos y no lee
`netlify.toml` ni empaqueta `netlify/functions/`. Hay que usar la CLI:

```bash
npm install -g netlify-cli
netlify login
# parado adentro de esta carpeta:
netlify deploy --prod
```

Elegi "create a new site", publish directory `public`. Al terminar te da
la URL final, algo como `https://tu-sitio.netlify.app/.netlify/functions/calendly-webhook`.

Las variables de entorno se cargan despues, desde Site settings >
Environment variables en la web, o con `netlify env:set NOMBRE valor`.

## Crear el token y el webhook en Calendly

Calendly no deja crear webhooks desde la interfaz, solo por API. Necesitas
un **Personal Access Token** (Integrations > API & Webhooks > "Cree un
token de acceso personal"). Al crearlo te va a pedir marcar "ambitos"
(scopes). Marca solo estos dos, dejando el resto sin marcar (principio de
minimo privilegio, no necesitas mas):

- **Webhooks**: marca las dos opciones que aparezcan adentro (crear/gestionar
  suscripciones). Es el permiso central, sin esto no podes dar de alta el webhook.
- **Gestión de usuarios**: marca la opcion de solo lectura ("Ver"). Se usa
  para el llamado a `/users/me` que te da tu organization URI en el paso
  siguiente.

No marques Programación, Contactos, Notetaker ni Seguridad y cumplimiento:
no los usa este flujo. Si algun llamado te da 403 "insufficient scope",
volves a este token y agregas el permiso puntual que falte.

Con el token creado:

```bash
# 1) organization URI
curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer CALENDLY_TOKEN" | grep -o '"current_organization":"[^"]*"'

# 2) crear la suscripcion del webhook (siempre via POST, Calendly nunca usa GET)
curl -s -X POST https://api.calendly.com/webhook_subscriptions \
  -H "Authorization: Bearer CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://TU-SITIO.netlify.app/.netlify/functions/calendly-webhook",
    "events": ["invitee.created", "invitee.canceled"],
    "organization": "https://api.calendly.com/organizations/ORG_ID",
    "scope": "organization",
    "signing_key": "LA_MISMA_CLAVE_QUE_CALENDLY_SIGNING_KEY"
  }'
```

Si responde con `"state":"active"`, quedo. Requiere plan Standard de
Calendly o superior; en planes inferiores la API no deja crear webhooks.

## Prueba

1. Agenda una cita de prueba con el mismo email de un contacto que ya
   tenga `fbclid` cargado.
2. Netlify > Functions > calendly-webhook > Logs: aparece
   `{"ok":true,"mode":"forward",...}` (o `"mode":"api"` si usas el Modo B).
3. En GHL: el contacto se encontro/creo, tiene el tag correspondiente.
4. Meta Events Manager > Test Events (con el Test Code puesto en la accion
   CAPI): aparece `Schedule` con `fbc`.
5. Quita el Test Code de la accion y guarda.

## Reducir el riesgo de "mail distinto"

El match es por email. Prellena el link de Calendly que mandas desde GHL:

```
https://calendly.com/TU-USUARIO/llamada?email={{contact.email}}&name={{contact.first_name}}%20{{contact.last_name}}
```

## Prueba local (sin tocar GHL ni Calendly)

```bash
npm test
```
Corre los dos modos con `fetch` mockeado.
