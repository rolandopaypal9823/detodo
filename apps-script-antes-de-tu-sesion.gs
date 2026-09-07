/**
 * ═══════════════════════════════════════════════════════════════════════
 *  ANTES DE TU SESIÓN — recibe las respuestas del quiz y las escribe
 *  en esta misma planilla, una fila por persona.
 *
 *  CÓMO INSTALARLO (5 minutos, una sola vez)
 *  ─────────────────────────────────────────────────────────────────────
 *  1. Creá una planilla nueva en Google Sheets.
 *  2. Menú  Extensiones → Apps Script.
 *  3. Borrá todo lo que haya y pegá ESTE archivo completo. Guardá.
 *  4. Botón  Implementar → Nueva implementación.
 *       · Tipo:            Aplicación web
 *       · Ejecutar como:   Yo
 *       · Quién tiene acceso: CUALQUIER PERSONA   ← importante
 *  5. Copiá la URL que termina en  /exec  y pegámela: va en
 *     CONFIG.SHEETS_ENDPOINT dentro de quiz-antes-de-tu-sesion.html
 *
 *  OJO: cada vez que edites este script hay que hacer
 *  Implementar → Gestionar implementaciones → editar (lápiz) → Versión: Nueva.
 *  Si no, sigue corriendo la versión vieja.
 * ═══════════════════════════════════════════════════════════════════════
 */

var HOJA = 'Respuestas';

/* Orden de las columnas. La clave de la izquierda es la que manda el quiz. */
var COLUMNAS = [
  ['fecha',     'Fecha'],
  ['nombre',    'Nombre'],
  ['perfil',    'Perfil profesional'],
  ['contexto',  'Contexto personal'],
  ['dolor',     'Qué le pesa hoy'],
  ['situacion', 'Qué lo disparó'],
  ['intentos',  'Qué ya intentó'],
  ['costo',     'Qué le dolería no resolver'],
  ['urgencia',  'Urgencia (1-10)'],
  ['freno',     'Qué la frenaría'],
  ['origen',    'Origen']
];

function doPost(e) {
  try {
    var datos = JSON.parse(e.postData.contents);
    guardar(datos);
    return json({ok: true});
  } catch (err) {
    // Queda registrado en Ejecuciones por si algo falla
    console.error(err);
    return json({ok: false, error: String(err)});
  }
}

/* Sirve para probar desde el navegador: abrí la URL /exec y tiene que decir OK */
function doGet() {
  return ContentService.createTextOutput('OK — el endpoint está vivo');
}

function guardar(datos) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(HOJA) || ss.insertSheet(HOJA);

  // Encabezados la primera vez
  if (sh.getLastRow() === 0) {
    var titulos = COLUMNAS.map(function (c) { return c[1]; });
    sh.appendRow(titulos);
    sh.getRange(1, 1, 1, titulos.length)
      .setFontWeight('bold')
      .setBackground('#0c3452')
      .setFontColor('#ffffff');
    sh.setFrozenRows(1);
    sh.setColumnWidth(1, 150);   // fecha
    sh.setColumnWidth(2, 160);   // nombre
    [6, 7, 8].forEach(function (n) { sh.setColumnWidth(n, 380); }); // respuestas largas
  }

  var fila = COLUMNAS.map(function (c) {
    var v = datos[c[0]];
    if (c[0] === 'fecha') return fechaLegible(datos.fecha);
    return (v === undefined || v === null) ? '' : v;
  });

  sh.appendRow(fila);
  var n = sh.getLastRow();
  sh.getRange(n, 1, 1, COLUMNAS.length).setVerticalAlignment('top').setWrap(true);
}

/* ISO → "07/09/2026 14:32" en la zona horaria de la planilla */
function fechaLegible(iso) {
  try {
    var d = iso ? new Date(iso) : new Date();
    var tz = SpreadsheetApp.getActiveSpreadsheet().getSpreadsheetTimeZone();
    return Utilities.formatDate(d, tz, 'dd/MM/yyyy HH:mm');
  } catch (err) {
    return iso || '';
  }
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ─────────────────────────────────────────────────────────────────────
   PRUEBA MANUAL
   Ejecutá esta función desde el editor (botón Ejecutar) para verificar
   que escribe bien en la planilla, sin depender de la página.
   ───────────────────────────────────────────────────────────────────── */
function probar() {
  guardar({
    fecha: new Date().toISOString(),
    nombre: 'Prueba desde el editor',
    perfil: 'Líder o gerente de equipo',
    contexto: 'Soy madre',
    dolor: 'Vivo apagando incendios, sin poder priorizar lo importante',
    situacion: 'Texto de prueba de la primera pregunta abierta.',
    intentos: 'Texto de prueba de la segunda pregunta abierta.',
    costo: 'Texto de prueba de la tercera pregunta abierta.',
    urgencia: '8 de 10',
    freno: 'Dinero',
    origen: 'prueba manual'
  });
}
