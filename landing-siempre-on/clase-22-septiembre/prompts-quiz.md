# Prompts de imagen para las opciones del quiz

Cada opción del quiz lleva una imagen chica (cuadrada, se ve a 64–72 px de lado) a la izquierda del texto,
para que la persona se reconozca en un vistazo antes de leer. Son tres escenas de la misma serie: mismo
estilo, misma luz, distinto momento de vida.

## Reglas para las tres

1. **Cuadradas, 1:1.** Se recortan a un cuadrado chico, así que el sujeto va al centro y ocupa el cuadro.
   Nada importante en los bordes.
2. **Un solo sujeto, sin detalles chicos.** A 64 px, el detalle desaparece. Lo que tiene que leerse es la
   silueta, la luz y un objeto.
3. **Sin caras.** De espaldas, de perfil recortado o manos. Si aparece una cara, la persona compara en vez
   de proyectarse.
4. **Misma paleta:** azul profundo, grises fríos, un acento naranja o cálido por imagen. Luz natural o de
   lámpara, nunca neón.
5. **Estilo foto, no ilustración.** 35 mm, poca profundidad de campo, grano leve. Sin texto en la imagen.
6. **Ninguna tiene que parecer "peor" que otra.** La C es un punto de partida, no un fracaso: luz de
   mañana, orden, energía.

Bloque de estilo para pegar al principio de cada prompt:

```
Photorealistic photograph, square 1:1, single subject centred, no visible face, no text, no logos.
35mm lens, shallow depth of field, slight film grain. Colour palette: deep navy and cool greys with one
warm orange accent. Must read clearly as a tiny thumbnail: strong silhouette, simple background.
```

---

## Pregunta 1 · ¿En qué etapa estás hoy?

### Opción A · "Construí un sostén económico y una trayectoria… lo que me preocupa es lo que me está costando sostenerlo"

Lo que tiene que transmitir: *lo logré, y me pesa*. Éxito visible, cuerpo cansado.

```
[bloque de estilo]
A man in his late 40s seen from behind, standing alone at the floor-to-ceiling window of a quiet
corner office at night, city lights out of focus below. Suit jacket off, sleeves rolled, one hand
pressing the back of his neck. On the desk beside him, slightly blurred: a closed laptop and a framed
family photo turned toward the chair. Warm desk lamp is the only orange accent. Mood: he has everything
he built, and it is heavy.
```

### Opción B · "Tengo una carrera armada y estoy en etapa de seguir creciendo… me está costando desvelos, irritabilidad y tiempo"

Lo que tiene que transmitir: *estoy subiendo, y no duermo*. Crecimiento y desvelo en el mismo cuadro.

```
[bloque de estilo]
A person in their mid 30s seen from behind, sitting up in bed at night with a laptop open on their
knees, the screen glow lighting the room blue. On the nightstand, in focus: a phone showing a lit
screen and a bedside clock reading 01:40 in warm orange digits. The other side of the bed is occupied
and asleep, out of focus. Mood: the growth is real, and it is costing the night.
```

### Opción C · "Todavía estoy construyendo mi sostén profesional y económico. Estoy en un punto de partida"

Lo que tiene que transmitir: *estoy arrancando, con ganas*. Sin lástima: luz, orden, empuje.

```
[bloque de estilo]
A young professional in their late 20s seen from behind, at a small tidy desk by a bright window in the
morning, laptop open, a paper notebook with a hand-drawn plan beside it, a coffee cup, a small plant.
Clean light, energy, a fresh start. The orange accent is a single sticky note on the wall. Mood:
beginning, ambitious, nothing heavy yet.
```

---

## Pregunta 2 · ¿Hay gente cuyo trabajo depende de tus decisiones?

Misma serie que las de arriba: quien lidera una organización, después un equipo chico, después una persona trabajando sola.

### Opción A · "Sí, un equipo o una empresa a cargo"

```
[bloque de estilo]
Seen from behind the head of a long boardroom table: a person standing, one hand resting on the table,
addressing six or seven people who are seated and out of focus. Large window light, navy walls, one
orange folder on the table. Mood: many people are waiting for what this person decides.
```

### Opción B · "Sí, algunas personas"

```
[bloque de estilo]
Seen from behind: a person at a small round table with two colleagues, one laptop open between them,
pointing at the screen. Bright office or café, shallow depth of field, an orange mug as the accent.
Mood: a small team, decisions taken together, this person leads it.
```

### Opción C · "Todavía no"

```
[bloque de estilo]
Seen from behind: a single person working alone at a clean desk with headphones on, laptop open, a
window with daylight. No other people in frame. Orange accent: the headphones. Mood: focused, solo,
building.
```

---

## Cómo se cargan en la landing

Cada opción del quiz en `index.html` ya tiene el lugar de la imagen, oculto hasta que exista:

```html
<span class="nfm-opt__img" hidden><img src="PEGAR-URL" alt=""></span>
```

Cuando tengas la imagen subida a WordPress o a GHL: pegás la URL en el `src` y borrás la palabra
`hidden`. Con eso aparece el cuadrado a la izquierda del texto, en celular y en escritorio. Subilas en
**400 × 400 px, JPG**: alcanza de sobra para el tamaño en que se ven y pesan poco.
