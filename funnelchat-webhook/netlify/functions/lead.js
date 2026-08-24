// ═══════════════════════════════════════════════════════════
// LEAD → FUNNELCHAT (Netlify Function, sin n8n)
//
// Flujo:
//   Thank You Page ──POST──▶ esta función ──POST──▶ webhook
//   (nombre/email/tel)        (normaliza)            entrante
//                                                    de FunnelChat
//
// FunnelChat recibe { nombre, email, telefono, origen } y su
// automatización dispara la plantilla de WhatsApp.
//
// Config en Netlify (Site settings → Environment variables):
//   FUNNELCHAT_WEBHOOK_URL = la URL del disparador
//   "Webhook entrante" de tu workflow en FunnelChat.
//
// Endpoint una vez desplegado:
//   https://TU-SITIO.netlify.app/lead
// Acepta POST con JSON o GET con query params.
// ═══════════════════════════════════════════════════════════

export default async (req) => {
  const CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  // Preflight del navegador
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  // Junta datos de query params y/o body JSON
  const url = new URL(req.url);
  let data = Object.fromEntries(url.searchParams);
  if (req.method === 'POST') {
    try { data = { ...data, ...(await req.json()) }; } catch (e) { /* body vacío o no-JSON */ }
  }

  const pick = (...keys) => {
    for (const k of keys) if (data[k]) return String(data[k]).trim();
    return '';
  };

  // Normaliza los nombres de campo que puede mandar Calendly o la página
  const payload = {
    nombre:   pick('nombre', 'name', 'invitee_full_name', 'invitee_first_name'),
    email:    pick('email', 'invitee_email', 'correo'),
    telefono: pick('telefono', 'phone', 'invitee_phone', 'answer_1', 'whatsapp'),
    origen:   pick('origen', 'source') || 'thx-page',
    fecha:    new Date().toISOString(),
  };

  if (!payload.email && !payload.telefono) {
    return Response.json(
      { ok: false, error: 'Falta email o teléfono' },
      { status: 400, headers: CORS },
    );
  }

  const target = process.env.FUNNELCHAT_WEBHOOK_URL;
  if (!target) {
    return Response.json(
      { ok: false, error: 'FUNNELCHAT_WEBHOOK_URL no configurada en Netlify' },
      { status: 500, headers: CORS },
    );
  }

  // Reenvía a FunnelChat (server-side: sin problemas de CORS)
  let fcStatus = 0;
  try {
    const r = await fetch(target, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    fcStatus = r.status;
  } catch (e) {
    return Response.json(
      { ok: false, error: 'No se pudo contactar a FunnelChat: ' + e.message },
      { status: 502, headers: CORS },
    );
  }

  return Response.json(
    { ok: fcStatus >= 200 && fcStatus < 300, funnelchat_status: fcStatus },
    { headers: CORS },
  );
};

export const config = { path: '/lead' };
