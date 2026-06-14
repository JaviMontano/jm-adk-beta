#!/usr/bin/env bash
# validate-agent.sh — validate an agent file against references/agent-contract.md (beta-native).
# Usage: scripts/validate-agent.sh <agent.md> [<agent.md> ...]
#        scripts/validate-agent.sh --all        # officers + role-templates
# Exit: 0 if all pass (warnings OK), 1 if any ERROR.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

VALID_MODEL="haiku sonnet opus inherit"
VALID_COLOR="blue cyan green yellow magenta red"
VALID_TIER="ceo coo officer steward sme role-template spoke"
VALID_PHASE="Think Plan Build Review Validate Ship"

errors=0; warns=0; checked=0

fm_get() { # fm_get <file> <key> → value (first match in frontmatter)
  awk -v k="$2" '
    NR==1 && $0!="---"{exit}
    NR>1 && $0=="---"{exit}
    NR>1{ if ($0 ~ "^"k":") { sub("^"k":[[:space:]]*",""); print; exit } }' "$1"
}
in_set() { case " $2 " in *" $1 "*) return 0;; *) return 1;; esac; }

validate() {
  local f="$1"; local rel="${f#$ROOT/}"; checked=$((checked+1))
  [ -f "$f" ] || { echo "ERROR $rel: file not found"; errors=$((errors+1)); return; }
  [ "$(head -1 "$f")" = "---" ] || { echo "ERROR $rel: missing YAML frontmatter (--- first line)"; errors=$((errors+1)); return; }

  local name role desc model color tier phase
  name=$(fm_get "$f" name); role=$(fm_get "$f" role); desc=$(fm_get "$f" description)
  model=$(fm_get "$f" model); color=$(fm_get "$f" color); tier=$(fm_get "$f" tier); phase=$(fm_get "$f" phase)

  # required fields
  for kv in "name:$name" "role:$role" "description:$desc" "model:$model" "color:$color" "tier:$tier" "phase:$phase"; do
    [ -n "${kv#*:}" ] || { echo "ERROR $rel: missing required frontmatter '${kv%%:*}'"; errors=$((errors+1)); }
  done
  # enums
  [ -z "$model" ] || in_set "$model" "$VALID_MODEL" || { echo "ERROR $rel: model '$model' not in {$VALID_MODEL}"; errors=$((errors+1)); }
  [ -z "$color" ] || in_set "$color" "$VALID_COLOR" || { echo "ERROR $rel: color '$color' not in {$VALID_COLOR}"; errors=$((errors+1)); }
  [ -z "$tier" ]  || in_set "$tier"  "$VALID_TIER"  || { echo "ERROR $rel: tier '$tier' not in {$VALID_TIER}"; errors=$((errors+1)); }
  [ -z "$phase" ] || in_set "$phase" "$VALID_PHASE" || { echo "ERROR $rel: phase '$phase' not in {$VALID_PHASE}"; errors=$((errors+1)); }
  # sub-specialists: ≤5 (parametric focus-modes), officers only
  local specs; specs=$(fm_get "$f" specialists)
  if [ -n "$specs" ]; then
    local n; n=$(printf '%s' "$specs" | tr ',' '\n' | grep -c '[a-zA-Z]')
    [ "$n" -le 5 ] || { echo "ERROR $rel: specialists=$n (max 5 per officer)"; errors=$((errors+1)); }
  fi
  # name pattern (allow {{skill}} templating for role-templates/spokes)
  if [ -n "$name" ] && ! printf '%s' "$name" | grep -qE '^(\{\{skill\}\}-)?[a-z0-9][a-z0-9-]*[a-z0-9]$|\{\{skill\}\}'; then
    echo "WARN $rel: name '$name' not kebab-case"; warns=$((warns+1)); fi
  case " helper assistant agent tool " in *" $name "*) echo "WARN $rel: generic name '$name'"; warns=$((warns+1));; esac

  # body sections
  for sec in "## Mission" "## Scope" "## Acceptance"; do
    grep -qF "$sec" "$f" || { echo "WARN $rel: body missing '$sec'"; warns=$((warns+1)); }
  done
  grep -qiE 'anti-scope' "$f" || { echo "WARN $rel: no anti-scope declared"; warns=$((warns+1)); }
  # evidence tag present
  grep -qE '\[(CODE|CONFIG|DOC|INFERENCE|ASSUMPTION|CÓDIGO|INFERENCIA|SUPUESTO|EXPLICIT)\]' "$f" || { echo "WARN $rel: no evidence tags"; warns=$((warns+1)); }
  # governance — flag AFFIRMATIVE brand/color misuse only (not the rule text that forbids it)
  grep -qiE 'sofka' "$f" && ! grep -qiE 'no sofka|never .*sofka|sin sofka' "$f" && { echo "ERROR $rel: contains 'Sofka' (single-brand MetodologIA)"; errors=$((errors+1)); }
  grep -qiE 'green[ -]?(=|means|for|indicates|signals|to mean)[ -]*(success|ok|pass|done|positive)|✅.*green' "$f" && { echo "WARN $rel: possible green-as-success"; warns=$((warns+1)); }
  # officer thinness
  if [ "$tier" = "officer" ] && [ "$(wc -l <"$f")" -gt 80 ]; then
    echo "WARN $rel: officer body > 80 lines — push logic into a skill (officers are thin)"; warns=$((warns+1)); fi
}

files=()
if [ "${1:-}" = "--all" ]; then
  for f in "$ROOT"/agents/*.md "$ROOT"/agents/sme/*.md "$ROOT"/references/roles/*.md; do
    [ -f "$f" ] || continue; [ "$(basename "$f")" = "README.md" ] && continue; files+=("$f"); done
else
  files=("$@")
fi
[ ${#files[@]} -gt 0 ] || { echo "usage: $0 <agent.md>... | --all"; exit 2; }
for f in "${files[@]}"; do validate "$f"; done

echo "agents=$checked errors=$errors warnings=$warns"
[ "$errors" -eq 0 ]
