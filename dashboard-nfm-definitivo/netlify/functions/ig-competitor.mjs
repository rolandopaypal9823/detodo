// netlify/functions/ig-competitor.mjs
// Competidores de Instagram. Usa DOS actores dedicados de Apify:
//   - apify/instagram-reel-scraper  (reels + TRANSCRIPT)
//   - apify/instagram-post-scraper  (posts / carruseles)
// Corre ambos en paralelo, espera a que terminen (poll) y fusiona los resultados.
// READ-ONLY. Token solo en env var (APIFY_API_TOKEN). Proxy residencial para no ser bloqueado por IG.
export const config = { path: "/api/ig-competitor" };

const REEL_ACTOR = "apify~instagram-reel-scraper";
const POST_ACTOR = "apify~instagram-post-scraper";

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const token = process.env.APIFY_API_TOKEN;
  if (!token) return json({ error: "missing_api_key", message: "Configurá APIFY_API_TOKEN en Netlify (apify.com → Settings → Integrations)." }, 500);

  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }

  // ── POLL: ya hay runs en marcha ──
  if (Array.isArray(body?.runs) && body.runs.length) {
    try {
      const statuses = await Promise.all(body.runs.map(async (run) => {
        try {
          const r = await fetch(`https://api.apify.com/v2/actor-runs/${run.runId}?token=${token}`);
          const d = await r.json().catch(() => ({}));
          return { type: run.type, runId: run.runId, status: d?.data?.status || "UNKNOWN", datasetId: run.datasetId || d?.data?.defaultDatasetId };
        } catch { return { type: run.type, runId: run.runId, status: "UNKNOWN", datasetId: run.datasetId }; }
      }));
      const TERMINAL = ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"];
      const done = statuses.every((s) => TERMINAL.includes(s.status));
      if (!done) return json({ ok: true, status: "RUNNING", runs: statuses.map((s) => ({ type: s.type, runId: s.runId, datasetId: s.datasetId })) });

      let raw = [];
      for (const s of statuses) {
        if (s.status === "SUCCEEDED" && s.datasetId) {
          const items = await fetchItems(s.datasetId, token);
          raw.push(...items.map((it) => ({ ...it, _type: s.type })));
        }
      }
      const items = dedupe(normalize(raw));
      const debug = {
        rawCount: raw.length,
        firstKeys: Object.keys(raw[0] || {}),
        sample: JSON.stringify(raw[0] || {}).slice(0, 1500),
        runStatuses: statuses.map((s) => s.type + ":" + s.status).join(", ")
      };
      return json({ ok: true, status: "SUCCEEDED", items, debug });
    } catch (e) {
      return json({ ok: false, error: "apify_error", message: e?.message || String(e) }, 502);
    }
  }

  // ── START ──
  const rawProfile = (body?.profile || "").toString().trim();
  if (!rawProfile) return json({ error: "profile_required" }, 400);
  const username = rawProfile.replace(/^@/, "").replace(/^https?:\/\/(www\.)?instagram\.com\//i, "").replace(/[/?].*$/, "").trim();
  if (!username) return json({ error: "bad_profile" }, 400);
  const limit = Math.min(Math.max(parseInt(body?.limit, 10) || 18, 5), 40);

  // Formatos a traer: 'reel' (reels) y/o 'post' (carruseles/fotos). Default ambos.
  // Menos formatos = menos runs de Apify = menos créditos.
  const wanted = Array.isArray(body?.formats) && body.formats.length ? body.formats : ["reel", "post"];
  const wantReel = wanted.includes("reel");
  const wantPost = wanted.includes("post");

  // ── Los dos controles de gasto que faltaban ────────────────────────────
  // 1) La transcripción es lo más lento y lo más caro del scrapeo. Antes iba
  //    SIEMPRE en true, aunque nadie la mirara. Ahora la pide el dashboard.
  // 2) El rango acota cuántas piezas hay para traer: los actores cobran POR
  //    RESULTADO, así que "último mes" cuesta una fracción de "todo".
  const includeTranscript = body?.transcript === true;
  const desde = rangeSince(body?.range);

  // Estos actores dedicados manejan el proxy residencial internamente (no aceptan campo "proxy").
  const reelInput = { username: [username], resultsLimit: limit, includeTranscript };
  const postInput = { username: [username], resultsLimit: limit };
  if (desde) { reelInput.onlyPostsNewerThan = desde; postInput.onlyPostsNewerThan = desde; }

  try {
    const [reel, post] = await Promise.all([
      wantReel ? startRun(REEL_ACTOR, reelInput, token) : Promise.resolve(null),
      wantPost ? startRun(POST_ACTOR, postInput, token) : Promise.resolve(null),
    ]);
    const runs = [];
    if (reel) runs.push({ type: "reel", runId: reel.id, datasetId: reel.datasetId });
    if (post) runs.push({ type: "post", runId: post.id, datasetId: post.datasetId });
    if (!runs.length) return json({ error: "apify_error", message: "No pude arrancar los scrapers de Apify (¿crédito/residential disponible?)." }, 502);
    return json({ ok: true, status: "RUNNING", runs, username });
  } catch (e) {
    return json({ error: "apify_error", message: e?.message || String(e) }, 502);
  }
};

// 'month' | 'quarter' | 'all' → fecha ISO desde la que traer, o null (todo).
function rangeSince(range) {
  const dias = range === "month" ? 30 : range === "quarter" ? 90 : 0;
  if (!dias) return null;
  return new Date(Date.now() - dias * 86400000).toISOString().slice(0, 10);
}

async function startRun(actor, input, token) {
  try {
    const r = await fetch(`https://api.apify.com/v2/acts/${actor}/runs?token=${token}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input) });
    const d = await r.json().catch(() => ({}));
    if (r.ok && d?.data?.id) return { id: d.data.id, datasetId: d.data.defaultDatasetId };
  } catch { /* ignore */ }
  return null;
}

async function fetchItems(dsId, token) {
  if (!dsId) return [];
  const r = await fetch(`https://api.apify.com/v2/datasets/${dsId}/items?token=${token}&clean=true`);
  return await r.json().catch(() => []);
}

function num(v) { const n = Number(v); return isNaN(n) ? 0 : n; }

function normalize(items) {
  return (items || [])
    .filter((it) => it && (it.shortCode || it.url || it.id))
    .map((it) => {
      const shortCode = it.shortCode || (it.url || "").split("/").filter(Boolean).pop() || it.id || "";
      const type = it._type === "reel" ? "Reel" : (it.type === "Sidecar" ? "Carrusel" : it.type === "Video" ? "Video" : "Foto");
      return {
        id: shortCode,
        url: it.url || (shortCode ? `https://www.instagram.com/p/${shortCode}/` : ""),
        type,
        caption: it.caption || "",
        likes: Math.max(0, num(it.likesCount)),
        comments: Math.max(0, num(it.commentsCount)),
        views: num(it.videoViewCount) || num(it.videoPlayCount) || 0,
        thumb: it.displayUrl || "",
        videoUrl: it.videoUrl || "",
        transcript: (it.transcript || it.transcription || it.captions || it.subtitles || it.text || "").toString(),
        timestamp: it.timestamp || ""
      };
    });
}

function dedupe(rows) {
  const seen = new Set();
  return rows.filter((r) => { if (!r.id || seen.has(r.id)) return false; seen.add(r.id); return true; });
}

function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
