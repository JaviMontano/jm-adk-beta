<!-- distilled from alfa skills/kpi-framework -->
<!-- > -->
# Kpi Framework
> "Method over hacks."
## TL;DR
KPI design via metric trees: one North Star, leading→lagging chains, OKR alignment. Every metric carries an owner, definition, and target. [DOC]

## Core model
- **Metric tree**: North Star at root → input metrics → levers. A metric earns a place only if a team can move it. [DOC]
- **Leading vs lagging**: leading predicts and is actionable within a sprint (activation rate); lagging confirms outcomes but lags weeks (retention, revenue). Pair each lagging KPI with ≥1 leading driver. [INFERENCIA]
- **OKR alignment**: each KPI maps to one Objective; Key Results are the target deltas, not the metrics themselves. [DOC]
- **Good KPI test**: owned, defined unambiguously, instrumented, comparable over time, and tied to a decision. Fail any → it is a vanity metric. [INFERENCIA]

## Procedure
### Step 1: Discover
- Gather the decision the KPI must inform, the owning team, and existing instrumentation. No decision → no KPI. [DOC]
### Step 2: Analyze
- Build the metric tree; classify each node leading/lagging; check Constitution XIII/XIV compliance. [CONFIG]
### Step 3: Execute
- Write each KPI as: name · precise definition · owner · target · cadence · evidence tag. [DOC]
### Step 4: Validate
- Verify quality criteria; confirm every lagging KPI has a leading driver and every KPI a decision. [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied (single Alfa family)
- [ ] Constitution-compliant
- [ ] Actionable output (each KPI ties to a decision + owner)
- [ ] Every lagging KPI paired with a leading driver
- [ ] Definitions unambiguous and instrumented

## Decisions & trade-offs
- **One North Star, not many**: focuses teams but hides multi-sided tension (e.g. growth vs trust) — surface that tension as guardrail metrics, not co-North-Stars. [INFERENCIA]
- **Ratios over raw counts** for KPIs: normalize for scale and resist gaming; raw counts stay as diagnostic context. [SUPUESTO] Verify the denominator is stable before adopting.
- **Fewer KPIs (5–7 per tree)**: more are unmemorable and dilute ownership. [SUPUESTO] Confirm with the team's review cadence.

## Worked example
North Star = Weekly Active Teams. Tree: Activation rate (leading) → WAT (lagging); Time-to-first-value (leading) → Activation. KR: lift activation 32%→45% in Q3, owner Growth PM. [DOC]

## Failure modes
| Failure | Symptom | Fix |
|---------|---------|-----|
| Vanity metric | Goes up, nothing decided | Drop or attach a decision |
| All-lagging tree | Can't act mid-cycle | Add leading drivers |
| Metric gaming | Number up, outcome flat | Pair with a guardrail metric |
| Orphan KPI | No named owner | Assign or remove |

## Usage

Example invocations:

- "/kpi-framework" — Run the full kpi framework workflow
- "kpi framework on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and live instrumentation. [SUPUESTO] Confirm event tracking exists before defining KPIs.
- English-language output unless otherwise specified. [DOC]
- Does not replace domain expert judgment for final target-setting. [DOC]
- Anti-scope: does not build dashboards, run statistical significance tests, or set pricing. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No instrumentation for a metric | Mark `[SUPUESTO]`, propose tracking plan, do not report a value |
| Metric with no owner | Block: assign owner before publishing the KPI |
