<!-- distilled from alfa skills/firebase-deployment -->
<!-- > -->
# Firebase Deployment

> "Deploy with confidence — preview before you promote, rollback before you panic." — Unknown

## TL;DR

Guides Firebase project deployment — deploying Hosting, Functions, Firestore rules, and Storage rules with preview channels, selective deployments, rollback procedures, and multi-site management. Use when deploying Firebase projects to staging or production environments. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check current deployment targets in `firebase.json` and `.firebaserc`
- Review which services need deployment (Hosting, Functions, Rules, Indexes)
- Identify the current production version for potential rollback
- Check CI/CD pipeline for existing deployment automation

### Step 2: Analyze
- Plan deployment order: rules and indexes first, then functions, then hosting
- Design preview channel workflow for PR-based review deployments
- Evaluate selective deployment needs (`--only hosting`, `--only functions:specificFn`)
- Determine rollback strategy for each service type

### Step 3: Execute
- Deploy to preview channel first: `firebase hosting:channel:deploy staging`
- Deploy Firestore rules and indexes: `firebase deploy --only firestore`
- Deploy specific functions: `firebase deploy --only functions:functionName`
- Deploy Hosting: `firebase deploy --only hosting`
- Use `--project` flag for multi-environment deployments
- Set up GitHub Actions for automated deployment on merge to main
- Tag releases in Git for deployment traceability
- Configure deployment notifications (Slack, email)

### Step 4: Validate
- Verify preview channel deployment before promoting to production
- Check Cloud Functions logs for startup errors after deployment
- Test Firestore rules with the rules simulator after rules deployment
- Confirm rollback procedure works: `firebase hosting:rollback`

## Quality Criteria

- [ ] Preview channel tested before production deployment
- [ ] Selective deployments used (not deploying everything every time)
- [ ] Rollback procedure documented and tested
- [ ] Deployment automated via CI/CD (not manual `firebase deploy`)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Running `firebase deploy` without `--only` flag (deploys everything, including unchanged services)
- Deploying directly to production without preview/staging step
- Not tagging deployments in Git (makes rollback identification difficult)

## Related Skills

- `firebase-hosting` — hosting configuration that deployment pushes
- `github-actions-ci` — CI/CD pipeline for automated Firebase deployment

## Usage

Example invocations:

- "/firebase-deployment" — Run the full firebase deployment workflow
- "firebase deployment on this project" — Apply to current context


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
