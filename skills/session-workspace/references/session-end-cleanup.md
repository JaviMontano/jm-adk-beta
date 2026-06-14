<!-- distilled from alfa skills/session-end-cleanup -->
<!-- > -->
# Session End Cleanup

> "Method over hacks."

## TL;DR

Run at the end of an agent session to leave a reproducible closeout packet:
what changed, what was validated, what remains open, which durable logs need
updates, and what the next session does first. The deliverable is a handoff a
cold reader can act on without replaying the conversation. [EXPLICIT]

## Deterministic Resources

- `assets/activation-policy.json` — activation and false-positive rules.
- `assets/output-contract.json` — required closeout sections (canon for the list below).
- `assets/evidence-policy.json` — allowed evidence tags and proof rules.
- `assets/closure-checklist.json` — guardian checklist.
- `assets/update-policy.json` — tasklog/changelog update boundaries.
- `scripts/check.sh` — offline fixture validation for the JSON closeout contract.

Conflict rule: if this doc and an asset disagree, the asset wins; fix the doc. [INFERENCE]

## Evidence Tags

This is kit-facing output: use the Alfa core set in EN spelling, one tag per
claim, weakest applicable tag — `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`,
`[ASSUMPTION]`; plus closeout-local `[OPEN]` for an unfilled gap. Canon and
homologation: `references/verification-tags.md`. Never mix the Jarvis `{...}`
family into a closeout. [DOC]

## Inputs

Collect only session-local evidence before writing:

- User objective, active brand, active repo/workspace, explicit constraints.
- Files changed, commands run, validations passed/failed, PR/CI/merge state,
  unresolved blockers.
- Decisions made, assumptions accepted, risks found, follow-up tasks.
- Existing tasklog/changelog paths only when the user or repo policy authorizes
  durable updates.

If evidence is missing, mark it `[ASSUMPTION]` or `[OPEN]`; never invent a
successful command, PR state, merge state, or task closure. A fabricated green
is the single most damaging failure this skill exists to prevent. [DOC]

## Procedure

### Step 1: Inventory Evidence

- Read git status, diffs, command logs, PR/CI state, and task artifacts.
- List sources inspected and source gaps explicitly.
- Stop before durable writes if the working tree has unrelated changes (Step 3
  guards the write, but flag the contamination here).

### Step 2: Normalize The Session

- Produce sections in the Output Contract order; do not reorder.
- Tag every factual claim (see Evidence Tags).
- Separate completed work from proposed follow-up — never let a proposal read
  as done.

### Step 3: Update Durable Logs When Authorized

- Update only tasklog/changelog rows supported by local evidence.
- If log paths or authority are unclear, emit a proposed update block instead
  of writing. Default is propose-not-write: silence on authority means do not
  touch the ledger. [INFERENCE]
- Preserve chronology; never rewrite unrelated history.

### Step 4: Validate The Closeout

- Confirm every required section exists.
- Confirm every command and validation outcome is evidence-backed.
- Run `bash skills/session-end-cleanup/scripts/check.sh` when the skill itself
  is being maintained (not on every closeout).
- Block completion when validation, PR, CI, merge, or ledger evidence is
  absent. Blocking is a success state, not an error — emit the partial closeout
  with the gap named.

## Output Contract

Markdown for human handoff; JSON only when an automation requests a
machine-checkable closeout. The Markdown closeout must include, in order
(canon: `assets/output-contract.json`): [CONFIG]

1. Session Summary
2. Changes Completed
3. Decisions And Assumptions
4. Open Tasks
5. Insights Captured
6. Risks And Blockers
7. Validation Evidence
8. Durable Updates
9. Next Handoff
10. Guardian Decision

Guardian Decision is one of: `PASS` (all sections backed, no blockers),
`BLOCKED` (a required evidence class is absent — name it), or `PARTIAL`
(complete but carrying `[OPEN]`/`[ASSUMPTION]` the next session must resolve). [INFERENCE]

## Worked Example (abridged)

```
## Validation Evidence
- `pytest -q` → 142 passed, 0 failed [CODE]
- `npm run build` → exit 0 [CODE]
- CI status: not checked this session [OPEN]
## Durable Updates
- PROPOSED (no write authority given): tasklog row "T-19 → done" [ASSUMPTION]
## Guardian Decision
BLOCKED — merge state unverified; do not claim merged. [DOC]
```

## Quality Criteria

- [ ] Every factual claim carries exactly one Alfa-core tag (EN spelling).
- [ ] Validation outcomes name the exact command or local source.
- [ ] Completed tasks are evidence-backed; failed/skipped checks are visible,
      not hidden.
- [ ] Durable updates touch only authorized tasklog/changelog entries.
- [ ] Next Handoff is actionable without reading the whole conversation.
- [ ] Guardian Decision matches the evidence (no `PASS` over an `[OPEN]`).

## Usage

- `/session-end-cleanup` after a coding session.
- `Run session end cleanup for this PR and prepare the handoff.`
- `Close this session but do not update durable logs; give me proposed entries.`

## Assumptions & Limits

- Assumes access to current session evidence and relevant project files.
- Does not fetch remote status unless explicitly needed for PR/CI/merge evidence.
- Does not mark tasks complete, claim CI green, or claim merge success without
  local or remote proof.
- Does not summarize across sessions — it closes the current one only; prior
  closeouts are inputs, not material to rewrite. [INFERENCE]
- Does not replace domain expert judgment for legal, financial, medical,
  security, or contractual decisions.

## Failure Modes

| Failure | Symptom | Guard |
|---|---|---|
| Fabricated green | "CI passed" with no command/source | Tag demands a source; missing → `[OPEN]` + `BLOCKED`. |
| Proposal read as done | Follow-up listed under Changes Completed | Step 2 separates completed vs proposed. |
| Silent ledger write | Tasklog edited without authority | Step 3 default is propose-not-write. |
| History rewrite | Unrelated chronology reordered | Step 3 preserves chronology; touch only evidenced rows. |
| Tag drift | `{SUPUESTO}` mixed into a kit closeout | Evidence Tags pins Alfa-core EN, one family. |
| Over-blocking | `BLOCKED` on a trivially absent optional check | Block only on the five evidence classes (validation/PR/CI/merge/ledger). |

## Edge Cases

| Scenario | Handling |
|---|---|
| No files changed | No-change closeout with decisions, risks, next handoff; Guardian `PASS` or `PARTIAL`. |
| Validation failed | Block; place the failed command in Risks And Blockers; Guardian `BLOCKED`. |
| Missing durable log authority | Emit proposed tasklog/changelog entries only; do not write. |
| Conflicting session goals | Preserve both claims, mark conflict, request owner decision. |
| Unrelated local changes | Stop before writes; identify the unexpected paths in Risks And Blockers. |
| Session aborted mid-task | Closeout what exists, mark the in-flight task `[OPEN]`, name the resume point in Next Handoff. |
| Evidence and asset disagree | Asset wins; record the doc drift as a follow-up task. |
