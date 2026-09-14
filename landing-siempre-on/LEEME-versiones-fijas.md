# Versiones fijas, una por clase

Cada carpeta tiene la landing y la thank you page **clavadas a una sola clase**. No rotan, no calculan
nada, no dependen de ninguna fecha: muestran siempre esa clase y ese grupo de WhatsApp, pase lo que pase.

| Carpeta | Clase | Tema | Título | Grupo de WhatsApp |
|---|---|---|---|---|
| `clase-15-septiembre/` | mar 15 sep, 19:00 | B | Escalá tu vida, no tu cansancio | `clase-15-de-septiembre-de-neurociencia` |
| `clase-22-septiembre/` | mar 22 sep, 19:00 | Nueva | Neurociencia para el Alto Rendimiento Profesional | `clase-22-de-semptiembre-de-neurociencia` |

En cada carpeta: `index.html` va en la landing de registro, `thank-you.html` en la página de gracias.
Copiás de marcador a marcador, reemplazando el bloque entero.

---

## La del 22 es distinta: nueva temática y quiz

La carpeta `clase-22-septiembre/` ya **no** es la versión "Cumplís con todos" clavada al 22. Es la landing
nueva para el perfil de líderes, empresarios y profesionales con trayectoria:

- **Gancho:** *Más "productivo" sos, menos avanzás en tu vida.*
- **Evento:** *Neurociencia para el Alto Rendimiento Profesional con Nico Fernández Miranda.*
- **Ecuación** con la tercera línea borroneada. Lo que hay debajo del blur es un señuelo (dice "Lo que
  falta"); la variable real no está escrita en ningún lado del código, ni en comentarios. Queda en suspenso
  hasta el vivo.
- **Cinta de logos de prensa** abajo del hero (CNN, Infobae, Endeavor, TED, Yale, YPF, Samsung, Ternium), a
  color, desplazándose sola hacia la izquierda. Se frena al pasar el mouse. El bloque de credenciales en
  chips se sacó.
- **Hero centrado con la foto del TED de fondo**, estilo tarjeta: etiqueta "Evento en vivo", título del
  evento, "con Nico Fernández Miranda", el gancho, fecha, contador y botón. Cuando tengas la foto nueva en
  4K, cambiás sólo el `src` de la imagen dentro de `.nfm-hero__bg`. Toda la landing va centrada.
- **Quiz de tres preguntas antes del form**, con una imagen por opción en las dos primeras y un aviso
  amarillo arriba ("Clase en vivo exclusiva para empresarios, líderes y profesionales…"). La tercera es
  abierta: "¿A qué te dedicás, específicamente?". Las respuestas viajan al mismo form de siempre como
  campos extra (ver tabla abajo). En la landing todos ven el mismo form. En GHL, mandá el `Lead` por CAPI
  sólo con `califica = si` (o, si querés apuntar más fino a Platinum, sólo con `nivel = alto`).

  **Campos que llegan al form** (todos van en la URL del iframe, GHL los toma solo si existe un campo
  oculto con el mismo nombre):

  | Campo | Valores | Qué es |
  |---|---|---|
  | `etapa` | `A` / `B` / `C` | Pregunta 1 |
  | `equipo` | `A` / `B` / `C` | Pregunta 2 |
  | `dedicacion` | texto libre | Pregunta 3, a qué se dedica |
  | `califica` | `si` / `no` | `no` sólo si etapa = C |
  | `nivel` | `alto` / `medio` / `bajo` | alto = A o B con gente a cargo · medio = A o B sin gente a cargo · bajo = C |
  | `clase_fecha` | `2026-09-22` | Fecha de la clase |
  | `edicion` | `clase-sep22-alto-rendimiento` | Etiqueta de la edición |

  Cómo crearlos en GoHighLevel: Settings → Custom Fields → Add Field, objeto Contact, tipo Single Line,
  y el **Unique key** exactamente igual al nombre de la tabla (minúsculas, sin tildes). Después, en el
  Form Builder, agregás cada custom field al form y lo marcás como Hidden. GHL rellena los campos ocultos
  con los parámetros de la URL que tengan el mismo nombre. Las UTM no hace falta crearlas: GHL las captura
  solo.
- **Thank you page con dos variantes.** Si la persona eligió C, no ve el grupo de WhatsApp ni la agenda:
  ve "quedaste anotado, te avisamos primero". Si eligió A o B (o si no hay dato), ve todo como siempre.
  Para probar la variante C sin pasar por el quiz: `thank-you.html?etapa=C`. Como en la landing ya no se
  le avisa a los C que el evento no es para ellos, esta variante puede sorprenderlos: si preferís que
  todos vean la página normal, poné `VARIANTE_C: false` en el CONFIG de `thank-you.html` (el popup igual
  se muestra sólo a A/B).
- **Popup post-registro (USD 1 / USD 5):** hay un lugar reservado al final de `thank-you.html`, marcado
  con `POPUP POST-REGISTRO`. Cuando tengas el código, va ahí. Se muestra sólo a quien calificó; los C nunca
  lo ven. Si el popup es un script, envolvelo en `if(window.NFM_CALIFICA){ ... }`.
- **"Qué vas a aprender en el Zoom En Vivo"**: seis puntos de una línea, con número y emoji, sin bajadas.
- **Las cinco escenas de Nico** van apiladas y centradas (imagen arriba, texto abajo): el contador que
  llegó rápido, el precio por la productividad, el punto de inflexión en París, la variable para escalar
  sin agotarse (con dos fotos: TED y libro) y hoy. Las fotos reales se cargan con
  `clase-22-septiembre/editor-nico-escenas.html`: Rolando sube las fotos y edita el texto ahí, descarga el
  archivo y se pasan a la landing. Hoy son placeholders grises. En
  `clase-22-septiembre/prompts-gif-escenas.md` está, escena por escena, qué foto real conviene y un prompt
  para ChatGPT si no la tenés.
- El copy completo y sus fundamentos están en `clase-22-septiembre/nucleo-comunicacion.md`.

Lo que **no** cambió: mismo form de GHL (`kLh5onxCgHdGDA10c8NU`), mismos parámetros de siempre
(`clase_fecha`, `edicion`, UTMs de Meta pasan intactas), sólo `PageView` en el pixel, mismo grupo de WhatsApp
que ya me pasaste. Campaña por defecto para leads sin UTM: `clase-sep22-alto-rendimiento`.

---

## Cuándo pegar cada una

Son las mismas fechas de arranque de captación que ya habíamos definido:

- **Ya pegada** (desde el 2 de septiembre): la del **15**.
- **11 de septiembre, 00:00** → pegás la del **22**.
- **20 de septiembre, 00:00** → pegás la de octubre (falta definirla).

---

## Qué se probó

La del 15 se abrió con el reloj puesto en cuatro momentos distintos —hoy, 5 de septiembre, 18 de
septiembre y 30 de noviembre— y **en los cuatro muestra exactamente lo mismo**: misma fecha, mismo tema,
misma campaña, mismo grupo. No hay forma de que rote sola.

La del 22 se probó en escritorio y en celular con los tres caminos del quiz (A, B y C): el form recibe
`etapa`, `equipo` y `califica` correctos, las UTMs de la URL pasan intactas, la thank you page muestra la
variante que corresponde según lo que se eligió, y el botón de WhatsApp apunta al grupo del 22.

Verificado en todas: sólo `PageView` en el pixel, ningún evento de conversión, ningún placeholder crudo en
pantalla, y la página no se desborda a lo ancho en celular.

---

## Lo único a tener en cuenta

**Después de que pasa la clase, el contador queda en cero** y aparece el cartel de "la clase está
empezando ahora". Es esperable: la página está clavada a esa fecha y no sabe que hay una siguiente.
Por eso hay que reemplazarla en la fecha que corresponde. Si algún martes se te pasa, lo peor que
puede pasar es que muestre una clase vencida — nunca una fecha inventada.

**El título y la descripción del preview** (lo que se ve cuando alguien comparte el link por WhatsApp)
salen de GoHighLevel, no de estos archivos. Están puestos genéricos a propósito para que no queden
viejos entre clase y clase.

---

## La versión que rota sola sigue existiendo

`../index.html` y `../thank-you.html` son la versión con las tres clases cargadas, que cambia sola en
las fechas de captación. Si algún día preferís volver a esa, están ahí y funcionan. Estas versiones
fijas son para cuando querés control manual total y cero sorpresas.
