# Cómo instalar el Skill de Samy en cualquier cuenta de Claude

> Guion para el Loom. Tiempo: ~3 minutos. No requiere nada técnico.
> Recomendado: usar el modelo Claude más reciente (Opus 4.x / el que esté disponible).

## Opción A — Claude.ai con Proyectos (la recomendada para el equipo)

1. **Entrá a [claude.ai](https://claude.ai)** con tu cuenta.
2. En el panel izquierdo, **Projects → Create project**. Nombralo **"Skill de Samy"**.
3. Abrí el proyecto → **Project knowledge / Add content**.
4. **Subí los archivos del skill.** Tenés dos formas:
   - **Fácil (1 archivo):** subí `skill-samy-COMPLETO.md` (tiene todo junto).
   - **Detallada (7 archivos):** subí los 7 `.md` de la carpeta `samy/` (1-voz, 2-avatar, 3-oferta, 4-objeciones, 5-casos, 6-ctas, 7-otro-contexto).
   - *(Opcional)* subí también `GUIA_DE_USO.md` para tener los prompts a mano.
5. **Pegá esta instrucción en "Custom instructions" del proyecto:**
   ```
   Sos el cerebro de marca de Samy Bruttman (Flowscale). Respondé SIEMPRE en su voz
   (cercana, cruda, anti-corporativa, spanglish natural) usando los archivos del proyecto:
   voz, avatar (A crédito / B creadores), frameworks, objeciones, casos verificables, CTAs.
   Priorizá el dolor real del lead en SUS palabras y el mecanismo único camuflado.
   PROHIBIDO: inventar cifras de ingresos, escasez fabricada, presión de pago o tono
   corporativo (límite de la sección 10). Si te piden algo así, ofrecé la versión honesta.
   ```
6. **Listo.** Abrí un chat nuevo dentro del proyecto y pedile lo que quieras (ver `GUIA_DE_USO.md`). Empezá por el prompt de los anuncios para probarlo.

> Todos en el equipo pueden crear su propio proyecto con los mismos archivos. El skill no depende de una cuenta específica.

## Opción B — Para el dashboard Blissful (Cerebro IA)
En Blissful, andá a **"Cerebro IA / Contexto de marca"** y subí los mismos `.md` (o el COMPLETO). A partir de ahí, Blissful escribe en la voz de la marca combinando el skill con la data real del cliente.

## Opción C — Claude Code (para perfiles técnicos)
Copiá la carpeta `samy/` dentro del repo y referenciala, o pegá `skill-samy-COMPLETO.md` como contexto. (No es necesario para el equipo no técnico.)

---

## Cómo actualizar el skill
Cuando haya material nuevo (más calls, testimonios, cambios de oferta), se regenera `skill-samy-COMPLETO.md` y se vuelve a subir al proyecto (reemplazando el anterior). Nada más.

## Qué incluye el ZIP
- `samy/` → los 7 archivos del skill (el cerebro).
- `skill-samy-COMPLETO.md` → todo junto en un archivo (para subir rápido).
- `GUIA_DE_USO.md` → qué pedirle + prompts listos.
- `INSTALAR.md` → este archivo.
- `README.md` → arquitectura general.
- `plantilla-portable/` → molde vacío para crear el skill de OTRO cliente (no hace falta para usar el de Samy).
