<!-- distilled from alfa skills/proceso-seleccion-orchestrator -->
<!-- This skill should be used when the user asks to track a hiring or selection process, extract interview stages from supplied notes or emails, reconcile interviewer roles, build a candidate status board, identify the next action, or audit handoff evidence for an active selection workflow. -->
# Proceso Seleccion Orchestrator

## Purpose

Orchestrate a supplied hiring or selection-process packet into a deterministic status board. Extract only facts present in the provided messages, notes, interview feedback, or manual entries. Track candidate alias, target role, interviewer contacts, process stages, decision risks, evidence references, and exactly one next action. [DOC]

Use the skill for process tracking, not for legal, salary, immigration, background-check, or employment-law advice. Do not infer private facts, interview outcomes, compensation, dates, or commitments that are not present in evidence. [DOC]

### Anti-scope (out of bounds)
- No outcome prediction, candidate ranking, or fit scoring — the board records state, it does not judge. [DOC]
- No network/calendar/ATS/email fetch; the packet is the only world. [CONFIG]
- No date math against the current clock (see Deterministic Contract). [CONFIG]
- No editing of sibling skills or their assets (see Stop Conditions). [DOC]

## Deterministic Contract

Follow `assets/output-contract.json` for the JSON report shape and `templates/output.md` for the human-readable handoff. Use stable ordering:

1. Sort evidence by `received_date`, then `id`.
2. Sort contacts by normalized `name`, then `role`.
3. Sort stages by explicit `sequence`.
4. Keep risk order by severity rank from `assets/risk-policy.json`, then `id`.

Determinism rule: identical input must yield byte-identical output. Every tie has a documented second key above; never leave ordering to dict/insertion order. [INFERENCIA]

All dates must be ISO `YYYY-MM-DD`. If the user provides relative dates such as "tomorrow", "next Tuesday", or "ayer", preserve the text in notes and set a blocker instead of normalizing from the current clock. Do not call calendars, email, web, or network services unless the user separately provides that data in the prompt or workspace. [DOC]

**Edge cases.** Duplicate `received_date` → break by `id`. Missing `sequence` on a stage → `blocked`, not inferred order. Two contacts sharing a normalized name → keep both, disambiguate by `role`. Non-ASCII names sort by their ASCII fold but display verbatim (decision below). [INFERENCIA]

## Required Inputs

- Candidate alias or anonymized identifier.
- Target role or opportunity.
- At least one evidence item from supplied email text, meeting notes, recruiter messages, interview feedback, or manual entry.
- Known stages or enough evidence to derive stages.

When inputs are incomplete, return a blocked report with missing fields. Do not fabricate placeholders such as `TBD` as if they were evidence. [DOC]

## Workflow

1. Inventory all supplied evidence. Assign stable IDs such as `E-001`, `E-002`, and record source type using `assets/evidence-policy.json`.
2. Extract contacts only when a name and role/title are present in the supplied evidence. Preserve original names in display text, but use deterministic ASCII normalization only for sorting.
3. Build stages using `assets/status-policy.json`. Each stage needs `id`, `sequence`, `label`, `owner`, `status`, `status_reason`, and `evidence_ref`.
4. Select exactly one next action. It must point to one existing stage and one existing evidence item.
5. Add risks only when evidence supports them. Use the allowed severities and require mitigation text.
6. Validate the JSON report with `scripts/selection_board_validator.py`.
7. Produce the markdown handoff from `templates/output.md`, including validation status and remaining risks.

## Worked Example (minimal)

Input: alias `Cand-A`, role `Backend Eng`, one recruiter email "screen passed, panel next week".

- `E-001` recruiter_email → contact only if name+role present, else none. [INFERENCIA]
- Stage `S-001` Screen → `passed` `[EXPLICIT]`; `S-002` Panel → `scheduled`? No ISO date in evidence ("next week" is relative) → `blocked`, blocker logged, original text preserved. [INFERENCIA]
- Next action: points at `S-002` + `E-001` ("confirm panel date"). [INFERENCIA]
- Report status `blocked` (relative date present); validator must reject if forced to `complete`. [INFERENCIA]

## Output Rules

- Tag every board claim with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]` (the board's own provenance set; distinct from this doc's authoring tags). [DOC]
- Use `blocked` when evidence is missing, dates are relative, outcomes are promised, or stage status is contradictory.
- Never claim a candidate is hired, rejected, selected, or guaranteed unless the provided evidence explicitly says so.
- Never use the current date to resolve deadlines.
- Never expose raw email bodies in the final board; cite evidence IDs and short summaries.

## Decisions & Trade-offs

- **Display verbatim, sort on ASCII fold.** Preserves name dignity while keeping ordering reproducible across locales; trade-off is that visual order may not match byte order for accented names — acceptable because `id` is the stable tiebreak. [INFERENCIA]
- **Relative dates block rather than normalize.** Avoids silent clock-dependence that would make output non-deterministic and possibly wrong; cost is more `blocked` reports, which is the safe failure direction. [INFERENCIA]
- **Exactly one next action.** Forces a single unambiguous handoff; a list would reopen prioritization the board is meant to close. [SUPUESTO]
- **Offline-only.** No network means no leakage of candidate PII and fully replayable runs; cost is the operator must paste data in. [DOC]

## Failure Modes (and the guard)

- Fabricated contact from a name with no role → guard: rule 2 requires name AND role. [DOC]
- Next action pointing at a non-existent stage/evidence → guard: validator rejects unresolved references. [CÓDIGO]
- Promised-outcome phrasing copied as fact ("they'll hire him") → guard: guaranteed-outcome rejection + `blocked`. [DOC]
- Two stages sharing a `sequence` → guard: validator flags duplicate stages. [CÓDIGO]
- Tag family drift (mixing `[EXPLICIT]` board tags with authoring tags) → guard: board uses only its three-tag set. [INFERENCIA]

## Acceptance Criteria

- Report validates clean via `selection_board_validator.py` (exit 0) before any handoff is shared. [CÓDIGO]
- Every stage has all seven required fields; every next action resolves to one real stage + one real evidence id. [CONFIG]
- Same input twice ⇒ identical bytes (ordering keys honored). [INFERENCIA]
- Zero relative dates in resolved fields; any present ⇒ status `blocked` with the original text retained. [DOC]
- No outcome/compensation/private fact appears unless an evidence id backs it. [DOC]

## Assets

- `assets/manifest.json` lists every deterministic asset.
- `assets/output-contract.json` defines the required report structure.
- `assets/status-policy.json` defines allowed stage statuses and terminal states.
- `assets/evidence-policy.json` defines allowed evidence types and minimum fields.
- `assets/date-policy.json` defines ISO-only date handling and relative-date blockers.
- `assets/risk-policy.json` defines severity ranks and mitigation requirements.

## Scripts

Run local validation before using a report as evidence:

```bash
python3 skills/proceso-seleccion-orchestrator/scripts/selection_board_validator.py --input <report.json>
bash skills/proceso-seleccion-orchestrator/scripts/check.sh
```

The validator is offline, deterministic, and rejects missing evidence, duplicate stages, unsupported statuses, relative dates, guaranteed-outcome language, unresolved evidence references, and missing next actions. A clean exit is necessary but not sufficient — it checks shape and policy, not whether your extraction was faithful to the source. [INFERENCIA]

## Related Skills

- `simulador-entrevista`
- `gratitud-post-proceso`
- `red-y-referencias`

## Stop Conditions

Stop and ask for missing source data when the request requires accessing private mailboxes, live calendars, applicant tracking systems, or external profiles not supplied in the workspace. Stop when a requested change would require employment-law advice or direct modification of another skill. [DOC]
