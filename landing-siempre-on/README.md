# Landing Siempre-On · NFM

Una sola URL, prendida los 365 días. Las fechas y el copy se cambian solos.
Archivo único: **`index.html`**.

---

## 1. Decisión de los dos títulos

### TEMA A · `Cumplís con todos menos con vos` (ya definido, arranca el 10 de agosto)

Bajada: *La razón neurológica por la que tu cerebro ejecuta lo ajeno y archiva lo tuyo.*
Es el título que ya está decidido en el MD (Parte 2) y no se toca.

### TEMA B · `El que sostiene todo es el que no avanza` (25 de agosto)

Bajada: *Escalá tu vida, no tu cansancio: por qué tu operación crece y lo tuyo sigue exactamente donde estaba.*

**Por qué no dejé "Escalá tu vida, no tu cansancio" como título de la clase.** Me pediste que valide si atrae
Platinum. Contra el MD, no: recluta Gold. Tres razones, todas del documento:

1. **La puerta de entrada está del lado equivocado.** Parte 1: *"si la clase entra por salud y desborde
   personal, se llena de Gold. Si entra por 'tu operación te está comiendo y vos sos la variable de ajuste',
   se llena de Platinum"*. "Cansancio" es la puerta del cuerpo. En el corpus, los 4 de 4 Gold entran por el
   cuerpo y la vida personal; los Platinum entran por el negocio y el equipo.
2. **Le promete al Platinum algo que no quiere comprar.** Parte 1: *"NO quieren trabajar menos"* — Diego, 56:
   *"no me interesa estar inactivo a los 56 años, para nada"*. "No tu cansancio" vende alivio. El Platinum no
   paga US$3.000 por alivio: paga por dejar de ser el cuello de botella sin bajar la producción.
3. **Es un título de beneficio, sin mecanismo.** Se puede creer entero y seguir de largo (falla el test binario
   de Parte 2). "Cumplís con todos menos con vos" es espejo y obliga a preguntar *por qué*. El nuevo B
   mantiene esa propiedad.

**Qué hice en cambio, sin tirar nada:**

- `Escalá tu vida, no tu cansancio` **sigue siendo el nombre del ángulo B en la pauta** (los creativos ya
  existen y así queda cargado en el doc de Estrategia Siempre-On, Regla 03) y **vive como bajada dentro de la
  landing**. Nada de lo que ya está corriendo se rompe.
- El **título de la clase** del 25 pasa a ser `El que sostiene todo es el que no avanza`, que:
  - abre la puerta Platinum **sin jerga de gestión** → respeta Parte 9 (*"el ancho arriba, la puntería abajo"*:
    la jerga sube el CPL y baja el registro);
  - es una frase claramente distinta de la del 10, así el lead que ya vino no ve lo mismo dos veces;
  - corre sobre el **mismo mecanismo** (urgencia prestada) → no hay que rehacer la clase, sólo rotar el marco;
  - tiene respaldo textual real: Diego (*"la variable de ajuste se termina transformando en Diego"*),
    Marcelo (*"un engranaje en mi vida, no el motor"*), Francisco (delegó el seguimiento de lo ajeno, no el de
    lo suyo).
- `La variable de ajuste sos vos` queda donde el MD lo dejó: **creativos para dueños y gerentes, no como
  título**.

Para septiembre (4 clases al mes) el par A/B alterna solo, semana a semana. Cuando quieras un tercer tema, se
agrega un bloque `C` en `TEMAS` y se lo referencia en `CLASES`.

---

## 2. Las clases cargadas

| Fecha | Día | Hora | Tema | Título en pantalla | UTM de campaña |
|---|---|---|---|---|---|
| 2026-08-10 | lunes | 19:00 ART | A | Cumplís con todos menos con vos | `clase-ago10-cumplis-con-todos` |
| 2026-08-25 | martes | 19:00 ART | B | El que sostiene todo es el que no avanza | `clase-ago25-sostenes-todo` |

Para cambiarlas se toca **una sola línea** en `index.html`, bloque `CONFIG.CLASES`:

```js
CLASES: [
  { fecha:'2026-08-10', tema:'A', utm:'clase-ago10-cumplis-con-todos' },
  { fecha:'2026-08-25', tema:'B', utm:'clase-ago25-sostenes-todo'     }
],
```

---

## 3. Qué cambia solo y cuándo

**A las 19:00:00 hs de Argentina del día de la clase**, la landing salta sola a la clase siguiente. Cambian
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

**Lo que hay que hacer del lado de GHL:**

- Poner el Meta Pixel en *Settings → Tracking Code → HEAD* (en el archivo está sólo para que el preview
  funcione; si lo dejás en los dos lugares, cuenta doble).
- Crear los 3 campos personalizados del punto 3 (opcional pero recomendado).
- **Sumar al form la pregunta discriminante del MD (Parte 9): *"¿Hay gente cuyo trabajo depende de tus
  decisiones? ¿Cuántas?"***. Es lo que separa Platinum de Gold antes de agendar, y es gratis ponerlo acá.
- El evento `Lead` está **apagado** en la landing (`TRACKEAR_LEAD_EN_PAGINA: false`) porque asumo que ya lo
  dispara GHL. Si no lo dispara, poné `true` y la landing lo manda al enviarse el form.

---

## 5. Cómo verlo antes de publicar

| Querés ver | URL |
|---|---|
| La clase del 25 (tema B) tal como se va a ver | `?nfm_tema=B` |
| Cómo queda la landing el 11 de agosto | `?nfm_now=2026-08-11T15:00:00Z` |
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
- Estado "en vivo" con `MINUTOS_DE_GRACIA: 90`: oculta el contador y muestra el cartel.
- `CERRAR_CAPTACION_HORAS: 48`: el 8/8 a las 20:00 ya apunta al 25.
- UTM: con pauta pasa los de la URL; sin pauta etiqueta `directo` + la campaña de la clase.
- Cero errores de JavaScript en las 5 variantes.
- Mobile 390 px: sin scroll horizontal, ningún elemento desborda.

Las imágenes y los iframes (GHL, YouTube) están bloqueados en este entorno de prueba, así que eso hay que
mirarlo una vez publicado. Son las mismas URLs que ya usa la landing que está al aire.

---

## 7. Dos cosas para tener en el radar

- **El alto del form.** Está en `FORM_ALTO_MINIMO: 729`, heredado del form anterior. Si el "Form AGOSTO NUEVO"
  es más corto o más largo, se ajusta ese número (el script de GHL igual lo redimensiona solo en la mayoría
  de los casos).
- **Riesgo de creativo único.** Del doc de estrategia: un solo creativo trajo el 45% de los leads. La landing
  ahora aguanta dos ángulos, pero si la pauta sigue dependiendo de un anuncio, el cuello de botella se corre
  para arriba. Con dos títulos definidos ya hay material para dos familias de ganchos.
