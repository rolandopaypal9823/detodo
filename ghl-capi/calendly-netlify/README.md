# Puente agendas -> GHL (Netlify Function)

## Por que asi

El trigger "Inbound webhook" de GHL es PAGO. El trigger de **tag** es gratis.
Entonces esta funcion escribe directo al contacto con la API de GHL y le pone
un tag, y ese tag dispara el workflow que manda `Schedule` a Meta CAPI.

```
Thank you page de Calendly  ->  Netlify Function  ->  API de GHL
   (email + fbclid del browser)   (upsert + tag)        tag "agendo"
                                                             |
                                                             v
                                          Workflow GHL: Meta CAPI Schedule
```

Acepta dos formatos de entrada, sin cambiar nada:
- **A)** JSON simple desde la thank you page (lo que vas a usar ahora).
- **B)** El webhook real de Calendly, si algun dia queres cobertura 100%.

## Paso 1: token de GHL

1. GHL > Settings > **Private Integrations** > New.
   Si aca tambien aparece una corona (pago), avisame antes de seguir.
2. Scopes: `contacts.readonly` y `contacts.write`. Copia el token (`pit-...`).
3. GHL > Settings > Business Profile > copia el **Location ID**.

## Paso 2: subir a Netlify

**Opcion rapida (probar primero):** Netlify > Add new site > **Deploy manually**
> arrastra la carpeta descomprimida (la carpeta entera, no solo `public`).
Despues del deploy, anda a la pestana **Functions** del sitio. Si ves
`calendly-webhook` en la lista, quedo y no necesitas terminal.

**Si la funcion NO aparece ahi**, el deploy manual no la tomo y hay que usar
la CLI desde tu computadora:

```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

El endpoint final es:
`https://TU-SITIO.netlify.app/.netlify/functions/calendly-webhook`

## Paso 3: variables de entorno

Netlify > Site configuration > **Environment variables** > agrega las de
`.env.example`. Despues, Deploys > **Trigger deploy** para que las tome.

## Paso 4: la thank you page

1. Calendly > Event type > Confirmation page > Redirect to an external site
   > URL de tu pagina de gracias > activar **"Pass event details to your
   redirected page"**.
2. En el header de esa pagina pega `../thankyou-calendly-to-ghl.html`,
   cambiando la primera linea por la URL de tu endpoint de Netlify.

## Paso 5: el workflow en GHL

1. Workflows > Create Workflow.
2. Trigger: **Contact Tag** > Tag added > `agendo`. (Gratis.)
3. Accion: **Meta conversion API** > Integration > Funnel Event
   - Facebook Event Name: `Schedule`
   - Custom Mapping ON > FBCLID: `{{contact.fbclid}}`
4. Publish.

## Paso 6: probar

1. Agenda una cita de prueba con un mail que ya tenga `fbclid` cargado.
2. Netlify > Functions > calendly-webhook > Logs: tiene que aparecer
   `{"ok":true,"via":"thankyou",...}`.
3. GHL: el contacto tiene el tag `agendo` y el workflow corrio.
4. Meta Events Manager > Test Events: aparece `Schedule` con `fbc`.
5. Saca el Test Code de la accion CAPI y guarda.

## Limitaciones de la via thank you page

- Solo dispara si la persona llega a la pagina de gracias.
- No cubre cancelaciones ni reprogramaciones (pasan dentro de Calendly).

Cuando quieras cerrar eso, se da de alta el webhook real de Calendly
apuntando a la MISMA URL: el codigo ya lo acepta. Eso necesita un token de
Calendly y una llamada a su API.

## Prueba local

```bash
npm test
```
