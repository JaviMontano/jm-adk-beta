# Assets — google-workspace

Deterministic, offline assets that back the router's quality and routing gates.
None of these call Google, OAuth, HTTP, or MCP. [CODE]

## Files

- **`quality-rubric.json`** — the scored acceptance gate for a routing decision
  and offline plan: topic correctness, single-route, least-privilege scope,
  mutation safety, secrets policy, error taxonomy, evidence tags, no-invention.
  Consumed by `prompts/meta.md` (self-evaluation rubric). [CODE]
- **`routing-checklist.md`** — the step-by-step resolve → load → plan → gate
  checklist run on every invocation. Referenced by `prompts/meta.md` improvement
  loop and aligned with the `SKILL.md` acceptance gate. [DOC]
- **`manifest.json`** — the asset inventory consumed by the DoD validator;
  declares each asset's type, purpose, and `used_by` targets. [CODE]

## Usage

The lead/guardian agents apply `routing-checklist.md` during the flow and score
the result with `quality-rubric.json` before declaring "done". Both are stable
policy inputs — edit them, not the prose, when the routing or gate rules change. [DOC]
