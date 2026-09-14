# Prompts para las 6 escenas de Nico (GIF o foto)

La sección "Nicolás Fernández Miranda" de la landing del 22 cuenta la historia en seis escenas. Cada escena
tiene un recuadro de imagen (proporción **4:3**) que hoy muestra un placeholder gris. Este archivo tiene, por
escena: qué foto real serviría, y un prompt listo para pegar en ChatGPT por si no la tenés.

**Prioridad: foto real > imagen generada.** Las fotos verdaderas de Nico convierten más que cualquier
ilustración. Si tenés aunque sea una foto real por escena, usá esa y salteá el prompt.

---

## Reglas para todos los prompts

1. **Nunca generar la cara de Nico con IA.** Un rostro inventado que "se parece" destruye la confianza que la
   sección está construyendo. Por eso todos los prompts son de espaldas, de objetos, o de manos. Si se ve una
   persona, se ve de atrás o fuera de foco.
2. **Formato 4:3, horizontal.** Es la proporción del recuadro en la landing. Pedilo en cada prompt.
3. **Paleta de la marca.** Azules profundos (`#0c3452`, `#081f33`), grises fríos, y un solo acento naranja
   (`#FF6B00`) por imagen como máximo. Luz natural, nada de neón.
4. **Estilo fotográfico, no ilustración.** Lente de 35 o 50 mm, poca profundidad de campo, grano leve.
   Que parezca una foto tomada por alguien que estaba ahí, no un render.
5. **Sin texto dentro de la imagen.** El texto va en la landing, al lado.
6. **Sin lujo.** Sin relojes caros, autos, ni "mírenme". El arco es de credibilidad, no de aspiración.

Si querés GIF en vez de foto fija: generá la imagen con el prompt y después animala en un generador de
video (Runway, Pika, Kling o el que uses) con la indicación "**subtle camera push-in, 3 seconds, loop**".
Con ese movimiento mínimo alcanza; más movimiento distrae del texto.

Cómo se pega en la landing, escena por escena: buscá en `index.html` el bloque
`<div class="nfm-scene__ph">Escena N · GIF o foto</div>` y reemplazalo por
`<img src="URL-DE-LA-IMAGEN" alt="">` (o `<video autoplay muted loop playsinline src="URL"></video>` si es GIF
convertido a MP4, que pesa diez veces menos). El recuadro ya recorta y ajusta solo.

---

## Escena 1 · El contador que llegó rápido

**Texto que acompaña:** contador con medalla al mejor promedio, estudio propio, crecimiento rápido, los
medios lo llaman.

**Foto real ideal:** Nico joven en el estudio contable, o cualquier foto de esa época (una nota en un diario,
una entrevista temprana, la oficina). Si hay una captura de una nota de prensa de esos años, sirve tal cual.

**Prompt:**

```
Photorealistic editorial photograph, 4:3 horizontal. A young accountant seen from behind, seated at a desk
in a small professional office early in the morning, warm sunlight coming through a window. On the desk:
an overfull paper agenda, a ringing landline phone, stacks of folders, a calculator. The person is reaching
for the phone. Shallow depth of field, 35mm lens, natural light, slight film grain. Colour palette: deep
navy and cool greys with a single orange accent (a sticky note on the monitor). No visible face, no text,
no logos. Mood: fast, busy, promising.
```

---

## Escena 2 · El precio

**Texto que acompaña:** catorce horas por día, quince kilos, migrañas, pastillas como caramelos, clonazepam
para dormir, envidia de quien cierra la persiana a las seis.

**Foto real ideal:** la misma oficina de noche, o una foto de Nico de esa época que muestre el desgaste
(si existe y él está de acuerdo en usarla). Si no, esta es la escena donde más conviene el prompt de objetos.

**Prompt:**

```
Photorealistic photograph, 4:3 horizontal, night time. The same small office as before but now lit only by
a desk lamp and a monitor glow. In the foreground, slightly out of focus: an open blister pack of pills and
a half-empty glass of water next to a laptop. Through the office window in the background, across the
street, a shopkeeper is pulling down the metal shutter of a small store, warmly lit, going home. Shallow
depth of field, 50mm lens, slight film grain. Palette: deep navy shadows, cold blue screen light, one warm
orange glow from the shop across the street. No visible faces, no text. Mood: slow, heavy, quiet.
```

---

## Escena 3 · París

**Texto que acompaña:** mejor año de facturación, el viaje a Europa que siempre postergó, y en París no
podía disfrutarlo. Ya tenía el máster en neurociencia y no se lo aplicaba.

**Foto real ideal:** **esta es la más importante para tener real.** Si Nico tiene una foto de ese viaje a
París, aunque sea mala, va esa. Una foto real de él en París vale más que las otras cinco juntas, porque es
la prueba de que la escena pasó.

**Prompt (si no hay foto):**

```
Photorealistic travel photograph, 4:3 horizontal, late afternoon in Paris. A man seen from behind, standing
on a bridge over the Seine with the Eiffel Tower soft and out of focus in the distance. He is looking down
at his phone, shoulders slightly hunched, not at the view. Around him, other people are looking up and
taking photos of the city. Golden hour light, 35mm lens, shallow depth of field on the phone and hands.
Palette: warm stone and soft blue sky, muted; no strong colours. No visible face, no text. Mood: he is in
the place he dreamed of and he is somewhere else.
```

---

## Escena 4 · La pregunta

**Texto que acompaña:** volvió obsesionado con una sola pregunta: cómo seguir creciendo y al mismo tiempo
avanzar con lo importante. Y descubrió que nunca había definido qué era lo importante.

**Foto real ideal:** un cuaderno real de Nico con la pregunta escrita a mano. Se puede hacer hoy en cinco
minutos con el celular: cuaderno, una sola línea escrita, luz de ventana. Es la foto más fácil de producir
de las seis y queda mejor real que generada.

**Prompt (si no hay foto):**

```
Photorealistic close-up photograph, 4:3 horizontal, top-down angle. An open notebook on a plain wooden
table by a window, natural daylight. On the page, a single handwritten line in dark ink, centred, the rest
of the page blank. The handwriting must be blurred just enough to be unreadable (no legible words). A pen
resting beside it. Nothing else on the table. 50mm lens, shallow depth of field, slight film grain.
Palette: cream paper, warm wood, cool grey shadows; one small orange detail (the pen cap). No text, no
faces. Mood: one question, nothing else.
```

> Ojo: los generadores escriben mal el castellano. Por eso el prompt pide la letra **desenfocada e
> ilegible**. Si querés que se lea la pregunta, hacé la foto real.

---

## Escena 5 · El laboratorio

**Texto que acompaña:** se convirtió en su propio experimento, midió, se equivocó, volvió a probar. El
contador que desaprobó matemáticas cuatro veces terminó dando clases en la universidad.

**Foto real ideal:** Nico dando clase en la universidad (aula, pizarrón, alumnos de espaldas), o una foto de
su escritorio real de esa época con planillas y lo que usaba para medir.

**Prompt (si no hay foto):**

```
Photorealistic photograph, 4:3 horizontal, morning light. A home desk that looks like a personal
experiment: an open laptop showing a blurred spreadsheet with charts, a paper notebook with hand-drawn
tables, an analog wristwatch lying on the desk, a pair of running shoes on the floor next to the chair, a
glass of water. Everything orderly and deliberate. Seen from a slight side angle, no person in frame.
35mm lens, natural window light, slight film grain. Palette: cool greys and deep navy with one orange
accent (the laces of the running shoes). No legible text, no logos. Mood: from the office to the lab.
```

---

## Escena 6 · Hoy

**Texto que acompaña:** fundó el Instituto de Productividad, más de cuatrocientos profesionales y líderes
mentoreados, autor bestseller, dos charlas TED, segundo libro en camino. Sigue tomando él mismo las primeras
llamadas.

**Foto real ideal:** **acá va sí o sí foto real.** Nico en el escenario TED, dando clase, o en conferencia.
Es el cierre del arco y es la única escena donde tiene que verse la cara. Cualquier foto de las charlas TED
o de una capacitación en empresa sirve. Si es la misma que va arriba en el hero, buscá otra distinta para
que no se repita.

**No hay prompt para esta escena a propósito.** Generar "un hombre en un escenario" para el cierre de una
historia real sería justo lo que rompe la confianza que las cinco escenas anteriores construyeron.

---

## Resumen de qué pedirle a Nico

| Escena | ¿Necesita foto real? | Qué pedirle |
|---|---|---|
| 1 | Opcional | Foto o nota de prensa de la época del estudio contable |
| 2 | Opcional | Nada (prompt de objetos alcanza) |
| 3 · París | **Sí, muy recomendable** | Cualquier foto del viaje a París |
| 4 | Fácil de hacer hoy | Cuaderno con la pregunta escrita a mano, foto con el celular |
| 5 | Opcional | Foto dando clase en la universidad, si existe |
| 6 · Hoy | **Obligatoria** | Foto en el escenario TED o en conferencia (distinta a la del hero) |
