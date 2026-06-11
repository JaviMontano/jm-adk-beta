---
name: skill-foundry
description: "Create/certify skills, agents, commands, prompts, hooks, MCP servers, workflows. Topics: agent-creator, assembly-skill, auto-prompt-matching, benchmark-skill, certify-skill, design-skill, hook-creator, mcp-creator, meta-skill-creator, meta-skill-indexer, prompt-creator, prompt-forge, skill-search, workflow-creator, workflow-forge, x-ray-skill."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
