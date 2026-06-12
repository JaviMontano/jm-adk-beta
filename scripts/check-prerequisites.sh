#!/usr/bin/env bash
# check-prerequisites.sh — iikit pattern: phase completion = artifact existence.
# Usage: check-prerequisites.sh --phase <p0|p1|p2|p3|p4|p5> [--json]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PHASE="" JSON=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase) PHASE="$2"; shift 2 ;;
    --json) JSON=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

declare -a REQUIRED
case "$PHASE" in
  p0) REQUIRED=(catalog/coverage-matrix.csv migrate/build-refs.py) ;;
  p1) REQUIRED=(harness/manifest.json harness/manifest.schema.json catalog/skills.json runtime/core.md scripts/build-indexes.py hooks/hooks.json references/ontology/constitution-v7.0.0.md references/roles/lead.md) ;;
  p2) REQUIRED=(skills/kata/SKILL.md catalog/skills.json) ;;
  p3) REQUIRED=(catalog/consolidation-map.yaml skills/iikit/SKILL.md skills/firebase/SKILL.md skills/google-workspace/SKILL.md) ;;
  p4) REQUIRED=(CLAUDE.md AGENTS.md GEMINI.md SKILLS.md .agent/skills_index.json scripts/gen_mcp.py) ;;
  p5) REQUIRED=(scripts/validate-coverage.py harness/.manifest.json) ;;
  *) echo "usage: $0 --phase p0..p5 [--json]" >&2; exit 2 ;;
esac

MISSING=()
for f in "${REQUIRED[@]}"; do
  [[ -e "$ROOT/$f" ]] || MISSING+=("$f")
done

if [[ $JSON -eq 1 ]]; then
  printf '{"phase":"%s","ready":%s,"missing":[' "$PHASE" "$([[ ${#MISSING[@]} -eq 0 ]] && echo true || echo false)"
  for i in "${!MISSING[@]}"; do [[ $i -gt 0 ]] && printf ','; printf '"%s"' "${MISSING[$i]}"; done
  printf ']}\n'
else
  if [[ ${#MISSING[@]} -eq 0 ]]; then echo "phase $PHASE: READY"; else
    echo "phase $PHASE: BLOCKED — missing:"; printf '  %s\n' "${MISSING[@]}"
  fi
fi
[[ ${#MISSING[@]} -eq 0 ]]
