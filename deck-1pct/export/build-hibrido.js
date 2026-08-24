/* ═══════════════════════════════════════════════════════════════
   PPTX HÍBRIDO
   Fondo = el render real del HTML (mapa, Mini Nico, mockups) como
   imagen a 2x, con los textos borrados.
   Encima = solo los textos, como cuadros nativos editables, en las
   coordenadas exactas medidas del navegador.
   ═══════════════════════════════════════════════════════════════ */
const D = __dirname;
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const slides = JSON.parse(fs.readFileSync(`${D}/textos.json`, 'utf8'));

const ORANGE = 'FF6602';
const PX = 13.333 / 1920;             // px del canvas → pulgadas
const inch = px => +(px * PX).toFixed(3);
const pt = px => +(px * 0.5).toFixed(1);  // 1920px = 960pt  ⇒  1px = 0,5pt

/* "rgb(12, 52, 82)" → "0C3452" */
const hex = rgb => {
  const m = String(rgb).match(/(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (!m) return '000000';
  return [1, 2, 3].map(i => (+m[i]).toString(16).padStart(2, '0')).join('').toUpperCase();
};

/* La fuente que declara el CSS, mapeada a la que PowerPoint espera */
const face = fam => {
  const f = String(fam).toLowerCase();
  if (f.includes('montserrat')) return 'Montserrat';
  if (f.includes('jetbrains') || f.includes('mono')) return 'Consolas';
  return 'Open Sans';
};

const alinear = a => (a === 'center' ? 'center' : a === 'right' ? 'right' : 'left');

const pres = new pptxgen();
pres.defineLayout({ name: 'NFM', width: 13.333, height: 7.5 });
pres.layout = 'NFM';
pres.author  = 'Instituto NFM';
pres.company = 'Instituto de Productividad';
pres.title   = 'El mapa del 1%';

slides.forEach((sl, i) => {
  const s = pres.addSlide();

  // 1 · El fondo, tal cual sale del HTML
  s.addImage({
    path: `${D}/bg${String(i + 1).padStart(2, '0')}.png`,
    x: 0, y: 0, w: 13.333, h: 7.5,
  });

  // 2 · Los textos, editables, encima
  sl.bloques.forEach(b => {
    const base = hex(b.color);

    const runs = b.runs
      .filter(r => r.text !== '')
      .map(r => ({
        text: b.upper ? r.text.toUpperCase() : r.text,
        options: {
          color: r.naranja === true ? ORANGE : base,
          bold: b.weight >= 600 || r.naranja === 'bold' || r.naranja === true,
        },
      }));
    if (!runs.length) return;

    s.addText(runs, {
      x: inch(b.x), y: inch(b.y),
      w: inch(b.w + 8),        // 8px de aire: si alargan el texto no se corta
      h: inch(b.h + 6),
      fontFace: face(b.family),
      fontSize: pt(b.fontSize),
      color: base,
      bold: b.weight >= 600,
      align: alinear(b.align),
      lineSpacing: pt(b.lineHeight),
      charSpacing: b.spacing ? +(b.spacing * 0.5).toFixed(1) : 0,
      valign: 'top',
      margin: 0,
      isTextBox: true,
    });
  });

  // 3 · Notas del presentador
  const n = sl.nota;
  const limpio = t => String(t).replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
  const partes = [`${String(i + 1).padStart(2, '0')} / ${slides.length} · ${limpio(n.titulo)}`];
  if (n.notes.length) partes.push(n.notes.map(t => '• ' + limpio(t)).join('\n\n'));
  if (n.cue) partes.push('CÓMO DECIRLO\n' + limpio(n.cue));
  s.addNotes(partes.join('\n\n'));
});

pres.writeFile({ fileName: `${D}/El-mapa-del-1-pct-EDITABLE.pptx` })
  .then(f => console.log('escrito:', f));
