<!-- distilled from alfa skills/parallel-workflow -->
<!-- > -->
# Sequential-First, Parallel-Ready Workflow

> "Sequential is safe. Parallel is fast. Smart is knowing when to switch."

## TL;DR

**Default: sequential.** All tasks execute one after another along the critical path. Parallelism is activated ONLY when the approved plan explicitly marks tasks `[PARALLEL-OK]` with zero pre-dependencies, zero co-dependencies, and WIP <= 3 agents. Forward-only execution — no task waits for another parallel task. When in doubt: sequential. The burden of proof is on parallelism.

## Procedure

### Step 1: Discover
- Read the plan file — is parallelism explicitly approved? Look for `[PARALLEL-OK]` tags
- If no `[PARALLEL-OK]` tags: **STOP — execute sequentially along critical path**
- Map task dependencies: pre-dependencies (A must finish before B), co-dependencies (A and B share state), output dependencies (A's output is B's input)
- Check current git state: clean working tree, up-to-date with remote

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

### Step 4: Validate
- All worktrees merge cleanly into main
- Contract tests pass after integration
- No interface drift between parallel streams
- All quality gates (G0-G3) pass on the merged result
- Clean up worktrees after merge:
  ```bash
  git worktree remove ../task-auth
  git worktree remove ../task-dashboard
  ```

## Quality Criteria

- [ ] Plan has explicit `[PARALLEL-OK]` tags for parallelized tasks
- [ ] 4-point eligibility check passed (plan, zero-deps, WIP<=3, forward-only)
- [ ] WIP never exceeds 3 concurrent agents
- [ ] Interface contracts defined before parallel work begins
- [ ] Git worktrees used for isolation (not just branches)
- [ ] Each branch is atomic and independently mergeable
- [ ] No task waits for another parallel task (forward-only)
- [ ] Contract tests verify integration points
- [ ] All quality gates pass on merged result
- [ ] Worktrees cleaned up after merge
- [ ] Evidence tags applied to all claims

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

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
