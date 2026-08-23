#!/usr/bin/env python3
"""
Genera el QR real del deck a partir de la URL de agendar.

    pip install "qrcode[pil]"
    python3 hacer-qr.py "https://LA-URL-DE-AGENDAR"

Deja assets/SCREENSHOT-qr.png listo. El deck lo toma solo, sin tocar codigo.
"""
import sys, pathlib
import qrcode
from qrcode.constants import ERROR_CORRECT_H

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)

url = sys.argv[1].strip()
out = pathlib.Path(__file__).parent / "assets" / "SCREENSHOT-qr.png"
out.parent.mkdir(parents=True, exist_ok=True)

qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=24, border=2)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="#0c3452", back_color="white")
img.save(out)
print(f"QR generado: {out}  ({img.size[0]}x{img.size[1]}px)\nApunta a: {url}")
