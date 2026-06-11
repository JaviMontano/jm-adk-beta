<!-- distilled from alfa skills/data-strategy -->
<!-- > -->
# Data Strategy

> "Data is the new oil? No: Data is the new soil." — David McCandless

## TL;DR

Designs comprehensive data strategies covering architecture, governance, quality, and pipeline design to enable analytics, AI, and operational excellence. Use this skill when building data platforms, establishing data governance, or when data quality issues are impacting business decisions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Inventory existing data sources, stores, and consumers
- Assess current data quality: completeness, accuracy, timeliness, consistency
- Identify data stakeholders: producers, consumers, stewards, regulators
- Map current data flows and transformation pipelines

### Step 2: Analyze
- Classify data by sensitivity (public, internal, confidential, restricted)
- Identify data domains and ownership using data mesh principles
- Evaluate pipeline patterns: batch vs. streaming, ETL vs. ELT
- Assess gaps: missing data, quality issues, accessibility barriers

### Step 3: Execute
- Design a data architecture blueprint (medallion architecture or domain-oriented)
- Define data governance framework: ownership, stewardship, quality SLAs
- Create data quality rules and monitoring dashboards
- Design pipeline architecture with lineage tracking and observability
- Document a data catalog structure with metadata standards

### Step 4: Validate
- Verify data architecture supports both operational and analytical workloads
- Confirm governance roles are assigned and understood
- Check that quality rules are automated and monitored, not manual
- Validate compliance with data protection regulations (GDPR, CCPA)

## Quality Criteria

- [ ] Data inventory covers all sources with ownership assigned
- [ ] Governance framework defines roles, policies, and escalation
- [ ] Quality rules are measurable and automated
- [ ] Pipeline design includes error handling, retry, and dead-letter queues
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Data lake without governance becoming a data swamp
- ETL pipelines without lineage tracking or error monitoring
- Treating data quality as a one-time cleanup instead of continuous process

## Related Skills

- `database-design` — physical data modeling and schema design
- `compliance-assessment` — data protection regulatory requirements
- `event-architecture` — event-driven data pipeline patterns

## Usage

Example invocations:

- "/data-strategy" — Run the full data strategy workflow
- "data strategy on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
