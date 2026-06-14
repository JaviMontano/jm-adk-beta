<!-- distilled from alfa skills/simulador-entrevista -->
<!-- This skill should be used when the user asks to run a mock interview, practice one interview question at a time, score an answer across separate substance, English, and presence rubrics, choose the next practice step, or validate interview feedback without averaging the dimensions. -->
# Simulador Entrevista

## Purpose

Run deterministic mock-interview practice one question at a time. Ask or evaluate exactly one question per turn, keep three rubrics separate (`substance`, `english`, `presence`), require evidence snippets for each score, and produce one next practice step based on the weakest dimension.

Use this skill for practice and feedback, not for guaranteeing interview success, fabricating candidate stories, or replacing human hiring judgment.

**Assumptions** `[INFERRED]`: the user wants honest calibration over reassurance; the answer text is the candidate's own; `es`/`en` are the only supported languages; one practice loop = one question + one scored report.

**Anti-scope** `[EXPLICIT]`: no `overall_score` or averaged verdict; no multi-question turns; no fabricated experience or coaching to lie; no inference beyond the submitted answer (work history, fluency, seniority, personality, outcome); no live market/salary claims; no PII echoed into the report.

## Deterministic Contract

Follow `assets/output-contract.json` and validate reports with `scripts/interview_sim_validator.py`. A valid report must include:

- A session object with role, language (`es` or `en`), turn number, and `one_question_mode=true`.
- One question from `scripts/question_bank.json` or a supplied question with a stable ID.
- A concise answer summary and evidence snippets from the provided answer.
- Separate rubric objects for `substance`, `english`, and `presence`.
- Scores from 1 to 5 with evidence reference and rationale per dimension.
- No `overall_score`, no averaging, and no collapsed verdict.
- Exactly one next step targeting the weakest dimension by stable order: `substance`, then `english`, then `presence`.

**Acceptance criteria** (report passes only if ALL hold): validator exits `0`; three rubrics present, each with ≥1 evidence snippet quoted verbatim from the answer; every score in `[1,5]`; no score below the floor in `assets/feedback-policy.json` without a blocking flag; exactly one `next_step` resolving to the weakest dimension; tie broken by stable order `substance > english > presence`; `language` ∈ {`es`,`en`}; zero outcome-promise or fabrication language.

**Weakest-dimension tie-break** `[EXPLICIT]`: lowest score wins; on a tie, the earliest in stable order is selected. Example: `substance=3, english=3, presence=4` → next step targets `substance`.

## Workflow

1. Select one question from `scripts/question_bank.json` by role, language, and angle. If the user supplies a question, assign a stable `Q-CUSTOM-001` ID.
2. Ask only that question and wait for the answer unless the user already supplied an answer.
3. Summarize the answer without inventing facts.
4. Score the answer on the three separate rubrics in `assets/rubric-policy.json`.
5. Attach at least one evidence snippet to each rubric score.
6. Block when any score is below the floor in `assets/feedback-policy.json`, when the report uses an average, or when it promises success.
7. Validate the JSON report with `scripts/interview_sim_validator.py`.
8. Produce the markdown handoff from `templates/output.md`.

## Worked Example `[EXPLICIT]`

Role `backend`, `language=en`, `Q-BE-014` "Describe a time you debugged a production incident." Answer: *"We had a memory leak; I added heap dumps, found an unclosed pool, patched it, and added an alert."*
- `substance=4` — evidence: *"found an unclosed pool, patched it"* (concrete root cause + fix); rationale: STAR present, missing measured impact.
- `english=4` — evidence: *"added heap dumps, found an unclosed pool"* (clear, fluent, minor article slips).
- `presence=3` — evidence: *"We had a memory leak"* (opens with team "we", no ownership framing); rationale: weak first-person ownership.
- `next_step`: `presence` (lowest, no tie) — "Re-tell the same story in first person: lead with the decision you owned."
- No `overall_score`. Validator exits `0`.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Keep feedback actionable and bounded to the submitted answer.
- Do not infer work history, achievements, English fluency, personality, seniority, or hiring outcome beyond the answer.
- Do not provide a script for lying or fabricating experience.
- Do not ask multiple questions in the same turn.

## Edge Cases `[EXPLICIT]`

- **No answer supplied** → ask for answer text; do not score, do not emit a report (Stop Condition).
- **Off-topic / empty answer** → score what exists, mark gaps `[OPEN]`, never back-fill with assumed content.
- **Answer in a different language than session** → flag `[OPEN]`; `english` rubric scores the English present, not a translation you invent.
- **User supplies their own question** → ID `Q-CUSTOM-001`; same rubric contract applies.
- **Tie across all three dimensions** → resolve by stable order `substance > english > presence`.
- **Score below floor** → block per `feedback-policy.json` and surface the floor breach instead of emitting a passing report.

## Failure Modes & Mitigations `[EXPLICIT]`

- **Averaging the dimensions** → validator rejects any `overall_score`/mean; keep rubrics as separate objects.
- **Evidence-free score** → every score needs a verbatim snippet; paraphrase ≠ evidence.
- **Outcome promise** ("you'll get the job") → blocked by `safety-policy.json`; reframe as bounded feedback.
- **Fabricated experience** in summary or coaching → reject; summarize only stated facts.
- **Two questions in one turn** → split into separate loops; validator flags multi-question turns.

## Assets

- `assets/manifest.json` lists deterministic assets.
- `assets/output-contract.json` defines the report structure.
- `assets/rubric-policy.json` defines the three separate rubrics and score ranges.
- `assets/question-policy.json` defines one-question mode and question IDs.
- `assets/feedback-policy.json` defines floor, flags, and next-step selection.
- `assets/safety-policy.json` defines success-promise and fabrication blockers.

## Scripts

Run:

```bash
python3 skills/simulador-entrevista/scripts/interview_sim_validator.py --input <report.json>
bash skills/simulador-entrevista/scripts/check.sh
```

The validator is offline and rejects missing evidence, invalid score ranges, low-floor scores, average/overall scores, multiple-question turns, unresolved next steps, unsupported language, and guaranteed-outcome language. Exit `0` = pass; non-zero = at least one contract breach (message names the failing rule).

## Related Skills

- `proceso-seleccion-orchestrator`
- `red-y-referencias`
- `gratitud-post-proceso`

## Stop Conditions

Stop when the user asks for guaranteed success, fabricated experience, deception, or evaluation based on unstated private data. Ask for the answer text before scoring when no answer is supplied.
