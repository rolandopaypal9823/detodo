// ============================================================
// copy.js — TODA la voz visible de Focus en un solo lugar.
//
// Brief de voz (2 palabras): CLÍNICO + CONFRONTATIVO.
// - CLÍNICO domina: panel, stats, labels mono, errores, formularios.
//   Se nombra el dato, nunca el carácter ("0 marcados hoy",
//   jamás "sos inconstante").
// - CONFRONTATIVO solo en superficies marginales: nudge de racha,
//   subs de celebración, cierre de mes.
// Registro rioplatense (vos). Sin emojis: micro-símbolos ◆ ★ ⚡ ✓.
// ============================================================

export const COPY = {
  // ---------- card de racha: máquina de estados ----------
  racha: {
    nuevo: 'MARCÁ 1 HÁBITO Y ARRANCÁ TU RACHA',
    resetAntiCulpa: (best) => `TU MEJOR: ${best} DÍAS · HOY ARRANCA LA NUEVA`,
    enJuego: (n) => `${n} ${n === 1 ? 'DÍA' : 'DÍAS'} EN JUEGO · HOY: 0 MARCADOS`,
    asegurado: '✓ DÍA ASEGURADO',
    completo: (x) => `DÍA COMPLETO · ${x}/${x}`,
    vispera: (m) => `MAÑANA: ${m} DÍAS ◆`,
  },

  // ---------- avisos de inicio ----------
  avisos: {
    congeladorUsado: (quedan) =>
      `Un congelador salvó tu racha. Quedan <strong>${quedan}</strong>. Hoy marcá aunque sea un hábito y seguís sumando.`,
    rachaEnJuego: (n) =>
      `Tu racha de <strong>${n} ${n === 1 ? 'día' : 'días'}</strong> se define hoy. Un hábito alcanza.`,
    cerraElDia: 'Cerrá el día: marcá lo que hiciste hoy.',
    congeladorGanado: (n) => `Ganaste un congelador de racha. Tenés <strong>${n}</strong> en mano.`,
  },

  // ---------- celebraciones ----------
  hitos: {
    7:   { title: 'Una semana entera.', sub: 'Siete días seguidos marcando. El sistema ya arrancó.' },
    30:  { title: '30 días.', sub: 'Un mes sin soltar. Esto dejó de ser un intento: es un sistema.' },
    50:  { title: '50 días.', sub: 'La mitad de camino a los 100. Ya no dependés de la motivación.' },
    100: { title: '100 días.', sub: 'Tres dígitos. Esto ya es parte de quién sos.' },
    365: { title: 'Un año.', sub: '365 días. No hay mucho más que decir.' },
  },
  congeladorGanado: '◆ +1 CONGELADOR DE RACHA GANADO',
  diaPerfecto: (n) => `DÍA PERFECTO ✓ ${n}/${n}`,

  // ---------- cierre de mes ----------
  cierre: {
    titulo: (mes) => `Cierre de ${mes}`,
    intro: 'El mes cerró. Veredicto por hábito — decidí y seguí.',
    subiLaVara: 'Esto ya no te exige. Subí la vara.',
    teAplasta: 'Esta meta te está aplastando. Bajala o eliminá el hábito.',
    subir: (m) => `Subir meta → ${m}`,
    bajar: (m) => `Bajar meta → ${m}`,
    eliminar: 'Eliminar hábito',
    mantener: 'Mantener así',
  },

  // ---------- estados vacíos ----------
  vacios: {
    inicioTitulo: 'Todavía no definiste hábitos',
    inicioSub: 'Arrancá por uno. Con eso alcanza para hoy.',
    inicioCta: 'Definir mi primer hábito',
    panelTitulo: 'Tu panel está esperando',
    panelSub: 'Definí tus hábitos y empezá a marcar tus días.',
    panelCta: 'Definir mis hábitos',
  },

  // ---------- errores (nunca mostrar el string en inglés de Supabase) ----------
  errores: {
    credenciales: 'Email o contraseña incorrectos.',
    yaRegistrado: 'Ese email ya tiene cuenta. Probá entrar.',
    demasiadosIntentos: 'Demasiados intentos. Esperá un minuto.',
    emailSinConfirmar: 'Confirmá tu email desde el correo que te mandamos y después entrá.',
    passwordDebil: 'La contraseña necesita al menos 6 caracteres.',
    sinConexion: 'No pudimos conectar. Tus datos quedan guardados en este dispositivo. Probá de nuevo en unos minutos.',
    generico: 'Algo falló. Tus datos están guardados en este dispositivo. Probá de nuevo.',
  },
};
