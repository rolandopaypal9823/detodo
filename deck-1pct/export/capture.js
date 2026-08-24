/* Captura los 11 slides del deck a PNG (2x) y extrae las notas del presentador.
   Uso:  cd deck-1pct/export && npm i playwright && node capture.js   */
const OUT = __dirname;
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + require('path').resolve(OUT, '..', 'deck-mapa-1-pct.html'));
  await p.waitForTimeout(2500);

  const n = await p.evaluate(() => SLIDES.length);
  for (let i = 0; i < n; i++) {
    await p.evaluate(j => { idx = j; beat = 0; render(); }, i);
    await p.waitForTimeout(1400);            // esperar transiciones del mapa
    await (await p.$('#canvas')).screenshot({ path: `${OUT}/s${String(i + 1).padStart(2, '0')}.png` });
    process.stdout.write(`${i + 1} `);
  }

  const meta = await p.evaluate(() => SLIDES.map(s => {
    const x = notesFor(s);
    return { type: s.type, titulo: x.titulo || '', notes: x.notes || [], cue: x.cue || '' };
  }));
  fs.writeFileSync(`${OUT}/meta.json`, JSON.stringify(meta, null, 1));
  await b.close();
  console.log(`\n${n} slides + meta.json`);
})();
