#!/bin/bash
# stop-validator.sh v5.0.0 — Stop hook (harness-engineering sensor)
#
# Two jobs:
#   1. SENSOR (first-prompt routing): reads session transcript; if the
#      structured first-turn block (ENTENDIDO/MODO/...) is absent, vetoes
#      (non-zero exit) so the model re-emits it. Skips veto if transcript
#      unreadable OR `stop_hook_active` is true (avoid infinite loop).
#   2. Existing: mark session boundary in tasklog + best-effort timestamps.
#
# Truth: the transcript file, not assertions (hard rule #6).

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
REG="$PROJECT_ROOT/workspace/.workspace-registry.json"

# ── SENSOR: first-prompt routing block ──
INPUT="$(cat || true)"
STOP_ACTIVE=$(echo "$INPUT" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print('true' if d.get('stop_hook_active') else 'false')" 2>/dev/null || echo "false")
TRANSCRIPT=$(echo "$INPUT" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('transcript_path') or '')" 2>/dev/null || echo "")

if [[ "$STOP_ACTIVE" = "true" ]]; then
  echo "STOP: skip-routing-sensor (stop_hook_active)" >&2
elif [[ -z "$TRANSCRIPT" || ! -r "$TRANSCRIPT" ]]; then
  echo "STOP: skip-routing-sensor (transcript unreadable)" >&2
else
  # Block present = "ENTENDIDO:" marker anywhere in the transcript (once
  # emitted on turn 1, it stays for all subsequent stops this session).
  if ! grep -q 'ENTENDIDO:' "$TRANSCRIPT" 2>/dev/null; then
    echo "STOP-BLOCK: first-turn routing block missing. Re-emit ENTENDIDO/MODO/SUPUESTOS/GAPS/PERFIL/SKILL/TAREA/GATE (see runtime/delta-claude.md)." >&2
    exit 1
  fi
fi

[ ! -f "$REG" ] && { echo "STOP: no-workspace-system" >&2; exit 0; }

A=$(grep -o '"activeWorkspace"[[:space:]]*:[[:space:]]*"[^"]*"' "$REG" 2>/dev/null | \
  sed 's/.*"activeWorkspace"[[:space:]]*:[[:space:]]*"//' | sed 's/"//') || true
[ -z "$A" ] || [ "$A" = "null" ] && { echo "STOP: no-active-workspace" >&2; exit 0; }
[ ! -d "$PROJECT_ROOT/workspace/$A" ] && { echo "STOP: orphaned-workspace" >&2; exit 0; }

NOW_TIME=$(date +"%H:%M")
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TL="$PROJECT_ROOT/workspace/$A/tasklog.md"

if [ -f "$TL" ]; then
  ACTIONS=$(grep -c '^### ' "$TL" 2>/dev/null || echo "0")
  printf "\n---\n\n### %s — Session boundary\n- Actions logged: %s\n" "$NOW_TIME" "$ACTIONS" >> "$TL"
fi

# Best-effort timestamp updates
META="$PROJECT_ROOT/workspace/$A/.workspace.json"
[ -f "$META" ] && sed -i '' "s/\"updated\": \"[^\"]*\"/\"updated\": \"$NOW_ISO\"/" "$META" 2>/dev/null

CFG="$PROJECT_ROOT/.jm-adk.json"
[ -f "$CFG" ] && sed -i '' "s/\"date\": [^,]*/\"date\": \"$(date +%Y-%m-%d)\"/" "$CFG" 2>/dev/null

echo "STOP: workspace=$A actions=$ACTIONS" >&2
exit 0
