# Deep variation — business-analysis (depth=deep)

Exhaustive treatment of one topic, verifying at every step. Use when the deliverable feeds
a real decision, a sign-off, or a downstream architecture/plan phase.

## Do
1. Resolve `topic`; confirm scope boundaries (start/end events, affected groups, unit under
   assessment) before producing anything.
2. Run the full playbook procedure, not a subset:
   - process-modeling → as-is **and** to-be BPMN, value-stream map with timeline ladder,
     capability map, complexity×frequency automation matrix, owner sign-off on as-is.
   - flow-mapping → DDD taxonomy, all 8–12 flows with happy + ≥1 alt/error path each, one
     Mermaid `sequenceDiagram` per flow, full integration matrix reconciled both directions.
   - requirements → INVEST stories with happy/negative/boundary AC, NFRs, full traceability
     matrix with zero orphans.
   - feasibility → all 7 dimensions scored with evidence, decision rule applied, top-5 risk
     register with owners + mitigations, confidence % + biggest unknown, independent lead review.
   - scenario → ≥3 distinct scenarios, weights locked + rationale, weighted totals,
     sensitivity / close-call analysis, residual-risk section.
   - change-readiness → every affected group scored on all 5 ADKAR dimensions, barrier per
     group, owned + time-boxed interventions, outcome metrics beyond adoption count.
3. Verify each step as the playbook's Validate phase requires; do not defer verification to
   the end.
4. Attach the evidence-tag summary (% by tag type) and run the full acceptance gate
   (`assets/checklist.md`).

## Guardrails
- Apply the decision rules literally (feasibility mean rule, ADKAR first-≤3, weight lock).
- Honor the Firebase/Google/Hostinger lens and phase separation throughout.
- Block on any gate failure with named fixes — do not ship a partial gate.
