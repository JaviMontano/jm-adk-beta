<!-- distilled from alfa skills/pre-compact-context -->
<!-- > -->
# Pre Compact Context

> "Method over hacks."

## TL;DR

Use this skill before a context window is compacted, summarized, or handed to a
new thread. It decides what must be preserved verbatim, what may be compressed,
what can be dropped, and what the next session must read first. Output is a
single Markdown rehydration packet with fixed sections, evidence tags, and a
Guardian decision that can block compaction. [EXPLICIT]

## When To Use / Not Use

- USE before auto-compaction fires, before summarizing a long thread, before
  `/clear`, or before handing work to a fresh session. [EXPLICIT]
- DO NOT USE for session-end teardown (use `session-end-cleanup`) or to write
  durable memory without explicit authorization. [EXPLICIT]
- Anti-scope: does not summarize for the user, does not refactor code, does not
  resolve conflicting state — it preserves the conflict and flags it. [EXPLICIT]

## Deterministic Resources

- `assets/retention-policy.json` defines priority classes and drop rules.
- `assets/output-contract.json` defines the required packet sections.
- `assets/evidence-policy.json` defines source and evidence tag requirements.
- `assets/rehydration-checklist.json` defines the resume checklist.
- `assets/compaction-risk-policy.json` defines known loss modes and blockers.
- `scripts/check.sh` validates deterministic JSON packet fixtures offline.

JSON assets are the source of truth; if this doc and an asset disagree, the
asset wins and this doc is the defect. [INFERENCE]

## Inputs

Collect local and user-provided context before writing:

- Active objective, brand, repo/workspace, branch, PR/CI state, and hard rules.
- Current progress, pending tasks, blockers, assumptions, and decisions.
- Files, docs, commands, validation evidence, and source paths needed to resume.
- User preferences, naming conventions, scope boundaries, and forbidden changes.

If evidence is missing, mark it `[OPEN]` or `[ASSUMPTION]`; never invent command
results, task status, PR state, or durable context. [EXPLICIT]

## Procedure

### Step 1: Inventory Sources

- Read the active instructions, task state, git status, changed files, and any
  tasklog/changelog or review artifacts needed to resume.
- Identify context that must survive compaction without relying on hidden chat
  memory.

### Step 2: Classify Retention

- Mark P0 for hard rules, active objective, blockers, merge/PR state, and next
  action.
- Mark P1 for implementation details, file paths, validation commands, and
  decisions.
- Mark P2 for helpful background that can be summarized.
- Mark DROP for repeated chatter, stale alternatives, and details disproven by
  later evidence.

Tie-break when budget is tight: keep the item that, if lost, would force the
next session to redo work or violate a hard rule; drop the item that can be
re-derived from a named source. [INFERENCE]

### Step 3: Build The Rehydration Packet

- Produce fixed sections: trigger, preserve verbatim, compressed summary,
  discard list, open questions, risks, validation evidence, and rehydration
  prompt.
- Keep source paths and commands exact.
- Include first action for the next session.

### Step 4: Validate Before Compaction

- Ensure every P0 item has a source, evidence tag, and reason.
- Ensure DROP items do not contain active blockers or hard rules.
- Run `bash skills/pre-compact-context/scripts/check.sh` when maintaining this
  skill.
- Block compaction when critical evidence is missing or contradictory.

## Output Contract

The Markdown packet must include:

1. Compaction Trigger
2. Preserve Verbatim
3. Compressed Summary
4. Discard List
5. Open Questions
6. Risks And Blockers
7. Validation Evidence
8. Rehydration Prompt
9. Guardian Decision

Every section must be present even when empty: emit the heading with `none` plus
a one-line reason, so the next session can distinguish "nothing to record" from
"section forgotten". [INFERENCE]

## Quality Criteria

- [ ] Every P0 item has source, evidence tag, and reason.
- [ ] All factual claims use `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`,
  `[ASSUMPTION]`, or `[OPEN]`.
- [ ] The packet distinguishes preserve, compress, and discard decisions.
- [ ] The rehydration prompt names exact files, commands, branch/PR state, and
  next action.
- [ ] Guardian blocks if compaction would lose active blockers, hard rules, or
  validation state.

## Acceptance Criteria

The packet is done when a fresh session, given ONLY the packet (no chat
history), can: state the objective and hard rules; name the branch/PR/CI state;
run the next action without asking what it is; and reproduce validation evidence
from the listed commands. If any of these requires hidden memory, the packet
fails and must be revised. [INFERENCE]

## Worked Example (abridged)

Trigger: auto-compaction imminent, ~6% context left. [OPEN]
Preserve Verbatim — P0: hard rule "never echo secrets" [DOC]; objective "fix
flaky auth test" [EXPLICIT]; branch `fix/auth-flake`, PR #214 open, CI red on
`test_login_retry` [CODE].
Compressed Summary — P1: refactored retry helper in `src/auth/retry.ts`; root
cause is a 50 ms race; fix attempt 1 reverted. [CODE]
Discard List — DROP: early hypothesis "DNS timeout" disproven by CI logs;
reason recorded. [INFERENCE]
Validation Evidence: `npm test -- auth/retry` → 1 failing, 8 passing. [CODE]
Rehydration Prompt: "Resume on `fix/auth-flake`. Re-run `npm test -- auth/retry`,
then add a deterministic clock to `retry.ts:42`. Do not touch PR #214 metadata."
Guardian Decision: PROCEED — all P0 items sourced; no blocker in DROP.

## Failure Modes

- Silent over-drop: DROP swallows a hard rule or open blocker → Guardian must
  block; verify every DROP entry against P0 keys. [INFERENCE]
- False confidence: an `[ASSUMPTION]` is emitted as fact → next session acts on
  unverified state. Re-tag before validating. [INFERENCE]
- Stale exactness: a command or path was renamed mid-session but copied from
  early chat → re-read git status at Step 1, not memory. [INFERENCE]
- Secret leakage: raw token/key copied into Preserve Verbatim → redact to a
  reference; never echo. [EXPLICIT]

## Usage

Example invocations:

- `/pre-compact-context`
- `Before compaction, preserve the current PR state and next action.`
- `Prepare a rehydration packet for the next session.`

## Assumptions & Limits

- Assumes the current session has enough local evidence to classify context.
- Does not update durable memory unless explicitly authorized.
- Does not replace `session-end-cleanup`; it prepares for compaction before the
  session is necessarily complete.
- Does not claim that omitted context is irrelevant unless it is classified DROP
  with a reason.
- Cannot recover context already lost to a prior compaction; it only protects
  what is still in-window at invocation time. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|---|---|
| Context almost full | Emit a minimal P0/P1 packet and block low-value detail. |
| Conflicting task state | Preserve both claims and mark the conflict `[OPEN]`. |
| Unknown PR/CI status | Mark status unknown and include verification command. |
| Missing source path | Keep the item but mark source `[OPEN]`. |
| User asks to compact secrets | Preserve redacted reference only; do not echo secrets. |
| No changes / read-only session | Emit packet with objective + next read; sections may be `none`. |
| Multiple active branches/PRs | List each with its own state; do not merge into one. |
| Evidence contradicts a hard rule | Guardian blocks; surface the contradiction in Open Questions. |
