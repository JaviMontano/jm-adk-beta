<!-- distilled from alfa skills/iikit-08-taskstoissues -->
<!-- >- -->
# Intent Integrity Kit Tasks to Issues

Convert existing tasks into dependency-ordered GitHub issues for project tracking.

**Scope**: read `tasks.md`, mint one GitHub issue per task, link dependencies. **Anti-scope** [EXPLICIT]: does NOT author tasks (that is phase 05), does NOT close/triage existing issues, does NOT push code, does NOT create projects/milestones/boards, and never targets a non-GitHub forge.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Treat free-text args as a scope filter (e.g. "only US1", "phases 3-4") layered on top of `tasks.md` — never as a substitute for it [EXPLICIT].

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 08 --json
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 08 -Json`

2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`. Extract path to **tasks.md**.
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.

**Stop conditions** [EXPLICIT]: if `tasks.md` is absent from `AVAILABLE_DOCS`, STOP — phase 05 has not run. If the script exits non-zero or emits non-JSON, STOP and surface stderr; do not improvise paths.

## GitHub Remote Validation

```bash
git config --get remote.origin.url
```

**CRITICAL**: Only proceed if remote is a GitHub URL (`git@github.com:` or `https://github.com/`). Otherwise ERROR.

Extract `OWNER/REPO` from this URL — it is the single source of truth for issue targeting. Do NOT read it from `gh` defaults, env vars, or prior context, which may point at a fork or unrelated repo [EXPLICIT]. If `git config` returns empty (no `origin`), STOP: there is no remote to target.

## Execution Flow

### 1. Parse tasks.md

Extract: Task IDs, descriptions, phase groupings, parallel markers [P], user story labels [USn], dependencies.

Apply any `$ARGUMENTS` scope filter here. If filtering yields zero tasks, STOP and report the filter that matched nothing rather than creating zero issues silently [EXPLICIT].

### 2. Create GitHub Issues

**Title format**: `[FeatureID/TaskID] [Story] Description` — feature-id extracted from `FEATURE_DIR` (e.g. `001-user-auth`).

**Body**: use template from `issue-body-template.md`. **Labels** (create if needed): `iikit`, `phase-N`, `us-N`, `parallel`.

**Idempotency** [EXPLICIT]: re-running this phase must not duplicate issues. Before creating, query existing open+closed issues for the `[FeatureID/TaskID]` title prefix (e.g. `gh issue list --search "[001-user-auth/T012] in:title" --state all`). If a match exists, reuse its number and skip creation — record it as "existing" in the report.

### 3. Create Issues (parallel)

Use the `Task` tool to dispatch issue creation in parallel — one subagent per chunk of tasks (split by phase or user story). Each subagent receives:
- The chunk of tasks to create issues for
- The feature-id, repo `OWNER/REPO`, and label set
- Instructions to use `gh issue create` if available, otherwise `curl` the GitHub API
- The idempotency rule from step 2 (check-before-create)

```bash
# Preferred:
gh issue create --title "[001-user-auth/T012] [US1] Create User model" --body "..." --label "iikit,phase-3,us-1"
```

**Concurrency guard** [EXPLICIT]: GitHub label creation is racy — two subagents creating the same label concurrently both 422. Mitigate by creating the full label set ONCE in the parent before dispatch (idempotent: ignore "already exists"), so subagents only attach. Cap concurrency (~5 subagents) to stay under secondary rate limits.

**CRITICAL**: Never create issues in repositories that don't match the remote URL. Each subagent must target the `OWNER/REPO` passed to it and verify before dispatching.

Collect all created issue numbers from subagents. Verify all returned successfully before proceeding. If some failed: report failures, continue with successful issues only.

### 4. Link Dependencies

After all issues exist, edit bodies to add cross-references using `#NNN` syntax. Skip dependency links for any issues that failed to create — and for the *upstream* side too: never write a `#NNN` that points at a task whose issue did not get created, or the link will dangle [EXPLICIT].

## Report

Output: issues created (count + numbers), reused/existing (count + numbers), failures (count + details), link to repo issues list.

## Acceptance Criteria

- [ ] Every in-scope task in `tasks.md` maps to exactly one issue (created or reused) — no duplicates, no omissions [EXPLICIT]
- [ ] All issues live in the `OWNER/REPO` derived from `remote.origin.url`, never elsewhere [EXPLICIT]
- [ ] Titles follow `[FeatureID/TaskID] [Story] Description`; labels `iikit`, `phase-N`, `us-N`, `parallel` exist and are attached correctly [EXPLICIT]
- [ ] Dependency `#NNN` cross-references resolve to created issues; no dangling references [EXPLICIT]
- [ ] Report reconciles: created + reused + failed == in-scope task count [EXPLICIT]

## Error Handling

| Condition | Response |
|-----------|----------|
| Not a GitHub remote / empty origin | STOP with error [EXPLICIT] |
| `tasks.md` missing | STOP — run phase 05 first [EXPLICIT] |
| Scope filter matches zero tasks | STOP, report the filter [EXPLICIT] |
| `gh` not authenticated | Fall back to `curl` + token; if no token, STOP [EXPLICIT] |
| Secondary rate limit (HTTP 403/429) | Back off, retry remaining chunk serially [EXPLICIT] |
| Issue creation fails | Report, continue with remaining issues [EXPLICIT] |
| Duplicate title detected | Reuse existing issue, mark "existing" [EXPLICIT] |
| Partial failure | Link dependencies for successful issues only [EXPLICIT] |

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 08 --json`
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 08 -Json`

Parse the JSON and present:
1. `next_step` will be null (workflow complete)
2. If `alt_steps` non-empty: list as alternatives
3. Append dashboard link

If on a feature branch, offer to merge:
- **A) Merge locally**: `git checkout main && git merge <branch>`
- **B) Create PR**: `gh pr create`
- **C) Skip**: user will handle it

Format:
```
Issues exported! Review in GitHub, assign team members, add to project boards.
- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations:

- "/iikit-08-taskstoissues" — Run the full iikit 08 taskstoissues workflow
- "iikit 08 taskstoissues on this project" — Apply to current context
- "iikit 08 only US1" — Scope to user story 1 tasks via `$ARGUMENTS` filter

### Worked example

`tasks.md` holds `T012 [P] [US1] Create User model (deps: T010)`; `FEATURE_DIR=specs/001-user-auth`; remote `git@github.com:acme/app.git`.
1. Labels `iikit, phase-3, us-1, parallel` ensured in `acme/app` (parent, idempotent).
2. Title-search finds no `[001-user-auth/T012]` → create:
   `gh issue create --title "[001-user-auth/T012] [US1] Create User model" --body "<template>" --label "iikit,phase-3,us-1,parallel"` → `#42`.
3. `T010` mapped to `#40` → edit `#42` body appending `Depends on: #40`.
4. Report: `created 1 (#42), reused 0, failed 0`.

## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes `tasks.md` exists and is well-formed per phase 05 output [EXPLICIT]
- Assumes the operator has push/issue-write scope on `OWNER/REPO` (`repo` scope for `gh`/token) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not assign owners, set milestones, or add issues to project boards — left to the human post-export [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| Re-run after partial success | Reuse existing issues by title; only create the gaps [EXPLICIT] |
| Circular task dependency | Create issues, cross-link both ways, flag the cycle in report [EXPLICIT] |
| Task with no dependencies | Create issue; skip step 4 linking for it [EXPLICIT] |
| Dependency on an out-of-scope/uncreated task | Omit the `#NNN`, note the unlinked dependency in report [EXPLICIT] |
