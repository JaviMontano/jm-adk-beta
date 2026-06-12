# Assets — architecture

Supporting assets for the architecture router skill. Each is registered in
`manifest.json` with a `used_by` pointer to the file that consumes it. [DOC]

## Bundle

- **quality-rubric.json** — the machine-readable acceptance gate. Eight gates
  (single route, evidence tags, assumption pairing, trade-off honesty,
  measurable scenarios, no invented prices, no placeholder fields, depth
  honesty). The **guardian** agent and `templates/output.md` section 8 mirror
  it. Referenced from `SKILL.md`. Never green-as-success: any false gate fails.
- **routing-checklist.md** — pre-flight checklist used by `prompts/primary.md`
  and the README to resolve exactly one `topic` and avoid common mis-routes
  (e.g. contract shape → api-design, not system-architecture) before a playbook
  is loaded.

## Conventions
- Evidence tags use the Alfa-core family: `[DOC]` `[CONFIG]` `[CODE]`
  `[INFERENCE]` `[ASSUMPTION]`. One family, one spelling. [DOC]
- No invented prices anywhere; cost is FTE-months only. [DOC]
