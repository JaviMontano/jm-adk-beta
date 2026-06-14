<!-- distilled from alfa skills/session-start-bootstrap -->
<!-- > -->
# Session Start Bootstrap

> "Method over hacks."

## TL;DR

Run at the start of a session to establish safe operating state before any
write: active repo, branch, brand, instructions, context sources, blockers,
validation baseline, and first action. Output is a Markdown start packet plus a
Guardian decision that blocks execution on unresolved critical gaps. [DOC]

## Deterministic Resources

- `assets/bootstrap-contract.json` — required packet fields.
- `assets/environment-policy.json` — repo, branch, PR, and dirty-tree checks.
- `assets/context-loading-policy.json` — minimal context loading order.
- `assets/guardrails-policy.json` — stop conditions and hard-rule loading.
- `assets/source-priority.json` — source precedence.
- `scripts/check.sh` — validates JSON bootstrap packet fixtures offline; treat a
  non-zero exit as a Guardian block, not a warning. [CONFIG]

## Inputs

Collect:

- Active user objective and active brand. [DOC]
- Current repo/workspace, branch, git status, PR state, and merge baseline. [DOC]
- Applicable `AGENTS.md`, runtime instructions, tasklog/changelog or handoff
  packet, and user constraints. [DOC]
- Known blockers, stashes, pending validations, and next action. [DOC]

Mark unknown state `[OPEN]`; never infer a clean tree, current branch, PR state,
or user authorization without evidence. An absent signal is `[OPEN]`, never a
green default — see Failure Modes. [INFERENCIA]

## Procedure

### Step 1: Verify Environment

- Confirm repo identity and current branch.
- Run or record `git status --short --branch`. [CONFIG]
- Check open PRs or local blockers when the workflow requires exclusivity.
- Stop before writes if the repo is dirty outside the active scope.

### Step 2: Load Minimal Context

- Read root instructions first, then only task-relevant sources.
- Prefer recent handoff packets, review docs, tasklog/changelog entries, and
  files named by the user.
- Do not bulk-load private or unrelated context.

### Step 3: Initialize Guardrails

- Record hard rules, forbidden changes, validation requirements, and pause
  criteria.
- Resolve source precedence: explicit user config, repo instructions, active
  handoff, then inferred defaults (`source-priority.json` is canonical). [CONFIG]

### Step 4: Emit Start Packet

- Produce environment, context sources, guardrails, blockers, validation
  baseline, and first action.
- Block execution if the start packet has unresolved critical gaps.

## Output Contract

The Markdown packet must include, in order:

1. Environment
2. Context Sources Loaded
3. Active Guardrails
4. Current State
5. Blockers And Gaps
6. Validation Baseline
7. First Action
8. Guardian Decision (`PROCEED` | `PAUSE` | `BLOCK`)

A critical gap (unknown repo, unverified dirty tree, missing edit authority)
forces `PAUSE` or `BLOCK`; `PROCEED` requires sections 1–7 evidence-backed. [INFERENCIA]

## Quality Criteria

- [ ] Repo, branch, and dirty-tree state are evidence-backed.
- [ ] Context sources loaded are listed by path or command.
- [ ] Hard rules and pause criteria are explicit.
- [ ] First action is concrete and scoped.
- [ ] Guardian blocks when environment or context authority is missing.
- [ ] Every claimed fact carries a verification tag from one family. [DOC]

## Usage

- `/session-start-bootstrap`
- `Start this session from the prior handoff.`
- `Bootstrap the repo and tell me the first safe action.`

## Worked Example (abbreviated start packet)

```
Environment: repo jm-adk-beta @ main, tree DIRTY (2 paths) [CONFIG]
Context Sources Loaded: AGENTS.md; handoff 2026-06-10.md [DOC]
Active Guardrails: no force-push; tests green before commit [CONFIG]
Current State: feature/session-bootstrap unmerged; PR #14 OPEN [CONFIG]
Blockers And Gaps: edit authority for src/ [OPEN]
Validation Baseline: scripts/check.sh PASS (fixtures only) [CONFIG]
First Action: read handoff, then confirm src/ edit scope with user
Guardian Decision: PAUSE — dirty tree + unconfirmed edit authority [INFERENCIA]
```

Dirty tree plus an `[OPEN]` authority gap is the canonical `PAUSE`: state is
known but the next write is not yet authorized. [INFERENCIA]

## Assumptions & Limits

- Does not edit project files unless the start packet is valid and the next
  skill authorizes edits. [SUPUESTO]
- Does not bulk-load unrelated context.
- Does not treat stale handoffs as current without git/PR verification.
- Read-only by contract: no commits, pushes, stash pops, or branch switches —
  those belong to the skill that runs after a `PROCEED`. [INFERENCIA]
- Offline by default: `check.sh` validates fixtures, not live remotes; PR state
  recorded here may lag the server until re-fetched. [SUPUESTO]

## Anti-Scope (explicitly NOT this skill)

- Performing the work itself, or choosing the methodology/plugin to run.
- Resolving merge conflicts or cleaning a dirty tree — it only reports them.
- Fabricating brand, objective, or authorization to reach `PROCEED`. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|---|---|
| Dirty tree | Pause and list changed paths before writes. |
| Unknown repo | Request repo identity or inspect safe local markers. |
| Conflicting instructions | Preserve both, apply explicit user config first, and mark conflict. |
| Missing handoff | Start from repo instructions and mark missing handoff `[OPEN]`. |
| Open PR exists | Pause if workflow requires one PR at a time. |
| Detached HEAD | Record commit SHA as branch; flag `[OPEN]` and pause before writes. |
| No git repo | Treat as unknown repo; do not assume cwd is the target workspace. |
| Multiple brands in scope | Pick one before emitting; never mix brands in one packet. |

## Failure Modes

| Failure | Trigger | Guard |
|---|---|---|
| False-green tree | Skipping `git status`, assuming clean | Require recorded `git status --short --branch` output. [CONFIG] |
| Stale handoff applied as current | Trusting a handoff without re-checking git/PR | Re-verify branch + PR before honoring handoff state. [INFERENCIA] |
| Context bloat | Bulk-loading private/unrelated files | Load root instructions + task-relevant sources only. |
| Silent gap | Emitting `PROCEED` with an `[OPEN]` field | Any unresolved critical field downgrades to `PAUSE`/`BLOCK`. [INFERENCIA] |
| Authority overreach | Editing before the next skill grants edit rights | Read-only until packet is valid AND edits are authorized. [SUPUESTO] |

## Acceptance Criteria

- All eight Output Contract sections present and ordered. [DOC]
- Environment claims (repo, branch, tree, PR) each map to a command or path.
- No `PROCEED` while any critical field is `[OPEN]`.
- Tags drawn from one family only (Alfa core here); spelling consistent. [DOC]
- `scripts/check.sh` passes on the emitted fixture, or its failure is surfaced
  as a Guardian block. [CONFIG]
