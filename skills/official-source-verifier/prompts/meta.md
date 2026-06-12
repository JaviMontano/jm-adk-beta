# Meta Prompt — Tuning the Official Source Verifier

Use this to adapt the verifier to a specific decision context without weakening the
authority discipline.

## Calibrate before running

- **Scope check**: Does the `question` truly depend on an external document? If it is a
  local-code fact (checkable with Read/Grep/Glob) or a design opinion, decline — the
  guardian adds no value and the skill should not activate.
- **Authority surface**: Which producer owns the affected product? Identify the canonical
  doc set (ADK reference, Agent Skills spec, GitHub/Git manual, the SDK/API's own
  reference) before searching, so secondary results are not mistaken for authority.
- **Version anchor**: Capture `repo_version` first. Currency failures are the most common
  silent error — a correct doc for the wrong major is `unverified`.

## Knobs

- **Corroboration depth**: for high-impact decisions, require a second official source
  before `change_authorized=true`. For low-impact, one official source may suffice — but
  never zero.
- **Conflict posture**: when official sources disagree, default to recording a
  `blocking_gap`. Only override toward the spec when SKILL.md step 6 applies, and record
  the rationale.
- **Output mode**: JSON for machine contracts (run the validator); readable table for
  human consumers.

## Failure modes to pre-empt

- Treating a secondary source as authority because it agrees with the official one.
- Asserting a doc's stance without `WebFetch` of the text.
- Omitting `accessed_date` "because the URL is enough".
- Marking `pass` with open gaps under deadline pressure.

## Self-audit before delivery

Run the `assets/verification-checklist.md` items and the `assets/quality-rubric.json`
scoring. If any blocking criterion fails, return the report for correction — do not
deliver.
