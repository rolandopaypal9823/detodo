---
name: landing-venta-directa
description: Arquitectura de landing pages de venta directa (respuesta directa) para NFM / Instituto de Productividad — la estructura bloque por bloque, las mecánicas de conversión y la auditoría de páginas existentes. Activá SIEMPRE que el usuario pida armar, estructurar, rediseñar, reordenar, auditar o diagnosticar una landing, página de venta, sales page, página de producto, página de checkout previo, página de libro, página de curso o página de evento; cuando pregunte "por qué esta landing no vende", "dónde está floja", "qué le falta a la página", "en qué orden van las secciones"; cuando mencione "bloques", "esqueleto de landing", "wireframe", "above the fold", "order bump", "value stack", "garantía", "FAQ de objeciones", "descalificador", "prueba social"; o cuando pegue el HTML/screenshot de una página propia o de referencia para extraerle la estructura. Complementa a funnel400 (que aporta el copy y la curiosidad) resolviendo el ORDEN, la ARQUITECTURA y la MECÁNICA de la página.
---

# Landing de venta directa — arquitectura, mecánica y auditoría

funnel400 responde **qué decir**. Esta skill responde **en qué orden, en qué bloque, y con qué mecánica de página**.

Tesis central: **una landing de venta directa no es un texto largo con un botón al final — es una máquina de eliminar razones para no comprar, en el orden exacto en que esas razones aparecen en la cabeza del lector.** Cada bloque existe para matar una objeción específica. Si un bloque no mata una objeción, sobra.

Regla de oro estructural: **el orden de los bloques es el orden de las preguntas del lector.** No el orden en que a vos te resulta cómodo contar tu producto.

```
¿De qué se trata? → ¿Esto es para mí? → ¿Por qué me pasa esto? → ¿Por qué es distinto?
→ ¿Qué me llevo? → ¿Por qué te creo? → ¿Cuánto cuesta? → ¿Y si no funciona? → ¿Por qué ahora?
```

## Modos de uso

### Modo 1 — ARMAR una landing nueva
1. Confirmá que existe research y oferta (si no, mandá a `funnel400` → `research-dolor.md` y `ofertas-y-ads.md`). Sin oferta Insomnio/Última Vida, la mejor estructura no salva la página.
2. Leé `references/01-arquitectura-bloques.md` y elegí el set de bloques según el tipo de página (hay 3 variantes: producto de bajo ticket, evento/entrada, alto ticket con aplicación).
3. Leé `references/02-mecanicas-de-conversion.md` y decidí las mecánicas: CTA único, modal de orden, calculadora, bumps, garantía.
4. Escribí el copy de cada bloque con `references/03-copy-por-bloque.md` (cada bloque tiene su función, su objeción y su formato).
5. Maquetá con `references/05-implementacion-nfm.md` (sistema visual NFM, restricciones de Circle/Shopify).
6. Pasá el checklist del final de este archivo.

### Modo 2 — AUDITAR una landing existente
Leé `references/04-auditoria.md` y corré el scorecard. Entregá: bloques presentes, bloques faltantes, bloques fuera de orden, objeciones sin matar, y las 3 correcciones de mayor impacto primero. **No reescribas la página entera si el problema es de orden o de bloque faltante** — decilo y arreglá eso.

### Modo 3 — EXTRAER estructura de una página de referencia
Cuando el usuario pega el HTML o screenshots de una landing ajena: mapeá bloque por bloque **por función, no por copy**. Entregá una tabla `bloque → función → objeción que mata → si nos sirve`. Distinguí siempre entre lo que se puede ver (copy, estructura, tracking, mecánica) y lo que NO (conversión real, qué variante de test es, qué hay después del checkout). Nunca asumas que la página funciona solo porque es de alguien conocido.

## Qué leer según la tarea

| El usuario pide… | Leé |
|---|---|
| Estructura, orden de secciones, esqueleto, wireframe | `references/01-arquitectura-bloques.md` |
| CTA, modal, bumps, garantía, urgencia, calculadora, formulario | `references/02-mecanicas-de-conversion.md` |
| Qué escribir en cada bloque, headlines, bullets, FAQ | `references/03-copy-por-bloque.md` |
| Auditar / diagnosticar / "por qué no vende" | `references/04-auditoria.md` |
| Maquetar en el sistema visual NFM, Circle, Shopify, mobile | `references/05-implementacion-nfm.md` |

## Las 9 leyes de la landing de venta directa

1. **Un solo objetivo, un solo CTA.** Toda la página empuja a la misma acción, con el mismo texto de botón, repetido 5-8 veces. Cero links de navegación, cero menú, cero footer con "sobre nosotros". Cada salida alternativa es una fuga.

2. **Una objeción = una sección entera.** No metas cinco objeciones en un FAQ apretado al pie. La objeción principal ("no tengo tiempo", "ya probé de todo", "esto es para gente que ya vende") merece su propio bloque con título, argumento y prueba. El FAQ es para las objeciones chicas.

3. **El descalificador vende más que el calificador.** Decir en voz alta para quién NO es esto aumenta la conversión de los que sí son. Sin descalificador, el lector no siente que lo elegiste — siente que le vendés a cualquiera.

4. **Participación antes de la oferta.** Un elemento donde el lector hace algo (calculadora, selector, mini-diagnóstico, elegir su caso) justo antes del bloque de precio. Observar crea distancia, participar crea posesión. Es la ley 7 de funnel400 aterrizada en la página.

5. **El precio necesita una justificación honesta.** Si es barato, explicá por qué es barato (no "oferta por tiempo limitado" — eso es urgencia falsa y el lector la huele). Razón real: "es barato porque quiero que después compres X", "porque es digital y no tiene costo marginal", "porque prefiero 1.000 lectores que 50 compradores".

6. **La prueba social va pegada al reclamo, no amontonada al final.** Cada afirmación fuerte lleva su prueba al lado. Un bloque de 12 testimonios seguidos se saltea; un testimonio abajo de la promesa que valida, se lee.

7. **Above the fold se decide en 3 segundos.** Qué es + para quién + qué gana + botón. Si el lector tiene que scrollear para saber de qué se trata, la página ya perdió. El botón visible sin scroll no es negociable.

8. **Micro-compromiso antes de macro-compromiso.** Nunca mandes del botón directo a un formulario de 12 campos ni a un checkout frío. Un paso intermedio (modal, selector, primera pregunta) sube conversión porque el cerebro ya se comprometió. Escalón, no montaña.

9. **Mobile primero, siempre.** El 80%+ del tráfico de NFM es mobile. Si el above the fold no cierra en 640px de alto con el botón adentro, no está terminado.

## Anti-patrones (matan páginas)

- Menú de navegación arriba. Cada link es una salida.
- Headline de categoría en vez de promesa ("Curso de productividad" en vez de "Recuperá 2 horas por día sin trabajar más rápido").
- Hablar del producto antes de haber nombrado el problema con nombre propio.
- Botón que dice "Enviar", "Más info", "Comprar". El botón dice lo que el lector gana ("Conseguir mi ejemplar").
- Testimonios sin nombre, sin foto, sin resultado concreto. Peor que no tener.
- Contador regresivo que se reinicia al recargar. El lector lo detecta y pierde toda la confianza de la página.
- Precio escondido o "consultanos". En bajo ticket, esconder el precio es fuga.
- Bloques de 400 palabras sin subtítulo. La página se escanea antes de leerse: subtítulos, negritas y bullets tienen que contar la historia solos.
- Dos ofertas compitiendo en la misma página sin jerarquía visual clara.
- Copiar la estética de la referencia junto con su estructura. La estructura se copia; el sistema visual es de NFM (azul `#0c3452`, naranja `#ff6602`, Montserrat + Open Sans).

## Relación con las otras skills

- **funnel400** = el copy y la psicología (curiosidad → espejo → aha → menú → puente). Esta skill = el contenedor. Se usan juntas: leé `references/01-arquitectura-bloques.md` que trae el mapeo bloque ↔ paso del protocolo.
- **webinar-dan-henry** = presentaciones y VSLs (agreement engineering). Si la página es la puerta de un webinar, la landing la arma esta skill y el guion lo arma aquella.
- **nfm-super-skill** = voz, marca, avatar, testimonios reales. Toda landing pasa por ahí antes de publicarse. **Nunca inventes testimonios, cifras ni fechas** — solo lo que esté en `06_casos_exito_testimonios.md` o lo que el usuario confirme.

## Checklist antes de entregar cualquier landing

- [ ] ¿Above the fold responde qué es + para quién + qué gana, con botón visible sin scroll, en mobile?
- [ ] ¿Hay UN solo CTA, con el mismo texto, repetido 5-8 veces, sin menú ni links de salida?
- [ ] ¿El botón abre un micro-paso (modal/selector), no un salto grande?
- [ ] ¿Existe el bloque "esto NO es para vos"?
- [ ] ¿La objeción principal tiene su propia sección, no una línea en el FAQ?
- [ ] ¿El mecanismo tiene nombre propio y una prueba que lo respalda?
- [ ] ¿Hay un elemento de participación antes del bloque de precio?
- [ ] ¿Cada reclamo fuerte tiene su prueba al lado?
- [ ] ¿El precio está visible y justificado con una razón honesta?
- [ ] ¿La garantía está escrita en una sola frase que se entiende sin leer dos veces?
- [ ] ¿La urgencia es real (fecha, stock, cupo verificable) o no hay urgencia?
- [ ] ¿Los testimonios son reales, con nombre y resultado concreto?
- [ ] ¿Sistema visual NFM, con logo, tipografías y paleta correctas?
- [ ] ¿Pasa el checklist de funnel400 en el copy?
