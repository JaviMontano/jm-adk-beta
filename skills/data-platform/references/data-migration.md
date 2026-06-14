<!-- distilled from alfa skills/data-migration -->
<!-- CSV/JSON import to Firestore. Batch writes (500/batch). Schema evolution. Rollback procedures. Data transformation scripts. [EXPLICIT] -->
# data-migration {Data} (v1.1)
> **"Data is the product. Model it for queries, secure it with rules, back it up daily."**
## Purpose
CSV/JSON import to Firestore. Batch writes (500/batch). Schema evolution. Rollback procedures. Data transformation scripts. [EXPLICIT]
**When to use:** Database design, data management, or analytics within the Firebase ecosystem.
**Anti-scope:** not for SQL/relational migrations, cross-cloud ETL, or streaming pipelines — those route elsewhere. [INFERENCIA]
## Core Principles
1. **Law of Queries:** Design schema for read patterns. Firestore charges per read/write/delete, so denormalize for the hot path. [EXPLICIT]
2. **Law of Rules:** Security rules are mandatory. No collection without rules. Default-deny, then open per-path. [EXPLICIT]
3. **Law of Backups:** Production data gets scheduled backups before any migration write. No exceptions. [EXPLICIT]
## Core Process
### Phase 1: Design data model from requirements (query-first).
### Phase 2: Implement with security rules and indexes.
### Phase 3: Test with emulator. Validate rules. Set up backups. Dry-run on a sample, then run.
### Batch-write contract [INFERENCIA]
- Hard cap 500 ops/`WriteBatch`; chunk the source and commit sequentially.
- A batch is atomic: one bad doc fails all 500 — validate/transform before adding to the batch, not after.
- Make writes idempotent: derive doc IDs from a stable source key so re-runs upsert instead of duplicating.
- Throttle commits to respect the 10k writes/sec/db soft ceiling; back off on `RESOURCE_EXHAUSTED`. [SUPUESTO] — confirm current quota in console before bulk runs.

## Validation Gate
- [ ] Schema designed for actual query patterns (every read path has a supporting structure)
- [ ] Security rules cover all collections; default-deny verified in emulator
- [ ] Indexes defined for every compound query (no runtime `FAILED_PRECONDITION`)
- [ ] Backup taken and restore tested before first production write
- [ ] Migration script is idempotent and dry-run clean on a sample
- [ ] No SQL-style normalized design in Firestore

## Acceptance criteria
- Row counts reconcile: source ≈ destination minus documented drops (drops logged with reason). [INFERENCIA]
- Spot-check N sample docs field-by-field against source post-import. [INFERENCIA]
- Rules deny unauthenticated and cross-tenant reads in emulator tests. [INFERENCIA]
- Rollback rehearsed: a known-good backup restores the prior state within target RTO. [SUPUESTO] — set RTO with the data owner.

## Failure modes
| Failure | Cause | Mitigation |
|---|---|---|
| Partial import | Crash mid-run, non-idempotent writes | Stable doc IDs + resumable checkpoint of last committed chunk [INFERENCIA] |
| Duplicate docs | Auto-IDs on re-run | Derive ID from source key; upsert [INFERENCIA] |
| Cost spike | Full-collection scans / per-doc reads in transform | Export once, transform offline, batch-write back [EXPLICIT] |
| Rules lock-out | Deploying default-deny before app paths exist | Stage rules; test in emulator before deploy [INFERENCIA] |
| Missing index | Compound query at runtime | Predeclare in `firestore.indexes.json` [CONFIG] |

## Rollback
1. Stop the migration job; freeze writes to affected collections. [INFERENCIA]
2. Restore from the pre-migration backup (point-in-time or export). [EXPLICIT]
3. Reconcile counts; re-run only failed chunks from the checkpoint. [INFERENCIA]

## Worked example
Source `users.csv` (1,250 rows) → `users/{uid}`:
- Stream CSV, transform each row, validate; on error collect to a dead-letter list, do not abort the run. [INFERENCIA]
- Accumulate 500 valid docs → commit batch → repeat (3 batches: 500/500/250).
- `uid` derived from source `email` hash, so re-running upserts. [INFERENCIA]
- After run: assert destination count == 1,250 − dead-letter count. [INFERENCIA]

## Usage
Example invocations:
- "/data-migration" — Run the full data migration workflow
- "data migration on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes Firestore as the target store; other stores are out of scope. [SUPUESTO] — confirm target before running.
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain-expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Source exceeds 500 rows | Chunk into ≤500-op batches; commit sequentially |
| Schema evolution mid-flight | Version the doc shape; migrate lazily on read or in a backfill pass [INFERENCIA] |
| Re-run after partial failure | Idempotent upsert from checkpoint; never blind re-insert [INFERENCIA] |
