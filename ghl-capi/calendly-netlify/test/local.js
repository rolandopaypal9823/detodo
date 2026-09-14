const crypto = require("crypto");
const assert = require("assert");

process.env.GHL_API_TOKEN = "pit-test";
process.env.GHL_LOCATION_ID = "LOC123";
process.env.GHL_FIELD_FBCLID = "fbclid";
process.env.CALENDLY_SIGNING_KEY = "secret-test";

const { handler, _internal } = require("../netlify/functions/calendly-webhook.js");

function mockFetch(calls) {
  global.fetch = async (url, opts) => {
    calls.push({ url, method: opts.method, body: opts.body ? JSON.parse(opts.body) : null });
    if (url.endsWith("/contacts/upsert")) {
      return { ok: true, status: 200, text: async () => JSON.stringify({ contact: { id: "C1" } }) };
    }
    if (url.includes("/tags") && opts.method === "DELETE") {
      return { ok: false, status: 404, text: async () => "no tag" };
    }
    return { ok: true, status: 200, text: async () => "{}" };
  };
}
const post = (body, headers = {}) => ({ httpMethod: "POST", headers, body: JSON.stringify(body) });

(async () => {
  assert.strictEqual(_internal.normalizePhone("+54 9 11 5555-1234"), "+5491155551234");
  assert.deepStrictEqual(_internal.splitName("Juan Perez Lopez"), { firstName: "Juan", lastName: "Perez Lopez" });
  assert.strictEqual(_internal.parsePayload({ event: "agenda", email: "A@B.com" }).via, "thankyou");
  assert.strictEqual(_internal.parsePayload({ event: "invitee.created", payload: { email: "x@y.com" } }).via, "webhook");

  // CORS preflight
  let res = await handler({ httpMethod: "OPTIONS", headers: {} });
  assert.strictEqual(res.statusCode, 204);
  assert.strictEqual(res.headers["Access-Control-Allow-Origin"], "*");

  // A) thank you page: SIN firma, con fbclid
  let calls = []; mockFetch(calls);
  res = await handler(post({
    event: "agenda",
    email: "Juan@Test.com",
    fullName: "Juan Perez Lopez",
    phone: "+54 9 11 5555-1234",
    startTime: "2026-09-15T18:00:00Z",
    fbclid: "IwAR_test123",
  }));
  assert.strictEqual(res.statusCode, 200, `esperaba 200, dio ${res.statusCode} ${res.body}`);
  assert.strictEqual(JSON.parse(res.body).ok, true);
  let upsert = calls.find((c) => c.url.endsWith("/contacts/upsert"));
  assert.strictEqual(upsert.body.email, "juan@test.com");
  assert.strictEqual(upsert.body.phone, "+5491155551234");
  assert.deepStrictEqual(upsert.body.customFields, [{ key: "fbclid", field_value: "IwAR_test123" }]);
  let tagPost = calls.find((c) => c.url.endsWith("/contacts/C1/tags") && c.method === "POST");
  assert.deepStrictEqual(tagPost.body, { tags: ["agendo"] });
  assert.strictEqual(res.headers["Access-Control-Allow-Origin"], "*", "falta CORS en la respuesta");

  // B) webhook de Calendly: firma invalida -> 401
  const wh = { event: "invitee.created", payload: { email: "otro@test.com", name: "Ana Gomez" } };
  const raw = JSON.stringify(wh);
  const t = Math.floor(Date.now() / 1000);
  res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=deadbeef` }, body: raw });
  assert.strictEqual(res.statusCode, 401, "firma invalida deberia dar 401");

  // B) firma valida -> 200
  calls = []; mockFetch(calls);
  const v1 = crypto.createHmac("sha256", "secret-test").update(`${t}.${raw}`).digest("hex");
  res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=${v1}` }, body: raw });
  assert.strictEqual(res.statusCode, 200, `esperaba 200, dio ${res.statusCode} ${res.body}`);

  // cancelacion via thank you page
  calls = []; mockFetch(calls);
  res = await handler(post({ event: "cancelo", email: "x@y.com" }));
  tagPost = calls.find((c) => c.url.endsWith("/tags") && c.method === "POST");
  assert.deepStrictEqual(tagPost.body, { tags: ["cancelo_agenda"] });

  // sin email: no llama a GHL
  calls = []; mockFetch(calls);
  res = await handler(post({ event: "agenda" }));
  assert.strictEqual(res.statusCode, 200);
  assert.strictEqual(calls.length, 0, "no deberia llamar a GHL sin email");

  // JSON invalido
  res = await handler({ httpMethod: "POST", headers: {}, body: "no soy json" });
  assert.strictEqual(res.statusCode, 400);

  console.log("OK: funcion validada (thank you page, webhook Calendly, CORS, casos borde)");
})().catch((e) => { console.error("FALLO:", e.message); process.exit(1); });
