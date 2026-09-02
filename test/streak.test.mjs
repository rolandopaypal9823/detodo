// Racha y congelador de racha.
//
// La racha es la mecánica de retención central de Focus: si se rompe sin razón,
// el usuario abandona. El congelador la protege un día perdido a la vez, y es
// escaso a propósito. Estos tests fijan ese contrato.
//
// Referencia de diseño: .agents/skills/duo-retention/references/streak-freeze.md

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { store, D, fresh, markDays } from './helpers/harness.mjs';

describe('racha', () => {
  test('cuenta días consecutivos marcados', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 6);
    assert.equal(store.streak(D('2026-08-06')), 6);
  });

  test('hoy sin marcar no rompe la racha: el día se define hoy', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 4);
    assert.equal(store.streak(D('2026-08-05')), 4, 'la racha de ayer sigue viva hasta que termine el día');
  });

  test('cruza el borde de mes', async () => {
    const h = await fresh('2026-08-29');
    store.toggleToday(h.id, D('2026-08-30'));
    store.toggleToday(h.id, D('2026-08-31'));
    store.toggleToday(h.id, D('2026-09-01'));
    assert.equal(store.streak(D('2026-09-01')), 3);
  });

  test('un día congelado cuenta para la racha', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 3);
    store.reconcileFreezes(D('2026-08-05')); // el 4 queda congelado
    assert.equal(store.getState().freezes.used['2026-08-04'], true);
    assert.equal(store.streak(D('2026-08-05')), 4, '3 marcados + 1 congelado');
  });
});

describe('congelador: consumo', () => {
  test('cubre el día perdido y mantiene viva la racha', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 7);
    assert.equal(store.getState().freezes.available, 2, '1 inicial + 1 ganado al día 7');

    const gastó = store.reconcileFreezes(D('2026-08-09')); // el 8 sin marcar
    assert.equal(gastó, true);
    assert.equal(store.getState().freezes.used['2026-08-08'], true);
    assert.equal(store.getState().freezes.available, 1);
    assert.equal(store.streak(D('2026-08-09')), 8);
  });

  test('sin stock, la racha se corta en el segundo hueco y no gasta de más', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 5);
    store.reconcileFreezes(D('2026-08-08')); // 6 y 7 sin marcar, un solo congelador

    const f = store.getState().freezes;
    assert.equal(f.used['2026-08-06'], true, 'el primer hueco se protege');
    assert.ok(!f.used['2026-08-07'], 'el segundo no: no quedaba stock');
    assert.equal(f.available, 0);
    assert.equal(store.streak(D('2026-08-08')), 0, 'racha muerta en el segundo hueco');
  });

  test('con la racha ya muerta no se gastan más congeladores', async () => {
    const h = await fresh('2026-08-01');
    store.toggleToday(h.id, D('2026-08-01'));
    store.reconcileFreezes(D('2026-08-05')); // 2, 3 y 4 sin marcar

    const f = store.getState().freezes;
    assert.equal(f.used['2026-08-02'], true, 'el hueco contra una racha viva sí se protege');
    assert.ok(!f.used['2026-08-03'] && !f.used['2026-08-04'], 'muerta la racha, no se tira stock');
    assert.equal(f.available, 0);
  });

  test('reconciliar dos veces el mismo día no gasta doble', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 3);
    store.reconcileFreezes(D('2026-08-05'));
    const tras1 = store.getState().freezes.available;
    store.reconcileFreezes(D('2026-08-05'));
    assert.equal(store.getState().freezes.available, tras1, 'idempotente');
  });

  test('el gasto sobrevive a una recarga de la app', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 3);
    store.reconcileFreezes(D('2026-08-05'));
    await store.initStore(); // simula recargar la página
    assert.equal(store.getState().freezes.used['2026-08-04'], true);
  });

  test('el primer toggle tras días sin abrir reconcilia antes de calcular', async () => {
    // Regresión: el toggle corría antes que reconcile, así que la racha se
    // calculaba rota (streak=1) y el hito se perdía para siempre.
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 6);
    const ev = store.toggleToday(h.id, D('2026-08-08')); // el 7 quedó sin abrir

    assert.equal(store.getState().freezes.used['2026-08-07'], true, 'el toggle reconcilió solo');
    assert.equal(ev.streak, 8, 'eventos calculados con la racha ya reconciliada');
  });
});

describe('congelador: ganancia', () => {
  test('gana uno cada 7 días, con tope de 2', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 6);
    assert.equal(store.getState().freezes.available, 1, 'todavía el inicial');

    const ev = store.toggleToday(h.id, D('2026-08-07'));
    assert.equal(ev.earnedFreeze, true);
    assert.equal(store.getState().freezes.available, 2, 'tope alcanzado');
  });

  test('no gana dos veces el mismo día', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 7);
    store.toggleToday(h.id, D('2026-08-07')); // desmarca
    const ev = store.toggleToday(h.id, D('2026-08-07')); // vuelve a marcar
    assert.equal(ev.earnedFreeze, false);
    assert.equal(store.getState().freezes.available, 2);
  });
});

describe('hitos', () => {
  test('celebra el hito exacto', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 6);
    const ev = store.toggleToday(h.id, D('2026-08-07'));
    assert.equal(ev.milestone, 7);
  });

  test('celebra por CRUCE cuando un día congelado saltea el número', async () => {
    // Regresión: el guard usaba igualdad exacta (MILESTONES.includes(s)), así
    // que una racha que saltaba de 29 a 31 perdía el hito de 30 para siempre.
    const h = await fresh('2026-06-30');
    markDays(h.id, '2026-07', 1, 29);
    store.reconcileFreezes(D('2026-07-31')); // el 30 queda congelado
    assert.equal(store.getState().freezes.used['2026-07-30'], true);

    const ev = store.toggleToday(h.id, D('2026-07-31'));
    assert.equal(ev.streak, 31);
    assert.equal(ev.milestone, 30, 'el hito cruzado se celebra igual');
    assert.equal(store.getState().ui.lastMilestone, 30);
  });

  test('no repite un hito ya celebrado', async () => {
    const h = await fresh('2026-08-01');
    markDays(h.id, '2026-08', 1, 7);
    const ev = store.toggleToday(h.id, D('2026-08-08'));
    assert.equal(ev.milestone, 0, 'el 7 ya se celebró');
  });
});

describe('día perfecto', () => {
  test('solo cuando están todos los hábitos del día', async () => {
    const h1 = await fresh('2026-08-01');
    const h2 = store.addHabit('Lectura', 15);

    const primero = store.toggleToday(h1.id, D('2026-08-01'));
    assert.equal(primero.perfectDay, false, '1 de 2 no alcanza');

    const segundo = store.toggleToday(h2.id, D('2026-08-01'));
    assert.equal(segundo.perfectDay, true);
  });

  test('no se re-celebra el mismo día', async () => {
    const h = await fresh('2026-08-01');
    store.toggleToday(h.id, D('2026-08-01'));
    store.toggleToday(h.id, D('2026-08-01')); // desmarca
    const ev = store.toggleToday(h.id, D('2026-08-01')); // vuelve a marcar
    assert.equal(ev.perfectDay, false);
  });
});

describe('contadores que sobreviven a la racha', () => {
  test('bestStreak devuelve la mejor corrida histórica', async () => {
    const h = await fresh('2026-08-01');
    store.getState().freezes.available = 0; // sin congeladores: corridas puras
    for (const d of ['2026-08-01', '2026-08-02', '2026-08-03', '2026-08-10', '2026-08-11']) {
      store.toggleToday(h.id, D(d));
    }
    assert.equal(store.bestStreak(), 3);
  });

  test('bestStreak cuenta los días congelados', async () => {
    const h = await fresh('2026-08-01');
    store.getState().freezes.available = 0;
    for (const d of ['2026-08-01', '2026-08-02', '2026-08-03', '2026-08-10']) {
      store.toggleToday(h.id, D(d));
    }
    store.getState().freezes.used['2026-08-04'] = true;
    assert.equal(store.bestStreak(), 4);
  });

  test('totalActiveDays nunca se resetea', async () => {
    const h = await fresh('2026-08-01');
    store.getState().freezes.available = 0;
    for (const d of ['2026-08-01', '2026-08-02', '2026-08-03', '2026-08-10', '2026-08-11']) {
      store.toggleToday(h.id, D(d));
    }
    assert.equal(store.totalActiveDays(), 5, 'la racha se rompió, el total sigue');
  });
});
