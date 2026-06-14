# Assets — market-intel

Supporting assets for the router's validation and routing discipline. Declared
in `manifest.json`; each asset's `used_by` points to a real file in this skill.

## Bundle

| Asset | Type | Used by | What it does |
|---|---|---|---|
| `quality-rubric.json` | JSON | `agents/guardian.md`, `SKILL.md` | Scored rubric (0/1/2) with gate dimensions — routing integrity, single-family evidence, sourcing discipline, no-invented-price, single-brand/no-PII, playbook acceptance. The guardian gate fails unless every gate dimension scores 2. |
| `routing-checklist.md` | Markdown | `agents/lead.md`, `agents/guardian.md` | Resolve-the-topic checklist enforcing one enum value → one playbook, ask-only-when-ambiguous, and the anti-pattern guard against loading two playbooks. |

## How they're consumed

1. **Lead** runs `routing-checklist.md` to pick exactly one topic and commit one
   playbook from `routes.json`.
2. **Guardian** scores the staged deliverable against `quality-rubric.json` and
   re-checks `routing-checklist.md`'s guard section; `gate=pass` requires every
   gate dimension = 2.

Both assets are governance-bound: no invented prices, single brand per artifact,
no client PII, never green-as-success.
