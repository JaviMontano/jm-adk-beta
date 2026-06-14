<!-- distilled from alfa skills/git-hook-integration -->
<!-- > -->
# Git Hook Integration
> "Method over hacks."
## TL;DR
Plan (default) or install Git hooks — `pre-commit`, `commit-msg`, `pre-push` — with
non-destructive, reviewable commands and optional Conventional Commits enforcement. [EXPLICIT]

## Hook Matrix
Map each stage to one cheap, fast-failing job; defer slow checks to `pre-push`/CI. [INFERENCIA]

| Stage | Runs on | Purpose | Typical command | Budget |
|-------|---------|---------|-----------------|--------|
| `pre-commit` | staged files | format + lint + secret scan | `lint-staged` / `pre-commit run` | <5s [INFERENCIA] |
| `commit-msg` | commit message | Conventional Commits gate | `commitlint --edit "$1"` | <1s [INFERENCIA] |
| `pre-push` | pushed range | unit tests, typecheck, build | `npm test && npm run typecheck` | <60s [INFERENCIA] |

Conventional Commits regex (blocking, used by `commit-msg`): [EXPLICIT]
`^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-]+\))?!?: .{1,72}`

## Procedure

### Step 1: Discover
- Identify the repository, existing hook managers, current validation commands,
  and whether hook installation is allowed.
- Read existing hook files or config before proposing changes.
- Detect the active manager from artifacts: `.husky/`, `.pre-commit-config.yaml`,
  `.githooks/` + `core.hooksPath`, `lefthook.yml`, or bare `.git/hooks/`. [INFERENCIA]
- Default to `plan-only` when the user has not explicitly authorized mutation. [EXPLICIT]

### Step 2: Model
- Use `assets/git-hook-integration-schema.json` as the structured input
  contract.
- Ensure `pre-commit`, `commit-msg`, and `pre-push` stages are represented.
- If Conventional Commits are enabled, require a blocking `commit-msg` hook.

### Step 3: Compile
- Prefer `scripts/compile-git-hook-integration.py` when the task can be
  expressed as structured JSON.
- Use `assets/git-hook-integration-template.md` for Markdown output.
- Treat `assets/install-strategy-model.json` as the source for manager
  selection and install commands.

### Step 4: Validate
- Run `bash skills/git-hook-integration/scripts/check.sh` after changing the
  deterministic contract.
- Verify output contains evidence, hook matrix, commit policy, validation
  commands, install plan, validation, and risks.
## Decisions & Trade-offs
- **Manager choice** — Husky for JS/TS repos (npm-native, `prepare` script); `pre-commit`
  for polyglot/Python; `.githooks/` + `core.hooksPath` when zero dependencies are required.
  Trade-off: native `.githooks/` is dependency-free but each contributor must opt in via
  `git config core.hooksPath .githooks`. [INFERENCIA]
- **Where to gate** — keep `pre-commit` fast (staged-only) to avoid bypass habits; push
  expensive suites to `pre-push`/CI. Slow local hooks train developers to `--no-verify`. [INFERENCIA]
- **Bypass policy** — `--no-verify` is allowed for emergencies but the same checks MUST also
  run in CI, so a bypassed local hook cannot reach `main`. [EXPLICIT]

## Acceptance Criteria
- [ ] Output contains evidence, hook matrix, commit policy, validation commands, install plan,
      validation, and risks.
- [ ] Every required stage (`pre-commit`, `commit-msg`, `pre-push`) is present or explicitly N/A.
- [ ] When Conventional Commits are enabled, a blocking `commit-msg` hook is included.
- [ ] Install mode is explicit; no file is written/overwritten without authorization.
- [ ] Every hook command is shown verbatim and reviewable before installation.
- [ ] CI re-runs the same gates so `--no-verify` cannot bypass enforcement.

## Worked Example (plan-only, Husky + commitlint)
```sh
# proposed — NOT executed in plan-only mode
npx husky init
echo 'npx lint-staged'                 > .husky/pre-commit
echo 'npx commitlint --edit "$1"'      > .husky/commit-msg
echo 'npm test && npm run typecheck'   > .husky/pre-push
```
Output classifies this as `plan-only`; the user runs it or re-invokes with explicit mutation. [EXPLICIT]

## Failure Modes
| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Hooks never fire | `core.hooksPath` unset or wrong manager installed | Verify path; reinstall manager [INFERENCIA] |
| Hooks skipped in CI | hooks are local-only by design | Mirror gates as CI jobs [EXPLICIT] |
| `commit-msg` passes bad messages | regex too loose / hook non-blocking | Use the regex above; exit non-zero on fail [EXPLICIT] |
| Developers routinely `--no-verify` | `pre-commit` too slow | Move slow checks to `pre-push`/CI [INFERENCIA] |

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Required hook stages are present
- [ ] Conventional Commit policy is backed by `commit-msg` when enabled
- [ ] Install mode is explicit and non-destructive by default
- [ ] Hook commands are reviewable before installation
- [ ] Actionable output

## Usage

Example invocations:

- "/git-hook-integration" — Run the full git hook integration workflow
- "git hook integration on this project" — Apply to current context
- "compile a plan-only .githooks strategy with conventional commits" — Use
  the deterministic compiler contract

## Bundled Resources

- `assets/` contains schemas, policy models, validation catalog, install
  strategies, and the Markdown report template.
- `scripts/compile-git-hook-integration.py` compiles structured JSON into a
  deterministic Markdown plan.
- `scripts/check.sh` runs fixture checks for valid and invalid hook plans.


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not install, overwrite, or enable hooks unless the user explicitly asks
  for that mutation [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Hooks already managed by another tool | Read existing config; extend, do not overwrite [EXPLICIT] |
| Mutation requested but not authorized | Stay `plan-only`; surface exact commands for review [EXPLICIT] |
