#!/usr/bin/env python3
"""
Arma las dos imágenes de la landing SIN generación de IA.

La tapa (y por lo tanto la cara de Nico) nunca pasa por un modelo: se recorta,
se rota y se compone con manipulación de pixeles. Es imposible que cambie.

    python3 armar-mockups.py ebook.png

Salida:
    assets/ebook-primer-capitulo.png   (tablet inclinada 6° horario, cartel naranja)
    assets/ebook-libro-completo.png    (tablet inclinada 6° antihorario, cartel blanco)

Opciones:
    --no-recorte      la imagen de entrada ya viene con fondo transparente
    --tolerancia N    umbral del recorte de fondo blanco (default 32, subilo si queda halo)
    --font RUTA.ttf   fuente de los carteles (default: busca Montserrat, si no usa la del sistema)
    --salida DIR      carpeta de salida (default: assets)
"""
import argparse
import os
import sys
from collections import deque

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit("Falta Pillow.  pip install Pillow")

LIENZO = 1024
ALTO_DISPOSITIVO = 0.62          # el device ocupa 62% del alto del lienzo
NARANJA = (255, 102, 2, 255)
NAVY = (12, 52, 82, 255)
BLANCO = (255, 255, 255, 255)

PIEZAS = [
    dict(salida="ebook-primer-capitulo.png", angulo=-6.0,
         cartel="PRIMER CAPÍTULO", cartel_fondo=NARANJA, cartel_texto=BLANCO,
         cartel_borde=None, pie="PDF · GRATIS"),
    dict(salida="ebook-libro-completo.png", angulo=6.0,
         cartel="LIBRO COMPLETO", cartel_fondo=BLANCO, cartel_texto=NAVY,
         cartel_borde=NARANJA, pie="EDICIÓN COMPLETA"),
]

RUTAS_FUENTE = [
    "/Library/Fonts/Montserrat-Black.ttf",
    "/Library/Fonts/Montserrat-ExtraBold.ttf",
    os.path.expanduser("~/Library/Fonts/Montserrat-Black.ttf"),
    "/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
RUTAS_MONO = [
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
]


def buscar_fuente(rutas, tam):
    for r in rutas:
        if os.path.exists(r):
            try:
                return ImageFont.truetype(r, tam), r
            except OSError:
                continue
    return ImageFont.load_default(), None


def recortar_fondo(im, tolerancia):
    """Saca el fondo por flood fill desde los bordes, midiendo distancia al color de
    fondo real (muestreado en las esquinas), no a blanco puro. Con tolerancia amplia
    también se come la sombra suave, que es continua con el fondo.

    No toca el interior de la tapa: el blanco del logo de la editorial o de la
    ilustración queda intacto porque está rodeado de oscuro y el fill nunca llega."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    # color de fondo = mediana de las 4 esquinas (16x16 cada una)
    muestras = []
    for ox, oy in ((0, 0), (w - 16, 0), (0, h - 16), (w - 16, h - 16)):
        for dx in range(16):
            for dy in range(16):
                r, g, b, a = px[max(0, min(w - 1, ox + dx)), max(0, min(h - 1, oy + dy))]
                if a > 0:
                    muestras.append((r, g, b))
    if muestras:
        fondo = tuple(sorted(c[i] for c in muestras)[len(muestras) // 2] for i in range(3))
    else:
        fondo = (255, 255, 255)

    visto = bytearray(w * h)
    cola = deque()

    def claro(x, y):
        r, g, b, a = px[x, y]
        if a == 0:
            return False
        return max(abs(r - fondo[0]), abs(g - fondo[1]), abs(b - fondo[2])) <= tolerancia

    for x in range(w):
        for y in (0, h - 1):
            if not visto[y * w + x] and claro(x, y):
                visto[y * w + x] = 1
                cola.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visto[y * w + x] and claro(x, y):
                visto[y * w + x] = 1
                cola.append((x, y))

    while cola:
        x, y = cola.popleft()
        px[x, y] = (255, 255, 255, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visto[ny * w + nx] and claro(nx, ny):
                visto[ny * w + nx] = 1
                cola.append((nx, ny))

    # suaviza el borde del alpha para que no quede escalerita
    alpha = im.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    im.putalpha(alpha)
    return im


def recortar_a_contenido(im):
    caja = im.getchannel("A").getbbox()
    return im.crop(caja) if caja else im


def sombra(im, desenfoque=26, desplazamiento=22, opacidad=140):
    s = Image.new("RGBA", im.size, (0, 0, 0, 0))
    s.putalpha(im.getchannel("A").point(lambda v: min(opacidad, v)))
    s = s.filter(ImageFilter.GaussianBlur(desenfoque))
    lienzo = Image.new("RGBA", (im.width, im.height + desplazamiento), (0, 0, 0, 0))
    lienzo.alpha_composite(s, (0, desplazamiento))
    return lienzo


def cartel(texto, fuente, fondo, color_texto, borde, angulo=-8.0):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    caja = tmp.textbbox((0, 0), texto, font=fuente)
    tw, th = caja[2] - caja[0], caja[3] - caja[1]
    padx, pady = int(th * 1.05), int(th * 0.68)
    w, h = tw + padx * 2, th + pady * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * 0.22), fill=fondo,
                        outline=borde, width=3 if borde else 0)
    d.text((padx - caja[0], pady - caja[1]), texto, font=fuente, fill=color_texto)
    return im.rotate(angulo, resample=Image.BICUBIC, expand=True)


def armar(base, pieza, f_cartel, f_pie, opacidad_sombra=140):
    lienzo = Image.new("RGBA", (LIENZO, LIENZO), (0, 0, 0, 0))

    alto = int(LIENZO * ALTO_DISPOSITIVO)
    disp = base.copy()
    disp = disp.resize((max(1, round(disp.width * alto / disp.height)), alto), Image.LANCZOS)
    disp = disp.rotate(pieza["angulo"], resample=Image.BICUBIC, expand=True)

    x = (LIENZO - disp.width) // 2
    y = int(LIENZO * 0.40) - disp.height // 2

    if opacidad_sombra > 0:
        lienzo.alpha_composite(sombra(disp, opacidad=opacidad_sombra), (x, y))
    lienzo.alpha_composite(disp, (x, y))

    b = cartel(pieza["cartel"], f_cartel, pieza["cartel_fondo"],
               pieza["cartel_texto"], pieza["cartel_borde"])
    bx = max(8, x - int(b.width * 0.24))
    by = max(8, y + int(disp.height * 0.02))
    lienzo.alpha_composite(b, (bx, by))

    d = ImageDraw.Draw(lienzo)
    pie = " ".join(pieza["pie"])          # tracking amplio, a lo JetBrains Mono
    caja = d.textbbox((0, 0), pie, font=f_pie)
    d.text(((LIENZO - (caja[2] - caja[0])) // 2, int(LIENZO * 0.81)),
           pie, font=f_pie, fill=(243, 247, 251, 235))
    return lienzo


def main():
    ap = argparse.ArgumentParser(description="Arma los mockups sin tocar la tapa.")
    ap.add_argument("entrada", help="PNG/JPG del ebook (tablet con la tapa)")
    ap.add_argument("--no-recorte", action="store_true")
    ap.add_argument("--tolerancia", type=int, default=70)
    ap.add_argument("--sombra", type=int, default=140,
                    help="opacidad de la sombra de contacto (0 la desactiva)")
    ap.add_argument("--font")
    ap.add_argument("--salida", default="assets")
    a = ap.parse_args()

    base = Image.open(a.entrada).convert("RGBA")
    if not a.no_recorte:
        base = recortar_fondo(base, a.tolerancia)
    base = recortar_a_contenido(base)

    rutas = ([a.font] if a.font else []) + RUTAS_FUENTE
    f_cartel, usada = buscar_fuente(rutas, 40)
    f_pie, _ = buscar_fuente(RUTAS_MONO, 21)
    if usada and "ontserrat" not in usada:
        print(f"  ! Sin Montserrat, uso {os.path.basename(usada)}. "
              f"Para el tipo exacto: --font /ruta/Montserrat-Black.ttf")

    os.makedirs(a.salida, exist_ok=True)
    for p in PIEZAS:
        destino = os.path.join(a.salida, p["salida"])
        armar(base, p, f_cartel, f_pie, a.sombra).save(destino, optimize=True)
        print(f"  ✓ {destino}")
    print("\nListo. La tapa nunca pasó por un modelo: la cara es la original, pixel a pixel.")


if __name__ == "__main__":
    main()
