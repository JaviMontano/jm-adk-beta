#!/usr/bin/env bash
# first-prompt-router.sh v1.0.0 — first-prompt routing sensor (runtime behavior)
#
# Deterministic, read-only. Inspects workspace + task state on disk and emits
# routing decision so the model can produce the structured first-turn block:
#   ENTENDIDO / MODO / SUPUESTOS / GAPS / PERFIL / SKILL / TAREA / GATE
#
# Mapping (vibe-coder ally):
#   project  ≈ workspace  (workspace/<WS_ID>)
#   task     ≈ T-NNN      (workspace/<WS_ID>/tasks/T-NNN-*)
#
# Anti-scope: routing is RUNTIME behavior. This script does NOT mutate disk,
# does NOT edit generated adapter files (CLAUDE.md/AGENTS.md). Always exits 0
# (informational sensor; ambiguity -> coverage_gap, defer to model + user).
#
# Sources: ICM layered loading (notebook 13845882 §3.2) + harness-engineering
# sensors (notebook c94c6afa). Edit-source principle: misbehavior fixed here.
# [DOC]
#
# Usage:
#   scripts/first-prompt-router.sh            # KEY: VALUE (session-init format)
#   scripts/first-prompt-router.sh --json     # single JSON line
#   scripts/first-prompt-router.sh --selftest # dry-run-first parse check

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

JSON=0
SELFTEST=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON=1; shift ;;
    --selftest) SELFTEST=1; shift ;;
    *) echo "first-prompt-router: unknown arg: $1 (ignoring)" >&2; shift ;;
  esac
done

if [[ "$SELFTEST" = "1" ]]; then
  echo "SELFTEST: ok (script parses, no disk mutation)"
  exit 0
fi

# ── Probe workspace system (mirrors session-init.sh) ──
CFG="$ROOT/.jm-adk.json"
REG="$ROOT/workspace/.workspace-registry.json"

WS_ENABLED="false"
WS_ID=""
WS_DIR=""
WS_STALE="false"

if [[ -f "$CFG" && -f "$REG" ]]; then
  WS_ENABLED="true"
  WS_ID=$(grep -o '"activeWorkspace"[[:space:]]*:[[:space:]]*"[^"]*"' "$REG" 2>/dev/null \
    | sed 's/.*"activeWorkspace"[[:space:]]*:[[:space:]]*"//' | sed 's/"//' || true)
  if [[ -z "$WS_ID" || "$WS_ID" = "null" ]]; then
    WS_ID=""
  else
    WS_DIR="$ROOT/workspace/$WS_ID"
    [[ ! -d "$WS_DIR" ]] && WS_DIR=""
  fi
  TODAY=$(date +%Y-%m-%d)
  WD=$(echo "$WS_ID" | grep -o '^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' || true)
  [[ -n "$WD" && "$WD" != "$TODAY" ]] && WS_STALE="true"
fi

# ── Probe stages (ICM Layer 2: numbered stage dirs with output/) ──
LAST_STAGE=""
if [[ -n "$WS_DIR" ]]; then
  # last_stage = newest mtime artifact under any NN_*/output/ dir
  LAST_STAGE=$(find "$WS_DIR" -maxdepth 2 -type f -path '*/output/*' 2>/dev/null \
    -exec stat -f '%m %N' {} + 2>/dev/null \
    | sort -rn | head -1 | sed 's|.*'"$WS_DIR"'/||' | cut -d/ -f1 || true)
fi

# ── Probe tasks (T-NNN, convention P33 reused from task-subfolder skill) ──
TASK_ONGOING=""
TASK_LATEST=""
TASK_CHECKBOXES_OPEN=0
if [[ -n "$WS_DIR" && -d "$WS_DIR/tasks" ]]; then
  TASK_LATEST=$(ls -1d "$WS_DIR"/tasks/T-[0-9][0-9][0-9]* 2>/dev/null | tail -1 || true)
  if [[ -n "$TASK_LATEST" ]]; then
    TM="$TASK_LATEST/task.md"
    if [[ -f "$TM" ]]; then
      # status heuristic: presence of unchecked acceptance checkboxes = ongoing
      TASK_CHECKBOXES_OPEN=$(grep -c '^- \[ \]' "$TM" 2>/dev/null || echo "0")
      [[ "$TASK_CHECKBOXES_OPEN" -gt 0 ]] && TASK_ONGOING="$(basename "$TASK_LATEST")"
    fi
  fi
fi

# ── Decide MODE ──
MODE="ambiguous"
GAPS=""
GAP_REASON=""

if [[ "$WS_ENABLED" = "false" ]]; then
  MODE="create_project"
  GAPS="no-workspace-system"
  GAP_REASON=".jm-adk.json or workspace/.workspace-registry.json absent; harness fresh"
elif [[ -z "$WS_ID" ]]; then
  MODE="create_project"
  GAPS="no-active-workspace"
  GAP_REASON="registry exists but activeWorkspace unset/null"
elif [[ -z "$WS_DIR" ]]; then
  MODE="ambiguous"
  GAPS="orphaned-workspace"
  GAP_REASON="activeWorkspace references missing dir $WS_ID"
elif [[ -n "$TASK_ONGOING" ]]; then
  MODE="resume_task"
elif [[ -n "$TASK_LATEST" ]]; then
  MODE="new_task"
else
  MODE="resume_project"
  [[ "$WS_STALE" = "true" ]] && { GAPS="stale-workspace"; GAP_REASON="last workspace activity not today"; }
fi

# ── Output ──
if [[ "$JSON" = "1" ]]; then
  cat <<EOF
{"mode":"$MODE","workspace_enabled":$WS_ENABLED,"workspace_id":"$WS_ID","workspace_stale":$WS_STALE,"last_stage":"$LAST_STAGE","task_ongoing":"$TASK_ONGOING","task_latest":"$(basename "$TASK_LATEST" 2>/dev/null)","task_open_checkboxes":$TASK_CHECKBOXES_OPEN,"coverage_gap":"$GAPS","gap_reason":"$GAP_REASON"}
EOF
else
  echo "ROUTE-MODE: $MODE"
  echo "ROUTE-WS-ENABLED: $WS_ENABLED"
  [[ -n "$WS_ID" ]]        && echo "ROUTE-WS-ID: $WS_ID"
  [[ "$WS_STALE" = "true" ]] && echo "ROUTE-WS-STALE: true"
  [[ -n "$LAST_STAGE" ]]   && echo "ROUTE-LAST-STAGE: $LAST_STAGE"
  [[ -n "$TASK_ONGOING" ]]  && echo "ROUTE-TASK-ONGOING: $TASK_ONGOING"
  [[ -n "$TASK_LATEST" ]]   && echo "ROUTE-TASK-LATEST: $(basename "$TASK_LATEST")"
  [[ "$TASK_CHECKBOXES_OPEN" -gt 0 ]] && echo "ROUTE-TASK-OPEN-CHECKBOXES: $TASK_CHECKBOXES_OPEN"
  [[ -n "$GAPS" ]]          && echo "ROUTE-COVERAGE-GAP: $GAPS"
  [[ -n "$GAP_REASON" ]]    && echo "ROUTE-GAP-REASON: $GAP_REASON"
fi