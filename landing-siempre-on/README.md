# Landing Siempre-On · NFM

Una sola URL, prendida los 365 días. Las fechas y el copy se cambian solos.

- **`index.html`** — la landing de registro.
- **`thank-you.html`** — la página de gracias, con la misma lógica de fechas y el grupo de WhatsApp por clase.

**Estructura:** exactamente la misma de la landing que ya está al aire — nav → hero → prueba social →
espejo → formulario → mecanismo → qué vas a descubrir → testimonios → el giro → CTA final → footer. No se
agregó, sacó ni movió ninguna sección. Lo que cambia es el copy, y que ahora es dinámico.

---

## 1. Decisión de los dos títulos

### TEMA A · `Cumplís con todos menos con vos`

Bajada: *La razón neurológica por la que tu cerebro ejecuta lo ajeno y archiva lo tuyo.*
Es el título que ya está decidido en el MD (Parte 2) y no se toca.

### TEMA B · `Escalá tu vida, no tu cansancio`

Bajada: *La razón neurológica por la que el que sostiene todo es el último en avanzar.*

**Decisión de Nico: título ancho arriba, filtro abajo.** El título tiene que ser fácil de decir y de
recordar, y su trabajo es el show-up rate, no calificar. Es Parte 9 del MD: *"el ancho arriba, la puntería
abajo. Nunca al revés"* — el filtro se corre hacia donde no cuesta plata (bajada, semilla, quiz de registro).

**El riesgo conocido, y dónde se compensa.** Como título, "cansancio" entra por la puerta del cuerpo, que en
el corpus es la puerta Gold (Parte 1: *"si la clase entra por salud y desborde personal, se llena de Gold"*).
Por eso todo lo que viene abajo del título recluta Platinum de forma explícita:

| Dónde | Qué hace el filtro |
|---|---|
| Bajada | *"el que sostiene todo es el último en avanzar"* → mueve el foco del cuerpo a la operación |
| Semilla del hero | *"tu equipo, tus clientes, tu área: todo se mueve porque estás vos… la variable de ajuste siempre termina siendo la misma: vos"* |
| Micro bajo el botón | *"No es para trabajar menos: es para dejar de ser el cuello de botella de tu propia vida"* → desactiva la promesa de alivio, que es lo que rompía el perfil (Diego, 56: *"no me interesa estar inactivo a los 56 años"*) |
| Bajada del formulario | *"Para dueños, socios, gerentes y líderes que sostienen la operación de todos y hace años no mueven la propia"* |
| Quiz de registro | *"¿Hay gente cuyo trabajo depende de tus decisiones? ¿Cuántas?"* ← el discriminador real |

**Si el mix de leads del 25 viene más Gold que el del 10**, la palanca no es cambiar el título: es endurecer
la bajada y el quiz. El título se toca último.

`La variable de ajuste sos vos` sigue donde el MD lo dejó: **creativos para dueños y gerentes, no como
título**.

El par A/B alterna solo, clase a clase. Cuando quieras un tercer tema, se
agrega un bloque `C` en `TEMAS` y se lo referencia en `CLASES`.

---

## 2. Las clases cargadas

### Septiembre 2026 — ritmo semanal, martes 19:00 ART

Cada clase tiene **dos fechas distintas**, y esto es lo importante:

- **`fecha`** — cuándo se da la clase.
- **`desde`** — cuándo la landing **empieza a promocionarla** (00:00 hs de Argentina de ese día).

Son cosas separadas a propósito: la captación de una clase arranca días antes de que la anterior se dé.
El cambio de temática lo manda `desde`, no la fecha de la clase.

| Captación desde | Clase | Tema | Título en pantalla | Grupo de WhatsApp |
|---|---|---|---|---|
| ya corriendo (24 ago) | mar 8 sep | A | Cumplís con todos menos con vos | ✅ cargado |
| **2 sep, 00:00** | mar 15 sep | B | Escalá tu vida, no tu cansancio | ✅ cargado |
| **11 sep, 00:00** | mar 22 sep | A | Cumplís con todos menos con vos | ✅ cargado (revisar "semptiembre") |
| **20 sep, 00:00** | ⚠️ octubre, sin cargar | B | — | ⚠️ falta |

```js
CLASES: [
  { fecha:'2026-09-08', desde:'2026-08-24', tema:'A', utm:'clase-sep08-cumplis-con-todos' },
  { fecha:'2026-09-15', desde:'2026-09-02', tema:'B', utm:'clase-sep15-escala-tu-vida'    },
  { fecha:'2026-09-22', desde:'2026-09-11', tema:'A', utm:'clase-sep22-cumplis-con-todos' }
],
```

**Falta la clase de octubre con `desde:'2026-09-20'`**, que es cuando arranca su captación. Sin ella: del
20 al 22 la landing sigue mostrando la del 22 (correcto, todavía no pasó), y después del 22 a las 19:00
entra el modo semanal automático y muestra el martes 29, que no es una clase real.

Los temas se repiten alternados: A, B, A, B. El copy de cada tema está una sola vez en `TEMAS` —
no se duplica por clase.

---

## 3. Qué cambia solo y cuándo

**A las 00:00 hs de Argentina del día que dice `desde`**, la landing salta sola a la clase siguiente. Cambian
de una vez: contador, fecha del hero, fecha del formulario, fecha del CTA final, título del navegador, H1,
bajada, semilla, espejo completo (6 ítems), sección del mecanismo, los 4 puntos de "qué vas a descubrir",
el giro y el cierre. **Ninguna fecha se escribe a mano en el copy.**

El cálculo se hace en UTC con Argentina fija en UTC−3 (no tiene horario de verano), así el contador es
correcto para el que entra desde España, México o Miami.

### Tres perillas en `CONFIG`, todas listas para cuando lo definas con el trafficker

| Perilla | Ahora | Para qué |
|---|---|---|
| `MINUTOS_DE_GRACIA` | `0` | Minutos **después** de las 19:00 en los que la landing sigue apuntando a esa clase. En 0 el salto es a las 19:00 en punto, como pediste. Si lo pones en `90`, durante la clase la landing muestra un cartel **"La clase está empezando ahora — registrate y entrás directo"** en lugar del contador, y recién después salta. Ya está probado y funcionando. |
| `CERRAR_CAPTACION_HORAS` | `0` | Horas **antes** de la clase en las que la landing deja de captar para esa clase y pasa a la siguiente. Es exactamente lo que dijiste que iban a analizar: poné `48` y la captación del 10 de agosto se corta el sábado 8 a las 19:00, y desde ese momento todo el tráfico entra ya a la clase del 25. |
| `AUTO_SEMANAL` | `true` | Cuando se terminan las fechas cargadas, sigue solo: próximo martes 19:00, alternando tema A/B. La URL **nunca** muestra una fecha vencida, ni si te olvidás de cargar septiembre. |

Cambiar el día de la clase automática: `AUTO_DIA` (0 = domingo, 1 = lunes, 2 = martes…).

---

## 4. El form único + UTM (tu duda)

**Sí, conviene un solo form para siempre.** Es lo que hace que el pixel y la data se acumulen en vez de
reiniciarse en cada lanzamiento (Regla 02 del doc de estrategia). La landing ya lo resuelve así:

1. Los UTM que traiga la URL se **inyectan en el `src` del iframe** antes de que cargue, así llegan a GHL con
   el lead. Se pasan: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `utm_id`,
   `fbclid`, `gclid`, `ttclid`, `ad_id`, `adset_id`, `campaign_id`, `ref`.
2. **El que entra sin UTM no queda huérfano.** Orgánico, WhatsApp, link pegado a mano: si falta `utm_source`
   se etiqueta `directo`, y si falta `utm_campaign` se etiqueta con la campaña de la clase activa
   (`clase-ago10-cumplis-con-todos`, etc.). Hoy esos leads se pierden en "sin origen".
3. Además viajan tres parámetros propios: `clase_fecha` (`2026-08-25`), `clase_tema` (`A`/`B`) y `edicion`.
   **Si en el form de GHL creás tres campos personalizados con las claves `clase_fecha`, `clase_tema` y
   `edicion`, se llenan solos** y podés segmentar por clase sin depender de la pauta. Eso es lo que vuelve
   sistemática la cosa: un form para todo el año, y en el CRM cada lead sabe a qué clase se anotó.

**Plan B si GHL no guarda los campos personalizados:** poné `CLASE_EN_UTM_TERM: true` en `CONFIG` y la
clase viaja también en `utm_term`, que GHL captura nativo sin configurar nada. En ese caso hay que **sacar
`utm_term` de la URL de los anuncios** (ahí Meta manda el nombre del conjunto y se pisarían) y usar
`adset_id={{adset.id}}` en su lugar, que la landing ya reenvía al form.

**Lo que hay que hacer del lado de GHL:**

- Poner el Meta Pixel en *Settings → Tracking Code → HEAD* (en el archivo está sólo para que el preview
  funcione; si lo dejás en los dos lugares, cuenta doble).
- Crear los 3 campos personalizados del punto 3 (opcional pero recomendado).
- **Sumar al form la pregunta discriminante del MD (Parte 9): *"¿Hay gente cuyo trabajo depende de tus
  decisiones? ¿Cuántas?"***. Es lo que separa Platinum de Gold antes de agendar, y es gratis ponerlo acá.
- **Ningún evento de conversión se dispara por código.** Ni en la landing ni en la página de gracias.
  El único evento del pixel es `PageView`. La conversión (`Lead` / `CompleteRegistration`) la manda
  GoHighLevel por la **API de Conversiones**, filtrada por la respuesta del form. Ver sección 9.

---

## 5. `/test-landing2` · ver la segunda versión antes de que exista

Cualquier URL que contenga **`test-landing2`** muestra la landing tal como va a quedar sola
**después** de que pase la clase que está activa hoy. Funciona de dos formas:

- **Pegándoselo a la landing real:** `tulanding.com/clase?test-landing2` — no hay que crear nada.
- **Como página aparte en GHL:** creá una página con el path `/test-landing2` y pegale el mismo custom
  code. Detecta el path solo.

Lo que vas a ver ahí: título *El que sostiene todo es el que no avanza*, fecha **martes 25 de agosto**,
contador corriendo hacia el 25, y todo el copy del tema B. Arriba aparece una barra naranja
**"Modo prueba · simulando que ya pasó la clase del 10 de agosto"** para que no se confunda con la real.

No es una copia congelada: es el mismo motor salteando una clase. Si mañana cambiás las fechas o el copy,
`/test-landing2` muestra el cambio también. Después del 25 de agosto, esa misma URL te va a mostrar la
clase del 1 de septiembre. Ojo: si el pixel está puesto a nivel sitio en GHL, las visitas a esa página
cuentan como PageView igual que cualquier otra.

### Los demás modos de preview

| Querés ver | URL |
|---|---|
| La versión siguiente, la que se publica sola | `?test-landing2` |
| Sólo el copy del tema B, con la fecha de hoy | `?nfm_tema=B` |
| Un día puntual del calendario | `?nfm_now=2026-08-11T15:00:00Z` |
| Cómo queda en septiembre, en modo semanal | `?nfm_now=2026-09-20T15:00:00Z` |
| Que los UTM entren bien al form | `?utm_source=meta&utm_medium=cpc&utm_campaign=test` |

`nfm_now` es hora UTC: para simular las 19:00 de Argentina se usan las `22:00:00Z`.

---

## 6. QA hecho

Verificado en Chromium headless, con el código real del archivo:

- Selección de clase correcta en 15 momentos distintos: hoy, 18:59 del 10/8, 19:00:01 del 10/8, el 24/8,
  18:59 del 25/8, 19:00:01 del 25/8, y de ahí en adelante en modo semanal hasta diciembre (29/12 cae martes).
- Cambio completo de copy entre A y B: título del navegador, H1, bajada, semilla, espejo (6 ítems), mecanismo
  (título, nodos, cita), 4 puntos de la clase, giro y cierre. Sin restos del otro tema.
- Fechas en castellano y con el día de la semana correcto: *Lunes 10 de agosto*, *Martes 25 de agosto*,
  *Martes 1 de septiembre*.
- `/test-landing2` en las dos formas (como path de página y como `?test-landing2`): muestra el 25 de agosto
  con el tema B, el contador corriendo hacia el 25 y la barra de modo prueba, sin romper la landing real.
- Estado "en vivo" con `MINUTOS_DE_GRACIA: 90`: oculta el contador y muestra el cartel.
- `CERRAR_CAPTACION_HORAS: 48`: el 8/8 a las 20:00 ya apunta al 25.
- UTM: con pauta pasa los de la URL; sin pauta etiqueta `directo` + la campaña de la clase.
- Cero errores de JavaScript en las 5 variantes.
- Mobile 390 px: sin scroll horizontal, ningún elemento desborda.

Las imágenes y los iframes (GHL, YouTube) están bloqueados en este entorno de prueba, así que eso hay que
mirarlo una vez publicado. Son las mismas URLs que ya usa la landing que está al aire.

---

## 6bis. La thank you page (`thank-you.html`)

Misma estructura que la que ya tenías (nav, confirmación, video de Loom, los 2 pasos, el disclaimer del
mail, la tarjeta del evento y el footer). Lo que cambió: **fecha, día de la semana, título de la clase,
título del navegador y link del grupo de WhatsApp** salen del mismo calendario que la landing.

### ⚠️ Un grupo de WhatsApp por clase

El link que me pasaste tiene la fecha adentro (`clase-10-08-neurociencia-aplicada`), así que **cada clase
necesita su propio grupo**. Por eso el link va cargado por clase:

```js
CLASES: [
  { fecha:'2026-09-08', tema:'A', utm:'...', wa:'https://go.wha.link/clase-8-de-septiembre-neurociencia' },
  { fecha:'2026-09-15', tema:'B', utm:'...', wa:'' },   // ⚠️ falta
  { fecha:'2026-09-22', tema:'A', utm:'...', wa:'' }    // ⚠️ falta
]
```

**Sólo está cargado el grupo del 8.** Mientras `wa` esté vacío, el botón cae en `GRUPO_FALLBACK` (que hoy es
el grupo del 8) para que nunca quede roto — pero eso significa que los leads de esa clase entrarían al grupo
equivocado y nunca recibirían el acceso. **Cargá cada uno antes de las 19:00 del martes anterior.**

Para verificar: entrá a `thank-you.html?test-landing2` y mirá si la barra naranja dice *"⚠ falta cargar el
grupo de WhatsApp de esta clase"*. Cuando lo cargues, el aviso desaparece. También queda un warning en la
consola del navegador.

> Se evaluó usar un link permanente con redirect (`nicolasfernandezmiranda.com/webinar-whatsapp`) para no
> tener que cargar uno por semana. Se descartó: agrega un salto de WordPress entre el lead y el grupo, o sea
> un punto de falla más justo en el paso más crítico del embudo.

### El caso borde que resuelve

Alguien se registra 18:59 del día de la clase y aterriza en la thank you page 19:00:30, cuando la landing ya
rotó. Sin protección le mostraríamos la clase siguiente y lo mandaríamos al grupo equivocado. La landing deja
guardada la clase en el navegador (`sessionStorage`) y la thank you page la lee, así que ve la clase a la que
**realmente** se anotó. El orden de prioridad es: `?clase_fecha=` en la URL → lo guardado por la landing →
el calendario.

### Si querés un video distinto por clase

Agregale `loom:'ID_DEL_VIDEO'` a la clase en `CLASES`. Si no, usa el de `CONFIG.LOOM_ID` para todas.

### Mantenimiento

El bloque `CLASES` está duplicado en los dos archivos (la landing y la thank you page) porque en GHL cada
página es independiente. **Si agregás o cambiás una clase, hacelo en los dos.** Los dos archivos tienen un
comentario recordándolo.

---

## 7. Los 3 testimonios: dos están bien, uno no

El criterio del MD (Parte 5) es elegir **por afinidad de oficio con quien escucha**, y el discriminador
Platinum (Parte 1) es *"¿hay gente cuyo trabajo depende de sus decisiones?"* — 13 de 14 compradores Platinum
dicen sí. Contra eso:

| Caso | Veredicto | Por qué |
|---|---|---|
| **Celina** — arquitecta, lidera ~45 personas | ✅ **El más fuerte, va primero** | Lidera equipo grande, y su hecho es exactamente lo propio postergado años: la ciudadanía de los hijos, y su primer año con actividad física desde que es madre. Es urgencia prestada resuelta, contada sin una sola palabra de teoría. |
| **Andrés** — ing. agrónomo, lidera una comunidad | ✅ **Sirve** | Tiene gente a cargo, y "aprendió a decir que no" es literalmente dejar de aceptar urgencia ajena. Encaja con el mecanismo sin forzarlo. |
| **Pierina** — teóloga, doctoranda en Roma | ⚠️ **Es la que sobra** | No tiene gente cuyo trabajo dependa de sus decisiones. Es el perfil que en el corpus se queda en Gold (Carolina, profesora: *"se me escapaba el presupuesto"*). Su caso es admirable pero le habla al académico, no al dueño con equipo — y con el tema B, que apunta a dueños y gerentes, el desajuste se agranda. |

**El reemplazo correcto es Germán** — farmacéutico, dueño, 6 empleados: *"de burnout y números que no
cerraban a delegación y norte anual"* (MD Parte 5). Es el único caso del documento que junta las tres cosas
que compra el Platinum: dueño, equipo a cargo, y salida del cuello de botella sin bajar producción. Sirve
para las dos temáticas y es perfecto para la B.

**Lo que me falta para hacerlo: el video de Germán.** Los 3 IDs de YouTube que están en el código son los
que venían de la landing anterior; no tengo uno suyo y no lo voy a inventar. Así que la sección quedó
funcionando con los 3 actuales, ordenados de más fuerte a menos (Celina → Andrés → Pierina), y **dejé el
hueco preparado en el código**: hay un comentario arriba de la tercera tarjeta con el texto de Germán ya
escrito, sólo hay que pegar el ID del video. Si no aparece el de Germán, la segunda opción es Sol Romero
(contadora en compañía de seguros: la empresa le pagó la capacitación que iba a pagar ella, y volvió al
tango) — no lidera, pero al menos suena corporativo.

---

## 8. Dos cosas para tener en el radar

- **El alto del form.** Está en `FORM_ALTO_MINIMO: 729`, heredado del form anterior. Si el "Form AGOSTO NUEVO"
  es más corto o más largo, se ajusta ese número (el script de GHL igual lo redimensiona solo en la mayoría
  de los casos).
- **Riesgo de creativo único.** Del doc de estrategia: un solo creativo trajo el 45% de los leads. La landing
  ahora aguanta dos ángulos, pero si la pauta sigue dependiendo de un anuncio, el cuello de botella se corre
  para arriba. Con dos títulos definidos ya hay material para dos familias de ganchos.

---

## 9. Trackeo de Meta: por qué el código NO dispara conversiones

**Regla:** el pixel en las páginas dispara **sólo `PageView`**. Toda conversión sale de GoHighLevel por
la **API de Conversiones (CAPI)**.

### El problema que esto resuelve

Había un `fbq('track','Lead')` en la página de gracias, y al mismo tiempo GHL mandaba `Lead` por CAPI
para los leads que no son estudiantes. **El pixel y la CAPI no se deduplican solas**: Meta sólo une dos
eventos si comparten el mismo `event_id` y `event_name`. Sin ese `event_id` compartido, los suma.

Resultado observado: **4.000 leads reales → ~6.000 en Meta**. La cuenta cierra:

```
Pixel Lead (todos los que ven la página de gracias)   ≈ 4.000
CAPI Lead  (sólo los que NO son estudiantes)          ≈ 2.000
                                                      ────────
Meta reportaba                                        ≈ 6.000
```

Y el pixel infla todavía un poco más, porque dispara en **cada carga** de la página de gracias: un
refresh, un "volver atrás" o alguien que llega directo al link contaban como registro nuevo.

### Cómo quedó

| Página | Eventos del pixel | Conversión |
|---|---|---|
| Landing de registro | `PageView` | — |
| Página de gracias | `PageView` | la manda GHL por CAPI |

Se eliminó también el interruptor `TRACKEAR_LEAD_EN_PAGINA` de la landing, que estaba apagado pero
permitía volver a romper esto con un `true`.

### Si algún día se quiere volver a tener el evento por pixel

No alcanza con agregar el `fbq`. Habría que mandar **el mismo `event_id`** desde el pixel y desde la
CAPI para que Meta los una. Mientras GHL no exponga ese `event_id`, la única opción segura es la de
ahora: **uno solo de los dos lados, nunca los dos**.
