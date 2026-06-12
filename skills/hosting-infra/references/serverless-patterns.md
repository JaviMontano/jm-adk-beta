<!-- distilled from alfa skills/serverless-patterns -->
<!-- Fan-out (Firestore trigger to multiple ops). Saga (compensating transactions). Event sourcing with Firestore. [EXPLICIT] -->
# serverless-patterns {Backend} (v1.1)
> **"Firebase Functions are your backend. Design them like microservices, deploy them like magic."**
## Purpose
Fan-out (Firestore trigger to multiple ops). Saga (compensating transactions). Event sourcing with Firestore. [EXPLICIT]
**When to use:** Backend development within Firebase/Google ecosystem. [EXPLICIT]
**Anti-scope (do NOT use for):** AWS Lambda / Azure Functions targets (R-002); long-running jobs >540s (Cloud Run instead); >32MB request/response payloads (use Storage + signed URL); sub-100ms latency SLOs where cold start is unacceptable (provisioned Cloud Run / min-instances). [INFERENCIA]
## Pattern Selection
| Pattern | Use when | Trade-off accepted | Tag |
|---------|----------|--------------------|-----|
| Fan-out | One write must trigger N independent side-effects | At-least-once delivery → side-effects MUST be idempotent | [EXPLICIT] |
| Saga / compensating tx | Multi-step workflow spanning docs/services, no distributed 2PC | Eventual consistency; each step needs an inverse op | [EXPLICIT] |
| Event sourcing | Audit trail / replay / temporal queries required | Storage growth + read-model rebuild cost | [EXPLICIT] |
> Firestore triggers fire **at-least-once** and may arrive **out of order**; design every handler to be idempotent and order-independent. [DOC]
## Core Principles
1. **Law of Functions:** Each Cloud Function does ONE thing. Single responsibility. [EXPLICIT]
2. **Law of Cold Start:** Minimize dependencies. Use lazy imports. Set min instances for critical functions. [EXPLICIT]
3. **Law of Security:** Every HTTP function verifies Firebase ID tokens. No public endpoints without auth. [EXPLICIT]
4. **Law of Idempotency:** Dedupe by event ID / deterministic doc key so retries never double-apply. [INFERENCIA]
## Core Process
### Phase 1: Design
1. Map requirements to Cloud Functions triggers (HTTP, Firestore, Auth, Storage, scheduled). [EXPLICIT]
2. Define input/output contracts for each function. [EXPLICIT]
3. Design error handling and retry strategy; mark which handlers are retry-safe. [EXPLICIT]
### Phase 2: Implement
1. Create function with proper trigger type. [EXPLICIT]
2. Add auth middleware for HTTP functions. [EXPLICIT]
3. Implement business logic with error handling. [EXPLICIT]
4. Add Cloud Logging for observability. [EXPLICIT]
### Phase 3: Test + Deploy
1. Test with Firebase Emulator Suite. [EXPLICIT]
2. Deploy with `firebase deploy --only functions`. [EXPLICIT]
3. Verify in Firebase Console. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements | Text/Spec | Yes | What the function does |
| Trigger type | Enum | Yes | http / firestore / auth / storage / scheduled |
| Idempotency key | Field path | If retry-safe | Dedupe key for at-least-once delivery |
| Output | Type | Description |
|--------|------|-------------|
| Cloud Function code | TypeScript | Deployable function |
## Worked Example — fan-out (Firestore → N ops), idempotent
```typescript
// onCreate(orders/{id}): notify + index + audit, safe on retry
export const onOrder = onDocumentCreated("orders/{id}", async (e) => {
  const id = e.params.id;                     // delivery may repeat
  const seen = db.doc(`_processed/onOrder_${id}`);
  if ((await seen.get()).exists) return;      // dedupe guard [EXPLICIT]
  await Promise.all([notify(id), index(id), audit(id)]); // each idempotent
  await seen.set({ at: FieldValue.serverTimestamp() });
});
```
HTTP auth guard (Law of Security): reject before any logic runs.
```typescript
const decoded = await admin.auth().verifyIdToken(idToken); // throws → 401 [EXPLICIT]
```
## Validation Gate
- [ ] Single responsibility per function
- [ ] Auth middleware on HTTP endpoints
- [ ] Error handling with Cloud Logging
- [ ] Handlers idempotent (dedupe guard on at-least-once triggers)
- [ ] Saga steps each have a compensating inverse
- [ ] Emulator tests pass (incl. one duplicate-delivery test)
- [ ] No AWS/Azure services (R-002)
## 5. Self-Correction Triggers
> [!WARNING]
> IF function has no auth middleware THEN add verifyIdToken check.
> IF function imports 10+ dependencies THEN split or lazy-load to reduce cold start.
> IF a Firestore handler is not idempotent THEN add a dedupe guard before side-effects.
> IF a saga step lacks an inverse THEN block deploy until the compensation is defined.

## Failure Modes
| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Duplicate delivery | Side-effect applied twice (double email, double charge) | Dedupe guard keyed on event/doc ID [EXPLICIT] |
| Trigger loop | Handler writes the doc it triggers on → recursion + cost spike | Write to a different collection or gate on a changed field [INFERENCIA] |
| Cold-start timeout | First invocation slow / times out under SLO | Lazy imports; `minInstances` on hot paths [EXPLICIT] |
| Saga partial failure | Workflow stuck mid-sequence | Run compensations in reverse; persist saga state for resume [SUPUESTO] |
| Unbounded retries | Failing handler retried until quota burn | Cap retries; route poison events to a dead-letter doc [INFERENCIA] |

## Usage

Example invocations:

- "/serverless-patterns" — Run the full serverless patterns workflow
- "serverless patterns on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Targets 2nd-gen Cloud Functions for Firebase (TypeScript); 1st-gen trigger signatures differ [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Out-of-order trigger delivery | Reconcile from doc state, not event sequence [INFERENCIA] |
| Concurrent writes to same doc | Use a Firestore transaction, not read-then-write [DOC] |
