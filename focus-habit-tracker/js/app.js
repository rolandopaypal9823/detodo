// ============================================================
// app.js — router por hash + vistas + interacción
// ============================================================

import { supabaseEnabled } from './config.js';
import * as store from './store.js';
import { COPY } from './copy.js';

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const esc = (s = '') => s.replace(/[&<>"']/g, (c) => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
));

const MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
  'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
const DOW = ['D', 'L', 'M', 'X', 'J', 'V', 'S'];

const CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke="currentColor"><path d="M4.5 12.5l5 5 10-11"/></svg>';

// hábitos sugeridos — del método NFM (Focus Habit Tracker)
const SUGGESTIONS = [
  { name: 'Foco profundo (2 hs)', meta: 20 },
  { name: 'Celular con tope (1,5 hs)', meta: 20 },
  { name: 'Horas en tu meta / proyecto', meta: 20 },
  { name: 'Dormir 7,5 hs', meta: 25 },
  { name: 'Movimiento / ejercicio', meta: 15 },
  { name: 'Presencia real (sin celular)', meta: 20 },
  { name: 'Journaling / gratitud', meta: 25 },
  { name: 'Planificación AM o PM', meta: 25 },
  { name: 'Lectura / formación', meta: 20 },
];

const GOAL_FIELDS = [
  { key: 'meta', label: 'TU META (QUÉ + PARA CUÁNDO)', ph: 'Ej: Terminar mi segundo libro antes de diciembre 2026', optional: false },
  { key: 'porque', label: '¿PARA QUÉ LA QUERÉS? ¿QUÉ CAMBIA?', ph: 'Una frase: qué cambia en tu vida', optional: false },
  { key: 'horas', label: '¿CUÁNTAS HORAS DE FOCO NECESITA?', ph: 'Estimá el total de horas', optional: false },
  { key: 'pateando', label: '¿HACE CUÁNTO LA VENÍS PATEANDO?', ph: 'Meses / años', optional: true },
  { key: 'costo', label: '¿QUÉ TE CUESTA NO LOGRARLA?', ph: 'En plata, oportunidades, vínculos', optional: true },
  { key: 'quien', label: '¿QUIÉN MÁS GANA CUANDO LO LOGRES?', ph: 'Familia, equipo, hijos', optional: true },
];

// mes visible en el panel
let view = { y: new Date().getFullYear(), m: new Date().getMonth() };
let editingHabitId = null;

// ============================================================
// ARRANQUE
// ============================================================

async function boot() {
  if (supabaseEnabled()) {
    const user = await store.initSupabase().catch(() => null);
    if (!user) { showAuth('remote'); return; }
  } else {
    store.getState(); // noop
  }
  await store.initStore();
  if (!supabaseEnabled() && !store.getState().profile.name) { showAuth('local'); return; }
  showApp();
}

function showAuth(mode) {
  $('#screen-auth').hidden = false;
  $('#app').hidden = true;
  $('#auth-form').hidden = mode !== 'remote';
  $('#local-form').hidden = mode !== 'local';
  if (mode === 'local') { store.initStore(); }
}

function showApp() {
  $('#screen-auth').hidden = true;
  $('#app').hidden = false;
  renderChrome();
  route();
}

// ============================================================
// AUTH
// ============================================================

$('#local-form').addEventListener('submit', (e) => {
  e.preventDefault();
  store.setName($('#local-name').value);
  showApp();
});

$('#auth-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  await authAction(() => store.signIn($('#auth-email').value, $('#auth-pass').value));
});

$('#btn-signup').addEventListener('click', async () => {
  const email = $('#auth-email').value, pass = $('#auth-pass').value;
  if (!email || pass.length < 6) { authError('Completá email y una contraseña de 6+ caracteres.'); return; }
  await authAction(async () => {
    const hasSession = await store.signUp(email, pass);
    if (!hasSession) throw new Error('Revisá tu email para confirmar la cuenta y después entrá.');
  });
});

async function authAction(fn) {
  authError('');
  try {
    await fn();
    await store.initStore();
    if (!store.getState().profile.name) {
      // sin prompt() nativo: arranca con el prefijo del email, editable en la barra
      const email = store.getUser()?.email || '';
      const guess = email.split('@')[0].replace(/[._-]+/g, ' ').trim();
      if (guess) store.setName(guess[0].toUpperCase() + guess.slice(1));
    }
    showApp();
  } catch (err) {
    authError(traducirError(err.message || 'No pudimos entrar. Probá de nuevo.'));
  }
}

function authError(msg) {
  const el = $('#auth-error');
  el.hidden = !msg;
  el.textContent = msg;
}

function traducirError(msg) {
  if (/invalid login credentials/i.test(msg)) return COPY.errores.credenciales;
  if (/already registered/i.test(msg)) return COPY.errores.yaRegistrado;
  if (/rate limit/i.test(msg)) return COPY.errores.demasiadosIntentos;
  if (/email not confirmed/i.test(msg)) return COPY.errores.emailSinConfirmar;
  if (/password.*(short|weak|at least)/i.test(msg)) return COPY.errores.passwordDebil;
  if (/failed to fetch|network|fetch failed|load failed/i.test(msg)) return COPY.errores.sinConexion;
  if (/revisá tu email/i.test(msg)) return msg; // mensaje propio de signUp
  return COPY.errores.generico;
}

$('#btn-logout').addEventListener('click', async () => {
  await store.signOut();
  if (supabaseEnabled()) { location.reload(); }
});

// ============================================================
// CHROME (sidebar / tabbar / usuario)
// ============================================================

function renderChrome() {
  const now = new Date();
  $('#sidebar-date').textContent =
    `${now.getDate()} DE ${MONTHS[now.getMonth()].toUpperCase()}, ${now.getFullYear()}`;
  const name = store.getState().profile.name || '—';
  $('#user-name').textContent = name;
  $('#user-avatar').textContent = (name[0] || '·').toUpperCase();
  $('#user-mode').textContent = store.isRemote()
    ? (store.getUser()?.email || 'CUENTA').toUpperCase().slice(0, 22)
    : 'MODO LOCAL';
  $('#btn-logout').hidden = !store.isRemote();
}

$('#user-name').addEventListener('click', () => {
  const btn = $('#user-name');
  if (btn.dataset.editing) return;
  btn.dataset.editing = '1';
  const input = document.createElement('input');
  input.className = 'user-name-input';
  input.maxLength = 30;
  input.value = store.getState().profile.name;
  btn.replaceWith(input);
  input.focus();
  input.select();
  const commit = () => {
    if (input.value.trim()) store.setName(input.value);
    delete btn.dataset.editing;
    input.replaceWith(btn);
    renderChrome();
    route();
  };
  input.addEventListener('blur', commit);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') input.blur();
    if (e.key === 'Escape') { input.value = store.getState().profile.name; input.blur(); }
  });
});

// ============================================================
// ROUTER
// ============================================================

const routes = { inicio: renderInicio, habitos: renderHabitos, objetivos: renderObjetivos };

function currentRoute() {
  const r = location.hash.replace('#/', '');
  return routes[r] ? r : 'inicio';
}

function route() {
  lastRenderDay = store.todayKey();
  // si pasó la medianoche (o volvés de días sin abrir), reconciliar congeladores
  if (store.getState().habits.length) {
    const spent = store.reconcileFreezes();
    if (spent) renderChrome();
  }
  const r = currentRoute();
  $$('[data-nav]').forEach((a) => a.classList.toggle('active', a.dataset.nav === r));
  routes[r]();
  $('#main').scrollTop = 0;
  window.scrollTo(0, 0);
}

window.addEventListener('hashchange', route);

// cambio de día con la app abierta: al volver del background (PWA) o
// cruzar medianoche, re-renderizar para que "hoy" sea hoy de verdad.
let lastRenderDay = store.todayKey();
function checkDayChange() {
  if (store.todayKey() !== lastRenderDay && !$('#app').hidden) route();
}
document.addEventListener('visibilitychange', checkDayChange);
window.addEventListener('focus', checkDayChange);
setInterval(checkDayChange, 60 * 1000);

// re-render de la vista activa cuando cambia el estado (sync remoto, etc.)
store.onChange(() => { if (!$('#app').hidden) renderChrome(); });

// ============================================================
// VISTA: INICIO
// ============================================================

function saludo() {
  const h = new Date().getHours();
  if (h < 13) return 'Buenos días';
  if (h < 20) return 'Buenas tardes';
  return 'Buenas noches';
}

function renderInicio() {
  const s = store.getState();
  const today = store.todayProgress();
  const racha = store.streak();

  const steps = [
    { label: 'Definí tus hábitos', go: 'Ir a definir tus hábitos', action: 'open-habits', done: s.habits.length > 0 },
    { label: 'Marcá tu primer día en el panel', go: 'Ir al panel de hábitos', href: '#/habitos', done: Object.values(s.checks).some((m) => Object.keys(m).length) },
    { label: 'Escribí tus objetivos', go: 'Ir a objetivos', href: '#/objetivos', done: s.goals.some((g) => g?.meta?.trim()) },
  ];
  const allDone = steps.every((x) => x.done);
  const showSteps = !s.ui.stepsDismissed && !allDone;

  $('#main').innerHTML = `
    <header class="view-head">
      <div class="mono-label view-kicker">TU CENTRO DE CONTROL DIARIO</div>
      <h1 class="view-title">${saludo()}, ${esc(s.profile.name || 'crack')}.</h1>
    </header>

    ${showSteps ? `
    <section class="card steps-card">
      <div class="steps-head">
        <div>
          <h2 class="section-title">Tus primeros pasos</h2>
          <p class="steps-copy">No hace falta hacer todo hoy. Arrancá por lo que sientas más importante y seguí con el resto.</p>
        </div>
        <button type="button" class="btn-dismiss" data-dismiss-steps aria-label="Ocultar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>
        </button>
      </div>
      <div class="steps-list">
        ${steps.map((st) => `
          <div class="step ${st.done ? 'done' : ''}">
            <span class="step-check">${CHECK_SVG}</span>
            <span class="step-label">${st.label}</span>
            ${st.done ? '' : (st.action
              ? `<button type="button" class="step-go" data-action="${st.action}">${st.go} →</button>`
              : `<a class="step-go" href="${st.href}">${st.go} →</a>`)}
          </div>`).join('')}
      </div>
    </section>` : ''}

    ${renderNudge(s, today, racha)}

    <div class="stat-row">
      <div class="card stat-card">
        <span class="stat-num ${racha > 0 ? 'hot' : ''}">${racha}</span>
        <div class="stat-meta">
          <span class="mono-label">RACHA DE DÍAS</span>
          ${renderFreezes(s)}
          ${renderRachaState(s, today, racha)}
          ${renderMilestone(racha)}
        </div>
      </div>
      <div class="card stat-card">
        <span class="stat-num">${today.done}<span style="font-size:0.55em;color:var(--ink-faint)">/${today.total}</span></span>
        <div class="stat-meta">
          <span class="mono-label">HÁBITOS DE HOY</span>
        </div>
      </div>
    </div>

    <section>
      <div class="today-head">
        <h2 class="section-title">Hábitos de hoy</h2>
        ${today.total && today.done === today.total
          ? `<span class="perfect-inline">${COPY.diaPerfecto(today.total)}</span>`
          : today.total ? `<span class="today-pct">${today.pct}%</span>` : ''}
      </div>
      ${s.habits.length ? `
        <div class="today-list">
          ${s.habits.map((h) => {
            const checked = store.isChecked(h.id, store.todayKey());
            return `
            <button type="button" class="today-item ${checked ? 'checked' : ''}" data-toggle="${h.id}" aria-pressed="${checked}">
              <span class="check-circle">${CHECK_SVG}</span>
              <span class="habit-title">${esc(h.name)}</span>
            </button>`;
          }).join('')}
        </div>
        <p class="grid-hint" style="margin-top:12px">Marcás el día en el que estás. Mañana, el panel arranca de nuevo.</p>
      ` : `
        <div class="empty">
          <div class="empty-title">${COPY.vacios.inicioTitulo}</div>
          <div>${COPY.vacios.inicioSub}</div>
          <button type="button" class="btn btn-primary" data-action="open-habits">${COPY.vacios.inicioCta}</button>
        </div>`}
    </section>
  `;
  bindCommon();
}

// congeladores: escasos y visibles — ◆ lleno = disponible
function renderFreezes(s) {
  const f = s.freezes;
  const pips = [0, 1].map((i) => `<span class="pip ${i < f.available ? 'full' : ''}">◆</span>`).join('');
  return `<span class="freeze-row" title="Congelador de racha: si te salteás un día, se usa solo y tu racha sigue. Ganás 1 cada 7 días de racha (máximo 2).">${pips}<span class="freeze-label">${f.available === 1 ? 'CONGELADOR' : 'CONGELADORES'}</span></span>`;
}

// máquina de estados de la card de racha (loss-aversion: marco de pérdida
// para retener, marco de ganancia para arrancar; candor: el dato, no el carácter)
function renderRachaState(s, today, racha) {
  let line = '';
  let hot = false;
  if (racha === 0) {
    const best = store.bestStreak();
    line = best > 0 ? COPY.racha.resetAntiCulpa(best) : COPY.racha.nuevo;
  } else if (today.done === 0 && racha >= 3) {
    line = COPY.racha.enJuego(racha);
    hot = true;
  } else if (today.total > 0 && today.done === today.total) {
    line = COPY.racha.completo(today.total);
  } else if (today.done >= 1) {
    line = COPY.racha.asegurado;
  }
  return line ? `<span class="racha-state ${hot ? 'hot' : ''}">${line}</span>` : '';
}

// anticipación del próximo hito (celebration-moments: ver venir "el grande")
function renderMilestone(racha) {
  const next = store.nextMilestone(racha);
  if (!next || racha === 0) return '';
  const prev = store.prevMilestone(racha);
  const pct = Math.round(((racha - prev) / (next - prev)) * 100);
  const label = next - racha === 1 ? COPY.racha.vispera(next) : `HITO ${next} · FALTAN ${next - racha} DÍAS`;
  return `
    <span class="milestone-row">
      <span class="milestone-bar"><i style="width:${pct}%"></i></span>
      <span class="milestone-label">${label}</span>
    </span>`;
}

// avisos de inicio: un congelador te salvó / tu racha se define hoy
function renderNudge(s, today, racha) {
  const notices = [];
  if (s.ui.freezeNoticeDay === store.todayKey()) {
    notices.push(`<div class="notice"><span class="notice-dot" aria-hidden="true">◆</span>
      <span>${COPY.avisos.congeladorUsado(s.freezes.available)}</span></div>`);
  }
  // congelador ganado hoy: se anuncia acá aunque no haya hito
  // (en rachas 14, 21... se gana sin modal — que no sea en silencio)
  if (s.freezes.lastEarnDay === store.todayKey()) {
    notices.push(`<div class="notice"><span class="notice-dot" aria-hidden="true">◆</span>
      <span>${COPY.avisos.congeladorGanado(s.freezes.available)}</span></div>`);
  }
  const evening = new Date().getHours() >= 19;
  if (evening && s.habits.length && today.done === 0) {
    const msg = racha > 0 ? COPY.avisos.rachaEnJuego(racha) : COPY.avisos.cerraElDia;
    notices.push(`<div class="notice notice-hot"><span class="notice-dot" aria-hidden="true">⚡</span><span>${msg}</span></div>`);
  }
  return notices.join('');
}

// ============================================================
// CELEBRACIONES — 3 niveles (juicy-feedback / día perfecto / hito)
// El nivel chico es CSS puro en el check; acá van los dos grandes.
// ============================================================

// Tiering (celebration-moments): chico = CSS del check · medio = línea
// inline "DÍA PERFECTO" · grande = modal SOLO en hitos; 100/365 más largos.
function showCelebration(ev) {
  if (!ev.milestone) return; // el modal es solo para hitos
  const cel = $('#celebration');
  const c = COPY.hitos[ev.milestone];
  $('#cel-num').textContent = ev.milestone;
  $('#cel-title').textContent = c.title;
  $('#cel-sub').textContent = c.sub;
  const extra = $('#cel-extra');
  extra.hidden = !ev.earnedFreeze;
  if (ev.earnedFreeze) extra.textContent = COPY.congeladorGanado;
  cel.hidden = false;
  const box = $('.celebration', cel);
  box.classList.toggle('grand', ev.milestone >= 100); // hold y burst extendidos
  box.classList.remove('play');
  void box.offsetWidth;
  box.classList.add('play');
  $('#cel-close').focus();
}

function hideCelebration() {
  $('#celebration').hidden = true;
  // devolver el foco a la vista (el botón original ya fue re-renderizado)
  const target = $('[data-toggle]') || $('#main');
  if (target) target.focus();
}

$('#cel-close').addEventListener('click', hideCelebration);
$('#celebration').addEventListener('click', (e) => { if (e.target === $('#celebration')) hideCelebration(); });

// ============================================================
// VISTA: PANEL DE HÁBITOS
// ============================================================

function renderHabitos() {
  const s = store.getState();
  const now = new Date();
  const isCurrentMonth = view.y === now.getFullYear() && view.m === now.getMonth();
  const stats = store.monthStats(view.y, view.m);
  const keys = store.monthKeys(view.y, view.m);
  const todayK = store.todayKey();

  const R = 46, C = 2 * Math.PI * R;
  const dash = C - (C * stats.pct) / 100;

  const ranking = [...stats.perHabit].sort((a, b) => b.pct - a.pct).slice(0, 3);

  $('#main').innerHTML = `
    <header class="view-head">
      <div class="mono-label view-kicker">SEGUÍ TU CONSTANCIA, DÍA POR DÍA</div>
      <h1 class="view-title">Panel de hábitos</h1>
    </header>

    <div class="panel-toolbar">
      <div class="month-nav">
        <button type="button" data-month="-1" aria-label="Mes anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>
        <span class="month-label">${MONTHS[view.m]} ${view.y}</span>
        <button type="button" data-month="1" aria-label="Mes siguiente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <button type="button" class="btn btn-primary" data-action="open-habits">Gestionar hábitos</button>
    </div>

    ${renderMonthClose()}

    ${s.habits.length ? `
    <section class="card panel-summary">
      <div class="ring-wrap">
        <svg width="108" height="108" viewBox="0 0 108 108">
          <circle class="ring-bg" cx="54" cy="54" r="${R}" fill="none" stroke-width="9"/>
          <circle class="ring-fg" cx="54" cy="54" r="${R}" fill="none" stroke-width="9" stroke-linecap="round"
            stroke-dasharray="${C.toFixed(1)}" stroke-dashoffset="${dash.toFixed(1)}"/>
        </svg>
        <span class="ring-num">${stats.pct}%</span>
      </div>
      <div class="summary-stats">
        <div class="sum-item"><span class="summary-num">${stats.done}</span><span class="mono-label">COMPLETADOS</span></div>
        <div class="sum-item"><span class="summary-num">${stats.remaining}</span><span class="mono-label">RESTANTES</span></div>
        <div class="sum-item"><span class="summary-num">${stats.days}</span><span class="mono-label">DÍAS DEL MES</span></div>
        <div class="sum-item"><span class="summary-num">${store.totalActiveDays()}</span><span class="mono-label">CONSTANCIA TOTAL</span></div>
      </div>
    </section>

    <section class="card grid-card">
      <div class="grid-head">
        <h2 class="section-title">Mes completo</h2>
        <span class="grid-hint">Marcás solo el día en el que estás. El pasado no se edita.</span>
      </div>
      <div class="grid-scroll">
      <table class="habit-grid">
        <thead>
          <tr>
            <th class="hg-name"></th><th class="hg-meta">META</th>
            ${keys.map((k) => `<th class="hg-dow">${DOW[new Date(k + 'T12:00:00').getDay()]}</th>`).join('')}
            <th></th>
          </tr>
          <tr>
            <th class="hg-name"></th><th class="hg-meta"></th>
            ${keys.map((k, i) => `<th class="hg-day ${k === todayK ? 'today' : ''}">${i + 1}</th>`).join('')}
            <th></th>
          </tr>
        </thead>
        <tbody>
          ${stats.perHabit.map(({ habit, done, meta }) => `
          <tr>
            <td class="hg-name" title="${esc(habit.name)}">${esc(habit.name)}</td>
            <td class="hg-meta">${meta}</td>
            ${keys.map((k) => {
              const dow = new Date(k + 'T12:00:00').getDay();
              const checked = store.isChecked(habit.id, k);
              const frozen = !checked && Boolean(s.freezes.used[k]);
              const editable = k === todayK;
              const cls = ['cell', checked ? 'checked' : '', k === todayK ? 'today' : '',
                frozen ? 'frozen' : '',
                (dow === 0 || dow === 6) ? 'weekend' : '', editable ? 'editable' : ''].join(' ');
              return `<td>${editable
                ? `<button type="button" class="${cls}" data-toggle="${habit.id}" aria-pressed="${checked}" title="${esc(habit.name)} · hoy"></button>`
                : `<span class="${cls}" ${frozen ? 'title="Día cubierto por un congelador de racha"' : ''}></span>`}</td>`;
            }).join('')}
            <td class="hg-count"><span class="${done >= meta ? 'met' : ''}">${done}</span>/${meta}</td>
          </tr>`).join('')}
        </tbody>
      </table>
      </div>
    </section>

    ${stats.perHabit.length > 1 ? `
    <section class="card rank-card">
      <h2 class="section-title">Tus mejores hábitos de ${MONTHS[view.m].toLowerCase()}</h2>
      <div class="rank-list">
        ${ranking.map((r, i) => `
        <div class="rank-item">
          <span class="rank-pos">${i + 1}.</span>
          <span class="rank-name">${esc(r.habit.name)}</span>
          <span class="rank-pct">${i === 0 && r.pct > 0 ? '★ ' : ''}${Math.min(r.pct, 100)}%</span>
          <span class="rank-bar"><i style="width:${Math.min(r.pct, 100)}%"></i></span>
        </div>`).join('')}
      </div>
    </section>` : ''}
    ` : `
    <div class="empty">
      <div class="empty-title">${COPY.vacios.panelTitulo}</div>
      <div>${COPY.vacios.panelSub}</div>
      <button type="button" class="btn btn-primary" data-action="open-habits">${COPY.vacios.panelCta}</button>
    </div>`}
  `;

  // que el día de hoy quede a la vista en pantallas angostas
  const gridScroll = $('.grid-scroll');
  const todayHead = $('.hg-day.today');
  if (gridScroll && todayHead) {
    gridScroll.scrollLeft = Math.max(0, todayHead.offsetLeft - gridScroll.clientWidth * 0.6);
  }

  $$('[data-close-action]').forEach((b) => b.addEventListener('click', () => {
    store.decideMonthClose(b.dataset.closeMonth, b.dataset.habit, b.dataset.closeAction);
    renderHabitos();
  }));

  $$('[data-month]').forEach((b) => b.addEventListener('click', () => {
    const d = new Date(view.y, view.m + Number(b.dataset.month), 1);
    view = { y: d.getFullYear(), m: d.getMonth() };
    renderHabitos();
  }));
  // volver al mes actual si quedó en otro y no es navegación explícita
  if (!isCurrentMonth) { /* se queda donde el usuario navegó */ }
  bindCommon();
}

// Cierre de mes (green-machine paso 6: duplicá lo que funciona, cortá lo
// que no). Solo aparece si hay veredictos pendientes; banda media = silencio.
function renderMonthClose() {
  const report = store.monthCloseReport();
  if (!report) return '';
  const mesNombre = MONTHS[report.month.m];
  return `
  <section class="card close-card">
    <div class="mono-label">${COPY.cierre.titulo(mesNombre).toUpperCase()}</div>
    <p class="close-intro">${COPY.cierre.intro}</p>
    ${report.flagged.map(({ habit, done, pct, verdict }) => `
    <div class="close-row">
      <div class="close-info">
        <span class="close-name">${esc(habit.name)}</span>
        <span class="close-pct ${verdict === 'raise' ? 'good' : 'bad'}">${done}/${habit.meta} · ${pct}%</span>
        <span class="close-verdict">${verdict === 'raise' ? COPY.cierre.subiLaVara : COPY.cierre.teAplasta}</span>
      </div>
      <div class="close-actions">
        ${verdict === 'raise'
          ? `<button type="button" class="btn-mini" data-close-action="raise" data-close-month="${report.month.key}" data-habit="${habit.id}">${COPY.cierre.subir(Math.min(31, Math.round(habit.meta * 1.2) || habit.meta + 2))}</button>`
          : `<button type="button" class="btn-mini" data-close-action="lower" data-close-month="${report.month.key}" data-habit="${habit.id}">${COPY.cierre.bajar(Math.max(1, Math.round(habit.meta * 0.8)))}</button>
             <button type="button" class="btn-mini danger" data-close-action="delete" data-close-month="${report.month.key}" data-habit="${habit.id}">${COPY.cierre.eliminar}</button>`}
        <button type="button" class="btn-mini ghost" data-close-action="keep" data-close-month="${report.month.key}" data-habit="${habit.id}">${COPY.cierre.mantener}</button>
      </div>
    </div>`).join('')}
  </section>`;
}

// ============================================================
// VISTA: OBJETIVOS
// ============================================================

function renderObjetivos() {
  const s = store.getState();
  $('#main').innerHTML = `
    <header class="view-head">
      <div class="mono-label view-kicker">HASTA 3 METAS. CONCRETAS.</div>
      <h1 class="view-title">Objetivos y metas</h1>
      <p class="view-sub goals-intro">Escribí metas concretas y con fecha. Cuanto más claras, más te empuja el sistema.
      Evitá lo vago: «ganar más», «estar mejor». Mejor: «Lanzar mi curso online en marzo».</p>
    </header>
    ${[0, 1, 2].map((i) => {
      const g = s.goals[i] || {};
      const hasOptional = GOAL_FIELDS.some((f) => f.optional && g[f.key]?.trim());
      return `
      <section class="card goal-card" data-goal="${i}">
        <div class="goal-head">
          <span class="mono-label">META ${i + 1}</span>
          <span class="save-hint" data-save-hint>GUARDADO ✓</span>
        </div>
        <div class="goal-fields">
          ${GOAL_FIELDS.filter((f) => !f.optional).map((f) => `
          <label class="field">
            <span class="field-label">${f.label}</span>
            <textarea rows="1" data-field="${f.key}" placeholder="${f.ph}">${esc(g[f.key] || '')}</textarea>
          </label>`).join('')}
          <button type="button" class="goal-more" data-more ${hasOptional ? 'hidden' : ''}>+ Profundizar (potencia tu insight)</button>
          <div class="goal-optional" ${hasOptional ? '' : 'hidden'}>
            ${GOAL_FIELDS.filter((f) => f.optional).map((f) => `
            <label class="field">
              <span class="field-label">${f.label} <span style="letter-spacing:0.1em">· OPCIONAL</span></span>
              <textarea rows="1" data-field="${f.key}" placeholder="${f.ph}">${esc(g[f.key] || '')}</textarea>
            </label>`).join('')}
          </div>
        </div>
      </section>`;
    }).join('')}
  `;

  $$('.goal-card').forEach((card) => {
    const idx = Number(card.dataset.goal);
    const hint = $('[data-save-hint]', card);
    let hintTimer = null;
    $$('textarea', card).forEach((ta) => {
      autoGrow(ta);
      ta.addEventListener('input', () => {
        autoGrow(ta);
        store.setGoalField(idx, ta.dataset.field, ta.value);
        hint.classList.add('visible');
        clearTimeout(hintTimer);
        hintTimer = setTimeout(() => hint.classList.remove('visible'), 1600);
      });
    });
    const more = $('[data-more]', card);
    more.addEventListener('click', () => {
      more.hidden = true;
      $('.goal-optional', card).hidden = false;
    });
  });
  bindCommon();
}

function autoGrow(ta) {
  ta.style.height = 'auto';
  ta.style.height = `${Math.max(44, ta.scrollHeight)}px`;
}

// ============================================================
// MODAL GESTIONAR HÁBITOS
// ============================================================

const modal = $('#modal-habits');

function openHabitsModal() {
  editingHabitId = null;
  $('#habit-form').reset();
  $('#habit-meta').value = 24;
  $('#habit-submit').textContent = 'Crear hábito';
  renderModalList();
  modal.hidden = false;
  $('#habit-name').focus();
}

function closeHabitsModal() {
  modal.hidden = true;
  route(); // refrescar la vista de fondo
}

function renderModalList() {
  const s = store.getState();
  const list = $('#habit-list');
  list.innerHTML = s.habits.map((h) => `
    <li>
      <span class="habit-title">${esc(h.name)}</span>
      <span class="habit-goal">META ${h.meta}</span>
      <button type="button" class="icon-btn" data-edit="${h.id}" aria-label="Editar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
      </button>
      <button type="button" class="icon-btn danger" data-del="${h.id}" aria-label="Eliminar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/></svg>
      </button>
    </li>`).join('');

  // sugerencias del método NFM (solo las que no agregaste todavía)
  const taken = new Set(s.habits.map((h) => h.name.toLowerCase()));
  const sugs = SUGGESTIONS.filter((x) => !taken.has(x.name.toLowerCase()));
  $('#habit-suggestions').innerHTML = s.habits.length >= 4 || !sugs.length ? '' : `
    <span class="mono-label sug-label">SUGERIDOS DEL MÉTODO NFM</span>
    ${sugs.slice(0, 5).map((x, i) => `<button type="button" class="sug-chip" data-sug="${i}">${esc(x.name)}</button>`).join('')}
  `;
  $$('[data-sug]').forEach((b) => b.addEventListener('click', () => {
    const sug = sugs[Number(b.dataset.sug)];
    store.addHabit(sug.name, sug.meta);
    renderModalList();
  }));

  $$('[data-edit]', list).forEach((b) => b.addEventListener('click', () => {
    const h = s.habits.find((x) => x.id === b.dataset.edit);
    editingHabitId = h.id;
    $('#habit-name').value = h.name;
    $('#habit-meta').value = h.meta;
    $('#habit-submit').textContent = 'Guardar cambios';
    $('#habit-name').focus();
  }));

  $$('[data-del]', list).forEach((b) => b.addEventListener('click', () => {
    const h = s.habits.find((x) => x.id === b.dataset.del);
    if (confirm(`¿Eliminar «${h.name}»? Se pierde su historial de marcas.`)) {
      store.deleteHabit(h.id);
      if (editingHabitId === h.id) { editingHabitId = null; $('#habit-form').reset(); $('#habit-meta').value = 24; $('#habit-submit').textContent = 'Crear hábito'; }
      renderModalList();
    }
  }));
}

$('#habit-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const name = $('#habit-name').value.trim();
  const meta = Math.min(31, Math.max(1, Number($('#habit-meta').value) || 24));
  if (!name) return;
  if (editingHabitId) store.updateHabit(editingHabitId, name, meta);
  else store.addHabit(name, meta);
  editingHabitId = null;
  $('#habit-form').reset();
  $('#habit-meta').value = 24;
  $('#habit-submit').textContent = 'Crear hábito';
  renderModalList();
  $('#habit-name').focus();
});

modal.addEventListener('click', (e) => {
  if (e.target === modal || e.target.closest('[data-close]')) closeHabitsModal();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modal.hidden) closeHabitsModal();
  if (e.key === 'Escape' && !$('#celebration').hidden) hideCelebration();
  // trap de foco: el diálogo de celebración tiene un solo control
  if (e.key === 'Tab' && !$('#celebration').hidden) {
    e.preventDefault();
    $('#cel-close').focus();
  }
});

// ============================================================
// BINDINGS COMUNES
// ============================================================

function bindCommon() {
  $$('[data-action="open-habits"]').forEach((b) => b.addEventListener('click', openHabitsModal));
  $$('[data-toggle]').forEach((b) => b.addEventListener('click', () => {
    const ev = store.toggleToday(b.dataset.toggle);
    route();
    if (ev.milestone) showCelebration(ev);
  }));
  const dismiss = $('[data-dismiss-steps]');
  if (dismiss) dismiss.addEventListener('click', () => { store.dismissSteps(); route(); });
}

// ============================================================
// PWA
// ============================================================

if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => { /* sin SW, la app sigue */ });
  });
}

boot();
