<!-- distilled from alfa skills/firebase-functions -->
<!-- Cloud Functions development. HTTP, Firestore, Auth, Storage, scheduled triggers. 2nd gen functions. Node.js 20. [EXPLICIT] -->
# firebase-functions {Backend} (v1.1)
> **"Firebase Functions are your backend. Design them like microservices, deploy them like magic."**
## Purpose
Cloud Functions development. HTTP, Firestore, Auth, Storage, scheduled triggers. 2nd gen functions. Node.js 20. [EXPLICIT]
**When to use:** Backend development within Firebase/Google ecosystem. [EXPLICIT]
**When NOT to use (anti-scope):** Long-running jobs >540s (use Cloud Run), stateful/WebSocket servers, multi-cloud orchestration, or sub-100ms latency-critical paths. [INFERENCE]
## Core Principles
1. **Law of Functions:** Each Cloud Function does ONE thing. Single responsibility. [EXPLICIT]
2. **Law of Cold Start:** Minimize dependencies. Use lazy imports. Set `minInstances` for critical functions. [EXPLICIT]
3. **Law of Security:** Every HTTP function verifies Firebase ID tokens. No public endpoints without auth. [EXPLICIT]
4. **Law of Idempotency:** Background triggers fire AT-LEAST-once and may retry. Every handler must be safe to run twice (dedupe by `event.id`). [INFERENCE]
## Core Process
### Phase 1: Design
1. Map requirements to Cloud Functions triggers (HTTP, Firestore, Auth, Storage, scheduled). [EXPLICIT]
2. Define input/output contracts for each function. [EXPLICIT]
3. Design error handling and retry strategy (retryable vs. terminal). [EXPLICIT]
### Phase 2: Implement
1. Create function with proper trigger type. [EXPLICIT]
2. Add auth middleware for HTTP functions. [EXPLICIT]
3. Implement business logic with error handling. [EXPLICIT]
4. Add Cloud Logging for observability (structured JSON, no PII). [EXPLICIT]
### Phase 3: Test + Deploy
1. Test with Firebase Emulator Suite. [EXPLICIT]
2. Deploy with `firebase deploy --only functions`. [EXPLICIT]
3. Verify in Firebase Console. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements | Text/Spec | Yes | What the function does |
| Trigger type | Enum | Yes | http / firestore / auth / storage / scheduled [INFERENCE] |
| Auth model | Enum | If HTTP | ID-token, App Check, or callable [INFERENCE] |

| Output | Type | Description |
|--------|------|-------------|
| Cloud Function code | TypeScript | Deployable 2nd-gen function |
| Region + runtime opts | Config | region, memory, timeoutSeconds, minInstances [INFERENCE] |
## Trigger → Pattern Decisions
| Trigger | Use when | Trade-off [INFERENCE] |
|---------|----------|-----------|
| `onRequest` (HTTP) | Public/webhook APIs | You own auth + CORS; most control |
| `onCall` (callable) | First-party app clients | Auth + App Check auto-wired; SDK-only callers |
| Firestore `onDocumentWritten` | React to data changes | At-least-once; needs idempotency |
| `onSchedule` (cron) | Periodic jobs | Cold start each run; keep <9 min |
| Storage `onObjectFinalized` | Process uploads | Fires on every finalize incl. overwrites |
## Worked Example (callable, idempotent)
```ts
import { onCall, HttpsError } from "firebase-functions/v2/https";
export const award = onCall(
  { region: "us-central1", minInstances: 0, enforceAppCheck: true },
  async (req) => {
    if (!req.auth) throw new HttpsError("unauthenticated", "Sign in required");
    const { txnId } = req.data ?? {};
    if (!txnId) throw new HttpsError("invalid-argument", "txnId required");
    // idempotency: dedupe on txnId before mutating
    return { ok: true, txnId };
  }
);
```
`HttpsError` codes map to client-readable errors; never leak stack traces to callers. [INFERENCE]
## Validation Gate
- [ ] Single responsibility per function [EXPLICIT]
- [ ] Auth middleware on HTTP endpoints (`verifyIdToken` / `enforceAppCheck`) [EXPLICIT]
- [ ] Error handling with Cloud Logging [EXPLICIT]
- [ ] Background handlers idempotent (dedupe by event id) [INFERENCE]
- [ ] Secrets via `defineSecret`/Secret Manager, never hardcoded [INFERENCE]
- [ ] Emulator tests pass [EXPLICIT]
- [ ] No AWS/Azure services (R-002) [EXPLICIT]
## 5. Self-Correction Triggers
> [!WARNING]
> IF function has no auth middleware THEN add verifyIdToken / enforceAppCheck check. [EXPLICIT]
> IF function imports 10+ dependencies THEN split or lazy-load to reduce cold start. [EXPLICIT]
> IF a background handler mutates state THEN make it idempotent before deploy. [INFERENCE]
> IF a secret appears inline THEN move it to Secret Manager and redeploy. [INFERENCE]

## Failure Modes
| Symptom | Likely cause | Fix [INFERENCE] |
|---------|--------------|-----|
| Slow first call | Cold start | `minInstances>=1`; lazy-load heavy deps |
| Duplicate side effects | At-least-once retry | Dedupe by `event.id`; idempotent writes |
| Deploy fails on secrets | Missing grant | `firebase functions:secrets:set`; bind `secrets:[...]` |
| 403 on callable | Missing/expired App Check token | Verify client App Check; check `enforceAppCheck` |
| Timeout at 60s | Default cap | Raise `timeoutSeconds` (≤540); offload to Cloud Run if larger |
| Runaway cost | Unbounded retries / hot trigger | Set `maxInstances`; cap retry; add circuit breaker |

## Usage

Example invocations:

- "/firebase-functions" — Run the full firebase functions workflow
- "firebase functions on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes 2nd-gen functions, Node.js 20 runtime. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Max execution 540s; payload/response limits per Cloud Functions quotas apply. [INFERENCE]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| Trigger fires twice | Idempotent handler absorbs the retry safely [INFERENCE] |
| Cold start on critical path | Pin `minInstances`; document the cost trade-off [INFERENCE] |
