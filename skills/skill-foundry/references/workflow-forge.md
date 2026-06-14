<!-- distilled from alfa skills/workflow-forge -->
<!-- Creates slash-command workflow definitions with phase maps, agent handoffs, verification checkpoints, and deterministic validation. Use when the user asks to create a workflow, forge a slash command, turn a process into phases, define an agent workflow, or prepare a repeatable command flow. -->
# Workflow Forge

Create slash-command workflow definitions that are explicit enough to run,
review, and validate. A workflow is not a loose checklist: it is a phase-based
contract with named agents, inputs, outputs, checkpoints, and a final
verification gate. [DOC]

**Provenance convention.** This file uses the Alfa core tag set
(`references/verification-tags.md`): `[DOC]`, `[CONFIG]`, `[CÓDIGO]`,
`[INFERENCIA]`, `[SUPUESTO]`. Inside generated workflows, catalog references
carry the workflow markers `[EXPLICIT]` / `[INFERRED]` / `[OPEN]` — those are
domain values this skill emits, not provenance tags, and never mix with the
Alfa set in the same role. [DOC]

## Deterministic Workflow Compiler

Use `scripts/compile-workflow-forge.py` when the task needs a reproducible
workflow artifact from structured input. The compiler reads only local JSON
fixtures and local `assets/` policies; it never calls APIs, MCP tools, model
providers, or the network — identical input yields identical output. [CÓDIGO]

```bash
python3 skills/workflow-forge/scripts/compile-workflow-forge.py \
  --input skills/workflow-forge/scripts/fixtures/skill-audit-workflow.json \
  --output /tmp/skill-audit-workflow.md
```

For machine-readable output, add `--format json`. The stable output sections
are `frontmatter`, `phase_map`, `checkpoints`, `quality_gates`,
`example_dialogue`, and `validation`. [CÓDIGO]

Read `assets/workflow-forge-schema.json` for the input contract,
`assets/workflow-policy.json` for phase and checkpoint rules, and
`assets/source-map.md` for local source references. [CÓDIGO]

**Compiler vs. hand-authoring.** Prefer the compiler whenever input is
structured JSON: it enforces the policy and fails closed on schema violations,
so structure is provable rather than asserted. Hand-author only when input is
free-form prose that cannot yet be coerced into the schema; then run the
compiler on the result as a check. [INFERENCIA]

**Exit codes (for scripting):** `0` valid; `2` schema/policy violation (stderr
names the failing field); `3` I/O or missing asset. Treat any non-zero as a
hard block, not a warning. [SUPUESTO] — confirm against
`scripts/compile-workflow-forge.py` if wired into CI.

## When to Activate

Use this skill for workflow definitions, not for generic project plans. [DOC]

| User intent | Activate? | Reason |
|---|---:|---|
| "Create `/jm:triage-ticket` with phases and agents" | Yes | Slash-command workflow contract |
| "Turn this support process into a command flow" | Yes | Repeatable phase-based process |
| "Define agent handoffs and verification gates" | Yes | Workflow governance |
| "Write a one-off task list" | No | Use a plan/checklist skill |
| "Create a spreadsheet template" | No | Use a template/spreadsheet skill |
| "Document an existing manual runbook, no command" | No | Runbook skill; no trigger/handoff contract |
| "Orchestrate a one-time multi-step chat task" | No | Plan skill; not repeatable, no `command` |

**Anti-scope.** Workflow Forge does not execute workflows, schedule them,
register slash commands with the host, or guarantee that named agents/skills
exist at runtime (only that references are marked). It does not author the
agents or skills themselves. [DOC]

## Before Forging

1. Confirm the trigger command and deliverable are explicit. If either is
   missing, ask before writing — do not auto-fill. [DOC]
2. Inspect existing command/workflow files to avoid duplicating a command name.
   A collision is a hard stop, not a rename-on-the-fly. [DOC]
3. Cross-check declared agents and skills against available catalogs when the
   repo provides them. Unknown references must be marked `[OPEN]`. [DOC]
4. Load only the needed local assets: schema, workflow policy, output template,
   and source map. [DOC]

## Workflow Contract

A valid workflow definition must include: [DOC]

| Field | Rule | Failure if violated |
|---|---|---|
| `workflow_id` | Kebab-case, unique inside the workflow namespace | Reject: ambiguous identity |
| `command` | Slash command beginning with `/` | Reject: not invocable |
| `description` | One-line purpose with the expected outcome | Reject: intent unclear |
| `deliverable` | Concrete output produced by the workflow | Reject: no definition of done |
| `skills_involved` | Non-empty list of skill IDs | Reject: unverifiable capability |
| `agents_coordinated` | Non-empty list of agent IDs | Reject: no accountability |
| `phases` | ≥2 phases; first clarification/planning; final verification | Reject: no gate boundary |
| `quality_gates` | Testable criteria that block completion | Reject: cannot fail closed |
| `example_dialogue` | Minimal user/assistant exchange showing activation | Reject: activation unproven |

## Core Process

### Phase 1: Intent Mapping

- Extract `command`, `workflow_id`, deliverable, audience, and boundary of use.
- Identify missing inputs that would make the workflow ambiguous.
- Decide whether the request is a workflow, a runbook, or a one-off plan.

### Phase 2: Catalog Alignment

- List participating skills and agents.
- Mark each reference as `[EXPLICIT]` (found in catalog), `[INFERRED]`
  (plausibly exists, unverified), or `[OPEN]` (unknown/absent).
- Reject anonymous work: every phase must name at least one responsible agent.

### Phase 3: Phase Design

- Build 3-7 phases where possible.
- Phase 1 handles clarification/planning.
- Middle phases execute work with clear inputs and outputs.
- The final phase verifies completion against quality gates.
- Each phase includes a checkpoint that can fail closed before the next phase.

### Phase 4: Assembly

- Write frontmatter with `description`, `command`, `skills_involved`, and
  `agents_coordinated`.
- Render a phase map, handoff table, checkpoints, quality gates, and example
  dialogue.
- Include failure handling for missing inputs, unknown agents, and blocked
  validation.

### Phase 5: Verification

- Validate against `assets/workflow-policy.json`.
- Run the local compiler/check script when structured input is available.
- Confirm the workflow has no prohibited stack references and no missing final
  verification phase.

## Worked Example (minimal valid workflow)

Intent: "Create `/jm:review-skill` that audits a skill before release." [DOC]

```yaml
workflow_id: review-skill
command: /jm:review-skill
description: Audit a skill against DoD and emit a pass/block verdict.
deliverable: review-report.md with verdict + evidence per gate
skills_involved: [skill-foundry]
agents_coordinated: [intake-analyst, quality-guardian]
phases:
  - name: Clarify         # P1 planning
    agent: intake-analyst
    input: skill path
    output: scope + gate list
    checkpoint: target skill path resolved and readable
  - name: Audit           # middle
    agent: quality-guardian
    input: scope + gate list
    output: per-gate findings with evidence tags
    checkpoint: every gate has a pass/fail + evidence
  - name: Verify          # final gate
    agent: quality-guardian
    input: per-gate findings
    output: verdict (pass|block)
    checkpoint: zero open gates OR verdict=block with reasons
quality_gates:
  - Frontmatter complete
  - Every phase agent appears in agents_coordinated
  - Example dialogue present
example_dialogue:
  - user: "/jm:review-skill skills/foo"
  - assistant: "Auditing skills/foo against 3 gates..."
```

Note `quality-guardian` owns two phases — legal (see Edge Cases:
single-agent), but each phase keeps a distinct checkpoint. [INFERENCIA]

## Quality Standards

| Standard | Good | Bad |
|---|---|---|
| Command | `/jm:review-skill` | `review stuff` |
| Phase | "Verify gates: validate DoD, scripts, diff hygiene" | "Check everything" |
| Agent | `quality-guardian` owns final validation | "someone validates" |
| Checkpoint | "All phase outputs have owner, status, and evidence tag" | "Looks good" |
| Failure route | "Stop and ask for command name if missing" | "Continue with assumptions" |

## Validation Gate

- [ ] Frontmatter has `description`, `command`, `skills_involved`, and `agents_coordinated`
- [ ] Workflow has at least 2 phases
- [ ] First phase is clarification or planning
- [ ] Final phase is verification
- [ ] Every phase declares agents, inputs, outputs, and checkpoint criteria
- [ ] Every declared phase agent appears in `agents_coordinated`
- [ ] Every quality gate is observable and testable
- [ ] Example dialogue shows the workflow activation
- [ ] Missing or unknown references are marked `[OPEN]`
- [ ] No prohibited stack references appear unless the user explicitly scopes them
- [ ] `workflow_id` is unique in-namespace (checked against existing command files)

## Antipatterns & Failure Modes

| Antipattern / failure | Why it fails | Fix |
|---|---|---|
| Single-phase workflow | No handoff or verification boundary | Split into clarify, execute, verify |
| Agentless workflow | Accountability disappears | Assign responsible agents per phase |
| Vague checkpoint | Cannot fail closed | Use observable pass/fail criteria |
| Hidden assumptions | Surprises the user during execution | Mark assumptions and ask when blocking |
| Stack leakage | Violates local kit constraints | Reject or flag prohibited stack terms |
| Phase agent absent from `agents_coordinated` | Handoff table desyncs from roster | Reconcile both lists before assembly |
| Final phase is not verification | Workflow can complete unchecked | Force last phase to gate against `quality_gates` |
| Gate phrased as opinion ("looks good") | Not testable; never fails closed | Rewrite as observable predicate |
| Compiler run but exit code ignored | Silent invalid artifact ships | Treat non-zero exit as hard block |

## Edge Cases

- **Single-agent workflow:** Keep the same agent across phases, but still
  separate clarification, execution, and verification.
- **Unknown agent or skill:** Mark `[OPEN]`; do not invent a catalog entry.
- **Conflicting phase order:** Stop and resolve the dependency before writing.
- **Workflow too small:** Suggest a checklist or runbook instead of a command.
- **Workflow too large:** Split into parent workflow plus sub-workflows.
- **External stack requested:** Include only if user explicitly scopes it and the
  repo policy allows it.
- **Catalog files absent from repo:** Catalog check cannot run; mark all
  references `[INFERRED]` and state that verification is deferred. [INFERENCIA]
- **Command name collides:** Hard stop; ask the user to rename or confirm
  intentional overwrite — never silently shadow an existing command. [DOC]

## Reference Files

| Path | Use |
|---|---|
| `assets/workflow-forge-schema.json` | Input/output contract for deterministic compilation |
| `assets/workflow-policy.json` | Phase, checkpoint, stack, and quality gate rules |
| `assets/workflow-output-template.md` | Stable Markdown section order |
| `assets/source-map.md` | Local reference map for the skill |
| `scripts/compile-workflow-forge.py` | Offline compiler and validator |
| `scripts/check.sh` | Deterministic runtime check for positive and negative fixtures |

## Assumptions & Limits

- This skill creates workflow definitions; it does not execute, schedule, or
  register them with the host. [DOC]
- Catalog checks are only as complete as the files available in the current
  repo; absence yields `[INFERRED]`/`[OPEN]`, never silent `[EXPLICIT]`. [DOC]
- Deterministic validation proves structure, not business correctness — a
  schema-valid workflow can still encode the wrong process. [INFERENCIA]
- Free-form user requests may still require clarification before compilation. [DOC]
- Exit-code semantics above are [SUPUESTO] until confirmed against the compiler
  source; verify before depending on them in automation.

---
**Author:** Javier Montaño | **Last updated:** 2026-06-11
