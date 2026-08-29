# gstack — estado de la instalación

**Fuente:** https://github.com/garrytan/gstack — commit `07b59e3`, versión `1.75.0.0`
**Instalado en:** `~/.claude/skills/gstack` (modo solo, host `claude`, nombres cortos)

El archivo `skills.md` que circula es solo la **documentación**. El skill real es el repo
completo: un `SKILL.md` raíz que rutea, más 53 sub-skills con sus scripts y un binario
de browser de ~99 MB.

## Instalar

```bash
./gstack/install-gstack.sh
```

En una máquina normal equivale al comando oficial:

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack \
  && cd ~/.claude/skills/gstack && ./setup
```

Requisitos: git, [bun](https://bun.sh/) ≥ 1.0, node (obligatorio solo en Windows).

## Qué quedó funcionando

| Grupo | Comandos | Estado |
|---|---|---|
| Planificación | `/office-hours` `/spec` `/autoplan` `/plan-ceo-review` `/plan-eng-review` `/plan-design-review` `/plan-devex-review` `/plan-tune` | OK |
| Código | `/review` `/investigate` `/health` `/cso` `/ship` `/land-and-deploy` `/retro` | OK |
| Diseño | `/design-consultation` `/design-shotgun` `/design-html` `/design-review` | OK |
| Docs | `/document-generate` `/document-release` `/make-pdf` `/diagram` | OK |
| Seguridad | `/careful` `/freeze` `/guard` `/unfreeze` | OK |
| Contexto | `/learn` `/context-save` `/context-restore` | OK |
| Browser | `/browse` `/qa` `/qa-only` `/scrape` `/skillify` `/canary` `/benchmark` `/devex-review` | Parcial — ver abajo |
| iOS | `/ios-qa` `/ios-fix` `/ios-design-review` `/ios-clean` `/ios-sync` | No aplica en Linux |
| Externos | `/codex` `/setup-gbrain` `/sync-gbrain` `/pair-agent` | Requieren instalar la herramienta aparte |

## Parches que hizo falta aplicar en el contenedor remoto

Estos **no** hacen falta en una máquina local con red abierta. El `./setup` oficial
falla acá por dos razones del entorno:

1. **`cdn.playwright.dev` bloqueado por el proxy** → `./setup` moría al bajar Chromium
   (`set -e`), antes de enlazar los 53 skills. Se puentea el Chromium que ya trae el
   contenedor (`/opt/pw-browsers/chromium-1194`) al path que espera Playwright 1.62
   (`chromium-1234`), vía `PLAYWRIGHT_BROWSERS_PATH=~/.cache/gstack-pw`.
2. **Interceptación TLS del proxy** → toda navegación daba `ERR_CERT_AUTHORITY_INVALID`.
   Chromium no lee la CA del sistema sino el almacén NSS. Se agregan las 6 CA de
   Anthropic del bundle con `certutil` a `~/.pki/nssdb`.

Con ambos parches el daemon levanta sano y el TLS valida. Lo que **sigue** limitado es
el egreso: la política de red del entorno responde 403 a la mayoría de los hosts
(`example.com` da `ERR_TUNNEL_CONNECTION_FAILED`, `github.com` responde 403). Eso es
política de la organización, no de gstack — en tu máquina no pasa.

## Advertencias

- La instalación vive en `~/.claude/skills/`, que es **efímero** en Claude Code on the
  web: el contenedor se recicla y se pierde. Por eso está este script.
- gstack registra hooks en `~/.claude/settings.json` (uno de `Stop` para el timeline).
  Deja backup `settings.json.bak.<ts>`. Se quitan con
  `~/.claude/skills/gstack/bin/gstack-settings-hook remove-source --source gstack-timeline-stop`.
- Desinstalar: `~/.claude/skills/gstack/bin/gstack-uninstall`
- Los 53 skills suman ~682k tokens de documentación en disco; se cargan por demanda,
  no todos a la vez.
