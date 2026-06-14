# iikit Assets Bundle

Reusable, machine- and human-checkable artifacts that back the iikit router's
validation flow. Indexed by `manifest.json`.

## Contents

- **quality-rubric.json** — eight pass/fail criteria (QR-01…QR-08) spanning
  routing, dependency, determinism, integrity, evidence, hygiene, and handoff.
  The **guardian** agent scores an invocation against it; `SKILL.md` points to it
  from the validation gate.
- **checklist.md** — a Resolve → Depend → Execute → Validate checklist for a
  human or agent to run before declaring done. Referenced by `README.md` and the
  `prompts/meta.md` self-check.

## How it is used

The guardian maps each rubric criterion to the resolved stage's acceptance
criteria and reports `dod=pass` only when every criterion holds. The checklist is
the lightweight, prose form of the same gate for quick passes. Both carry the IIK
evidence taxonomy (`[EXPLICIT] [DOC] [CONFIG] [INFERENCE] [ASSUMPTION]`), one
family per artifact.

## Adding an asset

Add the file under `assets/`, then register it in `manifest.json` with `path`,
`type`, `purpose`, and a `used_by` list whose every entry is an existing file in
this skill.
