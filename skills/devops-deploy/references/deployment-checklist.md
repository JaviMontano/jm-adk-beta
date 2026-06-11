<!-- distilled from alfa skills/deployment-checklist -->
<!-- > -->
# Deployment Checklist

> "A checklist is the last line of defense between confidence and catastrophe." — Atul Gawande (adapted)

## TL;DR

Provides a comprehensive pre-deployment and post-deployment validation checklist — environment variable verification, build integrity checks, rollback planning, monitoring setup, and go-live procedures. Use before any production deployment to ensure nothing critical is missed. [EXPLICIT]

## Procedure

### Step 1: Discover
- Review all changes included in the deployment (commits, PRs, changelog)
- Check environment variables are configured for production
- Verify third-party service configurations (API keys, webhooks, DNS)
- Confirm staging/preview deployment was tested and approved

### Step 2: Analyze
- Assess deployment risk level (database migration, breaking API changes, new service)
- Plan rollback strategy for each deployed component
- Identify monitoring points (error rates, performance, key business metrics)
- Determine deployment window and communication plan

### Step 3: Execute
- **Pre-Deploy Checklist:**
  - [ ] All CI/CD checks pass (lint, test, build, security scan)
  - [ ] Environment variables set in production config
  - [ ] Database migrations tested and reversible
  - [ ] Feature flags configured for gradual rollout
  - [ ] Rollback procedure documented and tested
  - [ ] Team notified of deployment window
- **Deploy:**
  - [ ] Deploy to production using CI/CD pipeline (not manual)
  - [ ] Monitor deployment progress and logs
- **Post-Deploy Checklist:**
  - [ ] Verify application loads and critical flows work
  - [ ] Check error monitoring (Sentry, Cloud Error Reporting) for new errors
  - [ ] Verify analytics events still firing correctly
  - [ ] Monitor performance metrics for regressions
  - [ ] Confirm SSL certificates and security headers intact

### Step 4: Validate
- All checklist items completed and documented
- Monitoring shows no anomalies for 30 minutes post-deploy
- Rollback procedure confirmed available if needed
- Deployment logged in team changelog/release notes

## Quality Criteria

- [ ] Pre-deploy checklist completed with no skipped items
- [ ] Rollback plan documented and tested before deployment
- [ ] Post-deploy monitoring active for at least 30 minutes
- [ ] Deployment documented in release notes or changelog
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Deploying on Friday afternoon (reduced monitoring, slower incident response)
- Skipping staging validation ("it works locally")
- No rollback plan ("we'll fix forward" — until you can't)

## Related Skills

- `firebase-deployment` — Firebase-specific deployment procedures
- `github-actions-ci` — automated deployment pipeline execution

## Usage

Example invocations:

- "/deployment-checklist" — Run the full deployment checklist workflow
- "deployment checklist on this project" — Apply to current context


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
