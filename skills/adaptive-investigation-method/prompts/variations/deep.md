# Deep Variation — Large Domain, Multi-Hypothesis Investigation

For large domains (thousands of files / a wide corpus) with a moderate budget (e.g. 8–20 reads) and a goal that may require following delegation chains. Maximizes traceability and re-plan discipline.

## Inputs

`goal`, `budget` (8–20), `surface_root`, optional `cheap_tools`. Missing `goal`/`budget` → `{VACIO_CRITICO}`, stop, ask.

## Extended loop

1. **Install hard budget**; typed scratchpad with `plan`, `hypotheses`, `findings`, `replans`, `budget`, `stop_reason`.
2. **Layered cheap map.** Several `Glob` patterns + targeted `Grep -l` for the goal's symbols. Cluster candidate nodes by region (entrypoints, services, libs, tests). Zero budget.
3. **Rank a multi-hypothesis list** by value/cost; each hypothesis points at a region/node and states what evidence confirms vs invalidates it. Tie-break toward cheapest-to-invalidate.
4. **Iterate deep-dives** on top nodes. Each: one `Read`, decrement, finding `{ node, evidence, tag, verdict }`.
5. **Follow delegation chains.** A node that re-exports or calls out partially invalidates "it happens here" → re-plan to the delegate, logged with evidence.
6. **Re-plan only on invalidation.** Confirmed/intact hypotheses keep momentum. Track `replans` count vs deep-dives to detect thrash.
7. **Handle exhaustion.** All hypotheses invalidated with budget left → generate new hypotheses from accumulated findings; if none, close `goal_unresolved` honestly.
8. **Close** on `goal_resolved` or `budget_exhausted`. Synthesize the deliverable from findings; cite each node.

## Output

Full `templates/output.md`: goal, budget (total/used/remaining), layered surface map, ranked hypotheses with verdicts, full deep-dive log, replan log with invalidating evidence, findings (tagged), deliverable, stop reason, coverage statement and residual risks.

## Validation

Before delivery, run the deterministic compiler and the gate:

```bash
python3 scripts/compile-adaptive-investigation.py --input investigation.json --format markdown
bash scripts/check.sh
```

Discover-not-mutate. Every finding node-referenced and provenance-tagged. Partial coverage declared. Single brand (JM Labs); no invented prices; no client PII.
