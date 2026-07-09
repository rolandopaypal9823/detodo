/**
 * NFM — Tracking del "Test de Alto Rendimiento" → Google Sheet
 * ------------------------------------------------------------
 * Recibe cada evento del test (respuestas, hasta dónde llegó, clics en agendar/libro)
 * y lo agrega como una fila en la hoja "eventos".
 *
 * CÓMO CONECTARLO (5 minutos, gratis, sin servidor):
 *   1. Creá un Google Sheet nuevo (drive.google.com → Hoja de cálculo).
 *   2. Extensiones → Apps Script. Borrá lo que haya y pegá TODO este archivo. Guardá (💾).
 *   3. Implementar → Nueva implementación → engranaje ⚙️ → "Aplicación web".
 *        - Descripción: tracking test
 *        - Ejecutar como: Yo
 *        - Quién tiene acceso: Cualquier persona
 *      → Implementar. Autorizá los permisos que pida.
 *   4. Copiá la "URL de la aplicación web" (termina en /exec).
 *   5. En test-alto-rendimiento.html buscá  const TRACK_ENDPOINT = '';
 *      y pegá esa URL entre las comillas. Subí el HTML. Listo.
 *
 * Cada vez que cambies el código, tenés que crear una NUEVA implementación (o "Administrar
 * implementaciones" → editar → nueva versión) para que tome los cambios.
 */

var SHEET_NAME = 'eventos';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    appendRow_(data);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

// Permite abrir la URL en el navegador para chequear que está viva.
function doGet() {
  return json_({ ok: true, msg: 'NFM tracking endpoint activo' });
}

function appendRow_(obj) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000); // evita filas pisadas si entran varios eventos a la vez
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    var lastCol = Math.max(1, sh.getLastColumn());
    var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0].filter(String);

    if (headers.length === 0) {
      // Orden inicial sugerido; se agregan columnas nuevas al final si aparecen.
      headers = ['ts', 'event', 'q', 'answerText', 'value', 'count',
                 'profession', 'profile', 'pct', 'camino', 'cta',
                 'visitorId', 'ip', 'sessionId', 'step',
                 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
                 'lang', 'tz', 'screen', 'referrer', 'url', 'ua'];
      sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }

    // Agrega columnas nuevas si el evento trae una clave desconocida.
    Object.keys(obj).forEach(function (k) {
      if (headers.indexOf(k) === -1) {
        headers.push(k);
        sh.getRange(1, headers.length).setValue(k).setFontWeight('bold');
      }
    });

    var flat = {};
    Object.keys(obj).forEach(function (k) {
      var v = obj[k];
      flat[k] = (v && typeof v === 'object') ? JSON.stringify(v) : v;
    });

    var row = headers.map(function (h) { return (h in flat) ? flat[h] : ''; });
    sh.appendRow(row);
  } finally {
    lock.releaseLock();
  }
}

function json_(o) {
  return ContentService
    .createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}
