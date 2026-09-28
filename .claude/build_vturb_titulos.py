#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los titulos para cargar en Vturb (Headlines > Codigo: HTML, CSS y JS)
y una vista previa local. El tamaño de letra depende del ancho del recuadro del
titulo (unidades cqi), no del ancho de la ventana: la vista previa de Vturb
muestra un celular dentro de la ventana de la computadora."""
import io, os

BASE = "/home/user/detodo/vturb-titulos"
FUENTES = "https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Open+Sans:wght@400&family=JetBrains+Mono:wght@500&display=swap"

CSS = """@import url('%s');
.nfm-tit{container-type:inline-size;box-sizing:border-box;width:100%%;max-width:680px;margin:0 auto;padding:4px 12px 14px;text-align:center;font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;color:#0c3452}
.nfm-tit *{box-sizing:border-box}
.nfm-tit__k{margin:0 0 8px;font-family:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace;font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:#c04a00}
.nfm-tit .nfm-tit__t{margin:0;font-weight:900;font-size:19px;font-size:clamp(17px,5.4cqi,28px);line-height:1.18;letter-spacing:-.01em;color:#0c3452;text-wrap:balance;overflow-wrap:break-word;hyphens:none}
.nfm-tit .nfm-tit__t span{color:#ff6602}
.nfm-tit .nfm-tit__b{margin:8px auto 0;max-width:58ch;font-family:'Open Sans',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;font-size:14px;font-size:clamp(14px,3.3cqi,16px);font-weight:400;line-height:1.5;color:#33536b}
@container (max-width:420px){.nfm-tit__k{letter-spacing:.12em}}""" % FUENTES

ANTE = "Para quienes tienen gente a cargo"
TITULOS = [
    ("t1-sobreprecio",
     "Experto en Neurociencia revela: 5 claves para dejar de pagar <span>el sobreprecio de ser “productivo”</span>", None),
    ("t2-sueno-salud-familia",
     "Experto en Neurociencia revela: 5 claves para rendir más <span>sin pagarlo con tu sueño, tu salud y tu familia</span>", None),
    ("t3-deja-para-el-final",
     "Magíster en Neurociencias te explica por qué tu cerebro le cumple a cualquiera <span>y a vos te deja para el final</span>", None),
    ("t4-te-cobra-sobreprecio",
     "Experto en Productividad y Neurociencia revela por qué ser “productivo” <span>te está cobrando un sobreprecio</span> en tu cuerpo, tu tiempo y tu salud mental",
     "Y las 5 claves para dejar de pagarlo."),
    ("t5-sin-sumar-cansancio",
     "Experto en Productividad y Neurociencia te explica 5 claves para <span>cumplir con todo sin sumar más cansancio</span>",
     "Y recuperar tu tiempo, tu descanso y tu claridad mental, sin soltar nada de lo que construiste."),
]


def html(titulo, bajada):
    h = '<div class="nfm-tit">\n  <p class="nfm-tit__k">%s</p>\n  <h1 class="nfm-tit__t">%s</h1>\n' % (ANTE, titulo)
    if bajada:
        h += '  <p class="nfm-tit__b">%s</p>\n' % bajada
    return h + '</div>'


def js(codigo):
    return ("// Deja el codigo de este titulo en la pagina: viaja al survey como titulo_vsl\n"
            "window.NFM_TITULO = '%s';\n"
            "try { sessionStorage.setItem('nfm_titulo', '%s'); } catch (e) {}") % (codigo, codigo)


if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    out = ["TITULOS PARA VTURB · VSL Instituto de Productividad",
           "Cargalos en Vturb: Editar > Headlines > Agregar Headline > Codigo.",
           "En cada uno pegás su HTML, el CSS (es el mismo para los cinco) y su JS.",
           "Si ya los cargaste, reemplazá TODO el CSS por el de este archivo: el HTML y el JS no cambiaron.",
           "Cargá los mismos cinco en el video A y en el video B.", ""]
    for i, (codigo, t, b) in enumerate(TITULOS, 1):
        out += ["=" * 70, "TITULO %d · codigo: %s" % (i, codigo), "=" * 70, "",
                "----- HTML -----", html(t, b), "", "----- CSS -----", CSS, "",
                "----- JS -----", js(codigo), "", ""]
    io.open(os.path.join(BASE, "vturb-titulos.txt"), "w", encoding="utf-8").write("\n".join(out))

    prev = ['<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Títulos Vturb</title>',
            '<style>body{margin:0;background:#f3f5f7;font-family:system-ui}'
            '.fila{display:flex;flex-wrap:wrap;gap:28px;justify-content:center;padding:24px 16px 48px}'
            '.cel{width:360px;background:#fff;border:10px solid #222;border-radius:28px;padding:18px 8px;overflow:hidden}'
            '.lbl{font:600 12px/1.4 system-ui;color:#888;margin:0 0 8px;text-align:center}'
            '.vid{aspect-ratio:16/9;background:#000;border-radius:6px}', CSS, '</style></head><body><div class="fila">']
    for i, (codigo, t, b) in enumerate(TITULOS, 1):
        prev.append('<div class="cel" data-codigo="%s"><div class="lbl">Título %d · %s</div>%s<div class="vid"></div></div>'
                    % (codigo, i, codigo, html(t, b)))
    prev.append('</div></body></html>')
    io.open(os.path.join(BASE, "vista-previa-titulos.html"), "w", encoding="utf-8").write("\n".join(prev))
    print("ok · %d titulos" % len(TITULOS))
