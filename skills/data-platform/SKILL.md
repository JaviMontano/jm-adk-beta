---
name: data-platform
description: "Data engineering lifecycle: pipelines, quality, validation, migration, export, flow architecture. Topics: data-engineering, data-export, data-flow-architecture, data-migration, data-quality, data-validation, etl-patterns, schema-evolution."
params:
  topic:
    enum: [data-engineering, data-export, data-flow-architecture, data-migration, data-quality, data-validation, etl-patterns, schema-evolution]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  data-engineering: references/data-engineering.md
  data-export: references/data-export.md
  data-flow-architecture: references/data-flow-architecture.md
  data-migration: references/data-migration.md
  data-quality: references/data-quality.md
  data-validation: references/data-validation.md
  etl-patterns: references/etl-patterns.md
  schema-evolution: references/schema-evolution.md
---

# data-platform

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
