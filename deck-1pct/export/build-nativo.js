/* ═══════════════════════════════════════════════════════════════
   EL MAPA DEL 1% → PPTX 100% EDITABLE
   Todo se construye con formas y cuadros de texto nativos de
   PowerPoint. Las únicas imágenes son las ilustraciones de Mini
   Nico (una ilustración no puede ser "nativa").
   ═══════════════════════════════════════════════════════════════ */
const D = __dirname;
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const meta = JSON.parse(fs.readFileSync(`${D}/meta.json`, 'utf8'));

/* ── Marca NFM ── */
const NAVY   = '0C3452';
const DARK   = '061D30';
const ORANGE = 'FF6602';
const WHITE  = 'FFFFFF';
const LOCKED = 'C9D2DA';
const GREY   = '6B7280';
const DISP   = 'Montserrat';
const SANS   = 'Open Sans';

/* Lienzo 13,333 × 7,5" = 1920×1080. Factor px → pulgadas */
const PX = 13.333 / 1920;
const x = px => +(px * PX).toFixed(3);

const pres = new pptxgen();
pres.defineLayout({ name: 'NFM', width: 13.333, height: 7.5 });
pres.layout = 'NFM';
pres.author  = 'Instituto NFM';
pres.company = 'Instituto de Productividad';
pres.title   = 'El mapa del 1%';

const strip = s => String(s).replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');

function notas(s, i) {
  const m = meta[i];
  if (!m) return;
  const partes = [`${String(i + 1).padStart(2, '0')} / 11 · ${strip(m.titulo)}`];
  if (m.notes && m.notes.length) partes.push(m.notes.map(n => '• ' + strip(n)).join('\n\n'));
  if (m.cue) partes.push('CÓMO DECIRLO\n' + strip(m.cue));
  s.addNotes(partes.join('\n\n'));
}

/* ── Barra de marca: raya naranja + kicker ── */
function brandbar(s, txt, top, color) {
  s.addShape(pres.ShapeType.rect, { x: x(130), y: x(top), w: x(96), h: x(5), fill: { color: ORANGE } });
  s.addText(txt.toUpperCase(), {
    x: x(244), y: x(top - 14), w: x(900), h: x(34),
    fontFace: 'Courier New', fontSize: 13, bold: true, color: color || NAVY,
    charSpacing: 4, valign: 'middle', margin: 0,
  });
}

/* ── Contador de página ── */
function contador(s, n, color) {
  s.addText(`${String(n).padStart(2, '0')} / 11`, {
    x: x(1620), y: x(985), w: x(200), h: x(40),
    fontFace: 'Courier New', fontSize: 13, color: color || LOCKED,
    align: 'right', charSpacing: 3, margin: 0,
  });
}

/* ═══════════════════════════════════════════════════════════════
   EL MAPA — origen + 3 estaciones, todo con formas nativas
   estadoActual: 0 = ninguna, 1..3 = esa estación activa, 4 = todas hechas
   ═══════════════════════════════════════════════════════════════ */
const EST = [
  { n: 1, label: 'LA APLICACIÓN', cx: 520 },
  { n: 2, label: 'LA ENTREVISTA', cx: 1080 },
  { n: 3, label: 'EL ACCESO',     cx: 1640 },
];

function mapa(s, actual, topPx) {
  const T = topPx;              // desplazamiento vertical del mapa
  const yLinea = T + 150;       // eje del sendero
  const R = 46;                 // radio de las estaciones

  // Sendero punteado completo (gris)
  s.addShape(pres.ShapeType.line, {
    x: x(186), y: x(yLinea), w: x(1640 - 186), h: 0,
    line: { color: LOCKED, width: 3, dashType: 'sysDot' },
  });

  // Tramo recorrido (naranja sólido) hasta la estación actual
  if (actual >= 1) {
    const hasta = actual >= 4 ? EST[2].cx : EST[Math.min(actual, 3) - 1].cx;
    s.addShape(pres.ShapeType.line, {
      x: x(186), y: x(yLinea), w: x(hasta - 186), h: 0,
      line: { color: ORANGE, width: 4 },
    });
  }

  // Punto de origen
  s.addShape(pres.ShapeType.ellipse, {
    x: x(186 - 13), y: x(yLinea - 13), w: x(26), h: x(26), fill: { color: NAVY },
  });
  s.addText('ESTÁS ACÁ', {
    x: x(186 - 120), y: x(yLinea + 26), w: x(240), h: x(30),
    fontFace: 'Courier New', fontSize: 11, color: NAVY, align: 'center', charSpacing: 3, margin: 0,
  });

  // Estaciones
  EST.forEach(e => {
    const hecha  = actual >= 4 || e.n < actual;
    const activa = actual < 4 && e.n === actual;
    const col    = (hecha || activa) ? NAVY : LOCKED;

    // Halo naranja en la estación activa
    if (activa) {
      s.addShape(pres.ShapeType.ellipse, {
        x: x(e.cx - R - 12), y: x(yLinea - R - 12), w: x((R + 12) * 2), h: x((R + 12) * 2),
        fill: { type: 'none' }, line: { color: ORANGE, width: 3 },
      });
    }

    // Disco de la estación
    s.addShape(pres.ShapeType.ellipse, {
      x: x(e.cx - R), y: x(yLinea - R), w: x(R * 2), h: x(R * 2),
      fill: { color: WHITE }, line: { color: col, width: 3 },
    });

    // Tilde verde cuando ya está hecha
    if (hecha) {
      s.addShape(pres.ShapeType.ellipse, {
        x: x(e.cx + R - 20), y: x(yLinea - R - 4), w: x(30), h: x(30),
        fill: { color: '25D366' },
      });
      s.addText('✓', {
        x: x(e.cx + R - 20), y: x(yLinea - R - 4), w: x(30), h: x(30),
        fontSize: 12, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0,
      });
    }

    // Número y etiqueta
    s.addText(String(e.n).padStart(2, '0'), {
      x: x(e.cx - 80), y: x(yLinea + R + 6), w: x(160), h: x(48),
      fontFace: DISP, fontSize: 26, bold: true,
      color: activa ? ORANGE : col, align: 'center', margin: 0,
    });
    s.addText(e.label, {
      x: x(e.cx - 180), y: x(yLinea + R + 52), w: x(360), h: x(36),
      fontFace: DISP, fontSize: 15, bold: true,
      color: col, align: 'center', charSpacing: 1, margin: 0,
    });
  });

  // Mini Nico parado sobre la estación actual
  if (actual >= 1) {
    const cx = actual >= 4 ? EST[2].cx : EST[Math.min(actual, 3) - 1].cx;
    s.addImage({
      path: `${D}/img/mini-nico-marker.png`,
      x: x(cx - 62), y: x(yLinea - R - 182), w: x(124), h: x(182),
    });
  }
}

/* ═══════════════════════════════════════════════════════════════
   Tarjeta genérica (para mockups y bloques de contenido)
   ═══════════════════════════════════════════════════════════════ */
function tarjeta(s, o) {
  s.addShape(pres.ShapeType.roundRect, {
    x: x(o.x), y: x(o.y), w: x(o.w), h: x(o.h),
    fill: { color: o.fill || WHITE },
    line: { color: o.line || 'E2E8F0', width: 1 },
    rectRadius: 0.12,
    shadow: o.sombra === false ? undefined
      : { type: 'outer', color: '0C3452', opacity: 0.10, blur: 18, offset: 6, angle: 90 },
  });
}

/* Ítem de lista con viñeta naranja */
function bullet(s, o) {
  s.addText('·', {
    x: x(o.x), y: x(o.y), w: x(24), h: x(34),
    fontFace: DISP, fontSize: 20, bold: true, color: ORANGE, margin: 0,
  });
  s.addText(o.texto, {
    x: x(o.x + 26), y: x(o.y), w: x(o.w), h: x(o.h || 120),
    fontFace: SANS, fontSize: o.size || 13, color: o.color || WHITE,
    lineSpacingMultiple: 1.32, valign: 'top', margin: 0,
  });
}

/* ═══════════════════════════════════════════════════════════════
   SLIDE 01 · PORTADA
   ═══════════════════════════════════════════════════════════════ */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  brandbar(s, 'Instituto de Productividad · NFM', 360);

  s.addText(
    [
      { text: '¿Querés que te muestre cómo aplicar el sistema completo en tu vida con nuestro ', options: { color: NAVY } },
      { text: 'acompañamiento', options: { color: ORANGE } },
      { text: '?', options: { color: NAVY } },
    ],
    {
      x: x(130), y: x(430), w: x(1560), h: x(300),
      fontFace: DISP, fontSize: 40, bold: true,
      lineSpacingMultiple: 1.06, charSpacing: -0.5, valign: 'top', margin: 0,
    },
  );

  s.addText('El camino que empieza hoy.', {
    x: x(130), y: x(760), w: x(1000), h: x(60),
    fontFace: SANS, fontSize: 20, bold: true, color: NAVY, margin: 0,
  });

  contador(s, 1);
  notas(s, 0);
}

/* ═══════════════════════════════════════════════════════════════
   SLIDE 02 · EL CAMINO (intro)
   ═══════════════════════════════════════════════════════════════ */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  mapa(s, 0, 250);

  s.addText(
    [
      { text: 'Va a ser así.\nTres pasos.\nY ', options: { color: NAVY } },
      { text: 'uno solo depende de vos', options: { color: ORANGE } },
      { text: '.', options: { color: NAVY } },
    ],
    {
      x: x(130), y: x(560), w: x(1100), h: x(300),
      fontFace: DISP, fontSize: 42, bold: true,
      lineSpacingMultiple: 1.02, charSpacing: -0.5, margin: 0,
    },
  );

  s.addText('La aplicación, la entrevista, y el acceso a tu sistema. El de hoy te lleva 90 segundos.', {
    x: x(130), y: x(880), w: x(1200), h: x(60),
    fontFace: SANS, fontSize: 15, color: GREY, margin: 0,
  });

  contador(s, 2);
  notas(s, 1);
}

/* ═══════════════════════════════════════════════════════════════
   SLIDES 03-08 · LOS 6 NODOS
   ═══════════════════════════════════════════════════════════════ */
const NODOS = [
  { est: 1, paso: 'PASO 01 / 03 · LA APLICACIÓN', titulo: 'Reservás tu entrevista',
    copy: 'Elegís tu horario y nos contás unos datos, para asignarte el coach que corresponde a tu caso.',
    mock: 'form' },
  { est: 1, paso: 'PASO 01 / 03 · LA APLICACIÓN', titulo: 'Tu autodiagnóstico',
    copy: 'Te lo mandamos por WhatsApp. Con eso armamos tu sistema personal.',
    mock: 'wa' },
  { est: 2, paso: 'PASO 02 / 03 · LA ENTREVISTA', titulo: 'Con tu coach asignado',
    copy: 'Vemos tu caso en profundidad y si realmente podemos ayudarte. Puede que no.',
    mock: 'foto' },
  { est: 2, paso: 'PASO 02 / 03 · LA ENTREVISTA', titulo: 'Lo único que te pedimos',
    copy: 'Que confirmes por WhatsApp y que cumplas el horario que elegiste.',
    mock: 'pares' },
  { est: 3, paso: 'PASO 03 / 03 · EL ACCESO', titulo: 'Accedés a tu sistema',
    copy: 'Si hacemos match, entrás a todo. Y no me tenés solo a mí: tenés al equipo entero atrás.',
    mock: 'widget' },
  { est: 3, paso: 'PASO 03 / 03 · EL ACCESO', titulo: 'Y si no hacemos match',
    copy: 'Te llevás igual tu entregable, preparado con el autodiagnóstico que hiciste en el paso uno.',
    mock: 'tracker' },
];

const PARES = [
  { k: 'Confirmás', t: 'Nos contestás por WhatsApp', d: 'Con eso queda tomado tu lugar y sabemos que vas.' },
  { k: 'Asistís',   t: 'Cumplís el horario que elegiste', d: 'Del otro lado hay profesionales preparando tu caso antes de la llamada.' },
];

const INCLUYE = [
  ['01', 'Tu coach dedicada, 1 a 1'],
  ['02', 'Biblioteca de +20 módulos'],
  ['03', 'Llamadas grupales en vivo'],
  ['04', 'Comunidad + mastermind presencial'],
  ['05', 'Equipo multidisciplinario'],
  ['06', 'Método y sistemas listos'],
];

NODOS.forEach((nd, k) => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  mapa(s, nd.est, 96);   // 96 y no 22: Mini Nico mide 182px y se salía por arriba

  // Bloque de texto (izquierda)
  s.addText(nd.paso, {
    x: x(130), y: x(690), w: x(900), h: x(34),
    fontFace: 'Courier New', fontSize: 13, bold: true, color: ORANGE, charSpacing: 3, margin: 0,
  });
  s.addText(nd.titulo, {
    x: x(130), y: x(740), w: x(820), h: x(90),
    fontFace: DISP, fontSize: 34, bold: true, color: NAVY, charSpacing: -0.5, margin: 0,
  });
  s.addText(nd.copy, {
    x: x(130), y: x(848), w: x(820), h: x(120),
    fontFace: SANS, fontSize: 16, color: NAVY, lineSpacingMultiple: 1.4, margin: 0,
  });

  // Bloque visual (derecha)
  const RX = 1010, RY = 560, RW = 780, RH = 460;

  if (nd.mock === 'form') {
    tarjeta(s, { x: RX, y: RY, w: 370, h: RH });
    s.addText('Reservá tu entrevista', {
      x: x(RX + 28), y: x(RY + 28), w: x(310), h: x(40),
      fontFace: DISP, fontSize: 14, bold: true, color: NAVY, margin: 0 });
    ['Nombre y apellido', 'WhatsApp', 'A qué te dedicás hoy'].forEach((campo, i) => {
      s.addShape(pres.ShapeType.roundRect, {
        x: x(RX + 28), y: x(RY + 84 + i * 74), w: x(310), h: x(54),
        fill: { color: 'F4F7FA' }, line: { color: 'E2E8F0', width: 1 }, rectRadius: 0.06 });
      s.addText(campo, {
        x: x(RX + 44), y: x(RY + 84 + i * 74), w: x(290), h: x(54),
        fontFace: SANS, fontSize: 11, color: GREY, valign: 'middle', margin: 0 });
    });
    s.addShape(pres.ShapeType.roundRect, {
      x: x(RX + 28), y: x(RY + 310), w: x(310), h: x(56),
      fill: { color: ORANGE }, rectRadius: 0.06 });
    s.addText('Elegir horario  →', {
      x: x(RX + 28), y: x(RY + 310), w: x(310), h: x(56),
      fontFace: DISP, fontSize: 13, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0 });

    // Calendario simplificado
    tarjeta(s, { x: RX + 410, y: RY, w: 370, h: RH });
    s.addText('Elegí tu horario', {
      x: x(RX + 438), y: x(RY + 28), w: x(310), h: x(40),
      fontFace: DISP, fontSize: 14, bold: true, color: NAVY, margin: 0 });
    for (let f = 0; f < 4; f++) for (let c = 0; c < 5; c++) {
      const activo = (f === 1 && c === 2);
      s.addShape(pres.ShapeType.roundRect, {
        x: x(RX + 438 + c * 62), y: x(RY + 84 + f * 62), w: x(52), h: x(52),
        fill: { color: activo ? ORANGE : 'F4F7FA' },
        line: { color: 'E2E8F0', width: 1 }, rectRadius: 0.05 });
    }

  } else if (nd.mock === 'wa') {
    tarjeta(s, { x: RX, y: RY, w: RW, h: RH, fill: 'EDE5DD' });
    s.addShape(pres.ShapeType.rect, {
      x: x(RX), y: x(RY), w: x(RW), h: x(74), fill: { color: NAVY } });
    s.addText('Asesor · Instituto de Productividad', {
      x: x(RX + 78), y: x(RY + 14), w: x(600), h: x(28),
      fontFace: DISP, fontSize: 13, bold: true, color: WHITE, margin: 0 });
    s.addText('en línea', {
      x: x(RX + 78), y: x(RY + 42), w: x(400), h: x(24),
      fontFace: SANS, fontSize: 10, color: 'C9D2DA', margin: 0 });
    s.addShape(pres.ShapeType.ellipse, {
      x: x(RX + 20), y: x(RY + 16), w: x(44), h: x(44), fill: { color: ORANGE } });
    s.addText('IP', {
      x: x(RX + 20), y: x(RY + 16), w: x(44), h: x(44),
      fontFace: DISP, fontSize: 12, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0 });

    const msgs = [
      '¡Felicitaciones! Recibimos tu solicitud.',
      'Tu próximo paso: realizá este autodiagnóstico para desbloquear tus recursos y herramientas.',
      'Autodiagnóstico de Alto Rendimiento · 3 minutos',
    ];
    let yy = RY + 100;
    msgs.forEach(m => {
      const alto = m.length > 60 ? 96 : 60;
      s.addShape(pres.ShapeType.roundRect, {
        x: x(RX + 24), y: x(yy), w: x(500), h: x(alto),
        fill: { color: WHITE }, line: { color: 'E2E8F0', width: 1 }, rectRadius: 0.08 });
      s.addText(m, {
        x: x(RX + 42), y: x(yy), w: x(464), h: x(alto),
        fontFace: SANS, fontSize: 12, color: '2D3748', valign: 'middle',
        lineSpacingMultiple: 1.3, margin: 0 });
      yy += alto + 16;
    });

  } else if (nd.mock === 'foto') {
    tarjeta(s, { x: RX, y: RY, w: RW, h: RH, sombra: false, line: 'FFFFFF' });
    s.addImage({ path: `${D}/img/mini-nico-videollamada.jpg`,
      x: x(RX), y: x(RY), w: x(RW), h: x(RH) });

  } else if (nd.mock === 'pares') {
    PARES.forEach((p, i) => {
      const py = RY + i * 236;
      tarjeta(s, { x: RX, y: py, w: RW, h: 210 });
      s.addText(p.k.toUpperCase(), {
        x: x(RX + 32), y: x(py + 26), w: x(400), h: x(30),
        fontFace: 'Courier New', fontSize: 12, bold: true, color: ORANGE, charSpacing: 3, margin: 0 });
      s.addText(p.t, {
        x: x(RX + 32), y: x(py + 62), w: x(700), h: x(46),
        fontFace: DISP, fontSize: 19, bold: true, color: NAVY, margin: 0 });
      s.addText(p.d, {
        x: x(RX + 32), y: x(py + 116), w: x(700), h: x(70),
        fontFace: SANS, fontSize: 13, color: GREY, lineSpacingMultiple: 1.35, margin: 0 });
    });

  } else if (nd.mock === 'widget') {
    INCLUYE.forEach((it, i) => {
      const col = i % 2, fila = (i / 2) | 0;
      const cx0 = RX + col * 400, cy0 = RY + fila * 156;
      tarjeta(s, { x: cx0, y: cy0, w: 372, h: 132 });
      s.addText(it[0], {
        x: x(cx0 + 24), y: x(cy0 + 24), w: x(60), h: x(36),
        fontFace: DISP, fontSize: 16, bold: true, color: ORANGE, margin: 0 });
      s.addText(it[1], {
        x: x(cx0 + 24), y: x(cy0 + 62), w: x(324), h: x(60),
        fontFace: DISP, fontSize: 14, bold: true, color: NAVY,
        lineSpacingMultiple: 1.25, margin: 0 });
    });

  } else if (nd.mock === 'tracker') {
    tarjeta(s, { x: RX, y: RY, w: 370, h: RH });
    s.addText('Habit Tracker', {
      x: x(RX + 28), y: x(RY + 28), w: x(310), h: x(36),
      fontFace: DISP, fontSize: 14, bold: true, color: NAVY, margin: 0 });
    for (let f = 0; f < 5; f++) for (let c = 0; c < 7; c++) {
      s.addShape(pres.ShapeType.roundRect, {
        x: x(RX + 28 + c * 44), y: x(RY + 80 + f * 44), w: x(34), h: x(34),
        fill: { color: (f + c) % 3 === 0 ? ORANGE : 'F4F7FA' },
        line: { color: 'E2E8F0', width: 1 }, rectRadius: 0.04 });
    }
    tarjeta(s, { x: RX + 410, y: RY, w: 370, h: RH });
    s.addText('Tu entregable', {
      x: x(RX + 438), y: x(RY + 28), w: x(310), h: x(36),
      fontFace: DISP, fontSize: 14, bold: true, color: NAVY, margin: 0 });
    ['Tu diagnóstico de foco', 'Dónde se te va la energía', 'Tus 3 primeros movimientos'].forEach((t, i) => {
      s.addShape(pres.ShapeType.roundRect, {
        x: x(RX + 438), y: x(RY + 82 + i * 78), w: x(310), h: x(60),
        fill: { color: 'F4F7FA' }, line: { color: 'E2E8F0', width: 1 }, rectRadius: 0.06 });
      s.addText(t, {
        x: x(RX + 456), y: x(RY + 82 + i * 78), w: x(280), h: x(60),
        fontFace: SANS, fontSize: 11, color: NAVY, valign: 'middle', margin: 0 });
    });
  }

  contador(s, 3 + k);
  notas(s, 2 + k);
});

/* ═══════════════════════════════════════════════════════════════
   SLIDE 09 · CALIFICADOR
   ═══════════════════════════════════════════════════════════════ */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  brandbar(s, 'Antes de agendar', 118, WHITE);

  s.addText('Dos cosas, para ser honestos.', {
    x: x(110), y: x(178), w: x(1600), h: x(100),
    fontFace: DISP, fontSize: 40, bold: true, color: WHITE, charSpacing: -0.5, margin: 0,
  });

  // Divisor central
  s.addShape(pres.ShapeType.line, {
    x: x(960), y: x(300), w: 0, h: x(700),
    line: { color: 'FFFFFF', width: 1, transparency: 86 },
  });

  /* Columna SÍ */
  s.addText('Esto es para vos si…', {
    x: x(110), y: x(330), w: x(760), h: x(56),
    fontFace: DISP, fontSize: 25, bold: true, color: WHITE, margin: 0,
  });
  const SI = [
    [{ text: 'Ya tenés algo andando: un negocio, un equipo, una carrera, un estudio. Y llegaste hasta acá a fuerza de horas.' }],
    [{ text: 'Hoy ' }, { text: 'el cuello de botella sos vos', options: { color: ORANGE, bold: true } },
     { text: '. Todo pasa por tus manos, delegar te cuesta más que hacerlo, y sabés que de acá no pasás sumando esfuerzo.' }],
    [{ text: 'No venís a empezar. Venís a que lo que ya construiste ' },
     { text: 'funcione sin que vos lo sostengas', options: { color: ORANGE, bold: true } },
     { text: ' — no a punta de voluntad, más disciplina o más esfuerzo, sino con un sistema integral.' }],
  ];
  let ys = 404;
  SI.forEach(p => {
    s.addText(p, {
      x: x(110), y: x(ys), w: x(760), h: x(150),
      fontFace: SANS, fontSize: 15, color: WHITE, lineSpacingMultiple: 1.42, valign: 'top', margin: 0,
    });
    ys += 158;
  });

  /* Columna SABER */
  s.addText('Y esto es lo que tenés que saber', {
    x: x(1050), y: x(330), w: x(760), h: x(56),
    fontFace: DISP, fontSize: 25, bold: true, color: ORANGE, margin: 0,
  });
  const SABER = [
    'Es una mentoría con un equipo que te sostiene: coaches, psicóloga, nutricionista, sesiones uno a uno. No estás comprando un curso, estás invirtiendo en un sistema integral.',
    'El monto se define en la entrevista, según tu caso y lo que necesites. No te vamos a recomendar el plan más caro: el que te vaya a dar resultados.',
    'Si buscás un cursito de 200 dólares que promete soluciones mágicas y a los diez días te devuelve a la misma rutina de antes, esto no es lo que estás buscando.',
  ];
  let yb = 404;
  SABER.forEach(t => {
    bullet(s, { x: 1050, y: yb, w: 730, h: 150, texto: t, size: 14 });
    yb += 150;
  });

  // Línea + cierre
  s.addShape(pres.ShapeType.line, {
    x: x(1050), y: x(862), w: x(756), h: 0,
    line: { color: 'FFFFFF', width: 1, transparency: 86 },
  });
  s.addText([
    { text: 'Trabajamos con gente que tiene ' },
    { text: 'un objetivo concreto y una vida exigente encima', options: { bold: true } },
    { text: ': un negocio, un equipo, una carrera, un proyecto propio. Si hoy tu prioridad es llegar a fin de mes o batallar para pagar el alquiler: ' },
    { text: 'hoy no es tu momento', options: { bold: true } },
    { text: ' — y está perfecto.' },
  ], {
    x: x(1050), y: x(886), w: x(756), h: x(130),
    fontFace: SANS, fontSize: 13, color: 'C9D2DA', lineSpacingMultiple: 1.4, margin: 0,
  });

  contador(s, 9, '6B7280');
  notas(s, 8);
}

/* ═══════════════════════════════════════════════════════════════
   SLIDE 10 · EL QR
   ═══════════════════════════════════════════════════════════════ */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  brandbar(s, 'Cómo se entra', 200, WHITE);

  s.addText([
    { text: 'No te pido que hagas todo hoy.\nTe pido ', options: { color: WHITE } },
    { text: 'tu 1%', options: { color: ORANGE } },
    { text: '.', options: { color: WHITE } },
  ], {
    x: x(130), y: x(280), w: x(950), h: x(200),
    fontFace: DISP, fontSize: 40, bold: true, lineSpacingMultiple: 1.06, charSpacing: -0.5, margin: 0,
  });

  s.addText('Escaneás el QR, respondés unas preguntas, elegís horario. Todo lo demás del camino que te mostré pasa solo.', {
    x: x(130), y: x(500), w: x(900), h: x(110),
    fontFace: SANS, fontSize: 16, color: 'C9D2DA', lineSpacingMultiple: 1.45, margin: 0,
  });

  ['01 · Escaneás', '02 · Respondés', '03 · Elegís horario'].forEach((p, i) => {
    s.addShape(pres.ShapeType.roundRect, {
      x: x(130 + i * 300), y: x(640), w: x(270), h: x(64),
      fill: { color: 'FFFFFF', transparency: 92 },
      line: { color: 'FFFFFF', width: 1, transparency: 80 }, rectRadius: 0.2 });
    s.addText(p, {
      x: x(130 + i * 300), y: x(640), w: x(270), h: x(64),
      fontFace: 'Courier New', fontSize: 12, bold: true, color: WHITE,
      align: 'center', valign: 'middle', charSpacing: 2, margin: 0 });
  });

  s.addText([
    { text: 'Entrevista de admisión. ', options: { bold: true, color: WHITE } },
    { text: 'Videollamada personal con nuestro Director de Admisiones.', options: { color: 'C9D2DA' } },
  ], {
    x: x(130), y: x(748), w: x(900), h: x(60),
    fontFace: SANS, fontSize: 14, margin: 0,
  });

  // Marco del QR — se reemplaza pegando la imagen encima
  s.addShape(pres.ShapeType.roundRect, {
    x: x(1240), y: x(300), w: x(440), h: x(440),
    fill: { color: WHITE }, rectRadius: 0.08 });
  s.addText('Pegá acá\nel QR', {
    x: x(1240), y: x(300), w: x(440), h: x(440),
    fontFace: DISP, fontSize: 16, bold: true, color: LOCKED,
    align: 'center', valign: 'middle', margin: 0 });
  s.addText('12 cupos esta semana.', {
    x: x(1240), y: x(766), w: x(440), h: x(50),
    fontFace: DISP, fontSize: 16, bold: true, color: ORANGE, align: 'center', margin: 0 });

  contador(s, 10, '6B7280');
  notas(s, 9);
}

/* ═══════════════════════════════════════════════════════════════
   SLIDE 11 · CIERRE
   ═══════════════════════════════════════════════════════════════ */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  mapa(s, 4, 250);

  s.addText([
    { text: 'Ese es el camino completo.\nAhora ', options: { color: NAVY } },
    { text: 'te toca a vos', options: { color: ORANGE } },
    { text: '.', options: { color: NAVY } },
  ], {
    x: x(130), y: x(600), w: x(1200), h: x(220),
    fontFace: DISP, fontSize: 42, bold: true, lineSpacingMultiple: 1.04, charSpacing: -0.5, margin: 0,
  });

  s.addText('Todo esto se basa en una sola cosa: que pases a la acción. Nos vemos del otro lado.', {
    x: x(130), y: x(840), w: x(1200), h: x(60),
    fontFace: SANS, fontSize: 16, color: GREY, margin: 0,
  });

  contador(s, 11);
  notas(s, 10);
}

pres.writeFile({ fileName: `${D}/El-mapa-del-1-pct-EDITABLE.pptx` })
  .then(f => console.log('escrito:', f));
