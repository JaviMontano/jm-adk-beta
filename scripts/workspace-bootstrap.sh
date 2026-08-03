#!/usr/bin/env bash
# workspace-bootstrap.sh v1.0.0 — instantiate a workspace from _template
#
# Creates the workspace system the harness expects (session-init.sh,
# first-prompt-router.sh): `.jm-adk.json`, `workspace/.workspace-registry.json`,
# and a fresh `workspace/<YYYY-MM-DD-slug>/` cloned from `workspace/_template/`.
#
# Anti-scope: runtime state only. Does NOT touch generated adapter files
# (CLAUDE.md/AGENTS.md/GEMINI.md). Script-first, dry-run-first (hard rule #4).
#
# Usage:
#   scripts/workspace-bootstrap.sh <slug> [--apply]
#   scripts/workspace-bootstrap.sh my-app --apply   # actually write
#   scripts/workspace-bootstrap.sh my-app           # dry-run (prints plan)

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TPL="$ROOT/workspace/_template"

SLUG="${1:-}"
APPLY=0
[[ "${2:-}" = "--apply" ]] && APPLY=1

if [[ -z "$SLUG" ]]; then
  echo "usage: workspace-bootstrap.sh <slug> [--apply]" >&2
  exit 1
fi

# slug sanity: lowercase, ascii, hyphens
SLUG=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//')
WS_ID="$(date +%Y-%m-%d)-${SLUG}"
WS_DIR="$ROOT/workspace/$WS_ID"
REG="$ROOT/workspace/.workspace-registry.json"
CFG="$ROOT/.jm-adk.json"

echo "PLAN: workspace_id=$WS_ID"
echo "PLAN: dir=$WS_DIR"
echo "PLAN: registry=$REG"
echo "PLAN: config=$CFG"

if [[ "$APPLY" = "0" ]]; then
  echo "DRY-RUN: re-run with --apply to write"
  exit 0
fi

# write
mkdir -p "$WS_DIR"
cp -R "$TPL/." "$WS_DIR/"

# registry (idempotent: create or update activeWorkspace)
mkdir -p "$ROOT/workspace"
if [[ ! -f "$REG" ]]; then
  cat > "$REG" <<EOF
{
  "activeWorkspace": "$WS_ID",
  "workspaces": ["$WS_ID"]
}
EOF
else
  # update active + append (macOS sed; portable enough for harness)
  sed -i '' "s/\"activeWorkspace\"[[:space:]]*:[[:space:]]*\"[^\"]*\"/\"activeWorkspace\": \"$WS_ID\"/" "$REG"
  grep -q "\"$WS_ID\"" "$REG" || sed -i '' "s/\"workspaces\"[[:space:]]*:[[:space:]]*\[/\"workspaces\": [\"$WS_ID\", /" "$REG"
fi

# harness config marker (session-init.sh probes .jm-adk.json existence)
if [[ ! -f "$CFG" ]]; then
  cat > "$CFG" <<EOF
{
  "version": "1.0.0",
  "date": "$(date +%Y-%m-%d)",
  "profile": "${JMADK_PROFILE:-profiles/metodologia.md}"
}
EOF
fi

echo "APPLIED: workspace=$WS_ID"
echo "NEXT: bash scripts/first-prompt-router.sh --json   # should now show resume_project"