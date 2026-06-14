<!-- distilled from alfa skills/iikit-04-testify -->
<!-- >- -->
# Intent Integrity Kit Testify

Generate executable Gherkin `.feature` files from requirement artifacts before implementation. Enables TDD by creating hash-locked BDD scenarios that serve as immutable acceptance criteria. [EXPLICIT]

**Position in pipeline**: phase 04, after `01-specify` + `02-plan` (+ optional `03`), before `05-implement`. This skill is the requirements→tests boundary: everything upstream is intent, everything downstream is held to the scenarios locked here. [INFERENCIA]

**Why hash-lock the scenarios** (decision): tests authored from requirements are only trustworthy if they cannot be silently edited to match buggy code. The SHA256 hash + git note make tampering detectable at implement time. Trade-off: legitimate requirement changes force a re-run of this skill (intentional — change must flow from spec, not from the test file). [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

This skill accepts **no user input parameters** — it reads artifacts automatically. Any text in `$ARGUMENTS` is ignored, not treated as a feature selector; feature selection happens via the prerequisites `needs_selection` flow below. [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (basic mode), then perform TDD assessment: [EXPLICIT]

**Scan for TDD indicators**:
- Strong (MUST/REQUIRED + "TDD", "test-first", "red-green-refactor") -> **mandatory**
- Moderate (MUST + "test-driven", "tests before code") -> **mandatory**
- Implicit (SHOULD + "quality gates", "coverage requirements") -> **optional**
- Prohibition (MUST + "test-after", "no unit tests") -> **forbidden** (ERROR, halt)
- None found -> **optional**

**Determination affects only the report, never generation**: `mandatory`/`optional` both proceed to generate `.feature` files; the label tells the user whether downstream `05-implement` will hard-block on missing tests. `forbidden` is the only branch that halts before generation. [INFERENCIA] On conflicting signals (e.g. one MUST for TDD and one MUST against), treat as **forbidden** and surface both citations — a constitution that both requires and prohibits test-first is a constitution bug the user must resolve, not one this skill should silently pick a side on. [SUPUESTO]

Report per `formatting-guide.md` (TDD Assessment section). [EXPLICIT]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 04 --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 04 -Json`
2. Parse for `FEATURE_DIR` and `AVAILABLE_DOCS`. Require **plan.md** and **spec.md** (ERROR if missing).
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.
4. Checklist gate per `checklist-gate.md`.

## Acceptance Scenario Validation

Search spec.md for Given/When/Then patterns. If none found: ERROR with `Run: /iikit-clarify`. [EXPLICIT] Rationale: this skill transforms scenarios, it does not invent them — generating Gherkin from a spec that has no acceptance scenarios would fabricate untraceable tests, defeating the integrity guarantee. Clarify is the correct upstream fix. [INFERENCIA]

## Execution Flow

### 1. Load Artifacts

- **Required**: `spec.md` (acceptance scenarios), `plan.md` (API contracts, tech stack)
- **Optional**: `data-model.md` (validation rules)

### 2. Generate Gherkin Feature Files

Create `.feature` files in `FEATURE_DIR/tests/features/`: [EXPLICIT]

**Output directory**: `FEATURE_DIR/tests/features/` (create if it does not exist)

**File organization**: Generate one `.feature` file per user story or logical grouping. Use descriptive filenames (e.g., `login.feature`, `user-management.feature`). [EXPLICIT] One-file-per-story (decision) keeps `@US-XXX` feature-level tags unambiguous and lets diffs map cleanly to a single requirement; trade-off is more files, accepted because BDD runners glob the directory anyway. Filenames are kebab-case, lowercase, ASCII — no spaces, no story IDs in the name (the `@US-XXX` tag carries the ID). [SUPUESTO]

#### 2.1 Gherkin Tag Conventions

Every scenario MUST include traceability tags: [EXPLICIT]
- `@TS-XXX` — test spec ID (sequential, unique across all .feature files)
- `@FR-XXX` — functional requirement from spec.md
- `@SC-XXX` — success criteria from spec.md
- `@US-XXX` — user story reference
- `@P1` / `@P2` / `@P3` — priority level
- `@acceptance` / `@contract` / `@validation` — test type

**SC-XXX coverage rule**: For each SC-XXX in spec.md, ensure at least one scenario is tagged with the corresponding `@SC-XXX`. If an FR scenario already covers the success criterion, add the `@SC-XXX` tag to that scenario rather than creating a duplicate. [EXPLICIT]

**Tag invariants** (must hold across all generated files): [INFERENCIA]
- `@TS-XXX` is globally unique and never reused — even for a deprecated scenario the ID is retired, not recycled (the hash and coverage matrix key on it).
- Exactly one priority tag (`@P1|@P2|@P3`) and one test-type tag (`@acceptance|@contract|@validation`) per scenario; zero or two is a generation defect.
- Every `@FR-XXX`/`@SC-XXX`/`@US-XXX` on a scenario must resolve to an ID that actually exists in spec.md — a tag pointing at a non-existent requirement is worse than no tag (false traceability). Drop or correct it; do not emit a dangling reference.
- Priority derives from the source requirement's priority in spec.md; if the source is unprioritized, default `@P2` and note it. [SUPUESTO]

Feature-level tags for shared metadata: [EXPLICIT]
- `@US-XXX` on the Feature line for the parent user story

#### 2.2 Transformation Rules

**From spec.md — Acceptance Tests**: For each Given/When/Then scenario, generate a Gherkin scenario.

Use `testspec-template.md` as the Gherkin file template. For transformation examples, advanced constructs (Background, Scenario Outline, Rule), and syntax validation rules, see `gherkin-reference.md`. [EXPLICIT]

**Worked example** — spec.md scenario → tagged Gherkin: [INFERENCIA]

> spec.md (FR-002, SC-001, US-003): *"Given a registered user with a valid password, when they submit the login form, then a session is created and they land on the dashboard."*

```gherkin
@TS-007 @FR-002 @SC-001 @US-003 @P1 @acceptance
Scenario: Registered user logs in with valid credentials
  Given a registered user "ana@example.com" with a valid password
  When she submits the login form
  Then a session is created
  And she lands on the dashboard
```

**Transformation rules made explicit**: [INFERENCIA]
- One spec scenario → one `Scenario` (or one `Scenario Outline` row-set when the spec enumerates variants). Do not collapse distinct Given/When/Then triples into a shared scenario — it destroys per-row traceability.
- Bind ambiguous nouns to concrete example values (`"ana@example.com"`) so steps are executable, not abstract.
- Negative/error paths in the spec become their own scenarios tagged `@validation`, never an afterthought in the happy-path scenario.
- Contract assertions from plan.md (status codes, schemas) become `@contract` scenarios; keep them separate from `@acceptance` behavior scenarios.

### 3. Add DO NOT MODIFY Markers

Add an HTML comment at the top of each `.feature` file: [EXPLICIT]
```gherkin
# DO NOT MODIFY SCENARIOS
# These .feature files define expected behavior derived from requirements.
# During implementation:
#   - Write step definitions to match these scenarios
#   - Fix code to pass tests, don't modify .feature files
#   - If requirements change, re-run /iikit-04-testify
```

### 4. Idempotency

If `tests/features/` already contains `.feature` files: [EXPLICIT]
- Preserve existing scenario tags (TS-XXX) where the source scenario is unchanged
- Add new scenarios for new requirements
- Mark removed scenarios as deprecated (comment out with `# DEPRECATED:`)
- Show diff summary of changes

**Idempotency contract** (decision: stable IDs, additive-by-default): re-running on an unchanged spec is a no-op that re-emits identical content and therefore an identical hash. [INFERENCIA] "Unchanged source scenario" is matched by semantic content, not by text equality — reflowing whitespace in the spec must not churn TS-XXX assignments. Never re-number existing `@TS-XXX` to close gaps left by deprecation; gaps are expected and harmless. A run that changes the hash without any spec change is a bug, not idempotency. [SUPUESTO]

### 5. Store Assertion Integrity Hash

**CRITICAL**: Store SHA256 hash of assertion content in both locations:

```bash
# Context.json (auto-derived from features directory path)
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh store-hash "FEATURE_DIR/tests/features"

# Git note (tamper-resistant backup — uses first .feature file for note attachment)
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/testify-tdd.sh store-git-note "FEATURE_DIR/tests/features"
```

**Windows (PowerShell):**
```powershell
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/testify-tdd.ps1 store-hash "FEATURE_DIR/tests/features"
pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/testify-tdd.ps1 store-git-note "FEATURE_DIR/tests/features"
```

The implement skill verifies this hash before proceeding, blocking if `.feature` file assertions were tampered with. [EXPLICIT]

**Hash scope and failure modes**: [INFERENCIA]
- The hash covers **assertion content** (steps + tags), not surrounding comments or file ordering — so adding/editing a `# DO NOT MODIFY` banner does not break the lock, but editing a `Then` step does. This is deliberate: the lock guards behavior, not formatting.
- Both writes (context.json and git note) must succeed. If `store-git-note` fails because the repo has **no commits yet** or the features dir has no `.feature` file, report it and do not claim LOCKED — a hash in context.json alone is mutable and not tamper-resistant. [SUPUESTO]
- Storing the hash is the **last** generation step: any later edit to a `.feature` file invalidates the lock and must trigger a re-run, not a manual re-hash. Manually re-hashing edited assertions silently defeats the entire integrity mechanism — never do it.

### 5b. Generate QA Test Coverage Matrix

Generate `FEATURE_DIR/qa/test-coverage.md` with FR→TS traceability: [EXPLICIT]

```markdown
# Test Coverage Matrix — {Feature Name}
Generated from .feature files | {date} [EXPLICIT]

## FR → TS Traceability
| Requirement | Tests | Coverage |
|-------------|-------|----------|
| FR-001 | TS-001, TS-002, TS-003 | 3 scenarios |
| FR-002 | TS-004 | 1 scenario |
| FR-003 | — | UNTESTED |

## Summary
- Total FR: {N} | Covered: {M} | Untested: {K}
- Coverage: {M/N * 100}%
- Assertion Hash: {sha256}
```

Each FR-XXX from spec.md is matched against @FR-XXX tags in .feature files. Untested FRs are flagged. [EXPLICIT]

### 6. Report

Output: TDD determination, scenario counts by source (acceptance/contract/validation), output directory path, number of `.feature` files generated, hash status (LOCKED). [EXPLICIT]

## Error Handling

| Condition | Response |
|-----------|----------|
| No constitution | ERROR: Run /iikit-00-constitution |
| TDD forbidden (or conflicting MUST signals) | ERROR with both citations, halt before generation |
| No plan.md | ERROR: Run /iikit-02-plan |
| No spec.md | ERROR: Run /iikit-01-specify |
| No acceptance scenarios | ERROR: Run /iikit-clarify |
| `.feature` syntax error | FIX: Auto-correct and report the correction; never emit invalid Gherkin |
| Prereq script absent / wrong OS | ERROR: surface the missing path; do not fabricate `FEATURE_DIR`/`AVAILABLE_DOCS` |
| `needs_selection` but `features` empty | ERROR: no feature to testify; run an upstream phase first |
| Tag references non-existent FR/SC/US | Drop or correct the tag; never emit a dangling reference |
| `store-git-note` fails (no commit / no `.feature`) | Report; status is NOT LOCKED — do not claim integrity |
| Tampered hash on re-run with unchanged spec | Generation bug: investigate; do not manually re-hash |

## Commit

```bash
git add specs/*/tests/features/ specs/*/context.json .specify/context.json
git commit -m "testify: <feature-short-name> BDD scenarios"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects the new testify artifacts: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```

Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 04 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 04 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Feature files generated! [EXPLICIT]
Next: [/clear → ] <next_step> (model: <tier>) [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-04-testify" — Run the full iikit 04 testify workflow
- "iikit 04 testify on this project" — Apply to current context


## Validation Gate

Skill-specific acceptance criteria — all must hold before reporting LOCKED: [EXPLICIT]
- [ ] Every `@SC-XXX` in spec.md is covered by ≥1 tagged scenario (matrix shows 0 untested SC) [EXPLICIT]
- [ ] Every generated scenario carries unique `@TS-XXX` + exactly one priority + one test-type tag [INFERENCIA]
- [ ] No tag references an FR/SC/US absent from spec.md (no dangling traceability) [INFERENCIA]
- [ ] Every `.feature` file parses as valid Gherkin and starts with the DO NOT MODIFY banner [EXPLICIT]
- [ ] Assertion hash stored in BOTH context.json and git note; status reported as LOCKED [EXPLICIT]
- [ ] `qa/test-coverage.md` regenerated and consistent with emitted tags [EXPLICIT]
- [ ] No placeholder content (TBD, TODO, `<...>`) left in any `.feature` file [EXPLICIT]

## Assumptions & Limits

- Requirements live in `spec.md`/`plan.md` at the resolved `FEATURE_DIR`; this skill does not read source code to infer behavior — untested-but-implemented behavior is out of scope by design. [INFERENCIA]
- Generates scenario specs only — it writes `.feature` files, never step definitions or production code (that is `05-implement`). [EXPLICIT]
- Anti-scope: does not run the tests, measure runtime pass/fail, or compute code coverage — "coverage" here means requirement→scenario mapping, not line/branch coverage. [INFERENCIA]
- English-language Gherkin keywords assumed unless the constitution specifies a localized dialect. [SUPUESTO]
- Quality of generated tests is bounded by spec.md quality: vague acceptance scenarios yield vague tests. It does not replace domain-expert review of the scenarios. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Spec has FRs but zero Given/When/Then | ERROR → /iikit-clarify (cannot invent scenarios) |
| Two spec scenarios describe identical behavior | Emit once; tag with both FR/SC IDs rather than duplicating |
| Spec scenario maps to no FR/SC/US | Generate scenario, flag the missing requirement link in the report |
| Requirement removed since last run | Comment out as `# DEPRECATED:`, retire its TS-XXX (never reuse) |
| Empty or minimal spec input | Request clarification before generating |
| Conflicting requirements in spec | Flag the conflict explicitly; do not silently pick one path |
| Out-of-scope request (e.g. "write the code") | Redirect to /iikit-05-implement |
