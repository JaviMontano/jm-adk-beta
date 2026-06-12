# Assets — claude-md-architecture

This bundle holds the declarative, ontology-first inputs and the quality rubric that
the skill uses to design and validate a hierarchical `CLAUDE.md` memory.

## Contents

- **`quality-rubric.json`** — the eight pass/fail criteria the guardian applies
  before a split is marked ready (scope separation, cacheable prefix, recursive
  globs, precedence, user-scope isolation, import DAG, upgrade safety, functional
  gate). Consumed by `SKILL.md` (acceptance gate) and `agents/guardian.md`.
- **`manifest.json`** — machine-readable index of this bundle. Each entry names the
  asset, its type, purpose, and the existing skill files that use it.

## How it is used

1. The skill declares the target architecture **before** writing any `CLAUDE.md`
   (ontology-first). The intended companions `architecture-schema.json` (shape) and
   `architecture-policy.json` (rules) are referenced in `SKILL.md`; the rubric here
   is the validation contract those declarations are checked against.
2. `agents/guardian.md` walks `quality-rubric.json` criterion by criterion and
   requires functional evidence per the skill's evidence taxonomy
   (`[DOC] [CONFIG] [CÓDIGO] [INFERENCIA] [SUPUESTO]`).

Single-brand (JM Labs); no client PII; no invented prices; never green-as-success.
