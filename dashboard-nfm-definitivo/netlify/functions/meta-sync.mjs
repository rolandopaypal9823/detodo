// netlify/functions/meta-sync.mjs
// Trae media orgánica de Instagram (reels/carruseles/posts) y la mapea a la MISMA estructura
// interna que el parser de CSV (normalizeMetaRows), para reusar todas las vistas.
// READ-ONLY (GET; instagram_basic + instagram_manage_insights). Token/IDs solo en env vars.
export const config = { path: "/api/meta-sync" };

const VER = process.env.META_API_VERSION || "v21.0";
const GRAPH = `https://graph.facebook.com/${VER}`;

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const token = process.env.META_ACCESS_TOKEN;
  if (!token) return json({ error: "missing_config", message: "Falta META_ACCESS_TOKEN en Netlify." }, 500);

  let body = {};
  try { body = await req.json(); } catch {}
  const marca = (body?.marca || "nico").toString();
  const limit = Math.min(Math.max(parseInt(body?.limit, 10) || 40, 5), 90);

  try {
    const igId = await resolveIgUserId(token, marca);
    if (!igId) return json({ error: "no_ig_account", message: `No encontré la cuenta de Instagram para "${marca}". Configurá META_IG_USER_ID_${envSuffix(marca)} (o META_IG_USER_ID por defecto) en Netlify.` }, 400);

    const fields = "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count";
    const mediaRes = await fetch(`${GRAPH}/${igId}/media?fields=${fields}&limit=${limit}&access_token=${encodeURIComponent(token)}`);
    const mediaData = await mediaRes.json().catch(() => ({}));
    if (!mediaRes.ok || mediaData.error) return json({ error: "meta_error", message: mediaData?.error?.message || ("HTTP " + mediaRes.status) }, 502);

    const media = mediaData.data || [];
    // Insights por pieza en paralelo, con degradación elegante.
    const rows = await Promise.all(media.map(m => mapMedia(m, marca, token)));
    return json({ ok: true, igId, marca, count: rows.length, rows, at: new Date().toISOString() });
  } catch (e) {
    return json({ error: "meta_error", message: e?.message || String(e) }, 502);
  }
};

// Sufijo de env var por marca: 'doble-click' -> 'DOBLECLICK'
function envSuffix(marca) { return String(marca || "").toUpperCase().replace(/[^A-Z0-9]/g, ""); }

// Resuelve el IG user id por marca: META_IG_USER_ID_<MARCA> → META_IG_USER_ID → vía page.
async function resolveIgUserId(token, marca) {
  const suf = envSuffix(marca);
  if (suf && process.env[`META_IG_USER_ID_${suf}`]) return process.env[`META_IG_USER_ID_${suf}`];
  if (process.env.META_IG_USER_ID) return process.env.META_IG_USER_ID;
  const pageId = (suf && process.env[`META_PAGE_ID_${suf}`]) || process.env.META_PAGE_ID;
  if (!pageId) return "";
  const r = await fetch(`${GRAPH}/${pageId}?fields=instagram_business_account&access_token=${encodeURIComponent(token)}`);
  const d = await r.json().catch(() => ({}));
  return d?.instagram_business_account?.id || "";
}

async function fetchInsights(mediaId, token) {
  const sets = ["reach,views,saved,shares,total_interactions", "reach,saved,shares", "reach"];
  for (const metric of sets) {
    try {
      const r = await fetch(`${GRAPH}/${mediaId}/insights?metric=${metric}&access_token=${encodeURIComponent(token)}`);
      const d = await r.json().catch(() => ({}));
      if (r.ok && Array.isArray(d.data)) {
        const out = {};
        d.data.forEach(x => { out[x.name] = x.values?.[0]?.value ?? 0; });
        return out;
      }
    } catch { /* probar set más chico */ }
  }
  return {};
}

function formatoFrom(m) {
  if (m.media_product_type === "REELS") return "Reel";
  if (m.media_product_type === "STORY") return "Story";
  if (m.media_type === "CAROUSEL_ALBUM") return "Carrusel";
  if (m.media_type === "VIDEO") return "Video";
  return "Foto";
}

async function mapMedia(m, marca, token) {
  const ins = await fetchInsights(m.id, token);
  const likes = num(m.like_count);
  const comments = num(m.comments_count);
  const saves = num(ins.saved);
  const shares = num(ins.shares);
  const reach = num(ins.reach);
  const views = num(ins.views) || reach;
  const engagement = num(ins.total_interactions) || (likes + comments + shares + saves);
  const engRate = reach > 0 ? (engagement / reach * 100) : 0;
  const isStory = m.media_product_type === "STORY";
  return {
    kind: isStory ? "meta-stories" : "meta-feed",
    marca, network: "instagram",
    postId: m.id,
    type: m.media_product_type || m.media_type || "",
    formato: formatoFrom(m),
    accountUsername: "", accountName: "", isCollab: false,
    isTest: /#nfm\b/i.test(m.caption || ""),
    description: m.caption || "",
    publishTime: m.timestamp || null,
    link: m.permalink || "",
    views, reach, likes, shares, comments, saves,
    replies: 0, stickerTaps: 0, navigation: 0, follows: 0, profileVisits: 0, duration: 0,
    engagement, engRate,
    source: "meta-api"
  };
}

function num(v) { const n = Number(v); return isNaN(n) ? 0 : n; }
function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
