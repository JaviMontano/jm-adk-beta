<!-- distilled from alfa skills/vendor-evaluation -->
<!-- > -->
# Vendor Evaluation
> "Method over hacks."
## TL;DR
Score vendors on weighted criteria, total their TCO over the contract horizon, grade lock-in, and require a costed exit plan before recommending. Output a defensible recommendation, not a preference. [DOC]

## Procedure
### Step 1: Discover
- Capture must-haves vs nice-to-haves, the decision horizon, and the switching trigger that would force re-evaluation. [DOC]
- Name the incumbent/build-in-house baseline; "do nothing" is always a candidate. [INFERENCE]
### Step 2: Analyze — scorecard
- Score each candidate 1–5 per criterion, multiply by weight, sum. Weights total 100%. [DOC]
- Default weights (tune to context): Fit-to-requirement 30, TCO 25, Lock-in/exit 15, Security & compliance 15, Vendor viability 10, Support & SLA 5. [SUPUESTO]
- A score of 1 on any must-have criterion is disqualifying regardless of total. [INFERENCE]
### Step 3: Analyze — TCO & lock-in
- TCO = licence/subscription + implementation + integration + migration-in + training + run/ops + exit cost, over the full horizon (default 3 yr). [DOC]
- Lock-in grade: data egress cost, proprietary formats, API portability, contractual notice period, re-platform effort. [DOC]
### Step 4: Execute & Validate
- Tag every figure with its source; mark estimates `[SUPUESTO]` and pair each with a verification step. [DOC]
- Verify totals reconcile, weights sum to 100%, and the exit plan is costed before marking done. [DOC]

## Scoring rubric (anchors)
| Score | Meaning |
|---|---|
| 5 | Meets requirement natively, evidence in vendor docs/demo |
| 3 | Meets with configuration or minor workaround |
| 1 | Gap requiring custom build or unmet — disqualifying if must-have |

## Quality Criteria
- [ ] Weights sum to 100%; every candidate scored on every criterion
- [ ] TCO covers the full horizon incl. exit cost, not just year-1 licence
- [ ] Lock-in graded and a costed exit plan exists
- [ ] Every number carries an Alfa tag; estimates have a verification step
- [ ] Recommendation states the runner-up and why it lost

## Worked example (abridged)
Two SaaS candidates, 3-yr horizon. A scores 4.1, B scores 3.6; B is 18% cheaper on TCO but graded high lock-in (proprietary export, 90-day notice). Recommend A: the TCO gap is recovered within one switching event. [INFERENCE] Numbers illustrative. [SUPUESTO]

## Usage
Example invocations:
- "/vendor-evaluation" — Run the full vendor evaluation workflow
- "vendor evaluation on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and at least two real candidates. [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Does not negotiate contracts, set prices, or replace legal/security sign-off. [DOC]
- Anti-scope: not a procurement RFP, not a security audit — feeds them, does not replace them. [INFERENCE]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Single candidate only | State no comparison is possible; score vs the build/do-nothing baseline |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Prices unknown | Tag `[SUPUESTO]`, request quotes; never invent figures |
| Scores cluster within noise (<0.3) | Declare a tie; decide on lock-in/exit, not total |
| Out-of-scope request | Redirect to appropriate skill or escalate |
