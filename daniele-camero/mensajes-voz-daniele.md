# Mensajes de ManyChat en la voz de Daniele

Basado en 56 transcripciones de su canal de YouTube "El Origen" (unas 286.000 palabras). Este archivo reemplaza los textos de `flujo-manychat.md` y de `paso-ia-manychat.md`.

## Vocabulario: qué dice él y qué no
| Usar (lo dice él) | Veces en sus videos | En vez de (no lo dice o casi nunca) |
|---|---|---|
| **multiplicar tus resultados** | 28 | "siguiente nivel" (3) · "desbloquear" (1) |
| **punto ciego** | 30 | — (ya lo usábamos, queda) |
| **lo que te está deteniendo** | 18 | "lo que te frena" |
| **techo invisible** / **termostato financiero** | 8 / 29 | "techo financiero" |
| **estancado** | 45 | "me estanqué" (queda igual en espíritu) |
| **tu mejor versión** | 36 | — |
| **riqueza real** / **riqueza integral** (en cada área de tu vida) | 81 / 48 | "nivel económico" |
| **reprogramar tu mente** | 99 | — (es público, se puede usar) |
| **calificar** ("vemos si puedes calificar") | 80 | "ver si es para ti" |
| **mi equipo** | 76 | — |
| **"no necesitas una nueva estrategia, no necesitas más conocimiento"** | — | nuestro "probé muchos cursos" |
| siempre **tú** | — | nunca vos |

No usar: "autosabotaje" (lo dicen los leads, él nunca), "quinta dimensión" (solo 3 veces, es de adentro del programa), "papá" (lo dice en video, no en DM).

---

## Bienvenida: 4 variantes para testear
Con el randomizador, 25% cada una, y etiquetas `bienvenida_v1` … `bienvenida_v4`.

**V1 · Punto ciego**
> ¡Hola! Te doy la bienvenida 🙌 A mis nuevos seguidores les estoy regalando un entrenamiento para identificar el punto ciego que te está deteniendo de multiplicar tus resultados. Responde unas preguntas rápidas y te lo envío 👇

Botón: **QUIERO VERLO 👀**

**V2 · Techo invisible**
> ¡Hola! Bienvenido 🙌 Si sientes que estás estancado, que hay un techo invisible que no te deja crecer aunque hagas todo bien, preparé un entrenamiento para ti. Responde unas preguntas rápidas y te lo envío 👇

Botón: **ROMPER MI TECHO 🚀**

**V3 · Termostato financiero**
> ¡Hola! Qué bueno tenerte aquí 🙌 Tu mente tiene un termostato financiero que decide cuánto dinero generas, ni más ni menos. Te preparé un entrenamiento para reprogramarlo. Responde 3 preguntas rápidas y te lo envío 👇

Botón: **QUIERO EL MÍO 👉**

**V4 · Calificar**
> ¡Bienvenido! 🎁 No todo el mundo califica para trabajar conmigo, pero a todos mis nuevos seguidores les regalo un entrenamiento para construir riqueza real. Responde unas preguntas rápidas y te lo envío 👇

Botón: **RECIBIR MI REGALO 🎁**

**Recordatorio** (si no toca el botón en 3 h)
> ¿Seguimos? Tu entrenamiento te está esperando 👇

---

## Filtro
> Para empezar: ¿cómo están hoy tus resultados?
> 1️⃣ Genero bien, pero estoy estancado: hay un techo invisible que no me deja multiplicar mis resultados
> 2️⃣ Genero, pero no logro sostenerlo: un mes subo y al otro vuelvo a bajar
> 3️⃣ Estoy empezando de cero o saliendo de deudas

| Botón | Etiqueta | `p1_respuesta` | Ruta |
|---|---|---|---|
| 1. Estoy estancado | `p1_techo` | Estancado, con un techo invisible | HT |
| 2. Subo y bajo | `p1_variable` | Genera pero no lo sostiene | HT |
| 3. Empezando/deudas | `p1_dificil` | Empezando o con deudas | LT |

## Preguntas abiertas
**1 · Situación** → `ocupacion`
> Cuéntame un poco de ti: ¿a qué te dedicas hoy? (negocio, empleo, trading… cualquier herramienta que uses para generar capital)

**2 · Tu mejor versión** → `objetivo_90d`
> Imagina que pasan 90 días y ya estás viviendo tu mejor versión. ¿Qué resultados estás viendo?

**3 · Punto ciego** → `freno`
> ¿Y qué sientes que te está deteniendo hoy? Ese punto ciego que no te deja multiplicar tus resultados.

---

## Rama HT: mensaje con el botón al mini VSL
> Gracias {nombre} 🙌 Con lo que me contaste te preparé esto: dónde estás hoy, a dónde quieres llegar y el punto ciego que te está deteniendo. Míralo completo 👇
> [Ver mi video]

Seguimiento (lo manda la setter o se automatiza a las ~6 h):
> ¿Pudiste verlo? Si sientes que es para ti, escríbeme aquí y con mi equipo vemos si puedes calificar para trabajar conmigo.

## Rama LT
**Audio** (guion para que lo grabe Daniele o alguien del equipo):
> Hola {nombre}, vi tus respuestas. Te quiero compartir un entrenamiento donde te explico cómo funciona tu termostato financiero y por qué, aunque trabajes duro, sigues generando lo mismo. Míralo completo, que ahí está la llave.

**Mensaje con la clase:**
> Aquí lo tienes 👉 [LINK_CLASE_LARGA]
> Se estrena hoy a las 7 de la noche 🕖

**Oferta** (~20 h después, dentro de la ventana de 24 h de Instagram):
> Si quieres seguir reprogramando tu mente conmigo cada semana, te espero en Sociedad Élite 👉 [LINK_CHECKOUT_LT]

---

## Paso de IA: ajustes al prompt
En el prompt de `ia_datos` (archivo `paso-ia-manychat.md`), reemplazar las reglas de estilo por estas:
```
- Escribe en segunda persona (tú), con el vocabulario de Daniele Camero: "estás estancado", "techo invisible", "multiplicar tus resultados", "punto ciego", "lo que te está deteniendo", "tu mejor versión".
- No uses "siguiente nivel", "desbloquear", "autosabotaje" ni "vos".
```
