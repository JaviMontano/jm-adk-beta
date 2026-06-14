<!-- distilled from alfa skills/scenario-analysis -->
<!-- Evaluate 3+ implementation scenarios. Weighted criteria matrix. Risk/reward. Firebase/Google stack constrained. [EXPLICIT] -->
# scenario-analysis {Analysis} (v1.1)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Evaluate 3+ implementation scenarios against weighted criteria, surface risk/reward, recommend one — all through Firebase/Google/Hostinger feasibility. [EXPLICIT]
**When to use:** Analysis mode (MAO DNA), before architecture or development. [EXPLICIT]
**Anti-scope (do NOT):** pick tools/write code (that is plan/dev phase, Art. 1.5); evaluate <3 scenarios (no real comparison); invent criteria weights without stating rationale. [EXPLICIT]
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No deliverable ships without all required sections. [EXPLICIT]
3. **Law of Firebase Lens:** Every scenario scored for Firebase/Google/Hostinger feasibility; an off-stack scenario must justify the exception or be marked infeasible. [EXPLICIT]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems). [EXPLICIT]
2. Parse for requirements, constraints, context. [EXPLICIT]
3. **Define criteria + weights BEFORE generating scenarios** — weights set after seeing options bias the result. Weights sum to 1.0; each weight carries a one-line rationale. [INFERENCE]
### Phase 2: Analyze
1. Generate ≥3 materially distinct scenarios (not trivial variants of one). Include a "do-nothing / baseline" when status quo is viable. [INFERENCE]
2. Score each scenario per criterion on a fixed scale (1–5; define what 1 and 5 mean per criterion to keep scoring reproducible). [INFERENCE]
3. Tag every score and claim with an evidence tag; a [ASSUMPTION] score must name the assumption inline. [EXPLICIT]
4. Weighted total = Σ(weight × score). Rank. Run sensitivity: if the top two are within ~10%, flag as "close call" and state the swing criterion. [INFERENCE]
### Phase 3: Document
1. Produce the deliverable in markdown: criteria table, scenario matrix, ranked result, recommendation + justified trade-off, residual risks. [EXPLICIT]
2. Include evidence tag summary (% by tag type). [EXPLICIT]
3. If >30% [ASSUMPTION], add prominent WARNING banner. [EXPLICIT]
### Worked example (illustrative scoring, scale 1–5)
Criteria → weights: Feasibility-on-stack 0.35 (hard constraint), Time-to-value 0.25, Cost/FTE-months 0.20, Risk-inverse 0.20. [ASSUMPTION: weights illustrative]

| Scenario | Feas .35 | TTV .25 | Cost .20 | Risk⁻¹ .20 | Weighted |
|----------|:--:|:--:|:--:|:--:|:--:|
| A: Firebase-native | 5 | 4 | 3 | 4 | **4.15** |
| B: Hybrid + Hostinger | 3 | 3 | 4 | 3 | 3.20 |
| C: Off-stack custom | 2 | 2 | 2 | 2 | 2.00 |

Recommend **A**: highest weighted score AND clears the Firebase-lens hard constraint. Trade-off accepted: A's cost score (3) is below B's (4), justified because Feasibility carries the largest weight and B fails the stack constraint at scale. [INFERENCE]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Criteria + weights | Text | No | Defaults applied + flagged [ASSUMPTION] if absent |

| Output | Type | Description |
|--------|------|-------------|
| Analysis deliverable | Markdown | Criteria table, scored matrix, ranked recommendation, evidence-tagged |
## Validation Gate (acceptance criteria)
- [ ] ≥3 materially distinct scenarios evaluated
- [ ] Criteria weights stated, sum to 1.0, each with rationale
- [ ] Every score/finding has an evidence tag
- [ ] Firebase/Google/Hostinger feasibility scored for each scenario
- [ ] Single recommendation with a justified trade-off (not just the top number)
- [ ] Sensitivity / close-call check performed
- [ ] Deliverable follows R-008 output standards
- [ ] No implementation details (phase separation, Art. 1.5)
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).
> IF <3 scenarios OR weights unstated THEN block — gate fails.
> IF top two scenarios within ~10% THEN label "close call" and name the swing criterion; do not present as decisive.

## Failure Modes
| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Weight gaming | Weights chosen after scoring to favor a pick | Lock weights in Phase 1; record rationale |
| False distinctness | 3 "scenarios" are one option reskinned | Require a differing axis (stack, sequencing, or build-vs-buy) per scenario |
| Hidden assumptions | Scores look confident, no basis | Force tag on every score; assumption named inline |
| Stack blind spot | Off-stack option wins on paper | Firebase-lens is a hard gate, not just a criterion |

## Usage
Example invocations:
- "/scenario-analysis" — Run the full scenario analysis workflow
- "scenario analysis on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Quantitative scores are decision aids, not guarantees; weights encode judgment, not fact [INFERENCE]
- No prices — express cost as FTE-months only [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Only one viable scenario | State why others were eliminated; document, do not fabricate filler options |
| All scenarios fail Firebase lens | Mark infeasible-on-stack; escalate the constraint rather than forcing a pick |
| Criteria genuinely incomparable | Use a tie-break criterion or present trade-off explicitly, no forced single winner |
