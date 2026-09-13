// Calendly -> GHL bridge
//
// Modo A (recomendado, sin token de GHL):
//   Verifica la firma de Calendly y reenvia un JSON limpio, por POST,
//   a la URL del trigger "Inbound Webhook" de un workflow de GHL.
//   Adentro del workflow, GHL busca/crea el contacto por email
//   ({{trigger.body.email}}) y sigue con tag / Meta CAPI.
//   Variable necesaria: GHL_INBOUND_WEBHOOK_URL
//
// Modo B (respaldo, si tu plan de GHL no tiene Inbound Webhook trigger):
//   La funcion misma hace upsert del contacto y le pone el tag via la
//   API de GHL (Private Integration token).
//   Variables necesarias: GHL_API_TOKEN, GHL_LOCATION_ID
//
// Si estan las dos, se usa el Modo A.

const crypto = require("crypto");

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const env = (k, fallback) => {
  const v = process.env[k];
  return v === undefined || v === "" ? fallback : v;
};

// --- Verificacion de firma de Calendly ---------------------------------
function verifySignature(rawBody, header, signingKey) {
  if (!signingKey) return true;
  if (!header) return false;
  const parts = Object.fromEntries(
    header.split(",").map((p) => p.trim().split("=").map((s) => s.trim()))
  );
  if (!parts.t || !parts.v1) return false;
  const expected = crypto
    .createHmac("sha256", signingKey)
    .update(`${parts.t}.${rawBody}`)
    .digest("hex");
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(parts.v1));
  } catch {
    return false;
  }
}

// --- Helpers de datos ----------------------------------------------------
function pickPhone(invitee) {
  if (invitee.text_reminder_number) return invitee.text_reminder_number;
  const qa = invitee.questions_and_answers || [];
  const hit = qa.find((q) =>
    /tel|phone|whatsapp|celular|m[oó]vil|n[uú]mero/i.test(q.question || "")
  );
  return hit ? hit.answer : "";
}

function normalizePhone(p) {
  if (!p) return "";
  const s = String(p).trim();
  const digits = s.replace(/[^\d]/g, "");
  if (!digits) return "";
  return `+${digits}`;
}

function splitName(invitee) {
  if (invitee.first_name || invitee.last_name) {
    return { firstName: invitee.first_name || "", lastName: invitee.last_name || "" };
  }
  const full = (invitee.name || "").trim();
  if (!full) return { firstName: "", lastName: "" };
  const [firstName, ...rest] = full.split(/\s+/);
  return { firstName, lastName: rest.join(" ") };
}

function buildCleanPayload(eventType, invitee) {
  const { firstName, lastName } = splitName(invitee);
  return {
    event: eventType, // "invitee.created" | "invitee.canceled"
    email: (invitee.email || "").trim().toLowerCase(),
    phone: normalizePhone(pickPhone(invitee)),
    firstName,
    lastName,
    startTime: (invitee.scheduled_event && invitee.scheduled_event.start_time) || "",
    source: "Calendly",
  };
}

// --- Modo A: reenviar a un Inbound Webhook de GHL ------------------------
async function forwardToGhlWebhook(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`GHL webhook -> ${res.status}: ${text.slice(0, 300)}`);
  return text;
}

// --- Modo B: API de GHL (respaldo) ---------------------------------------
async function ghlApi(path, method, body) {
  const res = await fetch(`${GHL_BASE}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${env("GHL_API_TOKEN")}`,
      Version: GHL_VERSION,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json = {};
  try { json = text ? JSON.parse(text) : {}; } catch { json = { raw: text }; }
  if (!res.ok) throw new Error(`GHL ${method} ${path} -> ${res.status}: ${text.slice(0, 300)}`);
  return json;
}

async function upsertAndTagViaApi(payload) {
  const body = {
    locationId: env("GHL_LOCATION_ID"),
    email: payload.email,
    firstName: payload.firstName,
    lastName: payload.lastName,
    source: "Calendly",
  };
  if (payload.phone) body.phone = payload.phone;
  const fechaKey = env("GHL_FIELD_FECHA_AGENDA", "");
  if (fechaKey && payload.startTime) {
    body.customFields = [{ key: fechaKey, field_value: payload.startTime }];
  }
  const out = await ghlApi("/contacts/upsert", "POST", body);
  const contactId = out.contact && out.contact.id ? out.contact.id : null;
  if (!contactId) throw new Error("upsert sin contact.id");

  const tag = payload.event === "invitee.canceled"
    ? env("GHL_TAG_CANCELO", "cancelo_agenda")
    : env("GHL_TAG_AGENDO", "agendo");
  try { await ghlApi(`/contacts/${contactId}/tags`, "DELETE", { tags: [tag] }); } catch {}
  await ghlApi(`/contacts/${contactId}/tags`, "POST", { tags: [tag] });
  return contactId;
}

// --- Handler -------------------------------------------------------------
exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  const rawBody = event.isBase64Encoded
    ? Buffer.from(event.body || "", "base64").toString("utf8")
    : event.body || "";

  const sigHeader =
    event.headers["calendly-webhook-signature"] ||
    event.headers["Calendly-Webhook-Signature"];

  if (!verifySignature(rawBody, sigHeader, env("CALENDLY_SIGNING_KEY"))) {
    return { statusCode: 401, body: "Bad signature" };
  }

  let data;
  try {
    data = JSON.parse(rawBody);
  } catch {
    return { statusCode: 400, body: "Invalid JSON" };
  }

  const eventType = data.event;
  const invitee = data.payload || {};
  const payload = buildCleanPayload(eventType, invitee);
  if (!payload.email) return { statusCode: 200, body: "No email, ignored" };

  const inboundUrl = env("GHL_INBOUND_WEBHOOK_URL", "");

  try {
    if (inboundUrl) {
      await forwardToGhlWebhook(inboundUrl, payload);
      console.log(JSON.stringify({ ok: true, mode: "forward", ...payload }));
      return { statusCode: 200, body: JSON.stringify({ ok: true, mode: "forward" }) };
    }
    const contactId = await upsertAndTagViaApi(payload);
    console.log(JSON.stringify({ ok: true, mode: "api", contactId, ...payload }));
    return { statusCode: 200, body: JSON.stringify({ ok: true, mode: "api", contactId }) };
  } catch (err) {
    console.error(JSON.stringify({ ok: false, ...payload, error: err.message }));
    return { statusCode: 500, body: JSON.stringify({ ok: false, error: err.message }) };
  }
};

exports._internal = { verifySignature, pickPhone, normalizePhone, splitName, buildCleanPayload };
