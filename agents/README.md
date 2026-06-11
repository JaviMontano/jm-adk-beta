# Agents

Alfa shipped 261 agents — 90%+ were 1:1 per-skill wrappers around 4 near-identical role bodies. [DOC] Beta replaces them with:

- **4 parametrized role templates** (`references/roles/{lead,support,guardian,specialist}.md`), instantiated at dispatch with `skill=<id>`; the orchestrator fills `{{skill}}`. [DOC]
- **A small set of genuinely distinct agents** here — each with a compressed output contract (caveman pattern) and a `model-tier` hint (`haiku`|`sonnet`|`opus`). [DOC]

**When a standalone agent is justified** (else use a parametrized role): multi-skill orchestration in one turn; a non-skill tool contract; a bespoke output schema a role template can't express; or a guardrail that must run regardless of skill. [INFERENCE]

**Add checklist** [INFERENCE]
1. State which of the 4 roles you tried and why each is insufficient.
2. Declare `model-tier` (default `sonnet`; reserve `opus` for cross-domain synthesis, `haiku` for narrow extraction).
3. Define the output contract: required fields, evidence tags, refusal/escalation path.

**Anti-scope:** no per-skill wrappers (regression to Alfa); no agent that only renames a role's `{{skill}}`; no price logic. [DOC]
**Done when:** routable by the orchestrator, dispatch resolves cleanly, output contract validates on one real input. [INFERENCE]
