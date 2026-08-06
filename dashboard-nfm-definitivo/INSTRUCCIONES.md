# 🚀 Cómo poner tu dashboard online (10 minutos, sin saber programar)

Es como instalar un programa: subís la carpeta y listo. No necesitás GitHub ni escribir una línea de código.

---

## Paso 1 — Subirlo a Netlify (gratis)

1. Entrá a **https://app.netlify.com/drop**
2. Si no tenés cuenta, creá una **gratis** (con tu Google o tu email).
3. **Arrastrá esta carpeta entera** (la que descomprimiste del ZIP) a la zona que dice *"Drag and drop your site folder here"*.
4. Esperá ~1 minuto. ✅ Tu dashboard queda online en una dirección tipo `algo-random.netlify.app`.
5. (Opcional) Tocá **Site configuration → Change site name** para ponerle un nombre lindo.

La primera vez que lo abrís te va a hacer **5 preguntas** (tu nombre, tu marca, tu logo, qué querés lograr y qué secciones querés usar). Con eso arma el menú a tu medida. Se puede rehacer cuando quieras desde **⚙ Configuración**.

✅ **Ya funciona.** Podés subir tus CSV y ver embudo, rankings, tendencias, objetivos, reporte, calendario y el Radar de noticias. Nada de esto necesita configuración extra ni cuesta un peso.

---

## Paso 2 (opcional) — Prender la IA 🧠

La IA usa **Anthropic (Claude)**. Es tu cuenta y tu gasto: pagás solo lo que uses.

1. Sacá tu key en **console.anthropic.com** → cargá un poco de saldo → **API Keys → Create Key** (copiá la que empieza con `sk-ant-`).
2. En Netlify: tu sitio → **Site configuration → Environment variables → Add a variable**.
   - Key: `ANTHROPIC_API_KEY` — Value: tu key — **Save**.
3. Andá a **Deploys** y volvé a arrastrar la carpeta (o **Trigger deploy**) para que tome la key.

**Cuánto sale.** Los insights y el chat **solo consumen cuando los pedís**: navegar el dashboard no gasta nada. Cada análisis ronda **1,4 centavos de dólar** y cada pregunta del chat **1 centavo**. Con **USD 5** te alcanza para unos cientos. El dashboard lleva su propio contador en **⚙ Configuración → Gasto en IA**.

---

## Paso 3 (opcional) — Prender Competidores de YouTube 🕵️ (gratis)

Usa la **YouTube Data API**. Es gratis y no accede a ninguna cuenta: solo lee datos públicos.

1. En **console.cloud.google.com**: **New Project** → **APIs & Services → Library** → buscá **"YouTube Data API v3"** → **Enable**.
2. **Credentials → Create credentials → API key** (copiá la que empieza con `AIza...`).
3. En Netlify: **Environment variables → Add a variable** → Key `YOUTUBE_API_KEY` → Value tu key → **Save**.
4. Volvé a arrastrar la carpeta (o **Trigger deploy**).

---

## Paso 4 (opcional) — Competidores de Instagram 📸 (pago por uso)

Instagram no tiene API pública para perfiles ajenos, así que se usa un scraper (**Apify**). Se paga **por pieza traída**.

1. Creá tu cuenta en **apify.com** (arranca con USD 5 gratis) → **Settings → Integrations** → copiá tu token.
2. En Netlify: `APIFY_API_TOKEN` → tu token → **Save** → re-deploy.
3. En el dashboard, andá a **Competidores → Instagram**. Antes de cada búsqueda vas a ver **cuánto va a costar** y **cuántas búsquedas te entran con tu saldo**.

**Los tres controles que definen la factura** (todos están arriba de la búsqueda):

| Control | Qué hace |
|---|---|
| **Cuántas piezas** (10/20/30) | Es el más directo: la mitad de piezas, la mitad del costo. |
| **Desde** (último mes / tres meses / todo) | Cuanto más corto el rango, menos hay para traer. |
| **Transcripción** (no traer / traer) | Lo más lento y lo más caro. Dejala apagada para explorar; prendela solo cuando ya sepas qué perfil querés a fondo. Igual ves el copy completo de cada pieza. |

Cargá tu saldo real de Apify en el panel **💵 Gasto en Apify** y el dashboard te descuenta solo desde ese momento.

---

## Paso 5 (opcional) — El resto de los módulos

Todos se prenden igual: cargás la variable en Netlify y re-deployás.

| Querés | Variable(s) | Dónde se saca |
|---|---|---|
| Anuncios de Meta, orgánico de IG y Stories | `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID` + `META_IG_USER_ID` | Token System User de tu App de Meta (read-only) |
| Email / Newsletter | `KIT_API_SECRET` **o** `DOPPLER_API_KEY` + `DOPPLER_ACCOUNT` | Kit → Settings → Advanced · Doppler → API |
| Mi YouTube (tu propio canal) | `YT_OAUTH_CLIENT_ID` + `YT_OAUTH_CLIENT_SECRET` + `YT_OAUTH_REFRESH_TOKEN` | Ver `HANDOFF.md` §5 (paso a paso, sin código) |
| Estudio visual (generar imágenes) | `GEMINI_API_KEY` | aistudio.google.com |
| Proteger la nube con contraseña | `NFM_DATA_TOKEN` | La inventás vos |

---

## ¿Cómo sé qué quedó activo?

Abrí `https://TU-SITIO.netlify.app/api/whoami` en el navegador. Te dice qué keys están cargadas, sin revelarlas.

## ¿Cómo actualizo a una versión nueva?

Te paso un ZIP nuevo, lo descomprimís y lo **volvés a arrastrar**. Tu data, tu configuración inicial y tu objetivo se mantienen (viajan en la nube del dashboard).

## Preguntas frecuentes

- **¿Pago Netlify?** No para empezar: el plan gratis alcanza.
- **¿Sirve sin ninguna key?** Sí. Toda la analítica, el embudo, los objetivos, el calendario, el reporte y el Radar funcionan sin nada.
- **¿Mi data la ve alguien?** No: es tu sitio, tu almacenamiento y tus keys. Los CSV crudos y los DMs nunca salen de tu navegador.
- **La vista me satura.** Las secciones vienen **plegadas**: abrís solo lo que querés mirar y el dashboard se acuerda. Si preferís verlo todo abierto, apagá esa opción en **⚙ Configuración**.
- **Me sobran secciones en el menú.** Apagá las que no uses en **⚙ Configuración → Secciones del menú**. No se borra nada: se vuelven a prender cuando quieras.
