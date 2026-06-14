# Body of Knowledge — data-platform

Domain knowledge for the data-engineering lifecycle on a Firestore / Cloud
Functions stack. Scoped to what this router and its eight playbooks actually
decide. Evidence convention: Alfa-core family — `[EXPLICIT]` (stipulated, ≈
`[DOC]`), `[INFERENCE]`, `[SUPUESTO]`, `[CONFIG]`.

## 1. The eight topics and their boundary

| Topic | Owns | Hand off when |
|-------|------|---------------|
| data-engineering | end-to-end pipeline: ingestion, orchestration, storage zones, lineage, observability | dbt modeling → analytics-engineering; dashboards → bi-architecture [EXPLICIT] |
| etl-patterns | transform-in-motion: batch/stream/micro-batch, idempotency, watermarks | tool selection (Airflow vs Dagster), warehouse schema [EXPLICIT] |
| data-quality | profiling, validation rules, data contracts, anomaly thresholds, SLA monitoring | write-time type schemas → data-validation [EXPLICIT] |
| data-validation | Zod/Yup client, Cloud Functions server, Firestore rules, end-to-end types | statistical profiling → data-quality [EXPLICIT] |
| data-migration | CSV/JSON import, batch writes, rollback, transformation scripts | recurring read-out → data-export [EXPLICIT] |
| data-export | scheduled extracts, formats, recurring read-out | one-time bulk load → data-migration [INFERENCE] |
| schema-evolution | field shapes over time, backward/forward compatibility | live transform → etl-patterns [EXPLICIT] |
| data-flow-architecture | Firestore triggers → Cloud Functions event chains, real-time sync | app logic, auth → out of skill [EXPLICIT] |

## 2. Reliability invariants (cross-cutting)

1. **Idempotency by design.** Every pipeline stage is safely replayable: upsert /
   MERGE on a business key, or load to staging then atomic swap. A re-run must
   not duplicate or corrupt. This is the foundational reliability property. [EXPLICIT]
2. **Watermark only post-commit.** Persist the high-watermark after the batch
   commits, never before — a crash between read and commit must re-read, not
   skip. [EXPLICIT]
3. **Exactly-once delivery.** Idempotent producers (`enable.idempotence=true`) +
   transactional/read-committed consumers; idempotent sinks via natural-key
   upsert or partition-overwrite. [EXPLICIT]
4. **Schema evolution, not revolution.** Backward/forward compatibility is
   mandatory; additive columns pass through; breaking changes are planned with
   consumer sign-off, never surprises. [EXPLICIT]
5. **Data contracts.** Producer publishes schema + SLA + ownership; consumer
   registers the dependency and validates. Without contracts, quality is nobody's
   responsibility. [EXPLICIT]

## 3. Standards & hard limits

- **Firestore batch cap: 500 writes per batch.** Bulk loads must chunk; improvising
  bulk writes outside data-migration is an anti-pattern. [CONFIG]
- **Formats:** AVRO for schema-evolution flexibility on the streaming hop, Parquet
  at rest, Protobuf for performance-critical paths, JSON only for prototyping. [EXPLICIT]
- **Schema registry compatibility modes:** backward (new reads old) is the safe
  default; CI blocks breaking changes before deployment. [EXPLICIT]
- **Constitution v6.0.0 gates:** evidence tags on every claim, script-first
  execution, rollback path before destructive ops. [CONFIG]

## 4. Decision rules

- **Reload vs incremental:** prefer incremental upsert keyed on the business key
  once volume or churn makes truncate-reload slow; the trade-off is needing a
  reliable watermark + dedup. [EXPLICIT]
- **Streaming vs micro-batch:** use streaming only when sub-minute latency is
  required; micro-batch (1–5 min) is simpler and cheaper when "near-real-time
  enough." [EXPLICIT]
- **Prevention over detection:** for quality, contracts at ingestion and
  quarantine patterns beat end-of-pipeline inspection. [EXPLICIT]
- **Severity + owner + review-date** on every validation rule, or the rule rots. [EXPLICIT]

## 5. Failure modes to guard

- Late / out-of-order data → widen watermark window with overlap + upsert; never
  advance past unprocessed late rows. [EXPLICIT]
- Source soft-deletes (row vanishes) → high-watermark misses them; use CDC
  tombstones or periodic full-key diff. [EXPLICIT]
- Duplicate keys in source → dedup to grain pre-load (latest-wins by
  `updated_at`); fail loudly if ambiguous. [EXPLICIT]
- Partial batch failure → roll back to staging or replay by `batch_id`; never
  leave a half-loaded committed state. [EXPLICIT]
- Clock skew on watermark → store UTC, add a safety lag so source-clock skew
  cannot skip rows. [EXPLICIT]

## 6. Validation: what "done" requires

Reconcile source vs target row counts and a checksum on (key + a numeric
measure); assert no duplicate keys and no NULLs in the key at the target grain;
alert on drift beyond tolerance. A kill-mid-batch must leave the last committed
state and resume with zero gap, zero duplication. [EXPLICIT]
