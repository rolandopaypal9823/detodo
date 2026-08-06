// netlify/functions/whoami.mjs
import { createHash } from "node:crypto";
var config = {
  path: "/api/whoami"
};
var whoami_default = async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors() });
  }
  const key = process.env.ANTHROPIC_API_KEY || "";
  const hasKey = key.length > 0;
  const keyFingerprint = hasKey ? createHash("sha256").update(key).digest("hex").slice(0, 12) : null;
  return json({
    ok: true,
    siteLabel: process.env.SITE_LABEL || "(sin SITE_LABEL)",
    hasAnthropicKey: hasKey,
    keyFingerprint,
    // comparable entre sitios, no revela la key
    keyLength: hasKey ? key.length : 0,
    keyPrefix: hasKey ? key.slice(0, 7) : null,
    // ej "sk-ant-" (no es secreto)
    hasYoutubeKey: !!process.env.YOUTUBE_API_KEY,
    hasGeminiKey: !!process.env.GEMINI_API_KEY,
    hasApifyToken: !!process.env.APIFY_API_TOKEN,
    hasMetaToken: !!process.env.META_ACCESS_TOKEN,
    hasMetaIgId: !!(process.env.META_IG_USER_ID || process.env.META_PAGE_ID),
    hasMetaAdAccount: !!process.env.META_AD_ACCOUNT_ID,
    hasKitKey: !!(process.env.KIT_API_SECRET || process.env.CONVERTKIT_API_SECRET),
    hasDopplerKey: !!(process.env.DOPPLER_API_KEY && process.env.DOPPLER_ACCOUNT),
    hasYtOauth: !!(process.env.YT_OAUTH_CLIENT_ID && process.env.YT_OAUTH_CLIENT_SECRET && process.env.YT_OAUTH_REFRESH_TOKEN),
    dataTokenRequired: !!(process.env.DATA_TOKEN || process.env.NFM_DATA_TOKEN),
    node: process.version,
    at: (/* @__PURE__ */ new Date()).toISOString()
  });
};
function cors() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  };
}
function json(payload, status = 200) {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: { "Content-Type": "application/json", ...cors() }
  });
}
export {
  config,
  whoami_default as default
};
