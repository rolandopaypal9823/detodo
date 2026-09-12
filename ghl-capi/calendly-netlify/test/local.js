// Prueba local sin tocar GHL: mockea fetch y simula un webhook de Calendly.
const crypto = require("crypto");
const assert = require("assert");

process.env.GHL_API_TOKEN = "pit-test";
process.env.GHL_LOCATION_ID = "LOC123";
process.env.CALENDLY_SIGNING_KEY = "secret-test";
process.env.GHL_FIELD_FECHA_AGENDA = "fecha_agenda";

const calls = [];
global.fetch = async (url, opts) => {
  calls.push({ url, method: opts.method, body: opts.body ? JSON.parse(opts.body) : null });
  if (url.endsWith("/contacts/upsert")) {
    return { ok: true, status: 200, text: async () => JSON.stringify({ contact: { id: "C1" }, new: false }) };
  }
  if (url.includes("/tags") && opts.method === "DELETE") {
    return { ok: false, status: 404, text: async () => "no tag" };
  }
  return { ok: true, status: 200, text: async () => "{}" };
};

const { handler, _internal } = require("../netlify/functions/calendly-webhook.js");

const payload = {
  event: "invitee.created",
  payload: {
    email: "Juan@Test.com",
    name: "Juan Perez Lopez",
    text_reminder_number: "+54 9 11 5555-1234",
    scheduled_event: { start_time: "2026-09-15T18:00:00.000000Z" },
    questions_and_answers: [{ question: "Tu WhatsApp", answer: "11 4444 5555" }],
  },
};
const rawBody = JSON.stringify(payload);
const t = Math.floor(Date.now() / 1000);
const v1 = crypto.createHmac("sha256", "secret-test").update(`${t}.${rawBody}`).digest("hex");

(async () => {
  // helpers
  assert.deepStrictEqual(_internal.splitName({ name: "Juan Perez Lopez" }), { firstName: "Juan", lastName: "Perez Lopez" });
  assert.strictEqual(_internal.normalizePhone("+54 9 11 5555-1234"), "+5491155551234");
  assert.strictEqual(_internal.pickPhone({ questions_and_answers: [{ question: "Tu WhatsApp", answer: "11 4444" }] }), "11 4444");

  // firma invalida -> 401
  let res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=deadbeef` }, body: rawBody });
  assert.strictEqual(res.statusCode, 401, "firma invalida deberia dar 401");

  // firma valida -> 200 y llamadas correctas a GHL
  calls.length = 0;
  res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=${v1}` }, body: rawBody });
  assert.strictEqual(res.statusCode, 200, `esperaba 200, dio ${res.statusCode} ${res.body}`);

  const upsert = calls.find((c) => c.url.endsWith("/contacts/upsert"));
  assert.ok(upsert, "no hubo upsert");
  assert.strictEqual(upsert.body.email, "juan@test.com");
  assert.strictEqual(upsert.body.phone, "+5491155551234");
  assert.strictEqual(upsert.body.firstName, "Juan");
  assert.strictEqual(upsert.body.locationId, "LOC123");
  assert.deepStrictEqual(upsert.body.customFields, [{ key: "fecha_agenda", field_value: "2026-09-15T18:00:00.000000Z" }]);

  const tagPost = calls.find((c) => c.url.endsWith("/contacts/C1/tags") && c.method === "POST");
  assert.ok(tagPost, "no se agrego el tag");
  assert.deepStrictEqual(tagPost.body, { tags: ["agendo"] });

  // canceled -> tag cancelo_agenda
  calls.length = 0;
  const cancel = JSON.stringify({ ...payload, event: "invitee.canceled" });
  const v1c = crypto.createHmac("sha256", "secret-test").update(`${t}.${cancel}`).digest("hex");
  res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=${v1c}` }, body: cancel });
  assert.strictEqual(res.statusCode, 200);
  const tagCancel = calls.find((c) => c.url.endsWith("/tags") && c.method === "POST");
  assert.deepStrictEqual(tagCancel.body, { tags: ["cancelo_agenda"] });

  console.log("OK: todas las pruebas pasaron");
})().catch((e) => { console.error("FALLO:", e.message); process.exit(1); });
