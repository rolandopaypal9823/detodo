# Implementación NFM

Cómo se maqueta y se conecta una landing de NFM. Restricciones reales de las plataformas que se usan hoy.

## Índice
- [Sistema visual](#sistema-visual)
- [Mobile](#mobile)
- [Circle (páginas del ecosistema)](#circle)
- [Shopify (checkout)](#shopify)
- [Entradas / eventos](#entradas)
- [Entrega de código](#entrega-codigo)

<a id="sistema-visual"></a>
## Sistema visual

Paleta y tipografías vienen de `nfm-super-skill/references/03_manual_de_marca.md` y no se negocian:

```css
--nfm-azul:      #0c3452;   /* fondos institucionales, texto principal */
--nfm-naranja:   #ff6602;   /* CTAs y solo CTAs */
--nfm-blanco:    #ffffff;
```

- Titulares: **Montserrat Bold**. Cuerpo: **Open Sans Regular**.
- **El naranja es exclusivo de la acción.** Si se usa como decoración en tres lugares, el botón deja de destacar y la página pierde su jerarquía.
- Toda landing lleva el logo: navy sobre fondo claro, blanco sobre fondo oscuro. En HTML autocontenido va embebido como data URI, nunca como link externo.

### Tratamiento "azul elegante"

Para secciones de fondo oscuro, en vez de un azul plano se usa la capa compuesta ya validada en la landing de gira:

```css
.navy-elegante{
  position:relative;
  background:
    radial-gradient(120% 90% at 18% 12%, rgba(23,70,109,.6), transparent 55%),
    radial-gradient(90% 80% at 88% 106%, rgba(255,102,2,.07), transparent 60%),
    linear-gradient(180deg, #0e3352 0%, #0c3452 45%, #061d30 100%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06);
}
```

Complementos del mismo sistema:
- **Capa neuronal**: un `<canvas>` en `position:absolute; inset:0; z-index:0; pointer-events:none`, con nodos y líneas por proximidad, enmascarado con `mask-image: radial-gradient(78% 68% at 50% 42%, #000 20%, transparent 80%)` para que se desvanezca en los bordes. Respetar `prefers-reduced-motion` y pausar en `visibilitychange`.
- **Paneles glass**: `rgba(255,255,255,.04)` de fondo, borde `rgba(255,255,255,.12)`, `backdrop-filter: blur(8px)` (con prefijo `-webkit-`).
- **Ring de luz en imágenes**: `box-shadow: 0 40px 100px rgba(0,0,0,.5), 0 0 0 1px rgba(255,255,255,.10)`. Cuidado: si una media query pisa `box-shadow`, hay que repetir el ring adentro.

Orden de CSS: el bloque de fondos va **después** de las reglas de sección que sobrescribe y **antes** de las media queries, o gana la regla equivocada.

<a id="mobile"></a>
## Mobile

- Breakpoints usados: 520px y 900px.
- Above the fold tiene que cerrar en 640px de alto **con el botón adentro**. Si no entra, se recorta el subheadline, no el botón.
- Botones: ancho completo, alto mínimo 52px, texto que no se parta en dos líneas.
- `background-attachment: fixed` **se rompe en páginas largas y en iOS**. Para un fondo fijo, usar un pseudo-elemento:
  ```css
  body::before{ content:''; position:fixed; inset:0; z-index:-1; background: /* gradientes */; }
  ```
- Tipografía mínima de cuerpo: 16px. Menos que eso, iOS hace zoom en los inputs.

<a id="circle"></a>
## Circle (páginas del ecosistema)

La landing del libro vive en Circle, que es una SPA de React. Esto cambia las reglas:

- **No hay HTML exportable.** Para auditar hace falta screenshots del scroll completo o el texto pegado.
- **Los CTA se renderizan después de la carga** y Circle les engancha sus propios handlers. Un `addEventListener` sobre el botón al cargar la página no encuentra nada.
- La forma que funciona es un **listener delegado en `document`, en fase de captura**, que identifica el botón por atributo, texto o href, y le gana al handler de Circle:

  ```js
  document.addEventListener("click", e => {
    const el = e.target.closest && e.target.closest("a,button,[role='button']");
    if (!el || contenedorPropio.contains(el)) return;
    const txt  = (el.textContent || "").trim().toLowerCase();
    const href = (el.getAttribute("href") || "").toLowerCase();
    const esCompra = el.hasAttribute("data-comprar")
      || TEXTOS.some(t => txt.includes(t))
      || HREFS.some(h => href.includes(h));
    if (!esCompra) return;
    e.preventDefault();
    e.stopPropagation();
    abrir();
  }, true);
  ```

- **Guarda de doble init obligatoria** (`if (window.__flag) return;`) — Circle puede re-ejecutar el snippet al navegar entre páginas.
- **Aislar estilos.** La página host tiene `text-align:center` y line-heights propios que se filtran. Todo módulo inyectado declara su propio `box-sizing`, `text-align` y `line-height`, y usa nombres de clase prefijados (`.sel-pack`, no `.pack`).
- Insertar código requiere plan Plus o superior. Si el plan no lo permite, el fallback es alojar el módulo como página independiente y apuntar los botones ahí.

<a id="shopify"></a>
## Shopify (checkout)

- **Cart permalink** para armar un carrito pre-cargado sin desarrollo:
  ```
  https://TIENDA.myshopify.com/cart/VARIANT_ID:1,VARIANT_ID:1?utm_source=...&utm_content=pack1
  ```
  Soporta mezclar producto físico y digital en el mismo carrito. Funciona hoy, sin depender de nadie.
- **Los IDs de variante y los precios van en un único bloque de configuración** arriba del código, comentados con el nombre del producto. Nunca dispersos en el HTML.
- **Un "pack" solo existe si hay un descuento automático con requisito de combo.** Si el descuento del producto no tiene mínimo, comprar suelto cuesta exactamente lo mismo y el pack es solo una palabra. Verificar en `automaticDiscountNodes` antes de comunicar un ahorro.
- **Antes de prometer envío internacional**, revisar `deliveryProfiles`: si la única zona configurada es AR, el camino "fuera del país" tiene que terminar en producto digital, no en un checkout que va a fallar.
- **Producto físico con `inventoryPolicy: DENY`**: el link se rompe cuando el stock llega a cero. Si la landing se va a pautar, hay que prever el estado agotado.
- **Digitales**: verificar `inventoryItem.requiresShipping: false`. Si el checkout igual pide dirección, el motivo suele ser el requisito de **dirección de facturación**, que es una configuración del checkout/gateway y no del producto.
- El costo de envío se comunica en la landing. Sorpresa en el checkout = abandono.

<a id="entradas"></a>
## Entradas / eventos

- Cada función es un link propio de la ticketera, con UTM por función (`utm_content=ciudad`).
- Funciones sin link se muestran con estado explícito ("PRÓXIMAMENTE"), en un estilo visualmente apagado respecto de las activas.
- **Las fechas, salas y horarios nunca se infieren.** Se confirman con el usuario o se dejan como "sala a confirmar".
- Barra sticky inferior en mobile con el CTA, a partir del primer scroll.

<a id="entrega-codigo"></a>
## Entrega de código

Preferencia declarada del usuario: **el código completo pegado en el chat, listo para copiar y pegar**, además del archivo. No entregar solo el path del archivo cuando lo que se pidió es el código.

- Un solo archivo HTML autocontenido (CSS y JS inline, imágenes embebidas) salvo que se pida lo contrario.
- Comentarios en castellano, explicando los valores que después hay que cambiar (IDs, precios, links).
- Si algo no se pudo verificar porque un dominio está bloqueado por el proxy (ticketera, tienda), **decirlo explícitamente en vez de completar con datos supuestos.**
