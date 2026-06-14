<!-- distilled from alfa skills/cloud-functions -->
<!-- > -->
# Cloud Functions

> "Serverless means someone else worries about the server — but you still worry about the code." — Unknown

## TL;DR

Guides Cloud Functions for Firebase development — HTTP endpoints, Firestore document triggers, Auth event handlers, Storage upload triggers, and PubSub messaging. Covers TypeScript patterns, error handling, cold start optimization, and deployment strategies. Use when you need server-side logic in a Firebase project. [EXPLICIT]

Default to `firebase-functions/v2`; v1 only for triggers v2 lacks (e.g. `auth.user().onCreate` — v2 has no native Auth-create trigger, use blocking functions `beforeUserCreated` or an Identity Platform path instead). [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify server-side logic needs (data validation, aggregation, notifications, integrations)
- Check existing functions, trigger types, runtime version, and per-function region/memory/concurrency
- Review runtime config and secrets (`firebase functions:secrets:access`); note any legacy `functions.config()` (deprecated, removed after Mar 2026 — migrate to `defineSecret`/params) [EXPLICIT]

### Step 2: Analyze
- Categorize by trigger: HTTP (`onCall`/`onRequest`), Firestore (`onDocument{Created,Updated,Deleted,Written}`), Storage (`onObjectFinalized`), Scheduled (`onSchedule`), PubSub (`onMessagePublished`)
- Plan organization: feature folders + `index.ts` barrel; use codebases in `firebase.json` to split large function sets
- Map cold-start budget and idempotency strategy per trigger (see Failure Modes)

### Step 3: Execute
- Scaffold with TypeScript + `firebase-functions/v2`; set runtime to a maintained Node LTS (e.g. nodejs20) [EXPLICIT]
- `onCall` for authenticated client RPC (SDK injects/validates the Firebase ID token — no manual header parsing); `onRequest` only for webhooks/public HTTP or non-Firebase callers
- Firestore triggers for denormalization/aggregation; Storage triggers for thumbnail/scan pipelines
- User-profile init on sign-up: blocking `beforeUserCreated` (v2) or a v1 Auth trigger — not a plain `onCall` the client may skip [EXPLICIT]
- `onSchedule` (cron syntax) for periodic jobs; set `timeZone` explicitly to avoid UTC drift
- Errors: throw `HttpsError(code, msg)` in callables (only its `code`/`message`/`details` reach the client; everything else is scrubbed to `INTERNAL`); for background triggers make handlers idempotent + rely on at-least-once retries
- `defineSecret`/`defineString` params for config; bind secrets per-function so deploy injects them at runtime
- Pin region(s) near users/data; minimize cross-region Firestore round-trips

### Step 4: Validate
- Run the Emulator Suite (Functions + Firestore/Auth/Storage) before deploy; seed and replay trigger events
- Prove idempotency: fire the same event twice, assert one net effect
- Deploy granularly: `firebase deploy --only functions:fnName`; check Cloud Logging + error rate after rollout
- Confirm secrets resolve and cold-start latency is within budget in staging

## Quality Criteria

- [ ] All functions use TypeScript with strict typing
- [ ] `onCall` validates `request.auth` and input shape; rejects with typed `HttpsError`
- [ ] Background triggers are idempotent (safe to re-execute under at-least-once delivery)
- [ ] Secrets via `defineSecret`/params, never hardcoded or in `functions.config()`
- [ ] Region, memory, `timeoutSeconds`, and concurrency set intentionally per function
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- `onRequest` for authenticated endpoints (manual token parsing) instead of `onCall`
- Heavy init inside the handler body instead of module scope / lazy singletons (re-pays on every cold start)
- Recursive trigger: `onDocumentWritten` that writes the same collection without a guard → infinite loop + billing blowout
- Unbounded fan-out: a single trigger spawning thousands of writes with no batching or queue
- Deploying all functions when one changed (slow, raises cross-function failure blast radius)
- Returning raw errors from callables (leaks internals; client only honors `HttpsError`)

## Decisions & Trade-offs

| Decision | Choose | Because / Trade-off |
|----------|--------|---------------------|
| Auth client RPC | `onCall` over `onRequest` | Built-in token + App Check verification; trade-off: Firebase-client callers only [EXPLICIT] |
| Config | params/`defineSecret` over `functions.config()` | Typed, deploy-time validated, secrets in Secret Manager; legacy API is removed post-Mar-2026 [EXPLICIT] |
| Cold start | min instances vs scale-to-zero | `minInstances>0` cuts p99 latency but bills idle; reserve for user-facing hot paths only |
| Concurrency (v2) | raise `concurrency` for I/O-bound | Fewer instances, lower cost; trade-off: shared memory/CPU per request — keep handlers stateless |
| Long jobs | PubSub/Tasks queue vs one big function | Decouples + retries independently; trade-off: more moving parts vs 9-min (HTTP) / 60-min (event) ceiling [EXPLICIT] |

## Worked Example

Authenticated callable with input validation, secret binding, and typed errors:

```ts
import { onCall, HttpsError } from "firebase-functions/v2/https";
import { defineSecret } from "firebase-functions/params";

const STRIPE_KEY = defineSecret("STRIPE_KEY");

export const createCharge = onCall(
  { region: "us-central1", secrets: [STRIPE_KEY], enforceAppCheck: true },
  async (request) => {
    if (!request.auth) throw new HttpsError("unauthenticated", "Sign in required.");
    const amount = request.data?.amount;
    if (typeof amount !== "number" || amount <= 0)
      throw new HttpsError("invalid-argument", "amount must be a positive number.");
    // ...use STRIPE_KEY.value(); on failure rethrow as HttpsError("internal", ...)
    return { ok: true };
  }
);
```

Idempotent Firestore trigger (guards against re-delivery and self-trigger loops):

```ts
import { onDocumentCreated } from "firebase-functions/v2/firestore";

export const onOrderCreated = onDocumentCreated("orders/{orderId}", async (event) => {
  const snap = event.data;
  if (!snap || snap.get("aggregated") === true) return; // already processed → no-op
  await snap.ref.parent.parent /* ... */ ;              // do work
  await snap.ref.update({ aggregated: true });          // mark; also breaks the write-loop
});
```

## Related Skills

- `firebase-setup` — Functions are initialized as part of Firebase project setup
- `serverless-patterns` — general serverless patterns apply to Cloud Functions

## Usage

Example invocations:

- "/cloud-functions" — Run the full cloud functions workflow
- "cloud functions on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and a configured Firebase project on the Blaze plan (Functions require billing) [EXPLICIT]
- Assumes `firebase-functions/v2` as default; v1 only where a v2 trigger does not exist [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Anti-scope: does not cover non-Firebase GCP Cloud Run/Functions IaC, VPC connectors, or org-level IAM design [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Need an Auth `onCreate` trigger in v2 | Use blocking `beforeUserCreated`, or v1 Auth trigger — v2 has no native equivalent [EXPLICIT] |
| Trigger writes its own collection | Add a processed-flag guard (see example) to prevent infinite recursion |
| `functions.config()` in legacy code | Migrate to params/`defineSecret`; legacy API removed after Mar 2026 [EXPLICIT] |

## Failure Modes

| Mode | Symptom | Mitigation |
|------|---------|------------|
| Duplicate event delivery | Side effect applied twice (double charge, double count) | Idempotency key / processed-flag; use atomic transactions |
| Cold-start latency spike | p99 jumps after idle | Module-scope init, lazy heavy deps, `minInstances` on hot paths |
| Secret missing at runtime | `undefined` / auth failures only in prod | Bind secret in function options; verify with `secrets:access` in staging |
| Timeout on long job | Function killed mid-work, partial writes | Raise `timeoutSeconds` within ceiling, or offload to a queue with checkpointing |
| Recursive trigger loop | Runaway invocations + cost alert | Guard self-writes; never write the watched path unconditionally |
| Region mismatch | Added cross-region latency to Firestore | Co-locate function region with the database region |
