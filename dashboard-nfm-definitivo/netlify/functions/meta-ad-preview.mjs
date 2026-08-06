// netlify/functions/meta-ad-preview.mjs
// Devuelve el iframe de PREVIEW de un anuncio (incluye dark posts sin link público).
// READ-ONLY (GET, ads_read).
export const config = { path: "/api/meta-ad-preview" };

const VER = process.env.META_API_VERSION || "v21.0";
const GRAPH = `https://graph.facebook.com/${VER}`;

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const token = process.env.META_ACCESS_TOKEN;
  if (!token) return json({ error: "missing_config", message: "Falta META_ACCESS_TOKEN en Netlify." }, 500);

  let body = {};
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }
  const adId = (body?.adId || "").toString().trim();
  if (!adId) return json({ error: "ad_id_required" }, 400);
  // Formatos válidos: INSTAGRAM_STANDARD, INSTAGRAM_STORY, INSTAGRAM_REELS, DESKTOP_FEED_STANDARD, MOBILE_FEED_STANDARD
  const format = (body?.format || "INSTAGRAM_STANDARD").toString();

  try {
    const url = `${GRAPH}/${adId}/previews?ad_format=${encodeURIComponent(format)}&access_token=${encodeURIComponent(token)}`;
    const r = await fetch(url);
    const d = await r.json().catch(() => ({}));
    if (!r.ok || d.error) return json({ error: "meta_error", message: d?.error?.message || ("HTTP " + r.status) }, r.status === 400 ? 400 : 502);
    const html = d?.data?.[0]?.body || "";
    if (!html) return json({ error: "no_preview", message: "Meta no devolvió preview para ese anuncio/formato." });
    return json({ ok: true, adId, format, html });
  } catch (e) {
    return json({ error: "meta_error", message: e?.message || String(e) }, 502);
  }
};

function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
