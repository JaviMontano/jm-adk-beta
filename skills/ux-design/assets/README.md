# Assets — ux-design

Operational assets the ux-design router consumes at run time. These are not
deliverables; they are the machinery that enforces correct routing and the
validation gate.

## Contents

| Asset | Type | Consumed by | What it does |
|-------|------|-------------|--------------|
| `quality-rubric.json` | rubric | `agents/guardian.md`, `SKILL.md` | Weighted scoring the guardian applies before marking a deliverable done. `fail_if_zero` dimensions (single-playbook, shape match, color/contrast, evidence tags, governance) hard-block; PASS needs >= 80% of max weighted score. |
| `routing-checklist.md` | checklist | `agents/lead.md`, `prompts/primary.md`, `SKILL.md` | Top-to-bottom gate the lead runs: resolve topic -> load exactly one playbook -> discover -> execute + tag -> deterministic checks -> gate. |

## Usage

- The **lead** agent walks `routing-checklist.md` to drive a request from
  resolution to gate.
- The **guardian** agent scores the assembled deliverable against
  `quality-rubric.json`; a `fail_if_zero` dimension at 0 blocks the output.
- The **deterministic checks** referenced in both assets (hex-literal grep,
  success-yellow, WCAG AA contrast) are the cheap, repeatable checks support runs
  whenever the artifact is concrete.

## Conventions

- Validator green means `dod=pass`, never a quality verdict. Green is not success.
- Success state color is yellow `#FFD700`, never green; green is decorative
  chart-only.
- Keep these assets lean — they are gates, not documentation.
