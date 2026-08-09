# Para pegar a las 00:00 · Clase del martes 25 de agosto

Dos archivos, listos para pegar en GHL. Están **fijados a la clase B**: la del 10 de agosto ya no
está cargada, así que desde el momento en que los pegás, todo el tráfico entra a la del 25.

| Archivo | Dónde va |
|---|---|
| `index.html` | Custom code de la **landing de registro** |
| `thank-you.html` | Custom code de la **página de gracias** |

En los dos, copiá **de marcador a marcador**:
`<!-- DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL -->` … `<!-- HASTA ACÁ -->`
Reemplazá el bloque entero, no edites pedazos.

---

## Qué queda distinto respecto de la versión que está al aire hoy

| | Hoy (clase del 10) | Al pegar esto (clase del 25) |
|---|---|---|
| Título | Cumplís con todos menos con vos | **Escalá tu vida, no tu cansancio** |
| Bajada | la razón por la que tu cerebro ejecuta lo ajeno | la razón por la que el que sostiene todo es el último en avanzar |
| Fecha y contador | lunes 10 de agosto | **martes 25 de agosto**, 19:00 ART |
| Campaña (UTM) | `clase-ago10-cumplis-con-todos` | `clase-ago25-escala-tu-vida` |
| `clase_fecha` en el form | 2026-08-10 | **2026-08-25** |
| Grupo de WhatsApp | clase-10-08-neurociencia-aplicada | **clase-neurociencia-25-08-escala-tu-vida** |

El resto —diseño, secciones, form, pixel, UTM, testimonios— es idéntico.

---

## Lo que hay que revisar después de pegar

1. **La landing:** que el contador apunte al 25 y que el título diga *Escalá tu vida, no tu cansancio*.
2. **La thank you page:** que el botón verde lleve a `clase-neurociencia-25-08-escala-tu-vida`.
   Hacé clic y fijate a qué grupo entra, no lo des por hecho.
3. **Que no se vea ningún `[[` ni `{{`** en pantalla. Si aparece, el editor de GHL volvió a tocar los
   placeholders — avisame.
4. **Un lead de prueba** para confirmar que el contacto llega con `clase_fecha = 2026-08-25`.

---

## Después del 25 a las 19:00

Estos archivos siguen andando solos: pasan al martes siguiente (1 de septiembre) con el tema A y la
fecha nueva, y así todas las semanas. La URL nunca queda con fecha vencida.

Lo único que **no** se resuelve solo es el grupo de WhatsApp: las clases que se generan automáticamente
no tienen el suyo cargado, así que el botón cae en `WA_FALLBACK`. Antes del 25 a la noche, cargá el
grupo de la clase siguiente en el bloque `CLASES` de `thank-you.html`.

---

## Cómo se generaron

Salen de `../index.html` y `../thank-you.html` cambiando sólo: el bloque `CLASES`, los textos estáticos
del hero y del `<head>` (para que el preview del link y el primer pintado ya muestren el tema B), y el
link del grupo. **28 líneas de diferencia en la landing y 23 en la thank you page**, nada más.

Si cambiás algo en los archivos de arriba, hay que volver a generar estos dos.
