<!-- distilled from alfa skills/session-protocol -->
<!-- > -->
# Session Protocol

> "AI sessions start with zero context. Without a protocol, the first 10 minutes are wasted re-establishing what was done."

## TL;DR

Mandatory session-init sequence from the Constitution: (1) load context files in order, (2) recover state from recent activity, (3) propose closure for pending items, (4) suggest next steps. Every session starts productive from minute one with full awareness of project state, open tasks, and recent decisions. [EXPLICIT]

**When to run:** at session start, after a context compaction, or when resuming a branch you have not touched in >1 day. **When to skip:** mid-session continuations where context is already loaded (re-running wastes tokens and re-prompts the user). [INFERENCE]

## Deterministic Resources

- `assets/context-load-order.json` — ordered source loading and missing-file handling.
- `assets/state-recovery-policy.json` — changelog, tasklog, git, and spec checks.
- `assets/closure-policy.json` — close/continue/defer/archive recommendation rules.
- `assets/next-step-policy.json` — next-step ranking and confirmation boundaries.
- `assets/protocol-report-contract.json` — report shape validated by `scripts/check.sh`.

Policy lives in JSON, not prose: thresholds (e.g. staleness days, changelog window) are tuned without editing this playbook, and `scripts/check.sh` validates output against the contract. [INFERENCE]

## Procedure

### Step 1: Discover — Context Loading
Load in order (read each file):
1. `CLAUDE.md` — project instructions and agent rules
2. `CONSTITUTION.md` or `references/ontology/constitution-v5.2.0.md` — governance
3. `insights/README.md` — insights index (load domain files on-demand, not eagerly)
4. `changelog.md` — recent changes and decisions
5. `tasklog.md` — open tasks and pending work

Order is load-bearing: governance constrains how later files are interpreted, so it precedes changelog/tasklog. A missing file is reported `[OPEN]` and the sequence continues — never silently skipped, never aborted. [EXPLICIT]

### Step 2: Analyze — State Recovery
After loading context:
1. Read last 5 `changelog.md` entries — understand recent session outcomes
2. Read all open items in `tasklog.md` — identify pending work, blockers, stale tasks
3. Check `insights/` for any insight tagged `tentative` or `needs validation`
4. Check `git status` and recent commits on current branch
5. Check `.specify/` for in-progress specs, plans, or debates

Read-only step: no commits, no task edits, no file writes. Recovery observes; mutation waits for Step 3 confirmation. [EXPLICIT]

### Step 3: Execute — Pending Closure
Before accepting new work:
1. List all open tasks from `tasklog.md` with their age (days since last progress)
2. For each: recommend `close` (done), `continue` (active), `defer` (deprioritize), or `archive` (no longer relevant)
3. Flag stale items (>7 days without progress)
4. Present summary to user — confirm before closing or archiving

Each recommendation cites its evidence (the changelog entry, commit, or task note that justifies it). `continue`/`defer` are reversible and may be applied on user assent; `close`/`archive` are destructive to the open set and require explicit per-item confirmation. [EXPLICIT]

### Step 4: Validate — Next Steps Proposal
After pending items resolved:
1. Analyze current feature state (IIKit dashboard, branch status, phase progress)
2. Suggest 2-3 concrete next steps ranked by impact
3. Include at least one improvement beyond the current task (from insights gaps, constitution TODOs, or observed patterns)
4. Wait for user direction — never start work without explicit confirmation

The "1 improvement step" rule forces escape from pure continuation: a session that only ever advances the open task never pays down debt or acts on a known gap. [INFERENCE]

## Worked Example

State: `changelog.md` last entry "auth refactor merged"; `tasklog.md` has T-12 "add rate-limit tests" (last touched 9 days ago) and T-15 "wire metrics" (touched today); `git status` clean on `feat/metrics`.

1. **Discover** — 5 files loaded; `CONSTITUTION.md` absent → `references/ontology/constitution-v5.2.0.md` used instead. [DOC]
2. **Analyze** — recent outcome = auth merge; T-12 stale (9d > 7d), T-15 active; one insight tagged `tentative`.
3. **Closure** — T-12 → `defer` (stale, unrelated to active branch) [evidence: no commits touch rate-limit since merge]; T-15 → `continue` [evidence: commit today]. Present both; await confirmation before deferring T-12.
4. **Next steps** — (a) finish T-15 metrics wiring; (b) validate the `tentative` insight; (c) **improvement:** add the rate-limit tests T-12 deferred, now that auth is stable. Await user pick.

## Quality Criteria

- [ ] All 5 context files loaded in correct order; missing ones reported `[OPEN]`
- [ ] Last 5 changelog entries reviewed
- [ ] All open tasklog items identified, each with an age
- [ ] Stale items (>7 days) flagged
- [ ] Closure recommendations provided, each citing evidence
- [ ] 2-3 next steps proposed with rationale, including ≥1 improvement step
- [ ] No `close`/`archive` applied without per-item user confirmation
- [ ] No work started without user confirmation
- [ ] Steps 1-2 produced zero writes/commits
- [ ] `scripts/check.sh` passes against `protocol-report-contract.json`

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping context loading | Repeat past mistakes, miss decisions | Always load all 5 files |
| Aborting on a missing file | Loses recoverable state | Tag `[OPEN]`, continue sequence |
| Starting work before closure | Task accumulation, invisible debt | Close pending items first |
| Only proposing continuation | Misses improvement opportunities | Include ≥1 improvement step |
| Auto-closing without consent | User loses control | Confirm `close`/`archive` per item |
| Re-running protocol mid-session | Wastes tokens, re-prompts user | Run once per cold start only |
| Closure without evidence | Unjustified, irreversible loss | Cite changelog/commit per item |

## Related Skills

- `continuous-learning` — Insights loaded during context recovery
- `tasklog-management` — Tasklog is primary input for pending closure
- `changelog-management` — Changelog is primary input for state recovery
- `session-manager` — Owns `.specify/context.json` stage tracking read in Step 2

## Usage

Example invocations:

- "/session-protocol" — Run the full session protocol workflow
- "session protocol on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Staleness threshold is fixed at 7 days; per-project tuning lives in `state-recovery-policy.json`, not here [ASSUMPTION]
- Does not auto-execute closures or next steps — proposes only; the user remains the actor [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| A required context file is missing | Report `[OPEN]`, continue with remaining files |
| `tasklog.md` empty (greenfield) | Skip closure; go straight to next-step proposal |
| `git` unavailable or not a repo | Skip Step 2.4, note it, continue from artifacts |
| All open tasks stale (>7d) | Recommend `defer`/`archive`, never bulk-close without confirmation |
| User declines all closures | Honor it; carry items forward, still propose next steps |
| Mid-session re-invocation | Confirm context already loaded; skip rather than reload |
