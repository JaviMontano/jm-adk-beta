<!-- distilled from alfa skills/prompt-creator -->
<!-- Generates deterministic prompt files for agentic ecosystems using the canonical prompt-type matrix, including meta prompts, system-user pairs, handoffs, committee deliberation, synthesis, validation, fallback, and redirects for agent constitutions and workflow steps. Use when the user asks to create a prompt, write a handoff prompt, generate a meta prompt, build a committee deliberation prompt, make a fallback prompt, or design agent prompts. If prompt type or owning agent is missing, interview for the minimum required inputs before writing. [EXPLICIT] -->
# Prompt Creator

Generate deterministic prompt files for multi-agent ecosystems. The output is a prompt artifact plus a validation packet, not a free-form writing exercise. Covers 9 prompt types from system prompts to committee deliberation to fallback recovery. [EXPLICIT]

## When to Activate

Use this skill when the user requests one of these actions:

- create, write, generate, or improve a reusable prompt for an agent
- create a meta prompt, handoff prompt, validation prompt, fallback prompt, committee deliberation prompt, or synthesis prompt
- design a prompt contract for multi-agent routing, execution, validation, recovery, or handoff
- the user names an agent but omits prompt type; interview for prompt type, target agent, source files, and success criteria

Do not use this skill for the downstream work the prompt will perform. For full agent constitutions, route to `agent-constitution-creator`. For workflow step definitions, route to `workflow-creator`.

**Anti-scope** (out of bounds even if asked): executing the generated prompt; authoring the agent constitution itself (type 1 → redirect); inventing the runtime that fills placeholders; producing prompts for agents that do not exist on disk; embedding live secrets, PII, or fetched remote content. [EXPLICIT]

## Assumptions & Limits

- **Assumes** an agentic ecosystem with defined agents; generated prompts must reference real source agent files or report the gap. [SUPUESTO]
- **Assumes** the orchestrator, not this skill, supplies values for `{{placeholders}}` at runtime. [SUPUESTO]
- **Limit**: Prompts are templates, not runtime; placeholders (`{{var}}`) are filled by the orchestrator.
- **Limit**: Committee prompts (deliberation/synthesis) require at least 3 agents to be meaningful; with fewer, emit `insufficient_committee_size` and propose a single validation_prompt instead. [EXPLICIT]
- **Limit**: One artifact per invocation. A request that bundles types (e.g. "handoff + fallback") is split into separate files, not merged. [EXPLICIT]
- **Trade-off**: More detailed prompts = more predictable agent behavior but less adaptability. For creative/open-ended tasks, keep the Framework loose and the Constraints tight (bound the failure surface, not the method). [INFERENCIA]
- **Trade-off**: Strict frontmatter + validation gate add friction to authoring but make prompts machine-checkable by `validate_prompt_artifact.py`; this skill always pays that cost. [INFERENCIA]

## Usage

```
/prompt-creator meta_prompt data-analyst
/prompt-creator handoff_prompt customer-onboarding
/prompt-creator committee_deliberation                # interview mode
```

Parse `$1` as prompt type, `$2` as owning agent ID. If either is missing, enter interview mode and ask for: prompt type, target agent, source agent path, success criteria. Do not guess. [EXPLICIT]

## Before Generating

1. **Read the agent**: `Read agents/$2/agent.md` or the user-provided source path. If absent, emit `missing_source_agent` and ask before writing. [EXPLICIT]
2. **Check existing prompts**: `Glob agents/$2/prompts/*.md` to avoid duplicates and name collisions. Collision without explicit "update" intent → stop and ask. [EXPLICIT]
3. **Read prompt spec**: `Read references/prompt-types-spec.md` if available, then apply `assets/prompt-type-matrix.json` for the type's required sections and failure modes.
4. **Apply checklist**: use `assets/prompt-contract-checklist.md` before finalizing.

## Deterministic Contract

The single source of no-invention rules for this skill. All other sections defer here. [EXPLICIT]

- **Type**: must be one of the 9 rows in `assets/prompt-type-matrix.json`. Unknown type → `unknown_prompt_type`, list the 9, ask.
- **Owning agent ID**: from a source file, explicit user input, or a clearly marked placeholder — never invented.
- **Frontmatter**: must include `type`, `owningAgent`, `sourceAgentMd`, `version`, `createdBy`, `validationStatus`. Missing any → fail the gate.
- **Placeholders**: every placeholder is descriptive snake_case inside `{{...}}`. Reject `{{x}}`, `{{var}}`, `{{1}}`, and unlabeled placeholders.
- **No invention**: do not invent agents, tools, commands, files, quality gates, brand constraints, dates, or time estimates. Use user-provided values or explicit placeholders. Never claim an agent constitution was read unless a path was inspected.
- **No overwrite**: do not overwrite an existing prompt path unless the user explicitly asks for an update.
- **No execution**: do not perform the prompt's downstream task.
- **Time / network / randomness**: use the session date only when the user or runtime provides it, else `{{created_date}}`; do not fetch remote fonts, templates, or examples; no random names or nondeterministic ordering — sort candidates by prompt type then slug.
- **Missing context**: if required context is missing, return a gap packet (see below) instead of filling creatively.

### Gap packet (the deterministic failure output)

When context is missing, do not write a partial prompt. Return:

```yaml
status: gap
missing:
  - id: missing_source_agent      # machine-readable code
    need: "path to agents/<id>/agent.md"
    blocks: "agent identity preamble, sourceAgentMd frontmatter"
next_action: "ask user for source path, then re-run"
```

Known codes: `missing_source_agent`, `unknown_prompt_type`, `insufficient_committee_size`, `prompt_path_collision`, `coverage_gap`, `redirect_required` (types 1/4). [EXPLICIT]

## The 9 Types

| # | Type | File Pattern | Purpose | Complexity |
|---|---|---|---|---|
| 1 | `agent_system_prompt` | `agent.md` | Full constitution | → Use `/agent-constitution-creator` |
| 2 | `meta_prompt` | `prompts/meta-{topic}.md` | Behavioral instruction for ONE aspect | Low |
| 3 | `system_user_pair` | `prompts/pair-{scenario}.md` | Reusable system+user template | Low |
| 4 | `workflow_step_prompt` | Inline in skill.yaml | Step-level LLM instruction | → Use `/workflow-creator` |
| 5 | `handoff_prompt` | `prompts/handoff.md` | Task transfer protocol | Medium |
| 6 | `committee_deliberation` | `prompts/deliberation.md` | Independent multi-agent evaluation | High |
| 7 | `committee_synthesis` | `prompts/synthesis.md` | Merge multiple agent responses | High |
| 8 | `validation_prompt` | `prompts/validation.md` | Quality validation of outputs | Medium |
| 9 | `fallback_prompt` | `prompts/fallback.md` | Recovery when primary fails | Medium |

Types 1 and 4 redirect (emit `redirect_required`); this skill handles types 2, 3, 5-9. [EXPLICIT]

## Output Format

Write to `agents/{agentId}/prompts/{filename}.md`: [EXPLICIT]

```markdown
---
type: "{promptType}"
owningAgent: "{agentId}"
sourceAgentMd: "agents/{agentId}/agent.md"
version: "1.0.0"
createdBy: "prompt-creator"
validationStatus: "draft|validated"
---

# {Title}

{Content per type-specific rules below}
```

Every generated body — regardless of type — must contain these seven elements (the universal contract): purpose, inputs, procedure, output contract, validation gate, failure handling, and a handoff/next-action boundary. Type-specific rules below say *how* each type expresses them, not whether. [EXPLICIT]

## Type-Specific Rules

### meta_prompt — Behavioral aspect instruction
- **Focus**: Exactly ONE aspect: reasoning OR formatting OR restrictions OR style.
- **Structure**: Preamble (agent identity) → Framework (the rules) → Constraints (boundaries).
- **Anti-pattern**: Combining reasoning + formatting in one meta_prompt → split into two files.
- **Edge**: If the user asks for two aspects in one, emit two artifacts, not one merged file.

```markdown
# Reasoning Meta-Prompt

You are {{agent.name}}. Your role: {{agent.role}}. [EXPLICIT]

## Framework
1. {Step 1 of reasoning process}
2. {Step 2}

## Constraints
- {Hard limit 1}
- {Hard limit 2}
```

### system_user_pair — Reusable scenario template
- **Must have**: `## System` and `## User` sections.
- **System**: Sets context, constraints, output format.
- **User**: Scenario template with `{{placeholders}}`.
- **Design rule**: Each pair handles ONE scenario (not a Swiss Army knife).
- **Edge**: A pair with zero `{{placeholders}}` is a hardcoded message, not a template → flag and ask whether parameterization was intended.

### handoff_prompt — Task transfer protocol
- **Must specify**:
  - Context to PASS: task state, progress, relevant data.
  - Context to OMIT: internal reasoning, failed attempts, irrelevant history.
  - Target agent: explicit ID (never `{{x}}` and never invented).
  - Success criteria: how the target agent knows it is done.
- **Anti-pattern**: Passing the entire conversation (context explosion). Passing-and-omitting must both be present — omitting nothing fails the gate.

### committee_deliberation — Independent evaluation
- **Must require**: each agent gives an INDEPENDENT opinion FIRST, before seeing others.
- **Must include**: a scoring rubric with weighted dimensions.
- **Must specify**: an output format for structured comparison.
- **Key insight**: committee value comes from independence — if agents see each other's work first, they converge prematurely (anchoring). Prompt must make sequencing explicit.
- **Edge**: fewer than 3 agents → `insufficient_committee_size`.

### committee_synthesis — Multi-response merger
- **Must define**: redundancy-removal strategy, conflict-resolution method, confidence weighting.
- **Merge strategies** (pick by output type):
  - Majority vote → binary / categorical decisions.
  - Weighted average → numeric assessments.
  - Reasoned selection → qualitative choices (requires written justification per pick).
- **Edge**: an unbreakable tie or contradictory high-confidence inputs → escalate, do not silently pick one.

### validation_prompt — Quality checker
- **Must define**: pass/fail criteria with severity levels (critical/major/minor).
- **Must produce**: actionable feedback — not "this could be better" but "section 3 missing required field X".
- **Must reference**: the DoD / qaChecklist from the originating workflow (cite it, do not re-derive criteria).
- **Edge**: no DoD available → `coverage_gap`; do not invent acceptance criteria.

### fallback_prompt — Recovery playbook
- **Must define**: trigger conditions (when does fallback activate?).
- **Must specify**: preservation priorities (what to save vs sacrifice).
- **Must include**: a user-communication template (how to explain the degradation honestly — no green-as-success spin on a degraded result).
- **Must have**: an escalation path if the fallback also fails (never a dead end).

## Worked Examples

### handoff_prompt — bad vs good

**Bad** (fails gate: no pass/omit split, no success criteria):
```
Hand off the task to the next agent. [EXPLICIT]
```

**Good**:
```markdown
## Handoff Protocol: {{source_agent}} → {{target_agent}}

### Context to Pass
- Task ID: {{task_id}}
- Current state: {{state_summary}}
- Completed steps: {{completed_steps}}
- Pending decision: {{decision_needed}}

### Context to Omit
- Internal reasoning chains
- Failed approaches and why they failed
- Intermediate calculations

### Success Criteria
The handoff is complete when {{target_agent}} confirms: [EXPLICIT]
- [ ] Context received and understood
- [ ] Can proceed without clarification
- [ ] Estimated completion: {{time_estimate}}
```

### validation_prompt — actionable, severity-tiered

```markdown
# Output Validation: {{artifact_name}}

## Criteria (from {{source_dod_path}})
Evaluate the artifact against the cited DoD only. Do not add criteria. [EXPLICIT]

## Report Format
| Severity | Location | Finding | Required fix |
|----------|----------|---------|--------------|
| critical | {{loc}}  | {{what is missing/wrong}} | {{exact change}} |

## Verdict
- PASS only if zero critical and zero major findings.
- Otherwise FAIL with the table above; never soften a critical to a minor.
```

### fallback_prompt — honest degradation

```markdown
# Fallback: {{primary_capability}} unavailable

## Trigger
Activate when {{trigger_condition}} (e.g. primary tool returns error 3x).

## Preserve vs Sacrifice
- Preserve: {{must_keep_outputs}}
- Sacrifice: {{acceptable_to_drop}}

## User Message Template
"{{primary_capability}} is unavailable, so this result is {{degraded_how}}.
What you can rely on: {{preserved}}. What is missing: {{sacrificed}}." [EXPLICIT]

## Escalation
If fallback also fails → {{escalation_target}} with {{handoff_summary}}.
```

## Validation Gate

Fail closed: any unchecked box blocks `validationStatus: validated`. [EXPLICIT]

- [ ] YAML frontmatter has type, owningAgent, sourceAgentMd, version, createdBy, validationStatus
- [ ] Type is one of the 9 (or redirects via `redirect_required`)
- [ ] agent.md was actually read and the prompt references agent identity
- [ ] Missing agent/spec/context emitted a gap packet instead of invented content
- [ ] The seven universal elements (purpose, inputs, procedure, output contract, validation gate, failure handling, handoff boundary) are all present
- [ ] Type-specific rules followed (see per-type section)
- [ ] No empty sections; no hardcoded message masquerading as a template
- [ ] All `{{placeholders}}` are descriptive snake_case (no `{{x}}`, `{{var}}`, `{{1}}`)
- [ ] Duplicate existing prompt path was checked (no silent overwrite)
- [ ] Committee prompts require independent evaluation before comparison and ≥3 agents
- [ ] Handoff prompts specify BOTH what to pass AND what to omit
- [ ] Validation prompts include severity levels and cite an external DoD
- [ ] Fallback prompts include preservation priorities AND an escalation path
- [ ] `assets/prompt-contract-checklist.md` was applied
- [ ] `scripts/validate_prompt_artifact.py` passes on the written file

## Downstream Boundaries

- Prompt files may be consumed by orchestrators, agents, validators, and renderers.
- The prompt artifact must not include hidden reasoning, secrets, private user context, or unverified runtime state.
- The validation packet must list unresolved gaps so the next workflow can stop or ask before execution.

## Assets & Scripts

- `assets/prompt-contract-checklist.md` — reusable deterministic prompt gate.
- `assets/prompt-type-matrix.json` — per-type required sections, redirects, failure modes (canonical type list).
- `scripts/validate_prompt_artifact.py` — validates frontmatter, required sections, placeholders, and type-specific gates.
- `scripts/check.sh` — runs deterministic fixtures; must pass before ledger closure.

## Edge Cases

| Scenario | Handling | Code |
|----------|----------|------|
| Empty or minimal input | Request clarification before proceeding | — |
| Conflicting requirements | Flag conflicts explicitly, propose resolution | — |
| Out-of-scope request | Redirect to appropriate skill or escalate | `redirect_required` |
| Type is 1 or 4 | Redirect to constitution/workflow creator | `redirect_required` |
| Unknown prompt type | List the 9, ask | `unknown_prompt_type` |
| Source agent.md absent | Gap packet, ask for path | `missing_source_agent` |
| Existing prompt at target path | Stop unless explicit update intent | `prompt_path_collision` |
| Committee with <3 agents | Propose single validation_prompt instead | `insufficient_committee_size` |
| Missing DoD for validation | Do not invent criteria; report | `coverage_gap` |
| Two prompt types requested at once | Split into separate artifacts | — |

---
**Author:** Javier Montaño | **Last updated:** March 12, 2026
