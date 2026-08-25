# FOCUS — Habit Tracker · Instituto NFM

Web app de hábitos y objetivos con la identidad NFM: azul que ordena (`#0c3452`), naranja que acciona (`#ff6602`). Todo señal, cero ruido.

**Funciona sin instalar nada:** es HTML/CSS/JS puro, sin build. Se abre, se usa.

## Qué hace (MVP)

- **Inicio** — saludo, "Tus primeros pasos" (checklist funcional que se marca solo), racha de días, y los hábitos de hoy para marcar con un toque.
- **Panel de hábitos** — grilla mensual (hábitos × días), anillo de progreso, completados/restantes, ranking de mejores hábitos del mes.
  - Regla del sistema: **solo se marca el día en el que estás.** El pasado no se edita. Eso te empuja a usarlo todos los días.
- **Gestionar hábitos** — crear, editar y eliminar, con meta mensual (cuántos días del mes querés cumplirlo) y sugeridos del método NFM.
- **Objetivos y metas** — hasta 3 metas concretas con los campos del método (qué + para cuándo, para qué, horas de foco; opcionales para profundizar). Guardado automático.
- **PWA** — instalable como ícono en el celular (ver abajo). Abre al instante gracias al service worker.

## Sistema de racha (mecánicas Duolingo, estética NFM)

Basado en las skills del playbook de Duolingo (`.agents/skills/duo-*`), traducido al producto:

- **Racha** — días consecutivos con al menos un hábito marcado. Si hoy todavía no marcaste, la racha de ayer sigue viva: hoy se define hoy. (`duo-retention/streak-mechanics`)
- **Congelador de racha ◆** — si te salteás un día, un congelador se usa solo y la racha sigue. Arrancás con 1, ganás 1 cada 7 días de racha, máximo 2 en mano. Es escaso a propósito: protege la racha sin diluir el incentivo diario. Los días congelados se ven con ◆ en la grilla. (`duo-retention/streak-freeze`)
- **Hitos** — 7 · 30 · 50 · 100 · 365 días, cada uno con su celebración y su copy. La card de racha muestra siempre el próximo hito y cuánto falta (la anticipación es parte de la celebración). (`duo-gamification/celebration-moments`)
- **Día perfecto** — completar todos los hábitos del día dispara la celebración media, una sola vez por día.
- **Feedback chico** — cada check tiene su micro-animación (260 ms, curva con rebote). Se apaga con `prefers-reduced-motion`. (`duo-design/juicy-motion`)
- **La racha se define hoy** — de noche (19+), si no marcaste nada, Inicio te lo dice en una línea. Sin push, sin spam: una sola señal, adentro de la app. (`duo-retention/notification-discipline`, loss-framing de `loss-aversion`)
- **Estados de la card de racha** — la card habla según el momento: "N días en juego · hoy: 0 marcados" (pérdida), "✓ Día asegurado" (primer check), "Día completo · X/X". Siempre el dato, nunca el carácter. (`duo-culture/candor-what-not-who`)
- **Reset anti-culpa** — cuando la racha muere, la card muestra tu mejor racha histórica y "hoy arranca la nueva". Sin rojo, sin drama. La **constancia total** (días con ≥1 marca, nunca se resetea) vive en el Panel. (`duo-retention/forever-product`)
- **Cierre de mes** — el día 1, el Panel te da el veredicto del mes cerrado por hábito: ≥95% → "subí la vara" (a un tap), <50% → "bajala o eliminá". Banda media: silencio. Hábitos con <7 días de datos no reciben veredicto. (`duo-culture/green-machine`, `duo-experimentation/sample-size`)
- **Voz centralizada** — todas las strings visibles viven en `js/copy.js` con el brief de voz (clínico + confrontativo) para auditarlas en una pasada. (`duo-voice/wholesome-unhinged` traducido a NFM)

## Modos de guardado

| Modo | Qué necesita | Dónde guarda |
|---|---|---|
| **Local** (por defecto) | Nada | En el dispositivo (localStorage) |
| **Cuenta** (login) | Configurar Supabase | En la nube, sincronizado entre dispositivos |

### Activar cuentas (Supabase, gratis)

1. Creá un proyecto en [supabase.com](https://supabase.com) (plan free alcanza).
2. En el **SQL Editor**, pegá y corré `supabase/schema.sql` (crea la tabla `user_data` con Row Level Security: cada usuario solo ve lo suyo).
3. En **Settings → API**, copiá la `URL` y la `anon public key`.
4. Pegalas en `js/config.js`:
   ```js
   export const SUPABASE_URL = 'https://xxxx.supabase.co';
   export const SUPABASE_ANON_KEY = 'eyJ...';
   ```
5. Listo: la app pasa a pedir login (email + contraseña). Si alguien venía usando modo local en ese dispositivo, su progreso se migra solo a la cuenta al entrar.

> Tip: en Supabase → Authentication → Providers → Email, podés desactivar "Confirm email" para que crear cuenta entre directo, sin paso de confirmación.

## Publicar en Netlify (recomendado)

El repo ya trae `netlify.toml` en la raíz (publica `focus-habit-tracker/`, sin build, con el header correcto para el service worker). Dos caminos:

**A. Conectado al repo (deploy automático en cada push):**
1. [app.netlify.com](https://app.netlify.com) → **Add new project** → **Importar from Git** → GitHub → elegí este repo.
2. Branch to deploy: la rama donde está la app. El resto lo toma del `netlify.toml` — no toques build command ni publish directory.
3. **Deploy**. Netlify te da una URL `https://<nombre>.netlify.app` con HTTPS.

**B. Manual (sin conectar Git):**
[app.netlify.com/drop](https://app.netlify.com/drop) → arrastrá la carpeta `focus-habit-tracker/`. Listo, pero cada actualización la subís a mano.

Después del primer deploy:
- **Site configuration → Domain management** para cambiar el nombre (`focus-nfm.netlify.app`) o colgar un dominio propio.
- Si activaste Supabase: en Supabase → **Authentication → URL Configuration**, poné la URL de Netlify como *Site URL* (para que los mails de confirmación redirijan bien).

Otras opciones: Vercel (mismos valores) o GitHub Pages (`/focus-habit-tracker/` — las rutas son relativas, funciona en subcarpeta).

Para probar local:

```bash
cd focus-habit-tracker
python3 -m http.server 8080
# abrir http://localhost:8080
```

## Atajo en el celular (app web)

- **iPhone (Safari)**: abrir la página → botón Compartir → **Agregar a inicio**.
- **Android (Chrome)**: abrir la página → menú ⋮ → **Agregar a pantalla principal** (o el aviso "Instalar app").

Queda con ícono propio y pantalla completa, como una app.

## Estructura

```
focus-habit-tracker/
├── index.html            shell de la app (SPA por hash)
├── css/styles.css        sistema de diseño NFM
├── js/
│   ├── app.js            router + vistas + interacción
│   ├── store.js          estado, métricas y persistencia (local + Supabase)
│   └── config.js         credenciales de Supabase (vacío = modo local)
├── supabase/schema.sql   tabla + políticas RLS
├── manifest.webmanifest  PWA
├── sw.js                 service worker (cache del shell)
└── assets/               íconos
```

## Decisiones del MVP (y qué viene después)

- **Solo el día actual es editable** — decidido en la review: marcar en el día potencia el uso diario. El congelador es la única excepción, y es automática.
- **Recordatorio nocturno**: push real necesita app nativa; por ahora, la línea "tu racha se define hoy" adentro de la app (19+ hs).
- **Íconos por hábito**: primero funcional; los chips visuales se agregan después.
- **Sin XP, sin ligas, sin corazones**: con un solo usuario y cero social, serían ruido. La progresión ya está en las metas mensuales y la racha (`duo-gamification/anti-grind`).
- **Sin recompensa variable ni "quests" diarias**: la sorpresa por la sorpresa es timba, y una cuota diaria convierte ganas en obligación. Un solo momento de confrontación con datos: el cierre de mes.
- **Regla dura**: el pasado no se edita, y no existe perdón de racha más blando que el congelador.
