# Deep variation — firebase

Use when `depth=deep`: apply the resolved playbook exhaustively with verification
at each phase.

## Do
- Run all three phases of the playbook (Discover/Design → Implement → Test/Validate).
- For `architecture`: produce the service matrix, Firestore hierarchy, Functions
  topology, Rules strategy, C4 context + container diagrams (Mermaid), and a
  per-feature cost estimate at the stated scale.
- For `firestore-security-rules`: cover get/list/create/update/delete per collection
  AND subcollection, immutable-field assertions, and emulator unit tests for allow
  AND deny on every path.
- For `cost-optimization`: walk Firestore → Functions → Storage/Billing phases with
  the cost-driver math worked out.
- Name every trade-off (write amplification, idle min-instances, cache staleness).
- Verify after each phase; do not advance on an unverified step.

## Required artifacts
- Populated `templates/output.md`.
- Validation Gate checklist fully ticked with evidence.
- Cost estimate as FTE-months / usage volume — never a price.

## Stop conditions
SQL-normalized schema, multi-cloud, Docker/K8s, or any price quote → halt and correct.
