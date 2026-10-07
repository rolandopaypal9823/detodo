# Landing de registro · clase del miércoles 14 de octubre · 19:00 hs (Argentina)

Dos variantes, las mismas del 7 (`landing-siempre-on/clase-7-octubre/`, rama `claude/nueva-landing-form-7ajo0h`):

| Archivo | Cómo se registra la gente |
|---|---|
| `index-popup.html` | **Con popup.** Cualquier botón (hero, bullets, cierre, barra fija) abre el quiz y el form en un popup. Se cierra sólo con la X. |
| `index.html` | Con el quiz y el form en la página. Los botones bajan hasta ahí. |

Cambios respecto de la del 7, iguales en las dos:

1. **Fecha y UTM:** `2026-10-14`, todos los textos que decían «miércoles 7» y `clase-oct14-alto-rendimiento`
   (va en el `utm_campaign` de los leads sin UTM, en `edicion` y en `clase_fecha` del form).
2. **Tráiler de autoridad (Loom)** debajo de la cinta «Su trabajo fue destacado en». El video son los
   conductores de TV presentando a Nico, sus credenciales, el libro, el TEDx y testimonios: es la cinta de
   logos en video, así que va pegado a ella. No va pegado al form: dura 4:30 y el que ya tocó «QUIERO MI
   LUGAR» tiene que llegar directo al quiz.
3. **En la variante con popup**, si alguien puso el video y después abre el registro, el video se corta para
   que el audio no siga sonando detrás del quiz.

## El video de Loom

El embed lleva `hideEmbedTopBar`, `hide_owner`, `hide_share`, `hide_title` y `hide_speed`. Con eso desaparecen
la barra de arriba (título, autor, compartir, que es donde Loom muestra las vistas) y el cartel de velocidad.
Queda sólo el botón de reproducir. Es un clic, en compu y en celular.

**La velocidad 1x no se puede fijar desde la página.** Loom reproduce todo a 1,2x por defecto. Se cambia en el
video: Loom → el video → **Settings → Audience → velocidad 1x**. El que mira puede cambiarla igual desde los
controles del reproductor.

**Subtítulos:** la transcripción automática de Loom tiene errores («Jakea tu cerebro», «Cáqueda tu cerebro»,
«Me quiero matar»). Si los subtítulos se muestran, se ven. Corregila en Loom (pestaña Transcript) o dejá los
subtítulos apagados.

## En GHL

Igual que la del 7: el bloque entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ» va en el custom code; el pixel va en
Settings → Tracking Code → HEAD (ya está puesto, es el mismo).
