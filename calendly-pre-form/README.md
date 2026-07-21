# Página puente: autocompleta Calendly + trackea quién agenda y quién no

La página funciona en **dos modos** (elige solo según cómo entre la persona):

### 🅰️ Modo recomendado — datos que llegan por la URL (sin formulario)
Si la persona **ya te dejó nombre, mail y WhatsApp antes** (ej: registro de la clase en
vivo), esos datos viajan **en el link** hacia esta página. La página los lee, **salta el
formulario** y muestra el Calendly **ya autocompletado**. La persona solo elige horario.
👉 Ver la sección **"Arrastrar los datos desde el registro (por la URL)"** más abajo.

### 🅱️ Modo respaldo — mini-formulario
Si alguien entra **directo** (sin datos en la URL), la página le pide **Nombre, Correo y
WhatsApp** y recién ahí muestra el Calendly autocompletado.

> El "Nombre y apellido" se divide solo: la primera palabra va al campo *Nombre* de Calendly
> y el resto al campo *Apellido*.

En los dos modos se registra **todo** en una Google Sheet:

- Cuando la persona llega → fila con estado **"Registrado — No agendó"**.
- Si termina de agendar en Calendly → esa misma fila pasa a **"Agendó ✅"**.

Así filtrás por **"Registrado — No agendó"** y tenés la lista de gente para escribirle por
WhatsApp y preguntarle por qué no terminó. 🎯

> Si la misma persona (mismo correo) entra dos veces, **no se duplica** la fila.

---

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La página que subís a Netlify. |
| `apps-script.gs` | El código que va DENTRO de tu Google Sheet. |

---

## Parte A — Google Sheet + Apps Script (guarda los datos)

1. Entrá a [sheets.new](https://sheets.new) y creá una planilla nueva. Ponele un nombre, ej: **"Leads Entrevista LE"**.
2. En el menú: **Extensiones → Apps Script**.
3. Borrá lo que haya y **pegá todo el contenido de `apps-script.gs`**. Guardá (💾).
4. Arriba a la derecha: **Implementar (Deploy) → Nueva implementación**.
   - Tipo (⚙️ Seleccionar tipo): **Aplicación web / Web app**.
   - **Ejecutar como:** *Yo (tu cuenta)*.
   - **Quién tiene acceso:** **Cualquier usuario / Anyone**. ⬅️ importante.
   - **Implementar**. Te va a pedir autorizar los permisos → aceptá con tu cuenta de Google.
5. Copiá la **URL del Web App** (termina en `/exec`). Se ve así:
   `https://script.google.com/macros/s/AKfy..................../exec`
6. Para probar que quedó viva: pegá esa URL en el navegador. Debería mostrar
   `{"ok":true,"message":"Endpoint activo"}`.

> La pestaña **"Leads"** con los títulos se crea sola la primera vez que llega un dato.

---

## Parte B — Configurar el `index.html`

Abrí `index.html` y editá **solo el bloque `NFM_CONFIG`** (arriba del todo):

```js
window.NFM_CONFIG = {
  calendlyUrl: "https://calendly.com/nicolasfernandezmiranda/entrevista-de-admision-li-clon",
  appsScriptUrl: "PEGÁ_ACÁ_LA_URL_/exec_DEL_PASO_A",
  campoWhatsApp: "a1"
};
```

- **`calendlyUrl`** → ya viene con tu link; cambialo si usás otro evento.
- **`appsScriptUrl`** → pegá la URL `/exec` de la Parte A.
  (Si lo dejás vacío, el autocompletado funciona igual pero **no guarda nada** en la planilla.)
- **`campoWhatsApp`** → `a1` porque el WhatsApp es la 1ª pregunta personalizada de tu Calendly.

---

## Parte C — Subir a Netlify

Opción más rápida (sin cuenta técnica):

1. Andá a **[app.netlify.com/drop](https://app.netlify.com/drop)**.
2. Arrastrá la **carpeta** `calendly-pre-form` (o solo el `index.html`) a la ventana.
3. Netlify te da una URL tipo `https://algo-random.netlify.app`. ¡Esa es tu página!
4. (Opcional) En **Site settings → Change site name** le ponés un nombre lindo,
   o le conectás tu propio dominio.

Esa URL de Netlify es la que ponés en tus anuncios / bio / mensajes, **en lugar** del link directo de Calendly.

---

## ⭐ Arrastrar los datos desde el registro (por la URL)

Este es el punto clave para que **no tengan que cargar los datos dos veces**.

Cuando tu página de registro (la de la clase en vivo) manda a la persona a esta página,
tenés que **adjuntar sus datos al final del link**, así:

```
https://TU-PAGINA.netlify.app/?nombre=Maria+Perez&email=maria@mail.com&whatsapp=+5491123456789
```

La página entiende varios nombres de parámetro (por si tu herramienta usa otros):

| Dato | Parámetros que acepta |
|---|---|
| Nombre | `nombre`, `name`, `fullname` — o `first_name` + `last_name` por separado |
| Correo | `email`, `correo`, `mail` |
| WhatsApp | `whatsapp`, `telefono`, `phone`, `celular`, `numero` |

👉 Lo importante: en tu herramienta de registro, en vez de escribir los datos a mano, usás
los **campos dinámicos (merge fields)** de la persona. Ejemplos según la herramienta:

- **Genérico / HTML propio:** armás el link con los valores reales al redirigir.
- **GoHighLevel / HighLevel:**
  `...netlify.app/?nombre={{contact.first_name}} {{contact.last_name}}&email={{contact.email}}&whatsapp={{contact.phone}}`
- **Systeme.io / Mailchimp / ActiveCampaign / ManyChat:** usá los merge tags equivalentes
  de cada uno (`*|FNAME|*`, `%FIRSTNAME%`, etc.) en la URL de redirección post-registro.

> El WhatsApp conviene mandarlo con **código de país** (ej: `+549...`). Si tu herramienta ya
> lo guarda así (como el `+54` de tu formulario de registro), sale perfecto.

**Importante:** que la redirección post-registro apunte a **esta página** (no directo a
Calendly). Si va directo a Calendly, se pierde el tracking de "no agendó".

---

## Sobre el autocompletado en Calendly (importante)

Calendly rellena las preguntas personalizadas por **orden**:
`a1` = 1ª pregunta, `a2` = 2ª, y así.

En tu formulario, el WhatsApp es la **1ª** pregunta personalizada → **a1**.
Por eso está configurado `campoWhatsApp: "a1"`.

👉 **Si algún día cambiás el orden de las preguntas en Calendly** (o agregás una nueva
antes del WhatsApp), actualizá ese valor en `NFM_CONFIG`.

**Verificación rápida:** abrí tu página agregándole datos de prueba en el link, ej:
`https://TU-PAGINA.netlify.app/?nombre=Maria+Perez&email=maria@mail.com&whatsapp=+5491123456789`
y fijate en Calendly que el WhatsApp aparezca bien cargado. Nombre, Apellido y Correo se
autocompletan siempre (son campos nativos de Calendly).

> Nota: el campo de teléfono de Calendly puede ser exigente con el formato. La página ya
> arma el número en formato internacional (ej. `+59171234567`). Si en tu Calendly el
> WhatsApp no se autocompleta, avisá y lo ajustamos (a veces conviene dejarlo como campo
> de texto en Calendly en vez de tipo "teléfono").

---

## Cómo usar la planilla para el seguimiento

En la pestaña **Leads** vas a tener estas columnas:

`Lead ID · Registrado · Nombre · Apellido · Correo · WhatsApp · Estado · Agendó · Origen`

- **Los que NO agendaron:** filtrá la columna **Estado** por **"Registrado — No agendó"**.
  Esa es tu lista para escribir por WhatsApp. Tenés el número ya en formato internacional.
- **Los que SÍ agendaron:** estado **"Agendó ✅"** con fecha y hora.
- **Origen:** te dice de dónde vino (parámetros UTM del link o página de referencia),
  útil si mandás la página desde distintos lados.

💡 Tip: podés crear un **filtro** o una **vista con filtro** en la columna Estado para no
tocar los datos originales, y armar una tabla dinámica "Agendó vs No agendó" para ver la
tasa de conversión.
