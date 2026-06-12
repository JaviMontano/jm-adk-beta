# Data-Platform Deliverable — {{system_or_task_name}}

> Routed topic: `{{topic}}` · Depth: `{{quick|deep}}` · Stack: Firestore + Cloud Functions
> Every claim carries one Alfa-core tag: `[EXPLICIT]` `[INFERENCE]` `[SUPUESTO]` `[CONFIG]`.

## 1. Routing decision
- **Topic chosen:** `{{topic}}` — playbook `references/{{topic}}.md`.
- **Why:** {{intent → topic rationale}}.
- **Deferred topic (if any):** {{topic or "none"}} — {{why deferred}}.

## 2. Discover
| Item | Value |
|------|-------|
| Source(s) | {{collections / files / events}} |
| Change marker | {{high-watermark column / CDC log / none}} |
| Target write semantics | {{append / upsert / overwrite}} |
| Grain (1 row = ?) | {{grain}} |
| Business/natural key | {{key}} |

## 3. Analyze
- **Pattern selected:** {{batch / incremental / streaming / micro-batch / rule / migration}}.
- **Rejected alternative + trade-off:** {{alt}} — {{trade-off}}.
- **Failure modes covered:** late/out-of-order · soft-deletes · duplicate keys ·
  schema drift · clock skew → {{handling per mode}}.

## 4. Execute
- **Idempotency mechanism:** {{upsert/MERGE on key | stage-then-swap}}. [EXPLICIT]
- **Watermark handling:** advanced only post-commit. [EXPLICIT]
- **Batch plan:** chunks of ≤500 Firestore writes, each tagged `batch_id`. [CONFIG]
- **Script(s):** {{command(s) — import / batch-write / reconcile / diff}}.

## 5. Rollback (state BEFORE running any destructive op)
- **Trigger:** {{when to roll back}}.
- **Procedure:** {{replay by batch_id / drop staging / restore snapshot}}. [ASSUMPTION]

## 6. Validate
- [ ] Source vs target row counts match within {{tolerance}}.
- [ ] Key + measure checksum matches.
- [ ] No duplicate keys, no NULL keys at grain.
- [ ] Kill-mid-batch resumes zero-gap, zero-duplication.
- [ ] Schema change additive or planned-with-sign-off.

## 7. Evidence ledger
| Claim | Tag | Verification step |
|-------|-----|-------------------|
| {{claim}} | {{[EXPLICIT]/[INFERENCE]/[SUPUESTO]/[CONFIG]}} | {{how verified}} |

## 8. Gate result
`dod = {{pass|fail}}` — {{one-line summary}}.
