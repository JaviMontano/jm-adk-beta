# Assets — ux-research

Reusable, machine- and human-readable artifacts that enforce the skill's quality
bar and routing discipline. Referenced by `SKILL.md`, the guardian/support agents,
and the eval suite. [DOC]

## Bundle

| Asset | Type | What it's for | Used by |
|-------|------|---------------|---------|
| `quality-rubric.json` | rubric (JSON) | Universal + route-specific acceptance criteria with severity weights and the `green_as_success_forbidden` flag. Support runs it; guardian scores against it. | `SKILL.md`, `agents/guardian.md`, `agents/support.md` |
| `checklist.md` | checklist (Markdown) | Fast operator route-selection + pre-fielding + gate checklist. The human-readable companion to the rubric. | `agents/support.md`, `agents/guardian.md` |

## How to use
1. **Route selection** — run section A of `checklist.md` to pick exactly one route.
2. **Pre-fielding** — section B confirms the decision, segment, and small-n /
   no-data guards before any study runs.
3. **Gate** — the guardian scores the deliverable against `quality-rubric.json`
   (universal criteria + the block matching the active route) and runs section C.

## Conventions
- Status is never asserted green by default; the rubric enforces
  `pass / conditional / gap / not-verified`. [CONFIG]
- The manifest (`manifest.json`) lists every asset; each `used_by` target is an
  existing file in this skill. [DOC]
