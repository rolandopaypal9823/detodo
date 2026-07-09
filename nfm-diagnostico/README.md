# Test de Alto Rendimiento NFM — Diagnóstico con Agreement Engineering

Entregable: **`test-alto-rendimiento.html`** (single-file, sin dependencias — se sube tal cual a cualquier hosting/página).

Es la reescritura del diagnóstico "rascada de olla" aplicando **Agreement Engineering** (Dan Henry),
personalizado a la marca de Nico Fernández Miranda / Instituto de Productividad, con la estética del
landing *"Escalá tu vida"*. Se anuncia por WhatsApp API como *"te habilitamos un test de alto
rendimiento con recomendaciones para tu rutina + un resumen de las 2 clases"* — y el archivo entrega
exactamente eso.

---

## 1. La One Belief (la columna vertebral)

Todo el test orbita **una sola creencia**. Está construida con las 5 capas del framework y pasa el
test binario (*"¿puede alguien creerla y aun así NO agendar/comprar, con coherencia lógica?"* → No).
No menciona el producto: describe una **ley del mundo**, y la oferta cae como corolario.

> **"No rendís de menos porque te falte disciplina, tiempo o información. Rendís de menos porque tu
> cerebro está en modo reserva — y un cerebro en reserva no se arregla sabiendo más: se reprograma
> con un sistema y con alguien que te sostenga mientras lo instalás."**

Por qué funciona:
- **Le saca la culpa a la persona** (no sos vago → tu corteza prefrontal está en ahorro de energía). Es
  el mismo movimiento que "muscle confusion" de P90X: quita culpa + crea curiosidad.
- **Cierra la salida lógica**: si creés que (a) el problema es el *estado* de tu cerebro y no tu
  voluntad, y (b) eso no se arregla con más info ni en soledad → necesitás el sistema + el
  acompañamiento. No agendar sería contradecir lo que ya afirmaste.
- **Es 100% de Nico**: sale de sus propios conceptos (cerebro frío/caliente, horno cognitivo, "el
  conocimiento sin implementación es entretenimiento", "hackear tu cerebro").

**Billboard (la frase repetida ~21x, reformulada):** *"No es tu voluntad. Es tu cerebro en reserva"* /
*"El conocimiento no te cambia la vida; la implementación sostenida, sí"* / *"Te falta un sistema — y
quién te lo sostenga"*.

> ⚠️ **Decisión abierta:** la One Belief está derivada de los materiales de Nico (diagnóstico + landing
> + libro). Si querés afinar el dolor #1 / avatar con **el "super skill de Nico"**, se ajusta la frase
> del `belief-strip`, los 3 `hammer` y el copy de perfiles — el resto de la arquitectura no cambia.

---

## 2. La escalera de 9 acuerdos (mapeo pantalla → peldaño)

En vez de "muchas preguntas para autolocalizarse", ahora son **pocas preguntas + afirmaciones donde la
persona ACUERDA punto por punto**. Cada paso está diseñado para producir un peldaño de la escalera. El
que sube los 9 = el avatar = lead calificado que agenda.

| Pantalla | Tipo | Acuerdo que ingeniería |
|---|---|---|
| Estado real | afirmación | **#1** El problema es serio y **compuesto** (empeora si no actuás) |
| 1 problema, 7 caras | multi-select | **#1/#2** Reconocimiento: no son 7 problemas, es 1 (refuerza la One Belief) |
| *Hammer 1* | interstitial | Martilla la One Belief |
| El método viejo no escala | afirmación | **#2** Lo que venís haciendo tiene techo estructural |
| La causa que no sabías | afirmación | **#3** Es química (corteza al 50%), te saca del gancho |
| *Hammer 2* | interstitial | "El conocimiento no cambia nada solo" |
| Otra categoría de solución | afirmación | **#5** Solución fundamentalmente distinta (diseñar en frío = *hackear el cerebro*) |
| Puente Instituto | prueba | **#6** Está probado (+400, equipo real) + **#4** "te entiende" |
| Alguien como vos ya pudo | afirmación (personalizada) | **#7** Identificación personal ("me veo yo") |
| *Hammer 3* | interstitial | Recap de la escalera → "esperar no tiene sentido" |
| El costo de no hacer nada | multi (personalizada) | **#8** El costo de la inacción > costo de actuar |
| Ahora, no después | afirmación | **#9** Urgencia real (inacción compuesta) |

*(Los peldaños #4 y #6 se pegan juntos en el "Puente Instituto", igual que Dan pega varios acuerdos con
una sola pieza.)*

---

## 3. Cómo califica al lead

Tres dimensiones de score se recalculan en cada respuesta:

- **`acuerdo`** — cuánto se alinea con la One Belief / el avatar (driver principal).
- **`aplicacion`** — cuánto ya viene aplicando.
- **`saturacion`** — cuán en "modo supervivencia" está.

**Perfil de salida** (define copy + % de "alto rendimiento"):

| Perfil | Cuándo | % |
|---|---|---|
| **El que está listo para el salto** (avatar) | acuerdo alto | 72–92% |
| **El que ya viene aplicando** | aplicación alta | 60–85% |
| **El que espera el momento** | acuerdo medio | 30–55% |
| **El que viene en modo supervivencia** | saturación domina | 12–32% |

**Ruteo del CTA** (calificación por mentalidad de inversión + capacidad económica, honesto con la plata):

- **Camino A — Agendar entrevista de admisión / sesión de claridad** → capacidad OK + mentalidad de
  inversión (el avatar). *Loom + link a `sesion-postclase`.*
- **Camino B — Libro "Hackea tu Cerebro"** → estudiante, o mentalidad dudosa, o momento económico
  ajustado. *Link a Circle.*
- **Camino C — Libro (oferta suave)** → prefiere lo gratuito, sin presión.

---

## 4. Qué cambió respecto del diagnóstico anterior

- ✅ **Menos preguntas de autolocalización, más afirmaciones de acuerdo** (lo que pediste).
- ✅ **One Belief martillada ~21x** entre bloques (los 3 `hammer` + cada `frame` + el resultado).
- ✅ **Reencuadre "Test de Alto Rendimiento"** (no "diagnóstico de implementación") — matchea el mensaje
  de WhatsApp.
- ✅ **Nueva sección "Tu resumen de las 2 clases"** en el resultado (valor prometido por WhatsApp + es
  repetición de la creencia).
- ✅ **"Brechas" → "3 recomendaciones para tu rutina esta semana"** (accionable, matchea WhatsApp).
- ✅ **Estética del landing "Escalá tu vida"**: gradiente navy profundo, naranja `#ff6602`, labels en
  JetBrains Mono, oferta como *"entrevista de admisión"*.

---

## 5. Knobs para editar (todo está arriba del archivo, en JS)

- **One Belief / dolor**: el `belief-strip` del intro + los 3 objetos `kind:'belief'` (hammers) + los
  `frame` de cada paso.
- **Preguntas / acuerdos**: array `flow` (cada objeto es una pantalla).
- **Perfiles y recomendaciones**: objeto `profiles`.
- **Resumen de las 2 clases**: array `resumen2clases`.
- **Ruteo y umbrales**: funciones `getProfileKey()`, `getPct()`, `getCamino()`.
- **Links reales** (heredados del diagnóstico vigente, cambialos si hace falta):
  - Sesión/entrevista: `nicolasfernandezmiranda.com/sesion-postclase`
  - Libro: `comunidadproductiva.circle.so/hackea-tu-cerebro`
  - Video: Loom `d5cd43a257d04220b60ed264f021e42b`
  - UTMs: `utm_source=test-alto-rendimiento`

---

## 6. Verificación

Probado end-to-end en Chromium (Playwright), 4 escenarios: **sin errores de JS**, las 18 pantallas
renderizan, el scoring diferencia los 4 perfiles (avatar 89% · ya-aplica 74% · espera 37% ·
saturado bajo) y el ruteo A/B/C funciona. *(En el sandbox no cargan Google Fonts ni el logo remoto —
tienen fallback; en producción cargan normal.)*
