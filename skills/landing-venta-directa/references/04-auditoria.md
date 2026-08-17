# Auditoría de landing

Cómo diagnosticar por qué una página no vende, sin reescribirla entera de entrada.

## Índice
- [Qué pedir antes de auditar](#que-pedir)
- [Las 4 fugas](#cuatro-fugas)
- [Scorecard](#scorecard)
- [Cómo entregar la auditoría](#entrega)
- [Extraer estructura de una página ajena](#extraer)

<a id="que-pedir"></a>
## Qué pedir antes de auditar

Sin esto la auditoría es opinión. Pedilo en un solo mensaje, y si no está disponible, **decí explícitamente qué parte de la auditoría queda sin fundamento** en vez de rellenar con suposiciones.

1. **La página** — URL, HTML pegado, o screenshots del scroll completo. Si la página está en una plataforma sin código exportable (Circle, Kajabi), screenshots del scroll entero alcanzan.
2. **Los números** — visitas, clics en el CTA, inicios de checkout, ventas. Con esos 4 se ubica la fuga en un minuto.
3. **La fuente de tráfico** — el ad o el reel que trae la gente. Una landing que "no convierte" muchas veces está bien y el problema es que el ad promete otra cosa.
4. **El checkout** — qué ve el comprador después del botón. La mitad de los problemas de "landing" son de checkout.

<a id="cuatro-fugas"></a>
## Las 4 fugas

Una página que no vende falla en uno de estos cuatro lugares. Ubicarlo primero evita reescribir lo que ya funciona.

| Fuga | Síntoma en los números | Causa típica |
|---|---|---|
| **1. Mensaje** | Mucha visita, poco scroll (75% se va antes del 50%) | El headline no coincide con lo que prometió el ad, o es una categoría en vez de una promesa |
| **2. Deseo** | Scrolean toda la página, no tocan el botón | Falta el mecanismo con nombre propio, o la oferta es "Tal Vez"/"Fastidio". Compiten por precio |
| **3. Fricción** | Clican el botón, no llegan al checkout | Salto demasiado grande, formulario largo, opciones confusas, precio sorpresa |
| **4. Checkout** | Llegan al checkout, no compran | Envío sorpresa, medios de pago, campos innecesarios (dirección para un producto digital), falta de confianza en el último paso |

**Orden de trabajo:** siempre de la fuga más tardía hacia atrás si hay datos (arreglar el checkout es más barato y da resultado más rápido que reescribir la página). Si no hay datos, de la 1 hacia adelante.

<a id="scorecard"></a>
## Scorecard

Puntuar cada ítem 0 / 1 / 2 (0 = no está, 1 = está pero flojo, 2 = está bien resuelto). Total sobre 40.

**Above the fold (0-8)**
- [ ] Headline es promesa específica, no categoría
- [ ] Se entiende para quién es
- [ ] Botón visible sin scroll en mobile
- [ ] Prueba instantánea verificable

**Argumento (0-10)**
- [ ] Espejo con escenas concretas, no categorías
- [ ] El enemigo saca la culpa del lector
- [ ] Mecanismo con nombre propio
- [ ] Prueba que respalda el mecanismo
- [ ] Bullets de curiosidad (abren loops, no describen contenido)

**Confianza (0-8)**
- [ ] Testimonios con nombre, cara y resultado concreto
- [ ] Prueba distribuida, no amontonada
- [ ] Bio que traduce credencial a beneficio
- [ ] Garantía en una frase clara

**Mecánica (0-10)**
- [ ] Un solo CTA, mismo texto, repetido
- [ ] Sin menú ni links de fuga
- [ ] El botón abre un micro-paso
- [ ] Elemento de participación antes del precio
- [ ] Descalificador explícito

**Cierre (0-4)**
- [ ] Precio visible y justificado, con envío incluido en la comunicación
- [ ] Objeción principal con sección propia

Lectura del puntaje: **<20** la página necesita reestructuración, no ajustes. **20-30** faltan bloques específicos, se arregla agregando. **>30** el problema probablemente no es la página — mirá el tráfico o el checkout.

<a id="entrega"></a>
## Cómo entregar la auditoría

1. **Veredicto en una línea.** Dónde está la fuga principal.
2. **Las 3 correcciones de mayor impacto**, en orden, con el motivo y el esfuerzo estimado. Nada de listas de 20 mejoras — se hacen cero.
3. **Tabla de bloques**: presente / faltante / fuera de orden.
4. **Lo que NO hay que tocar.** Explicitarlo evita que se rompa lo que funciona.
5. Recién después, si el usuario lo pide, el copy nuevo.

Si algo no se pudo ver (la página estaba bloqueada, no hay números, el checkout no es accesible), **se dice al principio**, no al final y no implícitamente.

<a id="extraer"></a>
## Extraer estructura de una página ajena

Cuando el usuario pega el HTML o screenshots de una referencia.

**Qué se puede ver:**
- Todo el copy, incluidos textos ocultos en modales y popups.
- La estructura de bloques y su orden.
- El sistema de diseño (tipografías, paleta, escala).
- La mecánica: qué hace cada botón, cuántos pasos tiene el formulario, qué bumps hay configurados.
- El stack de tracking (píxeles, herramientas de atribución) — dice cuánto invierten en medir.
- En páginas de builders (HighLevel, Webflow, Framer) el modelo completo de la página suele venir serializado en el payload: elementos, estilos, pasos del funnel, productos.

**Qué NO se puede ver, y hay que decirlo:**
- Si la página convierte. Nunca asumir que funciona porque el autor es conocido.
- Qué variante de test está sirviendo.
- Qué pasa después del checkout (upsells, secuencia de emails).
- Los datos: tráfico, costo por lead, tasa de cierre.

**Cómo entregarlo:** tabla `bloque → función → objeción que mata → ¿nos sirve?`. Después, una lista corta de las mecánicas que vale la pena copiar y **una advertencia explícita sobre lo que NO hay que copiar** — típicamente la estética, que es de la marca ajena, y las tácticas que no se sostienen con el público de NFM (urgencia falsa, valores inflados, testimonios sin nombre).

La estructura se copia. El copy y el diseño, nunca.
