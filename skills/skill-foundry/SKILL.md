---
name: skill-foundry
version: 1.0.0
description: "Router for building/certifying agentic assets — skills, agents, commands, prompts, hooks, MCP servers, workflows. Topics: agent-creator, assembly-skill, auto-prompt-matching, benchmark-skill, certify-skill, design-skill, hook-creator, mcp-creator, meta-skill-creator, meta-skill-indexer, prompt-creator, prompt-forge, skill-search, workflow-creator, workflow-forge, x-ray-skill."
params:
  topic:
    enum: [agent-creator, assembly-skill, auto-prompt-matching, benchmark-skill, certify-skill, design-skill, hook-creator, mcp-creator, meta-skill-creator, meta-skill-indexer, prompt-creator, prompt-forge, skill-search, workflow-creator, workflow-forge, x-ray-skill]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  agent-creator: references/agent-creator.md
  assembly-skill: references/assembly-skill.md
  auto-prompt-matching: references/auto-prompt-matching.md
  benchmark-skill: references/benchmark-skill.md
  certify-skill: references/certify-skill.md
  design-skill: references/design-skill.md
  hook-creator: references/hook-creator.md
  mcp-creator: references/mcp-creator.md
  meta-skill-creator: references/meta-skill-creator.md
  meta-skill-indexer: references/meta-skill-indexer.md
  prompt-creator: references/prompt-creator.md
  prompt-forge: references/prompt-forge.md
  skill-search: references/skill-search.md
  workflow-creator: references/workflow-creator.md
  workflow-forge: references/workflow-forge.md
  x-ray-skill: references/x-ray-skill.md
---

# skill-foundry

Router skill: dispatch one build/certify request to exactly ONE specialist playbook. [DOC]

## When to use
Use when the user wants to create, design, audit, certify, benchmark, index, or
search an agentic asset (skill / agent / command / prompt / hook / MCP server /
workflow): verb = build-an-asset, noun = one of the topics → route here. Do NOT
use to *run* an existing asset, edit unrelated files, or answer domain questions. [DOC]

## Procedure
**In:** `topic` (one enum value) + `depth` (quick|deep) + intent. **Out:** the
chosen playbook's artifact (definition / audit / cert verdict / index), tagged
and gates-passed. [INFERENCE]
1. **Resolve `topic`** against the enum. Map intent → topic via `routes.json`
   `desc` fields (each lists its own trigger phrases). [DOC]
2. **Read EXACTLY ONE** playbook from `routes:`. Never load the whole cluster —
   one route per invocation keeps context lean. [DOC]
3. **Apply by depth:** `quick` → essentials path only; `deep` → exhaustive, with
   verification at each step. [DOC]
4. **Validate** against the gate below before reporting done. [DOC]

Spine: Discover → Analyze → Execute → Validate. Gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule. [DOC]

Routing aids live in `assets/` — `assets/quality-rubric.json` (routing scorecard) and `assets/checklist.md` (spine checklist). [DOC]

## Tie-breakers (ambiguous topic) [INFERENCE]
- create a skill → `meta-skill-creator`; design a skill (spec only) → `design-skill`.
- improve/production-ize end-to-end → `assembly-skill`; audit only → `x-ray-skill`; certify only → `certify-skill`.
- create a prompt file → `prompt-creator`; create/review/port a system prompt → `prompt-forge`.
- workflow YAML/steps/RACI → `workflow-creator`; slash-command phases → `workflow-forge`.
- Still ambiguous → ask one disambiguating question; do not guess.

## Validation gate (Done = all true)
- Topic matched a valid enum value; exactly one playbook was read. [DOC]
- The playbook's own acceptance criteria/rubric passed (incl. constitution v6.0.0). [DOC]
- Every non-obvious claim carries one Alfa-set tag (`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`,
  EN spelling); no foreign taxonomy mixed in. [DOC]
- Output is single-brand; no invented prices; no green-as-success. [DOC]

## Anti-patterns
- Reading multiple route files "to compare" — pick one, route, done. [DOC]
- Inventing a topic outside the enum, or silently defaulting when intent is unclear. [DOC]
- Skipping the playbook gate and self-declaring success. [ASSUMPTION]

## Self-correction triggers
- No enum fits → out of foundry scope; redirect, don't force a route. [INFERENCE]
- Gate fails → fix the artifact and re-run the gate; never ship a failing asset. [DOC]