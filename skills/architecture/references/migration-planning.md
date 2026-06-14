<!-- distilled from alfa skills/migration-planning -->
<!-- > -->
# Migration Planning

> "The best time to plant a tree was 20 years ago. The second best time is now." — Chinese Proverb

## TL;DR

Plans technology and data migrations using incremental strategies (strangler fig, parallel run, feature flagging) to minimize blast radius and keep rollback available at every stage. Use when modernizing legacy systems, migrating databases, switching cloud providers, or upgrading major framework versions. [EXPLICIT]

**Default bias:** prefer incremental over big bang; prefer reversible steps over irreversible ones; never migrate and decommission in the same change. [INFERRED]

## Procedure

### Step 1: Discover
- Map current system: components, data stores, integrations, dependencies, ownership
- Identify drivers: EOL technology, scaling limits, cost, capability gaps, compliance
- Assess data volume, complexity, referential integrity, and PII/regulatory constraints
- Inventory every consumer (services, batch jobs, reports, dashboards, external partners) — undiscovered consumers are the top cause of post-cutover incidents [INFERRED]
- Capture pre-migration baselines now (latency p50/p95/p99, throughput, error rate, row counts) — you cannot prove parity later without them [INFERRED]

### Step 2: Analyze — strategy selection

| Strategy | When to choose | Trade-off |
|----------|----------------|-----------|
| **Strangler Fig** | Clear feature/seam boundaries; long-lived migration acceptable | Lowest risk; needs routing layer + dual maintenance during overlap |
| **Parallel Run** | Correctness must be proven before trust (finance, billing) | Highest confidence; doubles compute cost + needs output-diffing harness |
| **Big Bang** | System too small/coupled to split; short freeze tolerable | Fastest; rollback is all-or-nothing — use only with a tested restore path |

- Design data pipeline: extract → transform → validate → load → reconcile
- Define rollback per stage: explicit trigger condition, restore mechanism, time-to-restore target, and who decides [EXPLICIT]
- Sequence the migration: lowest-risk / lowest-coupling slice first to prove the mechanism before high-value data [INFERRED]
- Decide cutover style up front: point-in-time switch vs. gradual traffic shift (canary %)

### Step 3: Execute
- Phased plan with milestones and explicit rollback gates between phases
- Data scripts with built-in validation and reconciliation (idempotent + re-runnable, so a partial failure can resume) [INFERRED]
- Feature flags / routing to shift traffic between old and new; flags removed after the phase is decommissioned (stale flags become their own debt) [INFERRED]
- Dashboard tracking: rows migrated, reconciliation deltas, error counts, current rollback status
- Runbook per phase: pre-checks, ordered steps, verification, rollback steps, contacts
- Stakeholder comms: downtime windows, behavior changes, freeze periods, go/no-go owner

### Step 4: Validate
- Data integrity: row counts, checksums, referential integrity, spot-check sampled records
- Reconciliation delta within agreed tolerance (default 0 for financial/identity data) [EXPLICIT]
- Rollback rehearsed end-to-end in a non-prod environment, within the stated SLA window — an untested rollback is not a rollback [EXPLICIT]
- All inventoried consumers verified against the new system
- Performance meets or exceeds the baselines captured in Step 1

## Worked example — Postgres v11 → v15 with zero data loss

1. Stand up v15 replica via logical replication; let it catch up. [EXPLICIT]
2. Run app's read traffic against v15 (shadow/canary) and diff results. [INFERRED]
3. Reconcile: `count(*)` and per-table checksums must match before cutover. [EXPLICIT]
4. Brief write-freeze → final replication flush → repoint connection string. [EXPLICIT]
5. Keep v11 hot and read-only for the rollback window; decommission only after the window passes clean. [EXPLICIT]

## Quality Criteria

- [ ] Rollback capability defined and rehearsed at every phase
- [ ] Data migration includes validation + reconciliation, scripts idempotent
- [ ] Pre-migration baselines captured before any change
- [ ] Every consumer inventoried and re-tested post-migration
- [ ] Stakeholder communication plan covers all affected parties
- [ ] Runbooks exist per phase with rollback procedures
- [ ] Evidence tags applied to all non-obvious claims

## Anti-Patterns

- Big bang migration without a tested rollback plan
- Data migration without reconciliation (assuming it worked)
- Migrating and decommissioning the old system in the same step
- No pre-migration baseline, so "performance is fine" is unprovable
- Cutover scheduled before rollback has been rehearsed
- Non-idempotent scripts that cannot resume after a partial failure

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Hidden consumer | Errors from an un-inventoried client after cutover | Full consumer inventory (Step 1); monitor old-system traffic to zero before decommission |
| Silent data drift | Counts match, values differ | Checksums + sampled value comparison, not just row counts |
| Rollback too slow | Restore exceeds SLA mid-incident | Rehearse rollback; measure actual time-to-restore against target |
| Dual-write skew | Old and new diverge during overlap | Single source of truth per record; reconcile continuously, not once |

## Anti-Scope

- Does not author the target architecture → `system-architecture`
- Does not perform the migration code changes itself — produces the plan, gates, and runbooks [EXPLICIT]
- Does not own infrastructure provisioning or networking cutover

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
- Assumes a non-prod environment exists to rehearse rollback [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final go/no-go decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No baseline obtainable | Flag as a risk; parity cannot be proven without it |
| Irreversible step required | Surface explicitly; require a sign-off gate before it |
