/* ═══════════════════════════════════════════════════════════════
   CAPTURA HÍBRIDA
   Por cada slide:
     1. mide los bloques de texto editables (posición, estilos, runs)
     2. los oculta y saca el PNG → fondo idéntico al HTML
        (mapa, Mini Nico, mockups, todo)
   Después build-hibrido.js pone los textos encima como cuadros nativos.
   ═══════════════════════════════════════════════════════════════ */
const OUT = __dirname;
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/* Qué es texto editable en cada tipo de slide.
   Todo lo que NO esté acá queda dentro de la imagen: el mapa completo
   (sendero, discos, números, labels), los mockups y el contador. */
const EDITABLES = {
  cover:   ['.cover .kicker', '.cover h1', '.cover .sub'],
  intro:   ['.hero-slide .kicker', '.hero-slide h2', '.hero-slide .hero-foot'],
  node:    ['.node-slide .step-label', '.node-slide h2', '.node-slide .node-copy'],
  qualify: ['.qual .kicker', '.qual h2', '.qcol.yes h3', '.qcol.yes p',
            '.qcol.no h3', '.qlist li > span:last-child', '.qfoot'],
  cta:     ['.cta .kicker', '.cta h2', '.cta > div > p', '.cta-note', '.cupos'],
  close:   ['.hero-slide .kicker', '.hero-slide h2', '.hero-slide .hero-foot'],
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + '/home/user/detodo/deck-1pct/deck-mapa-1-pct.html');
  await p.waitForTimeout(2500);

  const n = await p.evaluate(() => SLIDES.length);
  const todo = [];

  for (let i = 0; i < n; i++) {
    await p.evaluate(j => { idx = j; beat = 0; render(); }, i);
    await p.waitForTimeout(1400);

    const info = await p.evaluate(({ i, EDITABLES }) => {
      const tipo = SLIDES[i].type;
      const slide = document.querySelectorAll('.slide')[i];
      const canvas = document.getElementById('canvas').getBoundingClientRect();
      const sels = EDITABLES[tipo] || [];

      // Separa el contenido en "runs" para conservar los tramos naranjas
      const runs = el => {
        const out = [];
        const walk = (nodo, naranja) => {
          for (const h of nodo.childNodes) {
            if (h.nodeType === 3) {
              const t = h.textContent;
              if (t) out.push({ text: t, naranja });
            } else if (h.nodeType === 1) {
              if (h.tagName === 'BR') { out.push({ text: '\n', naranja }); continue; }
              const c = getComputedStyle(h).color;
              const esNaranja = /255,\s*102,\s*2/.test(c);
              const bold = +getComputedStyle(h).fontWeight >= 600;
              walk(h, naranja || esNaranja || (bold ? 'bold' : false));
            }
          }
        };
        walk(el, false);
        return out;
      };

      const bloques = [];
      sels.forEach(sel => {
        slide.querySelectorAll(sel).forEach(el => {
          const r = el.getBoundingClientRect();
          if (!r.width || !r.height) return;
          const cs = getComputedStyle(el);
          bloques.push({
            sel,
            x: r.left - canvas.left, y: r.top - canvas.top,
            w: r.width, h: r.height,
            fontSize: parseFloat(cs.fontSize),
            lineHeight: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3,
            weight: +cs.fontWeight,
            color: cs.color,
            align: cs.textAlign,
            spacing: parseFloat(cs.letterSpacing) || 0,
            upper: cs.textTransform === 'uppercase',
            family: cs.fontFamily,
            runs: runs(el),
          });
        });
      });
      return { tipo, bloques };
    }, { i, EDITABLES });

    // Oculta los textos editables y saca el fondo
    await p.evaluate(({ i, sels }) => {
      const slide = document.querySelectorAll('.slide')[i];
      window.__ocultos = [];
      sels.forEach(s => slide.querySelectorAll(s).forEach(el => {
        window.__ocultos.push(el);
        el.style.visibility = 'hidden';
      }));
    }, { i, sels: EDITABLES[info.tipo] || [] });
    await p.waitForTimeout(250);

    await (await p.$('#canvas')).screenshot({ path: `${OUT}/bg${String(i + 1).padStart(2, '0')}.png` });

    await p.evaluate(() => (window.__ocultos || []).forEach(el => (el.style.visibility = '')));

    // Notas del presentador
    const nota = await p.evaluate(j => {
      const x = notesFor(SLIDES[j]);
      return { titulo: x.titulo || '', notes: x.notes || [], cue: x.cue || '' };
    }, i);

    todo.push({ ...info, nota });
    process.stdout.write(`${i + 1}(${info.bloques.length}) `);
  }

  fs.writeFileSync(`${OUT}/textos.json`, JSON.stringify(todo, null, 1));
  await b.close();
  console.log(`\n${n} fondos + ${todo.reduce((a, s) => a + s.bloques.length, 0)} bloques de texto`);
})();
