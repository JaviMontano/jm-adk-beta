# data-governance — README

Router skill for **governing data** (not building pipelines). It resolves one
`topic` and loads exactly one playbook — never the whole cluster. [DOC]

## What it does
Given a governance request, it disambiguates intent into one of seven topics and
applies the matching playbook to the user's case along the spine
**Discover → Analyze → Execute → Validate**. [DOC]

## When to use
The request is about controlling data — catalog/metadata/lineage, PII/PHI
handling, masking/anonymization, retention, consent, tamper-evident audit logs,
a governance operating model, quality gates *inside* a pipeline, a data
strategy/roadmap, or turning metrics into a narrative. [INFERENCE]
Do **not** use it to author ETL code or tune physical schemas. [INFERENCE]

## How it routes
| Signal | Topic | Playbook |
|---|---|---|
| Privacy / PII / masking / consent | `data-privacy-patterns` | references/data-privacy-patterns.md |
| Tamper-evident logs, who-did-what | `audit-trail-design` | references/audit-trail-design.md |
| Catalog / metadata / lineage docs | `data-documentation` | references/data-documentation.md |
| Org model, ownership, policies | `data-governance` | references/data-governance.md |
| DQ checks/SLAs inside pipelines | `pipeline-governance` | references/pipeline-governance.md |
| Vision, roadmap, capability model | `data-strategy` | references/data-strategy.md |
| Metrics → narrative for humans | `data-storytelling` | references/data-storytelling.md |

Tie-break: prefer the more specific topic (privacy/audit over governance). [INFERENCE]

## How it executes
1. Infer `topic` (ask only on a genuine tie) and `depth` (`quick` default, `deep`
   for exhaustive application). [DOC]
2. Read **one** playbook from `routes:` in `SKILL.md`. [DOC]
3. Apply it to the user's case; emit evidence-tagged output, no router boilerplate. [INFERENCE]
4. Pass the validation gate before declaring done. [CONFIG]

## References
- `references/data-privacy-patterns.md` — PII discovery, anonymization (k/l/t), consent lifecycle (GDPR).
- `references/audit-trail-design.md` — append-only, hash-chained, tamper-evident logs.
- `references/data-documentation.md` — data dictionaries, schema docs, column-grain lineage.
- `references/data-governance.md` — governance operating model, ownership, policy.
- `references/pipeline-governance.md` — G0–G3 phase gates and quality checkpoints.
- `references/data-strategy.md` — architecture blueprint, governance framework, roadmap.
- `references/data-storytelling.md` — insight extraction, narrative arc for metrics.

## Supporting bundle
- `agents/` — lead, specialist, support, guardian role contracts for this router.
- `knowledge/` — body of knowledge + concept graph.
- `prompts/`, `templates/`, `examples/`, `evals/` — operating prompts, output scaffold, worked example, eval cases.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).

## Evidence taxonomy
Alfa set: `[DOC]` / `[CONFIG]` / `[CÓDIGO]` / `[INFERENCIA]` (`[INFERENCE]`) /
`[SUPUESTO]` (`[ASSUMPTION]`). Every `[ASSUMPTION]` carries a verification step. [CONFIG]
