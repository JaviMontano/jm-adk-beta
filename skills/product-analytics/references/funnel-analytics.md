<!-- distilled from alfa skills/funnel-analytics -->
<!-- > -->
# Funnel Analytics

> "A funnel is a measurement contract before it is a chart."

## TL;DR

Use this skill to turn product, commerce, onboarding, or acquisition journeys into a deterministic funnel analysis contract: stages, events, denominators, identity/session rules, data quality checks, drop-off interpretation, and testable optimization hypotheses. Do not invent event names, traffic volumes, conversion rates, causal explanations, or experiment results without provided evidence. Mark gaps as `not verified`. [EXPLICIT]

## When to use vs. not

- Use when a journey can be expressed as ordered, observable steps with a shared unit and a measurable end state. [EXPLICIT]
- Do **not** use for unordered/parallel behaviors (use cohort or event analysis), for single-event volume questions (use metrics-instrumentation), or for branching multi-path journeys where "the funnel" hides reversals — model each path separately. [EXPLICIT]
- Funnels answer *where* drop-off happens, not *why*. Causal "why" requires experiment, session replay, or research. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the business goal: acquisition, signup, activation, checkout, retention, or another user journey.
- Capture the funnel unit of analysis: user, account, session, order, lead, or device. One funnel = one unit; never mix units across steps. [EXPLICIT]
- Inventory available evidence: analytics events, data warehouse tables, BI dashboards, product specs, tracking plans, experiment logs, and source code.
- Map each funnel step to a precise event or state transition, including entry criteria, exit criteria, timestamp, owner, and source.
- Choose funnel **type** and record it: *strict-ordered* (steps must occur in sequence) vs *any-order* (steps occur within window, order ignored). Choice changes denominators and is not interchangeable. [EXPLICIT]
- Set the **conversion window** (max elapsed time from step 1 to final step) explicitly; without it, late conversions and re-entries are counted ambiguously. [EXPLICIT]
- Record attribution, identity stitching, timezone, bot/internal-traffic filters, privacy constraints, and known tracking gaps.
- Mark missing instrumentation, formulas, samples, and segments as `not verified` instead of estimating them.

### Step 2: Analyze
- Define formulas before interpreting results: denominator, numerator, conversion rate, drop-off rate, confidence window, cohort window, and exclusion rules.
- Decide and state **denominator policy**: *step-to-step* (each rate over the prior step) vs *overall* (each rate over the entry cohort). Mixing them silently produces contradictory totals. [EXPLICIT]
- Compare counts across steps only when the unit, time window, and deduplication rules match.
- Separate evidence-backed facts from hypotheses. Avoid causal language when only observational funnel data is available.
- Inspect segment cuts such as channel, plan, device, geography, lifecycle stage, experiment bucket, and customer tier when sample size supports it.
- Watch for **Simpson's paradox**: a blended rate can move opposite to every segment when segment mix shifts. Decompose before concluding. [EXPLICIT]
- Look for instrumentation risks: duplicate events, missing events, out-of-order timestamps, late-arriving data, identity resets, funnel leakage, and step skipping.
- Prioritize opportunities by impact, confidence, effort, reversibility, and measurement readiness.

### Step 3: Execute
- Produce a funnel definition table with step, event/source, unit, denominator, numerator, exclusions, owner, and evidence status.
- Produce a drop-off table only from verified counts or explicitly label sample/proxy data.
- Add data-quality notes for every weak or missing measurement dependency.
- Convert findings into optimization hypotheses with required instrumentation, target metric, guardrail metrics, and validation method.
- Recommend experiments, instrumentation fixes, or research follow-ups according to evidence strength.
- When code or analytics configs are available, point to exact files/tables/events inspected.

### Step 4: Validate
- Confirm every quantitative claim has a source, sample window, unit, and denominator.
- Confirm step counts are monotonically non-increasing for strict-ordered funnels; an increase signals a denominator, dedup, or window bug, not a real result. [EXPLICIT]
- Confirm recommendations do not depend on unverified tracking.
- Confirm privacy-sensitive data is minimized and no direct personal identifiers are exposed in the deliverable.
- Confirm the deliverable follows `assets/deliverable-checklist.md`.
- If the repository includes scripts for the skill, run its check script and `validate-skill-scripts.py --strict --run-checks --skill funnel-analytics`.

## Acceptance Criteria

The deliverable is **done** only when all hold (else mark `not verified` and stop): [EXPLICIT]

- [ ] Funnel type (ordered/any-order), unit, conversion window, and denominator policy are stated once and applied uniformly.
- [ ] Every step maps to a named event/state with an evidence status; no step is inferred from a chart alone.
- [ ] Each rate shows its numerator, denominator, sample window, and dedup rule.
- [ ] Strict-ordered step counts are non-increasing; any exception is explained.
- [ ] Every causal/"why" statement cites experiment, replay, or research — or is labeled a hypothesis.
- [ ] Segment claims include sample size; blended-vs-segment direction was checked.
- [ ] No direct PII in the output; aggregates used where sufficient.

## Quality Criteria

- [ ] Funnel objective, audience, unit, time window, and data owner are explicit.
- [ ] Denominators, numerators, exclusions, and deduplication rules are documented before rates are interpreted.
- [ ] Data-quality gaps are marked `not verified` and not filled with invented assumptions.
- [ ] Recommendations are separated into instrumentation fixes, research tasks, product changes, and experiments.
- [ ] Evidence tags are applied to all claims.

## Worked Example (signup → activation)

Input: provided events `signup_completed=10,000`, `profile_created=6,500`, `first_action=2,600`; unit=user; window=7d; strict-ordered; step-to-step denominators. [EXPLICIT]

| Step | Event | Count | Step rate | Overall rate | Status |
|------|-------|-------|-----------|--------------|--------|
| 1 | signup_completed | 10,000 | — | 100% | verified |
| 2 | profile_created | 6,500 | 65% | 65% | verified |
| 3 | first_action | 2,600 | 40% | 26% | verified |

Read-out: biggest absolute drop is step 2→3 (3,900 users, 60% loss). *Hypothesis* (not a finding): activation friction after profile setup. Next step is instrumentation of intermediate states + a research/replay pass, **not** a redesign. Counts are non-increasing — passes the validation check. [EXPLICIT]

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Denominator drift | Overall rates don't multiply to the final rate | Fix policy in Step 2; recompute all rates from one base |
| Window too short | Real conversions excluded, rates depressed | Compare against a longer window; state chosen window |
| Identity reset mid-funnel | Step 3 > step 2, or inflated entries | Dedup on stitched ID; flag as `not verified` if no stitch |
| Late-arriving data | Recent steps look low, recover over days | Use a settled lookback; exclude the unsettled tail |
| Survivorship framing | "Converters did X" mistaken for cause | Compare against non-converters; require experiment for cause |
| Segment-mix shift | Blended rate contradicts every segment | Decompose (Simpson's); report per-segment |

## Anti-Patterns

- Treating a dashboard screenshot as enough evidence for event definitions.
- Comparing step counts with different units, windows, or deduplication rules.
- Claiming "users drop because of friction" without session replay, research, experiment, or product evidence.
- Recommending conversion tactics before the tracking plan is reliable.
- Hiding uncertainty in averages when segment or cohort effects may reverse the conclusion.
- Logging or displaying direct personal identifiers when aggregate metrics are sufficient.

## Output Contract

The default output is a concise Markdown report with:

- scope and evidence inventory
- funnel definition table (with funnel type, unit, window, denominator policy)
- metric formulas and denominator rules
- drop-off and segment analysis
- instrumentation and data-quality gaps
- optimization hypotheses and experiment backlog
- validation plan, privacy notes, and residual risks

## Usage

Example invocations:

- "/funnel-analytics" - Run the full funnel analytics workflow
- "analyze signup-to-activation drop-off from these events" - Build a verified funnel analysis
- "audit our checkout funnel tracking plan" - Check instrumentation before recommending optimization

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the language of the user request unless repo conventions require otherwise [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not certify analytics accuracy unless source data, tracking plan, and validation checks were inspected or provided [EXPLICIT]
- Does not create or mutate product instrumentation when the user asks only for analysis/specification [EXPLICIT]
- Establishes correlation/where, not causation/why; causal claims require an experiment or quasi-experiment out of this skill's scope [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a minimum viable tracking brief and ask for events, counts, and business goal |
| Counts without event definitions | Treat rates as provisional and request/source event taxonomy |
| Mixed units or time windows | Stop rate comparison until denominators are reconciled |
| Small sample or rare conversion | Prefer instrumentation/research next step over optimization claims |
| Conflicting dashboard values | Flag discrepancy, list likely causes, and request source-of-truth owner |
| Re-entry / repeat conversion | Define whether re-entries count once or each time; dedup per unit accordingly |
| Non-linear or branching journey | Model each path as its own funnel; do not collapse into one ordered chain |
| Out-of-scope request | Redirect to appropriate skill or escalate |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
