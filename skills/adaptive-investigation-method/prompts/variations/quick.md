# Quick Variation — Bounded Investigation in One Pass

For a small budget (typically 3–5 expensive reads) and a sharp goal. Minimize ceremony; keep every invariant.

## Inputs

`goal`, `budget` (3–5), `surface_root`. Missing `goal` or `budget` → `{VACIO_CRITICO}`, stop.

## One-pass loop

1. **Budget** set in scratchpad. `remaining = total`.
2. **One cheap map**: a single `Glob` + one `Grep` over the most likely region. Candidate nodes only. Zero budget.
3. **Top-1 hypothesis** by value/cost. Name the node that would confirm or refute it.
4. **Deep-dive** that node. Decrement. Record finding + verdict.
5. If **invalidated**, follow the delegation/lead it exposes (one re-plan); else accept the result.
6. **Close** on first `goal_resolved`, else when budget hits zero. Synthesize from findings.

## Output

Short form of `templates/output.md`: goal, budget used/remaining, 1–3 findings (each tagged), deliverable, stop reason. Declare if coverage is partial.

Discover-not-mutate. Provenance tag on every finding. Single brand (JM Labs).
