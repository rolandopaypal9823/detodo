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
  ui: { stepsDismissed: false },
});

let state = defaultState();
let supabase = null;     // cliente supabase-js (solo si está configurado)
let user = null;         // usuario autenticado (o null en modo local)
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
    if (raw) state = { ...defaultState(), ...JSON.parse(raw) };
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
}

async function pullRemote() {
  const { data, error } = await supabase
    .from('user_data').select('data').eq('user_id', user.id).maybeSingle();
  if (error) throw error;
  if (data?.data) {
    state = { ...defaultState(), ...data.data };
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
      if (JSON.stringify(state) === before && hadLocal) await pushRemote();
    } catch (e) { console.warn('Sync inicial falló, seguimos con lo local', e); }
  }
  emit();
}

export function save() {
  saveLocal();
  emit();
  if (user) {
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
export function toggleToday(habitId) {
  const key = todayKey();
  const map = state.checks[habitId] ?? (state.checks[habitId] = {});
  if (map[key]) delete map[key];
  else map[key] = true;
  save();
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

// Racha: días consecutivos (terminando hoy o ayer) con al menos un hábito marcado.
export function streak() {
  if (!state.habits.length) return 0;
  const dayDone = (key) => state.habits.some((h) => isChecked(h.id, key));
  let count = 0;
  const cursor = new Date();
  if (!dayDone(dateKey(cursor))) cursor.setDate(cursor.getDate() - 1); // hoy todavía no marcaste: la racha de ayer sigue viva
  while (dayDone(dateKey(cursor))) {
    count += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return count;
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
