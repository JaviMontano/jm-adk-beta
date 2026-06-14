<!-- distilled from alfa skills/iikit-03-checklist -->
<!-- >- -->
# Intent Integrity Kit Checklist

Generate "Unit Tests for English" — checklists that validate REQUIREMENTS quality, not implementation. [EXPLICIT]

**Scope (what this skill does):** review and extend a requirements checklist, resolve gaps by editing `spec.md`, drive items to 100%, record phase completion, refresh the dashboard. [EXPLICIT]

**Anti-scope (what it MUST NOT do):** write/run code or tests; assert that an implementation behaves correctly; create a checklist from scratch when one exists (extend instead); modify `plan.md`/`tasks.md` (read-only here); fabricate spec references to hit the 80% traceability bar. [INFERENCIA]

## Core Principle

Every checklist item evaluates the **requirements themselves** for completeness, clarity, consistency, measurability, and coverage. Items MUST NOT test implementation behavior. [EXPLICIT]

**Litmus test** — if an item can only be answered by executing the system, it tests implementation and belongs in a test suite, not here. If it can be answered by reading the spec alone, it is a valid requirements check. [INFERENCIA]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (basic mode). [EXPLICIT]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 03 --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 03 -Json`
2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.
   - If the script exits non-zero or emits non-JSON (e.g. not in an iikit repo, missing `.specify/`), STOP and report the raw error — do not guess `FEATURE_DIR`. [INFERENCIA]
   - If `AVAILABLE_DOCS` lacks `spec.md`, STOP: step 2 of Execution requires it. [INFERENCIA]
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.

## Execution Steps

### 1. Clarify Intent

Derive up to THREE contextual questions (skip if unambiguous from `$ARGUMENTS`): [EXPLICIT]
- Scope: include integration touchpoints?
- Risk: which areas need mandatory gating?
- Depth: lightweight sanity list or formal release gate?
- Audience: author-only or peer PR review?

### 2. Load Feature Context

Read from FEATURE_DIR: `spec.md` (required), `plan.md` (optional), `tasks.md` (optional). [EXPLICIT]

### 3. Generate Checklist

**Starting point**: `FEATURE_DIR/checklists/requirements.md` already exists (created by `/iikit-01-specify`). Review it, extend it with additional items, and resolve gaps. Do NOT create a duplicate — work with the existing file.

**Additional domain checklists** (optional): if the spec has distinct domains that warrant separate review (e.g., security, performance, accessibility), create additional files as `FEATURE_DIR/checklists/[domain].md`. These supplement `requirements.md`, not replace it.

**Item structure**: question format about requirement quality, with quality dimension tag and spec reference.

Correct: "Are visual hierarchy requirements defined with measurable criteria?" [Clarity, Spec SFR-1]
Wrong: "Verify the button clicks correctly" (this tests implementation) [EXPLICIT]

**Categories**: Requirement Completeness, Clarity, Consistency, Acceptance Criteria Quality, Scenario Coverage, SC-XXX Test Coverage, Edge Case Coverage, Non-Functional Requirements, Dependencies & Assumptions.

**Traceability**: >=80% of items must reference spec sections or use markers: `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`. Markers count toward the 80% — an item flagging a missing requirement is itself traceable to the gap it names. [INFERENCIA]

**Worked example — one item per category** (question form, dimension tag, spec ref): [INFERENCIA]
- Completeness: "Is every user-facing error state given a defined requirement?" `[Gap]`
- Clarity: "Is 'fast load' quantified (e.g. p95 < 2s)?" `[Ambiguity, Spec NFR-2]`
- Consistency: "Do SFR-3 and SFR-7 agree on the session-timeout value?" `[Conflict]`
- Acceptance Criteria: "Does SC-4 state a measurable pass/fail threshold?" `[Acceptance, Spec SC-4]`
- Edge Case: "Is empty-input behavior specified?" `[Gap]`

**Marker semantics** (one per finding type): `[Gap]` = a required statement is absent; `[Ambiguity]` = present but under-specified/unmeasurable; `[Conflict]` = two requirements contradict; `[Assumption]` = relied-upon condition not stated in spec. [INFERENCIA]

See `checklist-examples.md` for correct/wrong examples and required patterns. [EXPLICIT]

Use `checklist-template.md` for format structure. [EXPLICIT]

### 4. Gap Resolution (Interactive)

For each `[Gap]` item: follow the gap resolution pattern in `conversation-guide.md`. Present missing requirement, explain risk, offer options. On resolution: update spec.md and check item off. Skip if `--no-interactive` or no gaps. [EXPLICIT]

### 5. Remaining Item Validation

After gap resolution, validate ALL unchecked `[ ]` items against spec/plan/constitution: [EXPLICIT]
- If covered: check off with justification
- If genuine gap: convert to `[Gap]` and resolve or defer

Continue until all items are `[x]` or explicitly deferred. [EXPLICIT]

**Done criteria** (all must hold before Report): every item is `[x]` or carries an explicit `[Deferred: reason]`; no bare `[ ]` remains; traceability >=80%; no `TBD`/`TODO` text in the file; `spec.md` edits from gap resolution are saved. [INFERENCIA]

**Decision — defer vs resolve**: resolve when the answer is knowable from spec/plan/constitution or a quick user confirmation; defer only when resolution needs work owned by a downstream phase. Trade-off: deferring keeps this phase moving but every deferral is surfaced as a warning downstream, so default to resolve. [INFERENCIA]

**IMPORTANT**: Checklists are optional — not creating one is fine. But once created, they MUST reach 100% before the skill reports success.

### 6. Report

Output: checklist path, item counts (total/checked/deferred), gap resolution summary, completion percentage. [EXPLICIT]

## Commit

```bash
git add specs/*/checklists/ .specify/context.json
git commit -m "checklist: <feature-short-name> requirements review"
```

## Record Phase Completion

Write a timestamp to `.specify/context.json` so the dashboard knows the checklist phase was run (not just that requirements.md exists from specify): [EXPLICIT]

```bash
CONTEXT_FILE=".specify/context.json"
[[ -f "$CONTEXT_FILE" ]] || echo '{}' > "$CONTEXT_FILE"
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.checklist_reviewed_at = $ts' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
```

The write-to-tmp-then-`mv` pattern is deliberate: it prevents a corrupt/truncated `context.json` if `jq` fails mid-write. If `jq` exits non-zero the `&&` stops the `mv`, leaving the original intact — report the failure rather than proceeding. If `jq` is unavailable, STOP and surface it; do not hand-edit JSON. [INFERENCIA]

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects checklist completion: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```

Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 03 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 03 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

If deferred items remain, warn that downstream skills will flag incomplete checklists. [EXPLICIT]

Format:
```
Checklist complete!
Next: [/clear → ] <next_step> (model: <tier>)
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-03-checklist" — Run the full iikit 03 checklist workflow
- "iikit 03 checklist on this project" — Apply to current context


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
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| `requirements.md` missing (skipped specify) | Create it from `checklist-template.md`; do not silently no-op [INFERENCIA] |
| `spec.md` absent or empty | STOP at Load Feature Context — cannot evaluate requirements quality without a spec [INFERENCIA] |
| `--no-interactive` with open `[Gap]` items | Skip resolution, leave gaps marked, surface count in Report; never auto-invent requirements [INFERENCIA] |
| Item phrased as implementation test | Reword to a requirements question or drop it (see Litmus test) [INFERENCIA] |
| Traceability below 80% | Add spec refs/markers before Report; do not fabricate section IDs [INFERENCIA] |
| `set-active-feature` selection out of range | Re-present the numbered table; do not assume index 1 [INFERENCIA] |
| Dashboard script fails | Report the error; phase completion (context.json) already persisted, so do not re-run the whole skill [INFERENCIA] |
