// netlify/functions/feeds.mjs
var config = {
  path: "/api/feeds"
};
var MAX_URLS = 20;
var MAX_ITEMS = 20;
var TIMEOUT_MS = 9e3;
var feeds_default = async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);
  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  let urls = Array.isArray(body?.urls) ? body.urls : [];
  urls = urls.map((u) => typeof u === "string" ? normalizeInput(u) : "").filter(Boolean);
  urls = [...new Set(urls)].slice(0, MAX_URLS);
  if (!urls.length) return json({ error: "no_urls" }, 400);
  const feeds = await Promise.all(urls.map((u) => fetchFeed(u)));
  return json({ feeds, at: (/* @__PURE__ */ new Date()).toISOString() });
};
function normalizeInput(s) {
  let v = String(s || "").trim();
  if (!v) return "";
  if (!/^https?:\/\//i.test(v)) v = "https://" + v.replace(/^\/+/, "");
  try {
    return new URL(v).href;
  } catch {
    return "";
  }
}
var COMMON_PATHS = ["/feed/", "/feed", "/rss/", "/rss", "/rss.xml", "/atom.xml", "/index.xml", "/feed/rss/", "/feeds/posts/default?alt=rss", "/blog/feed/"];
async function httpGet(url) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      signal: ctrl.signal,
      redirect: "follow",
      headers: {
        "User-Agent": "Mozilla/5.0 (compatible; RadarBot/1.0; +dashboard)",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, text/html, */*"
      }
    });
    const text = res.ok ? await res.text() : "";
    return { ok: res.ok, status: res.status, text, finalUrl: res.url || url };
  } catch (e) {
    return { ok: false, status: 0, text: "", error: e?.name === "AbortError" ? "timeout" : String(e?.message || e), finalUrl: url };
  } finally {
    clearTimeout(t);
  }
}
function looksLikeFeed(xml) {
  if (!xml) return false;
  const head = xml.slice(0, 1500).toLowerCase();
  return /<rss[\s>]/.test(head) || /<feed[\s>]/.test(head) || /<rdf:rdf[\s>]/.test(head) || head.includes("<?xml") && (head.includes("<channel") || head.includes("<entry"));
}
function discoverFeedUrl(html, baseUrl) {
  const links = matchAll(html, /<link[^>]+>/gi);
  for (const tag of links) {
    if (!/type=["']application\/(rss|atom)\+xml["']/i.test(tag)) continue;
    const m = /href=["']([^"']+)["']/i.exec(tag);
    if (m) {
      try {
        return new URL(decode(m[1]), baseUrl).href;
      } catch {
      }
    }
  }
  return "";
}
async function fetchFeed(input) {
  const first = await httpGet(input);
  if (first.ok && looksLikeFeed(first.text)) return parseFeed(first.finalUrl, first.text);
  if (first.ok && first.text) {
    const discovered = discoverFeedUrl(first.text, first.finalUrl);
    if (discovered) {
      const r = await httpGet(discovered);
      if (r.ok && looksLikeFeed(r.text)) return parseFeed(discovered, r.text);
    }
  }
  let base;
  try {
    base = new URL(input);
  } catch {
    base = null;
  }
  if (base) {
    for (const p of COMMON_PATHS) {
      const candidate = new URL(p, base.origin).href;
      const r = await httpGet(candidate);
      if (r.ok && looksLikeFeed(r.text)) return parseFeed(candidate, r.text);
    }
  }
  const why = first.ok ? "no_feed_found" : first.error || "HTTP " + first.status;
  return { url: input, ok: false, error: why, items: [] };
}
function parseFeed(url, xml) {
  const feedTitle = decode(stripTags(firstTag(beforeFirstItem(xml), "title") || hostOf(url)));
  let blocks = matchAll(xml, /<item[\s>][\s\S]*?<\/item>/gi);
  let atom = false;
  if (!blocks.length) {
    blocks = matchAll(xml, /<entry[\s>][\s\S]*?<\/entry>/gi);
    atom = true;
  }
  const items = [];
  for (const b of blocks) {
    const title = decode(stripTags(firstTag(b, "title") || "(sin t\xEDtulo)"));
    const link = atom ? atomLink(b) : decode(stripTags(firstTag(b, "link"))) || extractGuidLink(b);
    const rawDate = firstTag(b, "pubDate") || firstTag(b, "published") || firstTag(b, "updated") || firstTag(b, "dc:date") || "";
    const date = normDate(rawDate);
    const _ts = date ? Date.parse(date) || 0 : 0;
    const rawSum = firstTag(b, "description") || firstTag(b, "summary") || firstTag(b, "content") || firstTag(b, "content:encoded") || "";
    const summary = decode(stripTags(rawSum)).slice(0, 240);
    items.push({ title, link: link || url, date, summary, _ts });
    if (items.length >= MAX_ITEMS) break;
  }
  items.sort((a, b) => (b._ts || 0) - (a._ts || 0));
  return { url, ok: true, title: feedTitle, items: items.map(({ _ts, ...rest }) => rest) };
}
function matchAll(s, re) {
  const out = [];
  let m;
  while ((m = re.exec(s)) !== null) {
    out.push(m[0]);
    if (re.lastIndex === m.index) re.lastIndex++;
  }
  return out;
}
function firstTag(block, tag) {
  if (!block) return "";
  const re = new RegExp("<" + tag + "(?:\\s[^>]*)?>([\\s\\S]*?)<\\/" + tag + ">", "i");
  const m = re.exec(block);
  if (!m) return "";
  return m[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1").trim();
}
function beforeFirstItem(xml) {
  const i = xml.search(/<(item|entry)[\s>]/i);
  return i === -1 ? xml : xml.slice(0, i);
}
function atomLink(block) {
  let m = /<link[^>]*rel=["']alternate["'][^>]*href=["']([^"']+)["']/i.exec(block);
  if (!m) m = /<link[^>]*href=["']([^"']+)["'][^>]*\/?>/i.exec(block);
  return m ? decode(m[1]) : "";
}
function extractGuidLink(block) {
  const g = firstTag(block, "guid");
  return /^https?:\/\//i.test(g) ? g : "";
}
function stripTags(s) {
  return String(s || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}
function decode(s) {
  return String(s || "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/gi, "'").replace(/&apos;/g, "'").replace(/&nbsp;/g, " ").replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16))).trim();
}
function normDate(raw) {
  const s = String(raw || "").trim();
  if (!s) return "";
  const d = new Date(s);
  if (isNaN(d.getTime())) return s;
  return d.toISOString();
}
function hostOf(u) {
  try {
    return new URL(u).hostname.replace(/^www\./, "");
  } catch {
    return u;
  }
}
function cors() {
  return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };
}
function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } });
}
export {
  config,
  feeds_default as default
};
