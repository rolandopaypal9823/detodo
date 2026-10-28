# La landing que ya está al aire vs. la que armé

**Fuente:** `origin/claude/nueva-landing-form-7ajo0h` → `landing-siempre-on/clase-15-septiembre/index.html` (87 KB, último commit 2026-09-02).

**Veredicto en una línea: la que ya existe es mejor que la mía, y la Live Edition tiene que construirse encima de esa, no al lado.**

---

## 1. Lo que encontré y no sabía

### El mecanismo con nombre propio ya existe, y es mejor que el que propuse

La landing al aire tiene esto en el centro:

> **URGENCIA PRESTADA** — *"Tu cerebro no ordena por importancia. Ordena por quién está esperando."*
> *"Lo ajeno llega con fecha, con nombre y con alguien del otro lado esperándolo. Lo tuyo llega solo."*

Yo había propuesto **"el efecto derrame"** (los 5 pilares como sistema). **Urgencia prestada le gana, y por un motivo estructural, no de gusto.**

Acordate de la fuga que marqué en el plan: la creencia de los 5 pilares se puede sostener entera y aun así decir *"bueno, los arreglo yo solo"*. Ahí se escapa la venta.

**Urgencia prestada no tiene esa fuga: el mecanismo se cierra solo.** Si tu cerebro sólo prioriza lo que tiene a alguien del otro lado, y lo tuyo no tiene a nadie — entonces *hacerlo solo* es, por definición, la condición que ya te falló. La única salida coherente es ponerle a lo tuyo alguien del otro lado. Eso es el producto.

Y hay algo todavía mejor: **una clase paga, en vivo, con fecha y hora, ES literalmente el mecanismo aplicado.** Pagás, hay una fecha, y del otro lado hay alguien esperándote. El producto no *ilustra* la big idea: la ejecuta. Eso es exactamente lo que Dan Henry hace cuando la oferta es el corolario inevitable de la creencia.

**No compiten con los 5 pilares.** Se apilan:
- **Urgencia prestada = el mecanismo.** Por qué te pasa. Es el POR QUÉ.
- **Los 5 pilares = el temario.** Qué vemos en las dos horas. Es el QUÉ.

### Los datos de autoridad que te venía pidiendo ya están publicados

El bloque *"Su trabajo fue destacado en"* de la landing lleva: **CNN · Infobae · Endeavor · TEDx · Yale · YPF · Samsung · Ternium**. Y el bloque de testimonios dice **"Más de 400 pasaron por el Instituto de Productividad"**.

Eso es exactamente la pieza que tenía marcada como bloqueante `[[AUTORIDAD]]`, y es el equivalente NFM de la *validación por pares* de Dan Henry (los reyes de la industria lo contrataron a él). **Ya no está bloqueado** — sólo confirmame que esos ocho logos siguen vigentes y los uso.

### La prueba social no usa fotos: usa video

Los testimonios son embeds de YouTube (Celina, Andrés). Eso resuelve mejor que una foto el pendiente #1 de mi auditoría: un video es prueba más difícil de fabricar. **Anulo ese pendiente.**

### El stack real es GoHighLevel, no HTML suelto

- La landing entera está delimitada por `DESDE ACÁ EMPIEZA LO QUE VA EN EL CUSTOM CODE DE GHL`.
- El formulario es un embed de GHL: `api.leadconnectorhq.com/widget/form/kLh5onxCgHdGDA10c8NU`.
- Pixel `1203017011123382`, y **sólo dispara `PageView`**. Hay un comentario explícito en el código: la conversión la manda GHL por **CAPI**, y si además la disparara el pixel, *"Meta contaría dos veces el mismo registro: el pixel y la CAPI no se deduplican solas si no comparten event_id"*.

⚠️ **Esto es un bug en la landing que armé:** yo disparo `Lead` e `InitiateCheckout` del lado del cliente. Con el setup de ustedes eso duplica conversiones. Hay que resolverlo antes de publicar (ver §4).

### Arquitectura "siempre-on"

Una sola URL prendida los 365 días, con dos temas (A/B) que alternan solos clase a clase, y dos fechas por clase: `fecha` (cuándo se da) y `desde` (cuándo la landing empieza a promocionarla). Countdown real atado a la fecha. Las versiones `clase-15-septiembre/` y `clase-22-septiembre/` son congeladas de esa misma base.

---

## 2. Comparación bloque por bloque

| # | Landing al aire (free) | La que armé (Live Edition) | Qué me llevo |
|---|---|---|---|
| 1 | Nav | — | La mía no tiene nav, y está bien: la ley 1 dice cero links de fuga. **Gana la mía.** |
| 2 | Hero + countdown real + micro-bajada que desactiva la promesa de alivio | Hero + barra de fecha | **Gana la de ellos.** El countdown atado a fecha real y la micro-bajada (*"No es para trabajar menos: es para dejar de ser el cuello de botella de tu propia vida"*) son mejores. |
| 3 | Prueba social: CNN, Infobae, Endeavor, TEDx, Yale, YPF, Samsung, Ternium | 4 píldoras de credenciales académicas | **Gana la de ellos, por lejos.** |
| 4 | Espejo — 7 escenas | Espejo — 5 escenas | Empate. Las de ellos son más específicas del sub-avatar líder. |
| 5 | **Formulario arriba, a mitad de página** | Modal desde el CTA | Distinto por diseño: free captura, pago tiene que vender antes de pedir plata. **Se queda la mía**, pero ver §4. |
| 6 | Mecanismo: **urgencia prestada** + quote de Francisco, 40, director de operaciones | Mecanismo: efecto derrame + 4 datos | **Gana la de ellos.** Ver §1. |
| 7 | Qué vas a descubrir — 5 bullets de curiosidad | Los 5 mitos | **Gana la mía** para el producto pago: los 5 mitos son el temario y abren cinco loops en vez de uno. |
| 8 | Testimonios en video, reencuadrados al mecanismo | 4 casos en texto | **Gana la de ellos** (video > texto). |
| 9 | **El giro** — creencia vieja vs paradigma nuevo, con la analogía del entrenador | Bloque de objeción principal | **Gana la de ellos.** Ver abajo. |
| 10 | CTA final + footer | Cierre con bifurcación + FAQ | **Gana la mía**: ellos no tienen FAQ ni descalificador explícito en dos columnas. |
| — | — | Calculadora de horas, order bump, garantía, descalificador, FAQ | **Sólo míos.** Los cuatro son requisitos de venta paga que la free no necesita. |

### La analogía del entrenador — lo mejor de toda la página

> *"Cuando contrataste un entrenador no fue porque no supieras hacer sentadillas — eso está gratis en YouTube. Fue porque el martes a las 7 hay alguien esperándote. Y funcionó. Nunca pensaste que ahí te faltaba carácter."*

Es una analogía de manual: toma un dominio donde el lector **ya acepta** que contratar a alguien no es falta de carácter, y lo traslada. Sube el peldaño en quince segundos y desactiva la vergüenza de comprar. **Va tal cual a la Live Edition**, y encima justifica el precio sin hablar de precio.

---

## 3. Lo que se mantiene de lo que armé

No todo se tira. Estos bloques no existen en la free porque no los necesita, y son obligatorios para vender:

1. **Descalificador en dos columnas** (la skill lo marca como el bloque de mayor impacto).
2. **Calculadora de horas** — participación antes del precio.
3. **Bloque de oferta** con value stack por resultado, precio y justificación honesta.
4. **Order bump** (libro + ebook de desintoxicación).
5. **Garantía** en una frase.
6. **FAQ** de objeciones operativas.
7. **Cierre con bifurcación.**
8. **Cero nav.**

Y del VSL: el guion sigue sirviendo casi entero, pero **hay que cambiarle el mecanismo** — sale "efecto derrame", entra "urgencia prestada". Es un cambio de dos bloques (III y IV), no una reescritura. El resto (historia de origen, los 5 mitos, la matemática, Pierina, el cierre) queda igual. Y el bloque de objeciones que escribí **ya estaba escrito sobre urgencia prestada sin saberlo** — porque es el mismo insight que me pasaste.

---

## 4. El problema técnico a resolver: cómo se cobra

La free captura con un form de GHL y la conversión va por CAPI. La paga necesita un checkout, y ahí hay dos caminos que no son equivalentes:

| | **A · Directo a checkout** | **B · Form primero, después checkout** |
|---|---|---|
| Flujo | Landing → Stripe/MP → thank you | Landing → form GHL (captura) → checkout → thank you |
| Si no paga | Lo perdés | **Te queda el lead**, entra a nutrición y retargeting |
| Fricción | Menor | Un paso más |
| Tracking | Pixel client-side + webhook de Stripe | Sigue el patrón CAPI que ya tienen |
| Encaja con el negocio | — | **Sí.** Toda la ganancia está en el backend: un lead que no compró los USD 17 hoy sigue valiendo. |

**Recomiendo B**, y con fuerza. A ROAS 1x el ticket no es el negocio; la lista sí. Tirar a la basura al que llegó hasta el checkout y no pagó es regalar justo lo que viniste a comprar.

Y sea cual sea: **hay que sacar los eventos client-side de mi landing** (`Lead`, `InitiateCheckout`) o darles `event_id` compartido con la CAPI, o Meta va a contar doble.

---

## 5. Qué propongo hacer

Rehacer `landing-live-edition.html` **partiendo del archivo de ellos**, no del mío:

1. Clonar `landing-siempre-on/clase-15-septiembre/index.html` como base — trae el sistema visual real, el countdown, los logos de prensa, los videos y la estructura validada.
2. Cambiar el hero de "clase gratuita" a la oferta paga, con el precio arriba.
3. Mantener **urgencia prestada** como mecanismo y **la analogía del entrenador**.
4. Reemplazar "Qué vas a descubrir" por **los 5 mitos** (el temario de los 5 pilares).
5. Insertar los bloques que faltan: descalificador, calculadora, oferta con stack, bump, garantía, FAQ.
6. Resolver el checkout según A o B.
7. Sacar los eventos duplicados del pixel.

Queda una sola URL congelada por clase, igual que hacen hoy con `clase-15-septiembre/` y `clase-22-septiembre/`.

---

## Nota sobre lo que pediste

**No me llegó ningún adjunto con la estructura de landings de Dan Henry.** En la carpeta de subidas de esta sesión sólo está el PDF de los 5 pilares. Si lo querés incluir, volvé a mandarlo (imagen, PDF o la URL de la landing) y lo cruzo con esta comparación. Mientras tanto, lo que usé de Dan Henry es la deconstrucción de su VSL que hicimos al principio.
