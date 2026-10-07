# Landing de registro · clase del miércoles 14 de octubre · 19:00 hs (Argentina)

`index.html` es la landing del 7 de octubre (`landing-siempre-on/clase-7-octubre/index.html`, rama
`claude/nueva-landing-form-7ajo0h`) con dos cambios:

1. **Fecha y UTM:** `2026-10-14`, todos los textos que decían «miércoles 7» y `clase-oct14-alto-rendimiento`
   (va en el `utm_campaign` de los leads sin UTM, en `edicion` y en `clase_fecha` del form).
2. **Tráiler de autoridad (Loom)** arriba del quiz y del form, del mismo ancho que la tarjeta del quiz.
   El botón «QUIERO MI LUGAR» del hero baja justo ahí: primero el video y abajo el quiz.

## El video de Loom

El embed lleva `hideEmbedTopBar`, `hide_owner`, `hide_share`, `hide_title` y `hide_speed`. Con eso desaparecen
la barra de arriba (título, autor, compartir, que es donde Loom muestra las vistas) y el cartel de velocidad.
Queda sólo el botón de reproducir. Es un clic, en compu y en celular.

**La velocidad 1x no se puede fijar desde la página.** Loom reproduce todo a 1,2x por defecto. Se cambia en el
video: Loom → el video → **Settings → Audience → velocidad 1x**. El que mira puede cambiarla igual desde los
controles del reproductor.

## En GHL

Igual que la del 7: el bloque entre «DESDE ACÁ EMPIEZA» y «HASTA ACÁ» va en el custom code; el pixel va en
Settings → Tracking Code → HEAD (ya está puesto, es el mismo).
