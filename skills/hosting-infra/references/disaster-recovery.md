<!-- distilled from alfa skills/disaster-recovery -->
<!-- > -->
# Disaster Recovery
> "Method over hacks."
## TL;DR
Set RTO/RPO targets per tier, prove failover by drill (not by faith), and keep a runbook a half-awake operator can execute. [DOC]
## Procedure
### Step 1: Discover
- Inventory each service's tier, dependencies, and data store; capture current RTO/RPO vs. target. [DOC]
- Confirm backups exist AND restore (see backup-strategy.md) — an untested backup is not a recovery option. [DOC]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV; pick a strategy whose cost matches the tier, not the worst case. [DOC]
- Strategies, ascending cost/speed: backup-restore (hours) → pilot-light → warm-standby → active-active (near-zero). [DOC]
- Trade-off: active-active removes the failover step but doubles run cost and forces multi-region data consistency. [INFERENCIA]
### Step 3: Execute
- Document trigger, failover steps, DNS/traffic cutover, and rollback in one runbook; tag every config claim. [CONFIG]
- Automate the cutover where the RTO is tighter than a human can react (e.g. health-check-driven DNS failover). [INFERENCIA]
### Step 4: Validate
- Run a game-day drill; measure actual RTO/RPO vs. target, file gaps as findings, and re-drill after any topology/data-model change. [DOC]
## Assumptions & Limits
- RTO = max tolerable downtime; RPO = max tolerable data loss. Both are per-tier, set by the business, not by ops. [DOC]
- Covers recovery design and rehearsal; excludes the backup mechanism (backup-strategy.md) and live incident command. [SUPUESTO]
- Assumes backups are restorable and the failover target region has capacity reserved or burstable. [SUPUESTO]
## Worked Example
- Tier-1 API, RTO 15min / RPO 5min: warm-standby in region B, async DB replication, health-check DNS failover, monthly drill. [INFERENCIA]
- Tier-3 internal tool, RTO 24h / RPO 24h: nightly backup-restore, no standby — paying for warm-standby here is waste. [INFERENCIA]
## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Backup restores but app won't boot | Drill the full restore-to-running path, not just data restore [DOC] |
| Primary AND failover region degraded | Define a degraded-mode / read-only fallback; document it explicitly [SUPUESTO] |
| Failover succeeds, failback undefined | Runbook MUST cover return-to-primary, incl. reconciling diverged writes [DOC] |
| No RTO/RPO set by business | Stop and escalate — do not invent targets; surface as a blocking gap [SUPUESTO] |
## Quality Criteria
- [ ] RTO/RPO defined per tier and traced to a business owner
- [ ] Failover AND failback steps documented and drilled
- [ ] Last successful drill date recorded; gaps filed as findings
- [ ] Evidence tags applied; Constitution-compliant; actionable output
