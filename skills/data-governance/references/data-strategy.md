<!-- distilled from alfa skills/data-strategy -->
<!-- > -->
# Data Strategy

> "Data is the new oil? No: Data is the new soil." — David McCandless

## TL;DR

Designs comprehensive data strategies covering architecture, governance, quality, and pipeline design to enable analytics, AI, and operational excellence. Use this skill when building data platforms, establishing data governance, or when data quality issues are impacting business decisions. [DOC]

## Scope & Anti-Scope

- **In scope**: data architecture blueprint, governance operating model, quality rule design, pipeline/lineage design, catalog + metadata standards. [DOC]
- **Out of scope** (redirect, see Related Skills): physical schema/index tuning → `database-design`; legal interpretation of regulations → `compliance-assessment`; live ETL code authoring; vendor/tool selection (recommend criteria, not products). [INFERENCIA]
- **Single deliverable**: a strategy document + decision log, not a running platform. [SUPUESTO] Verify by confirming the engagement is design-phase, not build-phase.

## Procedure

### Step 1: Discover
- Inventory data sources, stores, and consumers; record owner, refresh cadence, and volume for each. [DOC]
- Assess current quality on four axes — completeness, accuracy, timeliness, consistency — with a baseline number per axis, not a verdict. [DOC]
- Identify stakeholders: producers, consumers, stewards, regulators. Missing a steward role is the most common gap. [INFERENCIA]
- Map current flows and transformation pipelines, marking every hop where data is copied without lineage. [INFERENCIA]

### Step 2: Analyze
- Classify data by sensitivity: public, internal, confidential, restricted. Classification drives access, retention, and residency decisions downstream. [DOC]
- Identify domains and ownership using data-mesh principles **only when** ≥3 autonomous teams own distinct domains; below that, a centralized model is cheaper to run. [INFERENCIA]
- Choose pipeline patterns per source, not globally: batch vs. streaming, ETL vs. ELT (decision matrix below). [INFERENCIA]
- Assess gaps: missing data, quality defects, accessibility barriers. Rank by business impact, not by ease of fix. [SUPUESTO] Validate ranking with the data consumer.

### Step 3: Execute
- Design the architecture blueprint: medallion (bronze/silver/gold) for analytics-heavy estates, domain-oriented mesh for federated orgs. [INFERENCIA]
- Define the governance framework: ownership, stewardship, quality SLAs, and an escalation path with a named decision-maker. [DOC]
- Author quality rules as code with monitoring dashboards; each rule states metric, threshold, and action-on-breach. [DOC]
- Design pipeline architecture with lineage tracking, observability, and explicit error handling (retry + dead-letter). [DOC]
- Document the catalog structure and metadata standards so a new consumer can self-serve discovery. [INFERENCIA]

### Step 4: Validate
- Verify the architecture serves both operational and analytical workloads without coupling them (e.g., no analytics query load on the transactional store). [INFERENCIA]
- Confirm every governance role is assigned to a named person and acknowledged, not just defined on paper. [DOC]
- Check that quality rules run automatically and alert; a rule no one is paged for is decorative. [INFERENCIA]
- Validate compliance posture against applicable regimes (GDPR, CCPA, sector rules); flag residency and retention obligations. [SUPUESTO] Confirm the specific regimes with legal/compliance.

## Key Decisions & Trade-offs

| Decision | Choose A when… | Choose B when… | Cost of wrong call |
|---|---|---|---|
| **ETL vs. ELT** | Target store is compute-poor or transforms are heavy/sensitive (ETL) | Warehouse/lakehouse has cheap elastic compute and you want raw retained (ELT) | ETL-on-warehouse wastes spend; ELT-on-weak-store stalls loads [INFERENCIA] |
| **Batch vs. streaming** | Hours-fresh is fine; lower ops burden (batch) | Decisions need sub-minute data; event-driven (streaming) | Streaming where batch suffices multiplies ops cost with no value [INFERENCIA] |
| **Medallion vs. mesh** | One platform team, shared models (medallion) | Many autonomous domain teams (mesh) | Mesh without team maturity creates N inconsistent silos [INFERENCIA] |
| **Centralized vs. federated governance** | Few domains, high regulatory load (central) | Many domains, fast autonomy needed (federated) | Central at scale becomes a bottleneck; federated too early loses consistency [SUPUESTO] |

## Worked Example

Mid-size retailer: 12 sources, 5 consuming teams, GDPR in scope. [SUPUESTO]
- Discover finds order data 99% complete but 3-day stale; marketing needs same-day. [INFERENCIA]
- Decision: ELT into a lakehouse (cheap compute, raw retained), streaming only for the order feed, batch for the rest. [INFERENCIA]
- Governance: centralized (5 teams < mesh threshold), one steward per source, quality SLA = "orders ≥99% complete, ≤2h stale". [INFERENCIA]
- Rule on breach: page the order-domain steward; hold downstream gold refresh. [DOC]

## Quality Criteria

- [ ] Data inventory covers all sources with a named owner each. [DOC]
- [ ] Governance framework defines roles, policies, and a single escalation path. [DOC]
- [ ] Every quality rule has a metric, a numeric threshold, and an action-on-breach. [DOC]
- [ ] Pipeline design includes error handling, retry, and dead-letter queues. [DOC]
- [ ] Sensitivity classification drives at least one concrete access/retention control. [INFERENCIA]
- [ ] Evidence tags applied to all non-obvious claims, one per claim. [DOC]

## Anti-Patterns & Failure Modes

- Data lake without governance → data swamp; nobody trusts or finds anything. [INFERENCIA]
- Pipelines without lineage → an upstream schema change silently corrupts every downstream report. [INFERENCIA]
- Quality as one-time cleanup → drift returns within weeks; treat it as a continuous, monitored process. [INFERENCIA]
- SLAs defined but unmonitored → false confidence; the breach is discovered by the consumer, not the system. [INFERENCIA]
- Mesh adopted for fashion, not fit → duplicated, divergent domain models and higher total cost. [SUPUESTO]

## Related Skills

- `database-design` — physical data modeling and schema design
- `compliance-assessment` — data protection regulatory requirements
- `event-architecture` — event-driven data pipeline patterns

## Usage

Example invocations:

- "/data-strategy" — Run the full data strategy workflow
- "data strategy on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO] If absent, Step 1 stalls — request inventory before proceeding.
- Requires English-language output unless otherwise specified. [DOC]
- Recommends patterns and criteria, not specific vendors or prices. [DOC]
- Does not replace domain-expert or legal judgment for final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to the matching Related Skill or escalate |
| No data steward exists | Flag as a critical governance gap; propose an interim owner |
| Single team, one domain | Skip mesh; use centralized governance + medallion |
| Regulated data, regime unknown | Treat as restricted by default; confirm regime before design |
