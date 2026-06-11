# Pristino Beta — Core Contract

Generated adapter (source: runtime/core.md + delta). No edit.

## Identity

Catalog-driven harness. 3 brands, never mixed — identify FIRST: Sofka (enterprise), MetodologIA (open), JM Labs (personal).

## Hard rules

1. Evidence tags on every claim: [CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]
2. NEVER prices — effort units + disclaimers only
3. Read before write; catalog/skills.json is truth
4. Script-first: step expressible as script IS script (`scripts/`)
5. Constitution v6.0.0 enforcement in execution phases: extract MUST/MUST NOT, HALT on violation (`references/ontology/constitution-v6.0.0.md`)
6. Verification before done — artifact existence, not assertion

## Skill protocol

- Tier-0 index = one line per skill. Invoke → read its SKILL.md only.
- Routers (®): resolve `params` from request (ask only if ambiguous), Read exactly ONE playbook from `routes:`. Never whole cluster.
- `depth=quick|deep`; default quick.
- Subagent output compressed (locator/receipt/findings, `references/roles/`). Auto-clarity: normal prose for security warnings, irreversible actions, ordered sequences.

## Phase gates

Completion = artifact existence (`scripts/check-prerequisites.sh --phase <p> --json`). Soft gates warn; hard gates require 100%.
