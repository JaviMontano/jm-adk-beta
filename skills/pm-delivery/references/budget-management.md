<!-- distilled from alfa skills/budget-management -->
<!-- > -->
# Budget Management
> "Method over hacks."

## TL;DR
Track project spend in FTE-months: baseline the budget, measure burn rate, forecast at-completion, and explain variance with a corrective action. Never emit currency prices — effort and capacity only. [DOC]

## Scope
- In: cost baseline, burn-rate tracking, EAC/ETC forecasting, variance analysis + corrective actions. [DOC]
- Out (anti-scope): currency pricing/quotes, vendor rate negotiation, payroll, invoicing, procurement approval. Redirect these; do not fabricate numbers. [SUPUESTO]

## Core formulas (effort-based, no currency)
- Burn rate = FTE-months consumed ÷ elapsed periods. [DOC]
- EAC (estimate at completion) = actuals-to-date + remaining-work estimate. [INFERENCIA]
- Variance = baseline − EAC; negative variance = over budget. [DOC]
- Forecast confidence degrades as remaining-work estimate ages; re-baseline when variance exceeds the agreed threshold (default 10%). [SUPUESTO] → confirm threshold with the project owner.

## Procedure
### Step 1: Discover
- Gather baseline budget (FTE-months), team capacity, period boundaries, and actuals-to-date. If actuals are missing, this is a critical gap — stop and request them, do not infer spend. [SUPUESTO]
### Step 2: Analyze
- Compute burn rate, EAC, and variance per Constitution XIII/XIV. Flag any period where burn rate exceeds planned capacity. [INFERENCIA]
### Step 3: Execute
- Produce the variance table with evidence tags; for each over-threshold line, attach one corrective action and an owner. [DOC]
### Step 4: Validate
- Verify quality criteria below before marking complete. [DOC]

## Worked example
Baseline 12 FTE-months, 4 of 6 months elapsed, 9 FTE-months consumed.
Burn = 9÷4 = 2.25/mo; remaining work est. = 5 FTE-months; EAC = 9+5 = 14; variance = 12−14 = −2 FTE-months (≈17% over → re-baseline triggered). [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied (Alfa set: `[DOC]`/`[CÓDIGO]`/`[CONFIG]`/`[INFERENCIA]`/`[SUPUESTO]`)
- [ ] No currency prices anywhere in the output
- [ ] Every over-threshold variance has a corrective action + owner
- [ ] Forecast assumptions made explicit and paired with a verification step
- [ ] Constitution-compliant and actionable

## Usage
Example invocations:
- "/budget-management" — Run the full budget management workflow
- "budget management on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (baseline, actuals, capacity, configs). [SUPUESTO]
- English-language output unless otherwise specified. [DOC]
- Operates in FTE-months; does not convert to or emit currency. [DOC]
- Does not replace domain expert judgment for final budget decisions. [DOC]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Missing actuals-to-date | Critical gap — stop and ask; never infer spend |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| User requests a currency price | Decline; return FTE-months + disclaimer |
| Variance over threshold | Trigger re-baseline; attach corrective action + owner |
| Out-of-scope request | Redirect to appropriate skill or escalate |
