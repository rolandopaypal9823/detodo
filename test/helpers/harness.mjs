// Harness de tests para store.js.
//
// store.js corre en el navegador y usa localStorage. Acá lo sustituimos por un
// objeto en memoria para poder importar el módulo tal cual, sin build ni mocks
// de terceros. El reloj se inyecta por parámetro (todas las funciones de racha
// aceptan un `now`), así que los tests son deterministas y no dependen del día
// en que se corren.

let mem = {};

globalThis.localStorage = {
  getItem: (k) => mem[k] ?? null,
  setItem: (k, v) => { mem[k] = v; },
  removeItem: (k) => { delete mem[k]; },
};

export const store = await import('../../focus-habit-tracker/js/store.js');

/** Fecha fija a mediodía: evita cualquier corrimiento por huso horario. */
export const D = (yyyymmdd) => new Date(yyyymmdd + 'T12:00:00');

/**
 * Estado limpio con un hábito y la reconciliación puesta al día.
 * `start` es el día en que el usuario "se dio de alta": nada anterior
 * a esa fecha se evalúa ni consume congeladores.
 */
export async function fresh(start, { name = 'Foco', meta = 20 } = {}) {
  mem = {};
  store.resetLocal();
  await store.initStore();
  const habit = store.addHabit(name, meta);
  habit.createdAt = start;
  store.reconcileFreezes(D(start));
  return habit;
}

/** Marca un rango de días del mismo mes (inclusive). */
export function markDays(habitId, yyyymm, from, to) {
  for (let d = from; d <= to; d++) {
    store.toggleToday(habitId, D(`${yyyymm}-${String(d).padStart(2, '0')}`));
  }
}
