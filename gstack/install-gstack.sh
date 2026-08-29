#!/usr/bin/env bash
# Instala gstack (github.com/garrytan/gstack) en Claude Code.
#
# En una maquina normal (Mac/Linux con red abierta) alcanza con los pasos 1-2:
# los pasos 3-4 son parches para entornos tipo Claude Code on the web, donde
# el proxy de red bloquea cdn.playwright.dev y hace interceptacion TLS.
#
# Requisitos: git, bun >= 1.0, node (obligatorio en Windows).
set -euo pipefail

GSTACK_DIR="$HOME/.claude/skills/gstack"

# --- 1. Clonar --------------------------------------------------------------
if [ -d "$GSTACK_DIR/.git" ]; then
  echo "==> gstack ya clonado, actualizando"
  git -C "$GSTACK_DIR" pull --ff-only
else
  echo "==> Clonando gstack"
  mkdir -p "$(dirname "$GSTACK_DIR")"
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$GSTACK_DIR"
fi

# --- 2. Deteccion de entorno restringido ------------------------------------
# Si Playwright no puede bajar su Chromium, usamos el que ya trae el contenedor.
SANDBOX=0
[ -n "${CCR_AGENT_PROXY_ENABLED:-}" ] && SANDBOX=1
[ -d /opt/pw-browsers ] && SANDBOX=1

if [ "$SANDBOX" -eq 1 ]; then
  echo "==> Entorno con proxy detectado: aplicando parches"

  # --- 3. Puente de Chromium ------------------------------------------------
  # gstack trae Playwright 1.62 (espera chromium-1234) pero el contenedor
  # tiene chromium-1194. Enlazamos el que hay al path que Playwright busca.
  BRIDGE="$HOME/.cache/gstack-pw"
  SRC_FULL=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux 2>/dev/null | head -1 || true)
  SRC_HL=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux 2>/dev/null | head -1 || true)

  if [ -n "$SRC_FULL" ] && [ -n "$SRC_HL" ]; then
    REV=$(grep -o '"chromium".*"revision": *"[0-9]*"' "$GSTACK_DIR/node_modules/playwright-core/browsers.json" 2>/dev/null | grep -o '[0-9]*"$' | tr -d '"' || echo 1234)
    mkdir -p "$BRIDGE/chromium-$REV" "$BRIDGE/chromium_headless_shell-$REV/chrome-headless-shell-linux64"
    ln -sfn "$SRC_FULL" "$BRIDGE/chromium-$REV/chrome-linux64"
    for f in "$SRC_HL"/*; do
      ln -sfn "$f" "$BRIDGE/chromium_headless_shell-$REV/chrome-headless-shell-linux64/$(basename "$f")"
    done
    ln -sfn "$SRC_HL/headless_shell" \
      "$BRIDGE/chromium_headless_shell-$REV/chrome-headless-shell-linux64/chrome-headless-shell"
    touch "$BRIDGE/chromium-$REV/INSTALLATION_COMPLETE" \
          "$BRIDGE/chromium-$REV/DEPENDENCIES_VALIDATED" \
          "$BRIDGE/chromium_headless_shell-$REV/INSTALLATION_COMPLETE" \
          "$BRIDGE/chromium_headless_shell-$REV/DEPENDENCIES_VALIDATED"
    export PLAYWRIGHT_BROWSERS_PATH="$BRIDGE"
    echo "    Chromium puenteado en $BRIDGE (revision $REV)"
  fi

  # --- 4. CA del proxy en el almacen NSS de Chromium ------------------------
  # El proxy intercepta TLS; Chromium no lee la CA del sistema, usa NSS.
  # Sin esto toda navegacion falla con ERR_CERT_AUTHORITY_INVALID.
  if [ -f /root/.ccr/ca-bundle.crt ]; then
    command -v certutil >/dev/null 2>&1 || {
      apt-get update -qq >/dev/null 2>&1 || true
      apt-get install -y -qq libnss3-tools >/dev/null 2>&1 || true
    }
    if command -v certutil >/dev/null 2>&1; then
      mkdir -p "$HOME/.pki/nssdb"
      TMPCA=$(mktemp -d)
      ( cd "$TMPCA" && csplit -z -f c- -b "%03d.pem" /root/.ccr/ca-bundle.crt '/BEGIN CERTIFICATE/' '{*}' >/dev/null 2>&1 || true )
      i=0
      for f in "$TMPCA"/c-*.pem; do
        [ -f "$f" ] || continue
        # Solo las CA de interceptacion, no los 148 roots publicos.
        openssl x509 -in "$f" -noout -subject 2>/dev/null | grep -qi "anthropic" || continue
        certutil -d "sql:$HOME/.pki/nssdb" -A -t "C,," -n "anthropic-proxy-$i" -i "$f" 2>/dev/null && i=$((i+1))
      done
      rm -rf "$TMPCA"
      echo "    $i CA de interceptacion agregadas al almacen NSS"
    fi
  fi
fi

# --- 5. Setup oficial -------------------------------------------------------
echo "==> Corriendo ./setup"
cd "$GSTACK_DIR" && ./setup

echo
echo "Listo. gstack $(cat "$GSTACK_DIR/VERSION") instalado."
[ "$SANDBOX" -eq 1 ] && echo "Nota: exporta PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/gstack-pw para usar /browse."
