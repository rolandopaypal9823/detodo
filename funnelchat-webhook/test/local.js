// Prueba local sin red: ejecuta la función con payloads reales de GHL y de
// Calendly en modo debug y chequea que parsee bien.   →  node test/local.js
import handler from '../netlify/functions/lead.js';

const BASE = 'https://local.test';
let fallos = 0;

async function call(path, body, opts = {}) {
  const req = new Request(BASE + path, {
    method: body ? 'POST' : 'GET',
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  const res = await handler(req);
  return { status: res.status, json: await res.json() };
}

function check(nombre, cond, detalle) {
  console.log((cond ? '  ✓ ' : '  ✗ ') + nombre + (cond ? '' : '   ← ' + JSON.stringify(detalle)));
  if (!cond) fallos++;
}

// 1) Webhook del workflow de GHL (forma típica: contacto plano + customData)
{
  console.log('\n/webinar · payload del workflow de GoHighLevel');
  const { json } = await call('/webinar?debug=1', {
    contact_id: 'abc123',
    first_name: 'Juan',
    last_name: 'Pérez',
    full_name: 'Juan Pérez',
    email: 'Juan@Mail.com',
    phone: '+54 9 11 2345-6789',
    tags: ['clase-sep22', 'webinar'],
    location: { id: 'loc1', name: 'Instituto' },
    customData: {
      etapa: 'A', equipo: 'B', nivel: 'alto', califica: 'si',
      dedicacion: 'Dirijo una pyme', clase_fecha: '2026-09-22',
      edicion: 'clase-sep22-alto-rendimiento', utm_source: 'ig',
    },
  });
  const p = json.payload;
  check('flujo = webinar', json.flujo === 'webinar', json);
  check('telefono normalizado', p.telefono === '+5491123456789', p.telefono);
  check('telefono_sin_plus', p.telefono_sin_plus === '5491123456789', p.telefono_sin_plus);
  check('primer_nombre', p.primer_nombre === 'Juan', p.primer_nombre);
  check('email en minúsculas', p.email === 'juan@mail.com', p.email);
  check('clase_texto', p.clase_texto === 'martes 22 de septiembre', p.clase_texto);
  check('quiz (customData aplanado)', p.etapa === 'A' && p.nivel === 'alto' && p.califica === 'si', p);
  check('ghl_contact_id', p.ghl_contact_id === 'abc123', p.ghl_contact_id);
  check('origen', p.origen === 'webinar-registro', p.origen);
}

// 2) GHL con el teléfono sin + y "Phone" con mayúscula, sin quiz
{
  console.log('\n/webinar · teléfono sin + y claves con mayúscula');
  const { json } = await call('/webinar?debug=1', { 'Full Name': 'x', full_name: 'Ana López', Email: 'ana@x.com', Phone: '5491155556666' });
  const p = json.payload;
  check('telefono', p.telefono === '5491155556666', p.telefono);
  check('nombre', p.nombre === 'Ana López', p.nombre);
  check('califica por defecto = si', p.califica === 'si', p.califica);
}

// 3) Etapa C sin califica explícito → califica=no
{
  console.log('\n/webinar · etapa C');
  const { json } = await call('/webinar?debug=1', { first_name: 'Leo', phone: '+5491100000001', etapa: 'C' });
  check('califica = no', json.payload.califica === 'no', json.payload.califica);
}

// 4) Token
{
  console.log('\n/webinar · token');
  process.env.WEBINAR_TOKEN = 'secreto';
  const sin = await call('/webinar?debug=1', { phone: '+5491100000001' });
  check('sin token → 401', sin.status === 401, sin);
  const conQuery = await call('/webinar?debug=1&token=secreto', { phone: '+5491100000001' });
  check('con ?token= → 200', conQuery.status === 200, conQuery);
  const conHeader = await call('/webinar?debug=1', { phone: '+5491100000001' }, { headers: { 'x-nfm-token': 'secreto' } });
  check('con header → 200', conHeader.status === 200, conHeader);
  delete process.env.WEBINAR_TOKEN;
}

// 5) Sin teléfono → no manda, responde 200 para que GHL no reintente
{
  console.log('\n/webinar · sin teléfono');
  process.env.FUNNELCHAT_WEBHOOK_URL_WEBINAR = 'https://example.invalid/hook';
  const r = await call('/webinar', { first_name: 'Sin', email: 'sin@tel.com' });
  check('skipped, status 200', r.status === 200 && r.json.skipped === true, r);
  delete process.env.FUNNELCHAT_WEBHOOK_URL_WEBINAR;
}

// 6) Sin variable de entorno → 500 claro
{
  console.log('\n/webinar · sin FUNNELCHAT_WEBHOOK_URL_WEBINAR');
  const r = await call('/webinar', { phone: '+5491100000001' });
  check('500 con el nombre de la variable', r.status === 500 && /WEBINAR/.test(r.json.error), r);
}

// 7) /lead sigue igual que siempre (Calendly)
{
  console.log('\n/lead · params de Calendly (sin cambios)');
  const { json } = await call('/lead?debug=1&invitee_first_name=Juan&invitee_last_name=Perez&invitee_email=juan@mail.com&answer_1=%2B5491123456789&event_start_time=2026-08-24T09:20:00-04:00&assigned_to=Valent%C3%ADn%20Borja');
  const p = json.payload;
  check('flujo = agenda', json.flujo === 'agenda', json);
  check('nombre armado con first+last', p.nombre === 'Juan Perez', p.nombre);
  check('telefono', p.telefono === '+5491123456789', p.telefono);
  check('cita_texto', p.cita_texto === 'lunes 24 de agosto, 09:20 h', p.cita_texto);
  check('asesor_nombre', p.asesor_nombre === 'Valentín', p.asesor_nombre);
  check('link_autodiagnostico', p.link_autodiagnostico === 'https://test-presesion.netlify.app/?asignado=Valent%C3%ADn&nombre=Juan', p.link_autodiagnostico);
  check('origen', p.origen === 'thx-page', p.origen);
}

// 8) Flujo real: la función reenvía a FunnelChat (fetch simulado)
{
  console.log('\n/webinar · reenvío a FunnelChat (fetch simulado)');
  process.env.FUNNELCHAT_WEBHOOK_URL_WEBINAR = 'https://hooks.funnelchat.test/abc';
  process.env.WEBINAR_GRUPO_WHATSAPP = 'https://chat.whatsapp.com/XYZ';
  const realFetch = globalThis.fetch;
  let capturado = null;
  globalThis.fetch = async (url, init) => { capturado = { url, body: JSON.parse(init.body) }; return new Response('ok', { status: 200 }); };
  const r = await call('/webinar', { first_name: 'Juan', phone: '+5491123456789', clase_fecha: '2026-09-22' });
  globalThis.fetch = realFetch;
  check('respuesta ok', r.status === 200 && r.json.ok === true && r.json.funnelchat_status === 200, r);
  check('fue al webhook del webinar', capturado && capturado.url === 'https://hooks.funnelchat.test/abc', capturado && capturado.url);
  check('payload con grupo y primer_nombre', capturado && capturado.body.grupo_whatsapp === 'https://chat.whatsapp.com/XYZ' && capturado.body.primer_nombre === 'Juan', capturado && capturado.body);
  delete process.env.FUNNELCHAT_WEBHOOK_URL_WEBINAR;
  delete process.env.WEBINAR_GRUPO_WHATSAPP;
}

console.log(fallos ? `\n✗ ${fallos} chequeo(s) fallaron` : '\n✓ todo OK');
process.exit(fallos ? 1 : 0);
