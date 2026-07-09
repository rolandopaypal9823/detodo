/**
 * NFM — Tracking del "Test de Alto Rendimiento" → Google Sheet
 * ------------------------------------------------------------
 * Recibe cada evento del test (respuestas, hasta dónde llegó, clics en agendar/libro)
 * y lo agrega como una fila en la hoja "eventos".
 *
 * CÓMO CONECTARLO (5 minutos, gratis, sin servidor):
 *   1. Creá un Google Sheet nuevo (drive.google.com → Hoja de cálculo).
 *   2. Adentro de ESE Sheet: Extensiones → Apps Script. Borrá lo que haya y pegá TODO
 *      este archivo. Guardá (💾).
 *      (Importante: creá el script DESDE el Sheet con Extensiones, no como proyecto suelto.
 *       Si igual lo hiciste suelto, completá SHEET_ID abajo con el id de tu planilla.)
 *   3. Implementar → Nueva implementación → engranaje ⚙️ → "Aplicación web".
 *        - Ejecutar como: Yo
 *        - Quién tiene acceso: CUALQUIER PERSONA   ← clave, si no, no escribe
 *      → Implementar. Autorizá los permisos.
 *   4. Copiá la "URL de la aplicación web" (termina en /exec) y pegala en TRACK_ENDPOINT
 *      del HTML. Subí el HTML.
 *
 * ⚠️ Cada vez que edites este código, tenés que "Administrar implementaciones" → editar
 *    (lápiz) → Versión: NUEVA → Implementar. Si no, la URL /exec sigue con el código viejo.
 *
 * PROBAR SIN EL TEST: abrí en el navegador  <tu URL /exec>?test=1
 *   → debería aparecer una fila con event="test_ping" en la hoja "eventos".
 *   Si aparece: el Sheet funciona (el problema estaba en dónde probaste el HTML).
 *   Si NO aparece: es permiso/implementación (revisá los pasos 2-3).
 */

var SHEET_NAME = 'eventos';
var SHEET_ID = '';   // dejalo vacío si creaste el script DESDE el Sheet (Extensiones→Apps Script)

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return json_({ ok: false, error: 'sin body' });
    }
    appendRow_(JSON.parse(e.postData.contents));
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

// Abrí la /exec en el navegador: sin params muestra estado; con ?test=1 escribe una fila de prueba.
function doGet(e) {
  try {
    if (e && e.parameter && (e.parameter.test || e.parameter.write)) {
      appendRow_({ ts: new Date().toISOString(), event: 'test_ping', note: 'fila de prueba desde doGet' });
      return json_({ ok: true, wrote: true, msg: 'Fila de prueba escrita. Revisá la hoja "eventos".' });
    }
    return json_({ ok: true, msg: 'NFM tracking endpoint activo' });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function getSheet_() {
  var ss = SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    throw new Error('No encuentro la planilla. Si creaste el script suelto, completá SHEET_ID con el id del Sheet.');
  }
  return ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
}

function appendRow_(obj) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000); // evita filas pisadas si entran varios eventos a la vez
  try {
    var sh = getSheet_();
    var lastCol = Math.max(1, sh.getLastColumn());
    var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0].filter(String);

    if (headers.length === 0) {
      headers = ['ts', 'event', 'q', 'answerText', 'value', 'count',
                 'profession', 'profile', 'pct', 'camino', 'cta',
                 'visitorId', 'ip', 'sessionId', 'step',
                 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
                 'lang', 'tz', 'screen', 'referrer', 'url', 'ua'];
      sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }

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
