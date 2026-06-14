<!-- distilled from alfa skills/firebase-extensions -->
<!-- Configure Firebase Extensions: Stripe payments, SendGrid email, image resize, translation, Algolia search. [EXPLICIT] -->
# firebase-extensions {Backend} (v1.1)
> **"Firebase Functions are your backend. Design them like microservices, deploy them like magic."**

## Purpose
Install/configure Firebase Extensions and the Cloud Functions that back them: Stripe payments (`invertase/firestore-stripe-payments`), SendGrid/Trigger Email, image resize, translation, Algolia search. [EXPLICIT]
**When to use:** Backend work inside the Firebase/Google ecosystem — installing an official extension, or writing a custom function that complements one. [EXPLICIT]
**Anti-scope:** Not for choosing a cloud provider, not for non-Firebase backends, not for client-side SDK wiring (see auth/firestore skills). No AWS/Azure equivalents (R-002). [INFERRED]

## Core Principles
1. **Law of Functions:** Each Cloud Function does ONE thing. Single responsibility. [EXPLICIT]
2. **Law of Cold Start:** Minimize deps; lazy-import heavy SDKs (Stripe, SendGrid) inside the handler; set `minInstances` only for latency-critical, user-facing functions — it bills 24/7. [EXPLICIT]
3. **Law of Security:** Every HTTP function verifies a Firebase ID token. No public endpoints without auth. Extension webhooks (e.g. Stripe) verify the provider signature instead, not an ID token. [EXPLICIT]
4. **Law of Idempotency:** Firestore/Storage/PubSub triggers fire at-least-once. Guard side effects (charges, emails) with an idempotency key or a processed-marker doc. [INFERRED]
5. **Law of Secrets:** Provider keys (Stripe secret, SendGrid API key) live in Secret Manager / extension params, never in source or client. [INFERRED]

## Core Process
### Phase 1: Design
1. Map each requirement to a trigger type: HTTP/callable, Firestore, Auth, Storage, scheduled, or PubSub. [EXPLICIT]
2. Decide **official extension vs. custom function**: prefer an official extension when one covers the need (less code to own); write custom only for logic the extension can't express. [INFERRED]
3. Define input/output contract per function (shape, required fields, error codes). [EXPLICIT]
4. Design error handling, retry policy, and idempotency strategy up front. [EXPLICIT]

### Phase 2: Implement
1. Install extension (`firebase ext:install <publisher/ext>`) or scaffold the function with its trigger type. [EXPLICIT]
2. Add auth middleware (`verifyIdToken`) to HTTP functions; signature verification to webhook handlers. [EXPLICIT]
3. Implement business logic with try/catch and typed errors; mark processed records to stay idempotent. [EXPLICIT]
4. Emit structured Cloud Logging (severity + correlation id) for observability. [EXPLICIT]

### Phase 3: Test + Deploy
1. Test against the Firebase Emulator Suite (functions + Firestore + Auth). [EXPLICIT]
2. Deploy: `firebase deploy --only functions` (or `--only extensions` for installed extensions). [EXPLICIT]
3. Verify in Firebase Console: logs clean, params set, trigger wired. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements | Text/Spec | Yes | What the function/extension does |
| Provider keys | Secret | If 3rd-party | Stripe/SendGrid/Algolia credentials via Secret Manager |
| Trigger source | Enum | Yes | http / firestore / auth / storage / schedule / pubsub |

| Output | Type | Description |
|--------|------|-------------|
| Cloud Function code | TypeScript | Deployable function |
| Extension config | `*.env` / params | Installed-extension parameters |

## Worked Example — Stripe webhook (custom complement)
```ts
import { onRequest } from "firebase-functions/v2/https";
import { defineSecret } from "firebase-functions/params";
const STRIPE_KEY = defineSecret("STRIPE_SECRET");      // Secret Manager, not source [EXPLICIT]
const WH_SECRET  = defineSecret("STRIPE_WH_SECRET");

export const stripeWebhook = onRequest({ secrets: [STRIPE_KEY, WH_SECRET] }, async (req, res) => {
  const Stripe = (await import("stripe")).default;      // lazy import → faster cold start [EXPLICIT]
  const stripe = new Stripe(STRIPE_KEY.value());
  let event;
  try {
    event = stripe.webhooks.constructEvent(            // signature verify, NOT verifyIdToken [EXPLICIT]
      req.rawBody, req.headers["stripe-signature"]!, WH_SECRET.value());
  } catch { res.status(400).send("bad signature"); return; }   // reject unverified [EXPLICIT]
  const ref = db.doc(`events/${event.id}`);
  if ((await ref.get()).exists) { res.sendStatus(200); return; } // idempotency guard [EXPLICIT]
  await ref.set({ type: event.type, at: Date.now() });
  res.sendStatus(200);                                  // ack fast; offload heavy work [EXPLICIT]
});
```

## Validation Gate
- [ ] Single responsibility per function [EXPLICIT]
- [ ] Auth middleware on HTTP endpoints; signature verify on webhooks [EXPLICIT]
- [ ] Error handling with structured Cloud Logging [EXPLICIT]
- [ ] Side-effecting triggers are idempotent (processed-marker or key) [INFERRED]
- [ ] Secrets in Secret Manager / params, none in source or client [INFERRED]
- [ ] Emulator tests pass [EXPLICIT]
- [ ] No AWS/Azure services (R-002) [EXPLICIT]

## 5. Self-Correction Triggers
> [!WARNING]
> IF an HTTP function has no auth middleware THEN add a `verifyIdToken` check (or signature verify if it's a webhook).
> IF a function imports 10+ deps OR a heavy SDK at module top THEN split or lazy-load to cut cold start.
> IF a Firestore/Storage trigger performs a charge/email/write-to-external THEN add an idempotency guard — it can fire twice.
> IF a provider key appears in source or a client bundle THEN move it to Secret Manager and rotate the leaked key.

## Decisions & Trade-offs
| Decision | Chosen | Trade-off |
|----------|--------|-----------|
| Extension vs. custom function | Official extension when it fits | Less code to own; less control over edge logic [INFERRED] |
| `minInstances` for cold start | Only on latency-critical funcs | Removes cold start but bills 24/7 even idle [EXPLICIT] |
| Webhook ack timing | Ack 200 fast, defer heavy work | Avoids provider retries/timeouts; needs async follow-up [INFERRED] |

## Usage
Example invocations:
- "/firebase-extensions" — Run the full firebase extensions workflow
- "firebase extensions on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and a configured Firebase project + billing enabled (extensions and 2nd-gen functions require Blaze). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final architecture decisions. [EXPLICIT]
- Does not provision the 3rd-party accounts themselves (Stripe/SendGrid/Algolia) — assumes they exist. [INFERRED]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| Duplicate trigger delivery | Idempotency guard short-circuits the replay [INFERRED] |
| Provider webhook with bad/missing signature | Reject 400, do not process [INFERRED] |
| Missing secret / unset extension param | Fail fast at deploy/start with a clear error, do not run with a blank key [INFERRED] |
