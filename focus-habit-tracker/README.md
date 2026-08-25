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

## Publicar la página

Cualquier hosting estático sirve. Los tres típicos:

- **Vercel / Netlify**: arrastrá la carpeta `focus-habit-tracker/` o conectá el repo (root: `focus-habit-tracker`). Sin build command.
- **GitHub Pages**: serví el repo y entrá a `/focus-habit-tracker/`. Las rutas son relativas, funciona en subcarpeta.

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

- **Solo el día actual es editable** — decidido en la review: marcar en el día potencia el uso diario.
- **Recordatorio nocturno**: las notificaciones push reales necesitan app nativa (permisos del sistema). Queda para la fase app.
- **Íconos por hábito**: primero funcional; los chips visuales se agregan después.
