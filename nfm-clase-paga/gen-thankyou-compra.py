# -*- coding: utf-8 -*-
"""Genera las dos thank you de COMPRA (a donde Stripe manda después de pagar).

   Salen de la thank you de registro (thankyou-oto.html), así heredan el motor
   de fechas, el deep link de WhatsApp, la hora local y el video. Cambia:
     - sin pop-up de oferta (ya compraron)
     - título y H1 de «pago confirmado»
     - paso 3 → «Tus beneficios, desbloqueados», con el botón al portal
     - evento Purchase del pixel, una vez por sesión

   Entra : nfm-clase-paga/thankyou-oto.html
   Sale  : nfm-clase-paga/thankyou-compra-basic.html    (USD 1)
           nfm-clase-paga/thankyou-compra-premium.html  (USD 5)

   Correr desde la raíz del repo:  python3 nfm-clase-paga/gen-thankyou-compra.py
   En Stripe: cada Payment Link → «Después del pago» → redirigir a la URL de
   su thank you.
"""
import io

BASE = 'nfm-clase-paga/thankyou-oto.html'

TIERS = {
  'basic': {
    'archivo' : 'nfm-clase-paga/thankyou-compra-basic.html',
    'nombre'  : 'Asiento Premium Básico',
    'valor'   : 1,
    'portal'  : 'https://clase-beneficios.netlify.app/asiento-basic',
    'content' : 'asiento_basic',
    'texto'   : 'El <strong>workbook</strong> con el resumen y los accionables, y la <strong>grabación</strong> de la clase. '
                'Van a estar en tu portal el <strong>jueves 8 de octubre a las 12:00 hs (Argentina)</strong>.',
  },
  'premium': {
    'archivo' : 'nfm-clase-paga/thankyou-compra-premium.html',
    'nombre'  : 'Asiento Premium · Hackea tu Productividad',
    'valor'   : 5,
    'portal'  : 'https://clase-beneficios.netlify.app/premium-htc',
    'content' : 'asiento_premium_htc',
    'texto'   : 'El ebook de <strong>Hackea tu Cerebro</strong> y el curso <strong>El ABC del Alto Rendimiento</strong> ya están disponibles. '
                'El workbook y la grabación de la clase, el <strong>jueves 8 de octubre a las 12:00 hs (Argentina)</strong>.',
  },
}

CSS_BEN = """
/* ── PASO 3 · beneficios ── */
.nfm-ben-txt{ font-size:1rem; color:var(--nfm-tl); line-height:1.65; margin:0 !important; text-align:center !important; }
.nfm-ben-txt strong{ color:#fff; font-weight:600; }
.nfm-ben-btn{ display:flex; align-items:center; justify-content:center; gap:12px; width:100%; margin:16px 0 0;
  font-family:var(--nfm-font-h); font-size:1.12rem; font-weight:700; color:#fff; background:var(--nfm-orange);
  border:none; border-radius:50px; padding:19px 28px; cursor:pointer; box-shadow:0 8px 28px var(--nfm-orange-glow);
  transition:transform .25s var(--nfm-ease), box-shadow .25s var(--nfm-ease), background .25s var(--nfm-ease); }
.nfm-ben-btn:hover{ background:var(--nfm-orange-hover); transform:translateY(-2px); box-shadow:0 12px 36px var(--nfm-orange-glow); color:#fff; }
.nfm-ben-btn svg{ width:20px !important; height:20px !important; flex-shrink:0; }
.nfm-ben-micro{ font-size:.82rem; color:var(--nfm-tm); text-align:center !important; margin:12px 0 0 !important; line-height:1.5; }
@media (max-width:600px){ .nfm-ben-btn{ font-size:1rem; padding:17px 22px; } }
"""

def paso3(t):
    return f"""      <!-- PASO 3 — Beneficios -->
      <div class="nfm-step nfm-rv nfm-rv-4">
        <div class="nfm-step__head">
          <div class="nfm-step__num">3</div>
          <h3>Tus beneficios, desbloqueados</h3>
        </div>
        <div class="nfm-step__body">
          <p class="nfm-ben-txt">{t['texto']}</p>
          <a href="{t['portal']}" class="nfm-ben-btn" target="_blank" rel="noopener">
            VER MIS BENEFICIOS
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
          <p class="nfm-ben-micro">Guardá ese link: es tu acceso. Te lo mandamos también por mail.</p>
        </div>
      </div>
"""

def build(t):
    s = io.open(BASE, encoding='utf-8').read()

    def rep(old, new, n=1):
        nonlocal s
        assert s.count(old) == n, f'{s.count(old)}x :: ' + old[:80]
        s = s.replace(old, new)

    # ── título (el estático y el que pone el JS) ──
    rep("<title>¡Lugar reservado! · Neurociencia para el Alto Rendimiento Profesional · Nicolás Fernández Miranda</title>",
        f"<title>¡Pago confirmado! · {t['nombre']} · Nicolás Fernández Miranda</title>")
    rep("    tituloPagina: '¡Lugar reservado! · Neurociencia para el Alto Rendimiento Profesional · Nicolás Fernández Miranda',",
        f"    tituloPagina: '¡Pago confirmado! · {t['nombre']} · Nicolás Fernández Miranda',")

    # ── pixel: Purchase, una vez por sesión (recargar la página no lo duplica) ──
    rep("""  fbq('init', '1203017011123382');
  fbq('track', 'PageView');
}""",
f"""  fbq('init', '1203017011123382');
  fbq('track', 'PageView');
  /* Purchase · USD {t['valor']} · se manda UNA vez por sesión: si recargan, no se cuenta dos veces. */
  var k='nfm_purchase_{t['content']}', ya=false;
  try{{ ya = !!sessionStorage.getItem(k); }}catch(e){{}}
  if(!ya){{ fbq('track','Purchase',{{value:{t['valor']}, currency:'USD', content_name:'{t['content']}'}}); try{{ sessionStorage.setItem(k,'1'); }}catch(e){{}} }}
}}""")

    # ── H1 ──
    rep("""<h1 class="nfm-rv nfm-rv-1">¡Lugar reservado! Ahora, <span class="acc">tres pasos</span> para recibir el acceso.</h1>""",
        """<h1 class="nfm-rv nfm-rv-1">¡Pago confirmado! Ahora, <span class="acc">tres pasos</span> para tener todo listo.</h1>""")

    # ── paso 3 ──
    ini = s.index("      <!-- PASO 3 — Atento al grupo y al mail -->")
    fin = s.index("    </div>\n  </section>\n\n  <!-- FECHA + TÍTULO DE LA CLASE -->")
    s = s[:ini] + paso3(t) + "\n" + s[fin:]

    # ── CSS del paso 3, y fuera el CSS del pop-up ──
    a = s.index("/* ── POPUP POST-REGISTRO · asiento USD 1 / USD 5 (sólo A y B) ── */")
    b = s.index("/* ── BARRA DE MODO PRUEBA ── */")
    s = s[:a] + CSS_BEN.strip() + "\n\n" + s[b:]

    # ── fuera el pop-up entero ──
    a = s.index("<!-- ══════════════════════════════════════════════════════════════════\n     POPUP POST-REGISTRO")
    b = s.index("<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->")
    s = s[:a] + s[b:]

    assert 'nfm-oferta' not in s, 'quedó algo del pop-up'
    io.open(t['archivo'], 'w', encoding='utf-8').write(s)
    print('escrito', t['archivo'], len(s), 'bytes')

for t in TIERS.values():
    build(t)
