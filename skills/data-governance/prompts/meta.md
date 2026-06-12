# Meta prompt — reasoning policy for data-governance

How to think while running this router. This guides the orchestration, not the
deliverable itself.

## Routing discipline
- The single-playbook rule is the whole point. Resist "read two to be safe" — that
  is a defect, not diligence. Commit to one topic and justify the choice in one line.
- Distinguish *governing* data from *building* it: ETL authoring and physical
  schema tuning are out of scope — redirect rather than improvise.

## Confidence & questions
- Score topic-match confidence. If two topics are within a hair, ask exactly one
  question; otherwise pick the more specific and state the tie-break.
- Treat a missing required input (inventory, schema access, regulatory regime) as a
  hard stop with a `[SUPUESTO]` blocker. Never infer architecture from caches,
  history, or column names alone.

## Evidence reflex
- Tag each non-obvious claim as you write it, one tag per claim. An untagged output
  is a bypassed run (G3).
- Every `[SUPUESTO]`/`[ASSUMPTION]` must name how to verify it.

## Self-check before emitting
1. Did I load exactly one playbook?
2. Does the output answer the resolved topic, not the router?
3. Are the topic's own quality criteria met (privacy re-ID test, audit chain
   verifiability, doc drift = 0, gate confidence ≥ 0.95, etc.)?
4. Prices invented? PII leaked? Brands mixed? If yes to any — fix before done.

## Failure recovery
If validation fails, surface the specific unmet criterion and stop. Do not
auto-advance past an unmet gate.
