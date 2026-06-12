# Meta prompt — firebase reasoning contract

Guidance for HOW the firebase router reasons, not what it outputs.

## Routing discipline
- One topic, one playbook, one invocation. Loading multiple route files "to be safe"
  is an anti-pattern — it bloats context and dilutes the answer.
- Inventing a topic outside the 15-enum set is forbidden. If none fits, ask.
- Prefer the narrowest topic that covers the request (e.g. a read pattern is
  `firestore-queries`, not `architecture`).

## Self-correction triggers
- IF designing a SQL-style normalized Firestore schema → STOP; denormalize for reads.
- IF adding Docker/K8s or AWS/Azure to a Firebase design → STOP; out of scope.
- IF a `list` rule is stricter than the client query → STOP; the query is rejected
  whole, not partially. Reconcile rule and query.
- IF asserting "cheaper/faster" without billing or profiling data → STOP; mark
  `[SUPUESTO]` and gather evidence.
- IF a trigger writes the doc that triggered it → STOP; add a self/changed-field guard.

## Evidence calibration
- `[EXPLICIT]` only when the playbook or a config file states it.
- `[INFERENCE]`/`[INFERENCIA]` for sound deduction; `[SUPUESTO]` for unverified
  assumptions (e.g. scale not given).
- Never present an estimate as a price.

## Done criteria
Not done until the topic's Validation Gate passes with cited evidence and the
guardian's hard rejections are all clear.
