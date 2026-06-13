# Quick Variation — testing-qa

`depth=quick`: the essentials path most requests need. One discipline, fast.

## Use when
The request names a single test type or a focused gate, and the caller wants the
core deliverable, not an exhaustive pass.

## Procedure
1. Route to one `topic` (apply disambiguation; ask only on a true two-enum tie).
2. Read that ONE playbook.
3. Run the spine at essentials depth:
   - **Discover** — confirm the target and the single risk that matters.
   - **Analyze** — pick the runner/level/budget; skip exhaustive enumeration.
   - **Execute** — the minimal viable artifact (e.g. coverage gate config, the
     critical-path e2e spec, the Lighthouse budget block).
   - **Validate** — run the one decisive check (diff coverage, 3-engine run,
     budget assertion) and read its output.
4. Emit via `templates/output.md`, evidence-tagged.

## Guardrails
Still Read exactly one playbook; still run Validate with real output; still no
green-as-success. Quick trims breadth, not the gate.
