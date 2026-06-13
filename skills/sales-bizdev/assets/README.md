# Assets — sales-bizdev

Reusable, machine- and human-readable assets that the router and guardian draw on. Each is referenced by `SKILL.md` and/or the skill `README.md` and registered in `manifest.json`.

## Bundle contents

| Asset | Type | Purpose | Used by |
|-------|------|---------|---------|
| `routing-matrix.json` | json | Deterministic deliverable-type → topic mapping + tie-breaks + channel-strip rule. The first artifact the lead consults to avoid wrong-topic and double-load failures. | `SKILL.md`, `README.md` |
| `quality-rubric.json` | json | Scored gate dimensions (blocking + advisory) the guardian applies before handoff. | `SKILL.md` |
| `preflight-checklist.md` | markdown | Human-readable pre-flight checklist mirroring the guardian gate and per-playbook Validation Gates. | `SKILL.md` |

## How to use

1. **Route:** consult `routing-matrix.json` to classify the request to one topic by deliverable type.
2. **Execute:** run the loaded playbook's spine (Discover → Analyze → Execute → Validate).
3. **Gate:** score the draft against `quality-rubric.json` and walk `preflight-checklist.md`; any blocking dimension at 0 fails the deliverable.

## Conventions

- Governance is non-negotiable at every depth: no invented prices (FTE-months + disclaimer), single brand, evidence tags, no client PII.
- These assets describe *how to validate* a deliverable; they never contain client data or prices themselves.
