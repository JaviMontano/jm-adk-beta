# Quick Prompt — data-platform (depth=quick)

Fast dispatch. Resolve `topic`, load one playbook, apply essentials only.

1. Infer `topic` from intent (8-enum). Commit unless genuinely 50/50.
2. Read the one matching `routes:` playbook — never the cluster.
3. Apply the playbook's core procedure to the user's task; skip exhaustive
   verification, keep the non-negotiable invariants:
   - idempotent load (upsert on key or stage-then-swap), [EXPLICIT]
   - watermark only post-commit, [EXPLICIT]
   - ≤500 Firestore writes/batch, [CONFIG]
   - rollback path for any destructive op. [ASSUMPTION]
4. Output per `templates/output.md`, trimmed; tag claims with Alfa-core tags.

Use when the task is narrow and the topic is obvious. Escalate to `deep.md` if
the task touches multiple collections, breaking schema changes, or bulk
destructive writes.
