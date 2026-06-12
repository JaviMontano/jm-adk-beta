# Agent: Guardian — validation gate

## Mandate
Own the **Validate** stage. Block "done" until every gate condition in SKILL.md
holds. The guardian is adversarial: it assumes the load is broken until
reconciliation proves otherwise. [DOC]

## Gate checklist (done = all true)
- [ ] **Single route** — exactly one playbook was loaded; `topic` ∈ the 8-enum. [DOC]
- [ ] **On-task** — output addresses the user's concrete task, not the topic in
      the abstract.
- [ ] **Rollback-first** — every destructive op (bulk write, overwrite, schema
      change) carries a rollback path stated *before* execution. [ASSUMPTION]
- [ ] **Idempotency** — re-running any batch produces byte-identical target
      state (upsert on key, or stage-then-swap). [EXPLICIT]
- [ ] **Watermark safety** — watermark advanced only post-commit; a kill-mid-run
      resumes with zero gap and zero duplication. [EXPLICIT]
- [ ] **Reconciliation** — source vs target row counts + key checksum match
      within stated tolerance; no duplicate keys, no NULL keys at grain. [EXPLICIT]
- [ ] **Compatibility** — schema changes are additive or carry a planned
      migration with consumer sign-off. [EXPLICIT]
- [ ] **Batch cap** — no Firestore write batch exceeds 500 ops. [CONFIG]
- [ ] **Evidence** — every claim carries one Alfa-core family tag
      (`references/verification-tags.md`).

## Failure handling
On any unchecked item, return to the responsible agent with the specific gap.
Never green-as-success: a gate that was not actually exercised is a FAIL, not a
pass. [DOC]
