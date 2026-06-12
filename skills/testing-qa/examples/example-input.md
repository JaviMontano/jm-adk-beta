# Example Input — testing-qa

## Request
"Our React checkout SPA uses Firebase auth + Firestore. The `login → add card →
place order` journey keeps breaking in production but our unit tests are green.
Give me a Playwright e2e test for that journey, run against the emulator, with a
CI gate that blocks merges on failure. Depth: deep."

## Parameters
- `topic`: not supplied (must be inferred)
- `depth`: `deep`

## Context the router can use
- Stack: React SPA, Firebase Auth + Firestore, existing Vitest unit suite (green).
- Symptom: a multi-service *user journey* fails in prod despite green units.
- Constraint: tests must run against the Firebase emulator, headless in CI.
- No load/latency concern stated; this is functional journey coverage.
