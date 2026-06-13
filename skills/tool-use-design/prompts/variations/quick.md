# Quick Variation — Tool Use Design

Fast pass for a small surface (2–3 tools) when you need contracts now.

## Do

1. Name the overlap in one line (which two tools confuse the planner).
2. Rewrite each description: purpose · input format · 1 example · reciprocal boundary.
3. If a tool has >1 responsibility, split it (rename, two boundaries).
4. State the repo sequence `Grep → Read → Edit` and the Edit fallback `Read + Write` in one line each.
5. Set flags `offline=true`, `network_required=false`, `deterministic=true`.

## Skip

- Long rationale prose, multi-axis re-architecture, token-budget measurement.

## Gate (minimum)

≥2 contracts with boundary + examples · reciprocal delegation · `grep, read, edit` · Edit fallback documented. Tag claims with one Alfa-core family. [DOC]
