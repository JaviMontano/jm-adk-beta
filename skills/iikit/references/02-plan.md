<!-- distilled from alfa skills/iikit-02-plan -->
<!-- >- -->
# Intent Integrity Kit Plan

Generate design artifacts from the feature specification using the plan template. [EXPLICIT]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per `constitution-loading.md` (enforcement mode — extract rules, declare hard gate, halt on violations). [EXPLICIT]

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 02 --json
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 02 -Json`

2. Parse JSON for `FEATURE_SPEC`, `IMPL_PLAN`, `FEATURE_DIR`, `BRANCH`. If missing spec.md: ERROR (halt — planning has no source of truth without a spec). [EXPLICIT]
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in `conversation-guide.md`. After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.

## Spec Quality Gate

Before planning, validate spec.md: [EXPLICIT]

1. **Requirements**: count FR-XXX patterns (ERROR if 0, WARNING if <3)
2. **Measurable criteria**: scan for numeric values, percentages, time measurements (WARNING if none)
3. **Unresolved clarifications**: search for `[NEEDS CLARIFICATION]` — ask whether to proceed with assumptions
4. **User story coverage**: verify each story has acceptance scenarios
5. **Cross-references**: check for orphan requirements not linked to stories

Report quality score per `formatting-guide.md` (Spec Quality section). If score < 6: recommend `/iikit-clarify` first. [EXPLICIT]

**Gate semantics** (so downstream callers can rely on a deterministic contract): [EXPLICIT]
- ERROR halts the workflow; WARNING surfaces but allows continuation after explicit user acknowledgement. [EXPLICIT]
- A `< 6` score is a *recommendation*, not a halt — the user MAY override and proceed. Record the override as an assumption in research.md so it is traceable. [EXPLICIT]
- Trade-off: stricter auto-halts reduce bad plans but block legitimate spikes/PoCs. iikit chooses recommend-not-block at this gate because the spec, not the plan, is the right place to enforce requirement completeness. [EXPLICIT]
- Anti-scope: this gate validates spec *quality signals*, not domain correctness. It cannot detect a requirement that is well-formed but wrong; that remains human judgment. [EXPLICIT]

## Execution Flow

### 1. Fill Technical Context

Using the plan template, define: Language/Version, Primary Dependencies, Storage, Testing, Target Platform, Project Type, Performance Goals, Constraints, Scale/Scope. Mark unknowns as "NEEDS CLARIFICATION". [EXPLICIT]

When Tessl eval results are available for candidate technologies, include eval scores in the decision rationale in research.md. Higher eval scores indicate better-validated tiles and should factor into technology selection when choosing between alternatives. [EXPLICIT]

### 2. Tessl Tile Discovery

If Tessl is installed, discover and install tiles for all technologies. See `tessl-tile-discovery.md` for the full procedure. [EXPLICIT]

### 3. Research & Resolve Unknowns

For each NEEDS CLARIFICATION item and dependency: research, document findings in `research.md` with decision, rationale, and alternatives considered. Include Tessl Tiles section if applicable. [EXPLICIT]

### 4. Design & Contracts

**Prerequisites**: research.md complete

1. Extract entities from spec -> `data-model.md` (fields, relationships, validation, state transitions)
2. Generate API contracts from functional requirements -> `contracts/`
3. Create `quickstart.md` with test scenarios
4. Update agent context:

**Acceptance criteria** for this step (all must hold before advancing to step 5): every spec entity appears in data-model.md; every FR with an external interface maps to at least one contract; quickstart.md exercises at least one happy path plus one failure path; the agent-context script exits 0. [EXPLICIT]

**Failure modes**: if no entities are extractable, the spec is likely behavioural-only — emit a WARNING and produce contracts directly from FRs rather than fabricating a data model. If `update-agent-context.sh` fails (missing agent file), continue but flag in the Report; the plan artifacts are still valid. [EXPLICIT]
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/update-agent-context.sh claude
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/update-agent-context.ps1 -AgentType claude`

### 5. Pre-compute Dashboard Data

After the plan is complete, write pre-computed data to `.specify/context.json` for static dashboard generation. Use `jq` to merge into the existing file (create if missing). [EXPLICIT]

#### 5a. Architecture Node Classifications

If plan.md contains an architecture diagram (ASCII box-drawing), classify each named component as one of: `client`, `server`, `storage`, `external`. [EXPLICIT]

Write to `.specify/context.json` under `planview.nodeClassifications`: [EXPLICIT]

```bash
# Read existing or start fresh
CONTEXT_FILE=".specify/context.json" [EXPLICIT]
[[ -f "$CONTEXT_FILE" ]] || echo '{}' > "$CONTEXT_FILE"

# Merge node classifications (replace example with actual nodes from the plan diagram)
jq --argjson nodes '{
  "Browser SPA": "client",
  "API Gateway": "server",
  "PostgreSQL": "storage",
  "Stripe API": "external"
}' '.planview.nodeClassifications = $nodes' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
```

Classification rules: [EXPLICIT]
- **client**: browsers, CLIs, mobile apps, desktop apps — anything that initiates requests
- **server**: APIs, gateways, workers, middleware, backend services — anything that processes requests
- **storage**: databases, caches, queues, file stores, object storage — anything that persists data
- **external**: third-party APIs, SaaS services, payment providers — anything outside the project boundary

Tie-breakers for ambiguous nodes: a component that both serves and persists (e.g. an embedded KV store inside a service) is classified by its *dominant role in the diagram edge it terminates* — if other nodes read/write it, it is `storage`; if it only processes inbound requests, it is `server`. A managed cloud DB you operate is `storage`; a DB-as-a-service you cannot configure is `external`. [EXPLICIT]

If no architecture diagram exists in the plan, skip this step. [EXPLICIT]

#### 5b. Tessl Eval Scores

If Tessl tiles were installed in step 2, collect eval scores from the `fetch-tile-evals.sh` outputs and write a summary to `context.json`: [EXPLICIT]

```bash
# Merge eval scores (replace example with actual tile names and scores from step 2)
jq --argjson evals '{
  "workspace/tile-name": {"score": 85, "pct": 85, "scenarios": 3, "scored_at": "2026-01-15T10:00:00Z"}
}' '.planview.evalScores = $evals' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
```

Use the JSON output from each `fetch-tile-evals.sh --json` call (already run in step 2 via tessl-tile-discovery.md). Extract `score`, `pct`, `scenarios`, and `scored_at` fields for each tile. [EXPLICIT]

If no Tessl tiles were installed, skip this step. [EXPLICIT]

### 6. Constitution Check (Post-Design)

Re-validate all technical decisions against constitutional principles. On violation: STOP, state violation, suggest compliant alternative. [EXPLICIT]

### 7. Phase Separation Validation

Scan plan for governance content per `phase-separation-rules.md` (Plan section). Auto-fix by replacing with constitution references, re-validate. [EXPLICIT]

## Output Validation

Before writing any artifact: review against each constitutional principle. On violation: STOP with explanation and alternative. [EXPLICIT]

## Report

Output: branch name, plan path, generated artifacts (research.md, data-model.md, contracts/*, quickstart.md), agent file update status, Tessl integration status (tiles installed, skills available, technologies without tiles, eval results saved), dashboard pre-computed data status (node classifications written, eval scores written). [EXPLICIT]

## Semantic Diff on Re-run

If plan.md exists: compare tech stack, architecture, dependencies. Show diff per `formatting-guide.md` (Semantic Diff section) with downstream impact. Flag breaking changes. [EXPLICIT]

## Commit

```bash
git add specs/*/plan.md specs/*/research.md specs/*/data-model.md specs/*/quickstart.md specs/*/contracts/ .specify/context.json
git commit -m "plan: <feature-short-name> technical design"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects the new plan: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 02 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 02 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in `model-recommendations.md` for agent-specific switch commands.
5. Append dashboard link

Format:
```
Plan complete! [EXPLICIT]
Next: [/clear → ] <next_step> (model: <tier>) [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-02-plan" — Run the full iikit 02 plan workflow
- "iikit 02 plan on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes the prerequisites script and `jq` are available on PATH; without `jq`, step 5 (dashboard pre-compute) degrades to skipped, not failed. [EXPLICIT]
- Assumes a valid, present constitution; if absent, the enforcement hard gate cannot be declared and planning must halt per constitution-loading.md. [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- **Anti-scope**: this phase produces *design intent* (plan + research + data model + contracts), not implementation or task breakdown — those belong to later phases (05-tasks, 07-implement). It does not run tests or write production code. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| spec.md missing | ERROR and halt (step 2 of Prerequisites) — no spec, no plan [EXPLICIT] |
| `needs_selection: true` | Present features table, run set-active-feature, re-run prerequisites [EXPLICIT] |
| Unresolved `[NEEDS CLARIFICATION]` in spec | Ask whether to proceed with assumptions; record each assumption in research.md [EXPLICIT] |
| Tessl not installed | Skip tile discovery and eval-score pre-compute; note "no tiles" in Report [EXPLICIT] |
| No architecture diagram in plan.md | Skip node classification (step 5a) [EXPLICIT] |
| plan.md already exists | Run Semantic Diff; flag breaking tech-stack/architecture changes before overwrite [EXPLICIT] |
| Constitution violation at post-design check | STOP, state violation, propose compliant alternative — do not write artifacts [EXPLICIT] |
