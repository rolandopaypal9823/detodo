// ============================================================
// store.js — estado + persistencia
// Modo local: localStorage. Modo cuenta: Supabase (tabla user_data).
// La app siempre trabaja contra el estado en memoria; cada save()
// persiste local al instante y sincroniza remoto con debounce.
// ============================================================

import { SUPABASE_URL, SUPABASE_ANON_KEY, supabaseEnabled } from './config.js';

const LS_KEY = 'focus-nfm:v1';

const defaultState = () => ({
  profile: { name: '' },
  habits: [],            // [{id, name, meta, createdAt}]
  checks: {},            // {habitId: {'YYYY-MM-DD': true}}
  goals: [null, null, null], // hasta 3 metas
  ui: { stepsDismissed: false, lastPerfect: '', lastMilestone: 0, freezeNoticeDay: '', monthClosed: '', monthCloseDecided: {} },
  // Congelador de racha (skills/duo-retention/references/streak-freeze.md):
  // escaso a propósito — arrancás con 1, ganás 1 cada 7 días de racha, máximo 2.
  // Se gasta solo, un día perdido a la vez, y únicamente si la racha estaba viva.
  freezes: { available: 1, used: {}, earnedTotal: 0, lastEarnDay: '', lastReconciled: '' },
});

let state = defaultState();

// migración suave: estados guardados antes de que existieran freezes/ui nuevos
function mergeState(saved) {
  const base = defaultState();
  return {
    ...base,
    ...saved,
    ui: { ...base.ui, ...(saved.ui || {}) },
    freezes: { ...base.freezes, ...(saved.freezes || {}) },
  };
}
let supabase = null;     // cliente supabase-js (solo si está configurado)
let user = null;         // usuario autenticado (o null en modo local)
let remoteReady = false; // true solo tras un pull exitoso: sin esto NO se pushea
                         // (evita pisar lo remoto con estado local viejo si el pull falló)
let syncTimer = null;
let listeners = [];

// ---------- helpers ----------

export const uid = () => Math.random().toString(36).slice(2, 9) + Date.now().toString(36);

export function getState() { return state; }
export function getUser() { return user; }
export function isRemote() { return Boolean(user); }

export function onChange(fn) { listeners.push(fn); }
function emit() { listeners.forEach((fn) => fn(state)); }

// ---------- persistencia local ----------

function loadLocal() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) state = mergeState(JSON.parse(raw));
  } catch { /* storage bloqueado o corrupto: seguimos en memoria */ }
}

function saveLocal() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(state)); } catch { /* sin storage */ }
}

// ---------- persistencia remota (Supabase) ----------

export async function initSupabase() {
  if (!supabaseEnabled()) return null;
  const { createClient } = await import(
    'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'
  );
  supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  const { data } = await supabase.auth.getSession();
  user = data?.session?.user ?? null;
  return user;
}

export async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  user = data.user;
}

export async function signUp(email, password) {
  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) throw error;
  // con "confirm email" desactivado ya hay sesión; si no, avisamos
  user = data.session?.user ?? null;
  return Boolean(user);
}

export async function signOut() {
  if (supabase) await supabase.auth.signOut();
  user = null;
  remoteReady = false;
}

async function pullRemote() {
  const { data, error } = await supabase
    .from('user_data').select('data').eq('user_id', user.id).maybeSingle();
  if (error) throw error;
  if (data?.data) {
    state = mergeState(data.data);
  }
}

async function pushRemote() {
  if (!supabase || !user) return;
  await supabase.from('user_data').upsert({
    user_id: user.id,
    data: state,
    updated_at: new Date().toISOString(),
  });
}

// ---------- API de datos ----------

export async function initStore() {
  loadLocal();
  if (user) {
    // al entrar con cuenta: lo remoto manda; si no hay nada remoto,
    // subimos lo local (migración transparente del modo local a la cuenta)
    try {
      const hadLocal = state.habits.length > 0 || state.goals.some(Boolean);
      const before = JSON.stringify(state);
      await pullRemote();
      remoteReady = true; // el pull anduvo: recién ahora se permite pushear
      if (JSON.stringify(state) === before && hadLocal) await pushRemote();
    } catch (e) { console.warn('Sync inicial falló: seguimos con lo local y NO pisamos lo remoto', e); }
  }
  // reconciliar SIEMPRE sobre el estado final (local o ya sincronizado)
  if (state.habits.length) reconcileFreezes();
  emit();
}

export function save() {
  saveLocal();
  emit();
  if (user && remoteReady) {
    clearTimeout(syncTimer);
    syncTimer = setTimeout(() => pushRemote().catch((e) => console.warn('Sync falló', e)), 800);
  }
}

export function resetLocal() {
  state = defaultState();
  try { localStorage.removeItem(LS_KEY); } catch { /* sin storage */ }
}

// ---------- fechas ----------

export const dateKey = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

export const todayKey = () => dateKey(new Date());

export function addDays(key, n) {
  const d = new Date(key + 'T12:00:00');
  d.setDate(d.getDate() + n);
  return dateKey(d);
}

// ---------- hábitos ----------

export function addHabit(name, meta) {
  const habit = { id: uid(), name: name.trim(), meta, createdAt: todayKey() };
  state.habits.push(habit);
  save();
  return habit;
}

export function updateHabit(id, name, meta) {
  const h = state.habits.find((x) => x.id === id);
  if (!h) return;
  h.name = name.trim();
  h.meta = meta;
  save();
}

export function deleteHabit(id) {
  state.habits = state.habits.filter((x) => x.id !== id);
  delete state.checks[id];
  save();
}

// Regla del MVP: solo se puede marcar el día actual.
// Marcar en el día potencia el uso diario; el pasado no se edita.
export function toggleToday(habitId, now = new Date()) {
  // reconciliar primero: si venís de días sin abrir (PWA que despierta,
  // pestaña que cruzó medianoche), la racha y los congeladores tienen que
  // estar al día antes de calcular hitos/ganancias. Idempotente y barato.
  reconcileFreezes(now);
  const key = dateKey(now);
  const map = state.checks[habitId] ?? (state.checks[habitId] = {});
  const turnedOn = !map[key];
  if (turnedOn) map[key] = true;
  else delete map[key];

  // eventos de celebración — solo al marcar (nunca al desmarcar)
  const events = { turnedOn, earnedFreeze: false, milestone: 0, perfectDay: false, streak: 0 };
  if (turnedOn) {
    events.earnedFreeze = maybeEarnFreeze(now);
    const s = streak(now);
    events.streak = s;
    // hito nuevo: celebración grande, una sola vez por hito.
    // Detecta el CRUCE (lastMilestone < m <= s), no la igualdad exacta:
    // un día congelado puede hacer saltar la racha por encima del número.
    const crossed = MILESTONES.filter((m) => state.ui.lastMilestone < m && m <= s);
    if (crossed.length) {
      const top = crossed[crossed.length - 1];
      state.ui.lastMilestone = top;
      events.milestone = top;
    }
    // día perfecto: todos los hábitos de hoy, una sola vez por día
    const all = state.habits.length > 0 && state.habits.every((h) => isChecked(h.id, key));
    if (all && state.ui.lastPerfect !== key) {
      state.ui.lastPerfect = key;
      events.perfectDay = true;
    }
  }
  save();
  return events;
}

export const isChecked = (habitId, key) => Boolean(state.checks[habitId]?.[key]);

// ---------- métricas ----------

export function monthKeys(year, month /* 0-11 */) {
  const days = new Date(year, month + 1, 0).getDate();
  return Array.from({ length: days }, (_, i) =>
    `${year}-${String(month + 1).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`);
}

export function monthStats(year, month) {
  const keys = monthKeys(year, month);
  const perHabit = state.habits.map((h) => {
    const done = keys.filter((k) => isChecked(h.id, k)).length;
    return { habit: h, done, meta: h.meta, pct: h.meta ? Math.round((done / h.meta) * 100) : 0 };
  });
  const done = perHabit.reduce((a, x) => a + x.done, 0);
  const target = perHabit.reduce((a, x) => a + x.meta, 0);
  return {
    perHabit,
    done,
    target,
    remaining: Math.max(0, target - done),
    pct: target ? Math.round((done / target) * 100) : 0,
    days: keys.length,
  };
}

// Un día está "vivo" si marcaste al menos un hábito o si un congelador lo cubrió.
export const dayAlive = (key) =>
  state.habits.some((h) => isChecked(h.id, key)) || Boolean(state.freezes.used[key]);

const anyCheckOn = (key) => state.habits.some((h) => isChecked(h.id, key));

// Racha: días consecutivos vivos, terminando hoy o ayer
// (si hoy todavía no marcaste, la racha de ayer sigue viva: hoy se define hoy).
export function streak(now = new Date()) {
  if (!state.habits.length) return 0;
  let cursor = dateKey(now);
  if (!dayAlive(cursor)) cursor = addDays(cursor, -1);
  let count = 0;
  while (dayAlive(cursor)) {
    count += 1;
    cursor = addDays(cursor, -1);
  }
  return count;
}

// ---------- congelador de racha ----------
// skills/duo-retention/references/streak-freeze.md — el freeze se auto-aplica
// al día perdido, preserva la loss aversion y elimina el churn por culpa.
// Reglas: cubre solo días PASADOS (hoy siempre se marca a mano), solo si la
// racha venía viva hasta el día anterior, y nunca gasta de más: si se acaban
// los congeladores, la racha se corta ahí y no se sigue gastando.
export function reconcileFreezes(now = new Date()) {
  const yesterday = addDays(dateKey(now), -1);
  const f = state.freezes;
  if (!f.lastReconciled) {
    // primer arranque: nada anterior al alta se evalúa ni gasta congeladores
    f.lastReconciled = yesterday;
    save();
    return false;
  }
  if (f.lastReconciled >= yesterday) return false; // ya está al día

  let spent = false;
  let cursor = addDays(f.lastReconciled, 1);
  while (cursor <= yesterday) {
    if (!dayAlive(cursor)) {
      const prevAlive = dayAlive(addDays(cursor, -1));
      if (prevAlive && f.available > 0) {
        f.available -= 1;
        f.used[cursor] = true;      // el congelador absorbe el día perdido
        state.ui.freezeNoticeDay = dateKey(now); // avisarle hoy que se salvó
        spent = true;
      }
      // sin congelador o racha ya muerta: el día queda roto y no se gasta
    }
    cursor = addDays(cursor, 1);
  }
  f.lastReconciled = yesterday;
  save();
  return spent;
}

// Mejor racha histórica (anti-culpa: cuando la racha muere, el dato como
// registro, no como reproche — duo-gamification/anti-grind).
export function bestStreak() {
  const alive = new Set();
  for (const h of state.habits) for (const k of Object.keys(state.checks[h.id] ?? {})) alive.add(k);
  for (const k of Object.keys(state.freezes.used)) alive.add(k);
  if (!alive.size) return 0;
  const days = [...alive].sort();
  let best = 1, run = 1;
  for (let i = 1; i < days.length; i++) {
    run = days[i] === addDays(days[i - 1], 1) ? run + 1 : 1;
    if (run > best) best = run;
  }
  return best;
}

// Constancia total: días con al menos una marca desde el primer uso.
// Nunca se resetea — el ancla que sobrevive a cualquier racha rota
// (duo-retention/forever-product).
export function totalActiveDays() {
  const days = new Set();
  for (const h of state.habits) for (const k of Object.keys(state.checks[h.id] ?? {})) days.add(k);
  return days.size;
}

// ---------- cierre de mes (duo-culture/green-machine + kill-criteria) ----------
// El día 1 de cada mes: veredicto por hábito del mes cerrado.
// ≥95% → subí la vara · <50% → bajala o eliminá · 50-95% → sin comentario.
export function prevMonthOf(now = new Date()) {
  const d = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  return { y: d.getFullYear(), m: d.getMonth(), key: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}` };
}

export function monthCloseReport(now = new Date()) {
  if (!state.habits.length) return null; // sin hábitos no hay nada que cerrar (y no se escribe estado)
  const prev = prevMonthOf(now);
  if (state.ui.monthClosed === prev.key) return null; // ya decidido
  const keys = monthKeys(prev.y, prev.m);
  const monthEnd = keys[keys.length - 1];
  const decided = state.ui.monthCloseDecided?.[prev.key] ?? {};
  const flagged = [];
  let hadData = false;
  for (const h of state.habits) {
    const done = keys.filter((k) => isChecked(h.id, k)).length;
    if (done > 0) hadData = true;
    if (decided[h.id]) continue;
    // piso de datos: el hábito tiene que haber existido ≥7 días del mes
    // (duo-experimentation/sample-size: sin datos suficientes, sin veredicto)
    const born = h.createdAt || keys[0];
    const daysAlive = keys.filter((k) => k >= born && k <= monthEnd).length;
    if (daysAlive < 7) continue;
    const pct = h.meta ? Math.round((done / h.meta) * 100) : 0;
    if (pct >= 95) flagged.push({ habit: h, done, pct, verdict: 'raise' });
    else if (pct < 50) flagged.push({ habit: h, done, pct, verdict: 'cut' });
  }
  if (!hadData) { state.ui.monthClosed = prev.key; save(); return null; } // mes sin uso: nada que cerrar
  if (!flagged.length) { state.ui.monthClosed = prev.key; save(); return null; } // banda media: cero ruido
  return { month: prev, flagged };
}

export function decideMonthClose(monthKey, habitId, action) {
  const h = state.habits.find((x) => x.id === habitId);
  if (h) {
    if (action === 'raise') h.meta = Math.min(31, Math.round(h.meta * 1.2) || h.meta + 2);
    if (action === 'lower') h.meta = Math.max(1, Math.round(h.meta * 0.8));
    if (action === 'delete') { deleteHabit(habitId); }
  }
  const dec = state.ui.monthCloseDecided ?? (state.ui.monthCloseDecided = {});
  (dec[monthKey] ?? (dec[monthKey] = {}))[habitId] = true;
  save();
}

// Hitos de racha (skills/duo-gamification/references/celebration-moments.md:
// tratamiento distinto en 7, 30, 50, 100, 365).
export const MILESTONES = [7, 30, 50, 100, 365];

export function nextMilestone(s = streak()) {
  return MILESTONES.find((m) => m > s) ?? null;
}

export function prevMilestone(s = streak()) {
  const past = MILESTONES.filter((m) => m <= s);
  return past.length ? past[past.length - 1] : 0;
}

// Ganás 1 congelador cada 7 días de racha (máx. 2 en mano — la escasez
// mantiene vivo el incentivo diario, dice el nodo).
function maybeEarnFreeze(now) {
  const f = state.freezes;
  const s = streak(now);
  const today = dateKey(now);
  if (s > 0 && s % 7 === 0 && f.lastEarnDay !== today && f.available < 2) {
    f.available += 1;
    f.earnedTotal += 1;
    f.lastEarnDay = today;
    return true;
  }
  return false;
}

export function todayProgress() {
  const key = todayKey();
  const total = state.habits.length;
  const done = state.habits.filter((h) => isChecked(h.id, key)).length;
  return { done, total, pct: total ? Math.round((done / total) * 100) : 0 };
}

// ---------- objetivos ----------

export function setGoalField(index, field, value) {
  const goal = state.goals[index] ?? (state.goals[index] = {});
  goal[field] = value;
  save();
}

// ---------- perfil / ui ----------

export function setName(name) { state.profile.name = name.trim(); save(); }
export function dismissSteps() { state.ui.stepsDismissed = true; save(); }
