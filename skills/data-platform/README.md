# data-platform

Router skill for the **data-engineering lifecycle** on a Firestore / Cloud
Functions stack. It resolves a single `topic` from the user's request, loads
**exactly one** playbook from `routes:`, and applies it to the concrete data
task — never a generic answer from the router itself. [DOC]

## What it does

Dispatches a data task to one of eight specialist playbooks, then runs the
shared spine **Discover → Analyze → Execute → Validate** with constitution
v6.0.0 gates (evidence tags, script-first, rollback-before-destructive). [CONFIG]

## When to use

Use for: pipelines/ETL, write-time validation, profiling and health, bulk
migration, recurring export, schema change over time, and trigger/event wiring
on Firestore + Cloud Functions.

Not for: general backend logic, auth, UI state, or infra provisioning — those
route to other skills. [INFERENCE]

## How it routes

| Intent | Topic | Playbook |
|--------|-------|----------|
| Transform data in motion | `etl-patterns` | references/etl-patterns.md |
| Write-time / schema rules | `data-validation` | references/data-validation.md |
| Profiling / health / contracts | `data-quality` | references/data-quality.md |
| Bulk load into Firestore | `data-migration` | references/data-migration.md |
| Recurring read-out | `data-export` | references/data-export.md |
| Field shapes over time | `schema-evolution` | references/schema-evolution.md |
| Trigger / event chains | `data-flow-architecture` | references/data-flow-architecture.md |
| End-to-end pipeline design | `data-engineering` | references/data-engineering.md |

`depth=quick` runs essentials; `depth=deep` applies the playbook exhaustively
and verifies each step. [DOC]

## How it executes

1. Infer `topic` (ask only when two topics are equally plausible).
2. Read the one matching playbook; never load the cluster.
3. Apply Discover → Analyze → Execute → Validate to the user's task.
4. Pass the validation gate before declaring done.

## References

- `references/data-engineering.md` — pipeline architecture, ingestion, storage, lineage.
- `references/etl-patterns.md` — batch/stream/micro-batch, idempotent loads, watermarks.
- `references/data-quality.md` — profiling, validation rules, data contracts, SLAs.
- `references/data-validation.md` — Zod/Yup, Cloud Functions, Firestore rules, end-to-end types.
- `references/data-migration.md` — CSV/JSON import, 500/batch writes, rollback.
- `references/data-export.md` — scheduled extracts and read-out formats.
- `references/data-flow-architecture.md` — Firestore triggers → Cloud Functions chains.
- `references/schema-evolution.md` — backward/forward compatibility, field migration.

## Companion bundle

Role contracts in `agents/`, domain knowledge in `knowledge/`, prompts in
`prompts/`, the deliverable scaffold in `templates/output.md`, worked example in
`examples/`, and the reusable rubric/checklist in `assets/` (see
`assets/README.md`).
