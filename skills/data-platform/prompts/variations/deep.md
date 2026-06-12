# Deep Prompt — data-platform (depth=deep)

Exhaustive application with per-step verification. Use for multi-collection
pipelines, breaking schema changes, or bulk destructive writes.

1. **Discover** — inventory source(s), change marker (high-watermark / CDC log /
   none), target write semantics (append / upsert / overwrite), grain, and the
   business key for dedup. [EXPLICIT]
2. **Analyze** — choose the pattern from the playbook's decision table; state the
   rejected alternative and the trade-off. Map every failure mode (late/out-of-
   order, soft-deletes, duplicate keys, schema drift, clock skew). [EXPLICIT]
3. **Execute** — make every load idempotent; stage-then-publish or transaction-
   wrap; tag rows with `batch_id`; chunk bulk writes to ≤500/batch; persist the
   watermark only after commit; write the rollback procedure *before* running. [EXPLICIT]
4. **Validate** — reconcile source vs target counts + key checksum within
   tolerance; assert no duplicate keys, no NULL keys at grain; simulate a
   kill-mid-batch and confirm zero-gap, zero-duplication resume. [EXPLICIT]

Then run `prompts/meta.md` as a full self-audit. Every gate item must be
actually exercised — never green-as-success. Tag all claims with one Alfa-core
family tag.
