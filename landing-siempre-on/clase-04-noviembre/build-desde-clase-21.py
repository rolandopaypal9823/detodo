# -*- coding: utf-8 -*-
# Landings de registro de la clase del miércoles 4/11: las del 21/10 con otra fecha, otra UTM
# y el pixel de Meta adentro del bloque que se pega en GHL.
#   correr desde la raíz del repo:  python3 landing-siempre-on/clase-04-noviembre/build-desde-clase-21.py
import io

SRC = 'landing-siempre-on/clase-21-octubre/'
DST = 'landing-siempre-on/clase-04-noviembre/'

PIXEL = """
<!-- ════════════════════════════════════════════════════════════════
     META PIXEL · PageView · va ADENTRO del custom code para que viaje con el pegado.
     Si el pixel ya está en Settings → Tracking Code → HEAD de esta página, este bloque
     no vuelve a mandar el PageView (Meta no lo cuenta dos veces).
     La conversión (Lead) la manda GHL por la API de Conversiones: no agregarla acá.
     ════════════════════════════════════════════════════════════════ -->
<script>
(function(){
var yaHabia = !!window.fbq;
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
if(!yaHabia && !window.__nfm_pixel_land){
  window.__nfm_pixel_land = true;
  fbq('init', '1203017011123382');
  fbq('track', 'PageView');
}
})();
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1203017011123382&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel Code -->
"""

for nombre in ['index.html', 'index-popup.html']:
    s = io.open(SRC + nombre, encoding='utf-8').read()

    def rep(old, new, n=1):
        global s
        c = s.count(old)
        assert c == n, f'{nombre}: {c}x :: {old[:90]}'
        s = s.replace(old, new)

    # ── fecha y UTM (lo que va entre data-nfm-fecha igual lo reescribe el JS; se cambia para que el HTML ya diga lo correcto) ──
    rep("Clase del miércoles 21 de octubre · Sistema visual NFM", "Clase del miércoles 4 de noviembre · Sistema visual NFM")
    rep('<span data-nfm-fecha="pill">Mié 21 oct · 19:00 hs (Arg) · Zoom</span>', '<span data-nfm-fecha="pill">Mié 4 nov · 19:00 hs (Arg) · Zoom</span>')
    rep('<span data-nfm-fecha="diaYNumero">miércoles 21</span>', '<span data-nfm-fecha="diaYNumero">miércoles 4</span>')
    rep('<span data-nfm-fecha="larga">miércoles 21 de octubre</span>', '<span data-nfm-fecha="larga">miércoles 4 de noviembre</span>')
    rep('<span data-nfm-fecha="abr">21 de Oct.</span>', '<span data-nfm-fecha="abr">4 de Nov.</span>')
    rep('<span data-nfm-fecha="corta">21 de octubre</span>', '<span data-nfm-fecha="corta">4 de noviembre</span>')
    rep('<span data-nfm-fecha="completa">Miércoles 21 de octubre · 19:00 hs (Argentina) · En vivo por Zoom</span>',
        '<span data-nfm-fecha="completa">Miércoles 4 de noviembre · 19:00 hs (Argentina) · En vivo por Zoom</span>')
    rep("CONFIG · versión FIJA para la clase del 21 de octubre", "CONFIG · versión FIJA para la clase del 4 de noviembre")
    rep("  FECHA: '2026-10-21',                       // miércoles 21 de octubre",
        "  FECHA: '2026-11-04',                       // miércoles 4 de noviembre")
    rep("  UTM_CLASE: 'clase-oct21-alto-rendimiento', // etiqueta de campaña para leads sin UTM",
        "  UTM_CLASE: 'clase-nov04-alto-rendimiento', // etiqueta de campaña para leads sin UTM")

    # ── nunca "cabeza" (regla de marca) ──
    rep('presión, cansancio, la cabeza que no se apaga.', 'presión, cansancio, la mente que no se apaga.')

    # ── pixel: del <head> al bloque del custom code ──
    i = s.index('<!-- ════════════════════════════════════════════════════════════════\n     META PIXEL')
    j = s.index('<!-- End Meta Pixel Code -->', i) + len('<!-- End Meta Pixel Code -->')
    s = s[:i] + s[j:]
    rep('<!-- ═══════════ DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL ═══════════ -->\n',
        '<!-- ═══════════ DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL ═══════════ -->\n' + PIXEL)

    for bad in ['oct21', '2026-10-21', '21 de oct', 'Mié 21', 'miércoles 21', '21 de Oct', 'cabeza']:
        assert bad not in s, f'{nombre}: quedó {bad}'
    a, b = s.index('DESDE ACÁ EMPIEZA'), s.index('HASTA ACÁ EL CUSTOM CODE')
    assert s[a:b].count("fbq('track', 'PageView')") == 1 and s.count("fbq('track', 'PageView')") == 1
    io.open(DST + nombre, 'w', encoding='utf-8').write(s)
    print('ok', DST + nombre, len(s) // 1024, 'KB')
