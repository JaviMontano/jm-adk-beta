---
name: data-platform
version: 1.0.0
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

Router for the data-engineering lifecycle. Resolve `topic`, then Read EXACTLY
ONE playbook from `routes:`. Never load the cluster. [DOC]

**Use for** pipelines, ETL, quality/validation gates, migration, export, schema
evolution, data-flow wiring on Firestore/Cloud Functions. **Not for** general
backend logic, auth, UI state, infra provisioning. [INFERENCE]
**In:** `topic` (required, 8-enum), `depth`, the user's concrete data task.
**Out:** the routed playbook applied to that task — dispatch only, never a
generic answer from this file. [DOC]

## Routing
1. Infer `topic`; ask only if two topics are equally plausible. [INFERENCE]
2. Disambiguate by intent: transform in motion → `etl-patterns`; write-time
   rules → `data-validation`; profiling/health → `data-quality`; bulk load →
   `data-migration`; recurring read-out → `data-export`; field shapes over time
   → `schema-evolution`; trigger/event wiring → `data-flow-architecture`;
   end-to-end pipeline design → `data-engineering`. [INFERENCE]
3. `deep` → apply exhaustively, verify each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate. Gates: constitution v6.0.0
enforcement, evidence tags, script-first. [CONFIG]

## Validation gate (done = all true)
- Exactly one playbook loaded; topic ∈ enum. [DOC]
- Output addresses the user's task, not the topic in the abstract.
- Destructive ops carry a rollback path before execution. [ASSUMPTION]
- Claims tagged with one Alfa-core family tag (references/verification-tags.md).
- Gate scored via `assets/quality-rubric.json` + `assets/checklist.md` (≥0.85). [DOC]

## Anti-patterns
- Loading >1 route, or reading a playbook before fixing `topic`. [INFERENCE]
- Guessing `topic` when ambiguous instead of asking.
- Improvising bulk writes here (Firestore caps 500/batch) — defer to migration. [CONFIG]

## Self-correction
Two topics → run the dominant, name the deferred. Route yields nothing useful →
re-route once via step 2, don't force-fit. [INFERENCE]