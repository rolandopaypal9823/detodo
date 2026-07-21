/**
 * ===========================================================================
 *  Registro de leads del pre-formulario de Calendly — Asesores NFM
 * ===========================================================================
 *  Este script vive DENTRO de tu Google Sheet (Extensiones > Apps Script).
 *  Recibe los datos del formulario (index.html) y:
 *
 *    - action:"lead"      -> agrega una fila nueva con estado "Registrado — No agendó"
 *    - action:"scheduled" -> busca esa fila por Lead ID y la marca como "Agendó ✅"
 *
 *  Así, en la planilla vas a ver de un vistazo quiénes dejaron sus datos pero
 *  NO terminaron de agendar (para escribirles por WhatsApp) y quiénes sí.
 * ===========================================================================
 */

var SHEET_NAME = 'Leads';
var HEADERS = [
  'Lead ID',
  'Registrado (fecha/hora)',
  'Nombre',
  'Apellido',
  'Correo',
  'WhatsApp',
  'Estado',
  'Agendó (fecha/hora)',
  'Origen'
];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = getSheet_();

    if (data.action === 'scheduled') {
      markScheduled_(sheet, data);
    } else {
      addLead_(sheet, data);
    }
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Para probar en el navegador que el Web App está desplegado.
function doGet() {
  return json_({ ok: true, message: 'Endpoint activo' });
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function addLead_(sheet, d) {
  // Si ya existe una fila con este Lead ID o este correo, no duplicamos.
  if (findRow_(sheet, d.leadId, d.correo) > 0) return;
  sheet.appendRow([
    d.leadId || '',
    new Date(),
    d.nombre || '',
    d.apellido || '',
    d.correo || '',
    formatWhatsApp_(d.whatsapp),
    'Registrado — No agendó',
    '',
    d.origen || ''
  ]);
}

function markScheduled_(sheet, d) {
  var row = findRow_(sheet, d.leadId, d.correo);
  var now = new Date();
  if (row > 0) {
    sheet.getRange(row, 7).setValue('Agendó ✅');  // columna Estado
    sheet.getRange(row, 8).setValue(now);          // columna Agendó
  } else {
    // Por si el evento "scheduled" llega sin haber registrado el lead antes.
    sheet.appendRow([
      d.leadId || '',
      now,
      d.nombre || '',
      d.apellido || '',
      d.correo || '',
      formatWhatsApp_(d.whatsapp),
      'Agendó ✅',
      now,
      d.origen || ''
    ]);
  }
}

// Busca una fila por Lead ID; si no la encuentra, por correo. Devuelve el nro de fila o -1.
function findRow_(sheet, leadId, correo) {
  var last = sheet.getLastRow();
  if (last < 2) return -1;
  var data = sheet.getRange(2, 1, last - 1, HEADERS.length).getValues();
  var COL_ID = 0;      // 'Lead ID'
  var COL_CORREO = 4;  // 'Correo'
  if (leadId) {
    for (var i = 0; i < data.length; i++) {
      if (String(data[i][COL_ID]) === String(leadId)) return i + 2;
    }
  }
  if (correo) {
    var c = String(correo).trim().toLowerCase();
    for (var j = 0; j < data.length; j++) {
      if (String(data[j][COL_CORREO]).trim().toLowerCase() === c) return j + 2;
    }
  }
  return -1;
}

// Guardamos el WhatsApp como texto (con apóstrofo) para que la planilla
// no le coma el "+" ni lo convierta en número.
function formatWhatsApp_(v) {
  if (!v) return '';
  return "'" + String(v);
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
