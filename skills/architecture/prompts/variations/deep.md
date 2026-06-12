# Deep variation — architecture (depth=deep)

Exhaustive path for contested or hard-to-reverse decisions. Apply the whole
playbook and validate each step.

## Run
1. Resolve to one `topic` (ask if ambiguous). Load the one playbook.
2. **Discover** fully: drivers, ranked; constraints; consumers/integrations;
   pre-state baselines (for migration/performance). No unranked driver list.
3. **Analyze** exhaustively:
   - Walk every selector/pattern table in the playbook.
   - For trade-off-analysis: build the weighted matrix (≥3 options, weights sum
     to 1.0, per-cell rationale) and run the ±20% sensitivity check.
   - For system-architecture: write quality-attribute scenarios with measures;
     map each ranked driver to a decision.
   - For event/migration: state delivery semantics / rollback per stage.
4. **Execute**: produce the full deliverable into `templates/output.md`,
   including ADR(s) with context/decision/consequences and rejected options.
5. **Validate each step**: run the guardian gate check-by-check; flag fragile
   winners; supersede stale ADRs rather than editing them.

## Guardrails
Still ONE playbook — depth means thoroughness, not loading more. Every claim
tagged; every `[ASSUMPTION]` verified; no invented prices; no green without the
full gate passing.
