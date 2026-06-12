# Meta Prompt — Tuning the Adaptive Investigation Loop

Use this to configure or self-audit an adaptive-investigation run before or during execution. It governs *how* the loop is parameterized, not the investigation itself.

## Calibrate the budget

- Set `budget.total` from the cost ceiling (latency, tokens, tool calls), not from domain size. A larger domain does not raise the budget; it lowers expected coverage — which you declare.
- Rule of thumb: budget ≈ the number of nodes you can afford to read fully. If that number is the whole domain, the method is the wrong tool (read it whole instead).

## Calibrate the map

- Map breadth should exceed budget by a wide margin (you map far more than you read). If map size ≈ budget, the map is too narrow — broaden `Glob`/`Grep` patterns.
- Keep the map structural: names, paths, entrypoints, imports, symbol hits. Never pull bodies into the map.

## Calibrate the ranking

- Rank by expected value / cost. Tie-break toward the hypothesis **cheapest to invalidate** (most information per budget unit).
- If two hypotheses stay tied every turn, the ranking lacks a discriminator — add one (recency, centrality, delegation depth).

## Calibrate the re-plan trigger

- The only legal trigger is `hypothesis_invalidated`. Audit: count `replans` vs deep-dives. If `replans ≈ deep-dives`, you are re-planning reflexively — tighten the invalidation test.
- A "nearly refuted" hypothesis survives one extra turn by design; that is acceptable, not a bug.

## Self-audit questions (run before delivery)

1. Was the budget fixed and visible **before** the first deep-dive?
2. Did mapping spend any budget? (It must not.)
3. Is every deep-dive backed by a ranked hypothesis?
4. Did every re-plan cite an invalidated hypothesis?
5. Is the deliverable reconstructable from `findings` alone?
6. Is `stop_reason` set, and is partial coverage declared if budget ran out?

Tag every audit answer with provenance. Single brand (JM Labs); no invented prices.
