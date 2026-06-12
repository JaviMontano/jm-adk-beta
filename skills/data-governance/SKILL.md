---
name: data-governance
version: 1.0.0
description: "Router for data governance work: privacy patterns, data strategy, catalog/documentation, audit-trail design, pipeline governance, data storytelling. Resolves a topic and loads exactly one playbook. Topics: audit-trail-design, data-documentation, data-governance, data-privacy-patterns, data-storytelling, data-strategy, pipeline-governance."
params:
  topic:
    enum: [audit-trail-design, data-documentation, data-governance, data-privacy-patterns, data-storytelling, data-strategy, pipeline-governance]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  audit-trail-design: references/audit-trail-design.md
  data-documentation: references/data-documentation.md
  data-governance: references/data-governance.md
  data-privacy-patterns: references/data-privacy-patterns.md
  data-storytelling: references/data-storytelling.md
  data-strategy: references/data-strategy.md
  pipeline-governance: references/pipeline-governance.md
---

# data-governance

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. Never load the cluster. [DOC]

## When to use
Use when the request is about governing data — not building pipelines. Signals: data catalog, metadata, lineage, PII/PHI handling, masking/anonymization, retention, consent, audit logs, governance operating model, or turning metrics into a narrative. [INFERENCE]

## Inputs → Outputs
- **In:** `topic` (one enum value), `depth`. Infer `topic` from the request; ask only on a genuine tie. [DOC]
- **Out:** the single resolved playbook applied to the user's case — no router boilerplate echoed back. [INFERENCE]

## Topic disambiguation (pick the weakest-overlap match)
- Privacy/PII/masking/consent → `data-privacy-patterns`
- Tamper-evident logs, who-did-what → `audit-trail-design`
- Catalog/metadata/lineage docs → `data-documentation`
- Org model, ownership, policies → `data-governance`
- DQ checks/SLAs inside pipelines → `pipeline-governance`
- Vision, roadmap, capability model → `data-strategy`
- Metrics → narrative for humans → `data-storytelling`
If two fit, prefer the more specific (privacy/audit over governance). [INFERENCE]

## Spine
Discover → Analyze → Execute → Validate. `deep` → apply the playbook exhaustively, verifying at each step; `quick` → essentials only. [DOC]

## Validation gate (done means)
- Exactly one playbook loaded; no sibling routes read. [DOC]
- Output answers the resolved `topic`, not the router. [INFERENCE]
- Evidence tags present (Alfa set: `[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`); every `[ASSUMPTION]` has a verification step. [CONFIG]
- Quality gates honored: constitution v6.0.0 enforcement, script-first rule. [CONFIG]

## Assets
Routing checklist and grading rubric live in `assets/` (see `assets/manifest.json`). [CONFIG]

## Anti-patterns
- Reading multiple playbooks "to be safe" — defeats the router. [INFERENCE]
- Guessing `topic` silently when the request is truly ambiguous — ask one question. [ASSUMPTION]
- Restating playbook content here; this file only routes. [DOC]
