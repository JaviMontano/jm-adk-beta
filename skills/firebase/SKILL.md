---
name: firebase
description: "Firebase platform: auth, hosting, functions, firestore-adjacent setup, emulators, deploy, cost. Topics: architecture, auth, cloud-functions, cost-optimization, deployment, emulator-setup, extensions, firestore-modeling, firestore-queries, firestore-security-rules, functions, hosting, scheduled-functions, setup, storage."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
