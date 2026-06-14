<!-- distilled from alfa skills/iikit-core -->
<!-- >- -->
# Intent Integrity Kit Core

Core skill providing project initialization, status checking, and workflow help. [EXPLICIT]

## User Input

```text
$ARGUMENTS
```

Parse the user input to determine which subcommand to execute. [EXPLICIT]

## Subcommands

1. **init** - Initialize intent-integrity-kit in a new or existing project
2. **status** - Show current project and feature status
3. **use** - Select the active feature for multi-feature projects
4. **help** - Display workflow phases and command reference

If no subcommand is provided, show help. [EXPLICIT]

**Dispatch contract**: match the first whitespace-delimited token of `$ARGUMENTS` case-insensitively against the four verbs; everything after it is that subcommand's own arguments. An unrecognized first token falls through to help (see Error Handling), NOT to init — only an *empty* `$ARGUMENTS` defaults to help. [INFERENCIA] This distinction matters: a typo like `inot` must not silently bootstrap a project. [SUPUESTO]

## Subcommand: init

Initialize intent-integrity-kit in the current directory. Handles the full project bootstrap: git init, optional GitHub repo creation, or cloning an existing repo. Optionally seeds the project backlog from an existing PRD/SDD document. [EXPLICIT]

### Argument Parsing

The `$ARGUMENTS` after `init` may include an optional path or URL to a PRD/SDD document (e.g., `/iikit-core init ./docs/prd.md` or `/iikit-core init https://example.com/prd.md`). If present, store it as `prd_source` for use in Step 6. [EXPLICIT]

### Execution Flow

> **Working directory**: All script paths below are relative to the project root. Before running any script, verify you are in the project root directory (`pwd` should show the directory containing `tessl.json` or `.tessl/`). If the script path doesn't resolve, find it: `find . -path "*/iikit-core/scripts/bash/git-setup.sh" 2>/dev/null || find ~/.tessl -path "*/iikit-core/scripts/bash/git-setup.sh" 2>/dev/null`

#### Step 0 — Detect environment

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/git-setup.sh --json
# Windows: pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/git-setup.ps1 -Json
```

JSON fields: `git_available`, `is_git_repo`, `has_remote`, `remote_url`, `is_github_remote`, `gh_available`, `gh_authenticated`, `has_iikit_artifacts`. [EXPLICIT]

If the script is missing or exits non-zero, do NOT proceed blind: report the failure and fall back to the `find` lookup in the Working-directory note, or stop and ask. Treat every field as present-or-false; never assume a true. [INFERENCIA]

If `gh_available` is false, suggest: "GitHub CLI (`gh`) is not installed. Install it from https://cli.github.com/ for the best experience. Proceeding with `curl` fallback for GitHub operations." [EXPLICIT]

If `gh_available` is true but `gh_authenticated` is false, GitHub *repo creation* will fail even though the CLI exists — prompt `gh auth login` before offering Option A's create step, or fall back to the `curl`/API path. [INFERENCIA]

#### Step 1 — Git/GitHub setup

**Auto-skip**: If `is_git_repo` + `has_remote`, skip to Step 2.

| Option | Requires | Action |
|--------|----------|--------|
| A) Init here | `git_available` | `git init`, then offer GitHub repo create (`gh` or API). Ask public/private. |
| B) Clone | `git_available` | Ask for URL/`owner/name`. `gh repo clone` or `git clone`. |
| C) Skip | — | Proceed without git. Warn: no assertion integrity hooks. |

Hide options whose prerequisites aren't met. If `git_available` is false, only C is available. [EXPLICIT]

**Decision — why offer Skip (C) at all:** git is the substrate for assertion-integrity hooks (Step 4), so C produces a degraded project. It is kept because air-gapped or evaluation runs are legitimate; the trade-off (no pre/post-commit validation) is surfaced as an explicit warning rather than blocked, so the user owns the choice. [INFERENCIA]

#### Step 2 — Check if already initialized

`test -f "CONSTITUTION.md"`

If present, jump to **If Already Initialized** (below) instead of re-running Steps 3–7; re-init must be non-destructive and must never overwrite an existing `CONSTITUTION.md` or `PREMISE.md`. [INFERENCIA]

#### Step 3 — Create directory structure

`mkdir -p .specify specs`

#### Step 4 — Initialize hooks

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/init-project.sh --json
# Windows: pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/init-project.ps1 -Json
```

Installs pre-commit (assertion validation) and post-commit (hash storage) hooks. [EXPLICIT]

If `git_user_configured` is `false`: ask the user for their name and email, then run: [EXPLICIT]
```bash
git config user.name "<name>"
git config user.email "<email>"
```
Do NOT guess from hostname or system username. [EXPLICIT]

#### Step 5 — Create PREMISE.md

If `PREMISE.md` does not exist, create it from the user's input using `premise-template.md`. Extract from the user's init description: [EXPLICIT]
- **What**: project description (from the user's input text)
- **Who**: target users (infer from context, or ask)
- **Why**: problem being solved (infer from context, or ask)
- **Domain**: business/technical domain
- **Scope**: system boundaries

Replace ALL bracket placeholders `[PLACEHOLDER]` with actual content. This is MANDATORY — init is not complete without PREMISE.md. [EXPLICIT]

**Who/Why missing**: if the init text gives no basis to infer target users or the problem, ASK one consolidated question rather than inventing them — fabricated premises corrupt every downstream phase (constitution → spec → tasks). Never leave a `[PLACEHOLDER]` to "fill later." [INFERENCIA]

After writing PREMISE.md, validate: [EXPLICIT]
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/validate-premise.sh --json "$PROJECT_PATH"
```
If validation fails (remaining placeholders or missing sections), fix and re-validate. [EXPLICIT]

#### Step 6 — Report

Directories created, hook status, PREMISE.md status. Suggest `/iikit-00-constitution`. [EXPLICIT]

#### Step 7 — Seed backlog from PRD (optional)

**Gate**: Requires `is_github_remote` AND user provided a PRD/SDD document. If not met, skip silently.

Follow the detailed procedure in `prd-seeding.md`: resolve input → read document → extract and order features → present for user confirmation → create GitHub issues. [EXPLICIT]

**Why gated on `is_github_remote`**: seeding writes GitHub issues, which require a GitHub remote; on a non-GitHub or remote-less repo the step has no target and is skipped silently rather than erroring. The `prd_source` from Step 0 is the second half of the gate — both must hold. [INFERENCIA] Never create issues without the explicit user-confirmation step in prd-seeding.md, even when both gate conditions pass. [EXPLICIT]

### If Already Initialized

Show constitution status, feature count, and suggest `/iikit-core status`. [EXPLICIT] Do not re-create directories or hooks destructively; report current state and hand off to `status`. [INFERENCIA]

### init — Acceptance Criteria (done = all true) [INFERENCIA]

- [ ] `.specify/` and `specs/` directories exist.
- [ ] Pre-commit and post-commit hooks installed (unless Option C / no-git was chosen — then warned).
- [ ] `git config user.name` and `user.email` are set (asked, never guessed).
- [ ] `PREMISE.md` exists, contains zero `[PLACEHOLDER]` tokens, and passes `validate-premise.sh`.
- [ ] Report (Step 6) printed with next-step suggestion `/iikit-00-constitution`.

### init — Worked Example [INFERENCIA]

Input: `/iikit-core init ./docs/prd.md` in an empty dir with `gh` authenticated.
→ Step 0 detects `git_available=true, is_git_repo=false`. → Step 1 Option A: `git init`, create private GitHub repo. → Steps 3–4 create dirs + hooks. → Step 5 builds `PREMISE.md` from the init text. → Step 7 gate passes (`is_github_remote=true` + `prd_source` set) → seeds backlog issues after confirmation.

## Subcommand: status

### Execution Flow

1. Run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase status --json
   # Windows: pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase status -Json
   ```

2. **Present results** (all logic is in script output — just display):
   - Project name, `feature_stage`, artifact status (`artifacts` object), checklist progress (`checklist_checked`/`checklist_total`), `ready_for` phase, `next_step`
   - If `clear_before` is true, prepend `/clear` suggestion. If `next_step` is null, report feature as complete.

**Do not compute state here** — `status` is a pure display of script output; re-deriving the stage in-model risks drifting from the hook-enforced source of truth. If the script errors or the project is uninitialized, suggest `init` rather than fabricating an empty status. [INFERENCIA]

## Subcommand: use

Select the active feature when multiple features exist in `specs/`. [EXPLICIT]

### User Input

The `$ARGUMENTS` after `use` is the feature selector: a number (`1`, `001`), partial name (`user-auth`), or full directory name (`001-user-auth`). [EXPLICIT]

### Execution Flow

1. Run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selector>
   # Windows: pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selector>
   ```
   Parse JSON for `active_feature` and `stage`.

2. **Report** active feature, stage, and suggest next command: `specified` → `/iikit-clarify` or `/iikit-02-plan` | `planned` → `/iikit-03-checklist` or `/iikit-05-tasks` | `testified` → `/iikit-05-tasks` | `tasks-ready` → `/iikit-07-implement` | `implementing-NN%` → `/iikit-07-implement` (resume) | `complete` → done. Suggest `/clear` before next skill when appropriate.

If no selector, no match, or ambiguous match: show available features with stages and ask user to pick. [EXPLICIT] Never auto-pick on ambiguity — selecting the wrong active feature silently misroutes all subsequent phase commands. [INFERENCIA]

**Selector precedence**: a zero-padded number (`001`) and its bare form (`1`) both resolve to `001-*`; a partial name matches as a substring of the directory name. If a single repo has features `001-user-auth` and `011-user-billing`, the partial `user` is ambiguous → list both. [INFERENCIA]

## Subcommand: help (also default when no subcommand)

Display the workflow reference from `help-reference.md` verbatim. [EXPLICIT]

## Resources

- `spec-template.md`, `plan-template.md`, `agent-file-template.md` — feature scaffolding
- `prd-issue-template.md` — PRD backlog seeding
- `help-reference.md` — workflow command reference

## Error Handling

Unknown subcommand → show help. Not in a project → suggest `init`. Git unavailable → warn but continue. [EXPLICIT]

## Usage

Example invocations: [EXPLICIT]

- "/iikit-core" — Run the full iikit core workflow
- "iikit core on this project" — Apply to current context


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

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| Unknown first token (`inot`) | Fall through to help; do NOT init [INFERENCIA] |
| `init` on existing project | Non-destructive: report state, never overwrite CONSTITUTION.md / PREMISE.md [INFERENCIA] |
| Setup script missing / non-zero exit | Stop or `find` fallback; never proceed assuming success [INFERENCIA] |
| `gh` present but not authenticated | Prompt `gh auth login` or use curl/API path before repo create [INFERENCIA] |
| PREMISE validation fails | Fix placeholders/sections and re-run `validate-premise.sh`; init not done until pass [EXPLICIT] |
| Ambiguous `use` selector | List matches with stages; ask — never auto-pick [INFERENCIA] |
| `status` on uninitialized dir | Suggest `init` instead of emitting a blank status [INFERENCIA] |

## Failure Modes to Avoid [INFERENCIA]

- Guessing `git` identity from hostname/username (Step 4 forbids it).
- Leaving any `[PLACEHOLDER]` in PREMISE.md "to fill later."
- Creating GitHub issues (Step 7) without the explicit user-confirmation gate.
- Re-deriving feature stage in-model instead of trusting script output.
