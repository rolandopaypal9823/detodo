# Arquitectura de bloques

Cada bloque existe para matar una objeción. La columna "objeción que mata" es la que manda: si no matás ninguna, el bloque sobra y solo agrega scroll.

## Índice
- [El set completo (18 bloques)](#set-completo)
- [Mapeo con el protocolo Funnel 400](#mapeo-funnel400)
- [Variante A — producto de bajo ticket](#variante-a)
- [Variante B — evento / entrada / gira](#variante-b)
- [Variante C — alto ticket con aplicación](#variante-c)
- [Reglas de orden](#reglas-orden)

<a id="set-completo"></a>
## El set completo (18 bloques)

Este es el inventario. Ninguna página usa los 18 — cada variante toma un subconjunto.

| # | Bloque | Función | Objeción que mata |
|---|---|---|---|
| 1 | **Barra superior** | Contexto de urgencia real (fecha, cupo, envío) en una línea | "¿esto sigue vigente?" |
| 2 | **Eyebrow** | Ubica al lector: para quién y de qué categoría es | "¿esto es para mí?" |
| 3 | **Headline** | Promesa específica y medible, no categoría | "¿de qué se trata?" |
| 4 | **Subheadline** | Cómo se consigue la promesa, en una frase, + para quién | "¿y cómo?" |
| 5 | **CTA primario** | La acción única, visible sin scroll | — |
| 6 | **Prueba instantánea** | 3-5 números/logos/credenciales bajo el botón | "¿quién sos vos?" |
| 7 | **Video / carta** | El pitch en formato consumible | "no quiero leer 3.000 palabras" |
| 8 | **Espejo del problema** | La escena cotidiana del lector, en sus palabras | "no me entendés" |
| 9 | **El enemigo** | Nombra la causa externa, saca la culpa del lector | "el problema soy yo" |
| 10 | **El mecanismo** | El 1% faltante con nombre propio + prueba | "esto es lo mismo de siempre" |
| 11 | **Qué te llevás** | Bullets de curiosidad sobre resultados, no features | "¿qué me llevo concretamente?" |
| 12 | **Esto es para vos / esto NO es para vos** | Calificación + descalificación explícita | "¿me van a vender a mí igual que a cualquiera?" |
| 13 | **Prueba social** | Testimonios con nombre, cara y resultado | "¿le funcionó a alguien como yo?" |
| 14 | **Quién soy** | Autoridad + por qué te importa a vos | "¿por qué te creo?" |
| 15 | **Participación** | Calculadora, selector, mini-diagnóstico | "todavía no me siento parte" |
| 16 | **La oferta** | Value stack, precio, justificación del precio | "¿cuánto y qué incluye?" |
| 17 | **Garantía** | Reversión de riesgo en una frase | "¿y si no funciona?" |
| 18 | **Objeciones + cierre** | Objeción principal con sección propia, FAQ chico, CTA final | "lo dejo para después" |

<a id="mapeo-funnel400"></a>
## Mapeo con el protocolo Funnel 400

La estructura no reemplaza al protocolo: lo contiene. Así se corresponden.

| Paso del protocolo | Bloques que lo ejecutan |
|---|---|
| **Vacío de curiosidad** | 2, 3, 4 (eyebrow + headline + subheadline) |
| **Espejo** | 8, 12 (el problema en sus palabras + "esto es para vos") |
| **Momento Aha / 1% faltante** | 9, 10 (el enemigo + el mecanismo con nombre propio) |
| **Menú de posibilidades** | 11, 15 (qué te llevás + participación: "ya probaste X, Y, Z…") |
| **Puente obvio** | 16, 17, 18 (oferta + garantía + cierre) |

Los bloques 6, 7, 13 y 14 son **prueba transversal**: no son un paso del protocolo, son el sostén de credibilidad que hace que cada paso sea creíble. Por eso se distribuyen a lo largo de la página, no se amontonan.

**Consecuencia práctica:** una página puede tener copy impecable de funnel400 y aun así no vender, porque el paso 5 (puente) llega sin garantía, sin descalificador y sin participación previa. Y al revés: una página con los 18 bloques y copy genérico tampoco vende. Se necesitan las dos.

<a id="variante-a"></a>
## Variante A — producto de bajo ticket (libro, ebook, curso <$100)

El caso NFM más frecuente (Hackea tu Cerebro, Desintoxicación Digital, ABC del Alto Rendimiento).

```
1  Barra superior (envío / stock / fecha real)
3  Headline — promesa
4  Subheadline
5  CTA primario  ← abre selector, no va directo al checkout
6  Prueba instantánea (ejemplares vendidos, países, medios)
8  Espejo del problema
9  El enemigo
10 El mecanismo con nombre propio
11 Qué te llevás (bullets de curiosidad)
13 Prueba social (3-4 testimonios reales)
5' CTA repetido
14 Quién soy (corto: 150 palabras + foto)
15 Participación (mini-diagnóstico o selector de formato)
16 La oferta — packs, precio visible, justificación honesta del precio
17 Garantía
18 Objeción principal + FAQ (5-7) + CTA final
```

Bloques que se omiten: 2 (el headline ya ubica), 7 (video opcional), 12 (el descalificador es menos crítico en bajo ticket, pero suma si el público es amplio).

**Lo que más mueve la aguja en esta variante:** el CTA único que abre un micro-paso en vez de tirar al checkout, y el bloque 16 con los packs presentados como elección del lector, no como upsell.

<a id="variante-b"></a>
## Variante B — evento / entrada / gira

```
1  Barra superior (próxima función / últimas entradas — solo si es verdad)
3  Headline — nombre del show + promesa de lo que te llevás
4  Subheadline (formato, duración, para quién)
5  CTA "Ver funciones"
6  Prueba instantánea (funciones agotadas, ciudades, asistentes)
7  Video / trailer
8  Espejo del problema
10 El mecanismo (qué vas a entender que hoy no entendés)
11 Qué te llevás de la función
13 Prueba social (asistentes de funciones anteriores)
14 Quién soy
19 **Grilla de funciones** ← bloque exclusivo de esta variante: ciudad, fecha, sala, botón por función
17 Garantía / política de cambio
18 FAQ (accesibilidad, edad, duración, reembolsos) + CTA final
```

El bloque 19 (grilla) hace de oferta: cada función es una decisión independiente. Las funciones sin link van con estado explícito ("próximamente") y **nunca con fecha inventada** — la fecha se confirma con el usuario siempre.

<a id="variante-c"></a>
## Variante C — alto ticket con aplicación (PLATINUM, corporativo)

```
1  Barra superior (cohorte, cierre de inscripción real)
2  Eyebrow (para quién exactamente)
3  Headline
4  Subheadline
5  CTA "Aplicar" ← abre formulario por pasos, nunca 12 campos de golpe
6  Prueba instantánea
7  Video (carta del fundador)
8  Espejo del problema
9  El enemigo
10 El mecanismo con nombre propio
12 **Esto es para vos / esto NO es para vos** ← crítico acá, no opcional
11 Qué te llevás (por módulo / por fase)
13 Prueba social (casos con números y nombre)
14 Quién soy (extendido)
15 Participación (diagnóstico de nivel)
16 La oferta (stack completo; el precio puede ir en la llamada, pero el rango va en la página)
17 Garantía
18 Objeción principal (sección propia) + FAQ + CTA final
```

En alto ticket el descalificador (12) es el bloque de mayor impacto: filtra las llamadas basura y sube la tasa de cierre del comercial.

<a id="reglas-orden"></a>
## Reglas de orden

1. **El problema antes que el producto, siempre.** Ningún bloque de oferta o de features puede aparecer antes del bloque 10 (mecanismo). Si el lector ve el precio antes de entender por qué su problema tiene una causa que no conocía, compara por precio.

2. **La prueba se distribuye, no se acumula.** Regla práctica: nunca más de 4 testimonios seguidos. Si hay 12, se reparten: 3 después de la promesa, 3 después del mecanismo, 3 después de la oferta, 3 en el cierre.

3. **La participación va inmediatamente antes de la oferta.** No al principio (todavía no hay motivo) ni después del precio (ya decidió).

4. **La garantía va después del precio, nunca antes.** Antes del precio la garantía no significa nada porque no hay riesgo percibido todavía.

5. **El CTA se repite cada 2-3 bloques a partir del bloque 11.** Antes del 11 alcanza con el CTA del above the fold.

6. **La objeción principal va lo más tarde posible pero antes del último CTA.** Es lo último que queda entre el lector y el botón.

7. **Todo bloque tiene un subtítulo que se entiende solo.** Un lector que escanea solo los subtítulos tiene que poder contar el argumento completo de la página. Si no puede, los subtítulos están escritos como decoración.
