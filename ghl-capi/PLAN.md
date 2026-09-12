# Meta CAPI en GHL: plan de ejecucion (reemplazo de Hyros)

Objetivo: que Meta reciba Lead, CompleteRegistration, AsistioClase, Schedule y Purchase
del mismo contacto, con el fbclid del click original, para optimizar por agenda/asistencia.

## Paso 1: custom fields (Settings > Custom Fields)  ~3 min
Crear 3 campos de contacto, tipo texto: `fbclid`, `fbc`, `fbp`.

## Paso 2: hidden fields en el form del webinar  ~3 min
En el editor del form, agregar 3 campos ocultos mapeados a esos custom fields.
Las keys tienen que ser exactamente `fbclid`, `fbc`, `fbp` (se autocompletan desde la URL).

## Paso 3: header tracking code  ~2 min
Funnel > Settings > Tracking Code > Header: pegar `header-tracking-fbclid.html`
DESPUES del Pixel de Meta. Guardar y publicar.

## Paso 4: workflows (uno por trigger, sin "wait")  ~20 min
Accion en todos: "Meta conversion API" > Integration > Funnel Event.
Access Token y Dataset ID: los mismos en todos. Custom Mapping ON.
FBCLID -> etiqueta > Contact > `fbclid`  (el custom field del paso 1).

| Workflow | Trigger | Facebook Event Name | Value |
|---|---|---|---|
| CAPI Lead | Form Submitted (form webinar) | Lead | vacio |
| CAPI Registro | mismo form o tag "registrado" | CompleteRegistration | vacio |
| CAPI Asistio | tag "asistio" (lo pone la plataforma del webinar) | AsistioClase (custom) | vacio |
| CAPI Agenda | Appointment booked (GHL) o webhook Calendly | Schedule | vacio |
| CAPI Venta | Opportunity -> Won (o webhook Airtable) | Purchase | monto real + moneda |

Se manda SIEMPRE, haya o no fbclid. GHL toma email y telefono del contacto y los hashea.

## Paso 5: prueba  ~10 min
1. Events Manager > Test Events > copiar el codigo TEST.
2. Pegarlo en "Test Code" de la accion CAPI Lead. Guardar.
3. Abrir la landing como `https://tu-landing.com/?fbclid=TEST_abc123`.
4. Enviar el form con un mail nuevo.
5. Abrir el contacto: los 3 custom fields tienen que tener valor.
6. En Test Events tiene que aparecer Lead con `fbc` presente.
7. Borrar el Test Code y guardar de nuevo.
Repetir 2-7 con una prueba real clickeando un anuncio desde el celular (Instagram in-app).

## Paso 6: Ads Manager (recien con 1-2 lanzamientos de datos)
Cambiar el evento de optimizacion del conjunto de anuncios de Lead a AsistioClase
(o Schedule si el volumen semanal lo aguanta, ~50/semana por conjunto).
Purchase se manda para reportes, pero no se optimiza por Purchase: la mayoria de
las compras cierran fuera de la ventana de 7 dias click.
