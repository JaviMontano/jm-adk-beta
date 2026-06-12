---
name: firebase
version: 1.0.0
description: "Firebase platform router: auth, hosting, functions, firestore-adjacent setup, emulators, deploy, cost. Topics: architecture, auth, cloud-functions, cost-optimization, deployment, emulator-setup, extensions, firestore-modeling, firestore-queries, firestore-security-rules, functions, hosting, scheduled-functions, setup, storage."
params:
  topic:
    enum: [architecture, auth, cloud-functions, cost-optimization, deployment, emulator-setup, extensions, firestore-modeling, firestore-queries, firestore-security-rules, functions, hosting, scheduled-functions, setup, storage]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  architecture: references/architecture.md
  auth: references/auth.md
  cloud-functions: references/cloud-functions.md
  cost-optimization: references/cost-optimization.md
  deployment: references/deployment.md
  emulator-setup: references/emulator-setup.md
  extensions: references/extensions.md
  firestore-modeling: references/firestore-modeling.md
  firestore-queries: references/firestore-queries.md
  firestore-security-rules: references/firestore-security-rules.md
  functions: references/functions.md
  hosting: references/hosting.md
  scheduled-functions: references/scheduled-functions.md
  setup: references/setup.md
  storage: references/storage.md
---

# firebase

Router skill: resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — one route per invocation keeps context lean. [INFERENCE]

## When to use
Any Firebase/GCP-adjacent task: standing up a project, modeling Firestore,
writing security rules, building Cloud Functions, wiring emulators, deploying,
or cutting cost. NOT for raw GCP IAM/networking outside Firebase's surface. [INFERENCE]

## Inputs / Outputs
- **In**: `topic` (required, one of the 15 enums), `depth` (quick|deep). [CONFIG]
- **Out**: the resolved playbook applied to the user's request, with evidence
  tags per `references/verification-tags.md` (Alfa core EN family in this kit). [DOC]

## Routing
1. Map the request to ONE `topic`. Ambiguity rules: triggers/scheduled jobs →
   `scheduled-functions`; trigger/HTTP handler code → `functions` (alias
   `cloud-functions`); schema/collection layout → `firestore-modeling`; index
   or read pattern → `firestore-queries`; access control → `firestore-security-rules`. [INFERENCE]
2. If still ambiguous between two topics, ask once — do not load both. [INFERENCE]
3. Read the single mapped playbook. `deep` → apply exhaustively with verification
   at each step; `quick` → essentials only.

## Spine
Discover → Analyze → Execute → Validate.

## Quality gates
- Constitution v6.0.0 (enforcement), evidence tags, script-first rule. [DOC]
- Apply the reusable gates in `assets/` (`assets/quality-rubric.json` + `assets/checklist.md`) before "done". [DOC]
- Validate before "done": rules tested in emulator, deploys dry-run first,
  cost claims backed by billing/usage data — never asserted. [DOC]

## Anti-patterns
- Loading multiple route files "to be safe". [INFERENCE]
- Inventing a topic outside the 15-enum set — if none fits, ask. [INFERENCE]
- Quoting prices; emit FTE-months/usage estimates with disclaimers only. [DOC]
- Treating an emulator pass as production-safe without a staging deploy. [INFERENCE]
