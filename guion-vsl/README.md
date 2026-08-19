# Guion VSL Platinum — versión Netlify

Documento editable con guardado real en la nube, usando Netlify Functions + Netlify Blobs.

## Estructura

```
netlify.toml               config de build y el redirect /api/doc
package.json               dependencia @netlify/blobs
netlify/functions/doc.mjs  GET lee / PUT guarda, en Netlify Blobs
public/index.html          la página (shell + contenido por defecto)
```

## Desplegar

**Opción Git (recomendada).** Conectá este repo en Netlify y apuntá el
*base directory* a `guion-vsl/`. Netlify corre el build, instala la
dependencia y publica la función sola.

**Opción CLI.**

```bash
cd guion-vsl
npm install
npx netlify deploy --prod
```

> Arrastrar la carpeta a netlify.com/drop **no sirve**: las funciones con
> dependencias npm necesitan el paso de build.

## Proteger la escritura

Sin protección, cualquiera que conozca la URL puede sobrescribir el guion.

En Netlify → *Site configuration* → *Environment variables*, creá:

| Variable | Valor |
|---|---|
| `EDIT_TOKEN` | una clave larga que elijas vos |

Con eso, guardar exige la clave. La página la pide una sola vez y la
recuerda en ese navegador. Sin la variable, la página muestra un cartel
avisando que el documento está abierto.

## Cómo guarda

- Al abrir, la página pide `GET /api/doc`. Si hay algo guardado, lo usa;
  si no, arranca del contenido por defecto que viene en el HTML.
- Al guardar, manda `PUT /api/doc` con el JSON del contenido y el `rev`
  que tenía cargado.
- Si otra persona guardó en el medio, el servidor responde 409 y no pisa
  nada — la página avisa y ofrece recargar.
