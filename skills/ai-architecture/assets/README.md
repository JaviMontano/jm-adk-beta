# Assets — ai-architecture

Deterministic routing aids for the ai-architecture router. They make topic
selection and the validation gate repeatable across invocations. [CONFIG]

## Bundle
- **`routing-rubric.json`** — machine-readable intent→topic map, tie-breaker rules,
  the validation gate, and governance flags. Used by the lead/support agents and
  referenced from SKILL.md to keep routing deterministic. [CONFIG]
- **`routing-checklist.md`** — the pre-handoff gate as a human-runnable checklist
  (resolve → dispatch → validate → govern). Referenced by README.md and the
  guardian agent. [DOC]
- **`manifest.json`** — declares each asset, its type, purpose, and which existing
  files use it.

## Conventions
- Evidence tags are Alfa core only: `[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]`
  `[SUPUESTO]`. [CONFIG]
- No prices, no client PII, single brand. [SUPUESTO]
