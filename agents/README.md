# Agents

Alfa shipped 261 agents — 90%+ were 1:1 per-skill wrappers around 4 near-identical
role bodies. Beta replaces them with:

- **4 parametrized role templates** (`references/roles/{lead,support,guardian,specialist}.md`)
  instantiated at dispatch time with `skill=<id>` — the orchestrator fills `{{skill}}`.
- **A small set of genuinely distinct agents** in this directory, each with a
  compressed output contract (caveman pattern) and a model-tier hint.

To add an agent: justify why a parametrized role is insufficient.
