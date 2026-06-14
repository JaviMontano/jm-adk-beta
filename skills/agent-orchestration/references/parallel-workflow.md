<!-- distilled from alfa skills/parallel-workflow -->
<!-- > -->
# Sequential-First, Parallel-Ready Workflow

> "Sequential is safe. Parallel is fast. Smart is knowing when to switch."

## TL;DR

**Default: sequential.** All tasks execute one after another along the critical path. Parallelism activates ONLY when the approved plan explicitly marks tasks `[PARALLEL-OK]` with zero pre-dependencies, zero co-dependencies, and WIP <= 3 agents. Forward-only — no task waits for another parallel task. When in doubt: sequential. The burden of proof is on parallelism. [DOC]

**Why this default.** Parallel execution multiplies merge surface, fragments context across worktrees, and serializes review anyway (one human merges). Sequential wins unless the time saved exceeds the merge+review tax — true only for genuinely independent, contract-bounded work. [INFERENCIA]

## Procedure

### Step 1: Discover
- Read the plan file — is parallelism explicitly approved? Look for `[PARALLEL-OK]` tags. [CONFIG]
- If no `[PARALLEL-OK]` tags: **STOP — execute sequentially along critical path**
- Map task dependencies: pre-dependencies (A must finish before B), co-dependencies (A and B share mutable state), output dependencies (A's output is B's input)
- Check current git state: clean working tree, up-to-date with remote (`git status` clean, `git fetch` + no divergence) [CONFIG]

### Step 2: Analyze — Parallel Eligibility Check
Run the 4-point checklist. ALL must pass:
1. **Plan approval**: plan has explicit `[PARALLEL-OK]` on candidate tasks
2. **Zero dependencies**: no pre-deps, co-deps, or shared mutable files between candidates
3. **WIP <= 3**: no more than 3 agents will run simultaneously
4. **Forward-only**: each task can complete independently without waiting for another

If ANY check fails → **fall back to sequential execution**

- For eligible tasks: define interface contracts at integration points
- Plan merge order: contracts first → implementations → integration tests
- Assess operational risk: shared files, merge complexity, review bottleneck

**Shared-file test (the co-dependency trap).** Two tasks are NOT independent if they edit the same file, even on different lines — git merges textually, not semantically. Run `git diff --name-only` mentally per task; any filename intersection (especially lockfiles, route tables, barrel `index.ts`, shared config) fails check 2. Example: "add auth route" + "add dashboard route" both touch `routes.ts` → NOT parallel-eligible; sequence them or extract the route registry to a contract first. [INFERENCIA]

**Why WIP <= 3.** Above 3 concurrent streams, merge-conflict probability and reviewer context-switching cost rise faster than throughput gains; 3 keeps the integration graph reviewable in one pass. Treat 3 as a hard ceiling, not a target — 2 clean streams beat 3 entangled ones. [SUPUESTO] Verify by tracking conflict rate; if any batch exceeds one conflict, drop to 2.

### Step 3: Execute
- **Batch parallel tasks**: if 5 eligible, run in batches of 3 + 2 (never 5)
- Create worktrees for the current batch (max 3):
  ```bash
  # Batch 1: max 3 concurrent
  git worktree add ../task-auth feat/auth
  git worktree add ../task-dashboard feat/dashboard
  git worktree add ../task-api feat/api-contracts
  # Batch 2: after batch 1 completes
  git worktree add ../task-nav feat/navigation
  git worktree add ../task-footer feat/footer
  ```
- Define contracts before parallel work begins:
  ```typescript
  // contracts/user-api.ts — agreed interface
  export interface UserService {
    getUser(id: string): Promise<User>;
    updateUser(id: string, data: Partial<User>): Promise<void>;
  }
  ```
- Each worktree works independently, running its own tests
- Merge sequence: contracts first → independent implementations → integration tests
  ```bash
  # Merge in dependency order
  git checkout main
  git merge feat/api-contracts    # Contracts first
  git merge feat/auth             # Independent impl
  git merge feat/dashboard        # Independent impl
  ```

**Merge order rationale.** Contracts merge first so each implementation rebases onto a stable interface; merging an impl before its contract guarantees rework. Merge smallest/lowest-risk impl next to surface conflicts early while the integration graph is still simple. [INFERENCIA]

### Step 4: Validate
- All worktrees merge cleanly into main
- Contract tests pass after integration
- No interface drift between parallel streams (diff each impl's contract usage against `contracts/`) [INFERENCIA]
- All quality gates (G0-G3) pass on the merged result
- Clean up worktrees after merge:
  ```bash
  git worktree remove ../task-auth
  git worktree remove ../task-dashboard
  ```

## Decisions & Trade-offs

| Decision | Chosen | Rejected alternative | Why |
|---|---|---|---|
| Default mode | Sequential | Parallel-by-default | Merge/review tax exceeds savings unless work is provably independent [INFERENCIA] |
| Isolation unit | Git worktree | Shared branch / stash juggling | Worktrees give physical FS isolation; no cross-task contamination of working tree [DOC] |
| WIP ceiling | 3 | Unbounded / 5+ | Conflict + review cost grows super-linearly past 3 [SUPUESTO] |
| Contract timing | Before impl | Contracts emergent during impl | Emergent interfaces drift; merges break at integration [INFERENCIA] |
| History policy | Merge commits | Force-push / rebase shared | Force-push destroys peers' history on shared refs [DOC] |

## Acceptance Criteria

Done = ALL true (each is binary and checkable):
- [ ] Plan has explicit `[PARALLEL-OK]` tags for every parallelized task
- [ ] 4-point eligibility check passed (plan, zero-deps, WIP<=3, forward-only)
- [ ] WIP never exceeded 3 concurrent agents (verify: batch sizes in plan)
- [ ] Interface contracts committed BEFORE any parallel impl branch started
- [ ] Git worktrees used for isolation (not just branches sharing one working tree)
- [ ] Each branch is atomic and independently mergeable (each passes its own tests pre-merge)
- [ ] No task waited for another parallel task (forward-only; no cross-task blocking)
- [ ] Contract tests verify integration points and pass post-merge
- [ ] Zero interface drift: every impl conforms to committed `contracts/`
- [ ] All quality gates (G0-G3) pass on the merged result, not just per-branch
- [ ] Worktrees removed after merge (`git worktree list` shows only main)
- [ ] Evidence tags (`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`) applied to non-obvious claims [DOC]

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Defaulting to parallel | Merge risk, context fragmentation | Default to sequential; parallel requires plan approval |
| WIP > 3 | Cognitive overload, review bottleneck | Batch: 3 max concurrent, then next batch |
| Parallel with dependencies | Deadlocks, waiting, broken merges | Zero-dependency check BEFORE launching |
| Task waiting for another parallel task | Violates forward-only, creates deadlock | Stop dependent task, return to sequential queue |
| Parallel work without contracts | Integration breaks on merge | Define interfaces BEFORE parallel work |
| Force-pushing to shared branches | Destroys others' work history | Use merge commits, never force-push |
| Worktrees without cleanup | Disk bloat, stale references | Remove worktrees after merge |
| "Different lines, same file" assumed safe | Textual merge conflicts on shared file | Treat any shared mutable file as a co-dependency |
| Validating only per-branch | Green branches, red merge | Re-run G0-G3 on the integrated result |

## Failure Modes & Recovery

| Failure | Signal | Recovery |
|---|---|---|
| Merge conflict mid-batch | `git merge` reports conflict | Resolve in merge commit; if >1 conflict in batch, abort remaining, drop next batch to WIP 2 [INFERENCIA] |
| Hidden dependency surfaces after launch | Impl B needs Impl A's not-yet-merged code | Stop B, requeue B sequentially after A; do not block waiting [DOC] |
| Interface drift | Contract test fails post-merge | Roll back offending merge, realign impl to `contracts/`, re-merge |
| Worktree on dirty/wrong base | `git worktree add` fails or branches off stale main | Fetch + reset base to remote main before creating worktrees [CONFIG] |
| Quality gate fails only on merge | Per-branch green, merged red | Bisect by reverting last merge; fix integration, not the branch in isolation |
| Orphaned worktree after crash | `git worktree list` shows stale entry | `git worktree prune` then `remove` [CONFIG] |

## Related Skills

- `discovery-orchestration` — Identifies parallel execution opportunities in pipelines
- `api-design` — Defines API contracts for integration points
- `component-architecture` — Defines component interfaces for UI integration
- `github-actions-ci` — CI pipeline that validates merged result

## Usage

Example invocations:

- "/parallel-workflow" — Run the full parallel workflow workflow
- "parallel workflow on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- Assumes a single shared `main` and git worktree support (git >= 2.5) [SUPUESTO]
- Requires English-language output unless otherwise specified [DOC]
- Does not replace domain expert judgment for final decisions [DOC]
- **Anti-scope**: not a task scheduler, not a CI runner, not a substitute for plan approval. It decides *whether/how* to parallelize already-approved tasks; it never authorizes parallelism itself. [DOC]
- Not suited to tasks with unavoidable shared mutable state (DB migrations on one schema, monolithic config) — sequence those. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Exactly 1 eligible task | Run sequentially; parallelism overhead is pure cost [INFERENCIA] |
| All tasks share one file | Not parallel-eligible; sequence or extract a contract first |
| Plan tags `[PARALLEL-OK]` but deps exist | Plan is wrong — eligibility check overrides the tag; fall back to sequential |
| >3 eligible tasks | Batch in groups of <=3; never widen WIP to fit them all |
