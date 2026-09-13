const crypto = require("crypto");
const assert = require("assert");

function withEnv(vars, fn) {
  const prev = {};
  for (const k of Object.keys(vars)) prev[k] = process.env[k];
  Object.assign(process.env, vars);
  return Promise.resolve(fn()).finally(() => {
    for (const k of Object.keys(vars)) {
      if (prev[k] === undefined) delete process.env[k]; else process.env[k] = prev[k];
    }
  });
}

function sign(key, body, t) {
  return crypto.createHmac("sha256", key).update(`${t}.${body}`).digest("hex");
}

const basePayload = {
  event: "invitee.created",
  payload: {
    email: "Juan@Test.com",
    name: "Juan Perez Lopez",
    text_reminder_number: "+54 9 11 5555-1234",
    scheduled_event: { start_time: "2026-09-15T18:00:00.000000Z" },
  },
};

(async () => {
  delete require.cache[require.resolve("../netlify/functions/calendly-webhook.js")];
  const { handler, _internal } = require("../netlify/functions/calendly-webhook.js");

  assert.deepStrictEqual(_internal.splitName({ name: "Juan Perez Lopez" }), { firstName: "Juan", lastName: "Perez Lopez" });
  assert.strictEqual(_internal.normalizePhone("+54 9 11 5555-1234"), "+5491155551234");

  // ---- Modo A: forward a Inbound Webhook de GHL ----
  await withEnv({ CALENDLY_SIGNING_KEY: "secret-test", GHL_INBOUND_WEBHOOK_URL: "https://ghl.example/hooks/abc", GHL_API_TOKEN: "", GHL_LOCATION_ID: "" }, async () => {
    const calls = [];
    global.fetch = async (url, opts) => {
      calls.push({ url, method: opts.method, body: JSON.parse(opts.body) });
      return { ok: true, status: 200, text: async () => "ok" };
    };
    const raw = JSON.stringify(basePayload);
    const t = Math.floor(Date.now() / 1000);
    const v1 = sign("secret-test", raw, t);

    let res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=deadbeef` }, body: raw });
    assert.strictEqual(res.statusCode, 401, "firma invalida deberia dar 401");

    res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=${v1}` }, body: raw });
    assert.strictEqual(res.statusCode, 200, `esperaba 200, dio ${res.statusCode} ${res.body}`);
    assert.strictEqual(calls.length, 1);
    assert.strictEqual(calls[0].url, "https://ghl.example/hooks/abc");
    assert.strictEqual(calls[0].body.email, "juan@test.com");
    assert.strictEqual(calls[0].body.phone, "+5491155551234");
    assert.strictEqual(calls[0].body.firstName, "Juan");
    assert.strictEqual(calls[0].body.event, "invitee.created");
  });

  // ---- Modo B: API de GHL (respaldo, sin GHL_INBOUND_WEBHOOK_URL) ----
  await withEnv({ CALENDLY_SIGNING_KEY: "secret-test", GHL_INBOUND_WEBHOOK_URL: "", GHL_API_TOKEN: "pit-test", GHL_LOCATION_ID: "LOC123", GHL_FIELD_FECHA_AGENDA: "fecha_agenda" }, async () => {
    const calls = [];
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
    const raw = JSON.stringify(basePayload);
    const t = Math.floor(Date.now() / 1000);
    const v1 = sign("secret-test", raw, t);

    const res = await handler({ httpMethod: "POST", headers: { "calendly-webhook-signature": `t=${t},v1=${v1}` }, body: raw });
    assert.strictEqual(res.statusCode, 200, `esperaba 200, dio ${res.statusCode} ${res.body}`);

    const upsert = calls.find((c) => c.url.endsWith("/contacts/upsert"));
    assert.ok(upsert, "no hubo upsert");
    assert.strictEqual(upsert.body.email, "juan@test.com");
    assert.deepStrictEqual(upsert.body.customFields, [{ key: "fecha_agenda", field_value: "2026-09-15T18:00:00.000000Z" }]);

    const tagPost = calls.find((c) => c.url.endsWith("/contacts/C1/tags") && c.method === "POST");
    assert.ok(tagPost, "no se agrego el tag");
    assert.deepStrictEqual(tagPost.body, { tags: ["agendo"] });
  });

  console.log("OK: todas las pruebas pasaron (modo A y modo B)");
})().catch((e) => { console.error("FALLO:", e.message); process.exit(1); });
