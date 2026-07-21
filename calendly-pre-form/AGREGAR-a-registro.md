# Parche para tu página de registro (la de la clase en vivo)

Para que el Calendly se autocomplete **solo** (sin que la persona reescriba nada),
tu página de registro tiene que **guardar los datos en `localStorage`** antes de
redirigir a Zoom. Ya guarda nombre + email; solo falta sumarle el **teléfono** en una
clave que la página `agendar.html` sabe leer.

## Qué agregar (2 líneas)

En tu `index.html` de registro, buscá esta línea (dentro de la función `enviar()`,
~línea 496):

```js
    // marca de registro en este navegador (anti-duplicados)
    try{ localStorage.setItem(REG_KEY, JSON.stringify({ nombre:nombre, email:email, ts:Date.now() })); }catch(e){}
```

**Justo debajo**, pegá esto:

```js
    // guardamos los datos para autocompletar el Calendly (misma web, ej: /agendar)
    try{ localStorage.setItem('nfm_datos', JSON.stringify({ nombre:nombre, email:email, telefono:telFull, ts:Date.now() })); }catch(e){}
```

Listo. Eso es todo. `telFull` ya existe en esa función (es el número en formato
internacional, ej: `+5491123456789`).

> La clave `'nfm_datos'` tiene que ser **la misma** que está en `agendar.html`
> (config `localStorageKey: "nfm_datos"`). Si cambiás una, cambiá la otra.

## Muy importante: mismo sitio de Netlify

Para que `localStorage` se comparta entre las dos páginas, **las dos tienen que estar
en el MISMO sitio de Netlify** (mismo dominio). O sea:

```
zoom-nfm.netlify.app/            -> tu index.html de registro
zoom-nfm.netlify.app/agendar.html -> la página agendar.html
```

Si las subís a dos sitios distintos de Netlify (dos dominios), `localStorage` NO se
comparte y ahí sí hace falta pasar los datos por el link (ver README, sección de la URL).

## Cómo desplegar las dos juntas

1. Poné en una misma carpeta: tu `index.html` (registro) + `agendar.html`.
2. Arrastrá **la carpeta** a [app.netlify.com/drop](https://app.netlify.com/drop)
   (o al sitio que ya tenés, "Deploys" → arrastrar).
3. Quedan las dos en el mismo dominio → `localStorage` compartido → autocompletado solo. ✅
