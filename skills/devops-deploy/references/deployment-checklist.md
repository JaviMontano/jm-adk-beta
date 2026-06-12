<!-- distilled from alfa skills/deployment-checklist -->
<!-- > -->
# Deployment Checklist

## TL;DR

Pre- and post-deployment validation checklist: env-var verification, build integrity, rollback planning, monitoring, and go-live procedures. Run before any production deploy so nothing critical is missed. [EXPLICIT]

## Scope & Anti-Scope

- **In scope:** application/service deploys via CI/CD to a production or staging environment; schema migrations; config and secret rollout. [EXPLICIT]
- **Out of scope:** infra provisioning (IaC apply), DNS cutover design, and capacity planning — gate those separately; this checklist assumes the target environment already exists. [EXPLICIT]
- **Decision — CI/CD over manual deploy:** manual deploys skip the audit trail and are not reproducible for rollback. Trade-off: pipeline setup cost up front, paid back on the first incident. [INFERENCIA]

## Procedure

### Step 1: Discover
- Review all changes in the deploy (commits, PRs, changelog); flag anything touching auth, payments, or data shape.
- Confirm production env vars + secrets are set AND match the names the new build reads (drift here is the #1 silent failure). [INFERENCIA]
- Verify third-party config: API keys, webhook URLs, DNS, rate limits.
- Confirm staging/preview was tested and approved by a named owner.

### Step 2: Analyze
- Score deploy risk: **low** (code-only, no schema/API change) → **high** (irreversible migration, breaking API, new external dependency). Risk tier sets the rigor of the steps below. [EXPLICIT]
- Plan a rollback per component; for DB migrations, prefer expand/contract so old and new code run against the same schema. [INFERENCIA]
- Identify monitoring points: error rate, p95 latency, and one key business metric (signups, checkout, etc.).
- Set deploy window and comms plan; avoid windows with no on-call coverage.

### Step 3: Execute
- **Pre-Deploy:**
  - [ ] All CI/CD checks pass (lint, test, build, security scan) — no overrides
  - [ ] Env vars + secrets set in production config and name-matched to the build
  - [ ] DB migrations tested AND reversible (or expand/contract phased)
  - [ ] Feature flags configured for gradual rollout, defaulting OFF
  - [ ] Rollback procedure documented and dry-run at least once
  - [ ] Team notified of deploy window; on-call confirmed available
- **Deploy:**
  - [ ] Deploy via CI/CD pipeline (never manual / never local creds)
  - [ ] Watch deploy progress and logs through completion
  - [ ] For high-risk: roll out to a canary slice before full fleet
- **Post-Deploy:**
  - [ ] Application loads and critical user flows succeed (smoke test)
  - [ ] Error monitoring (Sentry, Cloud Error Reporting) shows no new error classes
  - [ ] Analytics events still firing with correct schema
  - [ ] Performance metrics within baseline (no p95 regression)
  - [ ] SSL certs valid and security headers intact

### Step 4: Validate
- All checklist items completed and documented; skips justified in writing.
- Monitoring shows no anomalies for **30 min** post-deploy (longer for high-risk).
- Rollback confirmed still available (artifact + procedure both reachable).
- Deploy logged in team changelog / release notes with version and owner.

## Acceptance Criteria

Done when ALL hold: [EXPLICIT]
- [ ] Pre-deploy checklist completed, zero unjustified skips.
- [ ] Rollback plan documented and dry-run before deploy.
- [ ] Post-deploy monitoring clean for ≥30 min (≥60 min if high-risk).
- [ ] Deploy recorded in release notes/changelog with version + owner.
- [ ] Every claim in the deploy record carries an evidence tag.

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Env-var / secret drift | App boots but 500s on first real request | Name-match build↔config in Step 1; smoke test in Step 4. |
| Irreversible migration | Rollback impossible after deploy | Expand/contract; never drop columns in the same release that stops writing them. |
| Canary skipped on high-risk | Full-fleet outage on a bad build | Risk tier in Step 2 forces canary for high-risk. |
| Monitoring blind spot | Regression ships unnoticed | Define error + latency + business metric BEFORE deploy, not after. |
| Flag default ON | New code path live before validation | Flags default OFF; flip post-smoke-test. |

## Worked Example — high-risk deploy with a migration

Service adds a `currency` column and reads it in checkout. [SUPUESTO]
1. **Discover:** PR touches payments → flag high-risk. Confirm `CURRENCY_DEFAULT` secret set.
2. **Analyze:** Migration is additive (expand phase) → reversible. Monitor checkout success rate.
3. **Execute (expand):** Ship migration adding nullable `currency` first, code still ignores it. Deploy code reading it behind a flag (OFF). Canary 5% → flip flag → watch checkout rate.
4. **Validate:** 30 min clean → roll to 100%. Later contract phase (make column non-null) ships as its own low-risk deploy.

## Anti-Patterns

- Deploying Friday afternoon (thin monitoring, slow incident response).
- Skipping staging ("it works locally").
- No rollback plan ("we'll fix forward" — until you can't).
- Coupling expand and contract migration phases in one release (removes the rollback window).

## Related Skills

- `firebase-deployment` — Firebase-specific deployment procedures
- `github-actions-ci` — automated deployment pipeline execution

## Usage

- `/deployment-checklist` — run the full workflow
- "deployment checklist on this project" — apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes the target environment already exists and is reachable. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Checklist guides but does not replace domain-expert judgment on the go/no-go call. [EXPLICIT]
- The 30-min window is a floor, not a guarantee; slow-burn regressions can surface later. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Rollback artifact unavailable | Block deploy until a tested rollback path exists |
| Migration not reversible | Require expand/contract or an explicit signed-off go/no-go |
