// Cierre de mes: el veredicto por hábito del mes que cerró.
//
// La regla es no hablar sin datos y no hablar de más: ≥95% pide subir la vara,
// <50% pide bajarla o cortar, y la banda del medio no dice nada. Un hábito con
// menos de 7 días de vida en el mes no recibe veredicto.
//
// Referencias: duo-culture/green-machine, duo-experimentation/sample-size

import { test, describe, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { store, D, fresh, markDays } from './helpers/harness.mjs';

const SEP_1 = D('2026-09-01'); // primer día del mes siguiente a agosto

/** Escenario base: agosto cerrado con cuatro hábitos de perfil distinto. */
async function agostoCerrado() {
  await fresh('2026-08-01', { name: 'Sobrado', meta: 10 });
  const s = store.getState();
  const [sobrado] = s.habits;

  const aplastado = store.addHabit('Aplastado', 25);
  const justo = store.addHabit('Justo', 20);
  const nuevo = store.addHabit('Nuevo', 20);
  aplastado.createdAt = '2026-08-01';
  justo.createdAt = '2026-08-01';
  nuevo.createdAt = '2026-08-28'; // menos de 7 días de vida en el mes

  markDays(sobrado.id, '2026-08', 1, 10);   // 10/10 = 100%
  markDays(aplastado.id, '2026-08', 1, 5);  //  5/25 =  20%
  markDays(justo.id, '2026-08', 1, 14);     // 14/20 =  70%

  return { sobrado, aplastado, justo, nuevo };
}

describe('cierre de mes', () => {
  test('marca para subir la vara al hábito que llegó al 100%', async () => {
    const { sobrado } = await agostoCerrado();
    const r = store.monthCloseReport(SEP_1);
    const item = r.flagged.find((f) => f.habit.id === sobrado.id);
    assert.equal(item.verdict, 'raise');
    assert.equal(item.pct, 100);
  });

  test('marca para bajar o cortar al hábito por debajo del 50%', async () => {
    const { aplastado } = await agostoCerrado();
    const r = store.monthCloseReport(SEP_1);
    const item = r.flagged.find((f) => f.habit.id === aplastado.id);
    assert.equal(item.verdict, 'cut');
    assert.equal(item.pct, 20);
  });

  test('la banda del medio no recibe veredicto: cero ruido', async () => {
    const { justo } = await agostoCerrado();
    const r = store.monthCloseReport(SEP_1);
    assert.ok(!r.flagged.some((f) => f.habit.id === justo.id), '70% no se comenta');
  });

  test('un hábito con menos de 7 días en el mes no recibe veredicto', async () => {
    const { nuevo } = await agostoCerrado();
    const r = store.monthCloseReport(SEP_1);
    assert.ok(!r.flagged.some((f) => f.habit.id === nuevo.id), 'sin datos suficientes');
  });

  test('apunta al mes correcto', async () => {
    await agostoCerrado();
    assert.equal(store.monthCloseReport(SEP_1).month.key, '2026-08');
  });

  test('un mes sin uso no genera cierre', async () => {
    await fresh('2026-09-01');
    assert.equal(store.monthCloseReport(SEP_1), null);
  });

  test('sin hábitos no genera cierre ni escribe estado', async () => {
    // Regresión: monthCloseReport marcaba el mes como cerrado antes de tener
    // hábitos, así que el primer cierre real nunca aparecía.
    await fresh('2026-09-01');
    store.getState().habits.length = 0;
    assert.equal(store.monthCloseReport(SEP_1), null);
    assert.equal(store.getState().ui.monthClosed, '', 'no se marca cerrado un mes que nunca se evaluó');
  });
});

describe('decisiones del cierre', () => {
  test('subir la meta la escala un 20%', async () => {
    const { sobrado } = await agostoCerrado();
    store.decideMonthClose('2026-08', sobrado.id, 'raise');
    assert.equal(store.getState().habits.find((h) => h.id === sobrado.id).meta, 12);
  });

  test('bajar la meta la reduce un 20%', async () => {
    const { aplastado } = await agostoCerrado();
    store.decideMonthClose('2026-08', aplastado.id, 'lower');
    assert.equal(store.getState().habits.find((h) => h.id === aplastado.id).meta, 20);
  });

  test('eliminar saca el hábito', async () => {
    const { aplastado } = await agostoCerrado();
    store.decideMonthClose('2026-08', aplastado.id, 'delete');
    assert.ok(!store.getState().habits.some((h) => h.id === aplastado.id));
  });

  test('mantener así deja la meta intacta y cierra el ítem', async () => {
    const { sobrado } = await agostoCerrado();
    store.decideMonthClose('2026-08', sobrado.id, 'keep');
    assert.equal(store.getState().habits.find((h) => h.id === sobrado.id).meta, 10);
    const r = store.monthCloseReport(SEP_1);
    assert.ok(!r || !r.flagged.some((f) => f.habit.id === sobrado.id));
  });

  test('decidido todo, la card desaparece y el mes queda cerrado', async () => {
    const { sobrado, aplastado } = await agostoCerrado();
    store.decideMonthClose('2026-08', sobrado.id, 'raise');
    store.decideMonthClose('2026-08', aplastado.id, 'delete');

    assert.equal(store.monthCloseReport(SEP_1), null);
    assert.equal(store.getState().ui.monthClosed, '2026-08');
    assert.equal(store.monthCloseReport(SEP_1), null, 'idempotente');
  });
});
