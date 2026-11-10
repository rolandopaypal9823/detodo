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

Mismo azul y mismo sistema visual. Orden de las secciones: hero → logos y tráiler → **¿Para quién está diseñada esta clase?** → historia de Nico (carrusel) → escalera → casos → cierre.

- **Hero:** sin subtítulo.
  - Etiqueta: "Para profesionales y empresarios que sienten que todo pasa por ellos".
  - Título: "Dejá de sobrecargarte con todo y armá un **sistema de neurociencia** que lo sostenga".
  - Debajo: "Neurociencia para el Alto Rendimiento Profesional · con Nico Fernández Miranda".
- **"¿Para quién está diseñada esta clase?"** (segundo bloque, en el lugar del widget de tachados, que se sacó): "Es para vos si…" / "No es para vos si…", sin hablar de plata.
- **Historia de Nico:** "Conocé su historia" · "Nicolás Fernández Miranda, fundador del Instituto de Productividad". Las cinco escenas en carrusel, igual que en la landing de la Comunidad (masterclass del 27/10): foto y texto corto, se deslizan con el dedo o con las flechas.
- **"Armá tu sistema de productividad en vivo el 16 de noviembre":** escalera dibujada con tres peldaños, cada uno con un título y tres o cuatro temas técnicos que se ven en la clase, nombrados sin explicar cómo:
  - **Cuidar tu bienestar mental:** funciones ejecutivas, memoria de trabajo y control inhibitorio, el costo del cambio de tarea, descarga mental.
  - **Cuidar tu bienestar físico:** luz y ritmo circadiano, sueño profundo, recuperación medible.
  - **Las habilidades técnicas que te permiten crecer:** hábitos, concentración profunda, delegación, inteligencia artificial.
  - Los temas salen de lo que los compradores contaron que aprendieron en la clase y de los temarios anteriores. **Conviene confirmar con Nico que el 16/11 los toca.**
  - ⚠️ **La escalera es un dibujo hecho acá, no la imagen original de Nico.** Si hay una imagen oficial, se reemplaza el bloque `.nfm-lad`.
- **Casos:** los mismos, con el título "Profesionales y empresarios que ya pasaron por el Instituto de Productividad" y sin bajada. Cierre "Ninguno vio caerse lo que había construido".
- **Cierre:** "El 16 de noviembre vas a ver cómo dejar de ser el cuello de botella de tu negocio", y debajo "Y volver a disfrutar lo que construiste: tu tiempo libre, tus hobbies, tu familia y unas vacaciones sin el celular".

Se sacaron, por pedido: el widget de tachados ("Más pasa por vos, más alto el precio que pagás"), el bloque naranja "¿Te reconocés?" y el bloque "Tu cerebro está decidiendo por todo tu equipo". Los textos siguen en `../COPY-landing-sistema-que-lo-sostenga.md` por si se quieren volver a usar.

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
