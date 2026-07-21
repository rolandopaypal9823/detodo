# Pre-formulario de Calendly con autocompletado + tracking en Google Sheets

Flujo en 2 pasos para tu **Entrevista de Admisión (LE)**:

1. **Paso 1 — Tus datos:** la persona completa Nombre, Apellido, Correo, WhatsApp y Profesión.
2. **Paso 2 — Calendly:** se muestra tu Calendly con **esos datos ya autocompletados** (no los vuelve a escribir) y elige día/horario.

Y en el medio se registra **todo** en una Google Sheet:

- Apenas envían el Paso 1 → fila con estado **"Registrado — No agendó"**.
- Si terminan de agendar en Calendly → esa misma fila pasa a **"Agendó ✅"**.

Así podés filtrar por **"Registrado — No agendó"** y tenés la lista de gente para escribirle por WhatsApp y preguntarle por qué no terminó. 🎯

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
  campoWhatsApp: "a1",
  campoProfesion: "a2"
};
```

- **`calendlyUrl`** → ya viene con tu link; cambialo si usás otro evento.
- **`appsScriptUrl`** → pegá la URL `/exec` de la Parte A.
  (Si lo dejás vacío, la página funciona igual pero **no guarda nada** en la planilla.)

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

## Sobre el autocompletado en Calendly (importante)

Calendly rellena los campos por **orden** de las preguntas personalizadas:
`a1` = 1ª pregunta, `a2` = 2ª, y así.

En tu formulario el orden es:

1. ¿Cuál es tu número de WhatsApp?  → **a1**
2. ¿Cuál es tu profesión…?          → **a2**

Por eso está configurado `campoWhatsApp: "a1"` y `campoProfesion: "a2"`.

👉 **Si algún día cambiás el orden de las preguntas en Calendly** (o agregás una nueva
antes de esas), actualizá esos dos valores en `NFM_CONFIG`.

**Verificación rápida:** entrá a tu página, completá el Paso 1 y fijate en Calendly que
el WhatsApp y la Profesión aparezcan bien cargados. Nombre, Apellido y Correo se
autocompletan siempre (son campos nativos de Calendly).

> Nota: el campo de teléfono de Calendly puede ser exigente con el formato. La página ya
> arma el número en formato internacional (ej. `+59171234567`). Si en tu Calendly el
> WhatsApp no se autocompleta, avisá y lo ajustamos (a veces conviene dejarlo como campo
> de texto en Calendly en vez de tipo "teléfono").

---

## Cómo usar la planilla para el seguimiento

En la pestaña **Leads** vas a tener estas columnas:

`Lead ID · Registrado · Nombre · Apellido · Correo · WhatsApp · Profesión · Estado · Agendó · Origen`

- **Los que NO agendaron:** filtrá la columna **Estado** por **"Registrado — No agendó"**.
  Esa es tu lista para escribir por WhatsApp. Tenés el número ya en formato internacional.
- **Los que SÍ agendaron:** estado **"Agendó ✅"** con fecha y hora.
- **Origen:** te dice de dónde vino (parámetros UTM del link o página de referencia),
  útil si mandás la página desde distintos lados.

💡 Tip: podés crear un **filtro** o una **vista con filtro** en la columna Estado para no
tocar los datos originales, y armar una tabla dinámica "Agendó vs No agendó" para ver la
tasa de conversión.
