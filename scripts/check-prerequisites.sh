#!/usr/bin/env bash
# check-prerequisites.sh — iikit pattern: phase completion = artifact existence.
# Usage: check-prerequisites.sh --phase <p0|p1|p2|p3|p4|p5|p6|p7> [--json]
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
  p6) REQUIRED=(scripts/first-prompt-router.sh scripts/workspace-bootstrap.sh scripts/stage-context-manifest.sh workspace/_template/CONTEXT.md workspace/_template/01_discovery/CONTEXT.md workspace/_template/02_spec/CONTEXT.md workspace/_template/03_build/CONTEXT.md workspace/_template/04_validate/CONTEXT.md workspace/_template/01_discovery/output/.gitkeep workspace/_template/02_spec/output/.gitkeep workspace/_template/03_build/output/.gitkeep workspace/_template/04_validate/output/.gitkeep workspace/_template/_config/.gitkeep references/ontology/constitution-must.md runtime/delta-claude.md) ;;
  p7) REQUIRED=(scripts/check-governance-consistency.sh) ;;
  *) echo "usage: $0 --phase p0..p7 [--json]" >&2; exit 2 ;;
esac

MISSING=()
for f in "${REQUIRED[@]}"; do
  [[ -e "$ROOT/$f" ]] || MISSING+=("$f")
done

# p7 is a true governance gate: the consistency sensor must exist AND pass.
# Other phases are pure artifact-existence (constitution: completion = artifact
# existence); p7 additionally runs the consistency sensor so "READY" means
# docs match source, not just "the script file is present".
CONSISTENCY_FAIL=""
if [[ "$PHASE" == "p7" && ${#MISSING[@]} -eq 0 ]]; then
  if ! CONSISTENCY_OUT=$(bash "$ROOT/scripts/check-governance-consistency.sh" 2>&1); then
    CONSISTENCY_FAIL="$CONSISTENCY_OUT"
  fi
fi

READY=$([[ ${#MISSING[@]} -eq 0 && -z "$CONSISTENCY_FAIL" ]] && echo true || echo false)
if [[ $JSON -eq 1 ]]; then
  printf '{"phase":"%s","ready":%s,"missing":[' "$PHASE" "$READY"
  for i in "${!MISSING[@]}"; do [[ $i -gt 0 ]] && printf ','; printf '"%s"' "${MISSING[$i]}"; done
  printf '],"consistency_fail":%s}\n' "$([[ -n "$CONSISTENCY_FAIL" ]] && printf '%s' "$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$CONSISTENCY_FAIL")" || echo '""')"
else
  if [[ "$READY" == "true" ]]; then
    echo "phase $PHASE: READY"
  else
    echo "phase $PHASE: BLOCKED"
    [[ ${#MISSING[@]} -gt 0 ]] && { echo "  missing:"; printf '    %s\n' "${MISSING[@]}"; }
    [[ -n "$CONSISTENCY_FAIL" ]] && printf '%s\n' "$CONSISTENCY_FAIL"
  fi
fi
[[ "$READY" == "true" ]]
