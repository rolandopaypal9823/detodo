// Genera los titulos de Vturb como PNG con fondo transparente.
// Uso: node .claude/render_titulos_png.js   (lee .claude/titulos.json, escribe vturb-titulos/png/)
const {chromium} = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const RAIZ = path.join(__dirname, '..'), FUENTES = path.join(__dirname, 'fuentes');
const {ante, titulos} = JSON.parse(fs.readFileSync(path.join(__dirname, 'titulos.json'), 'utf8'));
const f64 = n => fs.readFileSync(path.join(FUENTES, n)).toString('base64');
const FACE = `
@font-face{font-family:M;font-weight:900;src:url(data:font/woff2;base64,${f64('montserrat-latin-900-normal.woff2')}) format('woff2');unicode-range:U+0000-00FF,U+2018-201F}
@font-face{font-family:M;font-weight:900;src:url(data:font/woff2;base64,${f64('montserrat-latin-ext-900-normal.woff2')}) format('woff2');unicode-range:U+0100-024F}
@font-face{font-family:J;font-weight:500;src:url(data:font/woff2;base64,${f64('jetbrains-mono-latin-500-normal.woff2')}) format('woff2')}
@font-face{font-family:O;font-weight:400;src:url(data:font/woff2;base64,${f64('open-sans-latin-400-normal.woff2')}) format('woff2')}`;

// celular: pensado para verse a ~340px de ancho (letra del titulo ~19px en pantalla)
// En computadora se muestra con un tope de ancho (ver el HTML de Vturb en vturb-titulos.txt).
const FORMATOS = {
  celular: {w: 1080, k: 38, t: 64, b: 46, pad: 20},
};
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  for (const [fmt, m] of Object.entries(FORMATOS)) {
    const dir = path.join(RAIZ, 'vturb-titulos', 'png', fmt); fs.mkdirSync(dir, {recursive: true});
    const ctx = await b.newContext({viewport: {width: m.w, height: 1400}, deviceScaleFactor: 1});
    const p = await ctx.newPage();
    for (let i = 0; i < titulos.length; i++) {
      const t = titulos[i];
      await p.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${FACE}
        html,body{margin:0;background:transparent}
        .tit{box-sizing:border-box;width:${m.w}px;padding:${m.pad}px ${m.pad * 2}px ${m.pad}px;text-align:center;color:#0c3452}
        .k{font:500 ${m.k}px/1.3 J,monospace;letter-spacing:.1em;text-transform:uppercase;color:#c04a00;margin:0 0 ${Math.round(m.k * .55)}px}
        .t{font:900 ${m.t}px/1.14 M,sans-serif;letter-spacing:-.012em;margin:0;text-wrap:balance}
        .t span{color:#ff6602}
        .b{font:400 ${m.b}px/1.4 O,sans-serif;color:#33536b;margin:${Math.round(m.b * .45)}px auto 0;max-width:30em;text-wrap:balance}
      </style></head><body><div class="tit"><p class="k">${ante}</p><h1 class="t">${t.titulo}</h1>${t.bajada ? `<p class="b">${t.bajada}</p>` : ''}</div></body></html>`);
      await p.evaluate(() => document.fonts.ready);
      await p.waitForTimeout(150);
      const est = await p.evaluate(() => [...document.fonts].map(f => f.family + ' ' + f.weight + ' ' + f.status));
      const ok = est.filter(x => x.endsWith('loaded')).length >= (t.bajada ? 4 : 3);
      if (!ok) console.log(est);
      if (!ok) throw new Error('no cargaron las fuentes');
      const archivo = path.join(dir, `titulo-${i + 1}.png`);
      // mismo ancho en las cinco (asi el titulo sale del mismo tamaño en todas); recorte solo arriba y abajo
      const box = await p.evaluate(pad => { const r = document.createRange(); let x0=1e9,y0=1e9,x1=0,y1=0;
        for (const el of document.querySelectorAll('.k,.t,.b')) { r.selectNodeContents(el);
          for (const q of r.getClientRects()) { x0=Math.min(x0,q.left); y0=Math.min(y0,q.top); x1=Math.max(x1,q.right); y1=Math.max(y1,q.bottom); } }
        return {x: 0, y: Math.floor(y0 - pad/2), width: document.querySelector(".tit").offsetWidth, height: Math.ceil(y1 - y0 + pad)}; }, 16);
      await p.screenshot({path: archivo, omitBackground: true, clip: box});
      console.log(`${fmt}/titulo-${i + 1}.png  ${Math.round(box.width)}x${Math.round(box.height)}  ${Math.round(fs.statSync(archivo).size / 1024)} KB`);
    }
    await ctx.close();
  }
  await b.close(); process.exit(0);
})();
