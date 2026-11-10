# Landing "Un sistema que lo sostenga"

Landing de registro a la clase en vivo, apuntada al perfil Platinum (profesionales y empresarios con equipo). **Misma estructura y mismo azul que la del 04/11**, con el copy nuevo. El copy sale de las llamadas de venta del 22/09, 04/11 y octubre. Ver `../HANDOFF-landing-filtro-platinum.md`.

| Archivo | Qué es |
|---|---|
| `index-popup.html` | Landing con el quiz y el form en un popup. Cualquier botón lo abre; se cierra sólo con la X. |
| `calendario-clase-16-nov.md` / `.ics` | Link de Google Calendar y archivo para iPhone/Outlook. |

Se pega en GHL igual que las anteriores: lo que está entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ» va en el bloque de custom code. El pixel de Meta va adentro con la guarda para no contar dos PageView.

## Clase del lunes 16 de noviembre, 19:00 hs (Argentina)

1. **Fecha:** `FECHA: '2026-11-16'` en el `CONFIG` del final. La píldora, el contador, la hora local y todos los textos con fecha se arman solos desde ahí.
2. **`UTM_CLASE`:** `clase-nov16-sistema`. Va en `edicion` y en el `utm_campaign` de los leads sin UTM.
3. **Thank you de registro:** `nfm-clase-paga/thankyou-registro-sin-popup.html` (sin asientos USD 5 / USD 9), con la clase del lunes 16 y el grupo https://go.wha.link/b2DPze. Va en la redirección del "Form AGOSTO NUEVO". Si se toca `thankyou-oto.html`, regenerar con `python3 nfm-clase-paga/gen-thankyou-sin-popup.py` desde la raíz del repo.
4. **Calendario y QR:** `calendario-clase-16-nov.*` y `qr/qr-calendly-clase1611.*`.
5. **Puerta al Zoom** (`zoom-nfm.netlify.app`): actualizar el link de Zoom y la clave anti-duplicados para esta clase.

## Qué cambió respecto de la del 04/11

Las secciones y el orden son los mismos. Cambia el copy:

- **Hero:** sin subtítulo.
  - Etiqueta: "Para profesionales y empresarios que sienten que todo pasa por ellos".
  - Título: "Dejá de sobrecargarte con todo y armá un **sistema de neurociencia** que lo sostenga".
  - Debajo: "Neurociencia para el Alto Rendimiento Profesional · con Nico Fernández Miranda".
- **Widget de tachados** ("Esto tampoco es la solución"): "Más pasa por vos, más alto el precio que pagás". Tacha 5 cosas que ya probaron (hacerlo todo vos, contestar el celular en vacaciones, estar en cada decisión de tu equipo, otro libro o curso de productividad, exigirte más) y da como resultado "un sistema que lo sostenga".
- **Historia de Nico:** igual. Sólo cambia el último párrafo de "Hoy".
- **"Armá tu sistema de productividad en vivo el 16 de noviembre"** (reemplaza "Qué vas a ver"): sólo el título y una escalera dibujada con tres peldaños de una línea cada uno, sin bajadas ni textos chicos. De abajo hacia arriba: "Cuidar tu bienestar mental", "Cuidar tu bienestar físico" y "Las habilidades técnicas que te permiten crecer", con las etiquetas de ejemplo (hábitos, concentración, delegación, inteligencia artificial).
  - ⚠️ **La escalera es un dibujo hecho acá, no la imagen original de Nico.** Si hay una imagen oficial, se reemplaza el bloque `.nfm-lad`.
- **Casos:** los mismos. Encabezado para dueños y profesionales con equipo, y cierre "Ninguno vio caerse lo que había construido".
- **"Para quién es esta clase"** (vuelve, entre los casos y el cierre): es y no es para vos, sin hablar de plata, más la línea de seriedad.
- **Cierre:** "El 16 de noviembre vas a ver cómo armar el sistema que lo sostenga".

Se sacaron, por pedido: el bloque naranja "¿Te reconocés?" y el bloque "Tu cerebro está decidiendo por todo tu equipo". Los textos siguen en `../COPY-landing-sistema-que-lo-sostenga.md` por si se quieren volver a usar.

## Quiz

- **Pregunta de etapa:** sin cambios, mismas palabras.
- **Etapa A y B:** igual que antes. Pregunta del equipo, "a qué te dedicás" y el form principal ("Form AGOSTO NUEVO"), con etapa, equipo, nivel y dedicación en la URL.
- **Etapa C:** no ve form ni clase. Al tocar "Continuar" aparece un mensaje y el botón "Quiero el regalo de Nico", que va a `CONFIG.LEAD_MAGNET_URL` (https://hackeatuvida.netlify.app/).
  - El link lleva `utm_source=landing-clase`, `utm_medium=etapa-c`, `utm_campaign=<UTM_CLASE>` y el `utm_content` del anuncio si vino con uno.
  - El pixel manda un evento personalizado `EtapaC`, solo para contar cuántos C trae cada anuncio en Meta. No se optimiza por él.
  - Como la C ya no completa el form de Comunidad, esos contactos no entran a GHL desde esta landing. Si se quieren medir ahí, hay que volver a poner el form de Comunidad y cambiar su redirección en GHL al lead magnet.

## Probado

Con Chromium headless, en celular (390 px) y escritorio (1366 px): sin scroll horizontal ni errores de JS.
- La fecha se arma desde `CONFIG`.
- La etapa C ve el mensaje y el link con UTMs.
- La etapa A llega al form principal con `etapa=A&equipo=A&califica=si&nivel=alto&dedicacion=…`.
