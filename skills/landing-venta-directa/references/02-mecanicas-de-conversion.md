# Mecánicas de conversión

Las piezas funcionales de la página. Cada una es una decisión de ingeniería, no de copy.

## Índice
- [CTA único + modal de orden](#cta-modal)
- [El selector de camino](#selector)
- [Formulario por pasos](#form-pasos)
- [Value stack](#value-stack)
- [Order bumps](#bumps)
- [Justificación honesta del precio](#precio)
- [Garantía](#garantia)
- [Urgencia real vs falsa](#urgencia)
- [Elemento interactivo (calculadora / diagnóstico)](#interactivo)
- [Descalificador](#descalificador)
- [Prueba social que se lee](#prueba-social)
- [Tracking mínimo](#tracking)

<a id="cta-modal"></a>
## CTA único + modal de orden

La mecánica más importante de toda la página, y la más ignorada.

**Cómo funciona:** todos los botones de la página, sin excepción, dicen exactamente lo mismo y hacen exactamente lo mismo — abren un modal encima de la página en vez de navegar a otro lado.

Por qué gana:
- **Cero pérdida de contexto.** Navegar a otra página descarta todo el trabajo de convencimiento hecho en el scroll. El modal lo conserva de fondo.
- **Escalón, no montaña.** El modal es un compromiso chico ("miro qué hay") que ya activa el sesgo de consistencia.
- **Un solo punto de medición.** Todos los clics apuntan al mismo evento: la tasa de apertura del modal es una métrica limpia.
- **Se puede A/B testear el modal sin tocar la página.**

Reglas:
- Mismo texto en los 5-8 botones. Cambiar el texto entre botones fragmenta la métrica y confunde.
- El texto dice lo que el lector gana, en primera persona: **"Conseguir mi ejemplar"**, "Quiero mi lugar", "Aplicar a la cohorte". Nunca "Enviar", "Comprar", "Más info".
- Naranja Acción `#ff6602`, ancho completo en mobile, alto mínimo 52px.
- Cierre visible en el modal (X + click en el fondo + tecla Escape). Un modal que atrapa genera desconfianza.
- El modal nunca pide más de lo mínimo en el primer paso.

<a id="selector"></a>
## El selector de camino

Variante del modal para cuando hay más de un camino de compra (formato, geografía, pack). Convierte una decisión compleja en 2-3 preguntas de un clic.

Estructura tipo (caso NFM libro):

```
Paso 1: ¿Dónde estás?          → Argentina  |  Fuera de Argentina
Paso 2: ¿Cómo lo querés?       → Libro físico  |  Ebook        (solo si Argentina)
Paso 3: Elegí tu pack           → Pack 1  |  Pack 2
                                 → checkout con carrito pre-armado
```

Reglas:
- **Máximo 3 pasos.** El cuarto paso pierde gente.
- Cada paso tiene botón de "volver" y un indicador de progreso (paso 2 de 3). Sensación de avance constante.
- Ninguna opción es un callejón sin salida: si el lector está fuera del país y no hay envío, el camino sigue con el ebook, no termina en "no disponible".
- El último paso muestra precio real y qué incluye, antes de mandar al checkout.
- El estado del selector no se pierde al cerrar y volver a abrir dentro de la misma sesión.
- Los precios se declaran en un único bloque de configuración arriba del código, no dispersos en el HTML.

<a id="form-pasos"></a>
## Formulario por pasos

Nunca 12 campos de golpe. Se parte en pasos con la información de menor fricción primero.

- Paso 1: email (y nada más). El compromiso ya está tomado.
- Paso 2: datos de contacto.
- Paso 3: pago o calificación.

El email en el paso 1 permite recuperar abandonos aunque el lector no termine. Es la diferencia entre perder el lead y tener una secuencia de carrito abandonado.

<a id="value-stack"></a>
## Value stack

El bloque de oferta lista cada componente con: **qué es → qué resuelve → valor individual**, y después el precio total tachado y el precio real.

Reglas de honestidad (innegociables en NFM):
- El "valor individual" tiene que ser un precio al que ese componente **realmente se vende o se vendió**. Inflar valores es la forma más rápida de perder la confianza de un público que te sigue por rigor científico.
- Si el descuento no existe de verdad en el checkout, no se muestra tachado. Un precio tachado que no se refleja en el carrito destruye la venta en el peor momento posible.
- Si hay costo de envío, se dice en el bloque de oferta, no se descubre en el checkout. El envío sorpresa es la causa #1 de abandono de carrito.

<a id="bumps"></a>
## Order bumps

Ofertas chicas dentro del checkout, con checkbox, a precio muy inferior al principal.

- Precio del bump: 20-40% del producto principal. Más caro que eso deja de ser impulso y se vuelve decisión.
- Copy del bump: una frase de qué resuelve + el precio, nada más. El bump no se argumenta, se ofrece.
- Máximo 2 bumps visibles. Tres o más leen como manipulación.
- El bump tiene que ser complementario, no una versión mejor de lo que ya está comprando (eso genera arrepentimiento).

<a id="precio"></a>
## Justificación honesta del precio

Si el precio es bajo, el lector se pregunta por qué. Si no se lo explicás, lo explica él — y su explicación siempre es peor que la tuya ("debe ser malo").

Razones que funcionan porque son verdad:
- "Es digital: no me cuesta nada más imprimir uno más."
- "Prefiero que lo lean 10.000 personas y que 200 después vengan al programa."
- "El libro es la puerta. Si te sirve, ya sabés dónde encontrarme."
- "Lo cobro porque lo gratis no se lee."

Razones que NO se usan: "precio de lanzamiento" sin fecha real, "solo hoy" recurrente, "descuento del 80%" sobre un precio que nunca existió.

<a id="garantia"></a>
## Garantía

Una frase, sin asteriscos, entendible a la primera lectura.

- Bajo ticket digital: devolución total sin preguntas dentro de X días. El costo de las devoluciones es casi siempre menor al aumento de conversión.
- Físico: política de cambio clara + qué pasa si llega dañado.
- Alto ticket: garantía condicional pero verificable ("si hacés los 4 primeros módulos y no ves X, te devuelvo"). La condición filtra abuso sin sonar a letra chica.
- Nunca prometas resultados sin esfuerzo. Contradice el pilar de marca.

<a id="urgencia"></a>
## Urgencia real vs falsa

| Real (usar) | Falsa (nunca) |
|---|---|
| Fecha de una función confirmada | Contador que se reinicia al recargar |
| Stock físico verificable en el sistema | "Solo quedan 3" inventado |
| Cierre de cohorte con fecha en el calendario | "Oferta por tiempo limitado" permanente |
| Precio que sube en una fecha y efectivamente sube | Descuento sobre un precio que nunca se cobró |

El público de NFM compra por rigor. Una urgencia falsa detectada contamina toda la credibilidad científica de la página. **Si no hay urgencia real, la página no lleva urgencia** — y compensa con la fuerza de la oferta.

<a id="interactivo"></a>
## Elemento interactivo (calculadora / diagnóstico)

Va inmediatamente antes de la oferta. El lector ingresa 2-4 datos propios y recibe un número personalizado que reencuadra el precio.

Ejemplo NFM: el lector dice cuántas veces lo interrumpen por día y cuántas horas trabaja → la calculadora devuelve las horas que pierde por semana y su equivalente en dinero según su ingreso. El precio del libro al lado de ese número deja de ser un gasto.

Reglas:
- Máximo 4 inputs, todos con valores por defecto razonables (funciona sin tocar nada).
- El resultado se actualiza en vivo, sin botón "calcular".
- Debajo del resultado va el CTA. Es el momento de máxima disposición de toda la página.
- El cálculo tiene que ser defendible. Si alguien pregunta la fórmula, se muestra.
- Nunca inventar estudios ni cifras para sostener el cálculo. Si se cita investigación (Gloria Mark, Sophie Leroy), se cita con nombre y se verifica antes de publicar.

<a id="descalificador"></a>
## Descalificador

Bloque explícito de "esto NO es para vos si…". 3-5 ítems, concretos y verdaderos.

Cómo se escribe bien: cada ítem describe un comportamiento, no un insulto.
- ✅ "No es para vos si buscás una técnica que funcione sin cambiar nada de tu rutina."
- ✅ "No es para vos si ya tenés un sistema que funciona y solo querés validarlo."
- ❌ "No es para vos si no estás comprometido." (vacío, todos se creen comprometidos)

Efecto: el que se queda siente que fue elegido. El que se va no iba a comprar, o iba a pedir reembolso.

<a id="prueba-social"></a>
## Prueba social que se lee

Un testimonio útil tiene 4 cosas: **nombre real, cara, situación antes, resultado concreto después.** Si le falta alguna, se lee como inventado incluso cuando es verdadero.

- Formato ganador: una frase textual del alumno en grande + nombre y contexto en chico. Textual, con sus palabras, sin corregirle la gramática de más.
- Cada testimonio se coloca al lado del reclamo que valida, no en un carrusel genérico.
- Los carruseles automáticos pierden: nadie espera a que rote. Grilla estática.
- **En NFM: solo testimonios que existan en `nfm-super-skill/references/06_casos_exito_testimonios.md` o que el usuario confirme explícitamente. Jamás se inventa uno, ni siquiera como placeholder** — los placeholders se publican.

<a id="tracking"></a>
## Tracking mínimo

Sin esto no se puede optimizar nada:
- `ViewContent` al cargar.
- Evento propio al hacer clic en cualquier CTA (todos con el mismo nombre de evento).
- Evento por cada paso del selector/modal, para ver dónde se cae la gente.
- `InitiateCheckout` al salir hacia el checkout.
- UTMs en el link de salida, con `utm_content` distinto por camino, para saber qué pack/formato eligen.
- Scroll depth al 25/50/75/100% — dice qué bloque mata la lectura.

Con esos eventos, la pregunta "¿dónde está floja la landing?" se responde con datos en vez de opinión.
