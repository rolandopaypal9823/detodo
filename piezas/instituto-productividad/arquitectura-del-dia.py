# -*- coding: utf-8 -*-
"""LÁM. 01 — Arquitectura del día. Cronografía Silenciosa."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Wedge, Circle
from pathlib import Path

FDIR = Path(".claude/skills/canvas-design/canvas-fonts")
for f in FDIR.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))

SANS, GROT, SERIF, MONO = "Inter", "Space Grotesk", "EB Garamond", "JetBrains Mono"

# ---- lienzo -----------------------------------------------------------------
W, H = 827.0, 1169.0          # unidades = 1/100 in  (A4 vertical)
U2PT = 595.276 / W            # unidad -> punto tipográfico
def pt(u): return u * U2PT

PAPER = "#E7E1D4"
INK    = "#15171B"
GREY   = "#8E877A"
FAINT  = "#B9B2A3"
WARM   = "#B4552C"
COOL   = "#2C4551"

fig = plt.figure(figsize=(W/100, H/100), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H)
ax.set_aspect("equal"); ax.axis("off")

# grano de papel -------------------------------------------------------------
rng = np.random.default_rng(7)
grain = rng.normal(0.5, 0.5, (700, 495))
ax.imshow(grain, extent=(0,W,0,H), cmap="Greys", alpha=0.035,
          interpolation="bilinear", zorder=0)

def line(x0,y0,x1,y1,c=INK,lw=0.6,a=1.0,z=3,**k):
    ax.plot([x0,x1],[y0,y1],color=c,lw=lw,alpha=a,zorder=z,
            solid_capstyle="butt",**k)
def txt(x,y,s,size,fam=SANS,c=INK,ha="left",va="baseline",w="normal",
        sp=0.0,st="normal",a=1.0,z=5):
    ax.text(x,y,s,fontsize=pt(size),fontfamily=fam,color=c,ha=ha,va=va,
            fontweight=w,fontstyle=st,alpha=a,zorder=z,
            fontstretch="normal",**({"linespacing":1.0}))
def track(x,y,s,size,fam=MONO,c=GREY,ha="left",tr=3.2,**k):
    """tipografía con interletrado manual"""
    if ha == "right":
        # medir con un render fantasma no hace falta: dibujamos desde el final
        chars = list(s); total = 0
        for ch in chars: total += 0  # ancho real se resuelve abajo
    t = ax.text(x,y,(" "*0).join(s), fontsize=pt(size), fontfamily=fam, color=c,
                ha=ha, va="baseline", zorder=5, **k)
    return t

# ---- retícula de referencia -------------------------------------------------
M   = 72.0                    # margen
RGT = W - M                   # 755
line(M, 1090, RGT, 1090, c=INK, lw=0.9)
line(M, 222,  RGT, 222,  c=INK, lw=0.9)
line(M, 62,   RGT, 62,   c=FAINT, lw=0.5)

# ---- cabecera ---------------------------------------------------------------
txt(M, 1102, "I N S T I T U T O   D E   P R O D U C T I V I D A D", 7.4,
    MONO, INK, w="normal")
txt(RGT, 1102, "L Á M .  0 1   ·   C I C L O  Ø 2 4 H", 7.4, MONO, GREY, ha="right")

# ---- titular ----------------------------------------------------------------
txt(M-3, 1008, "ARQUITECTURA", 62, GROT, INK, w="light")
txt(M-3,  944, "DEL DÍA", 62, GROT, INK, w="light")
txt(RGT, 1008, "un mapa de fases", 15, SERIF, INK, ha="right", st="italic")
txt(RGT,  982, "del cuerpo despierto", 15, SERIF, INK, ha="right", st="italic")
txt(RGT,  944, "OBSERVACIÓN CONTINUA · 1440 MARCAS", 6.6, MONO, GREY, ha="right")

# ---- esfera -----------------------------------------------------------------
CX, CY, R = W/2, 602.0, 264.0
def ang(t):  return np.deg2rad(90.0 - t/24.0*360.0)   # 00:00 arriba, horario
def pol(t, r):
    a = ang(t); return CX + r*np.cos(a), CY + r*np.sin(a)

# noche: meridianos de apagado y encendido (el arco va en el aro exterior)
for e in (23.0, 6.5):
    x0,y0 = pol(e, 58); x1,y1 = pol(e, R-8)
    ax.plot([x0,x1],[y0,y1],color=COOL,lw=0.45,ls=(0,(1.6,4)),alpha=0.8,zorder=3)

# 1440 marcas de minuto
for i in range(1440):
    t = i/60.0
    if i % 60 == 0:      continue
    lng = 6.5 if i % 15 == 0 else (4.5 if i % 5 == 0 else 2.6)
    alp = 0.85 if i % 15 == 0 else (0.55 if i % 5 == 0 else 0.28)
    x0,y0 = pol(t, R-lng); x1,y1 = pol(t, R)
    line(x0,y0,x1,y1, c=INK, lw=0.35, a=alp, z=2)
# marcas horarias
for hh in range(24):
    lng = 15.0 if hh % 3 == 0 else 10.0
    x0,y0 = pol(hh, R-lng); x1,y1 = pol(hh, R)
    line(x0,y0,x1,y1, c=INK, lw=0.9 if hh%3==0 else 0.55, z=3)
# aro exterior
ax.add_patch(Circle((CX,CY), R, fill=False, ec=INK, lw=0.9, zorder=3))
ax.add_patch(Circle((CX,CY), R+9, fill=False, ec=FAINT, lw=0.45, zorder=3))

# numerales horarios
for hh in range(0,24,3):
    x,y = pol(hh, R+27)
    txt(x, y-3.2, f"{hh:02d}", 8.0, MONO, INK, ha="center")

# ---- curvas -----------------------------------------------------------------
t = np.linspace(0, 24, 2400)
def gauss(t, mu, s):
    d = np.minimum(np.abs(t-mu), 24-np.abs(t-mu))
    return np.exp(-(d**2)/(2*s**2))

cortisol = 0.10 + 0.90*gauss(t, 8.0, 2.3) + 0.10*gauss(t, 17.0, 1.4)
cortisol /= cortisol.max()
temp     = 0.5 + 0.5*np.sin(2*np.pi*(t-11.0)/24.0)
aden     = np.where(t >= 6.5, (t-6.5)/16.5, np.nan)
aden     = np.where(t >= 23.0, 1 - (t-23.0)/7.5, aden)
aden     = np.where(t < 6.5, 0.867 - (t)/7.5*0.867, aden)
aden     = np.clip(aden, 0, 1)
mela     = gauss(t, 3.0, 2.5)**1.7; mela /= mela.max()

COOL2 = "#587683"
BANDS = [(cortisol, 212.0, 34.0, WARM,  1.35, 0.11),
         (temp,     166.0, 30.0, INK,   0.95, 0.07),
         (aden,     120.0, 28.0, COOL,  0.95, 0.08),
         (mela,      76.0, 26.0, COOL2, 0.95, 0.08)]

for vals, base, amp, col, lw, fa in BANDS:
    # circunferencia de base, punteada
    ta = np.linspace(0,24,900); bx,by = pol(ta, base)
    ax.plot(bx,by,color=FAINT,lw=0.4,ls=(0,(1,3)),zorder=3)
    r = base + amp*vals
    x,y = pol(t, r)
    bxx,byy = pol(t, base)
    poly = np.column_stack([np.r_[x, bxx[::-1]], np.r_[y, byy[::-1]]])
    ax.add_patch(Polygon(poly, closed=True, facecolor=col, alpha=fa,
                         edgecolor="none", zorder=3))
    ax.plot(x,y,color=col,lw=lw,zorder=4,solid_capstyle="round")

# ---- bloques de foco --------------------------------------------------------
def arco(t0,t1,r,c,lw,z=5,a=1.0):
    tt = np.linspace(t0,t1,400); x,y = pol(tt,r)
    ax.plot(x,y,color=c,lw=lw,zorder=z,alpha=a,solid_capstyle="butt")

arco(23.0, 30.5, R+9, COOL, 1.2, z=5, a=0.7)
for e in (23.0, 30.5):
    x0,y0 = pol(e, R+5.5); x1,y1 = pol(e, R+12.5)
    line(x0,y0,x1,y1,c=COOL,lw=0.7,z=5)
xm,ym = pol(2.75, R+46); txt(xm, ym-3.4, "N", 9.0, MONO, COOL, ha="center", a=0.85)

for (t0,t1,num) in [(9.5,12.0,"I"), (15.5,18.0,"II")]:
    arco(t0,t1, R+9, WARM, 3.2)
    for e in (t0,t1):
        x0,y0 = pol(e, R+4.5); x1,y1 = pol(e, R+13.5)
        line(x0,y0,x1,y1,c=WARM,lw=0.8,z=5)
    xm,ym = pol((t0+t1)/2, R+46)
    txt(xm, ym-3.4, num, 9.5, MONO, WARM, ha="center")


# ---- centro -----------------------------------------------------------------
ax.add_patch(Circle((CX,CY), 58, fill=False, ec=FAINT, lw=0.45, zorder=3))
line(CX-9, CY, CX+9, CY, c=INK, lw=0.5, z=5)
line(CX, CY-9, CX, CY+9, c=INK, lw=0.5, z=5)
txt(CX, CY+30, "F A S E", 6.6, MONO, GREY, ha="center")
txt(CX, CY-38, "Ø 24 H", 6.6, MONO, GREY, ha="center")

# ---- pie: índice y protocolo ------------------------------------------------
txt(M, 200, "Í N D I C E   D E   F A S E S", 7.0, MONO, GREY)
items = [("01","CORTISOL","despertar · activación", WARM),
         ("02","TEMPERATURA","mínimo 04:30 · pico 17:00", INK),
         ("03","ADENOSINA","presión de sueño acumulada", COOL),
         ("04","MELATONINA","inicio ≈ 21:00 · pico 03:00", "#587683")]
yy = 174
for n,nom,det,col in items:
    line(M, yy+2.6, M+16, yy+2.6, c=col, lw=1.3, z=5)
    txt(M+23, yy, n, 7.0, MONO, GREY)
    txt(M+44, yy, nom, 8.2, SANS, INK, w="semibold")
    txt(M+150, yy, det, 8.2, SANS, GREY)
    yy -= 22

XP = 452.0
txt(XP, 200, "P R O T O C O L O", 7.0, MONO, GREY)
prot = [("06:30","luz directa a los ojos, 10 min"),
        ("09:30","bloque profundo  I"),
        ("14:30","último café del día"),
        ("15:30","bloque profundo  II"),
        ("22:30","descenso térmico · sin pantallas")]
yy = 174
for hh, det in prot:
    txt(XP, yy, hh, 8.2, MONO, WARM)
    txt(XP+58, yy, det, 8.2, SANS, INK)
    yy -= 22

# ---- pie de página ----------------------------------------------------------
txt(M, 44, "C R O N O G R A F Í A   S I L E N C I O S A", 6.6, MONO, GREY)
txt(RGT, 44, "el rendimiento no es voluntad: es fase", 10.5, SERIF, INK,
    ha="right", st="italic")

out = "piezas/instituto-productividad/arquitectura-del-dia.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
print("ok", out)
