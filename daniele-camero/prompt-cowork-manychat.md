Vas a armar un flujo nuevo en ManyChat para la cuenta de Instagram de Daniele Camero, usando mi computadora. Ya estoy logueado en ManyChat en el navegador. Trabajá paso a paso y mostrame una captura al terminar cada paso.

## Reglas
- No borres ni modifiques flujos, triggers ni secuencias que ya existen. Todo se hace en un flujo nuevo llamado **"Filtro Leads – Techo financiero (v1)"**.
- No actives el flujo ni lo conectes a un trigger en vivo hasta que yo te lo confirme por escrito. Dejá todo en borrador o desactivado.
- No toques facturación, pagos, integraciones ni ajustes de la cuenta.
- Si algo no coincide con lo que describo (un bloque que no existe, un límite de caracteres, un menú con otro nombre), pará y preguntame. No inventes.
- Antes de cualquier paso que no se pueda deshacer (publicar, activar, borrar), pedime confirmación.
- Los textos de abajo van tal cual. Si Instagram corta un botón por largo, abrevialo manteniendo el número y anotame cómo quedó.

## Datos que necesito que me pidas antes de empezar (si no te los di)
- LINK_MINI_VSL: video corto para leads high ticket
- LINK_CLASE_LARGA: clase larga para leads low ticket
- LINK_CHECKOUT_LT + TEXTO_OFERTA_LT: oferta low ticket (Sociedad Élite)
- AUDIO_LT: archivo de audio para leads low ticket (si no está, usá un texto "AUDIO PENDIENTE" y avisame)
- NOMBRE_SETTER: a quién se asigna la conversación de los leads high ticket
- PALABRAS_CLAVE: palabras clave de comentarios o DMs que también disparan este flujo
- CUENTA_PRUEBA: cuenta de Instagram para probar

## Paso 0: Revisar
1. Abrí ManyChat y confirmame el nombre de la cuenta de Instagram conectada.
2. Sacá una captura del flujo de bienvenida actual. No lo modifiques.

## Paso 1: Campos y etiquetas
En Configuración → Campos, creá 3 campos de usuario de tipo texto: `ocupacion`, `objetivo_90d`, `freno`.
En Configuración → Etiquetas, creá:
- `p1_techo`, `p1_variable`, `p1_dificil`
- `ruta_ht`, `ruta_lt`, `encuesta_completa`
- `origen_bienvenida` y una `origen_<palabra>` por cada palabra clave
Si alguno ya existe, usá el existente.

## Paso 2: El flujo (en este orden)

**Mensaje 1: Bienvenida**
> ¡Hola {nombre}! 🙌 Bienvenido/a. Te quiero regalar un entrenamiento para descubrir el punto ciego que hoy no te deja pasar a tu siguiente nivel. Para mandarte el que más te sirve, respondeme unas preguntas rápidas 👇

Botón: **Quiero el entrenamiento** → Mensaje 2.
Si no toca el botón en 3 horas: mandar una sola vez "¿Seguimos? 👇" con el mismo botón.

**Mensaje 2: Filtro**
> Para arrancar: ¿dónde está hoy tu techo financiero?
> 1️⃣ Genero bien, pero hace tiempo que estoy estancado en el mismo techo
> 2️⃣ Genero, pero todavía no logro sostenerlo: sube y baja
> 3️⃣ Hoy estoy empezando de cero o saliendo de deudas

Botones y acciones:
- **1. Estoy en un techo** → etiquetas `p1_techo` + `ruta_ht` → Mensaje 3
- **2. No lo sostengo** → etiquetas `p1_variable` + `ruta_ht` → Mensaje 3
- **3. Empezando/deudas** → etiquetas `p1_dificil` + `ruta_lt` → Mensaje 3

Si no responde en 3 horas: recordatorio una sola vez con los mismos botones.

**Mensaje 3: Situación actual** (bloque de entrada de usuario, respuesta de texto, guardar en `ocupacion`)
> Contame un poco de tu situación actual: ¿a qué te dedicás hoy? (si además tenés un negocio, trading o inversiones, contámelo también)

**Mensaje 4: Cafecito de 90 días** (entrada de usuario, texto, guardar en `objetivo_90d`)
> Imaginá que en 90 días nos tomamos un cafecito y me decís "lo logré". ¿Qué me estarías contando?

**Mensaje 5: Punto ciego** (entrada de usuario, texto, guardar en `freno`)
> ¿Y cuál sentís que es hoy ese punto ciego que te viene frenando?

Después del Mensaje 5: agregar la etiqueta `encuesta_completa`.
En los mensajes 3, 4 y 5: si no responde en 12 horas, que el flujo siga igual al paso siguiente y no se trabe.

**Condición:** si tiene la etiqueta `ruta_ht` → Rama HT. Si no → Rama LT.

**Rama HT**
1. Mensaje:
> Gracias {nombre} 🙌 Por lo que me contás, estás justo en el punto donde Daniele más ayuda. Te dejo este video corto 👉 LINK_MINI_VSL
> Miralo y contame qué fue lo que más te resonó 👇
2. Acción: notificar al admin y asignar la conversación a NOMBRE_SETTER con el texto "Lead HT · {ocupacion} · {objetivo_90d} · {freno}".
3. Nada más automático: la setter sigue a mano.

**Rama LT** (sin setter)
1. Audio: AUDIO_LT
2. Mensaje:
> Te comparto este entrenamiento 👉 LINK_CLASE_LARGA
> Se estrena hoy a las 19 h 🕖
3. Demora: unas 20 horas. Instagram solo deja mandar mensajes automáticos dentro de las 24 h desde el último mensaje de la persona, así que no pases de 23 h.
4. Mensaje: TEXTO_OFERTA_LT 👉 LINK_CHECKOUT_LT

## Paso 3: Triggers (sin activar)
- Preparalo para el trigger de bienvenida que te indique y uno por cada palabra de PALABRAS_CLAVE.
- Cada trigger agrega su etiqueta de origen (`origen_bienvenida`, `origen_<palabra>`) antes del Mensaje 1.
- Todo queda desactivado.

## Paso 4: Prueba
Con la vista previa o con CUENTA_PRUEBA, recorré el flujo dos veces:
- Una eligiendo el botón 1 (tiene que ir a HT).
- Otra eligiendo el botón 3 (tiene que ir a LT).

Verificá:
- Las etiquetas correctas aplicadas.
- Los 3 campos guardados con el texto que escribiste.
- La setter notificada solo en HT.
- Ningún mensaje automático fuera de la ventana de 24 h.

## Paso 5: Reporte
Devolveme:
1. Una captura del flujo completo.
2. La lista de campos, etiquetas y bloques creados.
3. Los textos que tuviste que acortar y cómo quedaron.
4. Lo que no pudiste hacer y por qué.
5. Qué falta para activarlo.
