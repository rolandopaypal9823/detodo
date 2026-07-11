# -*- coding: utf-8 -*-
"""Genera los MAILS HTML cortos del Reto de 7 Días (voz NFM, marca Instituto de Productividad).

Cada mail es súper cortito y visual: logo de Nico + título + mini spoiler + botón "Ir al Día N".
El contenido completo del reto vive en el sitio (una página por día). El mail solo lleva ahí.

Uso:  python3 build_emails.py
Salida: emails-html/bienvenida.html + emails-html/dia1.html .. dia7.html

Antes de cargar en el ESP, reemplazar SITE por el dominio real del sitio en Netlify.
Los mails son HTML de email real: layout con tablas, estilos inline, fuentes web-safe
(Arial/Helvetica) y botón "bulletproof" — se ven bien en Gmail, Outlook, Apple Mail, etc.
"""
import os
from string import Template
from build_sitio import DAYS  # misma fuente de títulos/spoilers/emojis que el sitio

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emails-html")

# TODO: reemplazar por el dominio real del sitio (sin barra final)
SITE = "https://retode7dias.netlify.app"
IG = "@nicofernandezmiranda"

NAVY = "#0c3452"
NAVY2 = "#123f63"
ORANGE = "#ff6602"
INK = "#22384a"
MUTED = "#5a7086"
BG = "#eef3f7"

LOGO = SITE + "/assets/logo-blanco.png"

# Plantilla de email HTML (tablas + inline styles = máxima compatibilidad)
EMAIL = Template("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light">
<title>$title</title>
</head>
<body style="margin:0;padding:0;background:$bg;">
<!-- preheader (texto de preview, oculto) -->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;font-size:1px;line-height:1px;color:$bg;">$preheader &#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:$bg;">
<tr><td align="center" style="padding:24px 12px;">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 6px 24px rgba(12,52,82,.12);">
    <!-- header navy con logo -->
    <tr><td align="center" style="background:$navy;padding:22px 24px;">
      <img src="$logo" width="150" alt="NFM — Instituto de Productividad" style="display:block;width:150px;max-width:60%;height:auto;border:0;">
    </td></tr>
    <!-- barra naranja fina -->
    <tr><td style="height:4px;background:$orange;line-height:4px;font-size:0;">&nbsp;</td></tr>
    <!-- cuerpo -->
    <tr><td style="padding:34px 34px 30px;font-family:Arial,Helvetica,sans-serif;">
      $body
    </td></tr>
    <!-- footer -->
    <tr><td align="center" style="background:$navy;padding:24px;font-family:Arial,Helvetica,sans-serif;">
      <div style="color:#ffffff;font-weight:bold;font-size:15px;margin-bottom:6px;">"No es motivación, es ciencia."</div>
      <div style="color:#9db8cc;font-size:12px;line-height:1.6;">Reto de 7 Días de Desintoxicación Digital<br>Nico Fernández Miranda · Instituto de Productividad</div>
    </td></tr>
  </table>
  <div style="font-family:Arial,Helvetica,sans-serif;color:#9db8cc;font-size:11px;padding:16px 12px 0;">Recibís esto porque te sumaste al Reto de 7 Días.</div>
</td></tr>
</table>
</body>
</html>
""")


def button(href, label):
    """Botón 'bulletproof' con tabla (se ve redondeado donde se puede, rectángulo en Outlook)."""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" style="margin:6px 0 4px;"><tr>
<td align="center" bgcolor="{ORANGE}" style="border-radius:50px;">
<a href="{href}" target="_blank" style="display:inline-block;padding:16px 40px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#ffffff;text-decoration:none;border-radius:50px;">{label}</a>
</td></tr></table>"""


def kicker(text):
    return f'<div style="color:{ORANGE};font-weight:bold;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">{text}</div>'


def day_email_body(d):
    n = d["n"]
    href = f"{SITE}/dia{n}"
    return "".join([
        kicker("Reto de 7 días · Detox digital"),
        f'<div style="font-family:Arial,Helvetica,sans-serif;font-size:30px;font-weight:bold;color:{NAVY};line-height:1.1;margin-bottom:6px;">Día {n} <span style="font-size:26px;">{d["emoji"]}</span></div>',
        f'<div style="font-family:Arial,Helvetica,sans-serif;font-size:21px;font-weight:bold;color:{NAVY};line-height:1.3;margin-bottom:12px;">{d["title"]}</div>',
        f'<p style="font-family:Arial,Helvetica,sans-serif;font-size:16px;color:{INK};line-height:1.6;margin:0 0 22px;">{d["subtitle"]}</p>',
        button(href, f"Ir al Día {n} &rarr;"),
        f'<p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:{MUTED};line-height:1.6;margin:20px 0 0;">Te toma 10-20 minutos. Nos vemos del otro lado.<br><span style="color:{NAVY};font-weight:bold;">— Nico</span></p>',
    ])


def welcome_body():
    href = f"{SITE}/"
    return "".join([
        kicker("Estás dentro"),
        f'<div style="font-family:Arial,Helvetica,sans-serif;font-size:26px;font-weight:bold;color:{NAVY};line-height:1.2;margin-bottom:12px;">Bienvenido al Reto de 7 Días 🧠</div>',
        f'<p style="font-family:Arial,Helvetica,sans-serif;font-size:16px;color:{INK};line-height:1.6;margin:0 0 14px;">Spoiler alert: esto no es un castigo. Durante 7 días te voy a mandar <strong>un mail por día</strong>, cortito, con un dato de cómo funciona tu cerebro y un accionable de 10-20 minutos. No es motivación, es ciencia.</p>',
        f'<p style="font-family:Arial,Helvetica,sans-serif;font-size:16px;color:{INK};line-height:1.6;margin:0 0 22px;"><strong>Mañana llega el Día 1</strong> y vas a descubrir un número tuyo que casi nadie se anima a mirar. Mientras tanto, mirá de qué se trata:</p>',
        button(href, "Ver el reto &rarr;"),
        f'<p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:{MUTED};line-height:1.6;margin:20px 0 0;">No estás haciendo esto solo: cada semana arranca gente nueva. Si querés, contá que empezaste y etiquetame en Instagram ({IG}).<br><span style="color:{NAVY};font-weight:bold;">— Nico</span></p>',
    ])


def build():
    os.makedirs(BASE, exist_ok=True)
    # bienvenida
    html = EMAIL.substitute(
        title="Bienvenido al Reto de 7 Días",
        preheader="Empezamos mañana con el Día 1. Te cuento cómo funciona.",
        bg=BG, navy=NAVY, orange=ORANGE, logo=LOGO, body=welcome_body(),
    )
    with open(os.path.join(BASE, "bienvenida.html"), "w", encoding="utf-8") as f:
        f.write(html)
    # días
    for d in DAYS:
        html = EMAIL.substitute(
            title=f"Día {d['n']} — {d['title']}",
            preheader=d["subtitle"].replace('"', "'"),
            bg=BG, navy=NAVY, orange=ORANGE, logo=LOGO, body=day_email_body(d),
        )
        with open(os.path.join(BASE, f"dia{d['n']}.html"), "w", encoding="utf-8") as f:
            f.write(html)
    print("OK — mails generados en", BASE)


if __name__ == "__main__":
    build()
