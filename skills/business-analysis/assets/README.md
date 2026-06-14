# Assets — business-analysis

Operational assets that gate and shape this skill's deliverables. They are consumed by the
router (`SKILL.md`), the guardian agent, and the prompts — not user-facing prose.

## Bundle

| Asset | Type | Purpose | Consumed by |
|-------|------|---------|-------------|
| `quality-rubric.json` | machine-readable rubric | Universal + per-topic pass/partial/fail criteria the guardian scores against | `SKILL.md`, `agents/guardian.md`, `templates/output.md` |
| `checklist.md` | human-readable gate | The acceptance checklist the lead runs before declaring done | `SKILL.md`, `prompts/primary.md`, `prompts/variations/deep.md` |

## How they fit together
- `quality-rubric.json` is the source of truth for *what passes*. Its `universal` block
  applies to every topic; `topic_specific` adds the discipline's own bars (resolved BPMN
  gateways, reconciled integration matrix, no-orphan traceability, feasibility decision
  rule, locked scenario weights, first-≤3 ADKAR barrier).
- `checklist.md` is the *operational* form of the same gate — a fast box-by-box pass the
  lead and guardian run before ship.

Keep both in sync with the acceptance section of `SKILL.md`. If a playbook's quality
criteria change, update the rubric's `topic_specific` entry and the checklist together.
The `manifest.json` next to this README declares each asset and the existing files that
use it; every `used_by` target must exist.
