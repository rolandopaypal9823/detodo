# HANDOFF — Landing "Hackea tu vida" (13 QR)

> Documento de traspaso. Esta pensado para pegarse entero en un chat nuevo de
> Claude que no tenga nada de contexto previo. Al final esta el codigo completo
> y funcionando de la landing.

---

## 1. Que es esto

Nicolas Fernandez Miranda (NFM) publica un libro llamado **"Hackea tu vida"**.
A lo largo del libro hay **13 codigos QR impresos**, numerados del 1 al 13.

Cuando un lector escanea cualquiera de esos QR, va a parar **siempre a la misma
pagina web**, pero el contenido que ve **cambia por completo** segun el numero
del QR. Son, en la practica, 13 paginas dentro de una sola.

El mecanismo es un parametro en la URL:

```
https://nicolasfernandezmiranda.com/HTV/          -> pagina general del libro
https://nicolasfernandezmiranda.com/HTV/?qr=1     -> contenido del QR 1
https://nicolasfernandezmiranda.com/HTV/?qr=7     -> contenido del QR 7
https://nicolasfernandezmiranda.com/HTV/?qr=13    -> contenido del QR 13
```

Si el parametro falta, no es un numero, o se va del rango 1-13, se muestra la
pagina general. Los 13 QR ya estan generados e impresos apuntando a esas URLs
exactas: **las URLs no se pueden cambiar** sin volver a generar los codigos.

## 2. Estado actual

- La landing esta **montada en WordPress con Elementor**, dentro de un widget HTML.
- Los 13 QR estan **generados y verificados**.
- **Los 13 contenidos estan vacios**: todos muestran el recuadro "Contenido
  disponible proximamente". Cargarlos es, casi siempre, la razon por la que
  alguien esta leyendo este documento.

## 3. Donde vive el codigo

Repositorio `rolandopaypal9823/detodo`, rama `claude/landing-qr-variants-nc7tc1`,
carpeta `landing/`:

| Archivo | Que es |
|---|---|
| `elementor.html` | **El archivo que esta en produccion.** Es el que se pega en el widget HTML de Elementor. Editar aca. |
| `index.html` | La misma landing como archivo suelto (hosting estatico / pruebas locales). Tiene el mismo bloque `CONTENIDOS`, pero **no es el que esta publicado**. |
| `codigos.html` | Arma los 13 enlaces a partir del dominio, para el generador de QR. |
| `qr/negro/`, `qr/azul-nfm/` | Los 13 QR en SVG y PNG. |
| `qr/hoja-de-control.html` | Hoja imprimible con los 13 codigos y su enlace. |

Si no tenes acceso al repo, el codigo completo esta en la seccion 7 de este
documento.

---

## 4. COMO EDITAR LOS 13 CONTENIDOS

Esto es lo importante. Todo el contenido vive en un objeto JavaScript llamado
`CONTENIDOS`, adentro del `<script>` de `elementor.html`.

### 4.1. Como arranca

Un bucle crea las 13 entradas con valores de relleno y estado `"proximamente"`:

```js
var CONTENIDOS = {};
for (var i = 1; i <= TOTAL_QR; i++) {
  CONTENIDOS[i] = {
    etiqueta: "QR " + (i < 10 ? "0" + i : i),
    titulo:   "Contenido del QR " + i,
    bajada:   ["Llegaste desde el QR numero " + i + " de " + LIBRO + "..."],
    estado:   "proximamente",
    bloques:  [],
    cta:      null
  };
}
```

### 4.2. Como se publica uno

**No hay que tocar ese bucle.** Se agrega una asignacion despues, en el lugar
marcado con el comentario `A PARTIR DE ACA SE EDITA CADA QR`. Esa asignacion
pisa por completo la entrada del bucle:

```js
CONTENIDOS[1] = {
  etiqueta: "QR 01 - CAPITULO 1",
  titulo:   "El verdadero costo de tu atencion",
  bajada:   [
    "Primer parrafo de la bajada.",
    "Segundo parrafo, opcional."
  ],
  estado:   "publicado",
  bloques:  [
    { titulo: "Video", texto: "Descripcion de lo que va a encontrar." },
    { titulo: "Ejercicio", texto: "Descripcion del ejercicio." }
  ],
  cta: { texto: "Ver el material", url: "https://..." }
};
```

### 4.3. Que hace cada campo

| Campo | Tipo | Que hace |
|---|---|---|
| `etiqueta` | texto | La pildora naranja arriba del titulo. Se muestra en mayusculas. |
| `titulo` | texto | El titulo grande de la pagina. |
| `bajada` | array de textos | Un parrafo por elemento. Puede ser `[]`. |
| `estado` | `"proximamente"` o `"publicado"` | Es el interruptor. Ver abajo. |
| `bloques` | array de `{titulo, texto}` | Tarjetas debajo de la bajada. **Solo se muestran si `estado` es `"publicado"`.** |
| `cta` | `{texto, url}` o `null` | Boton naranja. **Solo se muestra si `estado` es `"publicado"`** y tiene `url`. |

### 4.4. El interruptor `estado`

- `"proximamente"` → se muestra el recuadro azul "Contenido disponible
  proximamente" a la derecha. Se ignoran `bloques` y `cta`.
- `"publicado"` → **desaparece** el recuadro y se muestran los `bloques` y el
  boton `cta`.

Es decir: se pueden cargar los 13 contenidos con `estado: "proximamente"` y
publicarlos despues, de a uno, cambiando una sola palabra.

### 4.5. Reglas al editar

- Es JavaScript, no HTML. **Todo texto va entre comillas** y las entradas del
  objeto se separan con comas.
- Los textos se insertan con `textContent`, no con `innerHTML`: **no se pueden
  meter etiquetas HTML** dentro de `titulo`, `texto` ni `bajada`. Si aparecen,
  se van a ver como texto literal. Es a proposito: evita que un contenido mal
  pegado rompa la pagina.
- Se pueden usar tildes y enies sin problema (el archivo es UTF-8).
- Si se rompe la sintaxis, **la pagina queda en blanco**. Ante la duda, mirar la
  consola del navegador.
- Despues de editar `elementor.html`, hay que **volver a pegar el archivo
  entero** en el widget HTML de Elementor y publicar. No alcanza con guardar en
  el repo.

### 4.6. Como probar sin publicar

Abrir `index.html` en el navegador agregando el parametro a mano:
`file:///.../index.html?qr=5`. Ojo: `index.html` es una copia; el cambio real
va en `elementor.html`.

---

## 5. Decisiones ya tomadas (no deshacer sin motivo)

**Por que hay dos archivos y por que no se pega `index.html` en Elementor.**
`index.html` es un documento completo, con `<html>`, `<head>` y `<body>`.
WordPress descarta esas etiquetas pero conserva el CSS, asi que la regla
`body{background:azul; color:blanco}` no llega a pintar el fondo (el tema ya
tiene el suyo, blanco) pero si deja el texto en blanco: **texto blanco sobre
fondo blanco**, y ademas se desconfigura el resto del sitio. Ya paso.
`elementor.html` es un fragmento sin esas etiquetas y con **todo el CSS
encapsulado en `#htv-app`**, por lo que no puede tocar ningun estilo del sitio.

**Ancho completo.** El bloque se estira a todo el ancho de la pantalla aunque el
contenedor de Elementor sea angosto (`left:50%; margin-left:-50vw; width:100vw`).
Verificado que no genera scroll horizontal. Si no se quiere, se borran las 5
lineas marcadas `ANCHO COMPLETO`.

**El logo.** Sale de `https://nicolasfernandezmiranda.com/wp-content/uploads/2026/01/nuevo-logo-nfm-1.png`.
El tamano se controla con la variable `--htv-logo-alto` (230px en escritorio,
150px en tablet, 110px en movil): es el unico numero a tocar. Si el archivo
fuera la version oscura del logo, sobre el fondo azul no se veria; para eso hay
una regla comentada `filter:brightness(0) invert(1)` que lo fuerza a blanco.
Si el logo no carga, aparece un wordmark "NFM" de respaldo.

**Los QR.** Generados con la libreria `segno`, **correccion de errores nivel Q**
(33x33 modulos). Se eligio Q sobre H a proposito: con H salian de 41x41, un 20%
mas densos, lo que complica el escaneo impreso chico. Nivel Q tolera 25% de
superficie tapada, de sobra para papel. Tamano minimo impreso: 2 cm, recomendado
2,5-3 cm. Para imprenta se usan los SVG.

Si cambia el dominio o la ruta, **hay que regenerar los 13 QR**:

```bash
pip install segno
python3 -c "
import segno
for i in range(1,14):
    q = segno.make(f'https://nicolasfernandezmiranda.com/HTV/?qr={i}', error='q')
    q.save(f'qr/negro/qr-{i:02d}.svg', scale=10, border=4)
"
```

---

## 6. Marca NFM (para no inventar estilos)

Instituto de Productividad de Nicolas Fernandez Miranda. Estetica **clinica,
autoritaria y limpia**: mucho aire, jerarquia fuerte, cero adorno.

**Colores** (ya estan como variables CSS en el codigo):

```
--htv-blue:       #0c3452   Azul NFM: estructura, contenedores, autoridad
--htv-blue-dark:  #061d30   Fondo de la landing
--htv-blue-light: #e7edf2   Texto secundario sobre azul
--htv-orange:     #ff6602   Naranja Accion: CTAs, hitos, EL climax
```

Regla del naranja: **es escaso por diseno**. Marca el CTA y el dato que importa.
Si todo es naranja, nada es naranja.

**Tipografias:** Montserrat (titulos, 900 para los grandes), Open Sans (cuerpo),
JetBrains Mono (etiquetas en mayusculas con `letter-spacing` ancho — es la firma
visual de la marca). **Prohibidas:** Inter, Roboto, Arial, Helvetica, system-ui.

**Voz del copy:** rioplatense informal (vos), directo, sin guiones largos. NFM no
usa emojis en piezas seria.

**Titulo del libro:** es **"Hackea tu vida"** (confirmado). Vive en la constante
`LIBRO`, arriba del script, y de ahi se propaga a la cabecera, el pie y el
`<title>`: se cambia en un solo lugar. No afecta a los QR, porque las URLs solo
llevan el numero.

---

## 7. CODIGO COMPLETO (`elementor.html`)

Esto es lo que esta en produccion, pegado en un widget HTML de Elementor.

```html
<!--
  =========================================================================
  HACKEA TU VIDA - LANDING DE 13 QR  ::  VERSION PARA ELEMENTOR
  -------------------------------------------------------------------------
  Pega TODO este bloque dentro de un widget "HTML" de Elementor.
  Reemplaza por completo lo que haya adentro del widget.

  No lleva <html>, <head> ni <body>: dentro de una pagina de WordPress esas
  etiquetas se descartan y el CSS del body termina pintando el sitio entero.
  Aca todo el CSS esta encerrado en #htv-app, asi que no toca nada del resto
  de la pagina.

  El bloque se estira solo a todo el ancho de la pantalla, aunque el
  contenedor de Elementor sea angosto. Si NO lo queres a todo el ancho,
  borra las 5 lineas marcadas con "ANCHO COMPLETO" mas abajo.

  Para que se vea limpio, en Elementor conviene:
    - Contenedor: ancho "Completo", sin padding.
    - Pagina: layout "Lienzo de Elementor" o "Ancho completo".
  =========================================================================
-->

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Open+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

#htv-app{
  /* ---- ANCHO COMPLETO (borra estas 5 lineas si no lo queres) ---- */
  position:relative;
  left:50%;
  margin-left:-50vw;
  width:100vw;
  max-width:100vw;
  /* --------------------------------------------------------------- */

  /* Tamano del logo. Es el unico numero que hay que tocar para agrandarlo
     o achicarlo. Estaba en 46px; ahora esta 5 veces mas grande. */
  --htv-logo-alto:230px;

  --htv-blue:#0c3452;
  --htv-blue-dark:#061d30;
  --htv-blue-light:#e7edf2;
  --htv-orange:#ff6602;
  --htv-line:rgba(231,237,242,0.18);

  background:var(--htv-blue-dark);
  color:#ffffff;
  font-family:'Open Sans',sans-serif;
  font-size:16px;
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
  min-height:88vh;
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
#htv-app *,#htv-app *::before,#htv-app *::after{box-sizing:border-box;}

/* ---------- Cabecera / logo ---------- */
#htv-app .htv-top{
  padding:28px 40px;
  border-bottom:1px solid var(--htv-line);
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  flex-wrap:wrap;
}
#htv-app .htv-logo img{
  display:block;
  height:var(--htv-logo-alto);
  width:auto;
  max-width:min(80vw,900px);
  object-fit:contain;
  margin:0;
}

/* Si el logo se ve oscuro o directamente no se ve sobre el fondo azul,
   activa la linea de abajo quitandole el comentario: fuerza el logo a blanco puro. */
/* #htv-app .htv-logo img{filter:brightness(0) invert(1);} */
#htv-app .htv-wordmark{
  font-family:'Montserrat',sans-serif;
  font-weight:900;
  font-size:22px;
  letter-spacing:0.02em;
  line-height:1;
  color:#ffffff;
}
#htv-app .htv-wordmark span{
  display:block;
  font-family:'JetBrains Mono',monospace;
  font-weight:400;
  font-size:9px;
  letter-spacing:0.3em;
  text-transform:uppercase;
  color:var(--htv-blue-light);
  opacity:.7;
  margin-top:7px;
}
#htv-app .htv-book{
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  letter-spacing:0.28em;
  text-transform:uppercase;
  color:var(--htv-blue-light);
  opacity:.75;
}

/* ---------- Cuerpo ---------- */
#htv-app .htv-main{
  flex:1;
  width:100%;
  max-width:1180px;
  margin:0 auto;
  padding:80px 40px 96px;
  display:grid;
  grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);
  gap:72px;
  align-items:start;
  align-content:center;
}
#htv-app .htv-tag{
  display:inline-block;
  font-family:'JetBrains Mono',monospace;
  font-weight:700;
  font-size:12px;
  letter-spacing:0.3em;
  text-transform:uppercase;
  color:var(--htv-orange);
  border:2px solid var(--htv-orange);
  border-radius:100px;
  padding:8px 18px;
  margin:0 0 34px;
}
#htv-app h1.htv-h1{
  font-family:'Montserrat',sans-serif;
  font-weight:900;
  font-size:clamp(38px,5.4vw,62px);
  line-height:1.02;
  letter-spacing:-0.015em;
  color:#ffffff;
  margin:0 0 26px;
  padding:0;
  text-wrap:pretty;
}
#htv-app .htv-lead{
  font-size:19px;
  line-height:1.62;
  color:var(--htv-blue-light);
  margin:0;
  max-width:44ch;
  text-wrap:pretty;
}
#htv-app .htv-lead + .htv-lead{margin-top:18px;}

/* ---------- Recuadro proximamente ---------- */
#htv-app .htv-panel{
  background:var(--htv-blue);
  border:2px solid var(--htv-line);
  border-radius:12px;
  padding:48px 44px;
  box-shadow:0 40px 100px rgba(6,29,48,0.55);
}
#htv-app .htv-status{
  font-family:'JetBrains Mono',monospace;
  font-weight:700;
  font-size:11px;
  letter-spacing:0.3em;
  text-transform:uppercase;
  color:var(--htv-orange);
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:22px;
}
#htv-app .htv-status::before{
  content:"";
  width:8px;height:8px;border-radius:50%;
  background:var(--htv-orange);
  flex:none;
}
#htv-app h2.htv-h2{
  font-family:'Montserrat',sans-serif;
  font-weight:800;
  font-size:26px;
  line-height:1.22;
  color:#ffffff;
  margin:0 0 16px;
  padding:0;
  text-wrap:pretty;
}
#htv-app .htv-panel p{
  font-size:16px;
  line-height:1.6;
  color:var(--htv-blue-light);
  margin:0;
  text-wrap:pretty;
}
#htv-app .htv-meta{
  margin-top:32px;
  padding-top:24px;
  border-top:1px solid var(--htv-line);
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  letter-spacing:0.22em;
  text-transform:uppercase;
  color:var(--htv-blue-light);
  opacity:.65;
}

/* ---------- Contenido publicado ---------- */
#htv-app .htv-bloques{margin-top:34px;display:grid;gap:20px;}
#htv-app .htv-bloque{
  background:var(--htv-blue);
  border:2px solid var(--htv-line);
  border-radius:12px;
  padding:26px 28px;
}
#htv-app h3.htv-h3{
  font-family:'Montserrat',sans-serif;
  font-weight:700;
  font-size:17px;
  color:#ffffff;
  margin:0 0 8px;
  padding:0;
}
#htv-app .htv-bloque p{margin:0;font-size:15px;line-height:1.6;color:var(--htv-blue-light);}
#htv-app a.htv-cta{
  display:inline-block;
  margin-top:34px;
  background:var(--htv-orange);
  color:#ffffff;
  font-family:'Montserrat',sans-serif;
  font-weight:800;
  font-size:16px;
  letter-spacing:0.01em;
  text-decoration:none;
  padding:18px 34px;
  border-radius:10px;
  transition:transform .15s ease, box-shadow .15s ease;
}
#htv-app a.htv-cta:hover{transform:translateY(-2px);box-shadow:0 16px 34px rgba(255,102,2,0.32);color:#ffffff;}
#htv-app a.htv-cta[hidden]{display:none;}

/* ---------- Pie ---------- */
#htv-app .htv-footer{
  border-top:1px solid var(--htv-line);
  padding:26px 40px;
  font-family:'JetBrains Mono',monospace;
  font-size:10px;
  letter-spacing:0.26em;
  text-transform:uppercase;
  color:var(--htv-blue-light);
  opacity:.55;
}

@media (max-width:1024px){
  #htv-app{--htv-logo-alto:150px;}
  #htv-app .htv-main{grid-template-columns:1fr;gap:48px;padding:64px 32px 80px;}
}
@media (max-width:767px){
  #htv-app{--htv-logo-alto:110px;}
  #htv-app .htv-main{padding:52px 24px 68px;gap:40px;}
  #htv-app .htv-top{padding:20px 24px;}
  #htv-app .htv-footer{padding:22px 24px;}
  #htv-app .htv-panel{padding:34px 26px;}
  #htv-app .htv-lead{font-size:17px;}
}
</style>

<div id="htv-app">

  <div class="htv-top">
    <div class="htv-logo">
      <img src="https://nicolasfernandezmiranda.com/wp-content/uploads/2026/01/nuevo-logo-nfm-1.png" alt="Nicolas Fernandez Miranda"
           onerror="this.outerHTML='&lt;div class=\'htv-wordmark\'&gt;NFM&lt;span&gt;Nicolas Fernandez Miranda&lt;/span&gt;&lt;/div&gt;'">
    </div>
    <div class="htv-book" id="htv-book"></div>
  </div>

  <div class="htv-main">
    <div>
      <span class="htv-tag" id="htv-tag"></span>
      <h1 class="htv-h1" id="htv-titulo"></h1>
      <div id="htv-bajada"></div>
      <div class="htv-bloques" id="htv-bloques"></div>
      <a class="htv-cta" id="htv-cta" href="#" hidden></a>
    </div>

    <div>
      <div class="htv-panel" id="htv-panel">
        <div class="htv-status" id="htv-panel-status"></div>
        <h2 class="htv-h2" id="htv-panel-titulo"></h2>
        <p id="htv-panel-texto"></p>
        <div class="htv-meta" id="htv-panel-meta"></div>
      </div>
    </div>
  </div>

  <div class="htv-footer" id="htv-footer"></div>

</div>

<script>
/* =========================================================================
   La pagina se arma sola segun el parametro ?qr= de la URL.
       .../HTV/          -> pagina general
       .../HTV/?qr=1     -> contenido del QR 1
       .../HTV/?qr=13    -> contenido del QR 13

   Para cargar el contenido real de un QR, edita su entrada mas abajo:
   mientras "estado" sea "proximamente" se ve el recuadro; cuando lo pases
   a "publicado" se ven titulo, bajada, bloques y boton.
   ========================================================================= */
(function () {
  var LIBRO = "Hackea tu vida";              // titulo del libro
  var AUTOR = "Nicolas Fernandez Miranda";
  var TOTAL_QR = 13;

  var PROXIMAMENTE = {
    status: "Proximamente",
    titulo: "Contenido disponible proximamente",
    texto:  "Estamos terminando de preparar el material de esta seccion del libro. Volve a escanear este mismo QR en unos dias y ya vas a encontrarlo aca."
  };

  /* ---- Los 13 QR ---- */
  var CONTENIDOS = {};
  for (var i = 1; i <= TOTAL_QR; i++) {
    CONTENIDOS[i] = {
      etiqueta: "QR " + (i < 10 ? "0" + i : i),
      titulo:   "Contenido del QR " + i,
      bajada:   ["Llegaste desde el QR numero " + i + " de " + LIBRO + ". Este espacio es el complemento de lo que acabas de leer."],
      estado:   "proximamente",
      bloques:  [],
      cta:      null
    };
  }

  /* ---- A PARTIR DE ACA SE EDITA CADA QR ---------------------------------
     Ejemplo de uno ya publicado (descomentar y completar):

  CONTENIDOS[1] = {
    etiqueta: "QR 01 - CAPITULO 1",
    titulo:   "Titulo del contenido del capitulo 1",
    bajada:   ["Primer parrafo.", "Segundo parrafo."],
    estado:   "publicado",
    bloques:  [
      { titulo: "Video", texto: "Descripcion del video." },
      { titulo: "Ejercicio", texto: "Descripcion del ejercicio." }
    ],
    cta: { texto: "Ver el material", url: "https://..." }
  };
     --------------------------------------------------------------------- */

  /* ---- Pagina general: cuando entran sin ?qr= ---- */
  var HOME = {
    etiqueta: "Libro",
    titulo:   LIBRO,
    bajada:   [
      "Esta es la pagina de contenido complementario del libro. A lo largo de sus paginas vas a encontrar 13 codigos QR: cada uno te trae a este mismo lugar, pero con el material especifico de esa seccion.",
      "Escanea el QR que aparece en el libro para acceder a su contenido."
    ],
    estado:   "proximamente",
    bloques:  [],
    cta:      null
  };

  /* ======================= MOTOR (no hace falta tocar) =================== */
  function $(id){ return document.getElementById(id); }

  var params = new URLSearchParams(window.location.search);
  var n = parseInt(params.get("qr"), 10);
  var esQR = !isNaN(n) && n >= 1 && n <= TOTAL_QR;
  var data = esQR ? CONTENIDOS[n] : HOME;
  var nn = esQR ? (n < 10 ? "0" + n : "" + n) : "";

  $("htv-book").textContent = esQR ? LIBRO + " / QR " + nn : LIBRO;
  $("htv-tag").textContent = data.etiqueta;
  $("htv-titulo").textContent = data.titulo;

  var bajada = $("htv-bajada");
  (data.bajada || []).forEach(function (t) {
    var p = document.createElement("p");
    p.className = "htv-lead";
    p.textContent = t;
    bajada.appendChild(p);
  });

  var publicado = data.estado === "publicado";

  if (publicado) {
    $("htv-panel").parentNode.removeChild($("htv-panel"));

    var cont = $("htv-bloques");
    (data.bloques || []).forEach(function (b) {
      var div = document.createElement("div");
      div.className = "htv-bloque";
      var h = document.createElement("h3");
      h.className = "htv-h3";
      h.textContent = b.titulo;
      var p = document.createElement("p");
      p.textContent = b.texto;
      div.appendChild(h); div.appendChild(p);
      cont.appendChild(div);
    });

    if (data.cta && data.cta.url) {
      var a = $("htv-cta");
      a.textContent = data.cta.texto;
      a.href = data.cta.url;
      a.hidden = false;
    }
  } else {
    var px = data.proximamente || {};
    $("htv-panel-status").textContent = px.status || PROXIMAMENTE.status;
    $("htv-panel-titulo").textContent = px.titulo || PROXIMAMENTE.titulo;
    $("htv-panel-texto").textContent  = px.texto  || PROXIMAMENTE.texto;
    $("htv-panel-meta").textContent   = esQR ? "QR " + nn + " de " + TOTAL_QR : LIBRO;
  }

  $("htv-footer").textContent = LIBRO + " / " + AUTOR;

  if (esQR) { document.title = "QR " + nn + " - " + LIBRO; }
})();
</script>
```

---

## 8. Que pedirle a quien traiga el contenido

Para cargar un QR hace falta, por cada numero del 1 al 13:

1. A que capitulo o seccion del libro corresponde (para la `etiqueta`).
2. El titulo del contenido.
3. Uno o dos parrafos de bajada.
4. Que material hay: video, audio, PDF, ejercicio, plantilla (van como `bloques`).
5. El enlace del CTA, si hay uno, y el texto del boton.

Si de un QR solo hay una parte, se puede cargar igual y dejarlo en
`estado: "proximamente"` hasta que este completo.
