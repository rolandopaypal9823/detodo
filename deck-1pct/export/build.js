const D = __dirname;
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const meta = JSON.parse(fs.readFileSync(`${D}/meta.json`, 'utf8'));
const strip = s => String(s).replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');

const pres = new pptxgen();
pres.defineLayout({ name: 'NFM', width: 13.333, height: 7.5 });
pres.layout = 'NFM';
pres.author = 'Instituto NFM';
pres.company = 'Instituto de Productividad';
pres.title = 'El mapa del 1%';
pres.subject = 'El camino completo, en tres pasos';

meta.forEach((m, i) => {
  const dark = ['qualify', 'cta'].includes(m.type);
  const s = pres.addSlide();
  s.background = { color: dark ? '061D30' : 'FFFFFF' };
  s.addImage({ path: `${D}/s${String(i + 1).padStart(2, '0')}.png`, x: 0, y: 0, w: 13.333, h: 7.5 });
  const parts = [`${String(i + 1).padStart(2, '0')} / 11 · ${strip(m.titulo)}`];
  if (m.notes.length) parts.push(m.notes.map(n => '• ' + strip(n)).join('\n\n'));
  if (m.cue) parts.push('CÓMO DECIRLO\n' + strip(m.cue));
  s.addNotes(parts.join('\n\n'));
});

pres.writeFile({ fileName: `${D}/El-mapa-del-1-pct.pptx` }).then(f => console.log('escrito:', f));
