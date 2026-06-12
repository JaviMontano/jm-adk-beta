# testing-qa — Assets Bundle

Operational assets the skill and its guardian run a deliverable against. These are
the machine- and human-checkable gates for the testing-qa router — not reference
prose (that lives under `references/`).

## Contents
- **quality-rubric.json** — the weighted gate rubric the Guardian scores against
  (routing, scope, spine, evidence, governance), with explicit `fail_conditions`
  and the `pass | fail | not-verified` status vocabulary. Consumed by
  `agents/guardian.md` and surfaced in `templates/output.md`'s Validate section.
- **checklist.md** — the fast routing-and-gate checklist run before declaring a
  deliverable done; mirrors the spine in `SKILL.md` and `prompts/primary.md`.

## How to use
1. While routing, run `checklist.md` to confirm exactly one playbook and a
   concrete target.
2. After the Validate step, the Guardian scores the deliverable against
   `quality-rubric.json`; any `fail_condition` blocks "done".
3. Both assets are version-pinned to the skill (`quality-rubric.json.version`)
   so a drift in gates is visible in diffs.

See `manifest.json` for the machine-readable index and `used_by` wiring.
