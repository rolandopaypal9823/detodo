// ============================================================
// Configuración de Supabase (cuentas + sincronización)
//
// 1. Creá un proyecto gratis en https://supabase.com
// 2. Corré supabase/schema.sql en el SQL Editor del proyecto
// 3. Pegá acá la URL y la anon key (Settings → API)
//
// Si quedan vacíos, la app funciona igual en MODO LOCAL:
// el progreso se guarda en el dispositivo (localStorage).
// ============================================================

export const SUPABASE_URL = '';
export const SUPABASE_ANON_KEY = '';

export const supabaseEnabled = () =>
  Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);
