# -*- coding: utf-8 -*-
"""Genera la thank you de REGISTRO sin el pop-up de asientos.

   Sale de thankyou-oto.html (misma fecha, grupo de WhatsApp, video y pasos),
   sin el CSS ni el HTML/JS del pop-up. Es la que va mientras no hay oferta
   de asiento cargada (pauta prendida, links de pago todavía no creados).

   Entra : nfm-clase-paga/thankyou-oto.html
   Sale  : nfm-clase-paga/thankyou-registro-sin-popup.html

   Correr desde la raíz del repo:  python3 nfm-clase-paga/gen-thankyou-sin-popup.py
"""
import io

BASE = 'nfm-clase-paga/thankyou-oto.html'
OUT  = 'nfm-clase-paga/thankyou-registro-sin-popup.html'

s = io.open(BASE, encoding='utf-8').read()

# fuera el CSS del pop-up
a = s.index("/* ── POPUP POST-REGISTRO")
b = s.index("/* ── BARRA DE MODO PRUEBA ── */")
s = s[:a] + s[b:]

# fuera el pop-up entero (HTML + script)
a = s.index("<!-- ══════════════════════════════════════════════════════════════════\n     POPUP POST-REGISTRO")
b = s.index("<!-- ═══════════ HASTA ACÁ EL CUSTOM CODE DE GHL ═══════════ -->")
s = s[:a] + s[b:]

assert 'nfm-oferta' not in s, 'quedó algo del pop-up'
assert 'buy.stripe.com' not in s, 'quedó un link de pago'
io.open(OUT, 'w', encoding='utf-8').write(s)
print('escrito', OUT, len(s), 'bytes')
