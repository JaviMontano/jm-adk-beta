<!-- distilled from alfa skills/webhook-handling -->
<!-- > -->
# Webhook Handling

> "Trust, but verify — especially when the request claims to be from Stripe." — Unknown

## TL;DR

Receive, verify, and process webhooks from external services (Stripe, GitHub, SendGrid, custom). Covers signature verification, idempotent processing, fast-ack + async work, retry/backoff, and event ordering. Use when your app must react to events it does not poll for. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify webhook sources and their signing scheme (HMAC-SHA256, RSA, custom header). [EXPLICIT]
- Locate existing endpoints and their current processing/auth logic. [EXPLICIT]
- Select only the event types you act on — subscribing to all events inflates volume and attack surface. [INFERENCIA]
- Capture per-provider constraints: ack timeout, retry policy, payload max size, IP allowlist (if any). [EXPLICIT]

### Step 2: Analyze
- Map verification per provider (algorithm, which header, what bytes are signed). [EXPLICIT]
- Design idempotency: durable store keyed by provider event ID, write-once, with TTL. [INFERENCIA]
- Decide ordering strategy: rely on resource state/version in the payload, not arrival order. [INFERENCIA]
- Plan failure handling: what is retryable (5xx, transient), what is poison (bad signature, malformed) → dead-letter. [INFERENCIA]

### Step 3: Execute
- Expose the endpoint as a Cloud Function HTTP trigger configured for **raw body** access — signatures sign the exact bytes; any framework that re-serializes JSON breaks verification. [CÓDIGO]
- Verify the signature **before parsing or trusting any field**; reject on failure with `401`/`400`, no body processing. [EXPLICIT]
- Use a **constant-time** comparison for the signature digest (e.g. `crypto.timingSafeEqual` / `hmac.compare_digest`) — `==` leaks via timing. [CÓDIGO]
- Enforce a **timestamp tolerance** (e.g. ≤5 min) where the provider signs a timestamp (Stripe `t=`), to block replay of captured-but-valid payloads. [EXPLICIT]
- Check-and-insert the event ID **atomically** (conditional write / unique constraint); on duplicate, return `200` without re-processing. [INFERENCIA]
- Parse event type, route to a handler; **acknowledge fast (`200`)**, then do real work in the background (queue/task) — never block the ack on downstream I/O. [EXPLICIT]
- Log every received event (id, type, verification result, outcome) for audit and replay. [EXPLICIT]
- Handle named events: Stripe (`checkout.session.completed`, `invoice.paid`), GitHub (`push`, `pull_request`). [EXPLICIT]

### Step 4: Validate
- Drive the endpoint with the provider's tooling (Stripe CLI `stripe listen`, GitHub redelivery). [EXPLICIT]
- Confirm a tampered payload and an expired-timestamp payload are both **rejected**. [INFERENCIA]
- Confirm a replayed event ID is processed **exactly once** (side effects do not double-fire). [INFERENCIA]
- Confirm the endpoint acks within the provider timeout (typically 5–30 s) under load. [EXPLICIT]

## Decisions & Trade-offs

| Decision | Choice | Trade-off / Why [INFERENCIA] |
|---|---|---|
| Ack vs. process | Ack `200` first, process async | Avoids timeout→retry storms; cost is added queue infra + eventual-consistency window. |
| Idempotency key | Provider event ID | Provider-guaranteed unique; fails if a provider reuses IDs across resends of *different* events (rare) — fall back to content hash. |
| Bad signature | Return `400`, do **not** retry-invite | A signature failure is never transient; retrying wastes provider quota. |
| Transient downstream error | Return `5xx` so provider **retries** | Cheaper than building your own retry for the same effect; needs idempotency to be safe. |
| Ordering | Trust payload state/version, ignore arrival order | Out-of-order delivery is normal; sequencing by arrival is a latent bug. |

## Quality Criteria

- [ ] Signature verified (raw body, constant-time, timestamp-checked) before any processing. [EXPLICIT]
- [ ] Idempotent: duplicate deliveries cause no duplicate side effects. [EXPLICIT]
- [ ] Endpoint acks `200` within provider timeout; heavy work is async. [EXPLICIT]
- [ ] Every event logged (id, type, result) for audit/replay. [EXPLICIT]
- [ ] Poison events (bad sig/malformed) dead-lettered, not infinitely retried. [INFERENCIA]
- [ ] Evidence tags applied to all non-obvious claims. [EXPLICIT]

## Anti-Patterns

- Processing payload before verifying the signature — accepts forged events. [EXPLICIT]
- Verifying against a re-serialized/parsed body instead of raw bytes — verification silently always fails or, worse, is bypassed. [INFERENCIA]
- `==` for digest comparison — timing side-channel. [INFERENCIA]
- Synchronous heavy work in the handler — causes timeouts and retry storms. [EXPLICIT]
- No idempotency — retries double-charge, double-email, double-provision. [EXPLICIT]
- Sequencing by arrival order — breaks on normal out-of-order delivery. [INFERENCIA]

## Failure Modes

| Failure | Symptom | Mitigation [INFERENCIA] |
|---|---|---|
| Replay attack | Valid old payload re-sent by attacker | Timestamp tolerance + nonce/event-ID dedup. |
| Duplicate delivery | Same event arrives 2+ times | Atomic event-ID dedup before side effects. |
| Slow handler | Provider marks delivery failed, retries pile up | Fast `200` ack, async processing. |
| Secret rotation | Verification starts failing on all events | Accept both old+new signing secrets during the rotation window. |
| Out-of-order events | Stale event overwrites newer state | Apply only if payload version ≥ stored version. |
| Body mutation by proxy/middleware | Verification fails for legitimate events | Capture raw body at the edge, before any JSON middleware. |

## Related Skills

- `payment-integration` — Stripe webhooks complete the payment flow.
- `rest-api-development` — webhooks are a specialized HTTP endpoint pattern.

## Usage

Example invocations:

- "/webhook-handling" — Run the full webhook handling workflow.
- "webhook handling on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes the provider signs requests; if it does not, fall back to an IP allowlist + shared secret in a header and flag the weaker guarantee. [SUPUESTO]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not cover outbound webhooks (you *sending* events) — only inbound. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to appropriate skill or escalate. |
| Provider has no signing mechanism | Use IP allowlist + secret header; document reduced assurance. [SUPUESTO] |
| Signing secret mid-rotation | Verify against old and new secrets until cutover. [INFERENCIA] |
