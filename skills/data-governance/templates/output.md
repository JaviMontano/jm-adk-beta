# Data Governance Deliverable — {{topic}}

> Resolved topic: **{{topic}}** · Depth: **{{quick|deep}}** · Date: {{YYYY-MM-DD}}

## 1. Routing decision
- **Topic chosen**: {{topic}} — {{one-line reason via weakest-overlap rule}} [INFERENCIA]
- **Playbook loaded**: references/{{topic}}.md (exactly one) [DOC]
- **Tie-break** (if any): {{rejected topic}} dropped because {{reason}}. [INFERENCIA]

## 2. Discover — inputs & context
| Item | Value | Source | Tag |
|---|---|---|---|
| {{data source / dataset}} | {{owner / volume / cadence}} | {{DDL / catalog / profiling}} | [DOC] |
| Regulatory drivers | {{retention / residency / regime}} | {{policy ref}} | [SUPUESTO] |

Missing-input blockers: {{none | list with [SUPUESTO] + how to obtain}}.

## 3. Analyze — options & trade-offs
| Decision | Chosen | Rejected alternative | Trade-off / cost of wrong call | Tag |
|---|---|---|---|---|
| {{e.g. de-identification technique / write path / ETL vs ELT}} | {{choice}} | {{alt}} | {{cost}} | [INFERENCIA] |

## 4. Execute — the deliverable
{{Topic-specific body. Examples:
- privacy: field classification table, technique + parameters (k/l/t/ε), lawful basis + retention per field, consent model.
- audit-trail: record schema, integrity-chain design, retention + legal-hold.
- documentation: data dictionary rows, column-grain lineage, glossary mappings.
- pipeline: G0–G3 gate criteria + confidence threshold.
- strategy/governance: architecture blueprint, roles, quality rules (metric/threshold/action).
- storytelling: insight → narrative arc for the named audience.}}
Each claim evidence-tagged. [DOC]

## 5. Validate — gate checklist
- [ ] Exactly one playbook loaded; no siblings read. [DOC]
- [ ] Output answers the resolved topic, not the router. [INFERENCIA]
- [ ] Topic-specific quality criteria met ({{re-ID test / chain verifiable / drift=0 / confidence ≥ 0.95 / named owners}}). [DOC]
- [ ] Alfa evidence tags present; every [SUPUESTO] has a verification step. [CONFIG]
- [ ] No invented prices; criteria not vendors; no client PII; single brand. [CONFIG]

## 6. Decision log
| # | Decision | Rationale | Confidence | Tag |
|---|---|---|---|---|
| 1 | {{...}} | {{...}} | {{0.00–1.00}} | [INFERENCIA] |

## 7. Open assumptions & next steps
- {{[SUPUESTO] ...}} → verify by {{step}}.
- Next: {{handoff / follow-on skill}}.
