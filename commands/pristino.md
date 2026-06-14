---
name: pristino
description: "Dispatcher: /pristino <skill> [topic=...] [depth=quick|deep] [args...]. Routes any catalog skill."
argument-hint: "<skill> [params]"
---
# /pristino — dispatcher

Single entry point replacing alfa's 215+ per-skill command stubs. [DOC]

## Flow
1. Parse `$ARGUMENTS`: first token = skill id (resolve aliases via `catalog/skills.json.aliases`). Remaining = `key=value` flags + positional args.
2. Unknown id → fuzzy-match tier-0 index, propose top 3 by score, ask. Never auto-pick. [INFERENCE]
3. Read `skills/<id>/SKILL.md`. Router resolves `topic` from flags first, else request context; load exactly ONE playbook (`depth=deep` may chain a second). [DOC]
4. Execute under constitution enforcement; honor the skill's `allowed-tools`; report in compressed register. [EXPLICIT]

## Defaults & limits
- `depth` absent → `quick` (one playbook, no chaining). [ASSUMPTION]
- Routes catalog skills only — does NOT invent skills, edit the catalog, or bypass `allowed-tools`. [EXPLICIT]
- Empty/missing first token → list tier-0 index, do not guess. Ambiguous alias (≥2 exact hits) → ask. [EXPLICIT]

## Acceptance
- Resolved id maps to a real `skills/<id>/SKILL.md`; topic bound before execution; single brand per run; output in compressed register with evidence tags preserved. [EXPLICIT]
