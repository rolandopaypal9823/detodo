# Flujo ManyChat: filtro de leads de Daniele Camero

Basado en el análisis de 30 llamadas (`analisis-patrones.md`).

## Mapa
```
Trigger (bienvenida / palabra clave)
  → Bienvenida + botón "Quiero el entrenamiento"
  → P1 Momento económico (botón)        ← LA QUE MÁS FILTRA
  → P2 ¿A qué te dedicás? (texto)       ← para el CSV y para la setter
  → P3 ¿Qué te frena? (botón)
  → P4 ¿Cuánto conocés a Daniele? (botón)
  → Condición → 🔥 CALIENTE / 🌤 TIBIO / ❄️ FRÍO
```
Si no responde en X horas: recordatorio "¿seguimos? 👇" con los mismos botones (como el flujo actual).

---

## 0. Bienvenida
> ¡Hola {nombre}! Bienvenido/a 🙌
> Como regalo de bienvenida te quiero compartir un entrenamiento gratuito para desbloquear tu próximo nivel económico.
> Para mandarte el que más te sirve, respondé 3 preguntas rápidas 👇

Botón: **Quiero el entrenamiento**

*Decir "nivel económico" y no "tu negocio": el comprador que más cierra es empleado o profesional con un proyecto en paralelo. Si le hablás solo de "negocio", queda afuera.*

## P1. Momento económico (botones)
> ¿En qué momento económico estás hoy?
> 1️⃣ Tengo buenos ingresos, pero siento que me estanqué
> 2️⃣ Genero, pero mis ingresos suben y bajan
> 3️⃣ Estoy en una etapa difícil (deudas / no me alcanza)

| Botón | Etiqueta |
|---|---|
| 1. Me estanqué | `p1_techo` |
| 2. Suben y bajan | `p1_variable` |
| 3. Etapa difícil | `p1_dificil` |

## P2. Ocupación (texto libre → campo `ocupacion`)
> ¿A qué te dedicás? Escribilo en una línea 👇
> (Si además tenés un negocio, trading o inversiones, contámelo también)

No define la ruta. Sirve para el CSV y para que la setter vea si tiene un proyecto en paralelo (el perfil que más compra).

## P3. Qué lo frena (botones)
> A la hora de crecer, ¿qué sentís que más te frena hoy?
> 1️⃣ Sé lo que tengo que hacer, pero algo interno me frena (miedo, autosabotaje)
> 2️⃣ Probé muchos cursos y estrategias y no encuentro la que funcione
> 3️⃣ Me falta capital o tiempo

| Botón | Etiqueta |
|---|---|
| 1. Algo interno | `p3_interno` |
| 2. Busco estrategia | `p3_estrategia` |
| 3. Capital/tiempo | `p3_capital` |

## P4. Cercanía con Daniele (botones)
> Última 🙌 ¿Cuánto conocés a Daniele?
> 1️⃣ Ya participé de algo suyo o me lo recomendó alguien que está adentro
> 2️⃣ Lo sigo hace meses
> 3️⃣ Lo descubrí hace poco

| Botón | Etiqueta |
|---|---|
| 1. Ya participé | `p4_cliente` |
| 2. Hace meses | `p4_seguidor` |
| 3. Recién lo conocí | `p4_nuevo` |

---

## Reglas de ruta (en este orden)
| Ruta | Condición | Etiqueta |
|---|---|---|
| ❄️ **FRÍO** | `p1_dificil` **o** `p3_capital` | `ruta_fria` |
| 🔥 **CALIENTE** | (`p1_techo` o `p1_variable`) **y** `p3_interno` **y** (`p4_cliente` o `p4_seguidor`) | `ruta_caliente` |
| 🌤 **TIBIO** | todo el resto | `ruta_tibia` |

Por qué (datos de las llamadas):
- P1 difícil → cerró 1 de 11.
- P1 techo o variable + conoce bien a Daniele → cerraron 5 de 7.
- El que busca estrategia o recién conoce a Daniele necesita calentarse antes de hablar con una closer.

## Qué recibe cada ruta

### 🔥 Caliente → setter + mini VSL
> Gracias {nombre} 🙌 Por lo que me contás, estás justo en el punto donde Daniele más ayuda.
> Te dejo este video corto 👉 [mini VSL]
> Y contame en 1 o 2 frases: ¿qué querés lograr en los próximos 90 días?

- Esperar respuesta de texto → notificar a la setter.
- Preguntas de la setter (lo que más trabó ventas en las llamadas):
  1. Liquidez: "Si vemos que el programa es para vos, ¿podés invertir en vos este mes o depende de algo (cobrar, vender, consultarlo)?"
  2. Si menciona pareja o socio → invitarlo a la llamada.
  3. Aclarar el formato (grupal o 1 a 1) antes de agendar.

### 🌤 Tibio → mini VSL automático + seguimiento
- Mismo video, sin setter.
- A las 24 h: "¿Lo pudiste ver? ¿Qué fue lo que más te resonó?"
- Si responde → `ruta_caliente` y pasa a la setter.

### ❄️ Frío → audio + clase larga → low ticket (sin setter)
- Audio: "Hola {nombre}, vi que respondiste la encuesta. Por lo que me contás, te quiero compartir este entrenamiento que te va a ayudar a…"
- Clase larga en landing ("se estrena hoy a las 19 h").
- A las 24-48 h → oferta directa de Sociedad Élite (150/mes o 300/trimestre).

---

## Métricas que vas a poder leer
Ejemplo con 1.000 personas que entran al trigger:
1. % que toca "Quiero el entrenamiento"
2. % que responde P1, y el reparto techo / variable / difícil → **% calificado de entrada**
3. Cantidad de `ruta_caliente`, `ruta_tibia`, `ruta_fria`
4. Después: agendas y cierres por ruta → para ajustar las reglas
5. Exportar el campo `ocupacion` a CSV → analizarlo acá (profesiones que llegan vs. las que compran)

---

## Versión con el lenguaje de los closers y de la marca

### Lo que ya preguntan los closers (guion de Rossi, en orden)
| # | Pregunta en la llamada | Aparece en |
|---|---|---|
| 1 | "Vamos a ver en qué situación te encuentras, qué quieres lograr y qué te ha estado frenando… y veré si cumples con los requisitos" | encuadre |
| 2 | "¿Qué te ha motivado a agendar esta llamada?" | 14 llamadas |
| 3 | "Vayamos que de aquí a 90-120 días nos tomamos un cafecito y me dices: Rossi, logré estos 3 objetivos. ¿Cuáles serían?" | 15 llamadas |
| 4 | "¿Qué es lo que te ha estado frenando?" / "ese punto ciego" | 17 / 16 llamadas |
| 5 | "¿Qué hace que quieras trabajar esto hoy y no de aquí a 3 meses?" | 9 llamadas |
| 6 | "De una escala del 1 al 10, ¿qué tan comprometido y prioritario es?" | 15 llamadas |
| 7 | "Tema de capacidad de inversión al día de hoy… ¿monto único o mensual?" | 14 llamadas |
| + | Sebastián: "¿En cuánto está ahorita tu techo financiero?" / "¿cuánto llevas tratando de romperlo?" | sus llamadas |

Palabras de la marca que más se repiten: identidad (24 llamadas), reprogramación (23), riqueza real (19), punto ciego (16), siguiente nivel, techo / termostato financiero. Los leads repiten solos "punto ciego", "siguiente nivel", "techo", "identidad".

### Mensajes reescritos
**Bienvenida**
> ¡Hola {nombre}! 🙌 Bienvenido/a. Te quiero regalar un entrenamiento para descubrir el punto ciego que hoy no te deja pasar a tu siguiente nivel. Para mandarte el que más te sirve, respondeme unas preguntas rápidas 👇
Botón: **Quiero el entrenamiento**

**Filtro: techo financiero** (reemplaza "momento económico")
> Para arrancar: ¿dónde está hoy tu techo financiero?
> 1️⃣ Genero bien, pero hace tiempo que estoy estancado en el mismo techo
> 2️⃣ Genero, pero todavía no logro sostenerlo: sube y baja
> 3️⃣ Hoy estoy empezando de cero o saliendo de deudas

| Botón | Etiqueta | Ruta |
|---|---|---|
| 1. Estoy en un techo | `p1_techo` | HT |
| 2. No lo sostengo | `p1_variable` | HT |
| 3. Empezando / deudas | `p1_dificil` | LT |

**Contexto 1: situación actual** → `ocupacion`
> Contame un poco de tu situación actual: ¿a qué te dedicás hoy? (si además tenés un negocio, trading o inversiones, contámelo también)

**Contexto 2: el cafecito de los 90 días** → `objetivo_90d`
> Imaginá que en 90 días nos tomamos un cafecito y me decís "lo logré". ¿Qué me estarías contando?

**Contexto 3: el punto ciego** → `freno`
> ¿Y cuál sentís que es hoy ese punto ciego que te viene frenando?

### Lo que NO conviene pasar al bot
- **Compromiso del 1 al 10:** en las llamadas casi todos dicen 10, también los que no compran (Alexander 10/10, Elvis "al 10"). No filtra.
- **Capacidad de inversión:** que lo pregunte la setter, no el bot.
- **"¿Por qué hoy y no en 3 meses?":** que lo pregunte la setter.
- **"Quinta dimensión", "reprogramación":** son palabras de adentro del programa. Un lead frío no las entiende.
