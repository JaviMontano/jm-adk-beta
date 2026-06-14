<!-- distilled from alfa skills/benchmarking-analysis -->
<!-- > -->
# Benchmarking Analysis
> "Method over hacks."
## TL;DR
Compare a subject (team/product/process/metric) against industry benchmarks and internal baselines, quantify the gap, attribute root cause, and emit prioritized closure actions. Output is decision-grade, not a number dump. [EXPLICIT]

## Procedure
### Step 1: Discover
- Define the subject, the metric set, and the decision the benchmark must inform [EXPLICIT]
- Source benchmarks (industry reports, peer data, internal history); record provenance + date per figure [EXPLICIT]
- Normalize: same unit, period, segment, and definition before any comparison [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV [EXPLICIT]
- Gap = subject − reference; report as absolute AND % of reference; flag sign convention (higher-is-better vs lower-is-better) [EXPLICIT]
- Prefer median/quartile to mean for skewed metrics; compare like-for-like cohorts only [EXPLICIT]
### Step 3: Execute
- Implement with evidence tags; cite the benchmark source on every comparison [EXPLICIT]
- Rank gaps by (impact × closability), not by raw size [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met; re-check that no comparison crosses incompatible definitions or stale data [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Every benchmark figure carries source + as-of date [EXPLICIT]
- [ ] Subject and reference share unit, period, segment, definition [EXPLICIT]
- [ ] Gaps prioritized by impact × closability, not magnitude [EXPLICIT]

## Worked Example
Subject onboarding time-to-value = 14 days; industry median = 7 days (SaaS report, Q1-2026); lower-is-better.
Gap = +7 days = +100% vs median → top-quartile target ≤ 4 days. Root cause: manual data import (9 of 14 days). Action: automate import (impact: high, closability: high) ranked above UI polish (low × high). [EXPLICIT]

## Decisions & Trade-offs
- Median over mean: robust to outliers; trade-off — hides distribution tails, so report quartiles alongside [EXPLICIT]
- External benchmark over internal-only: situates performance vs market; trade-off — definition drift across sources, so normalize first [EXPLICIT]

## Usage

Example invocations:

- "/benchmarking-analysis" — Run the full benchmarking analysis workflow
- "benchmarking analysis on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not forecasting, not root-cause-only analysis, not vendor selection — those route to their own skills [EXPLICIT]
- Benchmark validity decays; figures older than the metric's cycle are flagged, not used silently [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No credible external benchmark exists | Fall back to internal baseline + trend; label "internal-only" [EXPLICIT] |
| Mismatched definitions across sources | Normalize or exclude; never silently average [EXPLICIT] |
| Stale benchmark (older than metric cycle) | Flag staleness; use only with explicit caveat [EXPLICIT] |
| Sample too small for percentile | Report range, not quartiles; mark low-confidence [EXPLICIT] |
