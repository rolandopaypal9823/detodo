// Puente agendas -> GHL (Netlify Function)
//
// Recibe el agendamiento por dos vias:
//   A) La thank you page de Calendly (JSON simple, desde el navegador)
//   B) El webhook de Calendly (invitee.created / invitee.canceled)
//
// En GHL: crea o actualiza el contacto, le guarda el fbclid si vino,
// y le pone un tag. El tag (trigger GRATIS) dispara el workflow que
// manda Schedule a Meta CAPI.
//
// Variables de entorno (Netlify > Site settings > Environment variables):
//   GHL_API_TOKEN     Private Integration token, empieza con pit-
//   GHL_LOCATION_ID   Settings > Business Profile
//   GHL_TAG_AGENDO    default: agendo
//   GHL_TAG_CANCELO   default: cancelo_agenda
//   GHL_FIELD_FBCLID  default: fbclid
//   ALLOWED_ORIGIN    default: *
//   CALENDLY_SIGNING_KEY  opcional, solo para la via B

const crypto = require("crypto");

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const env = (k, fallback) => {
  const v = process.env[k];
  return v === undefined || v === "" ? fallback : v;
};

const corsHeaders = () => ({
  "Access-Control-Allow-Origin": env("ALLOWED_ORIGIN", "*"),
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
});

const reply = (status, body) => ({
  statusCode: status,
  headers: { "Content-Type": "application/json", ...corsHeaders() },
  body: JSON.stringify(body),
});

function verifySignature(rawBody, header, signingKey) {
  if (!signingKey) return true;
  if (!header) return false;
  const parts = Object.fromEntries(
    header.split(",").map((p) => p.trim().split("=").map((s) => s.trim()))
  );
  if (!parts.t || !parts.v1) return false;
  const expected = crypto.createHmac("sha256", signingKey).update(`${parts.t}.${rawBody}`).digest("hex");
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(parts.v1));
  } catch {
    return false;
  }
}

function normalizePhone(p) {
  if (!p) return "";
  const digits = String(p).replace(/[^\d]/g, "");
  return digits ? `+${digits}` : "";
}

function splitName(full, first, last) {
  if (first || last) return { firstName: first || "", lastName: last || "" };
  const n = (full || "").trim();
  if (!n) return { firstName: "", lastName: "" };
  const [a, ...rest] = n.split(/\s+/);
  return { firstName: a, lastName: rest.join(" ") };
}

// Acepta las dos formas de payload y devuelve una sola
function parsePayload(data) {
  if (data && data.event && data.payload && typeof data.payload === "object") {
    const inv = data.payload;
    const qa = inv.questions_and_answers || [];
    const hit = qa.find((q) => /tel|phone|whatsapp|celular|m[oó]vil|n[uú]mero/i.test(q.question || ""));
    const { firstName, lastName } = splitName(inv.name, inv.first_name, inv.last_name);
    return {
      via: "webhook",
      canceled: data.event === "invitee.canceled",
      email: (inv.email || "").trim().toLowerCase(),
      firstName,
      lastName,
      phone: normalizePhone(inv.text_reminder_number || (hit ? hit.answer : "")),
      startTime: (inv.scheduled_event && inv.scheduled_event.start_time) || "",
      fbclid: "",
    };
  }
  const d = data || {};
  const { firstName, lastName } = splitName(d.fullName || d.name, d.firstName, d.lastName);
  return {
    via: "thankyou",
    canceled: d.event === "cancelo" || d.event === "invitee.canceled",
    email: (d.email || "").trim().toLowerCase(),
    firstName,
    lastName,
    phone: normalizePhone(d.phone),
    startTime: d.startTime || "",
    fbclid: d.fbclid || "",
  };
}

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
  if (!res.ok) throw new Error(`GHL ${method} ${path} -> ${res.status}: ${text.slice(0, 300)}`);
  try { return text ? JSON.parse(text) : {}; } catch { return {}; }
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: corsHeaders(), body: "" };
  }
  if (event.httpMethod !== "POST") {
    return reply(405, { ok: false, error: "Method not allowed" });
  }

  const rawBody = event.isBase64Encoded
    ? Buffer.from(event.body || "", "base64").toString("utf8")
    : event.body || "";

  let data;
  try {
    data = JSON.parse(rawBody);
  } catch {
    return reply(400, { ok: false, error: "Invalid JSON" });
  }

  const p = parsePayload(data);

  // La firma solo aplica a la via B (webhook de Calendly).
  if (p.via === "webhook") {
    const sig = event.headers["calendly-webhook-signature"] || event.headers["Calendly-Webhook-Signature"];
    if (!verifySignature(rawBody, sig, env("CALENDLY_SIGNING_KEY"))) {
      return reply(401, { ok: false, error: "Bad signature" });
    }
  }

  if (!p.email) return reply(200, { ok: true, skipped: "sin email" });

  try {
    const body = {
      locationId: env("GHL_LOCATION_ID"),
      email: p.email,
      firstName: p.firstName,
      lastName: p.lastName,
      source: "Calendly",
    };
    if (p.phone) body.phone = p.phone;
    if (p.fbclid) {
      body.customFields = [{ key: env("GHL_FIELD_FBCLID", "fbclid"), field_value: p.fbclid }];
    }

    const out = await ghl("/contacts/upsert", "POST", body);
    const contactId = out.contact && out.contact.id;
    if (!contactId) throw new Error("upsert sin contact.id");

    const tag = p.canceled ? env("GHL_TAG_CANCELO", "cancelo_agenda") : env("GHL_TAG_AGENDO", "agendo");
    // Quitar y volver a poner: asi dispara tambien si agenda dos veces
    try { await ghl(`/contacts/${contactId}/tags`, "DELETE", { tags: [tag] }); } catch {}
    await ghl(`/contacts/${contactId}/tags`, "POST", { tags: [tag] });

    console.log(JSON.stringify({ ok: true, via: p.via, email: p.email, contactId, tag }));
    return reply(200, { ok: true, contactId, tag });
  } catch (err) {
    console.error(JSON.stringify({ ok: false, via: p.via, email: p.email, error: err.message }));
    return reply(500, { ok: false, error: err.message });
  }
};

exports._internal = { verifySignature, normalizePhone, splitName, parsePayload };
