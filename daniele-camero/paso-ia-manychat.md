# Paso de IA en ManyChat → link personalizado al mini VSL

## Cómo funciona
```
Filtro (botón) + 3 preguntas abiertas
   → Paso IA 1: ia_datos    (para el link, corto y limpio)
   → Paso IA 2: ia_resumen  (para la setter, legible)
   → Botón "Ver mi video" con el link armado (los datos no se ven)
   → Página: punto A → punto ciego → punto B + video
```

## Campos nuevos (texto)
| Campo | Lo llena | Para qué |
|---|---|---|
| `p1_respuesta` | cada botón del filtro ("En un techo" / "No lo sostengo" / "Empezando o con deudas") | que la IA sepa qué eligió |
| `ia_datos` | Paso IA 1 | va dentro del link |
| `ia_resumen` | Paso IA 2 | lo lee la setter |

Los campos que ya existen: `ocupacion`, `objetivo_90d`, `freno`.

---

## Paso IA 1 → `ia_datos`
Usar la acción de IA de ManyChat (integración de OpenAI o paso de IA) y guardar la respuesta en `ia_datos`.

**Prompt:**
```
Eres un asistente que ordena las respuestas de un lead de Instagram para el equipo de Daniele Camero (mentor de desarrollo personal y riqueza).

Respuestas del lead:
- Nivel elegido: {{p1_respuesta}}
- Situación actual / a qué se dedica: {{ocupacion}}
- Qué quiere lograr en 90 días: {{objetivo_90d}}
- Qué siente que lo frena: {{freno}}

Devuelve UNA sola línea con 5 partes separadas por | en este orden:
ocupacion|punto_a|punto_ciego|punto_b|SI

Reglas:
- ocupacion: a qué se dedica, máximo 8 palabras (ej: Contador en un estudio y trading en paralelo).
- punto_a: dónde está hoy, en segunda persona (tú), máximo 15 palabras. Combina el nivel elegido con su situación.
- punto_ciego: lo que siente que lo frena, en segunda persona, máximo 12 palabras, con sus palabras.
- punto_b: lo que quiere lograr en 90 días, en segunda persona, máximo 15 palabras.
- Usa SOLO lo que dijo el lead. No inventes números, nombres ni metas. Corrige ortografía.
- Si alguna respuesta está vacía, es un chiste, un insulto, spam, no tiene sentido o no responde la pregunta, devuelve exactamente: NO
- Prohibido usar estos caracteres: | (salvo como separador) & # ? = + % " ' emojis y saltos de línea.
- No agregues ningún texto antes ni después.

Ejemplo de salida válida:
Contador en un estudio y trading en paralelo|Generas bien pero hace dos años que estás en el mismo techo|Sabes qué hacer pero el miedo te hace autosabotearte|Ser consistente en trading y dejar el estudio antes de fin de año|SI
```

## Paso IA 2 → `ia_resumen` (para la setter)
```
Resume para una setter de ventas, en máximo 5 líneas, lo que dijo este lead.

- Nivel: {{p1_respuesta}}
- Situación actual: {{ocupacion}}
- Objetivo 90 días: {{objetivo_90d}}
- Qué lo frena: {{freno}}

Formato:
Ocupación: ...
Punto A: ...
Punto B: ...
Punto ciego: ...
Señales: (marca solo las que aplican)
🟢 tiene empleo o profesión + proyecto propio en paralelo
🟢 pone el freno adentro (miedo, autosabotaje, techo, identidad)
🟡 busca estrategia o "el método"
🟡 menciona plata no disponible (cobros, deudas, vender algo)
🟡 menciona decidir con pareja o socio
🔴 respuestas sin sentido o vacías

No inventes nada que no esté en las respuestas.
```

---

## El botón
- **Condición:** si `ia_datos` = NO (o vacío) → botón con el link sin datos (la página muestra la versión general).
- **Si no:** botón **"Ver mi video"** con este link (insertar los campos con el selector de campos de ManyChat):
```
https://TU-DOMINIO/vsl?utm_source=instagram&utm_medium=manychat&utm_campaign=ht#n={{first_name}}&d={{ia_datos}}
```
- Los datos van **después del #**. Así no viajan al servidor ni quedan en los logs. Las UTM quedan normales para medir.
- Va en un botón, así que el lead no ve el link largo.

## Mensaje con el botón (rama HT)
> Gracias {nombre} 🙌 Con lo que me contaste te preparé esto: tu punto A, tu punto B y el video que explica cómo pasar de uno al otro 👇
> [Ver mi video]

## Cómo probar
1. Hacer la encuesta con respuestas reales → el botón tiene que abrir la página con tus datos.
2. Hacerla con respuestas sin sentido ("asdf") → `ia_datos` = NO → la página general.
3. Probar con acentos y ñ → que se vean bien. Si ManyChat no codifica el link y algo se rompe, avisame y cambiamos el formato.

## Para subir la página
En `vsl-personalizada.html`, arriba del todo en el `<script>`:
- `DEMO = false`
- `VIDEO_EMBED_URL` = link de embed del video (Vimeo o YouTube)
- `CALENDAR_URL` = link de agenda

---

## Texto para pasarle a Claude in Chrome (agregar al flujo que está armando)
```
Agregá esto al flujo "Filtro Leads – Techo financiero (v1)", sin activar nada:

1. Creá los campos de texto p1_respuesta, ia_datos, ia_resumen.
2. En cada botón del filtro, además de las etiquetas, guardá en p1_respuesta: "En un techo" / "No lo sostengo" / "Empezando o con deudas".
3. Después del Mensaje 5 (punto ciego), agregá dos acciones de IA:
   - IA 1 → guardar respuesta en ia_datos (prompt que te paso abajo).
   - IA 2 → guardar respuesta en ia_resumen (prompt que te paso abajo).
4. En la Rama HT, reemplazá el mensaje con el link del VSL por:
   - Condición: si ia_datos es "NO" o está vacío → mensaje con botón "Ver mi video" y link https://TU-DOMINIO/vsl?utm_source=instagram&utm_medium=manychat&utm_campaign=ht
   - Si no → mismo mensaje con botón "Ver mi video" y link https://TU-DOMINIO/vsl?utm_source=instagram&utm_medium=manychat&utm_campaign=ht#n={{first_name}}&d={{ia_datos}} (insertando los campos con el selector de ManyChat, no escritos a mano).
   Texto del mensaje: "Gracias {nombre} 🙌 Con lo que me contaste te preparé esto: tu punto A, tu punto B y el video que explica cómo pasar de uno al otro 👇"
5. En la notificación a la setter, usá {{ia_resumen}} en lugar de los 3 campos sueltos.
6. Probá con la cuenta de prueba: una vez con respuestas reales y otra con "asdf". Mandame captura de los valores de ia_datos e ia_resumen en las dos y del link que abre el botón.
Si la acción de IA de ManyChat no está disponible o pide una API key, pará y preguntame.

[pegar acá los dos prompts de IA de este documento]
```
