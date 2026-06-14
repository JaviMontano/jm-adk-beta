<!-- distilled from alfa skills/agent-creator -->
<!-- Create deterministic Claude Code custom agent definitions with trigger conditions, bounded system prompts, least-privilege tools, model selection, and validation checks. Use when the user asks to create an agent, add a subagent, make a custom agent, define an agent definition, or build an autonomous subprocess for a specific project responsibility. [EXPLICIT] -->
# Agent Creator

Create custom Claude Code agents: autonomous subprocesses with isolated
context, specific tools, and tailored system prompts. [EXPLICIT]

## When To Activate

Use this skill when the user asks for a persistent subagent or custom agent
definition, for example:

- "create an agent"
- "add a subagent"
- "make a custom agent"
- "define agent definition"
- "build an agent for X"
- "I need something to handle X automatically"

Use `agent-constitution-creator` instead when the user needs a full
governance constitution with identity, authority, memory, handoff, and
multi-agent operating rules.

### Negative Triggers (do NOT activate) [EXPLICIT]

- User wants a one-off action done now, not a reusable definition — just do it.
- User says "skill", "command", "hook", or "output style" explicitly — route there.
- User wants a multi-agent governance charter — route to
  `agent-constitution-creator`.
- User wants to edit an existing agent's behavior only — read the existing file,
  patch it, skip the discovery/normalize steps.

### Assumptions [EXPLICIT]

- Target runtime is Claude Code (subagents spawned by a parent session with
  isolated context). [EXPLICIT]
- Agent files are Markdown + YAML frontmatter at `.claude/agents/{name}.md`
  (project) or `~/.claude/agents/{name}.md` (global). [EXPLICIT]
- Built-in agent names `Explore`, `Plan`, `general-purpose` are reserved and
  must not be shadowed. [EXPLICIT]
- The parent — not the agent — decides when to spawn, based solely on the
  `description` field; the agent never sees parent chat history. [EXPLICIT]
- If any assumption is false (different runtime, different file layout), STOP and
  confirm with the user before compiling. [OPEN]

## Deterministic Contract

- Use `assets/agent-spec-schema.json` as the canonical structured input shape.
- Use `assets/tool-policy.json` to choose least-privilege tools and reject
  wildcard access.
- Use `assets/model-selection-policy.json` to map complexity to `haiku`,
  `sonnet`, or `opus`.
- Use `assets/description-trigger-policy.json` to keep descriptions focused on
  WHEN the parent should spawn the agent.
- Use `assets/agent-template.md` as the rendering skeleton.
- Run `scripts/compile-agent.py` before finalizing an agent definition from
  structured input.
- Run `scripts/check.sh` to verify positive and negative fixtures offline.
- Do not call external APIs, MCP servers, network resources, or live agent
  registries from the skill scripts.

## Procedure

### Step 1: Decide Whether An Agent Is Appropriate

Do not create an agent when a lighter artifact fits better:

| Situation | Better alternative |
|---|---|
| One-off task instruction | Inline response |
| Reusable multi-step workflow | Skill with assets and scripts |
| Simple output format change | Output style |
| Always-run automation | Hook |
| Persistent project rule | CLAUDE.md or AGENTS.md source |

If the request is underspecified, ask only for the missing fields required by
`assets/agent-spec-schema.json`: responsibility, scope, read/write authority,
expected output, and complexity.

Worked decision: "I want something to keep my changelog updated on every commit"
→ this is *always-run automation*, not an agent. Route to a Hook. [EXPLICIT]
"Review every PR diff for security issues when I ask" → bounded, on-demand,
read-only → agent is correct. [EXPLICIT]

### Step 2: Discover Existing Agents

1. Read project-local agent definitions, usually `.claude/agents/*.md`.
2. Read global definitions only when the user asks for a global agent.
3. Check for name collisions with built-ins: `Explore`, `Plan`,
   `general-purpose`.
4. Check for scope overlap. If another agent owns the same responsibility,
   propose rename, merge, split, or non-goals before writing.

### Step 3: Normalize The Spec

Normalize the request into five sections:

- `agent`: name, display name, role, responsibility, scope, and non-goals.
- `routing`: trigger phrases, negative triggers, destination scope, model,
  color, and tools.
- `behavior`: task statement, ordered process, output format, constraints, and
  reasoning tier.
- `quality`: quality bar, validation checks, escalation triggers, and residual
  risks.
- `evidence`: source labels and evidence tags for decisions that came from the
  user, codebase, or inference.

### Step 4: Compile

```bash
python3 skills/agent-creator/scripts/compile-agent.py \
  --input skills/agent-creator/scripts/fixtures/agent-spec-input.json
```

The compiler emits Markdown by default and stable JSON with `--format json`.
It fails if the name is invalid, trigger conditions are missing, model or tools
are unsafe, process steps are too thin, output format is absent, constraints
lack a negative boundary, or collision rules are violated.

### Step 5: Validate

- Run `bash skills/agent-creator/scripts/check.sh`.
- Run `python3 -B scripts/validate-skill-dod.py --skill agent-creator`.
- Run `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill agent-creator`.
- Treat runtime installation into `.claude/agents/` or `~/.claude/agents/` as a
  separate user-approved mutation.

## Worked Example: PR Security Reviewer [EXPLICIT]

Request: "Make an agent that reviews PR diffs for security problems when I ask."

Normalized spec (abridged):

- `agent.responsibility`: flag security issues in a supplied diff. `non-goals`:
  fixing code, running the app, reviewing style.
- `routing.triggers`: "review this diff for security", "security-check the PR".
  `negative_triggers`: "fix", "refactor", "format". `model`: `sonnet`.
  `tools`: `["Read", "Glob", "Grep"]` (read-only — it never writes).
- `behavior.output`: a table of `severity | file:line | issue | fix`.
- `quality.escalation`: if no diff is provided, report back instead of scanning
  the whole repo.

Compiled frontmatter:

```yaml
name: "pr-security-reviewer"
description: "Spawn when the user asks to review a PR or diff for security
  issues. Do NOT spawn to fix, refactor, or format code."
model: "sonnet"
tools: ["Read", "Glob", "Grep"]
```

Why these choices: read-only tools because the agent only *reports*
(least privilege, Tool Restriction Patterns); `sonnet` because security triage is
balanced reasoning, not a trivial check (Model Selection); negative triggers
because "review" and "fix" frequently co-occur and would otherwise over-spawn
(Edge Cases). [EXPLICIT]

## Acceptance Criteria [EXPLICIT]

An agent definition is DONE only when ALL hold:

1. `compile-agent.py` exits 0 on the structured input. [EXPLICIT]
2. `check.sh` passes positive AND negative fixtures. [EXPLICIT]
3. Every box in the Validation Gate is checked. [EXPLICIT]
4. The Worked Example pattern is matched: description states WHEN, tools are
   least-privilege, output format is a table or code block, constraints contain
   at least one "never"/"do not". [EXPLICIT]
5. No write to `.claude/agents/` happened without explicit user approval. [EXPLICIT]

## Agent File Anatomy

Project file: `.claude/agents/{name}.md`
Global file: `~/.claude/agents/{name}.md`

```markdown
---
name: "{kebab-case-name}"
description: "{When Claude should spawn this agent - be specific about trigger conditions}"
model: "{haiku|sonnet|opus}"
color: "{hex, e.g. #4CAF50}"
tools: ["{minimum tool set}"]
---

# {Agent Name}

You are {Name}, a specialized agent that {concrete role}.

## Your Task

{Specific, bounded description. Include what to analyze, what to produce, and
what format to use.}

## Process

{Numbered steps the agent follows. Each step is a concrete action.}

## Output Format

{Exact structure of the expected output. Use code blocks or tables.}

## Constraints

- {Hard boundaries: what NOT to do}
- {Escalation triggers: when to report back instead of acting}

## Reasoning Discipline

Apply structured thinking to every analysis and recommendation.

## Quality Bar

- {Minimum standard each output must meet}
```

## Frontmatter Decision Matrix

| Field | Required | Decision Logic |
|---|---|---|
| `name` | Yes | Kebab-case id for logs and routing. |
| `description` | Yes | Must state WHEN to spawn, not just WHAT it does. |
| `model` | Recommended | `haiku` for simple checks, `sonnet` for balanced analysis, `opus` for deep reasoning. |
| `color` | Optional | Hex color for terminal UI. |
| `tools` | Recommended | Explicit list following least privilege. Empty list is advisory-only. |

## Tool Restriction Patterns

| Pattern | Tools | Use Case | Risk Level |
|---|---|---|---|
| Advisory | `[]` | Planning, brainstorming | None |
| Read-only | `["Read", "Glob", "Grep"]` | Review, analysis, audit | Low |
| Read with shell | `["Read", "Glob", "Grep", "Bash"]` | Deterministic inspection | Medium |
| Read-write | `["Read", "Write", "Edit", "Glob", "Grep"]` | Artifact generation | Medium |
| Builder | `["Read", "Write", "Edit", "Bash", "Glob", "Grep"]` | Build and test | High |

Default to read-only unless the agent must create or modify artifacts.

## System Prompt Design Principles

| Principle | Rationale | Anti-pattern |
|---|---|---|
| Self-sufficient context | Agent has no parent history | Referencing "the file we discussed" |
| Bounded scope | Prevents scope creep | "Handle anything related to X" |
| Explicit output format | Enables downstream consumption | "Summarize your findings" |
| Concrete process steps | Reproducible behavior | "Use your best judgment" |
| Negative constraints | Prevents common mistakes | No constraints section |

## Validation Gate

- [ ] Request is better served by a subagent than by CLAUDE.md, a skill, an
      output style, or a hook.
- [ ] File is valid Markdown with YAML frontmatter.
- [ ] `name` and `description` are present and non-empty.
- [ ] `description` states trigger conditions (WHEN), not just capabilities
      (WHAT).
- [ ] `tools` is explicitly listed and limited by least privilege.
- [ ] System prompt is self-sufficient; no parent-context references.
- [ ] Output format is explicitly defined with a code block or table.
- [ ] Constraints include at least one "do not" or "never" boundary.
- [ ] No naming collision with `Explore`, `Plan`, or `general-purpose`.
- [ ] Model selection is justified by task complexity.
- [ ] Reasoning discipline section is present.
- [ ] Assets and scripts are used for deterministic compilation.
- [ ] Runtime write or installation is user-approved.

## Edge Cases

- If the agent needs project-specific context, include discovery steps in the
  prompt instead of copying parent chat history.
- If the agent spawns too often, narrow trigger phrases and add negative
  triggers.
- If the output is too verbose, add a hard line limit to the output format.
- If related agents overlap, define a team only when ownership boundaries are
  explicit per file, module, or workflow stage.

## Failure Modes [EXPLICIT]

| Symptom | Root cause | Fix |
|---|---|---|
| Agent never spawns | `description` states WHAT, not WHEN | Rewrite to trigger phrases the parent can match. |
| Agent spawns on unrelated turns | Triggers too broad; no negatives | Narrow phrases, add `negative_triggers`. |
| Agent edits files it should only read | Tools over-granted | Drop to read-only set; re-run compile. |
| Output unusable downstream | Format is prose, not structured | Define an exact table/code-block schema. |
| Agent asks parent for missing context | Prompt references parent history | Add in-prompt discovery steps (Glob/Grep/Read). |
| Two agents fight over the same files | Overlapping ownership | Split by file/module/stage, or merge into one. |
| `compile-agent.py` exits non-zero | Thin process, no negative constraint, unsafe tools | Read the error; it names the failing gate. |

## Trade-offs [EXPLICIT]

- Read-only vs read-write: read-only is safer and the default, but forces a
  human to apply changes. Grant write only when the agent's *purpose* is
  producing artifacts. [EXPLICIT]
- `haiku` vs `sonnet` vs `opus`: cheaper/faster models trade reasoning depth.
  Under-spec'ing causes shallow misses; over-spec'ing wastes budget on trivial
  checks. Justify the pick against task complexity, not preference. [EXPLICIT]
- One broad agent vs several narrow agents: broad agents over-spawn and blur
  ownership; narrow agents multiply maintenance. Split only on clear ownership
  boundaries (file, module, workflow stage). [EXPLICIT]

## Anti-scope (this skill does NOT) [EXPLICIT]

- Install or activate agents at runtime — that is a separate user-approved
  mutation.
- Author multi-agent governance constitutions — see
  `agent-constitution-creator`.
- Call external APIs, MCP servers, or live registries from scripts.
- Generate hooks, skills, commands, or output styles — route to their creators.

## Related Assets

- `assets/source-map.md`
- `references/domain-knowledge.md`
- `scripts/compile-agent.py`
