# Assets — station-create

Concrete, validation-grade assets consumed by this skill's gate. Each asset is
registered in `manifest.json` with a `used_by` target that exists.

## Bundle

| Asset | Type | Used by | Purpose |
|---|---|---|---|
| `quality-rubric.json` | rubric (JSON) | `agents/guardian.md` | Scoring thresholds (0/1/2) for the 7 acceptance criteria; pass = all met. |
| `checklist.md` | checklist (Markdown) | `agents/guardian.md` | Human-readable acceptance checklist the guardian walks before emitting a verdict. |

## How they fit

The **guardian** agent reads `checklist.md` to enumerate gate items and scores
each against `quality-rubric.json`. The rubric and checklist mirror the
acceptance gate in `SKILL.md`, so a pass here equals a pass there. Evidence tags
on every item stay within one Alfa-core family. No prices, single-brand
(JM Labs).
