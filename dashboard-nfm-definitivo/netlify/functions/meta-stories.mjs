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

  let body = {};
  try { if (req.method === "POST") body = await req.json(); } catch {}

  // mode:'archive' → devolver solo el archivo guardado (para que el front traiga las auto-capturadas por el cron)
  if (body?.mode === "archive") {
    const arch = await readArchive();
    return json({ ok: true, stories: arch, count: arch.length, source: "archive" });
  }

  const token = process.env.META_ACCESS_TOKEN;
  const igId = process.env.META_IG_USER_ID;
  if (!token || !igId) return json({ error: "missing_config", message: "Faltan META_ACCESS_TOKEN y META_IG_USER_ID en Netlify (token read-only)." }, 200);

  try {
    const stories = await fetchActiveStories(token, igId);
    const merged = await appendArchive(stories); // guarda las nuevas al archivo durable
    return json({ ok: true, stories, count: stories.length, archived: merged, fetchedAt: new Date().toISOString() });
  } catch (e) {
    return json({ ok: false, error: "fetch_error", message: e?.message || String(e) }, 502);
  }
};

export async function fetchActiveStories(token, igId, ver = process.env.META_API_VERSION || "v21.0") {
  const fields = "id,media_type,media_url,thumbnail_url,permalink,timestamp";
  const r = await fetch(`https://graph.facebook.com/${ver}/${igId}/stories?fields=${encodeURIComponent(fields)}&access_token=${encodeURIComponent(token)}`);
  const d = await r.json().catch(() => ({}));
  if (d.error) throw new Error(d.error.message || "Error de Meta");
  const now = new Date().toISOString();
  return (d.data || []).map((s) => ({
    id: s.id, type: s.media_type || "", mediaUrl: s.media_url || "",
    thumb: s.thumbnail_url || s.media_url || "", permalink: s.permalink || "",
    timestamp: s.timestamp || "", capturedAt: now,
  }));
}

async function readArchive() {
  try { const store = getStore(STORE); return (await store.get(KEY, { type: "json" })) || []; }
  catch { return []; }
}

export async function appendArchive(stories) {
  try {
    const store = getStore(STORE);
    const prev = (await store.get(KEY, { type: "json" })) || [];
    const seen = new Set(prev.map((x) => x.id));
    let added = 0;
    stories.forEach((s) => { if (s.id && !seen.has(s.id)) { prev.push(s); seen.add(s.id); added++; } });
    if (prev.length > 1000) prev.splice(0, prev.length - 1000);
    await store.setJSON(KEY, prev);
    return added;
  } catch { return 0; }
}

function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, GET, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
