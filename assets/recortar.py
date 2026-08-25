"""
Saca el fondo blanco de una foto de estudio y deja un PNG transparente.

Dos cosas que hacen la diferencia entre un recorte "de Paint" y uno fino:

1) NO borra "todo lo blanco". Borra sólo el blanco CONECTADO a los bordes de la
   imagen — o sea, el fondo real. Así la remera blanca de Valentina no se agujerea.

2) El borde no es un corte binario. En una franja de varios píxeles alrededor del
   contorno calcula un alfa PARCIAL a partir de cuánto blanco tiene mezclado cada
   píxel. Eso es lo que rescata los pelos sueltos, que es donde se nota si un
   recorte está bien hecho o no. Después descontamina el color para que no quede
   el halo blanco pegado al contorno.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC   = 'nico-valen.png'
BANDA = 7        # ancho en px de la franja de borde con alfa parcial
W_HI  = 250.0    # a partir de acá el píxel se considera fondo puro
W_LO  = 186.0    # por debajo de acá se considera sujeto puro

im  = Image.open(SRC).convert('RGB')
rgb = np.asarray(im).astype(np.float32)
h, w, _ = rgb.shape

mn  = rgb.min(axis=2)
sat = rgb.max(axis=2) - mn

# ── 1. el fondo: blanco pegado a los bordes ──────────────────────────────
blanco = (mn >= 232) & (sat <= 14)
lbl, _ = ndimage.label(blanco)
ids = np.unique(np.concatenate([lbl[0], lbl[-1], lbl[:, 0], lbl[:, -1]]))
fondo = np.isin(lbl, ids[ids != 0])

sujeto = ndimage.binary_fill_holes(~fondo)
lbl2, n2 = ndimage.label(sujeto)
if n2 > 1:                                    # descarto motitas sueltas
    areas = ndimage.sum(sujeto, lbl2, range(1, n2 + 1))
    sujeto = np.isin(lbl2, [i + 1 for i, a in enumerate(areas) if a > 0.002 * h * w])

# ── 2. tres zonas: sujeto seguro / fondo seguro / franja de borde ────────
seguro_fg = ndimage.binary_erosion(sujeto, iterations=BANDA)
seguro_bg = ~ndimage.binary_dilation(sujeto, iterations=BANDA)
franja    = ~(seguro_fg | seguro_bg)

# ── 3. alfa parcial en la franja, según cuánto blanco tiene mezclado ─────
alpha = seguro_fg.astype(np.float32)
mezcla = np.clip((W_HI - mn) / (W_HI - W_LO), 0.0, 1.0)
alpha[franja] = mezcla[franja]
alpha[seguro_bg] = 0.0

alpha = ndimage.gaussian_filter(alpha, sigma=0.7)     # suaviza la transición
alpha = np.clip(alpha * 1.06, 0, 1)                   # recupera opacidad plena adentro
alpha[seguro_fg] = 1.0
alpha[seguro_bg] = 0.0

# ── 4. descontaminación: saco el blanco mezclado del color del borde ─────
parcial = (alpha > 0.02) & (alpha < 0.985)
a3 = alpha[..., None]
limpio = rgb.copy()
limpio[parcial] = np.clip(
    (rgb[parcial] - 255.0 * (1 - a3[parcial])) / np.maximum(a3[parcial], 0.18), 0, 255)

out = np.dstack([limpio, alpha * 255]).astype(np.uint8)

# ── 5. recorte al contenido ──────────────────────────────────────────────
ys, xs = np.where(alpha > 0.05)
pad = 10
y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + pad + 1)
x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + pad + 1)
img = Image.fromarray(out[y0:y1, x0:x1], 'RGBA')

if img.width > 1100:
    img = img.resize((1100, round(img.height * 1100 / img.width)), Image.LANCZOS)

img.save('nico-valen-recortado.png', optimize=True)
img.save('nico-valen.webp', 'WEBP', quality=88, method=6)

a = np.asarray(img)[..., 3]
print(f"salida        : {img.width}x{img.height}")
print(f"borde suave   : {((a>=6)&(a<=249)).mean()*100:.2f}% de los píxeles (antes: 0.56%)")
print(f"opaco / vacío : {(a>249).mean()*100:.1f}% / {(a<6).mean()*100:.1f}%")
