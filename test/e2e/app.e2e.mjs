// E2E: la app real en un navegador real.
//
// Levanta un servidor estático sobre focus-habit-tracker/ y maneja la app como
// un usuario: siembra estado en localStorage, hace clic, y verifica lo que se
// ve en pantalla. Cubre lo que los unitarios no pueden: que el render, los
// listeners y el estado estén conectados de verdad.
//
// Requiere Playwright. Si no está instalado, la suite se saltea en vez de
// fallar (`npm run test:e2e` la corre; `npm test` solo corre los unitarios).

import { test, describe, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const ROOT = new URL('../../focus-habit-tracker/', import.meta.url).pathname;
const PORT = 8477;
const BASE = `http://localhost:${PORT}`;

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.webmanifest': 'application/manifest+json',
};

let chromium = null;
try { ({ chromium } = await import('playwright-core')); } catch { /* opcional */ }
try { if (!chromium) ({ chromium } = await import('playwright')); } catch { /* opcional */ }

const CHROME = process.env.PLAYWRIGHT_CHROMIUM_PATH
  || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

let server, browser, ctx, page;
const errors = [];

const dk = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const daysAgo = (n) => { const d = new Date(); d.setDate(d.getDate() - n); return dk(d); };

/** Estado sembrado: racha de 6 días con 2 hábitos y 1 congelador en mano. */
function estadoConRacha() {
  const habits = [
    { id: 'h1', name: 'Foco profundo', meta: 24, createdAt: daysAgo(6) },
    { id: 'h2', name: 'Lectura', meta: 24, createdAt: daysAgo(6) },
  ];
  const checks = { h1: {}, h2: {} };
  for (let i = 1; i <= 6; i++) checks.h1[daysAgo(i)] = true;
  return {
    profile: { name: 'Nico' }, habits, checks, goals: [null, null, null],
    ui: { stepsDismissed: true, lastPerfect: '', lastMilestone: 0, freezeNoticeDay: '', monthClosed: '', monthCloseDecided: {} },
    freezes: { available: 1, used: {}, earnedTotal: 0, lastEarnDay: '', lastReconciled: daysAgo(1) },
  };
}

async function sembrar(estado) {
  await page.goto(BASE + '/');
  await page.evaluate((s) => localStorage.setItem('focus-nfm:v1', JSON.stringify(s)), estado);
  await page.reload();
  await page.waitForSelector('#app:not([hidden])');
}

describe('app en el navegador', { skip: chromium ? false : 'Playwright no instalado' }, () => {
  before(async () => {
    server = createServer(async (req, res) => {
      const rel = normalize(decodeURIComponent(req.url.split('?')[0])).replace(/^(\.\.[/\\])+/, '');
      const file = join(ROOT, rel === '/' ? 'index.html' : rel);
      try {
        const body = await readFile(file);
        res.writeHead(200, { 'Content-Type': MIME[extname(file)] ?? 'application/octet-stream' });
        res.end(body);
      } catch { res.writeHead(404); res.end('not found'); }
    });
    await new Promise((r) => server.listen(PORT, r));

    browser = await chromium.launch({ executablePath: CHROME });
    ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(e.message));
  });

  after(async () => {
    await browser?.close();
    await new Promise((r) => server?.close(r));
  });

  test('carga sin errores de consola', async () => {
    await sembrar(estadoConRacha());
    assert.deepEqual(errors, []);
  });

  test('muestra la racha y el congelador disponible', async () => {
    await sembrar(estadoConRacha());
    assert.equal(await page.locator('.stat-num.hot').textContent(), '6');
    assert.equal(await page.locator('.pip.full').count(), 1);
  });

  test('anticipa el hito de mañana', async () => {
    await sembrar(estadoConRacha());
    const label = await page.locator('.milestone-label').textContent();
    assert.match(label, /MAÑANA: 7/);
  });

  test('marcar el día 7 abre la celebración del hito', async () => {
    await sembrar(estadoConRacha());
    await page.locator('.today-item').first().click();
    await page.waitForSelector('#celebration:not([hidden])');
    assert.equal(await page.locator('#cel-num').textContent(), '7');
    assert.match(await page.locator('#cel-extra').textContent(), /CONGELADOR/);
  });

  test('Escape cierra la celebración', async () => {
    await sembrar(estadoConRacha());
    await page.locator('.today-item').first().click();
    await page.waitForSelector('#celebration:not([hidden])');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#celebration').isHidden(), true);
  });

  test('completar el día muestra DÍA PERFECTO sin modal', async () => {
    await sembrar(estadoConRacha());
    await page.locator('.today-item').first().click();
    await page.waitForSelector('#celebration:not([hidden])');
    await page.keyboard.press('Escape');
    await page.locator('.today-item:not(.checked)').first().click();
    await page.waitForTimeout(300);

    assert.equal(await page.locator('#celebration').isHidden(), true, 'el día perfecto no interrumpe');
    assert.match(await page.locator('.perfect-inline').textContent(), /DÍA PERFECTO/);
    assert.match(await page.locator('.racha-state').textContent(), /DÍA COMPLETO/);
  });

  test('el congelador se gasta solo y avisa', async () => {
    const s = estadoConRacha();
    s.habits = [s.habits[0]];
    s.checks = { h1: Object.fromEntries([2, 3, 4].map((i) => [daysAgo(i), true])) }; // ayer sin marcar
    s.freezes.lastReconciled = daysAgo(2);
    await sembrar(s);

    assert.match(await page.locator('.notice').first().textContent(), /congelador salvó tu racha/);
    assert.equal(await page.locator('.stat-num.hot').textContent(), '4', '3 marcados + ayer congelado');
    assert.equal(await page.locator('.pip.full').count(), 0);

    const guardado = await page.evaluate(() => JSON.parse(localStorage.getItem('focus-nfm:v1')));
    assert.equal(guardado.freezes.used[daysAgo(1)], true, 'el gasto queda persistido');
  });

  test('el día congelado se ve en la grilla del panel', async () => {
    const s = estadoConRacha();
    // el día congelado NO puede estar marcado: la celda es una cosa o la otra
    delete s.checks.h1[daysAgo(3)];
    s.freezes.used = { [daysAgo(3)]: true };
    await sembrar(s);
    await page.goto(BASE + '/#/habitos');
    await page.waitForSelector('.habit-grid');
    assert.ok(await page.locator('.cell.frozen').count() >= 1);
  });

  test('el pasado no se puede marcar, solo hoy', async () => {
    await sembrar(estadoConRacha());
    await page.goto(BASE + '/#/habitos');
    await page.waitForSelector('.habit-grid');
    const editables = await page.locator('.cell.editable').count();
    const hoy = await page.locator('.cell.today').count();
    assert.equal(editables, hoy, 'solo las celdas de hoy son botones');
  });

  test('el aviso nocturno aparece a las 21 y se va al marcar', async () => {
    const noche = new Date(); noche.setHours(21, 0, 0, 0);
    await page.clock.install({ time: noche });
    await sembrar(estadoConRacha());

    assert.match(await page.locator('.notice-hot').textContent(), /se define hoy/);
    await page.locator('.today-item').first().click();
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    assert.equal(await page.locator('.notice-hot').count(), 0);
  });
});
