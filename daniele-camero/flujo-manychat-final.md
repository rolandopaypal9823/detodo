# Flujo ManyChat FINAL (voz de Daniele)

Versión que reemplaza a todas las anteriores. Siempre de **tú**.

## Mapa
```
TRIGGER (bienvenida / palabra clave) → etiqueta origen_…
 └ RANDOMIZADOR 25/25/25/25 → Bienvenida V1 | V2 | V3 | V4  (etiqueta bienvenida_v1…v4)
    └ FILTRO (botones) → etiqueta p1_… + ruta_ht / ruta_lt + campo p1_respuesta
       └ PREGUNTA 1 situación    → campo ocupacion
       └ PREGUNTA 2 mejor versión → campo objetivo_90d
       └ PREGUNTA 3 punto ciego   → campo freno     → etiqueta encuesta_completa
          └ IA 1 → ia_datos   ·   IA 2 → ia_resumen
             └ CONDICIÓN ruta_ht ?
                ├ SÍ → RAMA HT: botón "Ver mi video" (link con datos) + aviso a la setter
                └ NO → RAMA LT: audio + clase + oferta Sociedad Élite (sin setter)
```

## Campos (texto) y etiquetas
- **Campos:** `p1_respuesta`, `ocupacion`, `objetivo_90d`, `freno`, `ia_datos`, `ia_resumen`
- **Etiquetas:**
  - `origen_bienvenida`, `origen_<palabra>`
  - `bienvenida_v1`, `bienvenida_v2`, `bienvenida_v3`, `bienvenida_v4`
  - `p1_techo`, `p1_variable`, `p1_dificil`
  - `ruta_ht`, `ruta_lt`, `encuesta_completa`

---

## 1. Bienvenida (randomizador, 4 variantes)

**V1 · Punto ciego** → etiqueta `bienvenida_v1`
> ¡Hola! Te doy la bienvenida 🙌 A mis nuevos seguidores les estoy regalando un entrenamiento para identificar el punto ciego que te está deteniendo de multiplicar tus resultados. Responde unas preguntas rápidas y te lo envío 👇

Botón **QUIERO VERLO 👀**

**V2 · Techo invisible** → `bienvenida_v2`
> ¡Hola! Bienvenido 🙌 Si sientes que estás estancado, que hay un techo invisible que no te deja crecer aunque hagas todo bien, preparé un entrenamiento para ti. Responde unas preguntas rápidas y te lo envío 👇

Botón **ROMPER MI TECHO 🚀**

**V3 · Termostato** → `bienvenida_v3`
> ¡Hola! Qué bueno tenerte aquí 🙌 Tu mente tiene un termostato financiero que decide cuánto dinero generas, ni más ni menos. Te preparé un entrenamiento para reprogramarlo. Responde 3 preguntas rápidas y te lo envío 👇

Botón **QUIERO EL MÍO 👉**

**V4 · Calificar** → `bienvenida_v4`
> ¡Bienvenido! 🎁 No todo el mundo califica para trabajar conmigo, pero a todos mis nuevos seguidores les regalo un entrenamiento para construir riqueza real. Responde unas preguntas rápidas y te lo envío 👇

Botón **RECIBIR MI REGALO 🎁**

**Recordatorio** si no toca el botón en 3 h (una sola vez, con el mismo botón):
> ¿Seguimos? Tu entrenamiento te está esperando 👇

## 2. Filtro
> Para empezar: ¿cómo están hoy tus resultados?
> 1️⃣ Genero bien, pero estoy estancado: hay un techo invisible que no me deja multiplicar mis resultados
> 2️⃣ Genero, pero no logro sostenerlo: un mes subo y al otro vuelvo a bajar
> 3️⃣ Estoy empezando de cero o saliendo de deudas

| Botón | Etiquetas | `p1_respuesta` |
|---|---|---|
| **1. Estoy estancado** | `p1_techo` + `ruta_ht` | Estancado, con un techo invisible |
| **2. Subo y bajo** | `p1_variable` + `ruta_ht` | Genera pero no lo sostiene |
| **3. Empezando/deudas** | `p1_dificil` + `ruta_lt` | Empezando o con deudas |

Recordatorio si no responde en 3 h (una vez): "¿Seguimos? 👇" con los mismos botones.

## 3. Preguntas abiertas (entrada de usuario, texto)
Si no responde en 12 h, el flujo sigue igual al paso siguiente.

**P1 → `ocupacion`**
> Cuéntame un poco de ti: ¿a qué te dedicas hoy? (negocio, empleo, trading… cualquier herramienta que uses para generar capital)

**P2 → `objetivo_90d`**
> Imagina que pasan 90 días y ya estás viviendo tu mejor versión. ¿Qué resultados estás viendo?

**P3 → `freno`**
> ¿Y qué sientes que te está deteniendo hoy? Ese punto ciego que no te deja multiplicar tus resultados.

Acción después de P3: etiqueta `encuesta_completa`.

## 4. Paso IA 1 → `ia_datos`
```
Eres un asistente que ordena las respuestas de un lead de Instagram para el equipo de Daniele Camero (mentor de desarrollo personal y riqueza real).

Respuestas del lead:
- Nivel elegido: {{p1_respuesta}}
- A qué se dedica: {{ocupacion}}
- Qué resultados quiere ver en 90 días: {{objetivo_90d}}
- Qué siente que lo está deteniendo: {{freno}}

Devuelve UNA sola línea con 5 partes separadas por | en este orden:
ocupacion|punto_a|punto_ciego|punto_b|SI

Reglas:
- ocupacion: a qué se dedica, máximo 8 palabras.
- punto_a: dónde está hoy, máximo 15 palabras. Combina el nivel elegido con su situación.
- punto_ciego: lo que lo está deteniendo, máximo 12 palabras, con sus palabras.
- punto_b: los resultados que quiere ver en 90 días, máximo 15 palabras.
- Escribe en segunda persona (tú), con el vocabulario de Daniele Camero: "estás estancado", "techo invisible", "multiplicar tus resultados", "punto ciego", "lo que te está deteniendo", "tu mejor versión". No uses "siguiente nivel", "desbloquear", "autosabotaje" ni "vos".
- Usa SOLO lo que dijo el lead. No inventes números, nombres ni metas. Corrige ortografía.
- Si alguna respuesta está vacía, es un chiste, un insulto, spam, no tiene sentido o no responde la pregunta, devuelve exactamente: NO
- Prohibido usar estos caracteres: | (salvo como separador) & # ? = + % " ' emojis y saltos de línea.
- No agregues ningún texto antes ni después.

Ejemplo de salida válida:
Contador en un estudio y trading en paralelo|Generas bien pero hace dos años que estás estancado|El miedo a equivocarte te está deteniendo|Ser consistente en trading y dejar el estudio antes de fin de año|SI
```

## 5. Paso IA 2 → `ia_resumen` (para la setter)
```
Resume para una setter de ventas, en máximo 5 líneas, lo que dijo este lead.

- Nivel: {{p1_respuesta}}
- A qué se dedica: {{ocupacion}}
- Resultados que quiere en 90 días: {{objetivo_90d}}
- Qué lo está deteniendo: {{freno}}

Formato:
Ocupación: ...
Punto A: ...
Punto B: ...
Punto ciego: ...
Señales: (marca solo las que aplican)
🟢 tiene empleo o profesión + proyecto propio en paralelo
🟢 pone lo que lo detiene adentro (miedo, creencias, identidad, techo)
🟡 busca una estrategia o "el método"
🟡 menciona plata no disponible (cobros, deudas, vender algo)
🟡 menciona decidir con pareja o socio
🔴 respuestas sin sentido o vacías

No inventes nada que no esté en las respuestas.
```

## 6. Condición
- Tiene la etiqueta `ruta_ht` → **Rama HT**
- Si no → **Rama LT**

## 7. Rama HT
**Condición interna:** si `ia_datos` = NO o está vacío → link sin datos. Si no → link con datos.

**Mensaje:**
> Gracias {{first_name}} 🙌 Con lo que me contaste te preparé esto: dónde estás hoy, a dónde quieres llegar y el punto ciego que te está deteniendo. Míralo completo 👇

Botón **Ver mi video**:
- **Con datos:** `https://TU-DOMINIO/vsl?utm_source=instagram&utm_medium=manychat&utm_campaign=ht#n={{first_name}}&d={{ia_datos}}`
- **Sin datos:** `https://TU-DOMINIO/vsl?utm_source=instagram&utm_medium=manychat&utm_campaign=ht`

(Insertar los campos con el selector de ManyChat, no escritos a mano.)

**Acción:** notificar al admin y asignar la conversación a la setter con el texto: `Lead HT · {{ia_resumen}}`

**Seguimiento a las 6 h** (si no escribió):
> ¿Pudiste verlo? Si sientes que es para ti, escríbeme aquí y con mi equipo vemos si puedes calificar para trabajar conmigo.

## 8. Rama LT (sin setter)
**Audio** (lo graba Daniele o alguien del equipo):
> Hola {nombre}, vi tus respuestas. Te quiero compartir un entrenamiento donde te explico cómo funciona tu termostato financiero y por qué, aunque trabajes duro, sigues generando lo mismo. Míralo completo, que ahí está la llave.

**Mensaje:**
> Aquí lo tienes 👉 [LINK_CLASE_LARGA]
> Se estrena hoy a las 7 de la noche 🕖

**Demora de 20 h** (no pasar de 23 h: ventana de 24 h de Instagram). Después:
> Si quieres seguir reprogramando tu mente conmigo cada semana, te espero en Sociedad Élite 👉 [LINK_CHECKOUT_LT]

---

## Para pegarle a Claude in Chrome
```
Vamos a actualizar el flujo "Filtro Leads – Techo financiero (v1)" en ManyChat. Primero duplicalo y renombrá la copia como "Filtro Leads – Voz Daniele (v2)". Trabajá solo sobre la copia, no actives nada y pedime confirmación antes de cualquier paso irreversible.

Aplicá exactamente lo que dice el documento que te pego abajo:
1. Creá los campos y etiquetas que falten (si ya existen, reutilizalos).
2. Reemplazá la bienvenida por un randomizador 25/25/25/25 con las 4 variantes; cada una pone su etiqueta bienvenida_v1…v4.
3. Reemplazá los textos del filtro, de los botones y de las 3 preguntas abiertas. Cada botón del filtro guarda además p1_respuesta.
4. Actualizá el prompt de IA 1 (ia_datos) y agregá IA 2 (ia_resumen) si no existe.
5. Rama HT: mensaje nuevo, botón "Ver mi video" con la condición de ia_datos, notificación a la setter con {{ia_resumen}} y el seguimiento a las 6 h.
6. Rama LT: audio, clase, demora de 20 h y oferta de Sociedad Élite.
7. Si un botón supera el límite de caracteres de Instagram, abrevialo manteniendo el número y anotalo.
8. Probá con la cuenta de prueba: una vez por cada variante de bienvenida, una vez por HT y otra por LT, y una vez con respuestas sin sentido ("asdf"). Mandame capturas de las etiquetas, de los campos (sobre todo ia_datos e ia_resumen) y del link que abre el botón.
Al final, mandame una captura del flujo completo y la lista de lo que cambiaste.

[pegar acá todo este documento]
```
