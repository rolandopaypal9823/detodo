# -*- coding: utf-8 -*-
"""Genera los dos mails de confirmación de compra, en HTML de mail.

   HTML de mail ≠ HTML de web: tablas, estilos en línea, fuentes del sistema
   con respaldo, un ancho de 600px y un botón «a prueba de Outlook». Nada de
   CSS externo, flex ni grid: los clientes de mail los rompen.

   Sale : nfm-clase-paga/mail-compra-basic.html    (USD 1)
          nfm-clase-paga/mail-compra-premium.html  (USD 5)

   Correr desde la raíz del repo:  python3 nfm-clase-paga/gen-mail-compra.py
   Pegar el HTML entero en el editor de código del mail (GHL / Stripe / lo que
   se use). El asunto sugerido está en un comentario arriba de cada archivo.
"""
import io

LOGO   = 'https://nicolasfernandezmiranda.com/wp-content/uploads/2026/01/nuevo-logo-nfm-1.png'
WA     = 'https://go.wha.link/clase-de-neurociencia-6-10'
CLASE  = 'Miércoles 7 de octubre · 19:00 hs (Argentina) · vía Zoom'

TIERS = {
  'basic': {
    'archivo' : 'nfm-clase-paga/mail-compra-basic.html',
    'asunto'  : 'Tu asiento está confirmado — acá está tu acceso',
    'nombre'  : 'Asiento Premium Básico',
    'portal'  : 'https://clase-beneficios.netlify.app/asiento-basic',
    'items'   : [
      ('Workbook', 'Resumen de la clase y accionables concretos.'),
      ('Grabación', 'La clase completa, tuya para siempre.'),
    ],
    'nota'    : '',
  },
  'premium': {
    'archivo' : 'nfm-clase-paga/mail-compra-premium.html',
    'asunto'  : 'Tu asiento está confirmado — el libro y el curso ya están disponibles',
    'nombre'  : 'Asiento Premium · Hackea tu Productividad',
    'portal'  : 'https://clase-beneficios.netlify.app/premium-htc',
    'items'   : [
      ('Hackea tu Cerebro · versión ebook', 'El libro completo, para descargar ahora.'),
      ('El ABC del Alto Rendimiento', 'El curso en video, 6 módulos. Disponible ahora.'),
      ('Workbook', 'Resumen de la clase y accionables concretos.'),
      ('Grabación', 'La clase completa, tuya para siempre.'),
    ],
    'nota'    : 'El libro y el curso <strong style="color:#ffffff;">ya están disponibles</strong> en tu portal.',
  },
}

FONT_H = "'Space Grotesk', 'Helvetica Neue', Helvetica, Arial, sans-serif"
FONT_B = "'DM Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"

def fila(titulo, bajada):
    return f"""
                <tr>
                  <td valign="top" style="padding:0 12px 0 0; width:22px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
                      <td style="width:22px; height:22px; border-radius:6px; background:#3B2A1F; text-align:center; vertical-align:middle; font-family:Arial, sans-serif; font-size:13px; line-height:22px; color:#FF6602; font-weight:bold;">&#10003;</td>
                    </tr></table>
                  </td>
                  <td valign="top" style="padding:0 0 12px 0; font-family:{FONT_B}; font-size:15px; line-height:1.5; color:#B8C4D0;">
                    <strong style="color:#ffffff; font-weight:700;">{titulo}</strong><br>{bajada}
                  </td>
                </tr>"""

def mail(t):
    items = ''.join(fila(a, b) for a, b in t['items'])
    nota = (f'<!-- nota -->\n            <p style="margin:12px 0 24px; padding:14px 16px; background:#0B2440; border:1px solid #1C3D5E; border-radius:12px; font-family:{FONT_B}; font-size:14px; line-height:1.55; color:#B8C4D0;">{t["nota"]}</p>'
            if t['nota'] else '<div style="height:14px; line-height:14px; font-size:0;">&nbsp;</div>')
    return f"""<!-- ASUNTO SUGERIDO: {t['asunto']} -->
<!-- PREHEADER (lo que se ve en la bandeja debajo del asunto): Tu acceso a los beneficios del {t['nombre']}. -->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="x-apple-disable-message-reformatting">
<title>{t['asunto']}</title>
<!--[if mso]><style>table,td{{font-family:Arial,sans-serif !important;}}</style><![endif]-->
<style>
  body{{ margin:0; padding:0; background:#081F33; -webkit-text-size-adjust:100%; }}
  table{{ border-collapse:collapse; }}
  img{{ border:0; outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; }}
  @media only screen and (max-width:620px){{
    .w{{ width:100% !important; }}
    .p{{ padding-left:20px !important; padding-right:20px !important; }}
    .h1{{ font-size:26px !important; line-height:1.2 !important; }}
  }}
</style>
</head>
<body style="margin:0; padding:0; background:#081F33;">
<!-- preheader oculto -->
<div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#081F33;">Tu acceso a los beneficios del {t['nombre']}.&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#081F33" style="background:#081F33;">
  <tr>
    <td align="center" style="padding:28px 12px 40px;">

      <table role="presentation" class="w" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px; max-width:600px;">

        <!-- LOGO -->
        <tr>
          <td align="center" style="padding:6px 0 26px;">
            <a href="https://nicolasfernandezmiranda.com" target="_blank" style="text-decoration:none;">
              <img src="{LOGO}" width="160" alt="Nicolás Fernández Miranda" style="display:block; width:160px; height:auto; border:0;">
            </a>
          </td>
        </tr>

        <!-- TARJETA -->
        <tr>
          <td class="p" bgcolor="#0E2E4A" style="background:#0E2E4A; border:1px solid #1C3D5E; border-radius:20px; padding:36px 36px 30px;">

            <!-- eyebrow -->
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr>
              <td style="border:1px solid #7A4A2A; border-radius:50px; padding:6px 14px; font-family:{FONT_H}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:#FF6602;">{t['nombre']}</td>
            </tr></table>

            <!-- título -->
            <h1 class="h1" style="margin:18px 0 10px; font-family:{FONT_H}; font-size:30px; line-height:1.18; font-weight:bold; color:#ffffff; text-align:center; letter-spacing:-0.5px;">Tu asiento está <span style="color:#FF6602;">confirmado.</span></h1>
            <p style="margin:0 0 26px; font-family:{FONT_B}; font-size:16px; line-height:1.6; color:#B8C4D0; text-align:center;">Gracias por sumarte. Esto es lo que incluye tu asiento:</p>

            <!-- ítems -->
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 6px;">{items}
            </table>

            {nota}

            <!-- BOTÓN (a prueba de Outlook) -->
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center">
              <!--[if mso]>
              <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{t['portal']}" style="height:54px;v-text-anchor:middle;width:320px;" arcsize="50%" stroke="f" fillcolor="#FF6602">
                <w:anchorlock/>
                <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:17px;font-weight:bold;">VER MIS BENEFICIOS &rarr;</center>
              </v:roundrect>
              <![endif]-->
              <!--[if !mso]><!-->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="width:100%; max-width:320px; mso-hide:all;">
                <tr><td align="center" bgcolor="#FF6602" style="background:#FF6602; border-radius:50px;">
                  <a href="{t['portal']}" target="_blank" style="display:block; padding:0 18px; color:#ffffff; font-family:{FONT_H}; font-size:17px; font-weight:bold; line-height:54px; text-align:center; text-decoration:none; -webkit-text-size-adjust:none;">VER MIS BENEFICIOS &rarr;</a>
                </td></tr>
              </table>
              <!--<![endif]-->
            </td></tr></table>

            <p style="margin:14px 0 0; font-family:{FONT_B}; font-size:13px; line-height:1.5; color:#8A9BB0; text-align:center;">Tu acceso es este link: <a href="{t['portal']}" style="color:#FF8033; text-decoration:underline; word-break:break-all;">{t['portal'].replace('https://','')}</a><br>Guardá este mail.</p>

          </td>
        </tr>

        <tr><td style="height:16px; line-height:16px; font-size:0;">&nbsp;</td></tr>

        <!-- LA CLASE -->
        <tr>
          <td class="p" bgcolor="#0B2440" style="background:#0B2440; border:1px solid #1C3D5E; border-radius:16px; padding:22px 28px;">
            <p style="margin:0 0 4px; font-family:{FONT_H}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:#FF6602;">Tu clase en vivo</p>
            <p style="margin:0 0 6px; font-family:{FONT_H}; font-size:17px; font-weight:bold; color:#ffffff;">{CLASE}</p>
            <p style="margin:0; font-family:{FONT_B}; font-size:14px; line-height:1.55; color:#B8C4D0;">El acceso al Zoom llega por el grupo de WhatsApp. Si todavía no entraste: <a href="{WA}" style="color:#FF8033; text-decoration:underline;">unite al grupo acá</a>.</p>
          </td>
        </tr>
        <tr><td style="height:16px; line-height:16px; font-size:0;">&nbsp;</td></tr>

        <!-- PIE -->
        <tr>
          <td align="center" style="padding:14px 10px 0; font-family:{FONT_B}; font-size:12px; line-height:1.6; color:#6E8197;">
            Si algo no funciona, respondé este mail y lo resolvemos.<br>
            © Nicolás Fernández Miranda · Instituto de Productividad
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
</body>
</html>
"""

for t in TIERS.values():
    out = mail(t)
    io.open(t['archivo'], 'w', encoding='utf-8').write(out)
    print('escrito', t['archivo'], len(out), 'bytes')
