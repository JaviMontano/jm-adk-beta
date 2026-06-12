# Example Input — data-platform

## User request
"We have a nightly job that pulls orders from our Postgres `orders` table into
the Firestore `orders` collection. It re-reads the whole table every night and
sometimes creates duplicate Firestore docs when it crashes halfway. There are
about 3.2M orders and it's getting slow. Each order has an `updated_at` column
and a unique `order_id`. Make the sync incremental and crash-safe, and load it
into Firestore without blowing the batch limits."

## Parsed parameters
- `topic`: **etl-patterns** — the ask is transform-and-load in motion
  (batch→incremental, idempotent, crash-safe), not write-time schema rules or a
  one-off migration. [INFERENCE]
- `depth`: **deep** — 3.2M rows, duplicate-on-crash defect, and Firestore batch
  limits make this multi-step and destructive-adjacent. [INFERENCE]
- Source change marker: `updated_at` (monotonic) + unique `order_id`. [EXPLICIT]
- Target: Firestore `orders` collection, upsert semantics. [EXPLICIT]

## What good output must do
- Replace full-table reload with an incremental high-watermark read on
  `updated_at`.
- Make the Firestore load idempotent (upsert on `order_id`) so a crash cannot
  duplicate docs.
- Advance the watermark only after the batch commits.
- Chunk writes to ≤500 per Firestore batch with a `batch_id`.
- Provide a rollback path and a source↔target reconciliation.
