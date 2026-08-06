// netlify/functions/youtube.mjs
var config = {
  path: "/api/youtube"
};
var API = "https://www.googleapis.com/youtube/v3";
var MAX = 5;
var youtube_default = async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  const key = process.env.YOUTUBE_API_KEY;
  if (!key) return json({ error: "missing_api_key", message: "Configur\xE1 YOUTUBE_API_KEY en las env vars de Netlify." }, 500);
  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  const raw = (body?.channel || "").toString().trim();
  if (!raw) return json({ error: "channel_required" }, 400);
  const max = Math.min(Math.max(parseInt(body?.max, 10) || MAX, 1), 10);
  try {
    const ch = await resolveChannel(raw, key);
    if (!ch) return json({ error: "channel_not_found", message: "No encontr\xE9 ese canal. Prob\xE1 con la URL completa o el @handle." }, 404);
    const uploads = ch.contentDetails?.relatedPlaylists?.uploads;
    if (!uploads) return json({ error: "no_uploads", message: "El canal no tiene videos p\xFAblicos." }, 404);
    const pl = await apiGet(`${API}/playlistItems?part=contentDetails&maxResults=50&playlistId=${uploads}&key=${key}`);
    const ids = (pl.items || []).map((i) => i.contentDetails?.videoId).filter(Boolean);
    if (!ids.length) return json({ error: "no_videos", message: "No hay videos p\xFAblicos para analizar." }, 404);
    const vids = await apiGet(`${API}/videos?part=snippet,statistics,contentDetails&id=${ids.slice(0, 50).join(",")}&key=${key}`);
    const videos = (vids.items || []).map((v) => ({
      id: v.id,
      title: v.snippet?.title || "",
      url: "https://www.youtube.com/watch?v=" + v.id,
      views: parseInt(v.statistics?.viewCount, 10) || 0,
      likes: parseInt(v.statistics?.likeCount, 10) || 0,
      comments: parseInt(v.statistics?.commentCount, 10) || 0,
      published: v.snippet?.publishedAt || "",
      duration: iso8601ToClock(v.contentDetails?.duration || ""),
      thumb: pickThumb(v.snippet?.thumbnails)
    })).sort((a, b) => b.views - a.views).slice(0, max);
    return json({
      channel: {
        id: ch.id,
        title: ch.snippet?.title || "",
        thumb: pickThumb(ch.snippet?.thumbnails),
        subs: parseInt(ch.statistics?.subscriberCount, 10) || 0,
        url: "https://www.youtube.com/channel/" + ch.id
      },
      videos,
      at: (/* @__PURE__ */ new Date()).toISOString()
    });
  } catch (e) {
    return json({ error: "youtube_error", message: e?.message || String(e) }, 502);
  }
};
async function resolveChannel(raw, key) {
  let handle = "", username = "", channelId = "", query = "";
  const s = raw.replace(/\s+/g, " ").trim();
  const mCh = s.match(/youtube\.com\/channel\/(UC[\w-]{20,})/i);
  const mHandleUrl = s.match(/youtube\.com\/@([\w.\-]+)/i);
  const mUser = s.match(/youtube\.com\/(?:c|user)\/([\w.\-]+)/i);
  if (mCh) channelId = mCh[1];
  else if (mHandleUrl) handle = mHandleUrl[1];
  else if (mUser) username = mUser[1];
  else if (/^UC[\w-]{20,}$/.test(s)) channelId = s;
  else if (s.startsWith("@")) handle = s.slice(1);
  else query = s;
  if (channelId) {
    const r = await apiGet(`${API}/channels?part=snippet,statistics,contentDetails&id=${channelId}&key=${key}`);
    if (r.items?.length) return r.items[0];
  }
  if (handle) {
    const r = await apiGet(`${API}/channels?part=snippet,statistics,contentDetails&forHandle=@${encodeURIComponent(handle)}&key=${key}`);
    if (r.items?.length) return r.items[0];
    query = query || handle;
  }
  if (username) {
    const r = await apiGet(`${API}/channels?part=snippet,statistics,contentDetails&forUsername=${encodeURIComponent(username)}&key=${key}`);
    if (r.items?.length) return r.items[0];
    query = query || username;
  }
  if (query) {
    const sr = await apiGet(`${API}/search?part=snippet&type=channel&maxResults=1&q=${encodeURIComponent(query)}&key=${key}`);
    const id = sr.items?.[0]?.snippet?.channelId || sr.items?.[0]?.id?.channelId;
    if (id) {
      const r = await apiGet(`${API}/channels?part=snippet,statistics,contentDetails&id=${id}&key=${key}`);
      if (r.items?.length) return r.items[0];
    }
  }
  return null;
}
async function apiGet(url) {
  const res = await fetch(url);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const reason = data?.error?.errors?.[0]?.reason || data?.error?.message || "HTTP " + res.status;
    const e = new Error(reason);
    e.status = res.status;
    throw e;
  }
  return data;
}
function iso8601ToClock(d) {
  const m = /P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/.exec(d || "");
  if (!m) return "";
  const days = +(m[1] || 0), h = +(m[2] || 0) + days * 24, mi = +(m[3] || 0), s = +(m[4] || 0);
  const pad = (n) => String(n).padStart(2, "0");
  return h > 0 ? `${h}:${pad(mi)}:${pad(s)}` : `${mi}:${pad(s)}`;
}
function pickThumb(t) {
  return t?.medium?.url || t?.high?.url || t?.default?.url || "";
}
function cors() {
  return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };
}
function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } });
}
export {
  config,
  youtube_default as default
};
