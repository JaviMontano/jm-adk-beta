# Assets — docs-writing

Supporting assets the skill consumes during routing and validation. Each is registered
in `manifest.json` with the existing file that uses it. [CONFIG]

## Bundle contents

- **`quality-rubric.json`** — the acceptance rubric the guardian applies before a
  deliverable is declared done. Five blocker dimensions (routing integrity, spine
  completion, evidence taxonomy, route acceptance, governance) plus one major dimension
  (actionability). Referenced by `SKILL.md`, `agents/guardian.md`, and
  `templates/output.md`. [DOC]

- **`checklist.md`** — the per-invocation checklist covering routing, the
  Discover → Analyze → Execute → Validate spine, and the done gate. Referenced by
  `README.md` and `agents/lead.md`. [DOC]

## How they are used

The lead runs `checklist.md` to keep the one-route rule and the spine honest; the
guardian scores the draft against `quality-rubric.json` and returns PASS or BLOCK. The
output template embeds the rubric's gate as its Validate table. [INFERENCIA]

## Manifest contract

`manifest.json` lists every asset with `path`, `type`, `purpose`, and a `used_by` array.
Every `used_by` target is an existing file in this skill. Keep the manifest in sync when
adding or removing an asset. [CONFIG]
