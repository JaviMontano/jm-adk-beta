<!-- distilled from alfa skills/firebase-setup -->
<!-- > -->
# Firebase Setup

## TL;DR

Initializes a Firebase project end to end — `firebase init`, emulator suite, per-environment config, and dev/staging/prod aliases. Use when starting a new project or restructuring an existing one for multiple environments. [EXPLICIT]

## Scope

- IN: CLI init, `firebase.json`/`.firebaserc` structure, emulator suite, env strategy, project aliases, data export/import, gitignore hygiene. [EXPLICIT]
- OUT (defer to listed skill): data modeling (`firestore-modeling`), Functions logic (`cloud-functions`), CI/CD pipelines, security-rules authoring beyond a starter file, Terraform/IaC provisioning of GCP resources. [EXPLICIT]

## Procedure

### Step 1: Discover
- Confirm CLI installed and authenticated: `firebase --version`, `firebase login:list`. [CONFIG]
- Identify required services (Firestore, Auth, Functions, Hosting, Storage).
- Determine environment strategy: one GCP project per environment is the default. [EXPLICIT]
- If migrating, read existing `firebase.json` and `.firebaserc` before changing anything (read-before-write). [EXPLICIT]

### Step 2: Analyze
- Plan layout: monorepo vs separate repos for functions/hosting (see Decisions).
- Scope emulator set to services actually used — extra emulators slow startup. [INFERENCE]
- Design env-var strategy (`.env.local`, `.env.<project>`, runtime config; see Failure Modes for the `functions.config()` deprecation).
- Confirm billing: Functions, Extensions, and outbound network require the **Blaze** plan; Spark cannot deploy Functions. [DOC]

### Step 3: Execute
- `firebase init`, selecting required services.
- Configure aliases in `.firebaserc` (dev, staging, prod) — see worked example.
- Pin emulator ports in `firebase.json` so ports are stable across machines/CI. [CONFIG]
- Create `.env` files per environment with Firebase config values; never commit them.
- Add `firestore.rules` + `firestore.indexes.json`.
- Set up Functions with TypeScript, ESLint, and `package.json` scripts.
- Add emulator data export/import scripts for reproducible dev data:
  `firebase emulators:export ./emulator-data` and
  `firebase emulators:start --import=./emulator-data --export-on-exit`. [CONFIG]

### Step 4: Validate
- `firebase emulators:start` — all selected services bind and report ports. [EXPLICIT]
- Project switching works: `firebase use dev`, `firebase use prod`.
- Env vars resolve per environment (print one non-secret value to confirm wiring).
- `.gitignore` excludes `.env*`, `*serviceAccount*.json`, `emulator-data/` (unless seed is intentionally committed). [CONFIG]

## Decisions & Trade-offs

| Decision | Choose | Trade-off |
|----------|--------|-----------|
| One project per env vs shared project + prefixes | One project per env | Hard isolation of data/quota/billing; cost is more projects to administer. Prefixes leak prod blast radius into dev. [EXPLICIT] |
| Monorepo vs split repos | Monorepo for ≤2 deployables | Single install/CI graph; splits help only when teams or release cadences diverge. [INFERENCE] |
| Fixed vs default emulator ports | Fixed | Stable URLs for app config + CI; must avoid local port collisions. [CONFIG] |
| Commit emulator seed data | Only small, non-PII fixtures | Reproducible onboarding; large exports bloat the repo and drift. [INFERENCE] |

## Acceptance Criteria

- [ ] All required services initialized and present in `firebase.json`. [EXPLICIT]
- [ ] Emulator suite starts cleanly on fixed ports with seed data importing. [EXPLICIT]
- [ ] Aliases resolve for dev/staging/prod and map to distinct GCP project IDs. [EXPLICIT]
- [ ] No secret (`.env*`, service-account key) is tracked by git: `git ls-files | grep -Ei 'serviceaccount|\.env'` returns nothing. [CONFIG]
- [ ] Blaze confirmed before any Functions deploy attempt. [DOC]
- [ ] Every non-trivial claim carries an evidence tag. [EXPLICIT]

## Worked Example: `.firebaserc`

```json
{
  "projects": {
    "default": "myapp-dev",
    "dev": "myapp-dev",
    "staging": "myapp-staging",
    "prod": "myapp-prod"
  }
}
```

`firebase use staging` then targets `myapp-staging` for `deploy`, `firestore:*`, etc. [CONFIG]

## Worked Example: emulator block in `firebase.json`

```json
{
  "emulators": {
    "auth":      { "port": 9099 },
    "firestore": { "port": 8080 },
    "functions": { "port": 5001 },
    "storage":   { "port": 9199 },
    "ui":        { "enabled": true, "port": 4000 }
  }
}
```

## Anti-Patterns

- Sharing one Firebase project across dev and prod. [EXPLICIT]
- Hardcoding Firebase config instead of env vars.
- Skipping emulators and testing directly against production data.
- Committing service-account JSON or `.env` files.
- Deploying Functions on the Spark plan and reading the failure as a code bug. [DOC]

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Error: Your project must be on the Blaze plan` | Functions/Extensions on Spark | Upgrade billing, then redeploy. [DOC] |
| Emulator "port taken" / address in use | Default port collision with another process | Set fixed ports; free the port or change it. [CONFIG] |
| App connects to prod from local dev | Emulator host/env vars not wired | Set `FIRESTORE_EMULATOR_HOST` / SDK `connect*Emulator` for local runs. [INFERENCE] |
| `firebase deploy` hits the wrong env | Active alias not switched | `firebase use <env>` before deploy; verify with `firebase use`. [CONFIG] |
| Env values undefined at runtime | Wrong `.env` loaded / file untracked and absent on the machine | Confirm filename matches the active env and the file exists locally. [INFERENCE] |
| `functions.config()` empty/deprecated | Legacy runtime config removed in current tooling | Migrate to `.env` / `defineSecret` params. [DOC] |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to the appropriate skill (see Scope) or escalate. |
| Existing `firebase.json` present | Read and diff before overwriting; preserve unknown keys. [EXPLICIT] |
| No billing access for Blaze | Stop at emulator-only setup; flag the Functions/Extensions blocker. [DOC] |

## Assumptions & Limits

- Assumes Firebase CLI installed, an authenticated account, and access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes English-language output unless otherwise specified. [EXPLICIT]
- Does not provision GCP resources via IaC, author production security rules, or replace domain-expert judgment for final decisions. [EXPLICIT]

## Related Skills

- `firestore-modeling` — data modeling follows project setup.
- `cloud-functions` — Functions initialization is part of Firebase setup.

## Usage

- "/firebase-setup" — run the full firebase setup workflow.
- "firebase setup on this project" — apply to current context.
