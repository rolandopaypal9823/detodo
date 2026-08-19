// Guardado del guion en Netlify Blobs.
//   GET  /api/doc  -> { data, rev, at }      lee la versión guardada
//   PUT  /api/doc  -> { ok, rev, at }        guarda una versión nueva
//
// Protección: si existe la variable de entorno EDIT_TOKEN, toda escritura
// debe traer el header x-edit-token con ese valor. Si no existe, se permite
// escribir y la respuesta avisa que el documento está sin proteger.
//
// Concurrencia: el cliente manda el `rev` que tenía cargado. Si en el medio
// alguien guardó, devuelve 409 con el rev vigente y no pisa nada.

import { getStore } from "@netlify/blobs";

const KEY = "guion";
const STORE = "guion-vsl-platinum";
const MAX_BYTES = 4 * 1024 * 1024;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });

export default async (req) => {
  const store = getStore(STORE);
  const token = process.env.EDIT_TOKEN || "";
  const guarded = token.length > 0;

  if (req.method === "GET") {
    const hit = await store.getWithMetadata(KEY, { type: "json" });
    return json({
      data: hit ? hit.data : null,
      rev: hit?.metadata?.rev ?? 0,
      at: hit?.metadata?.at ?? null,
      guarded,
    });
  }

  if (req.method === "PUT") {
    if (guarded && req.headers.get("x-edit-token") !== token) {
      return json({ error: "unauthorized" }, 401);
    }

    let body;
    try {
      body = await req.json();
    } catch {
      return json({ error: "bad_json" }, 400);
    }
    if (!body || typeof body.data !== "object" || body.data === null) {
      return json({ error: "bad_payload" }, 400);
    }

    const payload = JSON.stringify(body.data);
    if (payload.length > MAX_BYTES) return json({ error: "too_large" }, 413);

    const hit = await store.getWithMetadata(KEY, { type: "json" });
    const curRev = hit?.metadata?.rev ?? 0;

    // compare-and-set: si el cliente venía de una versión vieja, no pisa
    if (typeof body.rev === "number" && body.rev !== curRev) {
      return json({ error: "conflict", rev: curRev, at: hit?.metadata?.at ?? null }, 409);
    }

    const rev = curRev + 1;
    const at = new Date().toISOString();
    await store.setJSON(KEY, body.data, { metadata: { rev, at } });
    return json({ ok: true, rev, at, guarded });
  }

  return json({ error: "method_not_allowed" }, 405);
};

export const config = { path: "/.netlify/functions/doc" };
