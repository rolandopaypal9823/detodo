# Versiones fijas, una por clase

Cada carpeta tiene la landing y la thank you page **clavadas a una sola clase**. No rotan, no calculan
nada, no dependen de ninguna fecha: muestran siempre esa clase y ese grupo de WhatsApp, pase lo que pase.

| Carpeta | Clase | Tema | Título | Grupo de WhatsApp |
|---|---|---|---|---|
| `clase-15-septiembre/` | mar 15 sep, 19:00 | B | Escalá tu vida, no tu cansancio | `clase-15-de-septiembre-de-neurociencia` |
| `clase-22-septiembre/` | mar 22 sep, 19:00 | A | Cumplís con todos menos con vos | `clase-22-de-semptiembre-de-neurociencia` |

En cada carpeta: `index.html` va en la landing de registro, `thank-you.html` en la página de gracias.
Copiás de marcador a marcador, reemplazando el bloque entero.

---

## Cuándo pegar cada una

Son las mismas fechas de arranque de captación que ya habíamos definido:

- **Ya pegada** (desde el 2 de septiembre): la del **15**.
- **11 de septiembre, 00:00** → pegás la del **22**.
- **20 de septiembre, 00:00** → pegás la de octubre (falta definirla).

---

## Qué se probó

Las dos versiones se abrieron con el reloj puesto en cuatro momentos distintos —hoy, 5 de septiembre,
18 de septiembre y 30 de noviembre— y **en los cuatro muestran exactamente lo mismo**: misma fecha,
mismo tema, misma campaña, mismo grupo. No hay forma de que roten solas.

También verificado en las cuatro: sólo `PageView` en el pixel, ningún evento de conversión, y ningún
placeholder crudo en pantalla.

---

## Lo único a tener en cuenta

**Después de que pasa la clase, el contador queda en cero** y aparece el cartel de "la clase está
empezando ahora". Es esperable: la página está clavada a esa fecha y no sabe que hay una siguiente.
Por eso hay que reemplazarla en la fecha que corresponde. Si algún martes se te pasa, lo peor que
puede pasar es que muestre una clase vencida — nunca una fecha inventada.

**El título y la descripción del preview** (lo que se ve cuando alguien comparte el link por WhatsApp)
salen de GoHighLevel, no de estos archivos. Están puestos genéricos a propósito para que no queden
viejos entre clase y clase.

---

## La versión que rota sola sigue existiendo

`../index.html` y `../thank-you.html` son la versión con las tres clases cargadas, que cambia sola en
las fechas de captación. Si algún día preferís volver a esa, están ahí y funcionan. Estas versiones
fijas son para cuando querés control manual total y cero sorpresas.
