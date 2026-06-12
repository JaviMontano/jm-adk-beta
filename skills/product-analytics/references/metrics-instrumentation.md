<!-- distilled from alfa skills/metrics-instrumentation -->
<!-- > -->
# Metrics Instrumentation
> "Method over hacks."

## TL;DR
Code-level metric capture: custom dimensions/metrics, event parameter schemas, and the instrumentation handoff that makes a metric measurable, attributable, and queryable in the destination tool. [EXPLICIT]

## When To Use
- The user needs to instrument a metric, custom dimension, event parameter, computed metric, or scoped user/session/product property in code (GA4, Amplitude, Mixpanel, Segment, OpenTelemetry, or SDK-level capture).
- A metric in `kpi-framework` or an event in `analytics-events` needs the concrete parameters, types, and scope that let it be computed downstream.

## When Not To Use
- Event taxonomy/naming design only — use `analytics-events`.
- KPI selection or target-setting — use `kpi-framework`.
- Dashboard layout or chart choice — use `data-visualization`.

## Procedure

### Step 1: Discover
- Gather the metric's definition, owner, the funnel/event it attaches to, and the destination tool's dimension/metric limits. [EXPLICIT]
- Record the unit, aggregation (count, sum, rate, unique, p50/p95), and scope (event, user, session, item) before writing any parameter. [INFERENCIA]

### Step 2: Analyze
- Evaluate capture options per Constitution XIII/XIV; choose client vs. server capture by trust and completeness needs. [CONFIG]
- Trade-off: client capture is cheaper and richer in UI context but lossy (ad-blockers, drop-off); server capture is authoritative but blind to client-only signals. State which and why. [INFERENCIA]

### Step 3: Execute
- Define each parameter with name (snake_case), type, scope, example value, cardinality bound, and PII class; tag every choice. [EXPLICIT]
- Reuse existing dimensions before minting new ones; respect the tool's custom-dimension quota. [EXPLICIT]

### Step 4: Validate
- Verify the metric computes correctly from captured parameters, matches its declared unit/aggregation, and survives the QA fixture. [EXPLICIT]

## Worked Example
Metric `checkout_completion_rate` = `count(purchase) / count(checkout_started)`, scope=session. Requires events `checkout_started` and `purchase`, shared dimension `cart_id` (string, high-cardinality, non-PII) for de-dup, and metric param `order_value` (number, scope=event, currency minor units). [EXPLICIT]

## Quality Criteria
- [ ] Each parameter has name, type, scope, unit, cardinality bound, and PII class.
- [ ] Aggregation and scope are explicit and consistent with the metric's KPI definition.
- [ ] Client vs. server capture chosen with a stated trade-off.
- [ ] No new dimension created where an existing one suffices; quota respected.
- [ ] Evidence tags applied; Constitution-compliant; output is actionable.

## Usage
- "/metrics-instrumentation" — Run the full metrics instrumentation workflow.
- "metrics instrumentation on this project" — Apply to current context.

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and the destination tool's schema/quotas. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Defines the parameter/dimension contract and handoff; does not write production SDK code unless requested. [EXPLICIT]
- Does not replace privacy/legal review for regulated data, nor domain-expert judgment for final metric definitions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request the metric definition and destination tool before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to `analytics-events`, `kpi-framework`, or escalate. |
| High-cardinality dimension | Warn on quota/cost blowup; propose bucketing or hashing. |
| PII in a parameter | Mark privacy review as blocking; propose a safe identifier. |
| Custom-dimension quota exhausted | Reuse or deprecate an existing dimension before adding one. |
