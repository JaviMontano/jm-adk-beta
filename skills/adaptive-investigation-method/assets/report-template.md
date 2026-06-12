# Adaptive Investigation Report — {{goal}}

## Goal
{{goal}}

## Budget
- Total (hard): {{budget.total}} {{budget.unit}}
- Used: {{budget.used}}
- Remaining: {{budget.remaining}}

## Surface map (cheap, zero budget)
{{#surface_map}}
- `{{node}}` — {{region}} (via {{discovered_by}})
{{/surface_map}}

## Ranked hypotheses
{{#hypotheses}}
- {{id}} (rank {{rank}}, {{value_cost}}) -> {{target_nodes}}
{{/hypotheses}}

## Deep-dive log
{{#deep_dives}}
- `{{node}}` -> {{verdict}} — {{evidence}} {{provenance_tag}}
{{/deep_dives}}

## Re-plan log (only on hypothesis_invalidated)
{{#replans}}
- {{invalidated_hypothesis}} invalidated — {{evidence}}
{{/replans}}

## Deliverable
{{deliverable}}

## Stop reason
{{stop_reason}}

---
Single brand: JM Labs. No invented prices. No client PII. Discover-not-mutate.
