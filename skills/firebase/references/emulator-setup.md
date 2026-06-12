<!-- distilled from alfa skills/firebase-emulator-setup -->
<!-- Firebase Emulator Suite configuration for Firestore, Auth, Functions, Storage, and Hosting with seed data -->
# 087 — Firebase Emulator Setup {Testing}

## Purpose
Configure and maintain the Firebase Emulator Suite as the local development and testing backbone. All services (Firestore, Auth, Functions, Storage, Hosting) run locally with reproducible seed data. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Local Parity**: The emulator mirrors production Firebase services. Code that works on emulators works on production — barring quota, scale, and the gaps below. [EXPLICIT]
2. **Law of Zero Cloud Cost**: All dev/testing runs on emulators. No reads/writes/invocations against live Firebase during dev. [EXPLICIT]
3. **Law of Reproducible State**: Emulators boot from exported seed data. Every developer and CI run starts from the same known state. [EXPLICIT]

### Parity gaps (do NOT assume identical) [INFERENCE]
- **Auth**: emulator skips real email/SMS delivery, phone verification, and most OAuth provider round-trips; tokens are unsigned-equivalent. Never test deliverability or real provider consent here.
- **Functions**: cold-start timing, concurrency, and IAM are not faithfully reproduced; scheduled (`pubsub.schedule`) triggers do not fire on a clock — invoke manually.
- **Firestore**: composite-index requirements are NOT enforced by the emulator, so a query that passes locally can fail in prod with `FAILED_PRECONDITION`. Validate indexes separately.
- **Storage/Security Rules**: rules ARE enforced, but signed-URL generation and CORS differ.

## Protocol

### Phase 1 — Configuration
1. `firebase init emulators` — select Firestore, Auth, Functions, Storage, Hosting. [EXPLICIT]
2. Configure non-default ports in `firebase.json` to avoid conflicts: Firestore 8080, Auth 9099, Functions 5001, Storage 9199, Hosting 5000, UI 4000. [EXPLICIT]
3. Add the config under the `"emulators"` key in `firebase.json`. [EXPLICIT]
4. Set the binary download path: `.cache/firebase/emulators/`; add it to `.gitignore` (binaries are large, machine-specific). [EXPLICIT]

### Phase 2 — Seed Data
1. Start emulators; populate manually or via seed script (skill 085). [EXPLICIT]
2. Export: `firebase emulators:export ./test/emulator-data`. [EXPLICIT]
3. Commit `./test/emulator-data/` for reproducibility. [EXPLICIT]
4. Boot with import: `firebase emulators:start --import=./test/emulator-data`. Add `--export-on-exit=./test/emulator-data` only on an opt-in "reseed" command — NOT the default start, or every local run silently mutates committed seed data. [EXPLICIT]

### Phase 3 — Developer Workflow
1. npm script: `"emulators": "firebase emulators:start --import=./test/emulator-data"`. [EXPLICIT]
2. App code wires emulators via `connectFirestoreEmulator()`, `connectAuthEmulator()`, `connectFunctionsEmulator()`, `connectStorageEmulator()`. Call each ONCE, immediately after the SDK instance is created and before any other SDK use, or the connection is ignored. [EXPLICIT]
3. Toggle with env var `FIREBASE_EMULATOR=true`; gate the `connect*` calls behind it. [EXPLICIT]
4. Emulator UI at `localhost:4000` for manual inspection. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| `firebase.json` config | Running emulator instances on configured ports |
| Seed data directory | Pre-populated Firestore, Auth, Storage state |
| App source code | Emulator-connected local development environment |
| CI pipeline | `firebase emulators:exec "<test cmd>"` test execution |

## Worked Example — CI step (GitHub Actions) [INFERENCE]
```yaml
- uses: actions/setup-java@v4
  with: { distribution: temurin, java-version: '17' }
- run: npm ci
- run: firebase emulators:exec --import=./test/emulator-data "npm test"
```
`emulators:exec` starts all emulators, runs the command, and tears down with the command's exit code — the correct primitive for CI (never `emulators:start` in a pipeline; it blocks).

## Quality Gates — 5 Checks

1. **All 5 emulators configured** — Firestore, Auth, Functions, Storage, Hosting. [EXPLICIT]
2. **Seed data committed** — `test/emulator-data/` exists in repo. [EXPLICIT]
3. **App auto-connects** when `FIREBASE_EMULATOR=true`; verify no live host is reachable in dev. [EXPLICIT]
4. **CI uses emulators** — zero live Firebase calls; assert via `emulators:exec`. [EXPLICIT]
5. **Emulator UI accessible** at `localhost:4000`. [EXPLICIT]

### Acceptance criteria (done = all true) [INFERENCE]
- `firebase emulators:start --import=./test/emulator-data` boots all 5 with zero port errors.
- A fresh clone + `npm run emulators` reproduces identical seed state (no manual setup).
- CI run blocks/fails on any attempted live-Firebase egress.

## Edge Cases

- **Java dependency**: Emulators require Java 11+ (17 LTS recommended). CI image must install it (`actions/setup-java`). [EXPLICIT]
- **Port conflicts**: Detect with `lsof -i :8080`; reassign in `firebase.json`. [EXPLICIT]
- **Functions environment**: Provide config via `.env.local` (preferred) or legacy `functions.config()`; emulator does not inherit prod runtime config. [EXPLICIT]
- **Storage rules**: Emulator enforces `storage.rules` — ensure the rules file is referenced in `firebase.json`. [EXPLICIT]
- **Auth users in seed**: exported Auth users carry no passwords for some providers; re-create test credentials in the seed script if sign-in tests need them. [INFERENCE]
- **Monorepo / multiple projects**: pin the project with `--project <id>` or `.firebaserc` so the emulator does not adopt an unintended live project ref. [INFERENCE]

## Anti-Scope (this skill does NOT) [INFERENCE]
- Deploy to live Firebase, manage prod IAM/quotas, or generate production composite indexes.
- Author the seed dataset itself (that is skill 085) or define security-rule logic (separate rules skill).
- Guarantee latency/concurrency fidelity — see Parity gaps.

## Self-Correction Triggers

- Emulator fails to start → check Java version, port conflicts, `firebase.json` syntax. [EXPLICIT]
- Seed data drifts from schema → re-export after each schema migration; treat seed as versioned with the schema. [EXPLICIT]
- `connect*` "ignored / already started" warning → a real call ran before the connect; move connect to immediately after SDK init. [INFERENCE]
- Query passes locally, fails in prod with `FAILED_PRECONDITION` → missing composite index (emulator doesn't enforce); add to `firestore.indexes.json`. [INFERENCE]
- Developer hits live Firebase accidentally → add a dev-mode runtime guard that throws on non-emulator hosts. [EXPLICIT]
- CI emulator timeout → optimize function cold starts; raise the test runner timeout (not `--inspect-functions`, which is a debug flag). [EXPLICIT]

## Usage

Example invocations:

- "/firebase-emulator-setup" — Run the full firebase emulator setup workflow
- "firebase emulator setup on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Assumes Firebase CLI installed and authenticated for the initial `init`/`export`. [INFERENCE]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
