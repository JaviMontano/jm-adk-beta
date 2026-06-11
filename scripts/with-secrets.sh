#!/usr/bin/env bash
# with-secrets.sh — exec wrapper: resolve secrets (keychain -> env) then exec command.
# Neutralizes Codex/Antigravity lack of ${ENV} expansion in MCP configs:
#   command = "/path/to/with-secrets.sh"  args = ["uvx", "workspace-mcp", ...]
# Secrets resolved (export only if found, never logged):
#   STITCH_API_KEY        <- keychain service "pristino-stitch" or env
set -euo pipefail

kc() { security find-generic-password -s "$1" -w 2>/dev/null || true; }

if [[ -z "${STITCH_API_KEY:-}" ]]; then
  v="$(kc pristino-stitch)"
  [[ -n "$v" ]] && export STITCH_API_KEY="$v"
fi

exec "$@"
