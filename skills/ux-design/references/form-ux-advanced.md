<!-- distilled from alfa skills/form-ux-advanced -->
<!-- > -->
# Form Ux Advanced
> "Method over hacks."
## TL;DR
Audit and improve multi-step forms: stepping, inline validation, smart defaults, draft preservation, and error recovery. Output a prioritized, evidence-tagged plan with deterministic copy. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather form journey context: user goal, step count, field count, required vs optional split, abandonment risks, device mix, and completion constraints (time, auth, payment). [DOC]
- Load reusable assets from `assets/`: `ux-heuristics.json`, `inline-validation-copy.json`, `wizard-progress-template.html`, `error-recovery-checklist.md`.
- If journey context is empty or single-field, stop and request clarification — do not audit a form you cannot model. [INFERENCIA]
### Step 2: Analyze
- Audit friction across steps, required fields, validation timing, smart defaults, progress visibility, back navigation, and recovery after failure.
- Use `scripts/audit-form-ux.py --journey <journey.json>` when the journey is expressible as JSON; otherwise audit manually against `ux-heuristics.json` thresholds. [CONFIG]
### Step 3: Execute
- Produce a prioritized UX improvement plan: friction score, blocking issues, recovery patterns, and deterministic copy recommendations.
- Apply `wizard-progress-template.html` for multi-step progress and `inline-validation-copy.json` for actionable field messages. Never invent copy when a pattern exists. [INFERENCIA]
### Step 4: Validate
- Run `scripts/check.sh` after changing bundled assets, fixtures, or the audit script.
- Verify the journey preserves input, supports back navigation, avoids premature errors, and gives a retry path after submit failure.

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set, one tag per claim)
- [ ] Constitution-compliant
- [ ] Actionable output (every finding maps to a concrete change)
- [ ] `assets/manifest.json` declares every reusable form UX asset
- [ ] `scripts/audit-form-ux.py` flags excessive friction, missing smart defaults, harsh validation timing, and weak recovery
- [ ] Multi-step UX includes progress, back navigation, draft preservation, inline feedback, and post-error recovery

## Acceptance Criteria (measurable)
- Friction score computed from `ux-heuristics.json` thresholds; every step above threshold has a named remediation. [CONFIG]
- Inline validation fires on blur or submit, never on first keystroke of an untouched field. [INFERENCIA]
- Required-field count is justified; each optional field marked optional explicitly (not the inverse). [DOC]
- Back navigation preserves all prior input; no step re-asks answered questions. [INFERENCIA]
- Submit failure returns to the form with input intact, the failing field identified, and a retry affordance. [INFERENCIA]
- Every error message is actionable: states what is wrong AND how to fix it. [DOC]

## Decisions & Trade-offs
- **Inline (on-blur) vs on-submit validation** → default on-blur for correctable fields (email, phone), on-submit for cross-field rules. Trade-off: on-blur catches errors early but can feel naggy; suppress until the field is touched and blurred. [INFERENCIA]
- **Multi-step wizard vs single long form** → wizard when fields > ~7 or steps are logically grouped; reduces perceived effort but adds navigation cost and risks mid-flow abandonment. Single form for short, flat journeys. [SUPUESTO] Verify against abandonment data when available.
- **Smart defaults vs blank fields** → pre-fill only when confidence is high and the value is easy to change; a wrong default the user misses is worse than a blank. Tag auto-filled values so they are auditable. [INFERENCIA]
- **Hard block vs soft warning on validation** → hard block only for data that breaks submission; use soft warnings for suspicious-but-valid input (e.g. unusual but legal formats). [INFERENCIA]

## Worked Example
Journey: 12-field checkout, single page, validation on every keystroke, no progress, submit failure wipes the form. [SUPUESTO]
Audit output:
1. Split into 3 steps (contact / shipping / payment); add `wizard-progress-template.html`. Friction: high → medium. [INFERENCIA]
2. Move validation to on-blur; pull messages from `inline-validation-copy.json`. [CONFIG]
3. Default country/region from locale; mark auto-filled. [INFERENCIA]
4. On submit failure, re-render with input intact + inline error on the failing field + retry button (per `error-recovery-checklist.md`). [DOC]

## Usage

Example invocations:

- "/form-ux-advanced" — Run the full form ux advanced workflow
- "form ux advanced on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/audit-form-ux.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill form-ux-advanced`
- Default behavior: render a Markdown audit to stdout; write files only with `--output`.
- Safety boundary: invalid journeys fail nonzero instead of producing incomplete UX advice. [DOC]

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/ux-heuristics.json` defines scoring thresholds and required journey capabilities.
- `assets/inline-validation-copy.json` provides deterministic copy patterns by validation problem.
- `assets/wizard-progress-template.html` provides accessible progress markup.
- `assets/error-recovery-checklist.md` provides the recovery baseline for failed submissions.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Anti-scope: does not perform live A/B testing, write production form code, or measure real abandonment — it audits and recommends. [INFERENCIA]
- Copy recommendations are English baselines; localization and legal/consent wording are out of scope. [SUPUESTO]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Journey not expressible as JSON | Audit manually against `ux-heuristics.json`; skip the script |
| Single-step / single-field form | Skip wizard patterns; audit validation + defaults only |
| Async/server-side validation | Treat as on-submit; require loading state + timeout recovery path |
| Conditional/branching fields | Validate per visible branch; never error on hidden fields |
| Required field with no smart default | Leave blank; do not fabricate a default to satisfy pre-fill [INFERENCIA] |
| Submit succeeds but partial save fails | Surface partial state; offer resume, not silent loss [INFERENCIA] |
