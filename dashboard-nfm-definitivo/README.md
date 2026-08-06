# Dashboard NFM · v1.0

Dashboard de métricas de contenido: Instagram, Stories, YouTube, Facebook, LinkedIn y TikTok, con embudo, objetivos de seguidores, anuncios de Meta, competidores, email e insights con Claude.

Es la **fusión** del dashboard NFM VIP (el más completo en funciones) con el dashboard Flowscale (el más cuidado en experiencia de uso). Base: el NFM VIP; encima, la capa de experiencia del otro. No se sacó nada.

## Empezar

- **¿Vas a deployarlo?** → `INSTRUCCIONES.md` (paso a paso, sin saber programar)
- **¿Vas a tocarle el código?** → `HANDOFF.md` (qué hace cada cosa y dónde está)

## Lo que trae

```
index.html            ← toda la app (HTML + CSS + JS en un archivo)
netlify.toml          ← config de build y guía de variables de entorno
package.json          ← dependencias de las funciones
netlify/functions/    ← 16 funciones (IA, Meta, YouTube, Apify, email, nube)
INSTRUCCIONES.md      ← guía de deploy para el usuario final
HANDOFF.md            ← documento técnico de traspaso
```

Se sube arrastrando la carpeta a **app.netlify.com/drop**. Sin ninguna API key, toda la analítica sobre tus CSV/XLSX funciona igual: las keys solo prenden módulos extra.

## Lo nuevo de esta versión

- **Configuración inicial** de 5 pasos la primera vez: tu nombre, tu marca, tu logo, qué querés lograr y qué secciones vas a usar.
- **Saludo por hora del día** en la portada, con tu nombre, más el pulso de la semana.
- **Secciones plegables**: abrís solo lo que querés mirar y el dashboard se acuerda.
- **Menú a medida**: lo que no usás desaparece (sin borrar nada).
- **🎯 Objetivos**: a cuántos seguidores querés llegar y cuántas piezas como tus mejores te faltan. Sin IA, aritmética sobre tu data.
- **⚡ FlowScore**: 1 a 100 comparándote contra vos mismo.
- **Control de gasto**: estimador de costo antes de cada scrapeo de Apify, contador de saldo, y contador de uso de IA.
