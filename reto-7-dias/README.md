# Reto de 7 Días — Detox Digital (bonus del e-book)

Bonus del paquete del e-book de Desintoxicación Digital, en la voz de **Nico (NFM)**.
La persona elige recibirlo por **email** o por **Instagram (ManyChat)**.

## Archivos

| Archivo | Qué es |
|---|---|
| `emails.md` | **8 mails listos para copiar** al ESP (bienvenida + días 1–7), firmados por Nico. |
| `manychat.md` | **Mensajes cortos de ManyChat** (bienvenida + 7 días): título + mini spoiler + link al día. |
| `sitio/` | **Sitio web del reto** (índice + 7 páginas, una por día). Listo para subir a Netlify. |
| `build_sitio.py` | Generador del sitio. Editar los textos acá y correr `python3 build_sitio.py` para regenerar. |
| `reto-7-dias-concepto.md` | Versión 1 del concepto (borrador inicial, superado por `emails.md`). |

## Deploy del sitio en Netlify

1. Arrastrar la carpeta `sitio/` completa a Netlify (o `netlify deploy --dir=sitio --prod`).
2. Cada día queda en `/dia1`, `/dia2` … `/dia7` (son carpetas con `index.html`, funcionan sin configuración).
3. Poner el dominio definitivo (ej. `retode7dias.netlify.app`) y actualizarlo en `manychat.md`.

## El sitio incluye

- Marca NFM completa: Azul `#0c3452`, Naranja Acción `#ff6602`, Montserrat + Open Sans, logo en header y footer.
- Barra de progreso de los 7 días (con día actual animado) y animaciones de aparición al scrollear.
- **Checklist interactivo** por día: la persona tilda cada paso y queda guardado en su dispositivo (localStorage). Al completar todo aparece un banner de festejo.
- **Día 4:** widget de respiración 4-4-6 guiada (círculo animado con las fases y contador de ciclos).
- **Día 7:** confeti + cartel "FELICITACIONES, completaste el reto" + campo para escribir *"después de estos 7 días, ¿qué cambió / cómo te sentiste / qué lograste?"* (se autoguarda) + invitación a sacar captura y etiquetar a Nico en Instagram.

## El "acompañado" sin humo

En la landing se promete un reto *acompañado*. Para que sea coherente sin inventar contadores falsos ni "1.234 personas online", el acompañamiento se sostiene con tres cosas **reales**:

1. **Nico te escribe todos los días** (email o DM): ese es el acompañamiento principal y es literal.
2. La frase que usamos en todos los mensajes: *"el reto está abierto todo el año y cada semana arranca gente nueva"* — describe cómo funciona el sistema, sin cifras inventadas.
3. La invitación a **subir historias etiquetando a Nico** (día 0, la franja de comunidad del sitio y el día 7) hace visible a la gente que realmente está haciendo el reto — la prueba social se genera sola y es verificable.

## Pendientes antes de lanzar

- [ ] `[LINK]` en `emails.md` y `#LINK-PRODUCTO` en `build_sitio.py` → link real del producto (confirmar destino: ¿libro *Hackea tu Cerebro* o programa Alto Rendimiento?). Regenerar el sitio después de editarlo.
- [ ] Confirmar handle de Instagram (`@nicofernandezmiranda`) en `emails.md`, `manychat.md` y `build_sitio.py`.
- [ ] Dominio definitivo del sitio en `manychat.md`.
- [ ] Palabra clave de ManyChat (sugerida: **RETO**).
- [ ] Hora de envío de los mails (sugerida: 7:30 am hora local).
