# firebase — assets bundle

Reusable artifacts the firebase skill applies to enforce its Definition of Done.
Every asset here is referenced by an existing file via `manifest.json`.

## Contents
- **`quality-rubric.json`** — the machine-readable quality gates (single-route,
  deny-by-default rules, composite indexes, idempotent triggers, tested-before-deploy,
  no-prices, single-brand, evidence-tagged). Consumed by `prompts/primary.md`,
  `agents/guardian.md`, and exercised by `evals/evals.json`.
- **`checklist.md`** — the human-readable pre-deploy checklist that mirrors the rubric,
  grouped by routing, Firestore/Rules, Functions, test/deploy, and cost/governance.
  Referenced by `README.md` and `agents/guardian.md`.
- **`manifest.json`** — declares each asset's path, type, purpose, and `used_by` targets.

## How to use
Before declaring any firebase deliverable done, the guardian agent runs the
`checklist.md` items and confirms each `quality-rubric.json` gate passes with cited
evidence. The rubric and checklist stay in lock-step — update both together.
