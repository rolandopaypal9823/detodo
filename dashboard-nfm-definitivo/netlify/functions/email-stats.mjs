// netlify/functions/email-stats.mjs
// Email / Newsletter READ-ONLY. Soporta Kit (ConvertKit) y Doppler.
// Solo GET a las APIs (nunca escribe). Las keys viven SOLO en env vars de Netlify.
//   Kit:     KIT_API_SECRET   (Kit → Settings → Advanced → API Secret)
//   Doppler: DOPPLER_API_KEY + DOPPLER_ACCOUNT (tu email de login de Doppler)
export const config = { path: "/api/email-stats" };

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }
  const provider = (body?.provider || "kit").toString().toLowerCase();

  try {
    if (provider === "kit") return json(await fetchKit());
    if (provider === "doppler") return json(await fetchDoppler());
    return json({ error: "bad_provider", message: "Proveedor no soportado: " + provider }, 400);
  } catch (e) {
    return json({ ok: false, error: "provider_error", provider, message: e?.message || String(e) }, 502);
  }
};

// ─────── KIT (ConvertKit API v3) ───────
async function fetchKit() {
  const secret = process.env.KIT_API_SECRET || process.env.CONVERTKIT_API_SECRET;
  if (!secret) return { error: "missing_config", provider: "kit", message: "Falta KIT_API_SECRET en Netlify (Kit → Settings → Advanced → API Secret)." };
  const base = "https://api.convertkit.com/v3";

  let account = "";
  try {
    const a = await (await fetch(`${base}/account?api_secret=${encodeURIComponent(secret)}`)).json();
    account = a?.name || a?.primary_email_address || "";
  } catch { /* sigue */ }

  // Suscriptores: total + recientes (para armar la curva de crecimiento)
  let total = 0, totalPages = 1;
  const subDates = [];
  for (let page = 1; page <= 6; page++) {
    const r = await fetch(`${base}/subscribers?api_secret=${encodeURIComponent(secret)}&page=${page}&sort_order=desc`);
    const d = await r.json().catch(() => ({}));
    if (page === 1) { total = num(d?.total_subscribers); totalPages = num(d?.total_pages) || 1; }
    (d?.subscribers || []).forEach((s) => { if (s?.created_at) subDates.push(s.created_at); });
    if (page >= totalPages) break;
  }
  const newByWeek = bucketByWeek(subDates);

  // Broadcasts (newsletters enviadas) + stats de apertura/click
  const campaigns = [];
  try {
    const b = await (await fetch(`${base}/broadcasts?api_secret=${encodeURIComponent(secret)}`)).json();
    const list = (b?.broadcasts || []).slice(0, 8);
    for (const bc of list) {
      try {
        const s = await (await fetch(`${base}/broadcasts/${bc.id}/stats?api_secret=${encodeURIComponent(secret)}`)).json();
        const st = s?.broadcast?.stats || {};
        campaigns.push({
          name: bc.subject || ("Broadcast " + bc.id),
          date: bc.created_at || "",
          recipients: num(st.recipients),
          openRate: round1(num(st.open_rate)),
          clickRate: round1(num(st.click_rate)),
          unsubs: num(st.unsubscribes),
        });
      } catch { /* salteá esta */ }
    }
  } catch { /* sigue */ }

  return { ok: true, provider: "kit", account, totalSubscribers: total, newByWeek, campaigns,
    debug: { sampledSubs: subDates.length, totalPages } };
}

// ─────── DOPPLER (restapi.fromdoppler.com) ───────
async function fetchDoppler() {
  const key = process.env.DOPPLER_API_KEY;
  const acct = process.env.DOPPLER_ACCOUNT; // tu email de login de Doppler
  if (!key || !acct) return { error: "missing_config", provider: "doppler", message: "Faltan DOPPLER_API_KEY y DOPPLER_ACCOUNT (tu email de Doppler) en Netlify." };
  const base = `https://restapi.fromdoppler.com/accounts/${encodeURIComponent(acct)}`;
  const headers = { Authorization: `token ${key}` };

  // Listas → suscriptores
  let lists = [], total = 0;
  try {
    const l = await (await fetch(`${base}/lists?page=1&per_page=200`, { headers })).json();
    lists = (l?.items || []).map((it) => ({ name: it.name, subscribers: num(it.subscribersCount), created: it.creationDate || "" }));
    total = lists.reduce((s, x) => s + x.subscribers, 0);
  } catch { /* sigue */ }

  // Campañas enviadas + métricas
  const campaigns = [];
  try {
    const c = await (await fetch(`${base}/campaigns?state=sent&page=1&per_page=10&sortColumn=date&sortOrder=DESC`, { headers })).json();
    const items = (c?.items || []).slice(0, 8);
    for (const it of items) {
      try {
        const id = it.campaignId || it.id;
        const d = await (await fetch(`${base}/campaigns/${id}`, { headers })).json();
        const sent = num(d.amountSentSubscribers || d.amountSubscribers);
        const opens = num(d.uniqueOpens != null ? d.uniqueOpens : d.opens);
        const clicks = num(d.uniqueClicks != null ? d.uniqueClicks : d.clicks);
        campaigns.push({
          name: d.name || it.name || ("Campaña " + id),
          date: d.creationDate || it.creationDate || "",
          recipients: sent,
          openRate: sent ? round1(opens / sent * 100) : 0,
          clickRate: sent ? round1(clicks / sent * 100) : 0,
          unsubs: num(d.unsubscribedSubscribers || d.amountUnsubscribers),
        });
      } catch { /* salteá esta */ }
    }
  } catch { /* sigue */ }

  return { ok: true, provider: "doppler", account: acct, totalSubscribers: total, lists, campaigns,
    debug: { listCount: lists.length } };
}

function bucketByWeek(dateStrings) {
  const map = {};
  dateStrings.forEach((ds) => {
    const d = new Date(ds); if (isNaN(d)) return;
    const day = d.getUTCDay(); const diff = (day === 0 ? 6 : day - 1);
    const monday = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - diff));
    const k = monday.toISOString().slice(0, 10);
    map[k] = (map[k] || 0) + 1;
  });
  return Object.entries(map).sort(([a], [b]) => a.localeCompare(b)).map(([week, added]) => ({ week, added }));
}
function num(v) { const n = Number(v); return isNaN(n) ? 0 : n; }
function round1(v) { return Math.round(v * 10) / 10; }
function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
