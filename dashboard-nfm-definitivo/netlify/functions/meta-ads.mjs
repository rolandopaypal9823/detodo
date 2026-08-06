// netlify/functions/meta-ads.mjs
// Lee data de ANUNCIOS de Meta (Marketing API) por nivel: campaña / conjunto / anuncio.
// READ-ONLY (solo GET, permiso ads_read). Token e IDs solo en env vars.
export const config = { path: "/api/meta-ads" };

const VER = process.env.META_API_VERSION || "v21.0";
const GRAPH = `https://graph.facebook.com/${VER}`;

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const token = process.env.META_ACCESS_TOKEN;
  let body = {};
  try { body = await req.json(); } catch {}
  // Cuenta publicitaria por marca: META_AD_ACCOUNT_ID_<MARCA> → META_AD_ACCOUNT_ID.
  const suf = String(body?.marca || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  let acct = (suf && process.env[`META_AD_ACCOUNT_ID_${suf}`]) || process.env.META_AD_ACCOUNT_ID || "";
  if (!token || !acct) return json({ error: "missing_config", message: `Configurá META_ACCESS_TOKEN y META_AD_ACCOUNT_ID${suf ? ("_" + suf + " (o el genérico)") : ""} en Netlify.` }, 500);
  if (!acct.startsWith("act_")) acct = "act_" + acct.replace(/^act_/, "");

  const level = ["campaign", "adset", "ad"].includes(body?.level) ? body.level : "campaign";
  const datePreset = (body?.datePreset || "last_30d").toString();

  const fields = [
    "campaign_name", "campaign_id", "adset_name", "adset_id", "ad_name", "ad_id",
    "spend", "impressions", "reach", "clicks", "ctr", "cpc", "cpm", "frequency",
    "actions", "action_values", "purchase_roas", "cost_per_action_type"
  ].join(",");

  try {
    const url = `${GRAPH}/${acct}/insights?level=${level}&fields=${fields}&date_preset=${encodeURIComponent(datePreset)}&limit=300&access_token=${encodeURIComponent(token)}`;
    const r = await fetch(url);
    const d = await r.json().catch(() => ({}));
    if (!r.ok || d.error) {
      return json({ error: "meta_error", message: d?.error?.message || ("HTTP " + r.status), code: d?.error?.code }, r.status === 400 ? 400 : 502);
    }
    const rows = (d.data || []).map((it) => normalizeAd(it, level));
    return json({ ok: true, level, datePreset, count: rows.length, rows, at: new Date().toISOString() });
  } catch (e) {
    return json({ error: "meta_error", message: e?.message || String(e) }, 502);
  }
};

function num(v) { const n = Number(v); return isNaN(n) ? 0 : n; }
function sumActions(actions, types) {
  if (!Array.isArray(actions)) return 0;
  return actions.filter(a => types.some(t => (a.action_type || "").includes(t))).reduce((s, a) => s + num(a.value), 0);
}
// Mapa action_type -> valor (para inspeccionar todos los eventos disponibles, incl. conversiones custom)
function arrToMap(arr) { const m = {}; if (Array.isArray(arr)) arr.forEach(a => { if (a.action_type) m[a.action_type] = num(a.value); }); return m; }
function normalizeAd(it, level) {
  const name = level === "ad" ? it.ad_name : level === "adset" ? it.adset_name : it.campaign_name;
  const id = level === "ad" ? it.ad_id : level === "adset" ? it.adset_id : it.campaign_id;
  const purchases = sumActions(it.actions, ["purchase"]);
  const leads = sumActions(it.actions, ["lead"]);
  const registrations = sumActions(it.actions, ["complete_registration", "registration"]);
  const schedules = sumActions(it.actions, ["schedule"]);
  const roas = Array.isArray(it.purchase_roas) && it.purchase_roas[0] ? num(it.purchase_roas[0].value) : 0;
  const purchaseValue = sumActions(it.action_values, ["purchase"]);
  return {
    level, id, name: name || "(sin nombre)",
    campaignName: it.campaign_name || "", adsetName: it.adset_name || "", adId: it.ad_id || "",
    spend: num(it.spend), impressions: num(it.impressions), reach: num(it.reach), clicks: num(it.clicks),
    ctr: num(it.ctr), cpc: num(it.cpc), cpm: num(it.cpm), frequency: num(it.frequency),
    purchases, leads, registrations, schedules, purchaseValue, roas,
    // breakdowns crudos: para mapear costo por registro/agendamiento/conversión (incl. eventos custom)
    results: arrToMap(it.actions),
    costs: arrToMap(it.cost_per_action_type)
  };
}

function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
