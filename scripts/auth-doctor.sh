#!/usr/bin/env bash
# auth-doctor.sh — diagnose MCP auth state for the 3 servers. Read-only.
set -uo pipefail
ok=0; warn=0

check() { # name condition hint
  if eval "$2"; then echo "OK   $1"; ok=$((ok+1)); else echo "WARN $1 — $3"; warn=$((warn+1)); fi
}

echo "== Pristino Beta auth doctor =="
check "notebooklm: nlm CLI"        'command -v nlm >/dev/null'                          "install notebooklm-mcp-cli (uv tool install notebooklm-mcp-cli)"
check "notebooklm: auth valid"     '[[ $(nlm login --check 2>&1 | grep -ci "valid") -gt 0 ]]' "run: nlm login"
check "notebooklm: mcp binary"     'command -v notebooklm-mcp >/dev/null'               "uv tool install notebooklm-mcp-cli"
check "stitch: gcloud ADC or key"  '[[ -f "$HOME/.config/gcloud/application_default_credentials.json" || -n "${STITCH_API_KEY:-}" ]] || security find-generic-password -s pristino-stitch -w >/dev/null 2>&1' "gcloud auth application-default login OR keychain add-generic-password -s pristino-stitch"
check "workspace-mcp: uvx"         'command -v uvx >/dev/null'                          "install uv"
check "workspace-mcp: oauth file"  '[[ -f "$HOME/.config/workspace-mcp/credentials.json" ]]' "place Google OAuth client credentials there"
check "codex config"               '[[ -f "$HOME/.codex/config.toml" ]]'                "codex not configured"
check "antigravity mcp config"     '[[ -f "$HOME/.gemini/config/mcp_config.json" ]]'    "antigravity not configured"

echo "-- $ok ok, $warn warn"
exit 0
