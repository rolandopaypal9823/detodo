// netlify/functions/yt-analytics.mjs
// YouTube Analytics del CANAL PROPIO (read-only) vía OAuth.
// Scope: https://www.googleapis.com/auth/yt-analytics.readonly (solo lectura).
// Env vars (Netlify): YT_OAUTH_CLIENT_ID, YT_OAUTH_CLIENT_SECRET, YT_OAUTH_REFRESH_TOKEN.
// Se saca un refresh token UNA vez (OAuth Playground) y se guarda en Netlify. No vence.
export const config = { path: "/api/yt-analytics" };

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const cid = process.env.YT_OAUTH_CLIENT_ID;
  const cs = process.env.YT_OAUTH_CLIENT_SECRET;
  const rt = process.env.YT_OAUTH_REFRESH_TOKEN;
  if (!cid || !cs || !rt) return json({ error: "missing_config", message: "Faltan YT_OAUTH_CLIENT_ID, YT_OAUTH_CLIENT_SECRET y YT_OAUTH_REFRESH_TOKEN en Netlify." }, 200);

  let body = {};
  try { body = await req.json(); } catch {}
  const days = Math.min(Math.max(parseInt(body?.days, 10) || 90, 7), 365);
  const end = new Date();
  const start = new Date(end.getTime() - days * 86400000);
  const startDate = start.toISOString().slice(0, 10);
  const endDate = end.toISOString().slice(0, 10);

  try {
    // 1) refresh token → access token
    const tokRes = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ client_id: cid, client_secret: cs, refresh_token: rt, grant_type: "refresh_token" }),
    });
    const tok = await tokRes.json().catch(() => ({}));
    if (!tok.access_token) return json({ error: "oauth_error", message: tok.error_description || tok.error || "No pude renovar el token de Google (revisá las credenciales/refresh token)." }, 200);

    // 2) reporte diario
    const params = new URLSearchParams({
      ids: "channel==MINE", startDate, endDate,
      metrics: "views,estimatedMinutesWatched,subscribersGained,subscribersLost",
      dimensions: "day", sort: "day",
    });
    const rep = await fetch("https://youtubeanalytics.googleapis.com/v2/reports?" + params.toString(), { headers: { Authorization: "Bearer " + tok.access_token } });
    const d = await rep.json().catch(() => ({}));
    if (d.error) return json({ error: "yt_error", message: d.error.message || "Error de YouTube Analytics" }, 200);

    const cols = (d.columnHeaders || []).map((c) => c.name);
    const ix = (n) => cols.indexOf(n);
    const series = (d.rows || []).map((r) => ({
      day: r[ix("day")],
      views: num(r[ix("views")]),
      minutes: num(r[ix("estimatedMinutesWatched")]),
      gained: num(r[ix("subscribersGained")]),
      lost: num(r[ix("subscribersLost")]),
    }));
    const totals = series.reduce((a, s) => ({ views: a.views + s.views, minutes: a.minutes + s.minutes, gained: a.gained + s.gained, lost: a.lost + s.lost }), { views: 0, minutes: 0, gained: 0, lost: 0 });
    return json({ ok: true, startDate, endDate, series, totals, at: new Date().toISOString() });
  } catch (e) {
    return json({ ok: false, error: "fetch_error", message: e?.message || String(e) }, 502);
  }
};

function num(v) { const n = Number(v); return isNaN(n) ? 0 : n; }
function cors() { return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }; }
function json(payload, status = 200) { return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } }); }
