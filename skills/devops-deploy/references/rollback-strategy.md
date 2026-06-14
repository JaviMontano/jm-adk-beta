<!-- distilled from alfa skills/rollback-strategy -->
# Rollback Strategy
> "Method over hacks."
## TL;DR
Pick a rollback pattern BEFORE deploy, not during the incident. Stateless app rollback is cheap; data/schema rollback is the hard part — design forward. [SUPUESTO]
## Scope
- IN: app-version revert, traffic shifting, flag disablement, schema-change safety. OUT: backup/restore DR, secret rotation, infra teardown. [INFERENCIA]
## Pattern Selection
| Pattern | Revert action | MTTR | Cost / limit |
|---|---|---|---|
| Blue-green | Repoint LB to old env | Seconds | 2x infra; in-flight sessions drop unless drained [SUPUESTO] |
| Canary | Halt rollout, route 100% to stable | <1 min | Needs metric gate + auto-abort threshold |
| Feature flag | Toggle off, no redeploy | Seconds | Only covers flagged code; stale flags = debt |
| Schema | Expand/contract migration | Minutes–hours | Never drop columns in same release [CÓDIGO] |
## Decision (Constitution XIII/XIV)
- Default to **flag-gated canary**: smallest blast radius + instant kill switch. [INFERENCIA]
- DB: ship **backward-compatible (expand) first, contract one release later** — an old app instance must run against the new schema during rollback. [SUPUESTO]
- Trade-off: blue-green buys speed at 2x cost; canary buys safety at slower full rollout. Choose by MTTR target, not preference. [INFERENCIA]
## Edge Cases / Failure Modes
- In-flight writes during blue-green cutover → enforce connection draining + idempotent writes. [SUPUESTO]
- Canary metric gate flaps on low traffic → require min sample size before abort. [INFERENCIA]
- Irreversible migration already ran → rollback is forward-fix only; flag-gate the read path. [CÓDIGO]
- Flag default flips on redeploy → pin default to safe state in config, not code. [CONFIG]
## Acceptance Criteria
- [ ] Rollback path chosen and tested in staging pre-deploy
- [ ] Rollback trigger + owner + MTTR target documented
- [ ] Migrations expand/contract-safe; no destructive change this release
- [ ] Kill switch (flag or LB) verified reachable under incident load
- [ ] Evidence tags applied; Constitution XIII/XIV-compliant
