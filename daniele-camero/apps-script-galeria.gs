/**
 * Galería del Punto Ciego → Google Sheets
 * Una fila por persona en la pestaña «Respuestas». Se completa a medida que avanza.
 * Cada envío también queda en la pestaña «Registro», por las dudas.
 */
const COLS = ['Primera vez', 'Última vez', 'ID', 'Nombre', 'Email', 'Teléfono', 'Pasos hechos', 'Patrón',
  'Tiempo en el mismo número', 'Después de un mes bueno', 'Qué hizo el último año', 'Frase que más se dice', 'Área a cambiar primero',
  'Punto A (hoy)', 'Punto B (90 días)', 'Qué cree que lo detiene', 'utm_source', 'utm_campaign', 'utm_content', 'Página'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    if (!d.id) d.id = 'sin-id-' + Date.now();
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    hoja(ss, 'Registro', ['Fecha', 'Evento', 'ID', 'Datos']).appendRow([new Date(), limpio(d.evento), limpio(d.id), JSON.stringify(d).slice(0, 45000)]);

    const q = d.quiz || {}, t = q.textos || [], f = d.ficha || {}, u = d.utm || {};
    const datos = {
      'Última vez': new Date(), 'ID': d.id, 'Nombre': f.nombre || d.nombre, 'Email': d.email, 'Teléfono': d.telefono,
      'Pasos hechos': d.pasos ? d.pasos + ' de 4' : '', 'Patrón': d.patron,
      'Tiempo en el mismo número': t[0], 'Después de un mes bueno': t[1], 'Qué hizo el último año': t[2],
      'Frase que más se dice': t[3], 'Área a cambiar primero': t[4],
      'Punto A (hoy)': f.a, 'Punto B (90 días)': f.b, 'Qué cree que lo detiene': f.d,
      'utm_source': u.utm_source, 'utm_campaign': u.utm_campaign, 'utm_content': u.utm_content, 'Página': d.pagina
    };

    const sh = hoja(ss, 'Respuestas', COLS);
    const ultima = sh.getLastRow();
    const ids = ultima > 1 ? sh.getRange(2, 3, ultima - 1, 1).getValues().map(r => String(r[0])) : [];
    let fila = ids.indexOf(String(d.id)) + 2, actual;
    if (fila < 2) { fila = ultima + 1; actual = COLS.map(() => ''); actual[0] = new Date(); }
    else actual = sh.getRange(fila, 1, 1, COLS.length).getValues()[0];
    COLS.forEach((c, i) => { const v = datos[c]; if (v !== undefined && v !== null && v !== '') actual[i] = limpio(v); });
    sh.getRange(fila, 1, 1, COLS.length).setValues([actual]);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput('Funciona. Esta URL recibe las respuestas de la galería.');
}

function hoja(ss, nombre, cols) {
  let sh = ss.getSheetByName(nombre);
  if (!sh) sh = ss.insertSheet(nombre);
  if (sh.getLastRow() === 0) { sh.appendRow(cols); sh.setFrozenRows(1); sh.getRange(1, 1, 1, cols.length).setFontWeight('bold'); }
  return sh;
}

// Corta textos largos y evita que un texto que empieza con = se lea como fórmula.
function limpio(v) {
  if (v instanceof Date) return v;
  const s = String(v).slice(0, 500);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
