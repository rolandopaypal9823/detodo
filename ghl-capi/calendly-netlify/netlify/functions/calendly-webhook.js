// Calendly -> GHL bridge
// Recibe el webhook de Calendly (invitee.created / invitee.canceled),
// hace upsert del contacto en GHL por email/telefono y le pone un tag.
// El tag dispara el workflow de GHL que manda Schedule a Meta CAPI.

const crypto = require("crypto");

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const env = (k, fallback) => {
  const v = process.env[k];
  return v === undefined || v === "" ? fallback : v;
};

// --- Verificacion de firma de Calendly ---------------------------------
// Header: Calendly-Webhook-Signature: t=<ts>,v1=<hmac_sha256_hex>
function verifySignature(rawBody, header, signingKey) {
  if (!signingKey) return true; // sin clave configurada, no verificamos
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
  return s.startsWith("+") ? `+${digits}` : `+${digits}`;
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

// --- Cliente GHL ---------------------------------------------------------
async function ghl(path, method, body) {
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
  if (!res.ok) {
    throw new Error(`GHL ${method} ${path} -> ${res.status}: ${text.slice(0, 300)}`);
  }
  return json;
}

async function upsertContact({ email, phone, firstName, lastName, customFields }) {
  const body = {
    locationId: env("GHL_LOCATION_ID"),
    email,
    firstName,
    lastName,
    source: "Calendly",
  };
  if (phone) body.phone = phone;
  if (customFields && customFields.length) body.customFields = customFields;
  const out = await ghl("/contacts/upsert", "POST", body);
  return out.contact && out.contact.id ? out.contact.id : null;
}

// Quitamos y volvemos a poner el tag para que el trigger "Tag added"
// dispare tambien si la persona agenda por segunda vez.
async function retag(contactId, tag) {
  try {
    await ghl(`/contacts/${contactId}/tags`, "DELETE", { tags: [tag] });
  } catch (e) {
    // si no tenia el tag, GHL puede devolver error: lo ignoramos
  }
  await ghl(`/contacts/${contactId}/tags`, "POST", { tags: [tag] });
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

  const eventType = data.event; // "invitee.created" | "invitee.canceled"
  const invitee = data.payload || {};
  const email = (invitee.email || "").trim().toLowerCase();
  if (!email) return { statusCode: 200, body: "No email, ignored" };

  const { firstName, lastName } = splitName(invitee);
  const phone = normalizePhone(pickPhone(invitee));
  const startTime =
    (invitee.scheduled_event && invitee.scheduled_event.start_time) || "";

  const customFields = [];
  const fechaKey = env("GHL_FIELD_FECHA_AGENDA", "");
  if (fechaKey && startTime) customFields.push({ key: fechaKey, field_value: startTime });

  const tagCreated = env("GHL_TAG_AGENDO", "agendo");
  const tagCanceled = env("GHL_TAG_CANCELO", "cancelo_agenda");

  try {
    const contactId = await upsertContact({ email, phone, firstName, lastName, customFields });
    if (!contactId) throw new Error("upsert sin contact.id");

    if (eventType === "invitee.created") {
      await retag(contactId, tagCreated);
    } else if (eventType === "invitee.canceled") {
      await retag(contactId, tagCanceled);
    }

    console.log(JSON.stringify({ ok: true, eventType, email, contactId, startTime }));
    return { statusCode: 200, body: JSON.stringify({ ok: true, contactId }) };
  } catch (err) {
    console.error(JSON.stringify({ ok: false, eventType, email, error: err.message }));
    // 500 hace que Calendly reintente
    return { statusCode: 500, body: JSON.stringify({ ok: false, error: err.message }) };
  }
};

// exportamos helpers para test local
exports._internal = { verifySignature, pickPhone, normalizePhone, splitName };
