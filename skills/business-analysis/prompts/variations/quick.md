# Quick variation — business-analysis (depth=quick)

Fast path for a single, well-scoped business-analysis question. Essentials only.

## Use when
- The topic is obvious from one dominant signal (no tie to break).
- The user wants the core artifact, not the exhaustive treatment.

## Do
1. Name the resolved `topic` in one line and why.
2. Load that one playbook; run the spine at essentials depth.
3. Produce only the headline artifact for the topic:
   - process-modeling → the as-is BPMN + the single biggest waste + PCE.
   - flow-mapping → the 3–4 most critical flows + their integration rows (not the full 8–12).
   - requirements → the top stories with happy + one negative AC each.
   - feasibility → the 7-dimension scorecard + go/no-go + confidence, one-line evidence per dim.
   - scenario → the criteria/weights table + scored matrix + the single recommendation.
   - change-readiness → one ADKAR table for the most-affected group + its barrier + one intervention.
4. Tag every claim. If >30% `[ASSUMPTION]`, say so and stop for input rather than padding.

## Skip
- Exhaustive coverage, secondary flows, sensitivity narratives, full risk registers.
- Anything that needs data the user has not provided — request it instead.

State explicitly: "depth=quick — essentials only; re-run deep for full coverage."
