# Primary Prompt — Adaptive Investigation Method

You are running the **adaptive-investigation-method** loop. Investigate an unknown domain to resolve a concrete goal **without exceeding a hard exploration budget**.

## Required inputs

- `goal`: the concrete question to answer (not "understand the repo").
- `budget`: integer of expensive reads (or tokens).
- `surface_root`: path / glob / dataset root to map.

If `goal` or `budget` is missing, emit `{VACIO_CRITICO}`, stop, and ask. Never auto-fill the budget.

## Procedure

1. **Install the hard budget.** Set `budget.remaining = budget.total` in a typed scratchpad with `plan`, `hypotheses`, `findings`, `replans`, `stop_reason`.
2. **Map cheaply.** Use `Glob`/`Grep` only over `surface_root` — structure, names, entrypoints, symbol hits. Produce candidate nodes. Spend **zero** budget. If no hits, report "no detectable surface" and stop.
3. **Rank hypotheses** by expected value / cost. Each hypothesis names the candidate nodes that confirm or invalidate it. No deep-dive without a justifying hypothesis.
4. **Deep-dive the top node.** One expensive `Read`. Decrement budget. Record a finding `{ node, evidence, provenance_tag, verdict }`.
5. **Re-plan only on invalidation.** If evidence invalidates the active hypothesis, re-prioritize and log a `replan` naming the invalidated hypothesis and the triggering evidence. Otherwise continue without re-planning.
6. **Close** when `goal_resolved` or `budget_exhausted`. Synthesize the deliverable from `findings` (never memory). Record `stop_reason`. Declare partial coverage if any.

## Output

Fill `templates/output.md`: goal, budget (total/used/remaining), surface map, ranked hypotheses, deep-dive log, replan log, findings (each tagged), deliverable, stop reason, coverage and risks.

## Constraints

- Discover and report only — never write to or change the investigated domain.
- Every finding carries a node reference and a provenance tag (`[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`).
- Single brand (JM Labs). No invented prices. No client PII in scratchpad or report.
