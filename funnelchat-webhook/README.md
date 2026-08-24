# Lead relay → FunnelChat (sin n8n)

Thank You Page → Netlify Function (`/lead`) → webhook entrante de FunnelChat →
FunnelChat dispara la plantilla de WhatsApp de confirmación.

## Setup (una vez, ~10 min)

1. **FunnelChat**: creá una automatización con disparador **Webhook entrante**
   (Inbound Webhook). Copiá la URL que te da.
2. **Netlify**: creá un sitio nuevo desde este repo con *base directory* =
   `funnelchat-webhook` (o `netlify deploy --prod` desde esta carpeta con el CLI).
3. En Netlify → Site settings → **Environment variables**, agregá
   `FUNNELCHAT_WEBHOOK_URL` = la URL del paso 1. Redeploy.
4. En la Thank You Page pegá `snippet-thx-page.html` (Elementor → HTML)
   reemplazando `TU-SITIO` por el subdominio real.
5. En la automatización de FunnelChat, mapeá los campos que llegan
   (`nombre`, `email`, `telefono`, `origen`) al contacto y agregá la acción
   de enviar la plantilla.

## Probar sin la página

```bash
curl -X POST https://TU-SITIO.netlify.app/lead \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Prueba Test","email":"prueba@test.com","telefono":"+5491100000000"}'
```

Respuesta esperada: `{"ok":true,"funnelchat_status":200}` y el mensaje
de WhatsApp llegando al número de prueba.
