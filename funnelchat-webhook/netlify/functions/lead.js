// ═══════════════════════════════════════════════════════════
// LEAD → FUNNELCHAT (Netlify Function, sin n8n)
//
// Un solo archivo, dos endpoints, dos flujos de FunnelChat:
//
//   /lead      Agenda hecha (Calendly)
//              Thank You Page ──POST──▶ /lead ──POST──▶ webhook FunnelChat "agenda"
//              (params de Calendly)    (normaliza)      → plantilla de confirmación
//
//   /webinar   Registro a la clase (formulario de GoHighLevel)
//              Form GHL → Workflow GHL → acción Webhook ──POST──▶ /webinar
//              ──POST──▶ webhook FunnelChat "webinar" → plantilla de bienvenida
//
// Config en Netlify (Site settings → Environment variables):
//   FUNNELCHAT_WEBHOOK_URL          webhook entrante del flujo de AGENDA   (para /lead)
//   FUNNELCHAT_WEBHOOK_URL_WEBINAR  webhook entrante del flujo de WEBINAR  (para /webinar)
//   WEBINAR_TOKEN                   (opcional) si está, /webinar exige ?token=… o header x-nfm-token
//   WEBINAR_SOLO_CALIFICA           (opcional) "1" → a los que eligieron C en el quiz (califica=no)
//                                   no se les manda nada (igual que la thank you, que no les muestra grupo)
//   WEBINAR_GRUPO_WHATSAPP          (opcional) link del grupo de la clase, viaja en el payload
//                                   como {{grupo_whatsapp}} para pegarlo en la plantilla
//   WEBINAR_CLASE_TITULO            (opcional) título de la clase, viaja como {{clase_titulo}}
//   WEBINAR_CLASE_HORA              (opcional) ej. "19:00 h (Argentina)", viaja como {{clase_hora}}
//
// Endpoints desplegados:
//   https://TU-SITIO.netlify.app/lead
//   https://TU-SITIO.netlify.app/webinar
// Aceptan POST con JSON (o form-urlencoded) y GET con query params.
// Agregá ?debug=1 para ver qué parseó SIN enviar nada a FunnelChat.
// ═══════════════════════════════════════════════════════════

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, x-nfm-token',
};

// Calendly a veces manda los valores con doble encoding
function safeDecode(value) {
  if (value === null || value === undefined) return '';
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
  return `${diaSemana(y, mo, d)} ${+d} de ${MESES[+mo - 1]}, ${hh}:${mm} h`;
}

// "2026-09-22" → "martes 22 de septiembre"
function formatFecha(ymd) {
  if (!ymd) return '';
  const m = String(ymd).match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return '';
  const [, y, mo, d] = m;
  return `${diaSemana(y, mo, d)} ${+d} de ${MESES[+mo - 1]}`;
}

const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
               'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
function diaSemana(y, mo, d) {
  return DIAS[new Date(Date.UTC(+y, +mo - 1, +d)).getUTCDay()];
}

// Si no encontramos el teléfono por nombre de campo, lo buscamos por forma:
// cualquier valor que parezca un número de 8 a 15 dígitos.
function findPhoneByShape(data) {
  for (const [key, value] of Object.entries(data)) {
    if (/email|name|nombre|uuid|url|time|fecha|id$|zip|postal|cp$/i.test(key)) continue;
    const digits = String(value).replace(/\D/g, '');
    if (digits.length >= 8 && digits.length <= 15 && /^[\d\s()+\-.]+$/.test(String(value))) {
      return String(value);
    }
  }
  return '';
}

// GoHighLevel manda a veces el contacto plano y a veces anidado
// (contact, customData, location…). Aplanamos hasta 3 niveles: la primera
// aparición de cada clave gana, así el nivel de arriba tiene prioridad.
function flatten(payload) {
  const out = {};
  const walk = (obj, depth) => {
    if (!obj || typeof obj !== 'object' || depth > 3) return;
    for (const [k, v] of Object.entries(obj)) {
      if (/^(location|workflow|calendar|owner|user|attribution)/i.test(k)) continue; // no es el contacto
      if (v && typeof v === 'object' && !Array.isArray(v)) walk(v, depth + 1);
      else if (out[k] === undefined) out[k] = Array.isArray(v) ? v.join(', ') : v;
    }
  };
  walk(payload, 0);
  return out;
}

// Junta query params + body (JSON o form-urlencoded) y decodifica todo
async function readInput(req) {
  const url = new URL(req.url);
  let raw = Object.fromEntries(url.searchParams);
  if (req.method === 'POST') {
    const text = await req.text();
    if (text) {
      try {
        raw = { ...raw, ...JSON.parse(text) };
      } catch (e) {
        try { raw = { ...raw, ...Object.fromEntries(new URLSearchParams(text)) }; } catch (e2) { /* nada */ }
      }
    }
  }
  const data = {};
  for (const [k, v] of Object.entries(flatten(raw))) data[k] = safeDecode(v);
  return { url, data };
}

function makePick(data) {
  // case-insensitive: GHL a veces manda "Phone" o "Email" con mayúscula
  const lower = {};
  for (const [k, v] of Object.entries(data)) lower[k.toLowerCase()] = v;
  return (...keys) => {
    for (const k of keys) {
      const v = lower[k.toLowerCase()];
      if (v !== undefined && v !== null && String(v).trim() && String(v) !== '[object Object]') {
        return String(v).trim();
      }
    }
    return '';
  };
}

function extractContact(data) {
  const pick = makePick(data);

  const telefono = normalizePhone(
    pick(
      'telefono', 'phone', 'whatsapp', 'celular', 'mobile',
      'invitee_phone',            // algunos setups de Calendly
      'text_reminder_number',     // campo nativo de recordatorio por SMS
      'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5',
    ) || findPhoneByShape(data),  // último recurso: buscar por forma
  );

  // Calendly manda invitee_full_name VACÍO y los datos partidos en first/last.
  // GHL manda full_name y también first_name/last_name.
  const nombre =
    pick('nombre', 'full_name', 'fullName', 'nombre_completo', 'invitee_full_name', 'name') ||
    [pick('invitee_first_name', 'first_name', 'firstName', 'firstname'),
     pick('invitee_last_name', 'last_name', 'lastName', 'lastname', 'apellido')].filter(Boolean).join(' ');

  const primerNombre = nombre.split(/\s+/)[0] || '';
  const email = pick('email', 'correo', 'invitee_email', 'email_address').toLowerCase();

  return { pick, telefono, nombre, primerNombre, email };
}

// ─── Payload para el flujo de AGENDA (Calendly) ─────────────────────────
function buildAgendaPayload(data) {
  const { pick, telefono, nombre, primerNombre, email } = extractContact(data);

  const inicio = pick('event_start_time');  // ISO con offset, ej. 2026-08-24T09:20:00-04:00
  const asesor = pick('assigned_to');       // "Valentín Borja"
  const asesorNombre = asesor.split(/\s+/)[0] || '';   // "Valentín", sin el apellido

  // Link del autodiagnóstico ya armado y encodeado, listo para pegar en la
  // plantilla. Dos motivos para armarlo acá y no con variables sueltas en
  // FunnelChat: (1) el apellido del asesor mete un espacio y WhatsApp corta
  // el enlace ahí; (2) los acentos sin encodear lo rompen igual.
  const linkDiag =
    'https://test-presesion.netlify.app/?asignado=' + encodeURIComponent(asesorNombre) +
    '&nombre=' + encodeURIComponent(primerNombre);

  return {
    nombre,
    primer_nombre: primerNombre,                    // para el "Hola {{}}" de la plantilla
    email,
    telefono,                                       // con +, ej. +5491112345678
    telefono_sin_plus: telefono.replace(/^\+/, ''), // sin +, ej. 5491112345678
    asesor,                                         // "Valentín Borja"
    asesor_nombre: asesorNombre,                    // "Valentín" — sin apellido
    cita_inicio: inicio,
    cita_texto: formatCita(inicio),                 // "martes 24 de agosto, 09:20 h"
    link_autodiagnostico: linkDiag,
    origen: pick('origen', 'source') || 'thx-page',
    fecha: new Date().toISOString(),
    params: data,  // TODO lo que llegó, por si querés mapear otro campo en FunnelChat
  };
}

// ─── Payload para el flujo de WEBINAR (form de GHL) ─────────────────────
function buildWebinarPayload(data) {
  const { pick, telefono, nombre, primerNombre, email } = extractContact(data);

  // Campos que la landing manda ocultos al form (ver LEEME-versiones-fijas.md)
  const etapa      = pick('etapa').toUpperCase();
  const equipo     = pick('equipo').toUpperCase();
  const nivel      = pick('nivel').toLowerCase();
  const califica   = (pick('califica').toLowerCase() || (etapa === 'C' ? 'no' : 'si'));
  const claseFecha = pick('clase_fecha');            // "2026-09-22"
  const edicion    = pick('edicion', 'utm_campaign'); // "clase-sep22-alto-rendimiento"

  return {
    nombre,
    primer_nombre: primerNombre,
    email,
    telefono,
    telefono_sin_plus: telefono.replace(/^\+/, ''),
    // datos de la clase: lo que vino del form gana; si no, lo que está en Netlify
    clase_fecha:  claseFecha,
    clase_texto:  formatFecha(claseFecha),                       // "martes 22 de septiembre"
    clase_titulo: pick('clase_titulo') || process.env.WEBINAR_CLASE_TITULO || '',
    clase_hora:   pick('clase_hora')   || process.env.WEBINAR_CLASE_HORA   || '',
    grupo_whatsapp: pick('grupo_whatsapp') || process.env.WEBINAR_GRUPO_WHATSAPP || '',
    edicion,
    // quiz
    etapa, equipo, nivel, califica,
    dedicacion: pick('dedicacion'),
    // tracking
    utm_source:   pick('utm_source'),
    utm_medium:   pick('utm_medium'),
    utm_campaign: pick('utm_campaign'),
    utm_content:  pick('utm_content'),
    ghl_contact_id: pick('contact_id', 'contactId', 'id'),
    origen: pick('origen', 'source') || 'webinar-registro',
    fecha: new Date().toISOString(),
    params: data,
  };
}

async function forward(target, payload) {
  const r = await fetch(target, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return { status: r.status, body: (await r.text()).slice(0, 300) };
}

export default async (req) => {
  // Preflight del navegador
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  const { url, data } = await readInput(req);
  const esWebinar = /\/webinar\/?$/.test(url.pathname);
  const flujo = esWebinar ? 'webinar' : 'agenda';

  // Token opcional para /webinar (la URL del workflow de GHL no es pública, pero por las dudas)
  if (esWebinar && process.env.WEBINAR_TOKEN) {
    const token = data.token || req.headers.get('x-nfm-token') || '';
    if (token !== process.env.WEBINAR_TOKEN) {
      return Response.json({ ok: false, error: 'token inválido' }, { status: 401, headers: CORS });
    }
  }
  delete data.token;

  const payload = esWebinar ? buildWebinarPayload(data) : buildAgendaPayload(data);

  // Modo prueba: muestra lo que parseó y no envía nada
  if (data.debug === '1') {
    return Response.json({ ok: true, debug: true, flujo, payload }, { headers: CORS });
  }

  if (!payload.email && !payload.telefono) {
    return Response.json(
      { ok: false, error: 'Falta email y teléfono', recibido: data },
      { status: 400, headers: CORS },
    );
  }

  if (esWebinar && !payload.telefono) {
    // Sin teléfono no hay WhatsApp que mandar. 200 para que GHL no reintente.
    return Response.json(
      { ok: false, flujo, skipped: true, error: 'El registro no trae teléfono', recibido: data },
      { headers: CORS },
    );
  }

  if (esWebinar && process.env.WEBINAR_SOLO_CALIFICA === '1' && payload.califica === 'no') {
    return Response.json(
      { ok: true, flujo, skipped: true, motivo: 'califica=no (eligió C en el quiz)', telefono: payload.telefono },
      { headers: CORS },
    );
  }

  const envName = esWebinar ? 'FUNNELCHAT_WEBHOOK_URL_WEBINAR' : 'FUNNELCHAT_WEBHOOK_URL';
  const target = process.env[envName];
  if (!target) {
    return Response.json(
      { ok: false, error: `${envName} no configurada en Netlify` },
      { status: 500, headers: CORS },
    );
  }

  // Reenvía a FunnelChat desde el servidor: sin CORS y sin exponer la URL
  let fc;
  try {
    fc = await forward(target, payload);
  } catch (e) {
    return Response.json(
      { ok: false, error: 'No se pudo contactar a FunnelChat: ' + e.message },
      { status: 502, headers: CORS },
    );
  }

  return Response.json(
    {
      ok: fc.status >= 200 && fc.status < 300,
      flujo,
      funnelchat_status: fc.status,
      funnelchat_respuesta: fc.body,
      enviado: { nombre: payload.nombre, email: payload.email, telefono: payload.telefono },
    },
    { headers: CORS },
  );
};

export const config = { path: ['/lead', '/webinar'] };
