<!-- distilled from alfa skills/sla-definition -->
<!-- > -->
# Sla Definition
> "Method over hacks."
## TL;DR
Define defensible service level agreements: pick metrics, set targets against measurement windows, attach credits/penalties, and wire monitoring so each clause is observable. [DOC]

## Procedure
### Step 1: Discover
- Capture business criticality per service, agreed hours of operation, and what the client can actually measure today. [DOC]
- Separate SLA (contractual, penalized) from SLO (internal target) and SLI (the raw signal). Only promise what monitoring can prove. [INFERENCIA]
### Step 2: Analyze
- For each candidate metric pick: measurement window, exclusions (planned maintenance, force majeure, client-caused), and the data source. Evaluate trade-offs per Constitution XIII/XIV. [INFERENCIA]
- Tighter targets cost more 9s of redundancy; quote the FTE-month delivery impact, never a price. [SUPUESTO] verify: confirm staffing model with delivery lead.
### Step 3: Execute
- Write each clause as: metric, formula, target, window, exclusions, credit. Tag every committed number. [DOC]
### Step 4: Validate
- Confirm each clause is machine-measurable from a named source before signing. Unobservable clause = drop or downgrade to SLO. [INFERENCIA]

## Core metrics (formulas)
| Metric | Formula | Typical target |
|--------|---------|----------------|
| Availability | (window − downtime) / window | per criticality tier [SUPUESTO] |
| P1 response | ack time from ticket open | minutes, business hrs [SUPUESTO] |
| P1 resolution | restore time from open | hours [SUPUESTO] |
| Error rate | failed reqs / total reqs | sub-percent [SUPUESTO] |

Targets are placeholders until set against the client's criticality tiers and measurement baseline; do not commit a number you cannot measure. [SUPUESTO] verify: agree tiers + baseline in discovery.

## Service credit structure
- Define breach tiers (e.g. minor / major / severe) as bands below target, each with a defined credit as a percentage of the period service fee. [DOC]
- Cap cumulative credits per period and make credits the sole financial remedy for SLA breach unless the contract states otherwise. [SUPUESTO] verify: legal review of remedy clause.
- Credits compensate; they are not pricing. State bands and caps, never currency amounts. [DOC]

## Worked example
P1 resolution SLA, business hours (Mon–Fri 08:00–18:00):
- Metric: restore time, ticket open → service restored, clock paused outside hours. [DOC]
- Target: 95% of P1s restored within the agreed threshold per month. [SUPUESTO]
- Exclusions: client-caused delay, third-party outage, declared maintenance. [DOC]
- Breach: <95% → minor band credit; <85% → major band credit; cap per period. [DOC]
- Source: ITSM ticket timestamps; reconciled monthly with the client. [INFERENCIA]

## Quality Criteria
- [ ] Every clause has metric, formula, target, window, exclusions, credit
- [ ] Each metric maps to a named, machine-readable data source
- [ ] Credits expressed as bands/caps, never currency
- [ ] Evidence tags applied (single Alfa family)
- [ ] Constitution-compliant and actionable

## Usage
Example invocations:
- "/sla-definition" — Run the full sla definition workflow
- "sla definition on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and current monitoring data. [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Defines SLA structure only; does not negotiate commercial terms or replace legal review of the remedy clause. [DOC]
- Does not replace domain expert judgment for final target-setting. [DOC]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Metric with no data source | Downgrade to internal SLO; do not put in contract |
| Target set with no baseline | Mark `[SUPUESTO]`, gather baseline before commit |
| 100% / zero-downtime demanded | Reject as unmeasurable; reframe as tiered availability |
| Exclusions undefined | Block sign-off; uncapped liability risk |
