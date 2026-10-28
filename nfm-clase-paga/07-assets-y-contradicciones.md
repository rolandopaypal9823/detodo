# Assets traídos del repo · y tres contradicciones que hay que zanjar

Barrido completo de las 29 ramas del repo para llenar los bloques que estaban
vacíos en `landing-v3-dan-henry.html` (bio, prensa, casos de éxito). Este
documento deja registrado **de dónde salió cada cosa** y **qué datos no
coinciden entre archivos**, para que nadie publique un número inflado.

---

## 1 · Lo que se integró a la landing

| Bloque | Fuente | Estado |
|---|---|---|
| Foto de Nico | `nicolasfernandezmiranda.com/wp-content/uploads/2025/04/nico-bio-card.jpg` (usada en `institutoproductividad.html`, `equipo-widget.html`) | URL de producción, no verificable desde este entorno (el proxy bloquea el dominio) |
| 8 logos de prensa | Bloque `.nfm-proof` de `landing-siempre-on/*/index.html` y `hackea-tu-cerebro-gira-2026.html` | Ídem — mismas URLs que ya corren al aire |
| 6 casos con video | `.claude/skills/nfm-super-skill/references/06_casos_exito_testimonios.md` (fuente maestra, 22 casos) | Frases **verbatim** de la fuente maestra |
| Grid de casos (CSS + click-to-load) | `tsl-a-larga.html` / `tsl-c-slides.html` | Reescrito con los tokens de esta landing |

### Los 6 casos elegidos y por qué

El criterio fue el **discriminador Platinum**: gente con personas a cargo,
dueños de negocio, o profesionales con trayectoria e ingresos.

| Caso | Perfil | Por qué entra | YouTube |
|---|---|---|---|
| **Germán** | Farmacéutico, dueño de farmacia familiar, 6 empleados | El discriminador Platinum más puro de los 22 | `jQ8AmqqiN_g` |
| **Celi** | Arquitecta en San Diego, lidera 45 personas, mamá | Liderazgo + carga familiar | `95H0-szcsMs` |
| **Cristian** | Bioquímico, laboratorio propio, empresario (Jujuy) | Empresario con empleados | `7x_hvNVvc88` |
| **Sol Romero** | Contadora, 10 años en impuestos, cía. de seguros | Espeja al avatar contable — y a Nico | `mVskd3R8hsc` |
| **Natalia** | Astrónoma CONICET + profesora + emprendedora, mamá de 2 | El número más duro: 3 h → 7-8 h de sueño | `CVo9A7ADvTs` |
| **Pierina** | Teóloga, doctoranda en Roma | **La variable aislada**: misma tesis, mismo output, la mitad de las horas | `vgF6e9MptW4` |

**Se sacó a Juan Jesús** de la versión anterior: es empleado + estudiante, no
tiene gente a cargo, y contradecía el perfil que buscamos.

---

## 2 · Tres contradicciones encontradas en el repo

### 2.1 · ⚠️ +400 vs +2.000 alumnos — factor 5x

| Número | Dónde aparece |
|---|---|
| **+2.000 alumnos acompañados** | `institutoproductividad.html`, `institutoproductividad-navy.html`, `instituto-booking.html` |
| **+400** | `landing-sesion-claridad/index.html`, `landing-siempre-on/clase-15-septiembre/index.html`, esta landing |

Tres archivos independientes y más recientes dicen 400; sólo la familia
`institutoproductividad*.html` dice 2.000.

**En la landing quedó +400** (el conservador). Si el número real es 2.000, se
cambia. Si es 400, hay tres páginas al aire con un número inflado 5x, y eso
frente a un avatar con alergia documentada al "vendehumo" es un pasivo, no un
activo. **Hay que zanjarlo con Nico.**

### 2.2 · ⚠️ Las frases de los widgets NO son verbatim

En `casos.json` y `casos-exito-widget.html` hay 14 casos con "frase" entre
comillas, y **al menos 8 de esas frases no figuran en la fuente maestra**. Son
paráfrasis editoriales presentadas como cita textual. Ejemplos:

| Caso | Widget (paráfrasis) | Fuente maestra (verbatim) |
|---|---|---|
| Celi | "El sistema correcto te permite rendir sin quemarte." | "Lo debería haber hecho 10 años antes." |
| Natalia | "Cuando dormís bien, todo lo demás empieza a acomodarse solo." | "Llegar a fin de año y levantar la copa: logré todo esto. El 1% te da eso." |
| Pierina | "Pasé de querer hacer todo y no poder nada, a hacer lo importante con claridad." | "Es una inversión para la vida…" |

**Esta landing usa sólo las verbatim.** Los widgets que corren al aire habría
que corregirlos: poner una cita que la persona no dijo es exactamente el
movimiento que este avatar castiga.

### 2.3 · ⚠️ Dos sistemas visuales paralelos en el repo

| Sistema | Tipografías | Dónde |
|---|---|---|
| **Oficial** (`biblia-estetica.html`) | Montserrat + Open Sans + JetBrains Mono | `institutoproductividad*.html`, `tsl-*`, widgets, **esta landing** |
| Alternativo | Space Grotesk + DM Sans | `landing-siempre-on/*`, `hackea-tu-cerebro-gira-2026.html` |

Los colores de marca se respetan en los dos. Pero son dos identidades
tipográficas distintas corriendo a la vez. **Esta landing sigue el oficial.**

Bonus: `equipo-widget.html` y `casos-exito-widget.html` declaran `'Space
Grotesk'` y `'Inter'` **sin cargarlas** — eso no es una decisión, es un bug.

---

## 3 · IDs de YouTube a verificar a mano

`casos.json` y la fuente maestra **no coinciden** en dos casos:

| Caso | `casos.json` | Fuente maestra |
|---|---|---|
| Jair | `7F5YjFM-EJY` | `S0XTipIlMsw` |
| Andrés | `0o-tzNPybNk` | `C6vf1vHDkJc` (1ª) / `w0lX8NFi7CY` (2ª) |

Ninguno de los dos está en esta landing, así que no bloquea. Los otros 12 IDs
coinciden entre ambas fuentes.

---

## 4 · Pendientes de datos

- `{{FECHA_LARGA}}` · `{{HORA}}` — fecha real de la clase
- `{{CAPITULO}}` — qué capítulo del libro va como bump
- Links de checkout (Stripe + Mercado Pago)
- Resolver +400 vs +2.000
- Confirmar que las URLs de imagen siguen vivas (no verificable desde este entorno)
