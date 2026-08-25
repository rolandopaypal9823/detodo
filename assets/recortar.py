"""
Saca el fondo blanco de la foto de Nico + Valentina y deja un PNG transparente.

Clave: NO borra "todo lo blanco" (eso agujerearía la remera blanca de Valentina).
Borra sólo el blanco CONECTADO a los bordes de la imagen — o sea, el fondo real.
Después suaviza el borde para que no quede aserrado y le quita el halo blanco.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = 'nico-valen.png'
im  = Image.open(SRC).convert('RGB')
rgb = np.asarray(im).astype(np.float32)
h, w, _ = rgb.shape

mn  = rgb.min(axis=2)
mx  = rgb.max(axis=2)
sat = mx - mn                      # cuán lejos del gris está el pixel

# 1) candidatos a fondo: muy claros y muy poco saturados
blanco = (mn >= 232) & (sat <= 14)

# 2) me quedo sólo con el blanco pegado al borde (el fondo de verdad)
lbl, n = ndimage.label(blanco)
bordes = np.concatenate([lbl[0], lbl[-1], lbl[:, 0], lbl[:, -1]])
ids = np.unique(bordes); ids = ids[ids != 0]
fondo = np.isin(lbl, ids)

# 3) tapo agujeritos que quedaron dentro del sujeto (reflejos, el libro, etc.)
sujeto = ndimage.binary_fill_holes(~fondo)
# me quedo con las dos figuras y descarto motitas sueltas del fondo
lbl2, n2 = ndimage.label(sujeto)
if n2 > 1:
    areas = ndimage.sum(sujeto, lbl2, range(1, n2 + 1))
    grandes = [i + 1 for i, a in enumerate(areas) if a > 0.002 * h * w]
    sujeto = np.isin(lbl2, grandes)

# 4) borde suave: alfa parcial en la transición, no un corte duro
alpha = ndimage.gaussian_filter(sujeto.astype(np.float32), sigma=1.1)
alpha = np.clip((alpha - 0.35) / 0.42, 0, 1)          # curva de contraste
# encojo medio pixel para comerme el halo blanco del contorno
alpha *= np.clip(ndimage.gaussian_filter(sujeto.astype(np.float32), sigma=0.6) * 1.25, 0, 1)

# 5) descontaminación: donde el alfa es parcial, saco el blanco mezclado
parcial = (alpha > 0.02) & (alpha < 0.98)
a3 = alpha[..., None]
limpio = rgb.copy()
limpio[parcial] = np.clip((rgb[parcial] - 255.0 * (1 - a3[parcial])) / np.maximum(a3[parcial], 0.12), 0, 255)

out = np.dstack([limpio, alpha * 255]).astype(np.uint8)

# 6) recorto al contenido con un margen chico
ys, xs = np.where(alpha > 0.06)
pad = 12
y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + pad + 1)
x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + pad + 1)
img = Image.fromarray(out[y0:y1, x0:x1], 'RGBA')

# 7) tamaño web: 1100 px de ancho alcanza y sobra para el hero
if img.width > 1100:
    img = img.resize((1100, round(img.height * 1100 / img.width)), Image.LANCZOS)

img.save('nico-valen-recortado.png', optimize=True)
print(f"original   : {w}x{h}")
print(f"recortado  : {img.width}x{img.height}  (bbox {x0},{y0} -> {x1},{y1})")
print(f"sujeto     : {sujeto.mean()*100:.1f}% de la imagen")
