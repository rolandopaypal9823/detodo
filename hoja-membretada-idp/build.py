#!/usr/bin/env python3
"""
Genera las piezas impresas del Instituto de Productividad para el teatro:

  output/hoja-membretada-idp-carta.pdf          hoja Carta (21.59 x 27.94 cm), lisa
  output/hoja-membretada-idp-carta-renglones.pdf  ídem con renglones suaves para escribir
  output/hoja-membretada-idp-a4.pdf             hoja A4 (21 x 29.7 cm), lisa
  output/hoja-membretada-idp-a4-renglones.pdf   ídem con renglones
  output/hoja-membretada-idp-*-bn.pdf           las mismas cuatro en blanco y negro
  output/tarjeta-invitacion-idp-90x50-v1.pdf / -v2.pdf   tarjeta 90 x 50 mm, dos textos (ver CARD_VARIANTS)
  output/tarjeta-invitacion-idp-plancha-carta-v1.pdf / -v2.pdf  10 tarjetas en una Carta con marcas de corte
  output/qr-idp-tsl-teatro.svg / .png           el QR solo, por si hace falta en otra pieza
  output/mockup-hoja-con-tarjeta.png            preview de la tarjeta pegada en la esquina

Uso:  python3 build.py
Requiere: playwright (python), segno, Pillow. Chromium en /opt/pw-browsers o el de playwright.
"""
import base64
import os
import pathlib
import shutil

import segno
from playwright.sync_api import sync_playwright

# ─────────────────────────── DATOS EDITABLES ────────────────────────────────
QR_URL = "https://mba.nicolasfernandezmiranda.com/idp-tsl?utm_source=teatro"
WEB_CTA_URL = "mba.nicolasfernandezmiranda.com/idp"
WEB_CTA_TEXTO = "Información sobre acompañamiento profesional del Instituto de Productividad en nuestra web"
IG_NICO = "@nicofernandezmiranda"
IG_IDP = "@institutodeproductividad"
CARD_SIGN = "— Nico y Equipo IDP"
CARD_VARIANTS = {
    "v1": {"headline": "Gracias por venir",
           "body": "Conocé cómo trabajar con Nico Fernández Miranda y el Instituto de Productividad."},
    "v2": {"headline": "Espero que disfrutes la función.",
           "body": "Si querés aplicar herramientas a tu caso específico, conocé cómo ser acompañado por profesionales del Instituto de Productividad."},
}
# ────────────────────────────────────────────────────────────────────────────

BLUE = "#0c3452"
BLUE_DARK = "#061d30"
BLUE_LIGHT = "#e7edf2"
ORANGE = "#ff6602"

HERE = pathlib.Path(__file__).parent.resolve()
ASSETS = HERE / "assets"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

PAGES = {
    "carta": (215.9, 279.4),
    "a4": (210.0, 297.0),
}
CARD_W, CARD_H = 90.0, 50.0  # mm


def b64(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


LOGO_NAVY = b64(ASSETS / "logo-nfm-navy.png", "image/png")
LOGO_WHITE = b64(ASSETS / "logo-nfm-blanco.png", "image/png")
LOGO_BLACK = b64(ASSETS / "logo-nfm-negro.png", "image/png")


def font_face(family: str, weight: int, file: str) -> str:
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url('{b64(ASSETS / 'fonts' / file, 'font/ttf')}') format('truetype');}}")


FONTS_CSS = "\n".join([
    font_face("Montserrat", 500, "Montserrat-500.ttf"),
    font_face("Montserrat", 600, "Montserrat-600.ttf"),
    font_face("Montserrat", 700, "Montserrat-700.ttf"),
    font_face("Montserrat", 800, "Montserrat-800.ttf"),
    font_face("Montserrat", 900, "Montserrat-900.ttf"),
    font_face("Open Sans", 400, "OpenSans-400.ttf"),
    font_face("Open Sans", 500, "OpenSans-500.ttf"),
    font_face("Open Sans", 600, "OpenSans-600.ttf"),
    font_face("JetBrains Mono", 500, "JetBrainsMono-500.ttf"),
])

# ─────────────────────────────── QR ─────────────────────────────────────────
qr = segno.make(QR_URL, error="q")
qr.save(str(OUT / "qr-idp-tsl-teatro.svg"), scale=10, border=2, dark=BLUE, light="#ffffff")
qr.save(str(OUT / "qr-idp-tsl-teatro.png"), scale=40, border=2, dark=BLUE, light="#ffffff")
QR_DATA = qr.svg_data_uri(scale=1, border=0, dark=BLUE, light=None)
QR_DATA_BLACK = qr.svg_data_uri(scale=1, border=0, dark="#111111", light=None)

# ───────────────────────────── ICONOS ───────────────────────────────────────
ICON_IG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/>'
    '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
)
ICON_WEB = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/>'
    '<path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
)
# Vector de crecimiento (flecha ascendente) — marca de agua
ARROW_SVG = (
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    '<g transform="rotate(45 50 50) translate(50 50) scale(0.68) translate(-50 -50)">'
    '<polygon points="50,2 92,44 66,44 66,98 34,98 34,44 8,44" fill="{color}"/>'
    '</g></svg>'
)

# ───────────────────────── HOJA MEMBRETADA ──────────────────────────────────

def letterhead_css(w: float, h: float, mono: bool = False) -> str:
    BLUE = "#111111" if mono else globals()["BLUE"]
    ORANGE = "#555555" if mono else globals()["ORANGE"]
    BLUE_LIGHT = "#d4d4d4" if mono else globals()["BLUE_LIGHT"]
    return f"""
    {FONTS_CSS}
    @page {{ size: {w}mm {h}mm; margin: 0; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: {w}mm; height: {h}mm; background: #fff; }}
    body {{ font-family: 'Open Sans', sans-serif; color: {BLUE}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .page {{ position: relative; width: {w}mm; height: {h}mm; overflow: hidden; }}

    /* Marca lateral: filete azul + tramo naranja (vector de crecimiento) */
    .rail {{ position: absolute; left: 0; top: 0; bottom: 0; width: 3.2mm; background: {BLUE}; }}
    .rail::after {{ content: ""; position: absolute; left: 0; right: 0; top: 0; height: 58mm; background: {ORANGE}; }}

    /* Cabecera: logo a la derecha; la esquina superior izquierda queda libre para pegar la tarjeta */
    .header {{ position: absolute; top: 14mm; right: 16mm; text-align: right; }}
    .header img {{ width: 44mm; display: block; margin-left: auto; }}
    .header .inst {{ margin-top: 2.6mm; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 9.2pt; letter-spacing: 0.18em; text-transform: uppercase; color: {BLUE}; }}
    .header .tag {{ margin-top: 1mm; font-family: 'JetBrains Mono', monospace; font-size: 6.4pt; letter-spacing: 0.22em; text-transform: uppercase; color: {ORANGE}; }}

    /* Marca de agua */
    .wm {{ position: absolute; left: 50%; top: 50%; width: 200mm; height: 200mm; transform: translate(-50%, -50%); opacity: 1; }}

    /* Renglones opcionales (divs reales: los degradados repetidos salen irregulares en PDF) */
    .line {{ position: absolute; left: 20mm; right: 16mm; height: 0.25mm; background: {BLUE_LIGHT}; }}

    /* Pie */
    .footer {{ position: absolute; left: 20mm; right: 16mm; bottom: 12mm; }}
    .footer .rule {{ height: 0.5mm; background: {BLUE}; position: relative; margin-bottom: 4mm; }}
    .footer .rule::after {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 22mm; background: {ORANGE}; }}
    .footer .row {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 8mm; }}
    .footer .cta {{ font-size: 7.6pt; line-height: 1.45; max-width: 130mm; color: {BLUE}; }}
    .footer .cta b {{ font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 9.4pt; display: block; margin-top: 0.8mm; letter-spacing: 0.01em; }}
    .footer .social {{ text-align: right; font-size: 7.6pt; line-height: 1.7; white-space: nowrap; }}
    .footer .social .item {{ display: flex; align-items: center; justify-content: flex-end; gap: 1.8mm; }}
    .footer .social svg {{ width: 3.4mm; height: 3.4mm; color: {ORANGE}; flex: none; }}
    .footer .social .h {{ font-family: 'Montserrat', sans-serif; font-weight: 700; }}
    .footer .social .lbl {{ font-family: 'JetBrains Mono', monospace; font-size: 5.6pt; letter-spacing: 0.2em; text-transform: uppercase; color: {ORANGE}; margin-bottom: 0.6mm; }}
    """


def ruled_lines(h: float, top: float = 58.0, bottom: float = 34.0, step: float = 8.5) -> str:
    y, out = top + step, []
    while y <= h - bottom:
        out.append(f'<div class="line" style="top:{y:.2f}mm"></div>')
        y += step
    return "".join(out)


def letterhead_html(w: float, h: float, lines: bool, mono: bool = False) -> str:
    wm = ARROW_SVG.format(color="rgba(0,0,0,0.045)" if mono else "rgba(12,52,82,0.035)")
    logo = LOGO_BLACK if mono else LOGO_NAVY
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{letterhead_css(w, h, mono)}</style></head>
<body><div class="page">
  <div class="rail"></div>
  <div class="wm">{wm}</div>
  {ruled_lines(h) if lines else ''}
  <div class="header">
    <img src="{logo}" alt="Nico Fernández Miranda">
    <div class="inst">Instituto de Productividad</div>
  </div>
  <div class="footer">
    <div class="rule"></div>
    <div class="row">
      <div class="cta">{WEB_CTA_TEXTO}:<b>{WEB_CTA_URL}</b></div>
      <div class="social">
        <div class="lbl">Seguinos en Instagram</div>
        <div class="item">{ICON_IG}<span class="h">{IG_NICO}</span></div>
        <div class="item">{ICON_IG}<span class="h">{IG_IDP}</span></div>
      </div>
    </div>
  </div>
</div></body></html>"""


# ───────────────────────────── TARJETA ──────────────────────────────────────

# Temas: "color" (marca), "bn" (mismo diseño en negro) y "bn-blanco" (fondo blanco, para impresora común)
CARD_THEMES = {
    "color":     {"suffix": "",           "bg": BLUE,      "fg": "#ffffff", "fg2": "rgba(255,255,255,0.86)", "muted": "rgba(255,255,255,0.7)", "accent": ORANGE,   "qr_border": "none"},
    "bn":        {"suffix": "-bn",        "bg": "#111111", "fg": "#ffffff", "fg2": "rgba(255,255,255,0.86)", "muted": "rgba(255,255,255,0.7)", "accent": "#bdbdbd", "qr_border": "none"},
    "bn-blanco": {"suffix": "-bn-blanco", "bg": "#ffffff", "fg": "#111111", "fg2": "#333333",                "muted": "#666666",               "accent": "#111111", "qr_border": "0.3mm solid #111111"},
}


def card_markup(v: str = "v1", theme: str = "color") -> str:
    """Bloque de la tarjeta (90x50 mm) reutilizable en la pieza suelta y en la plancha."""
    t = CARD_VARIANTS[v]
    logo = LOGO_WHITE if theme != "bn-blanco" else LOGO_BLACK
    qr_img = QR_DATA if theme == "color" else QR_DATA_BLACK
    return f"""
<div class="card">
  <div class="c-rail"></div>
  <div class="c-left">
    <img class="c-logo" src="{logo}" alt="Nico Fernández Miranda">
    <div class="c-lbl">Invitación · Instituto de Productividad</div>
    <div class="c-head">{t["headline"]}</div>
    <div class="c-body">{t["body"]}</div>
    <div class="c-sign">{CARD_SIGN}</div>
  </div>
  <div class="c-right">
    <div class="c-qr"><img src="{qr_img}" alt="QR"></div>
    <div class="c-scan">Escaneame</div>
  </div>
</div>"""


def card_css(theme: str = "color") -> str:
    th = CARD_THEMES[theme]
    return f"""
.card {{ position: relative; width: {CARD_W}mm; height: {CARD_H}mm; background: {th["bg"]}; color: {th["fg"]}; overflow: hidden;
         font-family: 'Open Sans', sans-serif; display: flex; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.c-rail {{ position: absolute; left: 0; top: 0; bottom: 0; width: 1.6mm; background: {th["accent"]}; }}
.c-left {{ flex: 1; padding: 4.2mm 3mm 4.2mm 5.4mm; display: flex; flex-direction: column; min-width: 0; }}
.c-logo {{ width: 19mm; display: block; }}
.c-lbl {{ margin-top: 2.6mm; font-family: 'JetBrains Mono', monospace; font-size: 4.3pt; letter-spacing: 0.18em; text-transform: uppercase; color: {th["accent"]}; white-space: nowrap; }}
.c-head {{ margin-top: 1.4mm; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 9.2pt; line-height: 1.12; letter-spacing: -0.005em; }}
.c-body {{ margin-top: 1.4mm; font-size: 5.4pt; line-height: 1.36; color: {th["fg2"]}; }}
.c-sign {{ margin-top: auto; font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 5.6pt; color: {th["accent"]}; }}
.c-right {{ width: 34mm; padding: 4.2mm 4.2mm 4.2mm 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.4mm; }}
.c-qr {{ width: 30mm; height: 30mm; background: #fff; border-radius: 1.6mm; padding: 2.6mm; border: {th["qr_border"]}; }}
.c-qr img {{ width: 100%; height: 100%; display: block; image-rendering: pixelated; }}
.c-scan {{ font-family: 'JetBrains Mono', monospace; font-size: 4.6pt; letter-spacing: 0.24em; text-transform: uppercase; color: {th["muted"]}; }}
"""


def card_html(v: str = "v1", theme: str = "color") -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
    {FONTS_CSS}
    @page {{ size: {CARD_W}mm {CARD_H}mm; margin: 0; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: {CARD_W}mm; height: {CARD_H}mm; background: #fff; }}
    {card_css(theme)}
    </style></head><body>{card_markup(v, theme)}</body></html>"""


def card_sheet_html(v: str = "v1", theme: str = "color") -> str:
    """Plancha Carta con 10 tarjetas (2 x 5) y marcas de corte."""
    w, h = PAGES["carta"]
    cols, rows, gap = 2, 5, 4.0
    grid_w = cols * CARD_W + (cols - 1) * gap
    grid_h = rows * CARD_H + (rows - 1) * gap
    left = (w - grid_w) / 2
    top = (h - grid_h) / 2
    cards = "".join(
        f'<div class="slot" style="left:{left + c * (CARD_W + gap)}mm;top:{top + r * (CARD_H + gap)}mm">{card_markup(v, theme)}</div>'
        for r in range(rows) for c in range(cols)
    )
    marks = []
    for c in range(cols):
        for x in (left + c * (CARD_W + gap), left + c * (CARD_W + gap) + CARD_W):
            marks.append(f'<div class="mk v" style="left:{x}mm;top:{top - 6}mm"></div>')
            marks.append(f'<div class="mk v" style="left:{x}mm;top:{top + grid_h + 1}mm"></div>')
    for r in range(rows):
        for y in (top + r * (CARD_H + gap), top + r * (CARD_H + gap) + CARD_H):
            marks.append(f'<div class="mk h" style="top:{y}mm;left:{left - 6}mm"></div>')
            marks.append(f'<div class="mk h" style="top:{y}mm;left:{left + grid_w + 1}mm"></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
    {FONTS_CSS}
    @page {{ size: {w}mm {h}mm; margin: 0; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: {w}mm; height: {h}mm; background: #fff; }}
    .slot {{ position: absolute; }}
    .mk {{ position: absolute; background: #888; }}
    .mk.v {{ width: 0.2mm; height: 5mm; }}
    .mk.h {{ height: 0.2mm; width: 5mm; }}
    .note {{ position: absolute; left: 0; right: 0; bottom: 5mm; text-align: center; font: 6pt 'JetBrains Mono', monospace; color: #999; letter-spacing: 0.15em; }}
    {card_css(theme)}
    </style></head><body>{cards}{''.join(marks)}
    <div class="note">TARJETA INVITACIÓN IDP · 90 × 50 MM · 10 POR PLANCHA · CORTAR POR LAS MARCAS</div>
    </body></html>"""


# ───────────────────────────── MOCKUP ───────────────────────────────────────

def mockup_html() -> str:
    w, h = PAGES["carta"]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
    {FONTS_CSS}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #d9dee3; padding: 18mm; width: {w + 36}mm; }}
    .stage {{ position: relative; width: {w}mm; height: {h}mm; box-shadow: 0 30px 80px rgba(12,52,82,0.25); }}
    .stage iframe {{ width: {w}mm; height: {h}mm; border: 0; display: block; }}
    .paste {{ position: absolute; left: 12mm; top: 12mm; transform: rotate(-1.5deg); box-shadow: 0 6px 18px rgba(0,0,0,0.28); }}
    {card_css()}
    </style></head><body>
    <div class="stage">
      <iframe srcdoc='{letterhead_html(w, h, True).replace("'", "&#39;")}'></iframe>
      <div class="paste">{card_markup("v2")}</div>
    </div></body></html>"""


# ───────────────────────────── RENDER ───────────────────────────────────────

def find_chromium():
    for p in ("/opt/pw-browsers/chromium", shutil.which("chromium"), shutil.which("chromium-browser")):
        if p and os.path.exists(p):
            return p
    return None


def main():
    src = OUT / "_html"
    src.mkdir(exist_ok=True)
    jobs = []
    for name, (w, h) in PAGES.items():
        for lines in (False, True):
            for mono in (False, True):
                fn = f"hoja-membretada-idp-{name}{'-renglones' if lines else ''}{'-bn' if mono else ''}"
                (src / f"{fn}.html").write_text(letterhead_html(w, h, lines, mono), encoding="utf-8")
                jobs.append((fn, w, h))
    for v in CARD_VARIANTS:
        for theme, th in CARD_THEMES.items():
            sx = v + th["suffix"]
            (src / f"tarjeta-invitacion-idp-90x50-{sx}.html").write_text(card_html(v, theme), encoding="utf-8")
            jobs.append((f"tarjeta-invitacion-idp-90x50-{sx}", CARD_W, CARD_H))
            (src / f"tarjeta-invitacion-idp-plancha-carta-{sx}.html").write_text(card_sheet_html(v, theme), encoding="utf-8")
            jobs.append((f"tarjeta-invitacion-idp-plancha-carta-{sx}", *PAGES["carta"]))
    (src / "mockup.html").write_text(mockup_html(), encoding="utf-8")

    with sync_playwright() as p:
        exe = find_chromium()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        for fn, w, h in jobs:
            page.goto((src / f"{fn}.html").as_uri())
            page.wait_for_timeout(200)
            page.pdf(path=str(OUT / f"{fn}.pdf"), width=f"{w}mm", height=f"{h}mm",
                     print_background=True, prefer_css_page_size=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print("ok", fn)
        # Previews PNG
        for fn, w, h in jobs:
            if fn.startswith("tarjeta-invitacion-idp-90x50"):
                page.set_viewport_size({"width": int(CARD_W * 3.7795), "height": int(CARD_H * 3.7795)})
                page.goto((src / f"{fn}.html").as_uri()); page.wait_for_timeout(200)
                page.screenshot(path=str(OUT / f"{fn}.png"), scale="device")
        page = browser.new_page(device_scale_factor=2, viewport={"width": 1000, "height": 1300})
        page.goto((src / "mockup.html").as_uri())
        page.wait_for_timeout(600)
        page.screenshot(path=str(OUT / "mockup-hoja-con-tarjeta.png"), full_page=True)
        print("ok mockup")
        browser.close()


if __name__ == "__main__":
    main()
