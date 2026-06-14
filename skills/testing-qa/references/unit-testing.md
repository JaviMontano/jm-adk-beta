<!-- distilled from alfa skills/unit-testing -->
<!-- Jest/Vitest unit testing with Firebase emulator mocking, TDD workflow, and 80%+ coverage enforcement -->
# 079 — Unit Testing {Testing}

## Purpose
Establish deterministic, fast-feedback unit test infrastructure using Jest or Vitest with Firebase service mocking. Enforce TDD red-green-refactor and hold coverage at/above 80% on changed modules. [DOC]

**In scope:** pure functions, hooks, reducers, components rendered with mocked Firebase. **Anti-scope:** real Firestore rules (use the emulator + integration suite), multi-service flows, E2E, performance/load, and visual regression — those belong to sibling references, not here. [INFERENCE] Routing a flow test through this reference is the most common misuse and produces slow, flaky suites.

## Physics — 3 Immutable Laws

1. **Law of Isolation**: Every unit test runs with no network, no live Firestore, no real Auth. All Firebase services are mocked or emulated. [DOC]
2. **Law of Speed**: Full unit suite under 60s; any single test over 5s is a smell — refactor the dependency, do not raise the budget. [DOC]
3. **Law of Determinism**: Same input → same output. No wall-clock, randomness, or test-order coupling. Flaky = quarantined same-day, fixed or deleted within one sprint. [DOC]

## Protocol

### Phase 1 — Setup
1. Select runner: Vitest (Vite projects) or Jest (legacy/CRA). [DOC]
2. Configure `vitest.config.ts` or `jest.config.ts` with `@testing-library/*` and Firebase mock paths. [CONFIG]
3. Create `__mocks__/firebase/` with stubs for `auth`, `firestore`, `functions`, `storage`. [CODE]
4. Set coverage thresholds in config: `{ branches: 80, functions: 80, lines: 80, statements: 80 }`. [CONFIG]

**Decision — Vitest vs Jest.** Default to Vitest on any Vite/ESM project: it reuses the Vite transform (no separate Babel/ts-jest pipeline) and starts faster. Choose Jest only when CRA, a Babel-only toolchain, or a Jest-coupled dependency forces it. Trade-off: Vitest's API is near-drop-in but `vi` ≠ `jest` globals, so a mid-project switch means rewriting mock/timer calls — pick once at setup. [INFERENCE]

### Phase 2 — TDD Execution
1. Write failing test (RED) — assert expected behavior before implementation; confirm it fails for the *right* reason, not a typo/import error. [DOC]
2. Write minimal code to pass (GREEN) — no gold-plating. [DOC]
3. Refactor — extract, rename, simplify while tests stay green. [DOC]
4. Run `vitest --coverage` (or `jest --coverage`) after each cycle. [CONFIG]

### Phase 3 — CI Gate
1. Add test command to `package.json`: `"test:unit": "vitest run --coverage"`. [CONFIG]
2. Fail CI if coverage drops below thresholds. [CONFIG]
3. Publish coverage artifact (lcov + HTML). [DOC]

## I/O

| Input | Output |
|-------|--------|
| Source module (`.ts`/`.tsx`) | `*.test.ts` with ≥3 cases/function (happy, boundary, error) |
| Firebase service dependency | Mock file in `__mocks__/firebase/` |
| Coverage config | `coverage/` report (lcov, HTML) |
| CI pipeline trigger | Pass/fail with coverage delta |

## Worked Example — async hook with mocked Firestore

```ts
// useUserDoc.test.ts  (Vitest)
import { renderHook, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { getDoc } from 'firebase/firestore';
import { useUserDoc } from './useUserDoc';

vi.mock('firebase/firestore'); // resolves to __mocks__/firebase/firestore

it('returns the user doc on success', async () => {           // happy path
  vi.mocked(getDoc).mockResolvedValue({
    exists: () => true, data: () => ({ name: 'Ada' }),
  } as never);
  const { result } = renderHook(() => useUserDoc('u1'));
  await waitFor(() => expect(result.current.data?.name).toBe('Ada'));
});

it('surfaces an error when the doc read rejects', async () => { // error path
  vi.mocked(getDoc).mockRejectedValue(new Error('permission-denied'));
  const { result } = renderHook(() => useUserDoc('u1'));
  await waitFor(() => expect(result.current.error).toMatch(/permission/));
});
```
Note `waitFor` over fixed delays (determinism), `vi.mocked()` for typed mocks (no `any`), and the explicit reject case (branch coverage). [INFERENCE]

## Quality Gates — 5 Checks

1. **Coverage ≥ 80%** on lines, branches, functions, statements — measured on the *diff*, not whole repo, so legacy gaps don't mask new misses. [CONFIG]
2. **Zero flaky tests** — run suite 3× in CI; all pass. [CONFIG]
3. **No `any` in test files** — TypeScript strict applies to tests; use `vi.mocked()`/typed fixtures. [DOC]
4. **One assertion concept per test** — multiple `expect`s are fine if they verify one behavior; split when they verify different ones. [DOC]
5. **Mock accuracy** — mocks mirror real Firebase SDK signatures (type-checked against installed `firebase` version). [DOC]

## Edge Cases

- **Firestore Timestamps**: freeze `Timestamp.now()` via `vi.useFakeTimers()`; restore in `afterEach` to avoid leaking fake time. [DOC]
- **Auth state changes**: `onAuthStateChanged` mock emitting a controlled sequence; assert unsubscribe is called on unmount (listener-leak guard). [DOC]
- **Cloud Functions callable**: mock `httpsCallable` with typed `{ data: T }` responses; cover the error/`HttpsError` branch. [DOC]
- **Environment variables**: `vi.stubEnv()` — never read real `.env`; restore with `vi.unstubAllEnvs()`. [DOC]
- **Optimistic / racing updates**: assert intermediate AND settled state, or the race window goes untested. [INFERENCE]

## Failure Modes — symptom → cause → fix

- Passes locally, fails in CI → hidden order/time/locale dependency → enforce randomized order; freeze time, locale, TZ. [INFERENCE]
- Green tests, real bug ships → mock drifted from SDK or asserted the mock, not behavior → regenerate mocks from SDK types; assert outputs. [INFERENCE]
- Coverage high, confidence low → tests exercise lines without meaningful assertions → spot-check via mutation testing on critical modules. [INFERENCE]
- Suite slows over time → unmocked I/O or growing `beforeEach` setup → profile, isolate the slow dependency (Law of Speed). [INFERENCE]

## Self-Correction Triggers

- Coverage drops below 80% on the diff → block merge, notify author. [DOC]
- Suite exceeds 60s → profile and split slow suites. [DOC]
- Snapshot tests exceed 20% of suite → convert to explicit assertions. [DOC]
- Mock drift detected (SDK update) → regenerate mocks from SDK types. [DOC]

## Usage

Example invocations:

- "/unit-testing" — Run the full unit testing workflow
- "unit testing on this project" — Apply to current context

## Acceptance Criteria

- Suite runs offline (no network/live Firebase) and passes 3× consecutively. [DOC]
- Diff coverage ≥ 80% across all four metrics; CI fails otherwise. [CONFIG]
- Every public function has happy + boundary + error cases; no `any`. [DOC]
- Full unit suite completes < 60s; no single test > 5s. [DOC]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [DOC]
- Verify step for the above: run `vitest run` at repo root; if it cannot resolve config/mocks, the assumption fails. [SUPUESTO]
- English-language output unless otherwise specified. [DOC]
- Does not replace integration/E2E coverage or domain-expert judgment for final decisions. [DOC]
