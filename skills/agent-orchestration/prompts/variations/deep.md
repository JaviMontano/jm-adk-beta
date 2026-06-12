# Deep variation — agent-orchestration

`depth=deep`. Apply the resolved playbook exhaustively and verify at each step.
[CONFIG]

1. Resolve `topic` with the full disambiguation table; record why the chosen
   topic beats the runner-up. [DOC]
2. Load that one playbook (still only one). [CONFIG]
3. Run the spine with verification gates between steps:
   - **Discover** — enumerate every required input; mark gaps `[OPEN]`; do not
     auto-fill. [DOC]
   - **Analyze** — apply the full policy (all confidence bands / decision-table
     rows / model tiers / checkpoint+resume contract). Record each option and the
     trade-off rejected. [DOC]
   - **Execute** — produce the full deliverable from `templates/output.md`; run
     the bundled deterministic script and attach its evidence (script-first). [CONFIG]
   - **Validate** — run the entire Guardian checklist; for resumable/recovery
     topics confirm state/ordering invariants. [DOC]
4. Enumerate edge cases and failure modes from the playbook and state the guard
   for each. [DOC]
5. Gate: constitution v6.0.0 + evidence tags (single family, EN/ES consistent) +
   script-first. A green positive run alone is insufficient — negative/edge
   fixtures must also hold where the topic defines them. [DOC]

Example: "Choose retention period for prod PII across EU + US, billing, and
audit" → `triad-composition`, deep: four domains + compliance scope → Committee
(max 5 agents) with a one-line justification of why a triad cannot own it, full
tie-breaker trace, and a `[PARTIAL]` plan if a role is unavailable. [INFERENCE]
