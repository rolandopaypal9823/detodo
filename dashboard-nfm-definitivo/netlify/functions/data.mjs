import { getStore } from "@netlify/blobs";

// Persistencia compartida del dashboard en Netlify Blobs.
//   GET  /api/data  -> devuelve { files, prompts, history }
//   POST /api/data  -> guarda { files, prompts } (+ opcional _log para el historial)
// Token opcional: si está seteada la env var NFM_DATA_TOKEN, se exige el header
// "x-nfm-token" igual. Si no está seteada, la función opera abierta (modo simple).
export const config = {
  path: "/api/data",
};

const STORE = "nfm-dashboard";
const KEY = "dataset";

export default async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors() });
  }

  // Auth opcional
  const required = process.env.NFM_DATA_TOKEN;
  if (required) {
    const got = req.headers.get("x-nfm-token");
    if (got !== required) return json({ error: "unauthorized" }, 401);
  }

  let store;
  try {
    store = getStore(STORE);
  } catch (e) {
    return json({ error: "blobs_unavailable", message: String(e?.message || e) }, 500);
  }

  if (req.method === "GET") {
    const data = await store.get(KEY, { type: "json" });
    return json(data || { files: [], prompts: {}, history: [] });
  }

  if (req.method === "POST") {
    let body;
    try {
      body = await req.json();
    } catch {
      return json({ error: "invalid_json" }, 400);
    }

    const prev = (await store.get(KEY, { type: "json" })) || {};
    const history = Array.isArray(prev.history) ? prev.history : [];

    if (body._log) {
      history.push({ at: new Date().toISOString(), ...body._log });
      // Mantener el historial acotado
      if (history.length > 200) history.splice(0, history.length - 200);
    }

    const payload = {
      files: Array.isArray(body.files) ? body.files : [],
      prompts: body.prompts && typeof body.prompts === "object" ? body.prompts : {},
      // Competidores (IG/YouTube) y Cerebro IA: se preservan si el POST no los manda.
      competitors: body.competitors && typeof body.competitors === "object" ? body.competitors : (prev.competitors || {}),
      context: Array.isArray(body.context) ? body.context : (prev.context || []),
      // Configuración inicial y objetivo de seguidores: viajan con la data para
      // que al re-deployar una versión nueva el dashboard siga siendo el tuyo.
      setup: body.setup && typeof body.setup === "object" ? body.setup : (prev.setup || null),
      goal: body.goal && typeof body.goal === "object" ? body.goal : (prev.goal || {}),
      history,
      updatedAt: new Date().toISOString(),
    };

    await store.setJSON(KEY, payload);
    return json({
      ok: true,
      savedAt: payload.updatedAt,
      files: payload.files.length,
      history: history.length,
    });
  }

  return json({ error: "method_not_allowed" }, 405);
};

function cors() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, x-nfm-token",
  };
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json", ...cors() },
  });
}
