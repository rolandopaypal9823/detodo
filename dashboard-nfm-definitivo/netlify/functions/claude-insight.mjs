import Anthropic from "@anthropic-ai/sdk";

export const config = {
  path: "/api/claude-insight",
};

const SYSTEM_PROMPT = `Sos un analista senior de redes sociales para Nicolás Fernández Miranda (NFM).

Te paso métricas reales y devolvés insights y recomendaciones en JSON estricto, sin texto extra.

Formato de salida (OBLIGATORIO — JSON puro, sin markdown, sin \`\`\`):
{
  "insights": [
    { "text": "Qué está pasando, con números concretos (HTML <strong> para resaltar)", "severity": "good|warn|bad|info", "confidence": "alta|media|baja" }
  ],
  "recos": [
    { "action": "Acción concreta y aplicable", "why": "Por qué — anclado a un número de la data", "confidence": "alta|media|baja" }
  ]
}

REGLAS DE CONFIANZA (lo más importante — es lo que hace útil el análisis):
- "confidence" mide cuánto te podés FIAR del patrón, NO si el número es alto.
- n>=4 piezas y consistente => "alta". n=2-3 => "media". n=1 (un solo dato) => SIEMPRE "baja".
- NUNCA recomendes repetir o escalar algo que viene de UNA sola pieza (n=1). Si un número es alto pero es n=1, describilo como "posible viral, sin confirmar" y la reco debe ser "testealo de nuevo antes de sacar conclusiones" (confidence "baja").
- Si un promedio está inflado por un outlier, decilo explícito y usá la MEDIANA (te la paso en la data).

SEVERITY:
- "good" = funciona, conviene mantener/duplicar. "bad" = problema que cuesta plata o alcance. "warn" = alerta temprana (ej. fatiga de creativo). "info" = neutro/descriptivo.

CONTENIDO:
- "insights" = QUÉ PASA (con números: views, eng rate, follows, ratios, y el n cuando importe).
- "recos" = QUÉ HACER, específico y aplicable (NO "publicá más contenido de calidad"). Cada reco con su "why" anclado a un número.
- El PRIMER insight es SIEMPRE el de mayor impacto en seguidores/alcance.
- Distinguí por formato (Reel vs Carrusel). Si hay CTA "comentá X", decí qué palabras traen seguidores — respetando la confianza por n (una palabra usada 1 sola vez = confidence baja aunque el número sea alto).
- QUÉ PODÉS LEER: tenés la DESCRIPCIÓN/caption de cada pieza. Podés analizar lo que está escrito: el CTA ("comentá X"), la primera línea (hook ESCRITO), el tema y los hashtags. Eso es dato conocido, no especules: citá el texto.
- QUÉ NO TENÉS: el audio hablado ni lo visual de los reels en video. NO afirmes "el hook del video funcionó por X" si ese hook no está en la descripción — no tenés la transcripción. Limitá tus conclusiones a lo que está en el texto y en los números.

REGLAS DE HONESTIDAD:
- Usá SOLO números que aparezcan en la data. Si das un ratio, mostrá los dos números base.
- No inventes data. Si la muestra total es chica (<10 piezas), decilo y bajá la confianza.
- 1 a 3 insights, 1 a 3 recos. Si no hay nada SÓLIDO para decir, devolvé arrays vacíos.
- Cada texto: una o dos oraciones, español rioplatense directo. <strong> permitido (HTML inline). NO emojis, NO markdown (ni *, ni #, ni listas con guiones).`;

export default async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }
  if (req.method !== "POST") {
    return json({ error: "method_not_allowed" }, 405);
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return json({ error: "missing_api_key" }, 500);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  const { metricsContext = "", scopeLabel = "general", systemPromptOverride, extraInstruction } = body;
  if (!metricsContext) {
    return json({ insights: [], recos: [] });
  }

  // Prompt editable desde el dashboard; si no viene, se usa el default.
  const sysText = (typeof systemPromptOverride === "string" && systemPromptOverride.trim())
    ? systemPromptOverride
    : SYSTEM_PROMPT;

  const client = new Anthropic({ apiKey });

  const system = [
    { type: "text", text: sysText },
  ];

  // Contexto de marca (Cerebro IA: voz, avatar, oferta). Antes se mandaba y se ignoraba.
  // Va como bloque cacheable para que las recos salgan en la voz NFM.
  if (typeof extraInstruction === "string" && extraInstruction.trim()) {
    system.push({
      type: "text",
      text: `--- CONTEXTO DE MARCA (voz, avatar, negocio) ---\nUsá esto para que las recomendaciones suenen como la marca y apunten a su oferta/audiencia. NO inventes números a partir de esto.\n\n${extraInstruction.trim()}`,
      cache_control: { type: "ephemeral" },
    });
  }

  system.push({
    type: "text",
    text: `--- DATA ---\n${metricsContext}`,
    cache_control: { type: "ephemeral" },
  });

  const userPrompt = `Generá insights y recomendaciones para el scope: ${scopeLabel}.
Devolvé SOLO el JSON, nada más.`;

  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      system,
      messages: [{ role: "user", content: userPrompt }],
    });

    const text = response.content
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("")
      .trim();

    // Intentar parsear como JSON. Si el modelo agregó algo extra, extraer el primer objeto.
    const parsed = tryParseJSON(text);
    if (!parsed) {
      return json({
        insights: [`No pude generar un insight estructurado. Respuesta raw: ${text.slice(0, 200)}`],
        recos: [],
      });
    }

    return json({
      insights: Array.isArray(parsed.insights) ? parsed.insights.slice(0, 3) : [],
      recos: Array.isArray(parsed.recos) ? parsed.recos.slice(0, 3) : [],
      _usage: response.usage,
    });
  } catch (err) {
    return json({ error: "anthropic_error", message: err?.message || String(err) }, 500);
  }
};

function tryParseJSON(text) {
  try {
    return JSON.parse(text);
  } catch {
    // Buscar primer { ... } balanceado
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start >= 0 && end > start) {
      try {
        return JSON.parse(text.slice(start, end + 1));
      } catch {
        return null;
      }
    }
    return null;
  }
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders() },
  });
}
