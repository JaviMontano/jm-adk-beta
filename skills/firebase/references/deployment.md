<!-- distilled from alfa skills/firebase-deployment -->
<!-- > -->
# Firebase Deployment

> "Deploy with confidence — preview before you promote, rollback before you panic." — Unknown

## TL;DR

Guides Firebase deployment — Hosting, Functions, Firestore/Storage rules and indexes — using preview channels, selective deploys, rollback, and multi-site/multi-env management. Use when shipping a Firebase project to staging or production. [EXPLICIT]

## Scope & Anti-Scope

- IN: `firebase deploy` surfaces (hosting, functions, firestore, storage, hosting channels), CI/CD wiring, rollback. [DOC]
- OUT: writing app code, designing security rules logic, GCP IAM/billing setup, custom-domain DNS provisioning, App Hosting/Cloud Run backends (different lifecycle). [SUPUESTO] → confirm target surface before running.

## Procedure

### Step 1: Discover
- Read deploy targets in `firebase.json` (rewrites, predeploy hooks) and aliases in `.firebaserc`. [CONFIG]
- List services needing deploy: Hosting, Functions, Firestore rules+indexes, Storage rules. [DOC]
- Record the current live version/release per service for rollback identification. [INFERENCIA]
- Check existing CI/CD (GitHub Actions, Cloud Build) so you don't double-deploy. [SUPUESTO]
- Confirm Node runtime in `functions/package.json` matches a supported Functions runtime; mismatch fails deploy. [CONFIG]

### Step 2: Analyze
- Order: rules + indexes → functions → hosting. Rationale: hosting/functions may read new rules or query new indexes; deploying hosting first risks runtime errors against stale backend. [INFERENCIA]
- Design a preview-channel flow for PR review; channels are isolated, auto-expire, and don't touch live. [DOC]
- Plan selective scope: `--only hosting`, `--only functions:fnName`, `--only firestore:rules`. [DOC]
- Define rollback per surface (see table) — they differ; one command does not cover all. [INFERENCIA]

### Step 3: Execute
- Preview first: `firebase hosting:channel:deploy staging --expires 7d`. [DOC]
- Rules + indexes: `firebase deploy --only firestore` (rules and `firestore.indexes.json` together). [DOC]
- Specific function: `firebase deploy --only functions:functionName`. [DOC]
- Hosting: `firebase deploy --only hosting`. [DOC]
- Multi-env: pass `--project staging|prod` (or `firebase use <alias>`); never rely on the default project for prod. [CONFIG]
- Automate deploy-on-merge with GitHub Actions; tag releases in Git for traceability. [DOC]
- Notify on deploy (Slack/email) via CI step or `--message` on channel deploys. [SUPUESTO]

### Step 4: Validate
- Open the preview URL and smoke-test before promoting: `firebase hosting:clone staging:live`. [DOC]
- Tail post-deploy logs: `firebase functions:log` — watch for cold-start/import errors. [DOC]
- Test rules in the Emulator/simulator before trusting a rules deploy; a permissive rule ships silently. [INFERENCIA]
- Confirm rollback actually works in staging: `firebase hosting:rollback`. [DOC]

## Worked Example (PR → prod)

```bash
firebase use staging
firebase hosting:channel:deploy pr-142 --expires 3d   # isolated preview
# review the printed channel URL, run smoke tests
firebase deploy --only firestore --project prod        # rules + indexes first
firebase deploy --only functions --project prod        # then functions
firebase deploy --only hosting --project prod          # finally hosting
git tag -a deploy-2026-06-11 -m "prod release" && git push --tags
```
If validation fails after the hosting step: `firebase hosting:rollback --project prod`, then redeploy the prior functions release. [INFERENCIA]

## Rollback Matrix

| Surface | Rollback method | Note |
|---|---|---|
| Hosting | `firebase hosting:rollback` or re-release prior version in console | Instant; previous releases retained. [DOC] |
| Functions | Redeploy the previous code (Git tag/commit); no built-in version revert | Keep tags so you can `git checkout` the last-good source. [INFERENCIA] |
| Firestore/Storage rules | Redeploy prior `*.rules` from Git | No automatic history via CLI; Git is the source of truth. [SUPUESTO] |
| Firestore indexes | Re-apply prior `firestore.indexes.json` | Index builds are async — a "rollback" delete can take minutes. [INFERENCIA] |

## Quality Criteria

- [ ] Preview channel smoke-tested before promotion. [DOC]
- [ ] `--only` used so unchanged services aren't redeployed. [DOC]
- [ ] Rollback documented AND tested in staging. [INFERENCIA]
- [ ] Deploy automated via CI/CD, not manual `firebase deploy` from a laptop. [DOC]
- [ ] Correct `--project`/alias targeted; prod deploy is explicit, never default. [CONFIG]
- [ ] Every claim carries one evidence tag from a single family. [DOC]

## Anti-Patterns

- Bare `firebase deploy` with no `--only` — redeploys everything, churns unchanged functions and risks unintended changes. [INFERENCIA]
- Shipping to prod with no preview/staging gate. [DOC]
- Hosting-first ordering, leaving the frontend pointed at stale rules/functions/indexes. [INFERENCIA]
- Untagged deploys in Git — rollback target becomes guesswork. [DOC]
- Assuming Functions has console "revert"; it does not — only Hosting does. [SUPUESTO]

## Failure Modes

| Symptom | Likely cause | Action |
|---|---|---|
| Deploy hangs/timeouts | Functions build or large bundle | Check `firebase deploy --debug`; split with `--only functions:fn`. [INFERENCIA] |
| `Missing required index` post-deploy | Indexes not deployed before queries | Deploy `--only firestore:indexes`, wait for build to finish. [DOC] |
| Rules deploy "succeeds" but access breaks | Permissive/wrong rule shipped untested | Roll back rules from Git; gate via Emulator next time. [INFERENCIA] |
| Functions error after deploy | Runtime/env mismatch | Verify Node runtime + `functions:config`/secrets; tail `functions:log`. [CONFIG] |
| Wrong environment deployed | Default project used | Always pass `--project` or `firebase use <alias>`. [CONFIG] |

## Related Skills

- `firebase-hosting` — hosting config that deployment pushes.
- `github-actions-ci` — CI/CD pipeline for automated Firebase deployment.

## Usage

Example invocations:

- "/firebase-deployment" — Run the full firebase deployment workflow.
- "firebase deployment on this project" — Apply to current context.

## Assumptions & Limits

- Assumes Firebase CLI authenticated and project artifacts (code, configs) accessible. [EXPLICIT]
- Assumes `firebase.json`/`.firebaserc` define the targets and aliases used. [CONFIG]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final go/no-go. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to appropriate skill or escalate. |
| No `.firebaserc` aliases | Stop; require explicit `--project` per deploy. [SUPUESTO] |
| Multi-site hosting | Use `target:apply hosting <target> <site>`, then `deploy --only hosting:<target>`. [DOC] |
