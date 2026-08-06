import Anthropic from "@anthropic-ai/sdk";

export const config = {
  path: "/api/claude-chat",
};

const SYSTEM_PROMPT = `Sos un analista senior de redes sociales que trabaja con Nicolás Fernández Miranda (NFM) y el Instituto de Productividad.

Tu rol:
- Analizar métricas reales de Instagram, YouTube, Facebook y LinkedIn que te paso adjuntas.
- Responder en español rioplatense, directo, sin vueltas, como si hablaras con un colega.
- Citar números concretos (views, eng rate, follows, etc.). Si no podés afirmar algo con la data, decilo.
- No inventes posts ni cuentas. Si te preguntan por algo que no está en la data, decilo.
- Cuando das una recomendación, es accionable y específica ("publicar reels en franja 18-21h porque X vs Y"), no genérica.
- Si ves un outlier que distorsiona promedios, marcalo.
- Si comparás marcas o redes, sé explícito sobre el criterio (views, eng rate, follows ganados, etc.).
- Distinguí por formato (Reel vs Carrusel) y, cuando aplique, reels de prueba (#NFM) vs reels normales.
- Las piezas marcadas como colaboración se publicaron con otra cuenta; tenelas en cuenta al juzgar el rendimiento de la cuenta principal.
- Cuando te pregunten por hooks o "qué funciona", mirá las descripciones de las piezas top y señalá patrones de apertura / palabras ganadoras, y decí con qué seguir y con qué no.

Las marcas que vas a ver:
- Nico Fernández (cuenta personal)
- Instituto de Productividad
- Hackeá tu Cerebro
- Doble Click

Formato: markdown ligero (bold, listas) cuando ayude a la lectura. Sin emojis salvo que el usuario los use primero.`;

export default async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: corsHeaders(),
    });
  }
  if (req.method !== "POST") {
    return json({ error: "method_not_allowed" }, 405);
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return json({ error: "missing_api_key", message: "Configurá ANTHROPIC_API_KEY en las env vars de Netlify." }, 500);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  const { messages = [], metricsContext = "", systemPromptOverride } = body;
  if (!Array.isArray(messages) || messages.length === 0) {
    return json({ error: "messages_required" }, 400);
  }

  // Prompt editable desde el dashboard; si no viene, se usa el default.
  const sysText = (typeof systemPromptOverride === "string" && systemPromptOverride.trim())
    ? systemPromptOverride
    : SYSTEM_PROMPT;

  const client = new Anthropic({ apiKey });

  // System como array de bloques para poder cachear el contexto de métricas.
  // El primer bloque (instrucciones) cambia poco; el segundo (data) tampoco
  // dentro de una sesión, así que marcamos el último con cache_control.
  const system = [
    { type: "text", text: sysText },
    {
      type: "text",
      text: `--- DATA ACTUAL DEL DASHBOARD ---\n${metricsContext || "(sin data cargada)"}`,
      cache_control: { type: "ephemeral" },
    },
  ];

  // Convertir mensajes al formato Anthropic. Solo roles user/assistant con string content.
  const apiMessages = messages
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content }));

  if (apiMessages.length === 0 || apiMessages[0].role !== "user") {
    return json({ error: "first_message_must_be_user" }, 400);
  }

  try {
    const stream = client.messages.stream({
      model: "claude-sonnet-4-6",
      max_tokens: 2048,
      system,
      messages: apiMessages,
    });

    // Construimos un ReadableStream que sólo emite los deltas de texto
    // (más simple de consumir desde el front que SSE crudo).
    const encoder = new TextEncoder();
    const readable = new ReadableStream({
      async start(controller) {
        try {
          for await (const event of stream) {
            if (
              event.type === "content_block_delta" &&
              event.delta?.type === "text_delta" &&
              event.delta.text
            ) {
              controller.enqueue(encoder.encode(event.delta.text));
            }
          }
          controller.close();
        } catch (err) {
          // Emitimos el error como texto al final para que el front lo vea
          controller.enqueue(
            encoder.encode(`\n\n[error: ${err?.message || "unknown"}]`)
          );
          controller.close();
        }
      },
    });

    return new Response(readable, {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-cache, no-store",
        "X-Accel-Buffering": "no",
        ...corsHeaders(),
      },
    });
  } catch (err) {
    return json({ error: "anthropic_error", message: err?.message || String(err) }, 500);
  }
};

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
