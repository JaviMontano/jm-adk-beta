<!-- distilled from alfa skills/survey-design -->
<!-- > -->
# Survey Design
> "Method over hacks."

## TL;DR
Quantitative attitude/segmentation surveys at scale: question + scale design,
sampling, fielding, and analysis. Standard metrics — NPS, CSAT, CES — with
benchmarks. NOT for generative "why" (use user-research) or evaluating a flow
(use user-testing). [DOC]

## When NOT to survey
- n you can reach is < ~30 per segment → numbers won't be stable; interview instead. [INFERENCIA]
- You don't yet know what to ask → run qual first; surveys quantify known hypotheses. [DOC]
- You need behavior, not stated attitude → instrument analytics; self-report overstates intent. [DOC]

## Procedure
### 1. Define
- One decision the data must inform + the metric that moves it. No "nice to know" items. [DOC]
- Target population, segments, and the minimum n per segment you can actually field. [DOC]

### 2. Draft questions
- One construct per item; no double-barreled ("fast and easy?"). [DOC]
- Balanced scales, labeled endpoints; avoid leading stems and absolutes ("always"). [DOC]
- Order: easy/screener → core → sensitive/demographic last to cut dropoff. [INFERENCIA]
- Keep < ~12 items / < 5 min; add an open-ended "anything else?" to catch blind spots. [INFERENCIA]

### 3. Field
- Pilot with 5–10 respondents; fix confusing items before full launch. [DOC]
- Randomize answer order (not scales) to kill primacy bias; track source/channel. [INFERENCIA]
- Watch response rate + straight-lining; screen out speeders and flatliners. [INFERENCIA]

### 4. Analyze
- Report n, % responding, and margin of error — never a bare average. [DOC]
- Segment before concluding; a flat top-line often hides opposing segments. [INFERENCIA]
- Tie each finding to the decision from step 1 and a recommended next step. [DOC]

## Standard metrics
| Metric | Question | Scale | Score |
|---|---|---|---|
| NPS | "How likely to recommend?" | 0–10 | %promoters(9–10) − %detractors(0–6) |
| CSAT | "How satisfied?" | 1–5 | % rating 4–5 |
| CES | "How easy was it?" | 1–7 agree | mean, or % top-2 |

Benchmarks are directional and industry-specific; compare to your own trend, not
a universal "good" number. NPS/CSAT/CES are not interchangeable — pick by the
decision (loyalty vs. transaction vs. friction). [SUPUESTO] Verify: pull last
period's own score as the baseline before reading any external benchmark.

## Worked example
Goal: does new checkout reduce friction? → CES post-purchase, 1–7.
Field to 400 buyers (≈200/variant), pilot 8, randomize nothing (single item).
Result: control top-2-box 58%, new 71%, n=392, ±5pp → ship, monitor refunds. [INFERENCIA]

## Failure modes
- Leading/loaded wording inflates favorable scores → blind-review stems. [INFERENCIA]
- Sampling only happy/active users → coverage bias; include churned/lapsed. [DOC]
- Reporting a mean on an ordinal scale as if interval → use top-box or median. [INFERENCIA]
- Acting on n too small for the segment cut → state MoE, withhold the cut. [INFERENCIA]

## Quality criteria (acceptance)
- [ ] Every item: single construct, balanced scale, non-leading. [DOC]
- [ ] n, response rate, and margin of error reported with each number. [DOC]
- [ ] Findings segmented and tied to the decision + a next step. [DOC]
- [ ] Evidence tags applied; one family, consistent spelling. [DOC]

## Usage
- "/survey-design" — run the full survey design workflow.
- "survey design on this project" — apply to current context.

## Assumptions & limits
- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Provides design + analysis method, not a fielding platform/panel, and does not replace domain-expert judgment. [DOC]

## Edge cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request the decision + target segment before drafting. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to user-research / user-testing or escalate. |
| Sample too small for a cut | Report top-line + MoE; withhold the cut. |
