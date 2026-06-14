<!-- distilled from alfa skills/ab-testing -->
<!-- > -->
# Ab Testing

> "Method over hacks. Evidence over assumption."

## TL;DR

Designs or audits an A/B test so a team can decide whether to run, fix, stop,
or interpret an experiment without confusing speed with evidence. [EXPLICIT]
Makes the hypothesis, metric contract, assumptions, sample-size needs, duration,
instrumentation, risks, and decision rule explicit before traffic is spent. [EXPLICIT]
Default posture: refuse to claim significance, lift, or causality until the
required data and method exist; return a readiness brief instead. [EXPLICIT]

## Scope & Anti-Scope

- IN: experiment design, pre-launch readiness review, validity-threat audit,
  decision-rule authoring, post-test interpretation given valid data. [EXPLICIT]
- OUT: choosing what to build, multi-armed bandit optimization, ML model
  evaluation, pricing experiments with legal exposure — route these out. [EXPLICIT]
- OUT: computing significance from raw event logs (no compute here); produce the
  method + inputs, hand execution to an analytics tool or notebook. [SUPUESTO]

## Procedure

### Step 1: Discover
- Identify experiment goal, decision owner, user segment, traffic source,
  current baseline, candidate variant, and business constraint. [EXPLICIT]
- Capture the primary metric, guardrail metrics, minimum detectable effect
  (MDE), desired power, significance threshold, and acceptable runtime. [EXPLICIT]
- Inspect existing analytics, event names, funnel definitions, docs, or code.
  If missing, mark the gap instead of inventing metrics. [EXPLICIT]
- Confirm randomization unit (user vs session vs account) and that it matches
  the metric's denominator; a mismatch silently biases results. [INFERENCIA]

### Step 2: Analyze
- Convert the idea into a falsifiable hypothesis:
  "If we change X for audience Y, metric Z will move by N because R." [EXPLICIT]
- Check whether an A/B test is even appropriate, or whether discovery, analytics
  cleanup, usability testing, or a flagged rollout is safer first. A/B testing
  needs enough traffic to reach power within the runtime; below that, prefer
  qualitative methods. [EXPLICIT]
- Estimate sample-size and duration from baseline, traffic, variance, MDE,
  power, and significance. If any required input is absent, return a
  requirements gap plus a formula-ready checklist — never a fabricated number.
  [EXPLICIT]
- Pick the test method up front: two-proportion z-test for binary conversion,
  t-test / Mann-Whitney for continuous metrics, CUPED or sequential testing if
  variance reduction or valid early stopping is required. State it before
  launch so the analysis cannot be method-shopped after seeing data. [INFERENCIA]
- Identify validity threats: novelty effects, peeking, seasonality, sample ratio
  mismatch (SRM), overlapping experiments, instrumentation drift, segment bias,
  and metric dilution from late-binding exposure. [EXPLICIT]

### Step 3: Execute
- Produce an experiment brief: hypothesis, variants, metric contract,
  sample-size assumptions, duration recommendation, launch checklist,
  monitoring plan, and decision rule. [EXPLICIT]
- If reviewing an existing test, classify it as ready, blocked, risky, or
  invalid, and name the blocking evidence for the verdict. [EXPLICIT]
- Keep implementation recommendations scoped to the experiment; route broader
  funnel or analytics work to related skills. [EXPLICIT]

### Step 4: Validate
- Verify the primary metric has one owner and one definition. [EXPLICIT]
- Verify every recommendation ties to evidence, an explicit assumption, or an
  open data requirement. [EXPLICIT]
- Verify the decision rule covers win, loss, inconclusive, harmed guardrail, and
  instrumentation-failure outcomes. [EXPLICIT]
- Do not claim statistical significance, lift, ROI, or causality unless the
  required data and method are available. [EXPLICIT]
- Verify SRM check is planned: if observed traffic split deviates from intended
  (chi-square p < 0.01), results are untrustworthy regardless of the p-value on
  the primary metric. [INFERENCIA]

## Worked Example: Sample Size

Inputs (illustrative, replace with real data): baseline conversion 5%, MDE = +0.5pp
absolute (5.0% → 5.5%), power 80%, significance α = 0.05 two-sided. [SUPUESTO]
Two-proportion z-test requires ~31k users per variant (≈62k total). At 9k
exposed users/day split 50/50, that is ~7 days minimum — round up to a full
weekly cycle (14 days) to absorb weekday/weekend seasonality. [INFERENCIA]
Read-through: a smaller MDE or lower baseline inflates the required N steeply
(N scales ≈ 1/MDE²); if traffic cannot reach N within the acceptable runtime,
the honest output is "underpowered — do not run as a fixed-horizon A/B." [INFERENCIA]

## Worked Example: Metric Contract

| Field | Value |
|---|---|
| Primary | checkout_completion_rate = completed_checkouts / checkout_starts |
| Owner | one named decision owner [SUPUESTO] |
| Guardrails | refund_rate, p95_page_load_ms, support_ticket_rate |
| Exposure event | `experiment_exposed` fired at variant assignment, deduped per user |
| Randomization unit | user_id (matches denominator) |
| Analysis method | two-proportion z-test, α=0.05, fixed 14-day horizon |

A guardrail breach blocks a ship even on a winning primary metric. [EXPLICIT]

## Decision Rule (template)

| Outcome | Condition | Action |
|---|---|---|
| Win | primary up, significant, no guardrail breach | Ship to 100% |
| Loss | primary down or flat, significant | Do not ship; archive learning |
| Inconclusive | CI spans MDE at planned horizon | Do not extend silently; pre-commit to ship-no / re-test |
| Guardrail harmed | any guardrail crosses threshold | Block ship regardless of primary |
| Instrumentation failure | SRM, missing exposures, event drift | Invalidate; fix and rerun |

Set every branch before launch; deciding after seeing data is peeking. [EXPLICIT]

## Quality Criteria

- [ ] Hypothesis is falsifiable and names change, audience, metric, expected
      movement, and rationale.
- [ ] Primary metric, guardrails, event names, and data source are defined or
      explicitly marked missing.
- [ ] Sample-size, MDE, power, significance, and duration are stated; absent
      inputs are listed as blocking requirements, not guessed.
- [ ] Analysis method named before launch and matches metric type.
- [ ] Launch, monitoring, stopping, and decision rules are actionable.
- [ ] Risks include peeking, seasonality, overlapping experiments, SRM, and
      instrumentation drift when relevant.
- [ ] Claims use evidence tags or are marked as assumptions/open questions.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Testing without a decision rule | Produces data but no decision | Define win, loss, inconclusive, and guardrail-failure actions before launch |
| Optimizing many primary metrics | Inflates false positives, weakens accountability | One primary metric; separate guardrails |
| Peeking and stopping early | Makes confidence claims unreliable | Fix the horizon or use a sequential method designed for early looks |
| Missing instrumentation checks | Invalidates results after traffic is spent | Verify events, exposure logging, and SRM before analysis |
| Significance = business value | A detectable lift may be too small to matter | Include MDE and a practical-impact threshold |
| Extending a flat test to "find" a win | Converts noise into a false positive | Pre-commit the horizon; treat inconclusive as a valid outcome |
| Ignoring SRM | A skewed split silently biases every metric | Run a chi-square SRM check before trusting any result |

## Related Skills

- `analytics-events`
- `funnel-analytics`
- `conversion-optimization`
- `data-validation`
- `experimentation-strategy`

## Usage

Example invocations:

- "/ab-testing" — Run the full ab testing workflow
- "ab testing on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- If baseline conversion, traffic, variance, or MDE are missing, produces a
  readiness brief but not a reliable sample-size claim. [EXPLICIT]
- Fixed-horizon framing assumes a frequentist test; Bayesian or sequential
  designs change the stopping and decision logic and must be declared. [SUPUESTO]
- No statistical computation is performed here; numeric outputs are templates
  to execute in a tool, not validated results. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Traffic too low for power in runtime | Declare underpowered; recommend qualitative method or longer horizon |
| Overlapping experiments on same surface | Flag interaction risk; recommend mutual exclusion or interaction analysis |
| SRM detected mid-flight | Mark invalid; diagnose assignment/logging before reading metrics |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
