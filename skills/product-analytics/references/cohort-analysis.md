<!-- distilled from alfa skills/cohort-analysis -->
# Cohort Analysis
> "Method over hacks."

## TL;DR
Group users by a shared acquisition event, then track a behavior (retention, revenue, lifecycle stage) over aligned time since that event. Answers "do users from cohort X stay/convert better than cohort Y?" — not aggregate trends, which hide mix shifts. [DOC]

## Scope
- **In:** cohort definition, retention curves, lifecycle-stage segmentation, cohort-vs-cohort comparison. [DOC]
- **Out (anti-scope):** causal attribution, forecasting, A/B significance testing, individual-user prediction — these need their own methods; do not infer causation from a curve gap. [SUPUESTO] (verify by running a controlled experiment)

## Procedure
### Step 1: Discover
- Fix the **cohort key** (signup week/month, first-purchase, channel) and the **measured event**. One key per analysis. [DOC]
- Confirm the data spans enough periods that the newest cohort has at least one observable follow-up window. [INFERENCIA]

### Step 2: Analyze
- Build the cohort × period grid; compute retention as `active_in_period / cohort_size`. Evaluate options per Constitution XIII/XIV. [DOC]
- Read the curve shape: steep early drop = onboarding/activation gap; flat tail = a sticky core; rising = expansion or survivorship. [INFERENCIA]

### Step 3: Execute
- Produce the retention table/heatmap plus a one-line read per cohort, each carrying an evidence tag. [DOC]

### Step 4: Validate
- Check denominators (cohort size at t0, not current size), period alignment, and that "active" is defined identically across cohorts. [DOC]

## Worked Example
Jan cohort = 1,000 signups; 420 active in month 1, 310 in month 3 → M1 retention 42%, M3 31%. Feb cohort holds 52% at M1 after an onboarding change → +10pp, attributable to the cohort boundary, not seasonality. [INFERENCIA] (confirm with an experiment before claiming causation)

## Failure Modes
- **Mixing cohort sizes into one average** — Simpson's paradox; a growing user base can mask declining per-cohort retention. [INFERENCIA]
- **Survivorship in late periods** — newest cohorts lack mature data; never compare a 1-month-old cohort's M6 cell (it is empty, not zero). [DOC]
- **Shifting "active" definition** between cohorts invalidates the comparison. [DOC]

## Quality Criteria
- [ ] Evidence tags applied (one per non-obvious claim, single family)
- [ ] Constitution-compliant
- [ ] Actionable output (each cohort has a read + next step)
- [ ] Denominators fixed at cohort t0; period windows aligned

## Usage
Example invocations:
- "/cohort-analysis" — Run the full cohort analysis workflow
- "cohort analysis on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to event-level data with a timestamp and stable user/cohort key. [SUPUESTO] (verify schema before running)
- Requires English-language output unless otherwise specified. [DOC]
- Does not replace domain expert judgment for final decisions. [DOC]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Newest cohort lacks follow-up periods | Mark cells empty, exclude from late-period comparison |
| Cohort size below significance floor | Report with a low-confidence caveat, do not over-read |
