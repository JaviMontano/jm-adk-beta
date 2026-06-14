# Body of Knowledge: skill-foundry

Domain knowledge for routing one build/certify request to exactly one of 16
agentic-asset playbooks. [DOC]

## 1. Core concept: the foundry is a router, not a builder

skill-foundry resolves a request to ONE specialist playbook and hands off. It owns
the *dispatch contract*, not the asset itself. The single load rule — read exactly
one `references/<topic>.md` per invocation — is the load-bearing constraint; it is
what keeps the foundry's context lean enough to route reliably. [DOC]

## 2. The 16 topics and four families

| Topic | Family | One-line job |
|-------|--------|--------------|
| `agent-creator` | create | Custom agent: triggers, bounded prompt, least-privilege tools, model, checks |
| `prompt-creator` | create | Prompt files from the canonical prompt-type matrix |
| `prompt-forge` | create | System prompts: Playbook format, portability, rubric, adversarial cases |
| `hook-creator` | create | Harness lifecycle hooks |
| `mcp-creator` | create | MCP server config: transport, scope, auth, secret, preflight, rollback |
| `workflow-creator` | create | 17-field workflow definition with DoD, RACI, KPIs |
| `workflow-forge` | create | Slash-command phase map with handoffs + checkpoints |
| `meta-skill-creator` | create | New 10x skill via skill-forge Trinity (Alfa-Atoms-Beta) |
| `design-skill` | design | Detailed skill spec only — frontmatter, procedure, criteria, edges |
| `x-ray-skill` | quality | Diagnostic scorecard + gap analysis ("what is the state?") |
| `certify-skill` | quality | Certification verdict ("can I ship this?") |
| `benchmark-skill` | quality | A/B diff of two skill states or against a standard |
| `assembly-skill` | quality | Full pipeline: x-ray → surgeon → certify (+ trigger) |
| `meta-skill-indexer` | index | Regenerate `skills_index.json` for BM25 search |
| `skill-search` | index | Find existing skills |
| `auto-prompt-matching` | index | Match a prompt to the right asset |

## 3. Decision rules (tie-breakers)

- **create vs design a skill**: build it → `meta-skill-creator`; spec only →
  `design-skill`. [DOC]
- **production-ize vs audit vs certify**: end-to-end → `assembly-skill`; audit only
  → `x-ray-skill`; verdict only → `certify-skill`. [DOC]
- **prompt file vs system prompt**: a prompt file → `prompt-creator`; create/review/
  port a *system* prompt → `prompt-forge`. [DOC]
- **workflow YAML vs slash command**: 17-field YAML/RACI → `workflow-creator`;
  phased slash command → `workflow-forge`. [DOC]
- Still tied → ask ONE disambiguating question; never guess. [DOC]

## 4. x-ray vs certify (the most common confusion)

| Aspect | x-ray-skill | certify-skill |
|--------|-------------|---------------|
| Output | Scorecard + gaps | Certification report + verdict |
| Tone | Descriptive | Prescriptive |
| Use | Before improvement | After improvement / standalone gate |

Certify is read-only — it never edits the skill under test; edits route to surgeon. [DOC]

## 5. Standards and gates

- **Constitution v6.0.0** enforcement applies to every routed asset. [DOC]
- **Spine**: Discover → Analyze → Execute → Validate. [DOC]
- **Script-first rule**: when a playbook ships a deterministic validator, run it
  before writing prose; manual reasoning is the tagged fallback. [DOC]
- **Certification levels** (certify route): MOAT / CERTIFIED / CONDITIONAL /
  BLOCKED, computed from explicit local JSON policy assets, offline only. [DOC]

## 6. Evidence taxonomy (Alfa set)

`[DOC]` (from SKILL.md / routes.json / playbook), `[INFERENCE]` (derived),
`[ASSUMPTION]` (unverified). Reference playbooks additionally emit `[EXPLICIT]` and
`[INFERRED]`; carry these through unchanged. Never mix a foreign taxonomy. [DOC]

## 7. Governance invariants

Single-brand output; no invented prices (FTE-months + disclaimers only); never
green-as-success; no client PII; respect each skill's `allowed-tools`; read before
write. [DOC]
