<!-- distilled from alfa skills/webhook-handling -->
<!-- > -->
# Webhook Handling

> "Trust, but verify — especially when the request claims to be from Stripe." — Unknown

## TL;DR

Guides reliable webhook handling — receiving, verifying, and processing webhooks from services like Stripe, GitHub, and custom integrations. Covers signature verification, idempotent processing, retry handling, and event ordering. Use when your application needs to react to events from external services. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify webhook sources (Stripe, GitHub, SendGrid, custom services)
- Check existing webhook endpoints and their processing logic
- Review webhook signing/verification mechanisms per provider
- Determine event types to subscribe to (not all events are needed)

### Step 2: Analyze
- Plan signature verification per provider (HMAC-SHA256, RSA, custom)
- Design idempotent processing (handle duplicate deliveries safely)
- Evaluate event ordering concerns (out-of-order delivery)
- Plan failure handling (retry logic, dead letter queue)

### Step 3: Execute
- Create webhook endpoint as Cloud Function HTTP trigger (raw body access required)
- Implement signature verification before any processing
- Parse event type and route to appropriate handler
- Store event ID to prevent duplicate processing (idempotency)
- Process asynchronously: acknowledge quickly (200 response), process in background
- Log all received events for debugging and audit
- Handle specific events: Stripe (`checkout.session.completed`), GitHub (`push`, `pull_request`)

### Step 4: Validate
- Test with provider's webhook testing tools (Stripe CLI, GitHub webhook deliveries)
- Verify signature verification rejects tampered payloads
- Confirm duplicate events are handled idempotently
- Check that webhook endpoint responds within provider timeout (typically 5-30 seconds)

## Quality Criteria

- [ ] Signature verification implemented for all webhook sources
- [ ] Idempotent processing prevents duplicate event handling
- [ ] Endpoint responds with 200 quickly, processes asynchronously if needed
- [ ] All webhook events logged for debugging and audit trail
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Processing webhook payload without verifying the signature (security vulnerability)
- Doing heavy processing synchronously (causes timeouts and retries)
- Not handling duplicate deliveries (webhooks retry on failures)

## Related Skills

- `payment-integration` — Stripe webhooks are critical for payment flow completion
- `rest-api-development` — webhooks are a specialized HTTP endpoint pattern

## Usage

Example invocations:

- "/webhook-handling" — Run the full webhook handling workflow
- "webhook handling on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
