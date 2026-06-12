# Data-Platform Done Checklist

Run before declaring any data-platform task done. Mirrors the SKILL.md gate and
the guardian agent. Used by `agents/guardian.md` and `templates/output.md`.

## Routing
- [ ] `topic` resolved to a single value in the 8-enum.
- [ ] Exactly one playbook loaded (never the cluster), and only after `topic` was fixed.
- [ ] If two topics were plausible, the dominant ran and the deferred is named.

## Application
- [ ] Output addresses the user's concrete task, not the topic in the abstract.
- [ ] Pattern chosen with the rejected alternative + trade-off stated.
- [ ] Loads are idempotent (upsert on business key or stage-then-swap).
- [ ] Watermark advanced only post-commit.
- [ ] Bulk writes chunked to ≤500 per Firestore batch with a `batch_id`.
- [ ] Schema change is additive or planned-with-sign-off.

## Safety & verification
- [ ] Every destructive op has a rollback path stated before execution.
- [ ] Source vs target reconciliation (counts + key checksum) passes within tolerance.
- [ ] No duplicate keys, no NULL keys at the target grain.
- [ ] Kill-mid-batch simulated → zero-gap, zero-duplication resume.

## Governance
- [ ] Every claim carries one Alfa-core family tag (`[EXPLICIT]`/`[INFERENCE]`/`[SUPUESTO]`/`[CONFIG]`).
- [ ] No invented prices, single-brand, no client PII.
- [ ] No green-as-success: every checked item was actually exercised.
