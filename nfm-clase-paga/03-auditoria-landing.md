# Auditoría de la landing — scorecard de 40 puntos

Rúbrica de `landing-venta-directa/references/04-auditoria.md`, aplicada a `landing-live-edition.html`.
Puntaje: 0 = no está · 1 = está pero flojo · 2 = bien resuelto.

## Resultado: 35 / 40

Lectura de la skill: **>30 = el problema probablemente no es la página.** 20-30 faltan bloques. <20 es reestructuración.

| Sección | Ítem | Pts | Nota |
|---|---|:--:|---|
| **Above the fold (7/8)** | Headline es promesa, no categoría | 2 | Es diagnóstico + pregunta abierta, no categoría. Específica y no reutilizable por un competidor. |
| | Se entiende para quién es | **1** | El subhead nombra el formato pero no al avatar. El descalificador lo resuelve, pero recién en el bloque 12. |
| | Botón visible sin scroll en mobile | 2 | Verificado con Playwright: borde inferior del botón a **451px** en 390×844 (objetivo ≤640). |
| | Prueba instantánea verificable | 2 | Sólo credenciales confirmadas. Pendiente `[[AUTORIDAD]]`. |
| **Argumento (9/10)** | Espejo con escenas concretas | 2 | Las 5 escenas salen del deck y del lenguaje literal del avatar. |
| | El enemigo saca la culpa | 2 | Cierra con la frase obligatoria: *"No es un problema de voluntad. Es un problema de arquitectura."* |
| | Mecanismo con nombre propio | 2 | **"El efecto derrame"** — es la palabra que Nico ya usa en vivo, no un naming inventado. |
| | Prueba que respalda el mecanismo | **1** | Los 4 datos son reales y de su propio material, pero **van sin atribución**. Ver pendiente #3. |
| | Bullets de curiosidad | 2 | Los 5 mitos abren loop y no lo cierran. |
| **Confianza (6/8)** | Testimonios con nombre, cara y resultado | **1** | Nombre ✓ · resultado ✓ · **cara ✗**. Ver pendiente #1 — es el más grave. |
| | Prueba distribuida | **1** | Los 4 casos van juntos. Están en el límite de la regla (nunca más de 4 seguidos) pero convendría repartir 2 arriba y 2 abajo. |
| | Bio traduce credencial a beneficio | 2 | *"Esa misma cabeza que sacaba las mejores notas no me alcanzaba para llegar al viernes."* |
| | Garantía en una frase | 2 | Sin asteriscos, se entiende a la primera. |
| **Mecánica (10/10)** | Un solo CTA, mismo texto | 2 | **Corregido:** los 8 botones dicen *"Quiero mi lugar"*. |
| | Sin menú ni links de fuga | 2 | Cero navegación, cero footer con links. |
| | El botón abre un micro-paso | 2 | Modal de 2 pasos (email → pack). El email del paso 1 permite recuperar abandonos. |
| | Participación antes del precio | 2 | Calculadora, con el CTA inmediatamente debajo del resultado. |
| | Descalificador explícito | 2 | Dos columnas del mismo largo, comportamientos concretos. Reciclado del deck. |
| **Cierre (4/4)** | Precio visible y justificado | 2 | Justificación honesta y verdadera, sin "precio de lanzamiento". |
| | Objeción principal con sección propia | 2 | *"Ya empecé cosas y no las terminé"* tiene sección entera, en fondo azul. |

---

## Los 3 pendientes, en orden de impacto

### 1. Faltan las fotos de los casos ← el más grave
La regla es dura: *"Un testimonio útil tiene nombre real, cara, situación antes y resultado concreto. Si le falta alguna, **se lee como inventado incluso cuando es verdadero**."*
Necesito las 4 fotos (Natalia, Pierina, Celi, Juan Jesús). El deck ya tiene los espacios marcados con *"cara real, para que se vea que es una persona de carne y hueso"*, así que probablemente ya existen.
**Con las fotos la landing pasa de 35 a 36, y sube el bloque de confianza de 6/8 a 7/8.**

### 2. Los 4 casos van amontonados
Repartir: 2 después del mecanismo, 2 después de la oferta. Es un cambio de 10 minutos que hago cuando lleguen las fotos.

### 3. La prueba del mecanismo va sin atribución
Los 4 datos (40% de caída de rendimiento, 20% del gasto energético, BDNF, 23 minutos de recuperación) son reales y de material que Nico ya enseña, pero en la landing van sin fuente.
La skill es explícita: *"la prueba, con nombre del investigador y la institución, **verificada** — una cita mal atribuida hace más daño acá que en cualquier otro lado"*.
**No les puse atribución a propósito**, porque no puedo verificar las fuentes originales desde acá y prefiero un dato sin cita que una cita inventada. Si tenés las fuentes (el dato de los 23 minutos suele atribuirse a Gloria Mark, UC Irvine — **a confirmar antes de publicar**), las agrego.

---

## Lo que NO hay que tocar

- El bloque de objeción principal. Es el que más convierte y está construido sobre tu insight del acompañamiento.
- La justificación honesta del precio. Sacarla reabre el "si es barato debe ser malo".
- El descalificador. La skill lo marca como el bloque de mayor impacto y además filtra al que no es avatar.
- La calculadora, y sobre todo el CTA pegado abajo del resultado: es el momento de máxima disposición de toda la página.

---

## Pendientes técnicos antes de publicar

| Token | Dónde | Qué falta |
|---|---|---|
| `{{FECHA}}` | 6 lugares | Fecha y hora de la clase |
| `{{CAPITULO}}` | value stack | Qué capítulo del libro entra como sampler |
| `{{CHECKOUT_STRIPE_17}}` | `CHECKOUT.solo` | Payment Link de Stripe, clase sola |
| `{{CHECKOUT_STRIPE_24}}` | `CHECKOUT.full` | Payment Link de Stripe, clase + bump |
| `[[AUTORIDAD]]` | prueba instantánea + bio | Datos actualizados de Nico |
| Pixel | `track()` | El pixel de Meta no está instalado — la función ya dispara `ViewContent`, `Lead`, `InitiateCheckout` y `ScrollDepth`, sólo falta el snippet |
| Mercado Pago | modal | Falta el segundo link de pago. Para argentinos evita el dólar tarjeta, que la data marca como **la fricción #1** |

## Verificado con Playwright

- Mobile 390×844: botón above the fold a 451px ✓
- Desktop 1280×900 ✓
- Modal de 2 pasos: abre, valida email, avanza al paso 2 ✓
- Calculadora: 12 interrupciones × 10 min → 220 h/año (28 jornadas) ✓
- **Cero errores de JavaScript** en ambos viewports ✓
- Las tipografías caen a Georgia en el sandbox porque no hay salida a Google Fonts; en producción cargan Montserrat / Open Sans / JetBrains Mono.
