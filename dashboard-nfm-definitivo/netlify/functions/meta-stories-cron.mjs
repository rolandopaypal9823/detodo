// netlify/functions/meta-stories-cron.mjs
// Tarea PROGRAMADA (1×/día): captura las stories activas y las archiva en Netlify Blobs,
// para tener un archivo histórico sin depender de que abras el dashboard.
// READ-ONLY. Usa el mismo token/IG id que meta-stories. Si no hay token, no hace nada.
import { fetchActiveStories, appendArchive } from "./meta-stories.mjs";

// Corre todos los días ~09:00 UTC (~06:00 ART). Ajustable.
export const config = { schedule: "0 9 * * *" };

export default async () => {
  const token = process.env.META_ACCESS_TOKEN;
  const igId = process.env.META_IG_USER_ID;
  if (!token || !igId) return new Response("skip: sin META_ACCESS_TOKEN / META_IG_USER_ID", { status: 200 });
  try {
    const stories = await fetchActiveStories(token, igId);
    const added = await appendArchive(stories);
    return new Response(`ok: ${stories.length} activas, ${added} nuevas archivadas`, { status: 200 });
  } catch (e) {
    return new Response("error: " + (e?.message || String(e)), { status: 200 });
  }
};
