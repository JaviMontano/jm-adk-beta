<!-- distilled from alfa skills/session-manager -->
<!-- Manages session state, pipeline progress, and cold-start priming. Reads/writes .specify/context.json to track feature stages and artifact completion. [EXPLICIT] -->
# session-manager {Core} (v1.1)

> **"Every session knows where it left off. Every feature knows its stage."**

## Purpose

Tracks pipeline progress across sessions using `.specify/context.json`.
Computes feature stage from real artifacts, primes cold starts from known
sources, and persists state only with evidence-backed authorization. [EXPLICIT]

## When to Activate

- A session starts and needs project state, last plan, active tasks, and next action.
- A user asks for `/jm:status`, session status, context recovery, or pipeline progress.
- A phase finishes and `.specify/context.json`, `.specify/score-history.json`, or
  `.specify/decisions/` may need an authorized update.

Do not activate for unrelated account, password, browser, weather, calendar, or
generic "session" questions that do not involve project pipeline state. [EXPLICIT]

**Anti-scope (explicitly NOT this skill's job):** [EXPLICIT]

- Editing source code, specs, plans, or tasks — session-manager only reads them
  as evidence and writes the three state targets in Phase 3.
- Running tests, gates, or builds. It reads their recorded outputs; it does not
  execute them.
- Inferring stage from git branch, commit message, elapsed time, or chat memory.
- Resolving a context-vs-artifact conflict on its own — that needs user
  confirmation (see Law of Authorized Persistence).

---

## Deterministic Resources

- `assets/state-contract.json` defines required status-report fields and allowed
  context states.
- `assets/stage-policy.json` defines allowed stages, artifact evidence, and
  no-skip stage progression.
- `assets/priming-policy.json` defines cold-start read order and missing-source
  handling.
- `assets/persistence-policy.json` defines authorized writes to `.specify/**`.
- `assets/source-boundary-policy.json` defines allowed source and output paths.
- `scripts/validate_session_manager_report.py` validates JSON reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

Precedence when resources disagree: a policy asset overrides this prose; this
prose overrides any inference. If an asset is missing or unparseable, treat its
domain as `[OPEN]` and block the writes it governs rather than guessing. [EXPLICIT]

---

## Core Principles (Immutable Laws)

1. **Law of State:** `.specify/context.json` is the project state source of truth
   after it is read and validated. [EXPLICIT]
2. **Law of Stages:** Feature stages progress linearly: `specified` -> `planned`
   -> `testified` -> `tasks-ready` -> `implementing` -> `complete`. [EXPLICIT]
3. **Law of Priming:** New sessions must read `.specify/context.json`, the latest
   plan, and active tasks before proposing work. [EXPLICIT]
4. **Law of Evidence:** Every stage, blocker, write, and next action must cite a
   local artifact or mark the gap as `[OPEN]`. [EXPLICIT]
5. **Law of Authorized Persistence:** Never write state from defaults, guesses, or
   stale memory; writes require artifact evidence and explicit process
   authorization. [EXPLICIT]

**Why linear, no-skip stages (trade-off):** a strict chain makes a missing
artifact unambiguous (the gap is exactly one named stage) and makes regressions
detectable. The cost is that legitimately parallel work (e.g. tests written
before a plan exists) reports the *lowest* consistent stage, which can understate
progress. We accept understatement over false-advance because a false `complete`
silently ships unvalidated work, while a conservative stage only delays a
correction the user can override. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Cold-Start Priming

1. Read `.specify/context.json` and record `present`, `missing`, or `invalid`.
2. Read the latest `.specify/plans/plan-*.md` by filename/date order when present.
3. Read active tasks from `tasks.md` or `.specify/tasks.md` when present.
4. Record all loaded and missing sources in order with evidence tags.
5. If the context file is missing or invalid, block persistence and ask for
   recovery input unless an existing repo policy authorizes initialization.

Tie-breaks: if multiple `plan-*.md` files share a date prefix, pick the
lexicographically last filename and record the ambiguity as `[OPEN]`. If both
`tasks.md` and `.specify/tasks.md` exist, `.specify/tasks.md` wins and the
duplicate is reported as a drift `[OPEN]`. [EXPLICIT]

### Phase 2: Stage Computation

Compute the stage from artifact evidence:

| Evidence | Stage |
|---|---|
| `spec.md` exists | `specified` |
| `plan-*.md` exists | `planned` |
| `tests/features/*.feature` exists | `testified` |
| `tasks.md` or `.specify/tasks.md` exists | `tasks-ready` |
| task evidence shows partial implementation | `implementing` |
| all task evidence is complete and validation evidence exists | `complete` |

Stage is the **highest** row whose evidence is present **and** for which every
lower row's evidence is also present (the chain is unbroken). A higher artifact
existing over a gap does not advance the stage; it raises a drift `[OPEN]`. [EXPLICIT]

Rules:

- Do not advance more than one stage in one session-manager pass.
- Do not report `implementing` unless task evidence exists and progress is
  between 1 and 99 percent.
- Do not report `complete` unless task evidence is complete and validation
  evidence is present.
- If artifacts contradict `context.json`, preserve both values and block
  persistence until the user confirms the correction.
- Empty or whitespace-only artifacts do not count as evidence; treat a
  zero-byte `spec.md` as absent for that stage. [EXPLICIT]

### Phase 3: State Persistence

1. Update `.specify/context.json` only after the computed stage is verified and
   the write is authorized.
2. Append `.specify/score-history.json` only after a named gate pass is present.
3. Create `.specify/decisions/DL-NNN.md` only after a concrete decision exists.
4. Refuse writes outside `.specify/context.json`, `.specify/score-history.json`,
   and `.specify/decisions/`.

Write discipline: writes are append- or replace-whole-file, never partial
in-place edits that could corrupt JSON. Compute the new content, validate it
parses, then write. `DL-NNN` uses the next zero-padded integer after the highest
existing decision file; never reuse or backfill a number. A pass that computes no
stage change and no new gate/decision performs **zero** writes (idempotent). [EXPLICIT]

### Phase 4: Status Report

Return a concise report with:

- context snapshot and source statuses
- computed stage and previous recorded stage
- artifact evidence
- persistence actions or blocked writes
- next action
- Guardian decision

The Guardian decision is one of `proceed`, `blocked`, or `needs-confirmation`,
and every `blocked`/`needs-confirmation` names the missing or conflicting
evidence. [EXPLICIT]

---

## Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `.specify/context.json` | JSON | Yes | Project state file and recorded stage. |
| `.specify/plans/plan-*.md` | Markdown | No | Latest plan evidence. |
| `tasks.md` or `.specify/tasks.md` | Markdown | No | Task and implementation evidence. |
| `tests/features/*.feature` | Gherkin | No | Testification evidence. |
| `.specify/score-history.json` | JSON | No | Gate pass history. |

### Outputs

| Output | Type | Description |
|---|---|---|
| Status report | Markdown | Current state, computed stage, blockers, and next step. |
| Updated context | JSON | Authorized `.specify/context.json` update only when safe. |
| Decision log | Markdown | Authorized `.specify/decisions/DL-NNN.md` when a decision exists. |
| Machine report | JSON | Optional report accepted by `scripts/validate_session_manager_report.py`. |

---

## Worked Examples

**A. Clean priming, one-stage advance.** `context.json` records `planned`;
`spec.md` and `plan-001.md` exist; `tests/features/login.feature` was just added.
Computed stage `testified` (chain spec->plan->tests intact). Advance is exactly
one step, so persist `testified`, report previous `planned`, Guardian `proceed`.
[EXPLICIT]

**B. Conflict, block.** `context.json` records `complete`; tasks show 3/10 done
and no validation evidence. Computed stage `implementing`. This is a regression
relative to the recorded value AND lacks the evidence `complete` claims, so
preserve both (`recorded=complete`, `computed=implementing`), write nothing,
Guardian `needs-confirmation` naming the missing validation evidence. [EXPLICIT]

**C. Drift gap.** `plan-001.md` exists but `spec.md` is missing. Chain is broken
at the lowest row, so the computed stage is `[OPEN]` (no consistent stage), not
`planned`. Block persistence, raise a drift `[OPEN]` for the absent spec, next
action: "recover or author `spec.md`". [EXPLICIT]

---

## Validation Gate (10x Checklist)

- [ ] `.specify/context.json` was read or marked missing/invalid with `[OPEN]`.
- [ ] Latest plan and active tasks were read or marked missing with `[OPEN]`.
- [ ] Computed stage cites artifact evidence and follows `assets/stage-policy.json`.
- [ ] No stage skip occurred without Guardian block.
- [ ] `implementing` and `complete` stages have task/validation evidence.
- [ ] Persistence actions stay inside `.specify/**` allowed targets.
- [ ] Writes are authorized before any state file changes.
- [ ] A no-change pass produced zero writes (idempotent).
- [ ] Output includes next action and an explicit Guardian decision value.
- [ ] Machine report passes `bash skills/session-manager/scripts/check.sh` when used.

**Acceptance criteria (done means all true):** the report names every source as
loaded/missing/invalid; computed stage equals the highest unbroken-chain row;
every persisted write cites the artifact that authorized it; no write touches a
path outside the three allowed targets; and on any conflict the Guardian decision
is `blocked` or `needs-confirmation`, never `proceed`. [EXPLICIT]

---

## Self-Correction Triggers

> [!WARNING]
> IF `.specify/context.json` is missing THEN do not silently create it. Block,
> report the missing source, and initialize only when a repo policy or user
> confirmation authorizes the write.

> [!WARNING]
> IF stage is `implementing` but no task file exists THEN block and roll back the
> computed stage to the latest evidence-backed stage.

> [!WARNING]
> IF context stage and artifact stage conflict THEN preserve both values, explain
> the conflict, and request confirmation before persistence.

> [!WARNING]
> IF a computed advance would skip a stage THEN cap it at one step, persist the
> single-step result, and report the remaining gap as the next action. [EXPLICIT]

## Failure Modes

| Failure mode | Symptom | Required response |
|---|---|---|
| Silent false-advance | Stage jumps 2+ steps in one pass | Cap at one step; report remaining gap. [EXPLICIT] |
| Memory inference | Stage cited from chat/branch, no artifact | Discard; recompute from files or mark `[OPEN]`. [EXPLICIT] |
| Out-of-boundary write | Edit proposed outside the 3 targets | Refuse the write; report attempted path. [EXPLICIT] |
| Corrupt context write | `context.json` left unparseable | Abort write; preserve prior file; report parse risk. [EXPLICIT] |
| Phantom `complete` | `complete` without validation evidence | Downgrade to `implementing` or block. [EXPLICIT] |
| Stale duplicate tasks | `tasks.md` and `.specify/tasks.md` disagree | Prefer `.specify/tasks.md`; raise drift `[OPEN]`. [EXPLICIT] |

## Usage

Example invocations:

- `/jm:status`
- `Run session-manager for this repo and show the next action.`
- `Update context.json after this phase completion if the evidence is valid.`

## Assumptions & Limits

- Assumes local access to `.specify/**` and related project artifacts. [EXPLICIT]
- Assumes one feature pipeline per `context.json`; multi-feature monorepos need
  one invocation per feature root. [ASSUMPTION]
- Does not infer progress from memory, conversation history, branch names, or
  elapsed time. [EXPLICIT]
- Does not execute tests, gates, or builds; it only reads their recorded
  evidence. [EXPLICIT]
- Does not replace project owner confirmation for conflicting or destructive
  state changes. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing context file | Block persistence and request recovery authorization. |
| Invalid JSON context | Report parse failure and avoid writes. |
| Plan exists but no spec | Compute the lowest consistent evidence-backed stage and block skip. |
| Tasks complete but no validation evidence | Report `implementing` or block `complete`. |
| Empty/zero-byte artifact | Treat as absent for stage purposes; do not advance. |
| Multiple plans, ambiguous order | Pick lexicographically last; record ambiguity as `[OPEN]`. |
| Recorded stage ahead of artifacts | Preserve both; Guardian `needs-confirmation`; no write. |
| Unrelated "session" request | Do not activate. |
