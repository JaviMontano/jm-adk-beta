# Meta prompt: generate a skill-foundry routing prompt

Use this to produce a tailored routing prompt for a specific foundry request,
before dispatching to a playbook.

## Interview (ask only what is missing)
1. **Asset kind** — skill, agent, command, prompt, hook, MCP server, or workflow?
2. **Action** — create, design, audit, certify, benchmark, index, or search?
3. **Depth** — quick or deep?
4. **Target** — for quality routes, the path to the existing skill/asset.

## Map answers → topic
- create + agent → `agent-creator`; create + system prompt → `prompt-forge`;
  create + prompt file → `prompt-creator`; create + hook → `hook-creator`;
  create + MCP → `mcp-creator`; create + workflow YAML → `workflow-creator`;
  create + slash command → `workflow-forge`; create + skill → `meta-skill-creator`.
- design + skill (spec only) → `design-skill`.
- audit → `x-ray-skill`; certify → `certify-skill`; compare → `benchmark-skill`;
  full pipeline → `assembly-skill`.
- index → `meta-skill-indexer`; find skill → `skill-search`; match prompt →
  `auto-prompt-matching`.

## Emit
A single-topic routing prompt that: states the resolved topic and the one
reference path, sets the depth path, and lists the gate to run. Tag the mapping
rationale `[INFERENCE]` and any rule cited from SKILL.md/routes.json `[DOC]`.

## Guardrails
Never emit a prompt that loads more than one reference. Never invent a topic
outside the enum. If the interview cannot resolve a single topic, emit a
disambiguation question instead of a route.
