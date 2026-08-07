// netlify/functions/meta-stories-cron.mjs
// Tarea PROGRAMADA (1×/día): captura las stories activas de TODAS las cuentas de
// Instagram configuradas y las archiva en Netlify Blobs — con la imagen bajada,
// no solo el link, porque los que da Meta vencen a las pocas horas.
// Así el archivo histórico existe sin depender de que abras el dashboard.
// READ-ONLY. Si no hay token, no hace nada.
import { fetchActiveStories, appendArchive, allIgAccounts } from "./meta-stories.mjs";

// Corre todos los días ~09:00 UTC (~06:00 ART). Ajustable.
export const config = { schedule: "0 9 * * *" };

export default async () => {
  const token = process.env.META_ACCESS_TOKEN;
  if (!token) return new Response("skip: sin META_ACCESS_TOKEN", { status: 200 });

  const cuentas = allIgAccounts();
  if (!cuentas.length) return new Response("skip: sin META_IG_USER_ID configurado", { status: 200 });

  const partes = [];
  for (const { marca, igId } of cuentas) {
    try {
      const stories = await fetchActiveStories(token, igId, undefined, marca);
      const added = await appendArchive(stories);
      partes.push(`${marca || "default"}: ${stories.length} activas, ${added} nuevas`);
    } catch (e) {
      // Una cuenta que falla no debe cortar el archivado de las demás.
      partes.push(`${marca || "default"}: error — ${e?.message || String(e)}`);
    }
  }
  return new Response("ok · " + partes.join(" · "), { status: 200 });
};
