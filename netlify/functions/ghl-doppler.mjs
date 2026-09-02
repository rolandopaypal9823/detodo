/**
 * Puente GoHighLevel -> Doppler Email Marketing.
 *
 * GHL (workflow: "Form submitted" -> accion "Webhook") hace POST JSON a esta URL.
 * La funcion normaliza el contacto y lo suscribe a una lista de Doppler con
 * POST /accounts/{cuenta}/lists/{listId}/subscribers
 * A partir de ahi, la Automatizacion de Doppler ("Al suscribirse a una lista")
 * dispara los mails sola.
 *
 * Variables de entorno (Netlify > Site configuration > Environment variables):
 *   DOPPLER_API_KEY      (obligatoria) API key de Doppler
 *   DOPPLER_ACCOUNT      (obligatoria) email de la cuenta de Doppler
 *   DOPPLER_LIST_ID      (obligatoria) id numerico de la lista destino por defecto
 *   WEBHOOK_SECRET       (opcional, recomendada) token compartido con GHL
 *   DOPPLER_FIELD_MAP    (opcional) JSON { "campoDelLead": "CAMPO_DOPPLER" }
 *   ALLOWED_LIST_IDS     (opcional) ids permitidos separados por coma para override por request
 */

const DOPPLER_BASE = "https://restapi.fromdoppler.com";

/* ---------- helpers ---------- */

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// GHL manda a veces el contacto plano y a veces anidado en customData / contact.
function flatten(payload) {
  const out = {};
  const walk = (obj, depth = 0) => {
    if (!obj || typeof obj !== "object" || depth > 3) return;
    for (const [k, v] of Object.entries(obj)) {
      if (v && typeof v === "object" && !Array.isArray(v)) walk(v, depth + 1);
      else if (out[k] === undefined) out[k] = v;
    }
  };
  walk(payload);
  return out;
}

function pick(flat, keys) {
  for (const k of keys) {
    const v = flat[k];
    if (typeof v === "string" && v.trim()) return v.trim();
    if (typeof v === "number") return String(v);
  }
  return "";
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function normalizeContact(payload) {
  const flat = flatten(payload);

  const email = pick(flat, ["email", "Email", "email_address", "contact_email"]).toLowerCase();

  let first = pick(flat, ["first_name", "firstName", "firstname", "nombre", "Nombre"]);
  let last = pick(flat, ["last_name", "lastName", "lastname", "apellido", "Apellido"]);

  if (!first) {
    const full = pick(flat, ["full_name", "fullName", "name", "contact_name", "nombre_completo"]);
    if (full) {
      const parts = full.split(/\s+/);
      first = parts.shift() || "";
      if (!last) last = parts.join(" ");
    }
  }

  return {
    email,
    first,
    last,
    phone: pick(flat, ["phone", "Phone", "telefono", "Telefono", "celular"]),
    country: pick(flat, ["country", "Country", "pais", "Pais"]),
    flat,
  };
}

function buildFields(contact, fieldMap) {
  const fields = [];
  if (contact.first) fields.push({ name: "FIRSTNAME", value: contact.first });
  if (contact.last) fields.push({ name: "LASTNAME", value: contact.last });

  for (const [source, target] of Object.entries(fieldMap)) {
    const raw = contact.flat[source];
    const value = raw === undefined || raw === null ? "" : String(raw).trim();
    if (value && !fields.some((f) => f.name === target)) {
      fields.push({ name: target, value: value.slice(0, 400) });
    }
  }
  return fields;
}

function parseFieldMap(raw) {
  if (!raw) return {};
  try {
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    console.warn("DOPPLER_FIELD_MAP no es JSON valido, se ignora");
    return {};
  }
}

/* ---------- llamada a Doppler ---------- */

async function postSubscriber({ account, apiKey, listId, body }) {
  const url = `${DOPPLER_BASE}/accounts/${encodeURIComponent(account)}/lists/${encodeURIComponent(
    listId
  )}/subscribers`;

  let last = { status: 0, text: "" };

  // Reintentos solo ante 429 / 5xx / error de red.
  for (let attempt = 0; attempt < 3; attempt++) {
    if (attempt) await sleep(400 * 2 ** (attempt - 1));
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: `token ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });
      const text = await res.text();
      last = { status: res.status, text };
      if (res.ok) return last;
      if (res.status !== 429 && res.status < 500) return last;
    } catch (err) {
      last = { status: 0, text: String(err && err.message ? err.message : err) };
    }
  }
  return last;
}

/* ---------- handler ---------- */

export default async function handler(request) {
  if (request.method === "GET") {
    return json(200, { ok: true, service: "ghl-doppler-bridge", hint: "usar POST" });
  }
  if (request.method !== "POST") {
    return json(405, { ok: false, error: "method_not_allowed" });
  }

  const { DOPPLER_API_KEY, DOPPLER_ACCOUNT, DOPPLER_LIST_ID, WEBHOOK_SECRET } = process.env;

  const missing = [
    ["DOPPLER_API_KEY", DOPPLER_API_KEY],
    ["DOPPLER_ACCOUNT", DOPPLER_ACCOUNT],
    ["DOPPLER_LIST_ID", DOPPLER_LIST_ID],
  ]
    .filter(([, v]) => !v)
    .map(([k]) => k);

  if (missing.length) {
    console.error("Faltan variables de entorno:", missing.join(", "));
    return json(500, { ok: false, error: "missing_env", missing });
  }

  const url = new URL(request.url);

  // Autenticacion del webhook: ?key=... o header x-webhook-token.
  if (WEBHOOK_SECRET) {
    const provided =
      request.headers.get("x-webhook-token") ||
      url.searchParams.get("key") ||
      (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
    if (provided !== WEBHOOK_SECRET) {
      return json(401, { ok: false, error: "unauthorized" });
    }
  }

  let payload;
  try {
    payload = await request.json();
  } catch {
    return json(400, { ok: false, error: "invalid_json" });
  }

  const contact = normalizeContact(payload);
  if (!EMAIL_RE.test(contact.email)) {
    return json(400, { ok: false, error: "invalid_email", email: contact.email || null });
  }

  // Lista destino: default por env, con override opcional (?list= o listId en el body).
  const requested = String(
    url.searchParams.get("list") || contact.flat.listId || contact.flat.doppler_list_id || ""
  ).trim();

  let listId = DOPPLER_LIST_ID;
  if (requested && requested !== DOPPLER_LIST_ID) {
    const allowed = (process.env.ALLOWED_LIST_IDS || "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    if (allowed.includes(requested)) listId = requested;
    else console.warn(`Lista ${requested} no permitida, se usa la lista por defecto`);
  }

  const fieldMap = parseFieldMap(process.env.DOPPLER_FIELD_MAP);
  const fields = buildFields(contact, fieldMap);

  let result = await postSubscriber({
    account: DOPPLER_ACCOUNT,
    apiKey: DOPPLER_API_KEY,
    listId,
    body: { email: contact.email, fields },
  });

  // Si Doppler rechaza por un campo inexistente, reintenta con lo minimo indispensable.
  if (result.status === 400 && fields.length && /field/i.test(result.text)) {
    console.warn("Doppler rechazo los fields, reintento solo con el email:", result.text);
    result = await postSubscriber({
      account: DOPPLER_ACCOUNT,
      apiKey: DOPPLER_API_KEY,
      listId,
      body: { email: contact.email },
    });
  }

  if (result.status >= 200 && result.status < 300) {
    console.log(`OK ${contact.email} -> lista ${listId} (${result.status})`);
    return json(200, { ok: true, email: contact.email, listId, dopplerStatus: result.status });
  }

  console.error(`Doppler ${result.status} para ${contact.email}: ${result.text}`);
  // 5xx para que GHL reintente; 4xx (dato invalido) no tiene sentido reintentarlo.
  const status = result.status >= 400 && result.status < 500 ? 422 : 502;
  return json(status, {
    ok: false,
    error: "doppler_error",
    dopplerStatus: result.status,
    detail: result.text.slice(0, 500),
  });
}

export const config = { path: "/api/ghl-doppler" };
