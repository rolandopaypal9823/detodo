// netlify/functions/gemini-image.mjs
// Generación de imágenes con Gemini (Nano Banana). El token va SOLO en env var.
export const config = { path: "/api/gemini-image" };

// Modelo estable por defecto; subir a gemini-3.1-flash-image (Nano Banana 2) vía env si se quiere.
const MODEL = process.env.GEMINI_IMAGE_MODEL || "gemini-2.5-flash-image";

export default async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const key = process.env.GEMINI_API_KEY;
  if (!key) return json({ error: "missing_api_key", message: "Configurá GEMINI_API_KEY en las env vars de Netlify (la sacás gratis en aistudio.google.com)." }, 500);

  let body;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }

  const prompt = (body?.prompt || "").toString().trim();
  if (!prompt) return json({ error: "prompt_required" }, 400);
  const aspectRatio = (body?.aspectRatio || "16:9").toString();

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
    const payload = {
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { responseModalities: ["Image"], imageConfig: { aspectRatio } }
    };
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify(payload)
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const reason = data?.error?.message || ("HTTP " + res.status);
      return json({ error: "gemini_error", message: reason }, res.status === 400 ? 400 : 502);
    }
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inlineData || p.inline_data);
    const inline = imgPart?.inlineData || imgPart?.inline_data;
    if (!inline?.data) {
      const txt = parts.find((p) => p.text)?.text;
      return json({ error: "no_image", message: txt ? ("El modelo respondió texto en vez de imagen: " + txt.slice(0, 200)) : "El modelo no devolvió una imagen. Probá reformular el prompt." }, 502);
    }
    const mime = inline.mimeType || inline.mime_type || "image/png";
    return json({ ok: true, image: `data:${mime};base64,${inline.data}`, mime, at: new Date().toISOString() });
  } catch (e) {
    return json({ error: "gemini_error", message: e?.message || String(e) }, 502);
  }
};

function cors() {
  return { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };
}
function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ...cors() } });
}
