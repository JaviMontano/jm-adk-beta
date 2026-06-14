<!-- distilled from alfa skills/backup-strategy -->
<!-- > -->
# Backup Strategy
> "Method over hacks."

## TL;DR
Define and verify backups for hosted data: scheduled Firestore/database exports, tiered retention, restore drills, and documented RTO/RPO. Output is a backup plan with evidence tags, not a one-off export. [DOC]

## Scope
- In: backup cadence, retention tiers, export targets, restore-test procedure, RTO/RPO targets. [DOC]
- Out: live HA/failover design, app-level soft-delete, secrets rotation, ransomware IR runbook (separate skills). [SUPUESTO]

## Procedure
### Step 1: Discover
- Inventory stateful stores (Firestore, SQL, object buckets, config) and current backup mechanism, if any. [DOC]
- Capture data criticality, regulatory retention, and tolerable loss/downtime per store. [DOC]
### Step 2: Analyze
- Set RPO (max data loss) and RTO (max restore time) per store; derive cadence from RPO. Evaluate options per Constitution XIII/XIV. [INFERENCIA]
- Choose retention tiers (e.g. daily x7, weekly x4, monthly x12) and a separate-account/region destination. [SUPUESTO]
### Step 3: Execute
- Implement scheduled exports to an isolated bucket; enable encryption + lifecycle rules; tag every config claim. [CONFIG]
### Step 4: Validate
- Run an end-to-end restore into a scratch environment; measure actual RTO against target. A backup unverified by restore does not count. [INFERENCIA]

## Quality Criteria
- [ ] RPO/RTO defined per store, cadence derived from RPO
- [ ] Backups land in an isolated account/region, encrypted, with lifecycle retention
- [ ] At least one successful restore drill recorded with measured RTO
- [ ] Evidence tags applied; Constitution-compliant; actionable output

## Usage
Example invocations:
- "/backup-strategy" — Run the full backup strategy workflow
- "backup strategy on this project" — Apply to current context

## Worked Example
Firestore prod: RPO 24h, RTO 4h. Scheduled daily export (`gcloud firestore export`) to a backup-project bucket in a second region; lifecycle keeps daily x7, weekly x4, monthly x6; quarterly restore drill into a staging project validates RTO. [CONFIG]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and to backup/restore IAM. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final retention/compliance decisions. [DOC]
- Cost and export windows scale with dataset size; very large stores may need incremental/PITR instead of full exports. [INFERENCIA]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No restore ever tested | Treat backups as unproven; mandate a drill before sign-off |
| Backup in same account/region as prod | Flag as single point of failure; require isolation |
| Retention shorter than compliance window | Block; surface the gap as `[SUPUESTO]` needing legal confirmation |
| Restore exceeds RTO target | Record gap, recommend incremental/PITR or warm standby |
