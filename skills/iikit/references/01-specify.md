<!-- distilled from alfa skills/iikit-01-specify -->
<!-- >- -->
# Intent Integrity Kit Specify

Create or update a feature specification from a natural language description. [EXPLICIT]

**Contract.** Input: free-text feature description (`$ARGUMENTS`). Output: `spec.md` (WHAT/WHY only), `checklists/requirements.md`, `qa/acceptance-criteria.md`, a feature branch + dir, refreshed dashboard. Side effects: creates a git branch and commit. Idempotent on re-run via semantic diff (§ Semantic Diff). [INFERENCIA]

**Anti-scope.** This phase does NOT design architecture, choose tech, write tasks, or implement — those are phases 02/05/07. No HOW. No code. If the description is a bug fix, it routes out (Step 0). [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (soft mode — warn if missing, proceed without). [EXPLICIT]

## Execution Flow

The text after `/iikit-01-specify` **is** the feature description. [EXPLICIT]

### 0. Bug-Fix Intent Detection

Before proceeding with feature specification, analyze the user description for bug-fix intent using **contextual analysis** (not keyword-only): [EXPLICIT]

**Bug-fix signals** (keywords in a fixing context): "fix", "crash", "broken", "bug", "doesn't work", "fails", "error" when used to describe existing broken behavior.

**NOT bug-fix** (keywords in a new-feature context): "Add error handling", "Implement crash recovery", "Create bug tracking" — these describe new capabilities, not fixes to existing behavior.

**Decision rule**: Is the primary intent to **fix existing broken behavior** or to **add new capability**? Keywords alone are insufficient — evaluate the full description.

If bug-fix intent is detected: [EXPLICIT]
1. Display: "This sounds like a bug fix. Consider using `/iikit-bugfix` instead."
2. Show example: `/iikit-bugfix '<the user description>'`
3. Ask the user to confirm: proceed with specification (it's genuinely a new feature) or switch to `/iikit-bugfix`
4. If the user confirms it is a new feature: proceed to Step 1
5. If the user wants bugfix: stop and suggest they run `/iikit-bugfix`

### 1. Generate Branch Name

Create 2-4 word action-noun name from description: [EXPLICIT]
- "I want to add user authentication" -> "user-auth"
- "Implement OAuth2 integration for the API" -> "oauth2-api-integration"

### 2. Create Feature Branch and Directory

Check current branch. If on main/master/develop, suggest creating feature branch (default). If already on feature branch, suggest skipping. [EXPLICIT]

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/create-new-feature.sh --json "$ARGUMENTS" --short-name "your-short-name"
# Add --skip-branch if user declined branch creation
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/create-new-feature.ps1 -Json "$ARGUMENTS" -ShortName "your-short-name"
# Add -SkipBranch if user declined
```

Parse JSON for `BRANCH_NAME`, `SPEC_FILE`, `FEATURE_NUM`. Only run ONCE per feature. [EXPLICIT]

**Failure modes** [INFERENCIA]
- Script exits non-zero or emits no JSON → stop; surface stderr verbatim, do not fabricate `SPEC_FILE`. [SUPUESTO]
- Branch name collides with existing branch → script should suffix `FEATURE_NUM`; if it errors, ask the user to pick a distinct short-name. [SUPUESTO]
- Dirty working tree blocks branch switch → instruct user to commit/stash first; never force-checkout. [INFERENCIA]
- Re-invoked after success (script run twice) → branch/dir already exist; skip creation, reuse parsed paths. [INFERENCIA]

### 3. Generate Specification

1. Parse user description — if empty: ERROR with usage example
2. Extract key concepts: actors, actions, data, constraints
3. For unclear aspects: make informed guesses. Only use `[NEEDS CLARIFICATION: question]` (max 3) when choice significantly impacts scope and no reasonable default exists. **Rationale:** cap at 3 to avoid clarification fatigue; defaulting is cheaper to correct downstream than blocking the spec. [INFERENCIA]
4. Fill User Scenarios with independently testable stories (P1, P2, P3 priorities)
5. Generate Functional Requirements (testable, with reasonable defaults)
6. Define Success Criteria (measurable, technology-agnostic)
7. Identify Key Entities (if data involved)

Write to `SPEC_FILE` using `spec-template.md` structure. [EXPLICIT]

### 4. Phase Separation Validation

Scan for implementation details per `phase-separation-rules.md` (Specification section). Auto-fix violations, re-validate until clean. [EXPLICIT]

### 5. Create Spec Quality Checklist

Generate `FEATURE_DIR/checklists/requirements.md` covering: content quality (no implementation details), requirement completeness, feature readiness. [EXPLICIT]

### 5b. Generate QA Acceptance Criteria

Generate `FEATURE_DIR/qa/acceptance-criteria.md` from the spec's SC-XXX success criteria: [EXPLICIT]

```markdown
# Acceptance Criteria — {Feature Name}
Generated from spec.md | {date}

## Success Criteria Checklist
- [ ] SC-001: {description} — Target: {measurable target}
- [ ] SC-002: {description} — Target: {measurable target}
...

## Traceability
| SC | Linked FR | Verifiable By |
|----|-----------|---------------|
| SC-001 | FR-001, FR-002 | Unit test / E2E |
```

Each SC-XXX from spec.md becomes a checkable acceptance criterion with a measurable target. Every SC must map to ≥1 FR; an SC with no linked FR is a defect (orphan criterion) — flag it, do not silently drop. [INFERENCIA]

### 6. Handle Clarifications

If `[NEEDS CLARIFICATION]` markers remain, present each as a question with options table and wait for user response. [EXPLICIT]

### 7. Report

Output: branch name, spec file path, checklist results, readiness for next phase. [EXPLICIT]

## Guidelines

- Focus on **WHAT** users need and **WHY** — avoid HOW
- Written for business stakeholders, not developers
- Success criteria: measurable, technology-agnostic, user-focused, verifiable

## Semantic Diff on Re-run

If spec.md already exists: extract semantic elements (stories, requirements, criteria), compare with new content per `formatting-guide.md` (Semantic Diff section), show downstream impact warnings, ask confirmation before overwriting. [EXPLICIT]

## Commit

```bash
git add specs/*/spec.md specs/*/checklists/requirements.md .specify/active-feature
git commit -m "spec: <feature-short-name> specification"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects the new spec: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 01 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 01 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Specification complete!
Next: [/clear → ] <next_step> (model: <tier>)
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Worked Example

Input: `"Let users reset their password via an emailed link that expires in 1 hour"` [INFERENCIA]
- Step 0: not a bug fix (new capability) → proceed.
- Step 1: branch `password-reset`.
- Step 3: actor=registered user; action=request reset, follow link, set new password; data=reset token (TTL 1h), email; one `[NEEDS CLARIFICATION]` candidate (lockout policy after N attempts) — defaulted to "no lockout in v1" since reasonable default exists, so no marker emitted.
- SC-001: "≥95% of valid reset requests deliver an email within 60s" → links FR-001 (issue token), FR-002 (send email).
- Output: `spec.md`, `requirements.md`, `acceptance-criteria.md`, branch + dashboard.

## Usage

Example invocations:

- "/iikit-01-specify" — Run the full iikit 01 specify workflow
- "iikit 01 specify on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Assumes a git repo is initialized and the `iikit-core` scripts are present at the `.tessl/...` paths; absent → Step 2 fails fast. [SUPUESTO]
- Constitution is soft-loaded: a missing constitution warns but does not block; downstream phases (02/03) may re-require it. [INFERENCIA]
- Produces a spec, not a contract — success criteria are measurable targets, not guarantees; final acceptance is human-gated (Step 6/7). [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | ERROR with usage example (Step 3.1); do not invent a feature |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, do not silently pick one |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Bug-fix intent | Route to `/iikit-bugfix` (Step 0); proceed only on explicit user override |
| `spec.md` already exists | Semantic diff + downstream-impact warning; confirm before overwrite (§ Semantic Diff) |
| On main/master/develop | Default to creating a feature branch; `--skip-branch` only if user declines |
| >3 genuine unknowns | Emit max 3 `[NEEDS CLARIFICATION]`; default the rest and note them in the spec |
| Detached HEAD / dirty tree | Stop before branch ops; ask user to checkout a branch or commit/stash |

## Step Acceptance Criteria
- `spec.md` contains no implementation detail (passes Step 4 phase-separation scan). [DOC]
- Every FR is independently testable; every SC is measurable and technology-agnostic. [DOC]
- Every SC traces to ≥1 FR in `acceptance-criteria.md`; no orphan criteria. [INFERENCIA]
- No `[NEEDS CLARIFICATION]` markers survive past Step 6 unanswered. [DOC]
- Branch, `SPEC_FILE`, and dashboard all exist and the commit landed before Step 7 reports done. [INFERENCIA]
