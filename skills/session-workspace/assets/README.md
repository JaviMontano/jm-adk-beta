# Assets — session-workspace

Deterministic resources that make router dispatch decisions checkable rather than
vibes-based. Both assets are consumed by the skill itself, not shipped to a
client.

## Bundle

- **`quality-rubric.json`** — scorable criteria for a dispatch decision. Eight
  mandatory criteria (single-route, topic-resolved, depth-honored,
  intent-not-keyword, write-boundary, evidence-tags, governance, guardian-emitted)
  plus two advisory. A dispatch passes only when every mandatory criterion is met;
  green is never the default. Used by `SKILL.md` (acceptance criteria) and
  `agents/guardian.md` (the validation gate).

- **`dispatch-checklist.md`** — the operational box-by-box gate the router walks
  before declaring done, mirroring `templates/output.md`'s Guardian section. Used
  by `SKILL.md` and the guardian/lead agents.

## Conventions

- Evidence tags are the Alfa core set: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
  `[ASSUMPTION]` `[OPEN]`. One family, one tag per claim.
- Assets are the source of truth for *how a dispatch is scored*; prose in agents
  or prompts that disagrees with an asset is the defect.
- See `manifest.json` for the machine-readable index and `used_by` wiring.
