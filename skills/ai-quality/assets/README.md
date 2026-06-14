# Assets — ai-quality

Deterministic, machine-readable assets that back the `ai-quality` router. They
are the source of truth for *how to route* and *how to gate*; when this bundle
and prose disagree, the asset wins. [CONFIG]

## Files

- **`manifest.json`** — the asset index the validator reads: each asset's path,
  type, purpose, and which in-repo file consumes it. [CÓDIGO]
- **`routing-matrix.json`** — the canonical topic → playbook map, intent and
  anti-scope per topic, the disambiguation rules for known collisions, and the
  router invariants (one playbook, one tag family, offline determinism,
  green ≠ safe). Consumed by `SKILL.md` (routing) and the lead/specialist
  agents. [CÓDIGO]
- **`quality-rubric.json`** — the guardian's scoring rubric: router-level
  blocking criteria (RQ-1…RQ-6), per-topic gate pointers, and the anti-patterns
  that force a `block` verdict. Consumed by `agents/guardian.md`. [CÓDIGO]

## How to use

1. Resolve `topic` using `routing-matrix.json` (intent + disambiguation rules),
   never by free association. [CÓDIGO]
2. Execute the one playbook the matrix points to.
3. Before "done", score the run against `quality-rubric.json`; any failed
   blocking criterion → `block`. [DOC]

## Determinism note
These are static JSON contracts. Editing one changes accepted router behavior and
must be versioned deliberately — do not inline a one-off rule that bypasses the
matrix or rubric. A passing rubric means a *well-formed* run, not a guarantee
that the underlying model or system is safe or correct. [INFERENCIA]
