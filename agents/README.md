# Agents — the officer committee

Beta's agent layer, on the native **agent contract** (`references/agent-contract.md`),
validated by `scripts/validate-agent.sh`. Three tiers: **officer** (here), **role-template**
(`references/roles/`), **spoke** (`skills/<id>/agents/`). [DOC]

Inspired by alfa (archetypes distilled — NOT its 260 per-skill wrappers), **BMAD-METHOD**
(domain-expert committee, phased flow) and **gstack** (officer roster, sprint phases). Beta
agents stay caveman-dense and dispatch explicitly via the orchestrator (hub-and-spoke) — no
proactive-trigger `<example>` blocks. [DOC]

## The 13 officers (by sprint phase)
| # | Officer | Phase | Color | Routes to (skills) |
|---|---------|-------|-------|--------------------|
| 1 | **orchestrator (Pristino)** | Plan | red | agent/subagent-orchestration, plan-mode |
| 2 | input-analyst | Think | cyan | prompting-and-meta-prompting, frontload-prompt |
| 3 | planner | Plan | blue | plan-mode-workflow |
| 4 | dev-coordinator (vibe-coding) | Build | green | safe-scripting, tool-use, mcp-engineering |
| 5 | transformation-architect | Plan | magenta | ai-architecture, agent-orchestration, automation |
| 6 | builder | Build | green | — |
| 7 | investigator | Think | cyan | adaptive-investigation-method |
| 8 | reviewer | Review | blue | — |
| 9 | governance-guardian | Review | red | guardrails |
| 10 | researcher | Validate | cyan | official-source-verifier, research-start |
| 11 | brand-design-lead | Ship | magenta | brand-output, ux-design, accessibility |
| 12 | estimation-officer | Validate | yellow | (scripts/estimate.py) |
| 13 | memory-steward | Ship | blue | persistent-memory-design, jarvis-os, session-* |

Sprint: input-analyst (Think) → planner (Plan) → dev/builder/transformation (Build) →
reviewer/governance-guardian (Review) → researcher/estimation (Validate) → brand/memory (Ship).
The orchestrator (Pristino) conducts all phases. [DOC]

## Officers are thin
An officer routes to skills (`routes:`) and orchestrates; it never re-implements a skill's
playbook. If a body grows past ~80 lines, the logic belongs in a skill (validator warns). [CONFIG]

## Per-skill dispatch (role-templates → spokes)
For single-skill work the orchestrator instantiates the 4 role-templates with `{{skill}}`:
**lead** (deliverable) · **specialist** (domain) · **support** (scripts/git/IO) · **guardian**
(read-only validate/gate). The 292 `skills/<id>/agents/*.md` are these instances. The
transversal **governance-guardian** officer (#9) is distinct from the per-skill `guardian`
spoke: officer = cross-cutting Constitution/profile governance; spoke = one skill's gate. [DOC]

## Adding an officer
1. Copy the contract shape from any officer here; set `tier: officer`.
2. Keep it thin — declare `routes:` instead of inlining a skill.
3. `bash scripts/validate-agent.sh agents/<name>.md` → 0 errors. [CONFIG]

**Anti-scope:** no per-skill wrappers (alfa regression); no agent that only renames a role's
`{{skill}}`; no price logic; single-brand only; no green-as-success. [DOC]
