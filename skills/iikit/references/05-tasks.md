<!-- distilled from alfa skills/iikit-05-tasks -->
<!-- >- -->
# Intent Integrity Kit Tasks

Generate an actionable, dependency-ordered tasks.md for the feature. [EXPLICIT]

**Anti-scope** — this phase ONLY produces the task breakdown. It does NOT write product code, run tests, create issues (that is `/iikit-08-taskstoissues`), or modify plan.md/spec.md. If plan.md is wrong, stop and route back to `/iikit-02-plan`. [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (basic mode — note TDD requirements for task ordering). [EXPLICIT]

If the constitution mandates TDD, every implementation task for a story MUST be preceded by its test task(s) in ID order; a story whose first task is an implementation task is a constitution violation — reorder before writing. [INFERENCIA]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 05 --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 05 -Json`
2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`. If missing plan.md: ERROR. If script exits with testify error: STOP and tell the user to run `/iikit-04-testify` first.
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.
4. Checklist gate per `checklist-gate.md`.

**Failure modes** — handle deterministically, do not improvise: [INFERENCIA]

| Symptom | Cause | Action |
|---------|-------|--------|
| `FEATURE_DIR` empty / no plan.md | Phase 02 not run | ERROR, route to `/iikit-02-plan` |
| script exits with testify error | Phase 04 not run | STOP, route to `/iikit-04-testify` |
| `needs_selection: true` | multiple active features | present table, set-active, re-run step 1 |
| script not found / non-zero exit | wrong cwd or uninstalled tile | report exact command + exit code, do not fabricate task output |
| both bash and pwsh fail | unsupported shell | report and ask user for environment |

## Plan Readiness Validation

1. **Tech stack**: verify plan.md has Language/Version defined (WARNING if missing — proceed but flag that file paths/extensions are inferred, not authoritative) [EXPLICIT]
2. **User story mapping**: verify each story in spec.md has acceptance criteria (story with zero criteria → WARNING, cannot generate verifiable tasks for it)
3. **Dependency pre-analysis**: identify shared entities used by multiple stories -> suggest Foundational phase

Report readiness per `formatting-guide.md` (Plan Readiness section). [EXPLICIT]

## Execution Flow

### 1. Load Documents

- **Required**: `plan.md`, `spec.md`
- **Optional**: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `tests/features/` (.feature files)

If .feature files exist (or legacy test-specs.md), tasks reference specific test IDs (e.g., "T012 [US1] Implement to pass TS-001"). [EXPLICIT]

### 2. Tessl Convention Consultation

If Tessl installed: query primary framework tile for project structure conventions and testing framework tile for test organization. Apply to file paths and task ordering. If not available: skip silently. [EXPLICIT]

### 3. Generate Tasks

Extract tech stack from plan.md, user stories from spec.md, entities from data-model.md, endpoints from contracts/, decisions from research.md. Organize by user story with dependency graph and parallel markers. [EXPLICIT]

**Coverage rule** — every required source artifact maps to at least one task; nothing in plan/spec/data-model/contracts is silently dropped. If an artifact yields no task (e.g., a documented-but-deferred endpoint), state that explicitly rather than omitting it. [INFERENCIA]

### 4. Task Format (REQUIRED)

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

- Checkbox: always `- [ ]`
- Task ID: sequential (T001, T002...), zero-padded to 3 digits, never reused or renumbered out of order [EXPLICIT]
- [P]: only if parallelizable (different files, no dependencies). Two tasks touching the SAME file MUST NOT both carry [P] — concurrent edits to one file are a merge hazard. [INFERENCIA]
- [USn]: required for user story tasks only (not Setup/Foundational/Polish)
- Description: clear action with exact file path (relative to repo root; one primary file per task — split if a task touches many)

**Examples**:
- `- [ ] T001 Create project structure per implementation plan` (setup, no story)
- `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py` (parallel, no story)
- `- [ ] T012 [P] [US1] Create User model in src/models/user.py` (parallel, story)
- `- [ ] T014 [US1] Implement UserService in src/services/user_service.py` (sequential, story)

**Wrong** — missing or misordered required elements:
- `- [ ] Create User model` (no ID, no story label)
- `T001 [US1] Create model` (no checkbox)
- `- [ ] [US1] Create User model` (no task ID)
- `- [ ] T020 [US1] [P] Create model` (order wrong: [P] must precede [USn])
- `- [ ] T030 [P] [US1] Update src/app.py` + `- [ ] T031 [P] [US2] Update src/app.py` (same file, both [P] — race)

**Traceability**: When referencing multiple test spec IDs, enumerate them explicitly as a comma-separated list. Do NOT use English prose ranges like "TS-005 through TS-010" — these break automated traceability checks.

**Correct**: `[TS-005, TS-006, TS-007, TS-008, TS-009, TS-010]`
**Wrong**: `TS-005 through TS-010`

### 5. Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites, complete before stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...) — tests -> models -> services -> endpoints -> integration
- **Final**: Polish & Cross-Cutting Concerns

Phases are sequential gates: no Phase 3 task may depend on an unfinished Phase 3+ task from a later story, and nothing in Setup/Foundational may depend on a story task (that would invert the gate). [INFERENCIA]

### 6. Task Organization

Map each component to its user story. Shared entities serving multiple stories go in Setup/Foundational. Each contract gets a contract test task. Story dependencies marked explicitly. [EXPLICIT]

### 7. Dependency Graph Validation

After generating, validate: [EXPLICIT]
1. **Circular dependencies**: detect cycles, ERROR if found with resolution options
2. **Orphan tasks**: warn about tasks with no dependencies and not blocking anything
3. **Critical path**: identify longest chain, suggest parallelization, list parallel batches per phase
4. **Phase boundaries**: no backward cross-phase dependencies
5. **Story independence**: warn on priority inversions (higher-priority depending on lower)

A clean graph is the acceptance bar for this phase: zero cycles, zero phase-boundary violations, every story task traceable to a spec story, every [P] file-disjoint. Cycles are a hard ERROR (block write); orphans and priority inversions are WARNINGs (write, but surface in the report). [INFERENCIA]

### 8. Write tasks.md

Use `tasks-template.md` with phases, dependencies, parallel examples, and implementation strategy. [EXPLICIT]

## Report

Output: path to tasks.md, total count, count per story, parallel opportunities, MVP scope suggestion, format validation. [EXPLICIT]

## Semantic Diff on Re-run

If tasks.md exists: preserve `[x]` completion status, map old IDs to new by similarity, warn about changes to completed tasks. Ask confirmation before overwriting. Use format from `formatting-guide.md` (Semantic Diff section). [EXPLICIT]

**Re-run edge cases** — never silently destroy completion state: [INFERENCIA]

| Scenario | Handling |
|----------|----------|
| Completed task no longer maps to any new task | Flag as "completed-but-dropped"; ask before removing — work may have shipped |
| New task has no old match | Mark as net-new; default unchecked |
| Old `[x]` task's description changed materially | Warn; keep `[x]` but surface the diff for user review |
| Ambiguous many-to-one ID mapping | Do NOT auto-merge completion; ask user to confirm mapping |

## Commit

```bash
git add specs/*/tasks.md
git commit -m "tasks: <feature-short-name> task breakdown"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects the new tasks: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```

Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 05 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 05 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Tasks generated! [EXPLICIT]
Next: [/clear → ] <next_step> (model: <tier>) [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-05-tasks" — Run the full iikit 05 tasks workflow
- "iikit 05 tasks on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]
- [ ] Dependency graph has zero cycles and zero phase-boundary violations [INFERENCIA]
- [ ] Every task ID is unique, sequential, and zero-padded; every [P] task is file-disjoint [INFERENCIA]
- [ ] Every spec story maps to ≥1 task; every required artifact is covered or explicitly deferred [INFERENCIA]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Assumes plan.md and spec.md are current and consistent; stale upstream docs produce stale tasks — this phase does not reconcile them [INFERENCIA]
- Parallelism markers are static hints from file-disjointness, not a runtime scheduler guarantee [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| spec.md story with no acceptance criteria | WARNING; generate placeholder-free skeleton task and flag the gap, do not invent criteria |
| Two stories share an entity | Hoist entity task to Foundational, mark both stories as dependents |
| Single story / trivial feature | Skip empty phases; never emit empty headers or TODO fillers |
| Contract present but no matching story | Flag orphan contract; propose a contract-test task or explicit deferral |
