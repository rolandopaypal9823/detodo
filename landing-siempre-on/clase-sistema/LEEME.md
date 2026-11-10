# Landing "Un sistema que lo sostenga"

Landing de registro a la clase en vivo, apuntada al perfil Platinum (profesionales y empresarios con equipo). El copy sale de las llamadas de venta del 22/09, 04/11 y octubre. Ver `../HANDOFF-landing-filtro-platinum.md` y `../COPY-landing-sistema-que-lo-sostenga.md`.

| Archivo | Qué es |
|---|---|
| `index-popup.html` | Landing con el quiz y el form en un popup. Cualquier botón lo abre; se cierra sólo con la X. |

Se pega en GHL igual que las anteriores: lo que está entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ» va en el bloque de custom code. El pixel de Meta va adentro con la guarda para no contar dos PageView.

## Antes de publicar

1. **Fecha:** lunes 16 de noviembre, 19:00 hs (Argentina) — `FECHA: '2026-11-16'` en el `CONFIG` del final. La píldora, el contador, la hora local y todos los textos con fecha se arman solos desde ahí.
2. **`UTM_CLASE`:** `clase-nov16-sistema`. Va en `edicion` y en el `utm_campaign` de los leads sin UTM.
3. **Thank you de registro:** `nfm-clase-paga/thankyou-registro-sin-popup.html` (sin el popup de asientos USD 5 / USD 9). Ya tiene la clase del lunes 16 y el grupo nuevo (https://go.wha.link/b2DPze). Es la que va en la redirección del "Form AGOSTO NUEVO".
   - Sale de `thankyou-oto.html`, que también quedó en el 16/11 por si se vuelve a usar el popup de asientos. Si se toca esa, regenerar con `python3 nfm-clase-paga/gen-thankyou-sin-popup.py` desde la raíz del repo.

## Lo demás de la clase del 16/11

| Pieza | Archivo |
|---|---|
| Calendario | `calendario-clase-16-nov.md` (link de Google Calendar) y `calendario-clase-16-nov.ics` (iPhone/Outlook). Llevan la puerta al Zoom y el grupo nuevo. |
| QR para la clase | `qr/qr-calendly-clase1611.{png,svg}` y `-negro.png`: Calendly con `utm_source=clase1611` (mismo Calendly que el 04/11). |
| Puerta al Zoom | `zoom-nfm.netlify.app`: actualizar el link de Zoom y la clave anti-duplicados para esta clase. |

## Qué cambió respecto de la del 04/11

- **Hero:** fondo blanco y texto en azul. La foto de Nico pasa abajo del botón.
  - Arriba: "Para profesionales y empresarios que sienten que todo pasa por ellos".
  - Título: "Dejá de sobrecargarte con todo y armá un sistema de neurociencia que lo sostenga".
  - Debajo: "Neurociencia para el Alto Rendimiento Profesional · con Nico Fernández Miranda".
- **"¿Te reconocés?"** (bloque naranja): reemplaza "Lo que este evento desarma". Tiene 14 situaciones de quien tiene equipo, clientes o negocio, sacadas de frases de compradores Gold y Platinum.
- **"Qué dice la neurociencia":** la creencia central. Tu cerebro está decidiendo por todo tu equipo, y el sistema no se arma con el mismo cerebro saturado que lo necesita.
- **Historia de Nico:** igual. Solo cambia el último párrafo de "Hoy".
- **Qué vas a aprender:** temas nuevos (imprescindible, soltar sin que se caiga nada, cortar a tiempo, dormir de corrido, concentración con equipo, recuperación, la variable). Sale el de IA. Fondo naranja suave.
- **Casos:** los mismos, en el único bloque azul. El cierre responde al miedo a que se caiga lo construido.
- **Bloque nuevo "Para quién es esta clase":** es y no es para vos, sin hablar de plata, más la línea de seriedad.
- **Cierre:** "Si no es ahora, ¿cuándo?". Bloque naranja con botón azul.
- **Contador:** barra naranja con los números en blanco.

## Quiz

- **Pregunta de etapa:** sin cambios, mismas palabras.
- **Etapa A y B:** igual que antes. Pregunta del equipo, "a qué te dedicás" y el form principal ("Form AGOSTO NUEVO"), con etapa, equipo, nivel y dedicación en la URL.
- **Etapa C:** no ve form ni clase. Al tocar "Continuar" aparece un mensaje y el botón "Quiero el regalo de Nico", que va a `CONFIG.LEAD_MAGNET_URL` (https://hackeatuvida.netlify.app/).
  - El link lleva `utm_source=landing-clase`, `utm_medium=etapa-c`, `utm_campaign=<UTM_CLASE>` y el `utm_content` del anuncio si vino con uno.
  - Además, el pixel manda un evento personalizado `EtapaC`, solo para contar cuántos C trae cada anuncio en Meta. No se optimiza por él.
  - Como la C ya no completa el form de Comunidad, esos contactos no entran a GHL desde esta landing. Si se quieren medir ahí, hay que volver a poner el form de Comunidad y cambiar su redirección en GHL al lead magnet.

## Probado

Con Chromium headless, en celular (390 px) y escritorio (1366 px): sin scroll horizontal ni errores de JS.
- La fecha se arma desde `CONFIG`.
- La etapa C ve el mensaje y el link con UTMs.
- La etapa A llega al form principal con `etapa=A&equipo=A&califica=si&nivel=alto&dedicacion=…`.
