# Body of Knowledge — ux-research

Domain knowledge for routing and running user research and validation. This is
the stable reference the lead/specialist draw on; the four playbooks under
`references/` hold the step-level procedure. [DOC]

## 1. The four routes and the question each answers

| Route | Question class | Output | Don't use when |
|-------|----------------|--------|----------------|
| user-research | *Why / what do users need?* (generative) | Personas, empathy maps, journey maps, framed opportunities | You already know the *why* and only need to count it |
| survey-design | *How many / how often?* (attitudes at scale) | Validated instrument + segmented analysis | Reachable n < ~30/segment, or you need behavior not attitude |
| user-testing | *Can users complete the task?* (evaluative) | Severity-rated usability findings | You need at-scale behavior (use analytics/A-B) |
| prototyping | *Is the concept right before build?* | Lowest-fidelity artifact that falsifies the assumption | No testable question is defined |

Decisive rule: pick the **method by the question type**, not by familiarity.
*Why/how* is qualitative; *how many/how often* is quantitative; *can they do it*
is task-based. [INFERENCIA]

## 2. Core concepts

- **Saturation** — qualitative sample size is reached when new interviews stop
  surfacing new themes; typically 5–8 per segment. Diagnostic, not statistical. [DOC]
- **Say-vs-Do gap** — divergence between stated and observed behavior; the gap is
  itself a finding, not noise. Self-report overstates intent. [DOC]
- **Moment of truth** — a critical journey touchpoint that disproportionately
  determines satisfaction; where sentiment swings hardest. [DOC]
- **Fidelity ladder** — sketch → wireframe → clickable mockup → high-fi
  interactive; each rung tests one assumption and costs more to change. Raise
  fidelity only after the lower rung passes. [INFERENCIA]
- **Severity × frequency** — usability findings are prioritized on a 2-axis
  matrix (blocker / major / minor / cosmetic), not on moderator preference. [DOC]
- **Construct validity** — a survey item measures the one thing it claims to;
  double-barreled or leading items break it. [DOC]

## 3. Standards and metrics

| Metric | Question | Scale | Score | Reads |
|--------|----------|-------|-------|-------|
| NPS | likelihood to recommend | 0–10 | %promoters(9–10) − %detractors(0–6) | loyalty |
| CSAT | satisfaction | 1–5 | % rating 4–5 | transaction |
| CES | effort/ease | 1–7 agree | mean or % top-2 | friction |
| SUS | system usability | 10 items | 0–100 composite | post-test usability |
| SEQ | single-task ease | 1–7 | per-task mean | in-test friction |

Benchmarks are directional and industry-specific. Compare to your **own prior
period** before any external "good" number. NPS/CSAT/CES/SUS are **not**
interchangeable — choose by the decision. [SUPUESTO] Verify: pull last period's
own baseline first.

## 4. Decision rules

1. Research that informs **no decision** is waste — name the decision before the
   method (every route, step 1). [DOC]
2. Report **n, response rate, and margin of error** with every survey number; a
   bare mean on an ordinal scale is invalid — use top-box or median. [DOC]
3. **Segment before concluding** — a flat top-line often hides opposing segments. [INFERENCIA]
4. Recruit **representative users, not internal staff**; state who was excluded
   and the coverage-bias risk. [INFERENCIA]
5. Each persona attribute and each test finding **traces to a source** (interview
   ID, analytics metric, verbatim quote). [DOC]
6. When qualitative and quantitative disagree, **reconcile — don't average**; the
   disagreement is the insight. [INFERENCIA]
7. With no reachable users, build **provisional** outputs from proxies (support
   tickets, analytics, sales notes), tag `[SUPUESTO]`, and name the validation
   study. [SUPUESTO]

## 5. Evidence taxonomy (Alfa-core, one family)

`[CODE]` runnable/observed in artifacts · `[CONFIG]` from config/contract ·
`[DOC]` from the playbooks/standards above · `[INFERENCIA]` reasoned conclusion ·
`[SUPUESTO]` assumption needing a paired verification step · `[EXPLICIT]` stated
in the playbook. One tag per claim; never mix families; never assert green. [CONFIG]

## 6. Failure modes to police

Persona sprawl (>4) or the "elastic user"; research theater (running studies then
ignoring findings); leading/loaded wording; happy-path-only journeys; n=1 quirks
treated as patterns; sampling only reachable/power users; reporting a mean on an
ordinal scale. [INFERENCIA]
