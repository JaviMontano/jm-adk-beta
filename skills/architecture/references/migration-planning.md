<!-- distilled from alfa skills/migration-planning -->
<!-- > -->
# Migration Planning

> "The best time to plant a tree was 20 years ago. The second best time is now." — Chinese Proverb

## TL;DR

Plans technology and data migrations using incremental strategies like strangler fig, parallel runs, and feature flagging to minimize risk and enable rollback at every stage. Use this skill when modernizing legacy systems, migrating databases, switching cloud providers, or upgrading major framework versions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Map the current system: components, data stores, integrations, dependencies
- Identify migration drivers: EOL technology, scaling limits, cost reduction, capability gaps
- Assess data volume, complexity, and referential integrity constraints
- Inventory all consumers of the system being migrated

### Step 2: Analyze
- Choose migration strategy:
  - **Strangler Fig**: incrementally replace legacy with new system feature by feature
  - **Parallel Run**: run both systems simultaneously, compare outputs, switch over
  - **Big Bang**: replace everything at once (highest risk, use sparingly)
- Design data migration pipeline: extract, transform, validate, load, reconcile
- Plan rollback at every stage: what triggers rollback, how long to restore
- Identify the migration sequence: which features/data migrate first

### Step 3: Execute
- Create a phased migration plan with milestones and rollback gates
- Design data migration scripts with validation and reconciliation checks
- Implement feature flags to control traffic routing between old and new systems
- Build a migration dashboard tracking: data migrated, errors, rollback status
- Document runbooks for each migration phase with step-by-step instructions
- Plan communication to stakeholders: downtime windows, behavior changes

### Step 4: Validate
- Verify data integrity post-migration: row counts, checksums, referential integrity
- Confirm rollback procedures work and can execute within SLA windows
- Test that all consumers work correctly against the new system
- Validate performance meets or exceeds pre-migration baselines

## Quality Criteria

- [ ] Migration plan has rollback capability at every phase
- [ ] Data migration includes validation and reconciliation steps
- [ ] Stakeholder communication plan covers all affected parties
- [ ] Runbooks exist for each migration phase with rollback procedures
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Big bang migration without rollback plan
- Data migration without reconciliation (assuming it worked)
- Migrating and decommissioning the old system in the same step

## Related Skills

- `system-architecture` — target architecture for the migrated system
- `risk-assessment` — risk analysis specific to migration scenarios
- `database-design` — target data model for migrated data

## Usage

Example invocations:

- "/migration-planning" — Run the full migration planning workflow
- "migration planning on this project" — Apply to current context


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
