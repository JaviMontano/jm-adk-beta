# Deep Variation — iikit (depth=deep)

Exhaustive routing with full gate verification. Use for high-stakes stages
(constitution, testify, implement) or when intent must be inferred.

1. **Resolve `topic` rigorously.** If intent is described, inspect artifacts on
   disk to find the earliest unmet stage; state the inference and its evidence.
2. **Predecessor audit.** Verify every upstream artifact the stage consumes
   exists and passed its own gate (e.g. testify requires plan.md + spec.md with
   Given/When/Then; missing scenarios → route to `clarify`).
3. **Read the one playbook** and walk every step, not just the essentials.
4. **Run all prescribed scripts** and parse their JSON; treat each field as
   present-or-false. Surface any failure verbatim.
5. **Verify each acceptance-criterion** in the stage's Validation Gate one by
   one; for testify confirm hash stored in BOTH context.json and git note → LOCKED.
6. **Self-check** against `prompts/meta.md` before declaring done.

Deep mode never trades a gate for speed. If a gate cannot be met, report the
specific failure and remediation rather than reporting done. Maintain one
evidence-tag family and zero placeholders throughout.
