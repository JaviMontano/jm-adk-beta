---
name: iikit
description: "Spec-driven pipeline: /iikit <constitution|specify|plan|checklist|testify|tasks|analyze|implement|taskstoissues|bugfix|clarify> [args]"
argument-hint: "<phase> [args]"
---
# /iikit

Phase wrapper over `skills/iikit` router; phase = topic. [DOC]

**Gates** (block, never auto-skip): [DOC]
- Artifact existence via `scripts/check-prerequisites.sh` — phase fails fast if upstream artifact missing. [CODE]
- Constitution enforced from `plan` onward (not on `constitution`/`specify`). [INFERENCE]
- Hard checklist gate before `implement`: unresolved items report BLOCKED; 100% or ask user (no CLI force flag). [DOC]

**Re-run semantics** (idempotent): semantic diff vs prior artifact — preserve `[x]` done-markers, surface downstream impact, require explicit overwrite confirm. [DOC]

**Contract:** unknown phase → list valid phases, exit non-zero, no writes. [ASSUMPTION] Missing `[args]` defers to router defaults. [ASSUMPTION] Each phase writes one artifact; gate failures are non-destructive (no partial writes). [INFERENCE]

**Anti-scope:** does not bypass gates, edit constitution, or run phases out of dependency order. [ASSUMPTION]
