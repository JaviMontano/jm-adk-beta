<!-- distilled from alfa skills/environment-management -->
<!-- Dev/staging/prod Firebase project separation, environment variables, .env files, and CLI project aliases -->
# 091 — Environment Management {DevOps}

## Purpose
Maintain strict separation between development, staging, and production environments. Prevent cross-environment data contamination through Firebase project isolation, environment variables, and CLI aliases. [EXPLICIT]

## Scope & Anti-Scope
- **In scope**: Firebase project topology, `.env` strategy, `.firebaserc` aliases, CI environment selection, secret hygiene. [EXPLICIT]
- **Out of scope**: Secret-manager rotation policy, runtime feature flags, blue/green or canary traffic-splitting (see `rollback-strategy.md`), multi-region replication. [INFERENCIA]
- **Assumes**: a Vite or CRA client + Firebase Functions v2 backend, GitHub Actions CI, one repo per app. Multi-app monorepos need per-app `.firebaserc` targets. [SUPUESTO]

## Physics — 3 Immutable Laws
1. **Law of Isolation**: Each environment (dev/staging/prod) maps to a separate Firebase project. No shared Firestore, Auth, or Storage across environments. [EXPLICIT]
2. **Law of Configuration Over Code**: Environment-specific values live in `.env` files and Firebase project config — never hardcoded in source. [EXPLICIT]
3. **Law of Least Privilege**: Developers get owner on dev, viewer on staging, no direct prod access (CI-only deploys via a service account). [EXPLICIT]

## Protocol

### Phase 1 — Firebase Project Setup
1. Create 3 Firebase projects: `myapp-dev`, `myapp-staging`, `myapp-prod`. [EXPLICIT]
2. Configure `.firebaserc` aliases: `{ "projects": { "dev": "myapp-dev", "staging": "myapp-staging", "prod": "myapp-prod" } }`. [CONFIG]
3. Switch: `firebase use dev` / `firebase use staging` / `firebase use prod`. [EXPLICIT]
4. **Trade-off — 3 projects vs 1 project + Firestore prefixes**: chose separate projects. Cost: 3× setup, 3× quota config. Benefit: hard isolation — a fat-fingered `prod` deploy cannot touch dev data, and IAM is enforced by Google, not by app code. Prefix-in-one-project saves setup but leaks across the same Auth/Storage bucket and shares quota. [INFERENCIA]

### Phase 2 — Environment Variables
1. Create `.env.development`, `.env.staging`, `.env.production`. [EXPLICIT]
2. Prefix client-exposed vars with `VITE_` (Vite) or `REACT_APP_` (CRA). Unprefixed vars are NOT bundled and are `undefined` in the browser. [EXPLICIT]
3. Firebase config vars: `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_PROJECT_ID`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_APP_ID`. [CODE]
4. Add `.env*` to `.gitignore`; commit `.env.example` with placeholder values only. [EXPLICIT]
5. **Note — client keys are public**: `VITE_FIREBASE_API_KEY` ships to the browser by design; it is an identifier, not a secret. Real protection is Firebase Security Rules + App Check, never key secrecy. Server secrets (Stripe, service-account JSON) must stay server-only and never carry a `VITE_`/`REACT_APP_` prefix. [INFERENCIA]

### Phase 3 — CI Environment Selection
1. GitHub Actions uses per-environment secrets (GitHub Environments: `dev`/`staging`/`prod`), gating prod behind required reviewers. [CONFIG]
2. Branch mapping: `develop` → dev, `staging` → staging, `main` → prod. [EXPLICIT]
3. Deploy with explicit alias: `firebase deploy --only hosting -P staging`. Always pass `-P`; never rely on the last `firebase use`. [EXPLICIT]
4. Functions config: Firebase Functions v2 reads `.env` / `.env.<project-id>` in `functions/`; `functions:config:set` is legacy (v1) and deprecated. [DOC]
5. Authenticate CI with `GOOGLE_APPLICATION_CREDENTIALS` (service-account JSON in a secret) or `firebase deploy --token` — never a personal login. [CONFIG]

## I/O

| Input | Output |
|-------|--------|
| Environment name (dev/staging/prod) | Correct Firebase project + config |
| `.env.<mode>` file | Environment-specific vars loaded at build |
| `.firebaserc` aliases | CLI targets the correct project |
| CI branch name | Automatic environment selection |
| Service-account secret | Non-interactive CI deploy auth |

## Worked Example — promote a build dev → staging
```bash
git checkout staging && git merge --no-ff develop   # branch mapping → staging env
firebase use staging                                 # local sanity check
firebase deploy --only hosting,functions -P staging  # -P overrides any prior `use`
# CI (.github/workflows): push to `staging` triggers job using the `staging`
# GitHub Environment secrets; VITE_* injected at build from staging values.
```
Expected: `myapp-staging` updated; `myapp-dev` and `myapp-prod` untouched; build embeds staging `VITE_FIREBASE_PROJECT_ID`. [INFERENCIA]

## Acceptance Criteria — measurable
1. `firebase projects:list` shows 3 distinct project IDs; `.firebaserc` aliases all resolve. [EXPLICIT]
2. `grep VITE_FIREBASE_PROJECT_ID .env.development .env.production` returns **different** IDs. [EXPLICIT]
3. `git check-ignore .env.development` exits 0 (ignored); `.env.example` IS tracked and contains zero real values. [EXPLICIT]
4. No secret value is duplicated across two GitHub Environments (no shared secrets). [EXPLICIT]
5. A `main`-branch push deploys only to `myapp-prod`; dev/staging projects show no new deploy in their console history. [INFERENCIA]
6. No source file outside `.env*` contains a literal Firebase project ID or API key (`grep -r "myapp-prod" src/` is empty). [SUPUESTO]

## Edge Cases & Failure Modes
- **Functions env**: v2 auto-loads `functions/.env` and `functions/.env.<project-id>`; the project-specific file wins on key collision. [DOC]
- **Emulator override**: when `FIREBASE_EMULATOR=true`, bypass all env config and connect to localhost — guard so it can NEVER evaluate true in a prod build. [EXPLICIT]
- **Third-party services**: Stripe, SendGrid, etc. need separate test/prod keys per environment; a test Stripe key in prod silently drops live charges. [INFERENCIA]
- **Database migrations**: schema changes flow dev → staging → prod, never skip a stage. [EXPLICIT]
- **`.env.local` shadowing**: Vite loads `.env.local` last and it overrides `.env.<mode>`; a stale `.env.local` makes a dev point at prod with no visible error. [INFERENCIA]
- **Build-time vs deploy-time mismatch**: `VITE_*` is baked at `vite build`. Building with dev vars then deploying with `-P prod` ships dev config to prod. Build inside the same CI job that sets the target. [INFERENCIA]
- **Wrong active alias**: a forgotten `firebase use prod` makes a later aliasless `deploy` hit prod. Mitigation: every deploy passes `-P`; CI never calls bare `firebase use`. [INFERENCIA]
- **Leaked secret**: if a real value lands in `.env.example` or git history, rotate the key — `.gitignore` does not untrack already-committed files. [SUPUESTO]

## Self-Correction Triggers
- Dev data appears in staging/prod → audit Firebase project IDs in every `.env` and CI secret. [EXPLICIT]
- Deploy hit the wrong environment → verify `.firebaserc` alias, the `-P` flag, and CI branch mapping. [EXPLICIT]
- Missing env var at runtime → check `.env.example` completeness and CI secret configuration. [EXPLICIT]
- Developer obtained prod access → revoke, enforce CI-only deploy via service account. [EXPLICIT]
- `undefined` client config → confirm the var carries the `VITE_`/`REACT_APP_` prefix. [INFERENCIA]

## Usage
- "/environment-management" — Run the full environment management workflow.
- "environment management on this project" — Apply to current context.

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- Firebase-specific: AWS Amplify / Vercel / Cloudflare have analogous but distinct project-isolation models not covered here. [SUPUESTO]
