// netlify/functions/yt-transcript.mjs
// Transcripción de YouTube. Método PRINCIPAL: Apify (proxy residencial, confiable desde server).
// Fallback GRATIS: API interna de YouTube (InnerTube) — funciona a veces desde datacenter.
// Apify es asíncrono: 1ra llamada arranca el run, las siguientes consultan estado.
export const config = { path: "/api/yt-transcript" };

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";
const INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8";
const APIFY_ACTOR = "topaz_sharingan~youtube-transcript-scraper";

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }

  const videoId = (body?.videoId || "").toString().trim().replace(/^.*v=/, "").slice(0, 20);
  if (!/^[\w-]{6,}$/.test(videoId)) return json({ error: "bad_video_id" }, 400);

  const token = process.env.APIFY_API_TOKEN;

  // ── POLL: ya hay un run de Apify en marcha ──
  if (body?.runId) {
    try {
      const r = await fetch(`https://api.apify.com/v2/actor-runs/${body.runId}?token=${token}`);
      const d = await r.json().catch(() => ({}));
      const status = d?.data?.status;
      if (status === "SUCCEEDED") {
        const items = await fetchItems(body.datasetId || d?.data?.defaultDatasetId, token);
        const text = extractTranscript(items);
        if (text) return json({ ok: true, videoId, text, via: "apify" });
        return json({ ok: false, videoId, error: "no_captions", message: "Apify corrió pero el video no tiene transcripción disponible." });
      }
      if (["FAILED", "ABORTED", "TIMED-OUT"].includes(status)) {
        return json({ ok: false, videoId, status, error: "run_failed", message: "El actor de Apify falló o se canceló. Probá de nuevo." });
      }
      return json({ ok: true, status: status || "RUNNING", runId: body.runId, datasetId: body.datasetId, via: "apify" });
    } catch (e) {
      return json({ ok: false, videoId, error: "apify_error", message: e?.message || String(e) }, 502);
    }
  }

  // ── START ──
  // 1) Apify primario (si hay token)
  if (token) {
    try {
      const input = { startUrls: [`https://www.youtube.com/watch?v=${videoId}`], timestamps: false };
      const r = await fetch(`https://api.apify.com/v2/acts/${APIFY_ACTOR}/runs?token=${token}`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input)
      });
      const d = await r.json().catch(() => ({}));
      if (r.ok && d?.data?.id) {
        return json({ ok: true, status: "RUNNING", runId: d.data.id, datasetId: d.data.defaultDatasetId, via: "apify" });
      }
      // si no arrancó, seguimos al método gratis
    } catch { /* fallback */ }
  }

  // 2) Fallback gratis (InnerTube)
  try {
    const tracks = await getCaptionTracks(videoId);
    if (!tracks.length) {
      return json({ ok: false, videoId, error: "no_captions", message: token
        ? "No pude arrancar Apify y el método gratis tampoco encontró subtítulos. Usá DownSub."
        : "YouTube bloqueó el pedido desde el servidor. Configurá APIFY_API_TOKEN para transcripción confiable, o usá DownSub." });
    }
    const pick = (re) => tracks.find((t) => re.test(t.languageCode || "") && t.kind !== "asr") || tracks.find((t) => re.test(t.languageCode || ""));
    const track = pick(/^es/i) || pick(/^en/i) || tracks[0];
    const { text } = await fetchTranscript(track.baseUrl);
    if (!text) return json({ ok: false, videoId, error: "empty_transcript", message: "No pude leer el texto de los subtítulos. Usá DownSub." });
    return json({ ok: true, videoId, lang: track.languageCode || "", text, via: "free" });
  } catch (e) {
    return json({ ok: false, videoId, error: "transcript_error", message: e?.message || String(e) }, 502);
  }
};

// ── Apify helpers ──
async function fetchItems(dsId, token) {
  if (!dsId) return [];
  const r = await fetch(`https://api.apify.com/v2/datasets/${dsId}/items?token=${token}&clean=true`);
  return await r.json().catch(() => []);
}
function extractTranscript(items) {
  const it = (items || [])[0];
  if (!it) return "";
  let t = it.transcript ?? it.text ?? it.captions ?? "";
  if (Array.isArray(t)) t = t.map((s) => (typeof s === "string" ? s : (s?.text || ""))).join(" ");
  return (t || "").toString().replace(/\s+/g, " ").trim();
}

// ── Fallback gratis: InnerTube ──
async function getCaptionTracks(videoId) {
  const viaApi = await innertubeCaptions(videoId);
  if (viaApi.length) return viaApi;
  return await scrapeCaptions(videoId);
}
async function innertubeCaptions(videoId) {
  const clients = [
    { clientName: "ANDROID", clientVersion: "19.09.37", androidSdkVersion: 30 },
    { clientName: "IOS", clientVersion: "19.09.3", deviceModel: "iPhone14,3" },
    { clientName: "WEB", clientVersion: "2.20240726.00.00" }
  ];
  for (const client of clients) {
    try {
      const res = await fetch(`https://www.youtube.com/youtubei/v1/player?key=${INNERTUBE_KEY}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8" },
        body: JSON.stringify({ context: { client: { ...client, hl: "es", gl: "US" } }, videoId })
      });
      const data = await res.json().catch(() => ({}));
      const t = data?.captions?.playerCaptionsTracklistRenderer?.captionTracks || [];
      const mapped = t.map((x) => ({ baseUrl: x.baseUrl, languageCode: x.languageCode, kind: x.kind || "", name: x.name?.simpleText || x.name?.runs?.[0]?.text || "" })).filter((x) => x.baseUrl);
      if (mapped.length) return mapped;
    } catch { /* siguiente cliente */ }
  }
  return [];
}
async function scrapeCaptions(videoId) {
  const res = await fetch(`https://www.youtube.com/watch?v=${videoId}&hl=es`, {
    headers: { "User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Cookie": "CONSENT=YES+1" }
  });
  const html = await res.text();
  const m = html.match(/"captions":\s*(\{.*?\}),"videoDetails"/s) || html.match(/ytInitialPlayerResponse\s*=\s*(\{.+?\});/s);
  if (!m) return [];
  let tracks = [];
  try {
    if (m[0].startsWith('"captions"')) tracks = JSON.parse(m[1])?.playerCaptionsTracklistRenderer?.captionTracks || [];
    else tracks = JSON.parse(m[1])?.captions?.playerCaptionsTracklistRenderer?.captionTracks || [];
  } catch { tracks = []; }
  return tracks.map((t) => ({ baseUrl: t.baseUrl, languageCode: t.languageCode, kind: t.kind || "", name: t.name?.simpleText || "" })).filter((t) => t.baseUrl);
}
async function fetchTranscript(baseUrl) {
  const url = baseUrl + (baseUrl.includes("fmt=") ? "" : "&fmt=json3");
  const res = await fetch(url, { headers: { "User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8" } });
  const raw = await res.text();
  try {
    const j = JSON.parse(raw);
    if (Array.isArray(j.events)) {
      const segments = [];
      for (const ev of j.events) {
        if (!ev.segs) continue;
        const t = ev.segs.map((s) => s.utf8 || "").join("").replace(/\n/g, " ").trim();
        if (t) segments.push({ start: Math.round((ev.tStartMs || 0) / 1e3), text: t });
      }
      return { text: segments.map((s) => s.text).join(" ").replace(/\s+/g, " ").trim(), segments };
    }
  } catch { /* probar XML */ }
  const segs = [];
  const re = /<text[^>]*start="([\d.]+)"[^>]*>([\s\S]*?)<\/text>/g;
  let mm;
  while ((mm = re.exec(raw)) !== null) {
    const t = decode(mm[2]).replace(/\s+/g, " ").trim();
    if (t) segs.push({ start: Math.round(parseFloat(mm[1]) || 0), text: t });
  }
  return { text: segs.map((s) => s.text).join(" ").replace(/\s+/g, " ").trim(), segments: segs };
}
function decode(s) {
  return String(s || "").replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n));
}
function cors() {
  return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };
}
function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } });
}
