# Example Output — data-platform

> Routed topic: `etl-patterns` · Depth: `deep` · Stack: Firestore + Cloud Functions

## 1. Routing decision
- **Topic chosen:** `etl-patterns` — playbook `references/etl-patterns.md`.
- **Why:** the request is a transform-and-load in motion — convert full reload
  to incremental, make the load crash-safe and idempotent. [INFERENCE]
- **Deferred topic:** `data-migration` — not a one-off bulk import; this is the
  recurring nightly sync, so etl-patterns dominates. [INFERENCE]

## 2. Discover
| Item | Value |
|------|-------|
| Source | Postgres `orders` (~3.2M rows) |
| Change marker | `updated_at` (monotonic), unique `order_id` |
| Target write semantics | upsert into Firestore `orders` |
| Grain | one Firestore doc per `order_id` |
| Business key | `order_id` |

## 3. Analyze
- **Pattern selected:** incremental high-watermark on `updated_at` + idempotent
  upsert keyed on `order_id`. [EXPLICIT]
- **Rejected alternative + trade-off:** full-batch reload — simple but rewrites
  3.2M docs nightly and is the root cause of the slowness; incremental needs a
  reliable watermark + dedup but avoids the full rebuild. [EXPLICIT]
- **Failure modes covered:**
  - Crash mid-load → idempotent upsert means re-run cannot duplicate. [EXPLICIT]
  - Late/out-of-order rows → read `updated_at > last_watermark - 5min` overlap,
    upsert absorbs the overlap. [EXPLICIT]
  - Clock skew → watermark stored in UTC with a safety lag. [EXPLICIT]
  - Soft-deletes in Postgres → high-watermark misses them; weekly full-key diff
    reconciles deletions. [INFERENCE]

## 4. Execute
- **Idempotency mechanism:** `set(doc(order_id), data, {merge:true})` — upsert on
  `order_id`, so re-running a failed batch is byte-identical. [EXPLICIT]
- **Read:** `SELECT * FROM orders WHERE updated_at > $watermark ORDER BY updated_at`.
- **Watermark handling:** persist `max(updated_at)` of the batch to a
  `_sync_state/orders` doc **only after** all chunks commit. [EXPLICIT]
- **Batch plan:** split rows into chunks of 500; one Firestore `WriteBatch` per
  chunk, each carrying `batch_id = <run_ts>-<chunk_n>`. [CONFIG]
- **Script outline:**
  ```
  read rows since watermark → chunk(500) → for each chunk: batch.set(merge) → commit
  → after all chunks commit: write _sync_state/orders.watermark
  ```

## 5. Rollback (stated before running)
- **Trigger:** reconciliation drift > 0.1% or duplicate-key assertion fails.
- **Procedure:** `batch_id` is stamped on every written doc; delete/replay docs
  for the failing `batch_id`, leave the prior watermark untouched so the next run
  re-reads the window. [ASSUMPTION]

## 6. Validate
- [x] Count check: Postgres rows with `updated_at` in window == Firestore docs
  upserted in this run. 
- [x] Checksum on (`order_id` + `total_amount`) matches within tolerance 0.1%.
- [x] No duplicate `order_id` docs; no doc with empty `order_id`.
- [x] Simulated `kill -9` after chunk 3/12 → next run resumes from the unmoved
  watermark, re-upserts chunks 1–12, zero duplicates. [EXPLICIT]

## 7. Evidence ledger
| Claim | Tag | Verification |
|-------|-----|--------------|
| Upsert makes re-run idempotent | [EXPLICIT] | kill-mid-batch test (sec 6) |
| Watermark advanced post-commit | [EXPLICIT] | code path: write after commit loop |
| ≤500 writes/batch | [CONFIG] | chunk size assertion |
| Weekly diff catches soft-deletes | [INFERENCE] | scheduled diff job design |

## 8. Gate result
`dod = pass` — incremental + idempotent upsert on `order_id`, post-commit
watermark, ≤500/batch, rollback by `batch_id`, reconciliation green.
