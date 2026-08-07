// netlify/functions/meta-stories.mjs
// Captura READ-ONLY de las stories ACTIVAS (últimas 24h) de la cuenta IG conectada,
// y las archiva en Netlify Blobs (para que el archivo histórico sea durable y compartido).
// Las stories no tienen embed público y son efímeras: por eso se capturan mientras viven.
// Solo GET a Meta. Token + IG user id en env vars: META_ACCESS_TOKEN, META_IG_USER_ID, META_API_VERSION.
import { getStore } from "@netlify/blobs";

export const config = { path: "/api/meta-stories" };

const STORE = "nfm-stories";
const KEY = "archive";

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST" && req.method !== "GET") return json({ error: "method_not_allowed" }, 405);

  // GET ?img=<id> → devuelve la IMAGEN guardada de esa story.
  // Los links que da Meta (media_url / thumbnail_url) van firmados y vencen a
  // las pocas horas: si guardábamos solo el link, el archivo histórico quedaba
  // lleno de imágenes rotas. Ahora se baja el archivo y se sirve desde acá.
  const url = new URL(req.url);
  const imgId = url.searchParams.get("img");
  if (imgId) return serveImage(imgId);

  let body = {};
  try { if (req.method === "POST") body = await req.json(); } catch {}

  // mode:'archive' → devolver solo el archivo guardado (para que el front traiga las auto-capturadas por el cron)
  if (body?.mode === "archive") {
    const arch = await readArchive();
    return json({ ok: true, stories: arch, count: arch.length, source: "archive" });
  }

  const token = process.env.META_ACCESS_TOKEN;
  const igId = resolveIgId(body?.marca);
  if (!token || !igId) return json({ error: "missing_config", message: "Faltan META_ACCESS_TOKEN y META_IG_USER_ID en Netlify (token read-only)." }, 200);

  try {
    const stories = await fetchActiveStories(token, igId, undefined, body?.marca);
    const merged = await appendArchive(stories); // guarda las nuevas + sus imágenes
    return json({ ok: true, stories, count: stories.length, archived: merged, fetchedAt: new Date().toISOString() });
  } catch (e) {
    return json({ ok: false, error: "fetch_error", message: e?.message || String(e) }, 502);
  }
};

// META_IG_USER_ID_<MARCA> → META_IG_USER_ID. Mismo criterio que meta-sync.
export function envSuffix(marca) { return String(marca || "").toUpperCase().replace(/[^A-Z0-9]/g, ""); }
export function resolveIgId(marca) {
  const suf = envSuffix(marca);
  if (suf && process.env[`META_IG_USER_ID_${suf}`]) return process.env[`META_IG_USER_ID_${suf}`];
  return process.env.META_IG_USER_ID || "";
}
// Todas las cuentas de IG configuradas, para que el cron diario las archive todas.
export function allIgAccounts() {
  const out = [];
  const vistos = new Set();
  const push = (marca, id) => { if (id && !vistos.has(id)) { vistos.add(id); out.push({ marca, igId: id }); } };
  ["NICO", "INSTITUTO", "HTC", "DOBLECLICK"].forEach((suf) => push(suf.toLowerCase(), process.env[`META_IG_USER_ID_${suf}`]));
  push("", process.env.META_IG_USER_ID);
  return out;
}

export async function fetchActiveStories(token, igId, ver = process.env.META_API_VERSION || "v21.0", marca = "") {
  const fields = "id,media_type,media_url,thumbnail_url,permalink,timestamp";
  const r = await fetch(`https://graph.facebook.com/${ver}/${igId}/stories?fields=${encodeURIComponent(fields)}&access_token=${encodeURIComponent(token)}`);
  const d = await r.json().catch(() => ({}));
  if (d.error) throw new Error(d.error.message || "Error de Meta");
  const now = new Date().toISOString();
  return (d.data || []).map((s) => ({
    id: s.id, marca, type: s.media_type || "", mediaUrl: s.media_url || "",
    thumb: s.thumbnail_url || s.media_url || "", permalink: s.permalink || "",
    timestamp: s.timestamp || "", capturedAt: now,
  }));
}

async function readArchive() {
  try { const store = getStore(STORE); return (await store.get(KEY, { type: "json" })) || []; }
  catch { return []; }
}

/* Guarda la story en el archivo Y baja su imagen.
   Los links de Meta vencen: sin bajar el archivo, el "archivo histórico" se
   convierte en una grilla de imágenes rotas a las pocas horas. Para los videos
   se baja la miniatura (thumbnail_url), que es lo que se muestra en la grilla. */
export async function appendArchive(stories) {
  try {
    const store = getStore(STORE);
    const prev = (await store.get(KEY, { type: "json" })) || [];
    const seen = new Set(prev.map((x) => x.id));
    const nuevas = stories.filter((s) => s.id && !seen.has(s.id));

    // Bajamos las imágenes en paralelo, pero sin romper si alguna falla:
    // que no se pueda guardar una foto no debe impedir archivar la story.
    await Promise.all(nuevas.map(async (s) => {
      const src = s.thumb || s.mediaUrl;
      if (!src) return;
      try {
        const r = await fetch(src);
        if (!r.ok) return;
        const tipo = r.headers.get("content-type") || "image/jpeg";
        if (!/^image\//.test(tipo)) return;
        const buf = await r.arrayBuffer();
        if (buf.byteLength > 8 * 1024 * 1024) return;   // una story no pesa esto: si pasa, algo raro
        await store.set(imgKey(s.id), buf, { metadata: { contentType: tipo } });
        s.hasImage = true;
      } catch { /* nos quedamos con el link como respaldo */ }
    }));

    nuevas.forEach((s) => { prev.push(s); seen.add(s.id); });
    if (prev.length > 1000) prev.splice(0, prev.length - 1000);
    await store.setJSON(KEY, prev);
    return nuevas.length;
  } catch { return 0; }
}

function imgKey(id) { return "img/" + String(id).replace(/[^A-Za-z0-9_-]/g, ""); }

async function serveImage(id) {
  try {
    const store = getStore(STORE);
    const res = await store.getWithMetadata(imgKey(id), { type: "arrayBuffer" });
    if (!res || !res.data) return new Response("not found", { status: 404, headers: cors() });
    return new Response(res.data, {
      status: 200,
      headers: {
        "Content-Type": (res.metadata && res.metadata.contentType) || "image/jpeg",
        // La story ya pasó: la imagen guardada no cambia más.
        "Cache-Control": "public, max-age=31536000, immutable",
        ...cors(),
      },
    });
  } catch (e) {
    return new Response("error", { status: 500, headers: cors() });
  }
}

function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, GET, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
