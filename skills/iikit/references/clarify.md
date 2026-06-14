<!-- distilled from alfa skills/iikit-clarify -->
<!-- >- -->
# Intent Integrity Kit Clarify (Generic Utility)

Ask targeted clarification questions to reduce ambiguity in the detected (or user-specified) artifact, then encode answers back into it. [EXPLICIT]

**Contract**: read-only scan → sequential Q&A → write each answer back immediately → validate → commit. The artifact is the source of truth; this skill never invents requirements, only surfaces and records human decisions. [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

If the user provides a target argument (e.g., `plan`, `spec`, `checklist`, `testify`, `tasks`, `constitution`), use that artifact instead of auto-detection. [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (soft mode — parse if exists, continue if not). [EXPLICIT] Constitution principles bound the *option space* of questions: never offer an option that violates a stated principle, and prefer questions whose answers enforce a principle currently under-specified in the artifact. [INFERENCIA]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase clarify --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase clarify -Json`
2. Parse JSON. If `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.
3. Determine the target artifact (see "Target Detection" below).

**Failure modes** [INFERENCIA]
- Script exits non-zero or emits non-JSON → surface stderr verbatim; do NOT proceed with a guessed feature dir. [SUPUESTO]
- `needs_selection: true` but `features` empty → no feature exists; route to `/iikit-01-specify`, do not clarify the constitution silently. [INFERENCIA]
- User picks an out-of-range index → re-prompt with the same table, do not default to feature 1. [EXPLICIT]

## Target Detection

If the user provided a target argument, map it: [EXPLICIT]

| Argument | Artifact file |
|----------|--------------|
| `spec` | `{FEATURE_DIR}/spec.md` |
| `plan` | `{FEATURE_DIR}/plan.md` |
| `checklist` | `{FEATURE_DIR}/checklists/*.md` (all files) |
| `testify` | `{FEATURE_DIR}/tests/features/*.feature` (read for scanning), `{FEATURE_DIR}/tests/clarifications.md` (write Q&A) |
| `tasks` | `{FEATURE_DIR}/tasks.md` |
| `constitution` | `{REPO_ROOT}/CONSTITUTION.md` |

If no argument, auto-detect by checking artifacts in reverse phase order. Pick the first that exists: [EXPLICIT]

1. `{FEATURE_DIR}/tasks.md`
2. `{FEATURE_DIR}/tests/features/*.feature`
3. `{FEATURE_DIR}/checklists/*.md`
4. `{FEATURE_DIR}/plan.md`
5. `{FEATURE_DIR}/spec.md`
6. `{REPO_ROOT}/CONSTITUTION.md`

**Why reverse phase order**: the latest-phase artifact is the one about to be consumed downstream, so resolving its ambiguity prevents the most rework. Auto-detect targets a single artifact; to clarify an earlier one, pass it explicitly. [INFERENCIA]

If no clarifiable artifact exists: ERROR with `No artifacts to clarify. Run /iikit-01-specify first or /iikit-00-constitution.` [EXPLICIT]

**Edge — explicit argument points at a missing file**: report `Target <arg> not found at <path>` and offer auto-detect; do not silently fall through. [INFERENCIA] **Edge — glob matches zero files** (`checklist`, `testify`): treat as missing, same handling. [INFERENCIA]

## Execution Steps

### 1. Scan for Ambiguities

Load the target artifact and perform a structured scan using the taxonomy for that artifact type from `ambiguity-taxonomies.md`. Mark each area: Clear / Partial / Missing. [EXPLICIT]

- **Clear** = unambiguous and testable as written.
- **Partial** = present but admits >1 reasonable interpretation, or lacks a measurable bound.
- **Missing** = the taxonomy expects it and the artifact is silent. [INFERENCIA]

Only `Partial` and `Missing` areas generate questions; `Clear` areas are skipped. Read the artifact's existing `## Clarifications` section first — already-answered items stay `Clear`, never re-asked. [EXPLICIT]

### 2. Generate Question Queue

**Constraints**:
- Each answerable with multiple-choice (2-5 options) OR short phrase (<=5 words)
- Identify related artifact items for each question:
  - Spec: FR-xxx, US-x, SC-xxx
  - Plan: section headers or decision IDs
  - Checklist: check item IDs
  - Testify: scenario names
  - Tasks: task IDs (T-xxx)
  - Constitution: principle names or section headers
- Only include questions that materially impact downstream phases
- Balance category coverage, exclude already-answered, favor downstream rework reduction

**Prioritization** (when more candidates than a reasonable session holds): rank by blast radius — a question touching multiple `FR`/`SC` or a constitution principle outranks a local one; a `Missing` outranks a `Partial` at equal blast radius. Cap a session at a manageable batch; surface the rest as "deferred" in the report rather than forcing the user through all of them. [INFERENCIA]

**Anti-scope** — do NOT queue: speculative tech-stack choices that don't block functional clarity; cosmetic wording; anything answerable from the artifact itself; questions whose every option leaves the same downstream behavior (no decision value). [EXPLICIT]

### 3. Sequential Questioning

Present ONE question at a time. [EXPLICIT]

**For multiple-choice**: follow the options presentation pattern in `conversation-guide.md`. Analyze options, state recommendation with reasoning, render options table. User can reply with letter, "yes"/"recommended", or custom text.

**After answer**: validate against constraints, record, move to next.

**Stop when**: all critical ambiguities resolved or user signals done.

**Answer-handling edges** [INFERENCIA]
- Custom free-text answer that violates a constraint (e.g., >5 words, or conflicts with a constitution principle) → echo the issue, re-ask once; if the user insists, record verbatim and tag the resulting artifact edit `[SUPUESTO]`. [SUPUESTO]
- Answer contradicts a *prior* answer this session → flag both, ask which wins, then reconcile both artifact edits.
- User answers a different question than asked → confirm intent before recording; never silently remap.

### 4. Integration After Each Answer

1. Ensure `## Clarifications` section exists in the target artifact with `### Session YYYY-MM-DD` subheading
2. Append: `- Q: <question> -> A: <answer> [<refs>]`
   - References MUST list every affected item in the artifact
   - If cross-cutting, reference all materially affected items
3. Apply clarification to the appropriate section of the artifact
4. **Save artifact after each integration** to minimize context loss

**Why save per-answer, not batched**: a crash or context overflow mid-session loses at most one answer, and the artifact is always in a committable state. The cost is extra writes — acceptable for the durability gain. [INFERENCIA]

**Testify exception**: `.feature` files are Gherkin syntax — do NOT add markdown sections to them. Instead:
- **Scan** `.feature` files for ambiguities (step 1)
- **Write** Q&A to `{FEATURE_DIR}/tests/clarifications.md` (create if missing)
- **Apply** changes to the `.feature` files themselves (update scenarios, add/remove steps)

See `clarification-format.md` for format details. [EXPLICIT]

### 5. Validation

After each write and final pass: [EXPLICIT]
- One bullet per accepted answer, each ending with `[refs]`
- All referenced IDs exist in the artifact
- No vague placeholders or contradictions remain

If a referenced ID does not exist (typo, or the item was renamed mid-session), halt the write and correct the reference before committing — a dangling ref silently breaks downstream traceability. [INFERENCIA]

### 6. Report

Output: questions asked/answered, target artifact and path, sections touched, traceability summary table (clarification -> referenced items), coverage summary (category -> status), deferred-questions count, suggested next command. [EXPLICIT]

**Next command logic**: run `check-prerequisites.sh --json status` and use its `next_step` field. This returns the actual next phase based on feature state (which artifacts exist), not what was just clarified. Clarify can run at any point — the next step depends on where the feature is, not where clarify was invoked. [EXPLICIT]

## Worked Example (spec target)

```
Scan: FR-003 marked Partial (no rate limit bound), SC-002 Missing (no latency target).
Q1 (FR-003): "Max requests per user per minute?"
  Recommended: B (100/min) — matches existing tier in plan.md §Quotas. [INFERENCIA]
  A) 60  B) 100  C) 1000  D) custom
User: B
  → spec.md ## Clarifications / ### Session 2026-06-11:
     - Q: Max requests/user/min? -> A: 100 [FR-003]
  → FR-003 body updated: "...limited to 100 req/user/min."
  → saved.
Q2 (SC-002): "P95 latency target?"  A: "under 200ms"
  → recorded [SC-002], SC-002 made measurable, saved.
Report: 2 asked / 2 answered, 0 deferred; coverage Performance=Clear, Security=Clear.
Next: /clear → /iikit-02-plan
```
This shows the invariant: every answer produces exactly one Clarifications bullet *and* one in-place edit, both carrying the same ref. [INFERENCIA]

## Behavior Rules

- No meaningful ambiguities found: "No critical ambiguities detected." and suggest proceeding [EXPLICIT]
- Continue until all critical ambiguities are resolved [EXPLICIT]
- Avoid speculative tech stack questions unless absence blocks functional clarity [EXPLICIT]
- Respect early termination signals ("stop", "done", "proceed") — on early stop, the partial session is still valid: everything answered is already written. Report what remains unaddressed. [EXPLICIT]
- For non-spec artifacts, adapt reference format to the artifact's native ID scheme [EXPLICIT]
- Never auto-answer to "finish faster"; an unasked ambiguity surfaces later as rework, the exact cost this skill exists to avoid. [INFERENCIA]

## Commit

Commit the modified artifact(s): [EXPLICIT]

```bash
git add -u
git commit -m "clarify: <target-artifact> Q&A"
```

`git add -u` stages only tracked files; a newly created `tests/clarifications.md` (testify path) is untracked — `git add` it explicitly before committing, or its Q&A is lost. [INFERENCIA] If zero answers were recorded, skip the commit (nothing changed). [INFERENCIA]

## Dashboard Refresh

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT] The `-safe` variant must not abort the workflow on dashboard error; a failed refresh is non-blocking — log and continue. [SUPUESTO]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase clarify --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase clarify -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding (always true for clarify — Q&A sessions consume significant context)
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Clarification complete! [EXPLICIT]
Next: /clear → <next_step> [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-clarify" — Run the full iikit clarify workflow
- "iikit clarify on this project" — Apply to current context
- "/iikit-clarify plan" — Force the target artifact, skipping auto-detect [INFERENCIA]

## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]
- [ ] Every Clarifications bullet has a matching in-place edit with the same ref [INFERENCIA]
- [ ] No dangling references; no contradictions between answers [INFERENCIA]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Assumes prerequisite scripts are present and executable at the `.tessl/...` paths; a relocated kit breaks every script call. [SUPUESTO]
- Resolves ambiguity already *implied* by the artifact and taxonomy; cannot surface requirements the author never hinted at. [INFERENCIA]
- Anti-scope: does not author new requirements, run tests, or modify code outside the target artifact (testify edits the `.feature` it scans — that is the one exception). [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| Explicit target missing / glob empty | Report path, offer auto-detect; never fall through silently [INFERENCIA] |
| Artifact has no taxonomy-relevant content | "No critical ambiguities detected."; skip commit [INFERENCIA] |
| User stops mid-session | Answered items already saved; report unaddressed remainder [INFERENCIA] |
| Two answers conflict in one session | Flag both, ask which wins, reconcile both edits [INFERENCIA] |
| Referenced ID absent from artifact | Halt write, fix reference before commit [INFERENCIA] |
| New `clarifications.md` (testify) | `git add` explicitly; `git add -u` won't stage it [INFERENCIA] |
