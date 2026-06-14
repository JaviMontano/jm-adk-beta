<!-- distilled from alfa skills/iikit-06-analyze -->
<!-- >- -->
# Intent Integrity Kit Analyze

Non-destructive cross-artifact consistency analysis across spec.md, plan.md, and tasks.md. [EXPLICIT]

## Operating Constraints

- **READ-ONLY** (exceptions: writes `analysis.md`, `.specify/score-history.json`, and regenerated `QA-PLAN.md`/`.specify/qa-plan.json`/dashboard). Never modify spec, plan, or task files. [EXPLICIT]
- **Constitution is non-negotiable**: conflicts are automatically CRITICAL. [EXPLICIT]
- **Diagnostic, not corrective**: this phase reports and scores; it never edits artifacts to fix findings. Remediation is offered (step 7) but applied only by a later explicit user action. [INFERENCIA]

**Anti-scope** (route elsewhere, do not absorb): resolving ambiguity by asking the user → `clarify`; authoring missing checklist items → `03-checklist`; writing tests → `04-testify`; generating tasks → `05-tasks`; implementing code → `07-implement`. Analyze surfaces these gaps as findings; it does not close them. [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (basic mode — ERROR if missing). Extract principle names and normative statements. [EXPLICIT]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 06 --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 06 -Json`
2. Derive paths: SPEC, PLAN, TASKS from FEATURE_DIR. ERROR if any missing.
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.
4. Checklist gate per `checklist-gate.md`.

## Execution Steps

### 0. Pre-Analysis: Generate QA Plan

Before analysis, regenerate the QA Plan to ensure cross-feature quality data is current: [EXPLICIT]
```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/sdd-qa-plan.js" .
```
This updates `QA-PLAN.md` and `.specify/qa-plan.json` with latest DoD status, AC coverage, and gate state. The analysis then uses this data for cross-artifact validation. [EXPLICIT]

### 1. Load Artifacts (Progressive)

From spec.md: overview, requirements, user stories, edge cases. [EXPLICIT]
From plan.md: architecture, data model refs, phases, constraints. [EXPLICIT]
From tasks.md: task IDs, descriptions, phases, [P] markers, file paths. [EXPLICIT]
From qa/acceptance-criteria.md: SC-XXX checkable items (if exists). [EXPLICIT]
From qa/test-coverage.md: FR→TS traceability matrix (if exists). [EXPLICIT]

### 2. Build Semantic Models

- Requirements inventory (functional + non-functional)
- User story/action inventory with acceptance criteria
- Task coverage mapping (task -> requirements/stories)
- Plan coverage mapping (requirement ID → plan.md sections where referenced)
- Constitution rule set

### 3. Detection Passes (limit 50 findings)

**A. Duplication**: near-duplicate requirements -> consolidate
**B. Ambiguity**: vague terms (fast, scalable, secure) without measurable criteria; unresolved placeholders
**C. Underspecification**: requirements missing objects/outcomes; stories without acceptance criteria; tasks referencing undefined components
**D. Constitution Alignment**: conflicts with MUST principles; missing mandated sections. For each principle, report status using these exact values:
- `ALIGNED` — principle satisfied across all artifacts
- `VIOLATION` — principle violated (auto-CRITICAL severity)
**E. Phase Separation Violations**: per `phase-separation-rules.md` — tech in constitution, implementation in spec, governance in plan
**F. Coverage Gaps**: requirements with zero tasks; tasks with no mapped requirement; non-functional requirements not in tasks; requirements not referenced in plan.md

> **Plan coverage detection**: Scan plan.md for each requirement ID (FR-xxx, SC-xxx). A requirement is "covered by plan" if its ID appears anywhere in plan.md. Collect contextual refs (KDD-x, section headers) where found.

> **Trade-off (substring matching)**: "ID appears anywhere" is deliberately cheap and false-positive-prone — `FR-1` matches inside `FR-12`, and an ID cited only in a "not in scope" note still counts as covered. Decision: accept the over-count to stay deterministic and dependency-free; never under-report coverage. Mitigate by matching on word boundaries (`\bFR-1\b`) so `FR-1` does not match `FR-12`. A plan ref that is purely an exclusion note is a known blind spot — out of scope to disambiguate here. [INFERENCIA]

**G. Inconsistency**: terminology drift; entities in plan but not spec; conflicting requirements

**G2. Prose Range Detection**: Scan tasks.md for patterns like "TS-XXX through TS-XXX" or "TS-XXX to TS-XXX". Flag as MEDIUM finding: "Prose range detected — intermediate IDs not traceable. Use explicit comma-separated list."

**H. Feature File Traceability** (when `FEATURE_DIR/tests/features/` exists):
Parse all `.feature` files in `tests/features/` and extract Gherkin tags: [EXPLICIT]
- `@FR-XXX` — functional requirement references
- `@SC-XXX` — success criteria references
- `@US-XXX` — user story references
- `@TS-XXX` — test specification IDs

**H1. Untested requirements**: For each FR-XXX and SC-XXX in spec.md, check if at least one `.feature` file has a corresponding `@FR-XXX` or `@SC-XXX` tag. Flag any FR-XXX or SC-XXX without a matching tag as "untested requirement" (severity: HIGH).

**H2. Orphaned tags**: For each `@FR-XXX` or `@SC-XXX` tag found in `.feature` files, verify the referenced ID exists in spec.md. Flag tags referencing non-existent IDs as "orphaned traceability tag" (severity: MEDIUM).

**H3. Step definition coverage** (optional): If `tests/step_definitions/` exists alongside `tests/features/`, run `verify-steps.sh` to check for undefined steps:
```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/verify-steps.sh --json "FEATURE_DIR/tests/features" "FEATURE_DIR/plan.md"
```
If status is BLOCKED, report undefined steps as findings (severity: HIGH). If DEGRADED, note in report but do not flag as finding. [EXPLICIT]

**Detection-pass failure modes** (degrade gracefully, never abort the run): [INFERENCIA]
- Optional input absent (`qa/acceptance-criteria.md`, `qa/test-coverage.md`, `tests/features/`) → skip its passes (D-coverage, H1–H3) and record "not present" in Metrics; do not emit findings for the missing file itself.
- Malformed or non-canonical IDs (`FR007`, `fr-7`, `FR_7`) → these will not match `\bFR-\d+\b`; flag as an Inconsistency (MEDIUM) "ID format off-convention", not as a coverage gap, to avoid a false zero-coverage CRITICAL.
- Findings exceed 50 → truncate to the 50 highest-severity (CRITICAL→LOW, then first-seen order) and add a final row "N additional findings suppressed (limit 50)". The cap bounds tokens; never silently drop without the count. [EXPLICIT]
- Constitution present but with zero MUST principles → pass D yields all `ALIGNED` by vacuity; note "no normative MUST statements found" so the green result is not mistaken for verified coverage. [SUPUESTO]

### 4. Severity

- **CRITICAL**: constitution MUST violations, phase separation, missing core artifact, zero-coverage blocking requirement
- **HIGH**: duplicates, conflicting requirements, ambiguous security/performance, untestable criteria, untested requirement (H1), BLOCKED step coverage (H3)
- **MEDIUM**: terminology drift, missing non-functional coverage, underspecified edge cases, orphaned traceability tag (H2), prose range (G2)
- **LOW**: style/wording, minor redundancy

**Tie-break rules** (apply in order, deterministic): [INFERENCIA]
1. A constitution `VIOLATION` is always CRITICAL — it cannot be downgraded by context.
2. When a finding fits two bands, assign the **higher** severity (fail-safe), except style/wording which floors at LOW.
3. Severity is per-finding, not per-requirement: one requirement can emit several findings at different bands.
4. Severity drives the health-score weight (step 5b), so mis-banding directly moves the score — prefer the documented band over judgment.

### 5. Analysis Report

Output to console AND write to `FEATURE_DIR/analysis.md`: [EXPLICIT]

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|

**Constitution Alignment**: principle name -> status (ALIGNED | VIOLATION) -> notes
**Coverage Summary**: requirement key -> has task? -> task IDs -> has plan? -> plan refs
**Phase Separation Violations**: artifact, line, violation, severity
**Metrics**: total requirements, total tasks, coverage %, ambiguity count, critical issues

**Health Score**: <score>/100 (<trend>)

## Score History

| Run | Score | Coverage | Critical | High | Medium | Low | Total |
|-----|-------|----------|----------|------|--------|-----|-------|
| <timestamp> | <score> | <coverage>% | <critical> | <high> | <medium> | <low> | <total_findings> |
```

**Worked example** (illustrative, 1 critical + 2 high + 3 medium + 1 low): [EXPLICIT]
```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Constitution | CRITICAL | spec.md §3; constitution P-II | FR-007 stores PII unencrypted, violates P-II "encrypt-at-rest" | Add encryption requirement or remove field |
| A2 | Coverage | HIGH | spec FR-012 | Requirement has zero tasks | Add a task in tasks.md or cut FR-012 |
| A3 | Ambiguity | HIGH | spec §2 | "fast response" — no measurable threshold | Replace with "p95 < 200ms" |
| A4 | Inconsistency | MEDIUM | plan §4 vs spec §1 | Entity "Account" in plan, "User" in spec | Unify terminology |

**Constitution Alignment**: P-I Test-First → ALIGNED; P-II Encrypt-at-rest → VIOLATION (A1)
**Coverage Summary**: FR-012 → no task → — → has plan? yes → §4
**Metrics**: 14 requirements, 22 tasks, coverage 93%, ambiguity 1, critical 1
**Health Score**: 64/100 (↓ declining)
```
Score check: `100 − (1·20 + 2·5 + 3·2 + 1·0.5) = 100 − 36.5 = 63.5 → 64` (round half-up). Always recompute from the finding counts; never copy a prior run's number. [INFERENCIA]

### 5b. Score History

After computing **Metrics** in step 5, persist the health score: [EXPLICIT]

1. **Compute health score**: `score = 100 - (critical*20 + high*5 + medium*2 + low*0.5)`, floored at 0, rounded to nearest integer.
2. **Read** `.specify/score-history.json`. If the file does not exist, initialize with `{}`.
3. **Append** a new entry for the current feature (keyed by feature directory name, e.g. `001-user-auth`):
   ```json
   { "timestamp": "<ISO-8601 UTC>", "score": <n>, "coverage_pct": <n>, "critical": <n>, "high": <n>, "medium": <n>, "low": <n>, "total_findings": <n> }
   ```
4. **Write** the updated object back to `.specify/score-history.json`.
5. **Determine trend** by comparing the new score to the previous entry (if any):
   - Score increased → `↑ improving`
   - Score decreased → `↓ declining`
   - Score unchanged or no previous entry → `→ stable`
6. **Display** in console output: `Health Score: <score>/100 (<trend>)`
7. **Include** the full `score_history` array for the current feature in `analysis.md` under the **Health Score** line and **Score History** table added in step 5.

**Score edge cases & failure modes**: [INFERENCIA]
- Many findings can drive the raw score below 0 → **clamp to 0**; never emit a negative score.
- No prior entry for this feature → trend is `→ stable` (not `↑`); a first run is never "improving".
- Equal scores across runs → `→ stable`, even if the finding mix changed.
- `score-history.json` exists but is malformed/non-JSON → do not crash the run: treat as `{}`, append, and note the reset in the report rather than discarding the analysis. [SUPUESTO]
- Rounding is half-up to the nearest integer (`63.5 → 64`); apply once, after clamping is checked.
- The score is a relative trend signal, not an absolute quality grade — a high score with low coverage still warrants scrutiny. Do not gate solely on the number. [SUPUESTO]

### 6. Next Actions

- CRITICAL issues: recommend resolving before `/iikit-07-implement`
- LOW/MEDIUM only: may proceed with improvement suggestions

### 7. Offer Remediation

Ask: "Suggest concrete remediation edits for the top N issues?" Do NOT apply automatically. [EXPLICIT]

## Operating Principles

- Minimal high-signal tokens, progressive disclosure, limit to 50 findings
- Never modify files, never hallucinate missing sections
- Prioritize constitution violations, use specific examples over exhaustive rules
- Report zero issues gracefully with coverage statistics

## Commit

```bash
git add specs/*/analysis.md .specify/score-history.json
git commit -m "analyze: <feature-short-name> consistency report"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects the analysis results: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```

Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 06 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 06 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. If CRITICAL issues were found: suggest resolving them, then re-run `/iikit-06-analyze`
3. If no CRITICAL: present `next_step` as the primary recommendation
4. If `alt_steps` non-empty: list as alternatives
5. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
6. Append dashboard link

Format:
```
Analysis complete! [EXPLICIT]
[- CRITICAL issues found: resolve, then re-run /iikit-06-analyze]
Next: [/clear → ] <next_step> (model: <tier>) [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-06-analyze" — Run the full iikit 06 analyze workflow
- "iikit 06 analyze on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Acceptance Criteria

This run is **DONE** only when all hold: [INFERENCIA]
- [ ] `analysis.md` written with all four report blocks (table, Constitution Alignment, Coverage Summary, Metrics) and the Health Score line. [EXPLICIT]
- [ ] Health score recomputed from this run's finding counts, clamped ≥ 0, and persisted to `.specify/score-history.json` under the feature key. [EXPLICIT]
- [ ] Every constitution principle reports exactly one status (`ALIGNED` | `VIOLATION`); any `VIOLATION` is rendered CRITICAL.
- [ ] Spec/plan/tasks left byte-for-byte unchanged (READ-ONLY honored).
- [ ] Findings ≤ 50, each carrying severity + location + recommendation; overflow reported as a count.
- [ ] Next Actions reflect whether any CRITICAL exists (block vs. proceed).

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Detection is lexical/structural (ID and term matching), not semantic — it cannot catch a requirement satisfied by differently-worded prose, nor judge whether a task *correctly* implements its requirement. False negatives on intent are expected. [INFERENCIA]
- Single-feature scope: analyzes the active FEATURE_DIR only; cross-feature contradictions are out of scope unless surfaced via the QA Plan. [SUPUESTO]
- Coverage % measures *traceability* (IDs linked), not *correctness* or *completeness* of the linked work. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input ($ARGUMENTS blank) | Proceed with full analysis on existing artifacts; do not block on empty args |
| Missing core artifact (spec/plan/tasks) | ERROR per Prerequisites; emit a CRITICAL "missing core artifact", do not fabricate sections |
| Missing constitution | ERROR (basic-mode load requires it) — stop, do not infer principles |
| Conflicting requirements | Flag as HIGH with both locations; propose resolution, never auto-pick a winner |
| Constitution conflict | Auto-CRITICAL `VIOLATION`; cannot be downgraded by context |
| Multiple features, none active (`needs_selection`) | Present numbered table, set active feature, re-run prerequisites |
| Optional QA/feature files absent | Skip dependent passes, record "not present"; no finding for the absence itself |
| Zero findings | Report gracefully with coverage stats + green-but-verify caveat; still write score history |
| > 50 findings | Truncate to 50 highest-severity; append suppressed-count row |
| Malformed/off-convention IDs | Flag as MEDIUM Inconsistency, not zero-coverage CRITICAL |
| Out-of-scope request | Redirect to appropriate skill (see Anti-scope) or escalate |
