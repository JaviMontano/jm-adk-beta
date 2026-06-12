# firebase — skill overview

Router skill for the **Firebase platform surface**: standing up projects, modeling
Firestore, authoring Security Rules, building Cloud Functions, wiring emulators,
deploying, and cutting cost. It resolves a single `topic` and reads exactly one
playbook from `routes:` so context stays lean.

## What it does
Maps a Firebase task to one of 15 topics and applies the matching playbook with
evidence tags. It does **not** load the whole cluster — one route per invocation.
Scope is Firebase's own surface (Auth, Firestore, Functions, Hosting, Storage,
Extensions, Emulators), not raw GCP IAM/networking.

## When to use
- New Firebase project setup, or redesign of an existing one (`architecture`, `setup`).
- Firestore schema, indexes, query patterns, or Security Rules
  (`firestore-modeling`, `firestore-queries`, `firestore-security-rules`).
- Cloud Functions — HTTP/Firestore/Auth/Storage/scheduled triggers
  (`functions`, `cloud-functions`, `scheduled-functions`).
- Emulator Suite, Hosting, Storage, Extensions, deploys, cost
  (`emulator-setup`, `hosting`, `storage`, `extensions`, `deployment`, `cost-optimization`).

## How it routes / executes
1. Resolve the request to ONE `topic` (enum in `SKILL.md`). Disambiguation rules:
   scheduled jobs → `scheduled-functions`; trigger/HTTP handler code → `functions`;
   schema/collection layout → `firestore-modeling`; index/read pattern →
   `firestore-queries`; access control → `firestore-security-rules`.
2. If two topics still fit, ask once — never load both.
3. Read the single mapped playbook. `depth=deep` applies it exhaustively with a
   verification step at each phase; `depth=quick` covers essentials only.
4. Spine: **Discover → Analyze → Execute → Validate.**

## References (one per invocation)
- `references/architecture.md` — end-to-end topology, C4 diagrams, cost estimate.
- `references/firestore-modeling.md` / `references/firestore-queries.md` — schema + reads.
- `references/firestore-security-rules.md` — `request.auth`, custom claims, deny-by-default.
- `references/functions.md` / `references/cloud-functions.md` / `references/scheduled-functions.md` — triggers, 2nd gen, Node 20.
- `references/auth.md`, `references/hosting.md`, `references/storage.md`, `references/extensions.md`.
- `references/setup.md`, `references/emulator-setup.md`, `references/deployment.md`, `references/cost-optimization.md`.

## Quality gates
Rules tested in the emulator (allow AND deny), deploys dry-run first, cost claims
backed by billing/usage data — never asserted. No prices: FTE-months/usage
estimates with disclaimers only. Single-brand, evidence-tagged output.

## DoD bundle
Role contracts in `agents/`, domain knowledge in `knowledge/`, prompts in
`prompts/`, the deliverable scaffold in `templates/output.md`, eval cases in
`evals/evals.json`, a worked example in `examples/`, and the reusable
quality-gate assets in `assets/` (see `assets/README.md`).
