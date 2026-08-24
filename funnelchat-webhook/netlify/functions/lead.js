// ═══════════════════════════════════════════════════════════
// LEAD → FUNNELCHAT (Netlify Function, sin n8n)
//
// Flujo:
//   Thank You Page ──POST──▶ esta función ──POST──▶ webhook
//   (params de Calendly)      (normaliza)           entrante
//                                                   de FunnelChat
//
// FunnelChat recibe { nombre, email, telefono, origen, params }
// y su automatización dispara la plantilla de WhatsApp.
//
// Config en Netlify (Site settings → Environment variables):
//   FUNNELCHAT_WEBHOOK_URL = URL del disparador "Webhook entrante"
//   de tu workflow en FunnelChat.
//
// Endpoint desplegado:  https://TU-SITIO.netlify.app/lead
// Acepta POST con JSON o GET con query params.
// Agregá ?debug=1 para ver qué parseó SIN enviar nada a FunnelChat.
// ═══════════════════════════════════════════════════════════

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// Calendly a veces manda los valores con doble encoding
function safeDecode(value) {
  if (!value) return '';
  try {
    let s = decodeURIComponent(String(value));
    if (/%[0-9A-Fa-f]{2}/.test(s)) {
      try { s = decodeURIComponent(s); } catch (e) { /* ya estaba bien */ }
    }
    return s;
  } catch (e) {
    return String(value);
  }
}

// "+54 9 11 2345-6789" → "+5491123456789"
function normalizePhone(raw) {
  if (!raw) return '';
  const cleaned = String(raw).replace(/[^\d+]/g, '');
  return cleaned.startsWith('+') ? '+' + cleaned.slice(1).replace(/\+/g, '') : cleaned;
}

// "2026-08-24T09:20:00-04:00" → "lunes 24 de agosto, 09:20 h"
// Respeta el offset que manda Calendly (la hora local del invitado).
function formatCita(iso) {
  if (!iso) return '';
  const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  if (!m) return '';
  const [, y, mo, d, hh, mm] = m;
  const dias = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
  const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  const dia = dias[new Date(Date.UTC(+y, +mo - 1, +d)).getUTCDay()];
  return `${dia} ${+d} de ${meses[+mo - 1]}, ${hh}:${mm} h`;
}

// Si no encontramos el teléfono por nombre de campo, lo buscamos por forma:
// cualquier valor que parezca un número de 8 a 15 dígitos.
function findPhoneByShape(data) {
  for (const [key, value] of Object.entries(data)) {
    if (/email|name|nombre|uuid|url|time|fecha/i.test(key)) continue;
    const digits = String(value).replace(/\D/g, '');
    if (digits.length >= 8 && digits.length <= 15) return String(value);
  }
  return '';
}

export default async (req) => {
  // Preflight del navegador
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  // Junta datos de query params y/o body JSON, y decodifica todo
  const url = new URL(req.url);
  let raw = Object.fromEntries(url.searchParams);
  if (req.method === 'POST') {
    try { raw = { ...raw, ...(await req.json()) }; } catch (e) { /* body vacío o no-JSON */ }
  }

  const data = {};
  for (const [k, v] of Object.entries(raw)) data[k] = safeDecode(v);

  const pick = (...keys) => {
    for (const k of keys) if (data[k]) return String(data[k]).trim();
    return '';
  };

  const telefono = normalizePhone(
    pick(
      'telefono', 'phone', 'whatsapp',
      'invitee_phone',            // algunos setups de Calendly
      'text_reminder_number',     // campo nativo de recordatorio por SMS
      'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5',
    ) || findPhoneByShape(data),  // último recurso: buscar por forma
  );

  // Calendly manda invitee_full_name VACÍO y los datos partidos en
  // first/last, así que lo armamos nosotros.
  const nombre =
    pick('nombre', 'name', 'invitee_full_name') ||
    [pick('invitee_first_name'), pick('invitee_last_name')].filter(Boolean).join(' ');

  const inicio = pick('event_start_time');  // ISO con offset, ej. 2026-08-24T09:20:00-04:00

  const payload = {
    nombre:      nombre,
    primer_nombre: nombre.split(/\s+/)[0] || '',   // para el "Hola {{}}" de la plantilla
    email:       pick('email', 'correo', 'invitee_email'),
    telefono:    telefono,
    asesor:      pick('assigned_to'),
    cita_inicio: inicio,
    cita_texto:  formatCita(inicio),               // "martes 24 de agosto, 09:20 h"
    origen:      pick('origen', 'source') || 'thx-page',
    fecha:       new Date().toISOString(),
    params:      data,  // TODO lo que llegó, por si querés mapear otro campo en FunnelChat
  };

  // Modo prueba: muestra lo que parseó y no envía nada
  if (data.debug === '1') {
    return Response.json({ ok: true, debug: true, payload }, { headers: CORS });
  }

  if (!payload.email && !payload.telefono) {
    return Response.json(
      { ok: false, error: 'Falta email y teléfono', recibido: data },
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

  // Reenvía a FunnelChat desde el servidor: sin CORS y sin exponer la URL
  let fcStatus = 0;
  let fcBody = '';
  try {
    const r = await fetch(target, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    fcStatus = r.status;
    fcBody = (await r.text()).slice(0, 300);
  } catch (e) {
    return Response.json(
      { ok: false, error: 'No se pudo contactar a FunnelChat: ' + e.message },
      { status: 502, headers: CORS },
    );
  }

  return Response.json(
    {
      ok: fcStatus >= 200 && fcStatus < 300,
      funnelchat_status: fcStatus,
      funnelchat_respuesta: fcBody,
      enviado: { nombre: payload.nombre, email: payload.email, telefono: payload.telefono },
    },
    { headers: CORS },
  );
};

export const config = { path: '/lead' };
