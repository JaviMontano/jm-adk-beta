# JM-ADK Beta — Agent Contract

The native shape of every agent in this harness. Synthesizes the useful parts of
plugin-dev (frontmatter discipline, color/model, least-privilege tools), BMAD-METHOD
(domain-expert committee, phased flow), and gstack (officer roster, sprint phases,
command-bound roles) — WITHOUT importing their verbose bodies. Beta agents stay
**caveman-dense**: every line earns its place. [DOC]

Validated by `scripts/validate-agent.sh`. Constitution v7 + the active profile govern
all agents; the active profile (`profiles/`) declares brand/domain. [CONFIG]

## The office (tiers)
A hierarchical office, not a flat list. [DOC]
- **ceo** — **Pristino** (`agents/pristino-ceo.md`). Intent intake, strategic delegation, final sign-off; reference for the SME layer. One.
- **coo** — the orchestration lead (`agents/orchestrator.md`). Operational dispatch/sequencing/gates/aggregation; reports to the CEO. One.
- **officer** — a functional committee member (13, `agents/*.md`), reports to the COO. Thin: routes to skills, never duplicates a skill's body. Each may declare **≤5 parametric sub-specialists** (focus-modes, NOT separate files). [DOC]
- **steward** — harness Ops/upkeep (`agents/*.md`): repo-steward, harness-maintainer, skill-curator, workspace-steward, context-optimizer. Reports to the COO. Keep the kit, the repo, local skills, workspaces, and the context window healthy. [DOC]
- **sme** — a domain consulting advisor (13, `agents/sme/*.md`) for the vibe coder + knowledge worker; read-only ADVICE (officers/spokes execute). Pristino is their reference. [DOC]
- **role-template** — a parametrized spoke (`references/roles/{lead,support,guardian,specialist}.md`), instantiated per skill with `{{skill}}`. [DOC]
- **spoke** — a per-skill instance (`skills/<id>/agents/*.md`) from a role-template. [DOC]

## Sub-specialists (parametric, ≤5 per officer)
An officer's specialized focus-modes are **parametric, not separate files** — "always still the
officer." Declare in frontmatter `specialists: [focus-a, focus-b, …]` (≤5) + a `## Sub-specialists`
section (one line each: focus + trigger) + a `focus` dispatch param. The officer activates a
focus-mode; no new agent file is created. [CONFIG]

## CORE vs LOCAL skills (preserve alfa's local-skill capability)
- **CORE** = `skills/` — the 73 kit skills. Immutable except via **harness-maintainer**. [CONFIG]
- **LOCAL** = `workspace/<active>/skills/` — project-scoped skills the user creates, owned by
  **skill-curator**; created/administered/used but NEVER written into `skills/` core, never
  registered in the core catalog, never allowed to shadow a core id silently. The
  `artifact-placement-guard` enforces the boundary. [CONFIG]

## Frontmatter (YAML) — required unless marked optional
```yaml
---
name: kebab-case            # officer: bare; spoke: "{{skill}}-{role}". start/end alnum, hyphens only
role: Title Case            # human role label (e.g. Orchestrator, Planner)
description: one line        # the DISPATCH trigger — when the hub routes here. No <example> blocks.
model: haiku|sonnet|opus|inherit   # tier hint: haiku=narrow extract, sonnet=default, opus=cross-domain synthesis
color: blue|cyan|green|yellow|magenta|red   # blue/cyan=analysis · green=build · yellow=validate · red=security/governance · magenta=creative/brand
tools: [Read, Grep, ...]    # least-privilege; omit ONLY for the orchestrator (needs Agent+all)
phase: Think|Plan|Build|Review|Validate|Ship   # gstack sprint position
tier: ceo|coo|officer|steward|sme|role-template|spoke
specialists: [focus-a, ...] # optional, officers only; ≤5 parametric focus-modes (NOT separate files)
routes: [skill-id, ...]     # optional; skills/playbooks this agent may dispatch (officers/dev)
---
```

## Body — compressed but complete (target ≤ ~60 lines)
```
# <Role>
> one-line creed

## Mission
2–3 lines: what this agent owns end-to-end.

## Scope / Anti-scope  [EXPLICIT]
- In: ...
- Anti-scope: ... (what it must NEVER do — hard refusals)

## Process
Discover → Analyze → Execute → Validate (compressed; name the tools/skills used per step).

## Inputs / Outputs
- In: ...
- Out: contract-format result (locator / receipt / findings / deliverable). Hub never forwards raw transcripts.

## Guardrails
Evidence tag every non-trivial claim ([CODE]/[CONFIG]/[DOC]/[INFERENCE]/[ASSUMPTION]).
Estimation = computed (P8), never guessed. Profile-aware (brand/currency from active profile).
No invented prices. No green-as-success. Single brand per output (active profile).

## Acceptance
The gate this agent's output must pass before it ships upstream.
```

## Rules
1. **Officers are thin.** An officer routes to skills (`routes:`) and orchestrates; it does
   not re-implement a skill's playbook. If an officer's body grows past ~60 lines, the logic
   belongs in a skill. [DOC]
2. **Hub-and-spoke isolation.** Spokes get fresh context + ONE routed playbook; the hub
   aggregates contract-format results only — never raw spoke transcripts (kata
   `hub-and-spoke-isolation`). [DOC]
3. **Least privilege.** `tools` is the minimum set. Read-only agents: `[Read, Grep, Glob]`
   (+`Bash` for inspection only). Only the orchestrator gets `Agent`. [CONFIG]
4. **Evidence + governance.** Every agent inherits Constitution v7 + the active profile;
   anti-scope must name the hard refusals; single-brand only, no invented prices, no green-as-success. [CONFIG]
5. **Pristino** is the orchestrator's persona, not a separate file. [DOC]

## Anti-patterns (rejected by validator or review)
- Verbose plugin-dev-style body (1000–2000 words) — beta is dense. [DOC]
- `<example>` trigger blocks — beta dispatches explicitly via the orchestrator, not proactive matching. [DOC]
- Missing `color`/`model`/`phase`/`tier`. [CONFIG]
- An officer that duplicates a skill instead of routing to it. [INFERENCE]
- Generic name (helper, assistant, agent). [CONFIG]
