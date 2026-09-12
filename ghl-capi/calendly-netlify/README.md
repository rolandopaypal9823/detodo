# Puente Calendly -> GHL (Netlify Function)

Cuando alguien agenda en Calendly, esta funcion:
1. Recibe el webhook `invitee.created` de Calendly.
2. Hace upsert del contacto en GHL por email (y telefono si viene).
3. Le pone el tag `agendo` (lo quita y lo vuelve a poner, asi dispara aunque agende dos veces).
4. El workflow de GHL "CAPI Agenda" (trigger: tag `agendo`) manda `Schedule` a Meta con `{{contact.fbclid}}`.

Si cancela (`invitee.canceled`), le pone el tag `cancelo_agenda`.

Sin n8n, sin Make. Solo Calendly -> Netlify -> GHL.

---

## 1. Deploy en Netlify (5 min)

1. Netlify > Add new site > Import from Git > elegi este repo.
   - Base directory: `ghl-capi/calendly-netlify`
   - Build command: (vacio)
   - Publish directory: `public`
2. Site settings > Environment variables > agrega las de `.env.example`:
   - `GHL_API_TOKEN`
   - `GHL_LOCATION_ID`
   - `GHL_TAG_AGENDO` = `agendo`
   - `GHL_TAG_CANCELO` = `cancelo_agenda`
   - `GHL_FIELD_FECHA_AGENDA` = `fecha_agenda` (opcional, ver paso 2.3)
   - `CALENDLY_SIGNING_KEY` = una clave larga que inventes (la misma va en el paso 3)
3. Deploy. La URL del endpoint queda:
   `https://TU-SITIO.netlify.app/.netlify/functions/calendly-webhook`

## 2. GHL (5 min)

1. **Token**: Settings > Private Integrations > New > scopes `contacts.readonly` y `contacts.write`. Copia el token (empieza con `pit-`) a `GHL_API_TOKEN`.
2. **Location ID**: Settings > Business Profile > copia el Location ID a `GHL_LOCATION_ID`.
3. (Opcional) Custom field texto `fecha_agenda` para guardar la fecha/hora de la cita.
4. **Workflow "CAPI Agenda"**:
   - Trigger: `Contact Tag` > Tag added > `agendo`
   - Accion: `Meta conversion API` > Integration > Funnel Event
     - Facebook Event Name: `Schedule`
     - Custom Mapping ON > FBCLID: `{{contact.fbclid}}`
   - Publicar.

## 3. Crear el webhook en Calendly (5 min)

Calendly no deja crear webhooks desde la interfaz: se hace con su API (plan Standard o superior).

1. Calendly > Integrations > API & Webhooks > Personal Access Token > copia el token.
2. Averigua tu organization URI:

```bash
curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer CALENDLY_TOKEN" | grep -o '"current_organization":"[^"]*"'
```

3. Crea la suscripcion (reemplaza URL, ORG y SIGNING_KEY):

```bash
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

Si responde con `"state":"active"`, quedo.

## 4. Prueba (5 min)

1. Agenda una cita de prueba en Calendly con el mismo email de un contacto que ya tenga `fbclid` cargado.
2. Netlify > Functions > calendly-webhook > Logs: tiene que aparecer `{"ok":true,...,"contactId":"..."}`.
3. En GHL, ese contacto tiene que tener el tag `agendo`.
4. Meta Events Manager > Test Events (con el Test Code puesto en la accion CAPI): aparece `Schedule` con `fbc`.
5. Quita el Test Code de la accion y guarda.

## Reducir el riesgo de "mail distinto"

El match Calendly -> GHL es por email. Para que la persona no tipee otro mail, prellena el link
de Calendly que mandas desde GHL:

```
https://calendly.com/TU-USUARIO/llamada?email={{contact.email}}&name={{contact.first_name}}%20{{contact.last_name}}
```

Como respaldo, el upsert tambien manda el telefono si Calendly lo pide en el form.

## Prueba local (sin tocar GHL)

```bash
npm test
```
