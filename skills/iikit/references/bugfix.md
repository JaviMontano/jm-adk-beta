<!-- distilled from alfa skills/iikit-bugfix -->
<!-- >- -->
# Intent Integrity Kit Bugfix

Report a bug against an existing feature, create a structured `bugs.md` record, and generate fix tasks in `tasks.md`. [EXPLICIT]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (soft mode — warn if missing, proceed without). [EXPLICIT]

## Execution Flow

The text after `/iikit-bugfix` is either a `#number` (GitHub issue) or a text bug description. [EXPLICIT]

### 1. Parse Input

Determine the input type: [EXPLICIT]

- **`#number` pattern** (e.g., `#42`): GitHub inbound flow (Step 2a)
- **Text description**: Text description flow (Step 2b)
- **Empty**: ERROR with usage example: `/iikit-bugfix 'Login fails when email contains plus sign'` or `/iikit-bugfix #42`

If input contains BOTH `#number` and text, prioritize the `#number` and warn that text is ignored. [EXPLICIT]

### 2a. GitHub Inbound Flow

1. Fetch issue: use `gh issue view <number> --json title,body,labels` if available, otherwise `curl` the GitHub API (`GET /repos/{owner}/{repo}/issues/{number}`). [EXPLICIT]
2. If fetch fails (issue not found, auth error, closed issue, or no GitHub remote): ERROR with a clear message + remediation, and suggest re-running with a text description instead. Do NOT silently continue with a half-populated record. [EXPLICIT]
3. Map fields: [EXPLICIT]
   - `title` → bug description
   - `body` → reproduction steps (preserve markdown; if empty, fall back to Step 5 prompt)
   - `labels` → severity. Precedence is highest-wins, evaluated in order: "critical"/"sev1"/"p0" → critical; "high"/"priority"/"p1" → high; "low"/"minor" → low; "bug" or no match → medium. First matching tier wins so a `bug,critical` pair resolves to critical, not medium. [INFERENCE]
4. Store the issue number for the GitHub Issue field in bugs.md. [EXPLICIT]
5. Continue to Step 3. [EXPLICIT]

### 2b. Text Description Flow

1. Store the text as the bug description
2. Continue to Step 3

### 3. Select Target Feature

Run feature listing: [EXPLICIT]

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/bugfix-helpers.sh --list-features
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/bugfix-helpers.ps1 --list-features
```

Parse the JSON array. If empty: ERROR with "No features found. Run `/iikit-01-specify` first to create a feature." [EXPLICIT]

Present a numbered table of features: [EXPLICIT]

| # | Feature | Stage |
|---|---------|-------|
| 1 | 001-user-auth | implementing-50% |
| 2 | 002-api-gateway | specified |

Prompt user to select a feature by number. [EXPLICIT]

### 4. Validate Feature

After selection, validate: [EXPLICIT]

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/bugfix-helpers.sh --validate-feature "<feature_dir>"
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/bugfix-helpers.ps1 --validate-feature "<feature_dir>"
```

If invalid: ERROR with the message from the JSON response. [EXPLICIT]

### 5. Gather Bug Details

**For text input (2b):** [EXPLICIT]
- Prompt for **severity** (one of): `critical` = data loss / outage / security, no workaround; `high` = core flow broken, workaround painful; `medium` = degraded but usable (default); `low` = cosmetic / edge.
- Prompt for **reproduction steps**: numbered list. If the user supplies none, record `_(not provided)_` rather than blocking — investigation (T-BNNN) can fill it later.

**For GitHub inbound (2a):** [EXPLICIT]
- Severity is pre-filled from labels (Step 2a.3). Confirm with the user only if no label matched (resolved to default `medium`).
- Reproduction steps are pre-filled from issue body. Confirm with user; do not re-prompt if body is non-empty.

Acceptance for this step: severity ∈ {critical,high,medium,low} and a description string is non-empty before continuing. [INFERENCE]

### 6. Generate Bug ID

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/bugfix-helpers.sh --next-bug-id "<feature_dir>"
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/bugfix-helpers.ps1 --next-bug-id "<feature_dir>"
```

The helper derives the next ID by scanning existing `BUG-NNN` markers in `bugs.md`. IDs are monotonic and never reused, even after a bug is closed — gaps are expected and acceptable. The ID is allocated here but only persisted in Step 7; if the run aborts between, the next run reuses the same ID (no orphan). [INFERENCE]

### 7. Write bugs.md

Create or append to `<feature_dir>/bugs.md` using the template at `bugs-template.md`. [EXPLICIT]

Fill in:
- **BUG-ID**: from Step 6
- **Reported**: today's date (YYYY-MM-DD)
- **Severity**: from Step 5
- **Status**: `reported`
- **GitHub Issue**: `#number` if from GitHub inbound, `_(none)_` otherwise
- **Description**: bug description
- **Reproduction Steps**: from Step 5
- **Root Cause**: `_(empty until investigation)_`
- **Fix Reference**: `_(empty until implementation)_`

If `bugs.md` already exists, append with `---` separator before the new entry. Do NOT modify existing entries. [EXPLICIT]

If `bugs.md` does not exist, create it with the header `# Bug Reports: <feature-name>` followed by the entry. [EXPLICIT]

### 8. Outbound GitHub Issue (Text Input Only)

For text-input bugs only (NOT for GitHub inbound — issue already exists): [EXPLICIT]

1. Create issue: use `gh issue create --title "<description>" --body "<bugs.md entry content>" --label "bug"` if `gh` available, otherwise `curl` the GitHub API (`POST /repos/{owner}/{repo}/issues`)
2. Store returned issue number in the bugs.md GitHub Issue field
3. If no GitHub remote configured: warn that GitHub issue creation was skipped, proceed with local workflow

### 9. Assess TDD Requirements

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh assess-tdd "CONSTITUTION.md"
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/testify-tdd.ps1 assess-tdd "CONSTITUTION.md"
```

Parse JSON response for `determination` field. [EXPLICIT]

### 10. BDD/TDD Flow (If Mandatory)

If TDD is mandatory (`determination` = `mandatory`): [EXPLICIT]

1. Create `<feature_dir>/tests/features/` if it doesn't exist
2. Create `<feature_dir>/tests/features/bugfix_<BUG-NNN>.feature`:
   ```gherkin
   @BUG-NNN
   Feature: Bug fix for BUG-NNN — <description>
     Scenario: <description>
       Given <conditions that trigger the bug>
       When <action that causes incorrect behavior>
       Then <expected correct behavior>
   ```
3. Re-hash the features directory:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh rehash "<feature_dir>/tests/features"
   ```
4. **Verify hash was stored** — if result is NOT `valid`, STOP and report error:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh verify-hash "<feature_dir>/tests/features"
   ```
5. Continue to Step 11 with TDD task variant

### 11. Generate Bug Fix Tasks

**Bug fix tasks use the `T-B` prefix** (e.g., T-B001, T-B002) to distinguish them from regular tasks (T001, T002). This is mandatory — the dashboard and parsers rely on the `T-B` prefix to identify bug fix tasks and calculate implementation progress correctly.

Get next task IDs: [EXPLICIT]

**Unix/macOS/Linux:**
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/bugfix-helpers.sh --next-task-ids "<feature_dir>" <count>
```
**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/bugfix-helpers.ps1 --next-task-ids "<feature_dir>" <count>
```

**Non-TDD task set** (count = 3):
```markdown
## Bug Fix Tasks

- [ ] T-BNNN [BUG-NNN] Investigate root cause for BUG-NNN: <description>
- [ ] T-BNNN+1 [BUG-NNN] Implement fix for BUG-NNN: <description>
- [ ] T-BNNN+2 [BUG-NNN] Write regression test for BUG-NNN: <description>
```

**TDD task set** (count = 2):
```markdown
## Bug Fix Tasks

- [ ] T-BNNN [BUG-NNN] Implement fix for BUG-NNN referencing test spec TS-NNN: <description>
- [ ] T-BNNN+1 [BUG-NNN] Verify fix passes test TS-NNN for BUG-NNN: <description>
```

If GitHub issue is linked, include reference in task descriptions (e.g., `(GitHub #42)`). [EXPLICIT]

Append to existing `<feature_dir>/tasks.md`. If tasks.md does not exist, create it with: [EXPLICIT]
```markdown
# Tasks: <feature-name>

## Bug Fix Tasks

[tasks here]
```

Do NOT modify existing entries or task IDs in tasks.md. [EXPLICIT]

### 12. Commit

```bash
git add specs/*/bugs.md specs/*/tasks.md specs/*/tests/features/
git commit -m "bugfix: <BUG-ID> <short-description>"
```

### 13. Dashboard Refresh (optional, never blocks)

Regenerate the dashboard so the pipeline reflects the new bug and tasks: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

### 14. Report

Output a summary: [EXPLICIT]

```
Bug reported successfully! [EXPLICIT]

  Bug ID:      BUG-NNN
  Feature:     <feature-name>
  Severity:    <severity>
  GitHub Issue: #number (or N/A)
  Tasks:       T-BNNN through T-BNNN+N

Files modified: [EXPLICIT]
  - <feature_dir>/bugs.md (created/appended)
  - <feature_dir>/tasks.md (appended)
  - <feature_dir>/tests/features/bugfix_BUG-NNN.feature (created, TDD only)

Next step:
  Run: bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase bugfix --json
  Parse `next_step` (will be /iikit-07-implement) and `model_tier`.
  Include `model_tier` for next_step and any alt_steps so user knows best model per option.
  - <next_step> — runs in bugfix mode (relaxed gates: no checklist or plan required, traces to bugs.md instead of spec)
  
  - Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Error Handling

| Condition | Response |
|-----------|----------|
| Empty input | ERROR with usage example |
| No features found | ERROR: "Run `/iikit-01-specify` first" |
| Feature validation failed | ERROR with specific message |
| GitHub API unreachable | Fall back: `gh` → `curl` GitHub API → skip with WARN |
| GitHub issue not found | ERROR with "verify issue number" |
| TDD mandatory | Auto-generate `bugfix_<BUG-NNN>.feature` (Step 10); STOP only if `verify-hash` ≠ `valid` |
| Existing bugs.md | Append without modifying existing entries |
| Existing tasks.md | Append without modifying existing entries |

## Usage

Example invocations: [EXPLICIT]

- "/iikit-bugfix" — Run the full iikit bugfix workflow
- "/iikit-bugfix 'Login fails when email contains plus sign'" — text inbound
- "/iikit-bugfix #42" — GitHub inbound from issue 42

## Validation Gate

The run is complete only when ALL hold: [EXPLICIT]

- [ ] A `BUG-NNN` entry exists in `<feature_dir>/bugs.md` with Status `reported`, a non-empty Severity ∈ {critical,high,medium,low}, and a Reported date. [EXPLICIT]
- [ ] Existing `bugs.md` / `tasks.md` entries are byte-for-byte unchanged; the new content was appended, not rewritten. [EXPLICIT]
- [ ] Generated tasks carry the `T-B` prefix and a `[BUG-NNN]` back-reference. [EXPLICIT]
- [ ] If TDD `mandatory`: a `bugfix_<BUG-NNN>.feature` file exists and `verify-hash` returned `valid`. [EXPLICIT]
- [ ] No placeholder leakage (`<description>`, `TBD`, `NNN`) in committed files. [EXPLICIT]

## Assumptions & Limits

- A feature directory already exists (created by `/iikit-01-specify`); this skill records bugs, it does not create features. [EXPLICIT]
- GitHub steps are best-effort: absent `gh`/`curl`/remote, the local workflow still completes with a WARN. [EXPLICIT]
- This skill REPORTS and PLANS a bug; it does NOT implement the fix — that is `/iikit-07-implement`. Writing fix code here is out of scope. [INFERENCE]
- English-language artifacts unless the constitution specifies otherwise. [EXPLICIT]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty input | ERROR with usage example (Step 1). [EXPLICIT] |
| Both `#number` and text given | Prioritize `#number`; WARN that text is ignored (Step 1). [EXPLICIT] |
| `#number` references a closed/missing/foreign-repo issue | ERROR; suggest text-description re-run (Step 2a). [EXPLICIT] |
| GitHub label set has no severity match | Default `medium`; flag for user confirmation (Step 2a.3). [INFERENCE] |
| No features found | ERROR: "Run `/iikit-01-specify` first" (Step 3). [EXPLICIT] |
| Duplicate bug (same description already `reported`) | Proceed but WARN — IDs are not deduplicated; surfacing the prior BUG-ID helps the user decide. [INFERENCE] |
| Run aborts after Step 6 (ID issued, not written) | Safe: next run re-derives the same ID by scanning `bugs.md`; no orphan. [INFERENCE] |
| TDD `mandatory` but `rehash`/`verify-hash` ≠ `valid` | STOP and report; do not generate TDD tasks against an unverified spec (Step 10.4). [EXPLICIT] |
| `git` absent or repo dirty mid-commit | Step 12 fails non-fatally; report the unstaged files so the user can commit manually. [INFERENCE] |
| Dashboard regen fails | Never blocks; the bug record is already persisted (Step 13). [EXPLICIT] |
