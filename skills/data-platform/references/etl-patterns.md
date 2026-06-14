<!-- distilled from alfa skills/etl-patterns -->
<!-- > -->
# Etl Patterns
> "Method over hacks."
## TL;DR
Design extract-transform-load pipelines: pick batch vs stream vs micro-batch, make loads idempotent, recover from partial failure without data loss or duplication. [EXPLICIT]

## When to use which pattern
| Pattern | Use when | Avoid when | [EXPLICIT] |
|---------|----------|------------|------------|
| Full batch reload | Source small (<10M rows) or no reliable change marker | Source large with high churn (rewrites everything nightly) |
| Incremental (CDC / high-watermark) | Source has monotonic `updated_at`/LSN/sequence | No trustworthy change column (silent missed rows) |
| Streaming (event-by-event) | Sub-minute latency required, unbounded source | Latency tolerant — streaming adds ops cost for no gain |
| Micro-batch | Near-real-time "enough" (1–5 min), simpler than streaming | Strict exactly-once at sub-second latency |

## Procedure
### Step 1: Discover
- Identify source change marker (high-watermark column, CDC log, or none) and target write semantics (append / upsert / overwrite). [EXPLICIT]
- Establish the grain (one row = ?) and the natural/business key for dedup. [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; choose pattern from table above. [EXPLICIT]
- Decision: prefer **incremental upsert keyed on business key** over truncate-reload once volume or churn makes reload slow — trade-off: needs a reliable watermark and dedup, but avoids full-rebuild cost and downstream gaps. [EXPLICIT]
### Step 3: Execute
- Make loads **idempotent**: upsert/MERGE on key, or load to staging then atomic swap — re-running a failed batch must not duplicate or corrupt. [EXPLICIT]
- Persist the watermark only **after** the batch commits, not before — crash between read and commit must re-read, not skip. [EXPLICIT]
- Wrap each load in a transaction or stage-then-publish; tag rows with `batch_id` for traceability and surgical rollback. [EXPLICIT]
### Step 4: Validate
- Reconcile source vs target row counts and a checksum on the key + a numeric measure; alert on drift beyond tolerance. [EXPLICIT]
- Assert no duplicate keys at target grain and no NULLs in the key. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Loads idempotent (safe to re-run)
- [ ] Watermark advanced only post-commit
- [ ] Source-to-target reconciliation passes

## Usage

Example invocations:

- "/etl-patterns" — Run the full etl patterns workflow
- "etl patterns on this project" — Apply to current context

## Acceptance Criteria
- A re-run of any single batch produces byte-identical target state (idempotent). [EXPLICIT]
- A kill -9 mid-batch leaves the target in its last committed state and the next run resumes with zero gap and zero duplication. [EXPLICIT]
- Reconciliation (counts + key checksum) matches source within stated tolerance. [EXPLICIT]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Anti-scope: not a tool selection guide (Airflow vs Dagster vs dbt), not a data-modeling/warehouse-schema reference (see `schema-evolution.md`), not data-quality rule authoring (see `data-quality.md`). [EXPLICIT]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Late-arriving / out-of-order data | Widen watermark window with overlap + upsert; never advance watermark past unprocessed late rows |
| Source soft-deletes (row vanishes) | High-watermark misses deletes — use CDC tombstones or periodic full-key diff |
| Duplicate keys in source | Deduplicate to grain pre-load (latest-wins by updated_at); fail loudly if ambiguous |
| Schema drift (new/renamed/typed column) | Fail fast on incompatible change; additive columns pass through; log and quarantine |
| Partial batch failure | Roll back to staging or replay by batch_id; never leave half-loaded committed state |
| Timezone / clock skew on watermark | Store watermark in UTC; add safety lag so source-clock skew can't skip rows |
