<!-- distilled from alfa skills/workflow-creator -->
<!-- Generates deterministic 17-field workflow definitions with step contracts, DoD, RACI, KPIs, validation rules, and failure handling for agentic ecosystems. Use when the user asks to create a workflow, define workflow steps, build workflow YAML, generate a workflow spec, design a RACI-backed procedure, or convert an agentic process into a repeatable workflow. -->
# Workflow Creator

Create complete workflow definitions that can be reviewed, executed, and
validated. A valid workflow is a 17-field contract with 3-7 ordered steps,
each step carrying 12 traceability fields, plus DoD, QA, RACI, KPIs, fallback,
and escalation routes. [EXPLICIT]

**Scope:** authoring of one workflow definition per request. **Anti-scope:**
executing workflows, orchestrating multi-workflow programs, editing the owning
skill, or asserting strategic correctness — those belong to runtime,
`workflow-forge`, and human review respectively. [EXPLICIT]

## Deterministic Assets

Load only the local assets needed for the request. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/workflow-definition-contract.json` | Required fields, field types, and deterministic validation rules |
| `assets/activation-policy.json` | Activate/decline rules, clarification triggers, and network policy |
| `assets/quality-gates.json` | Blocking quality gates for workflow definitions |
| `assets/workflow-output-template.md` | Stable Markdown/YAML section order |
| `scripts/validate_workflow_spec.py` | Offline validator for JSON workflow specs |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads local JSON only. It does not call APIs, MCP tools, model
providers, the network, system time, random sources, or repo-global state beyond
the provided files. This keeps a given spec+contract pair reproducible across
machines and runs; identical inputs yield an identical exit code. [EXPLICIT]
If an asset is absent, state which gate is unverifiable rather than skipping it
silently. [EXPLICIT]

## When To Activate

Use this skill for workflow definitions, not for generic plans or one-off task
lists. [EXPLICIT]

| User intent | Activate? | Reason |
|---|---:|---|
| "Create a workflow for agent handoff review" | Yes | Needs ordered steps, roles, QA, and failure routes |
| "Build workflow YAML with RACI and KPIs" | Yes | Requests the 17-field workflow contract |
| "Define the steps, DoD, and escalation route" | Yes | Workflow governance is explicit |
| "Give me a quick checklist" | No | Checklist does not require full workflow contract |
| "Write a project plan" | No | Use planning/project-management skills unless workflow fields are requested |
| "What is a workflow?" | No | Answer directly without loading assets |
| "Run / trigger this workflow now" | No | Authoring skill; route to runtime/executor |

If the user provides a workflow ID but no owning skill, ask for the owning skill
or state that the workflow is standalone before producing the final spec.
[EXPLICIT]

## Inputs

Minimum input required before final output: [EXPLICIT]

| Input | Rule |
|---|---|
| `workflow_id` | Kebab-case identifier, unique in the target context |
| `owning_skill_id` | Existing or explicitly proposed owner; unknown values stay `[OPEN]` |
| `objective` | Measurable outcome that names the deliverable |
| `trigger` | Concrete event, command, condition, or request |
| `actors` | Agents or human roles used in RACI/escalation |
| `inputs` | Named data required to start the workflow |
| `success_evidence` | Observable completion signals |
| `failure_modes` | At least one recoverable and one unrecoverable failure route |

Ask for missing blocking inputs. If the user asks to proceed with gaps, mark
each gap `[OPEN]` and lower confidence instead of inventing facts. Never
fabricate agent IDs, KPI targets, or owning skills to satisfy a gate — a
fabricated value passes structural validation but fails closed in execution.
[EXPLICIT]

## Output Contract

Produce a Markdown response with an embedded `workflow.yaml` block. The YAML
must contain these 17 top-level fields in this order: [EXPLICIT]

```yaml
- id: "{kebab-case-id}"
  title: "{Human-readable title}"
  objective: "{Measurable outcome that produces a named deliverable}"
  trigger: "{Specific event, command, or condition}"
  preconditions:
    - "{Checkable condition before starting}"
  inputs:
    - name: "{name}"
      type: "{string|object|array|boolean|number|file|url}"
      required: true
      description: "{what it provides and why it matters}"
  steps:
    - stepNumber: 1
      title: "{2-5 words}"
      desc: "{1-2 sentences}"
      whyThisMatters: "{Failure consequence, not a restatement}"
      inputNeeded: "{Specific data with types}"
      actionInstruction: "{Concrete operation or prompt construction rule}"
      promptToUse: "{Full prompt text, or null (mechanical step)}"
      expectedOutput: "{Success output format and content}"
      validationRule: "{Observable pass/fail condition}"
      failureSignal: "{Observable failure condition}"
      recoveryAction: "{Concrete recovery action}"
      handoffIfNeeded: "{agent-id, human role, or null}"
  mainOutput: "{Primary deliverable with format}"
  secondaryOutputs:
    - "{logs, metrics, notifications, state changes}"
  DoD:
    - "{Verifiable assertion that blocks completion}"
  qaChecklist:
    - "{Specific quality check}"
  raci:
    responsible: "{agent or role}"
    accountable: "{agent or role}"
    consulted: "{agent, role, or none}"
    informed: "{agent, role, or none}"
  kpis:
    - metric: "{metric name}"
      target: "{numeric or bounded value}"
      unit: "{seconds|minutes|percentage|count|ratio|boolean}"
      measurement: "{how to measure}"
  cadence: "{on-demand|hourly|daily|weekly|per-event|per-request}"
  errorHandling: "{Unrecoverable error strategy}"
  fallbackRoute: "{workflow-id, direct-response, or stop-and-ask}"
  escalationRoute: "{agent-id or human role}"
```

Field semantics worth fixing to avoid common errors: [EXPLICIT]
- `accountable` is exactly one owner — never a list, never `none`. [EXPLICIT]
- `validationRule` describes success; `failureSignal` is its observable
  negation, not a paraphrase of the same condition. [EXPLICIT]
- `promptToUse` is `null` for mechanical steps (scripts, file ops); a non-null
  prompt implies a model call and must be self-contained. [EXPLICIT]
- `fallbackRoute` is what runs when the workflow cannot complete;
  `recoveryAction` is per-step and runs first. [INFERRED]

When a deterministic check is required, mirror the YAML as JSON and run:

```bash
python3 skills/workflow-creator/scripts/validate_workflow_spec.py \
  --contract skills/workflow-creator/assets/workflow-definition-contract.json \
  --spec path/to/workflow.json
```

## Creation Process

1. Confirm activation using `assets/activation-policy.json`. [EXPLICIT]
2. Read the owning skill or local catalog only when available in the workspace.
   Unknown references must remain `[OPEN]`. [EXPLICIT]
3. Identify workflow ID, objective, trigger, actors, inputs, outputs, KPIs,
   failure modes, and escalation target. [EXPLICIT]
4. Decompose into 3-7 linear steps. Each step must have all 12 traceability
   fields. [EXPLICIT]
5. Assign RACI roles using real agents or explicit human roles. Do not use
   anonymous owners such as "team" or "someone". [EXPLICIT]
6. Add DoD, QA checklist, KPIs, fallback route, and escalation route before
   writing the final answer. [EXPLICIT]
7. Validate against `assets/quality-gates.json`; run the script when a JSON
   spec or fixture is available. [EXPLICIT]

## Quality Standards

| Field | Good | Block |
|---|---|---|
| `objective` | "Produce a reviewed PR package with local gates passed" | "Handle the PR" |
| `trigger` | "`/jm:harden-skill workflow-creator` is invoked" | "When needed" |
| `whyThisMatters` | "Without validation, ledger closure may certify an untested skill" | "This step validates" |
| `actionInstruction` | "Run `validate-skill-dod.py --skill {{skill}}` and capture exit code" | "Check the skill" |
| `validationRule` | "Exit code is 0 and output contains `dod=pass`" | "Looks correct" |
| `failureSignal` | "Exit code non-zero or missing `dod=pass` token" | "It fails" |
| `recoveryAction` | "Stop, patch missing asset or eval case, rerun the gate" | "Try again" |
| `kpis` | "`local_gate_failures`, target `0`, unit `count`" | "Quality is good" |

## Worked Example (minimal)

A 3-step workflow showing the contract's intent. The owning skill is unknown,
so it is flagged rather than invented. [EXPLICIT]

```yaml
- id: "pr-gate-review"
  title: "PR Gate Review"
  objective: "Produce a reviewed PR package with all local gates green"
  trigger: "`/pr-gate-review {branch}` is invoked"
  preconditions:
    - "Branch exists and is pushed"
  inputs:
    - name: "branch"
      type: "string"
      required: true
      description: "Git branch under review; selects the diff to gate"
  steps:
    - stepNumber: 1
      title: "Collect Diff"
      desc: "Fetch the branch diff against base."
      whyThisMatters: "A stale or empty diff certifies the wrong code."
      inputNeeded: "branch (string), base ref (string)"
      actionInstruction: "Run `git diff {base}...{branch}`, capture exit code"
      promptToUse: null
      expectedOutput: "Unified diff text, non-empty"
      validationRule: "Exit 0 and diff length > 0"
      failureSignal: "Exit non-zero or empty diff"
      recoveryAction: "Confirm branch/base names with user; refetch"
      handoffIfNeeded: null
    - stepNumber: 2
      title: "Run Gates"
      desc: "Execute lint, tests, and security scan."
      whyThisMatters: "Skipping a gate ships an unverified change."
      inputNeeded: "diff (string), repo root (path)"
      actionInstruction: "Run `make gate`, capture per-gate exit codes"
      promptToUse: null
      expectedOutput: "Gate report with pass/fail per gate"
      validationRule: "All gates report `pass`"
      failureSignal: "Any gate reports `fail` or errors"
      recoveryAction: "Surface failing gate to author; stop"
      handoffIfNeeded: "code-author"
    - stepNumber: 3
      title: "Assemble Package"
      desc: "Bundle diff, gate report, and summary."
      whyThisMatters: "An incomplete package blocks reviewer decision."
      inputNeeded: "diff (string), gate report (object)"
      actionInstruction: "Render `pr-package.md` from template"
      promptToUse: "Summarize the diff and gate results for a reviewer: {context}"
      expectedOutput: "`pr-package.md` with summary + green gate table"
      validationRule: "File exists and gate table shows all pass"
      failureSignal: "File missing or any gate not pass"
      recoveryAction: "Return to step 2; do not assemble on red"
      handoffIfNeeded: "reviewer"
  mainOutput: "`pr-package.md` review bundle"
  secondaryOutputs:
    - "Gate report log"
  DoD:
    - "All gates pass and package file exists"
  qaChecklist:
    - "Diff matches intended branch"
    - "No gate was skipped"
  raci:
    responsible: "ci-runner-agent"
    accountable: "code-author"
    consulted: "reviewer"
    informed: "none"
  kpis:
    - metric: "local_gate_failures"
      target: "0"
      unit: "count"
      measurement: "Count of fail exits per run"
  cadence: "per-request"
  errorHandling: "On unrecoverable gate error, stop and emit failing gate name"
  fallbackRoute: "stop-and-ask"
  escalationRoute: "reviewer"
```

## Validation Gate

- [ ] All 17 top-level fields are present.
- [ ] `id` is kebab-case and `title` is human-readable.
- [ ] `objective` names the expected deliverable and success outcome.
- [ ] `trigger` is a specific event, command, condition, or request.
- [ ] `preconditions`, `inputs`, `secondaryOutputs`, `DoD`, `qaChecklist`,
  and `kpis` are non-empty lists.
- [ ] There are 3-7 ordered steps.
- [ ] Every step includes all 12 step fields and `stepNumber` values are
  sequential.
- [ ] Every `validationRule`, `failureSignal`, and `recoveryAction` is
  observable enough to fail closed.
- [ ] `failureSignal` is the negation of `validationRule`, not a restatement.
- [ ] RACI fields name concrete agents or roles; `accountable` is a single owner.
- [ ] KPI units are measurable and target values are bounded.
- [ ] `fallbackRoute` and `escalationRoute` name concrete destinations.
- [ ] No placeholder values such as `TBD`, `when needed`, `someone`, or
  `check everything` remain.

## Failure Modes

| Failure | Symptom | Response |
|---|---|---|
| Structurally valid but semantically empty | Validator passes, fields are vague ("Check the skill") | Block on Quality Standards table, not just the schema |
| Branching logic forced into steps | Step desc contains "if/else" or parallel paths | Move alternatives into `validationRule`/`recoveryAction`/sub-workflow |
| Invented owner to clear a gate | `owning_skill_id` or agent named without evidence | Revert to `[OPEN]`; lower stated confidence |
| Non-idempotent step replays harmfully | Recovery rerun duplicates side effects | Make `recoveryAction` idempotent or gate it on prior-state check |
| KPI unmeasurable | `unit` is `boolean` for a continuous quantity | Re-pick unit; ensure `measurement` is executable |

## Edge Cases

- **Conditional logic:** Keep the main step sequence linear. Put alternatives
  in `validationRule`, `recoveryAction`, `fallbackRoute`, or a named
  sub-workflow.
- **External service:** Include timeout, retry budget, error code, and fallback.
- **Single-agent workflow:** Still use 3 phases: prepare, execute, verify.
- **Missing owning skill:** Ask once; if the user proceeds, mark owner `[OPEN]`.
- **Workflow too small:** Recommend a checklist or runbook instead of forcing
  the 17-field contract.
- **Workflow too large:** Split into parent workflow plus sub-workflows.
- **Retry/idempotency:** State whether a step is safe to re-run; non-idempotent
  steps need a guard in `recoveryAction`. [EXPLICIT]

## Decisions And Trade-offs

- **17 fixed fields over a flexible schema:** trades author freedom for
  reviewability and deterministic validation. Workflows that genuinely need
  fewer fields should be checklists/runbooks instead. [INFERRED]
- **Linear steps only:** a single ordered sequence is auditable; branching is
  pushed into recovery/fallback/sub-workflows so the happy path stays readable.
  Cost: deeply conditional processes need decomposition into several
  workflows. [INFERRED]
- **Offline validation only:** guarantees reproducibility and zero side effects,
  at the cost of not catching strategic or semantic errors — which is why human
  review and the Quality Standards table remain mandatory. [EXPLICIT]

## Assumptions And Limits

- This skill creates workflow definitions; it does not execute them.
- Deterministic validation proves structure, not strategic correctness.
- Catalog alignment depends on local files available in the current workspace;
  absent files make the corresponding gate unverifiable, not passed. [EXPLICIT]
- Network lookup is off by default and requires explicit user request plus
  source attribution.

---
**Author:** Javier Montano | **Last updated:** 2026-06-11
