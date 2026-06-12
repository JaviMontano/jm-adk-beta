# Integration Deliverable — {topic}

## 1. Routing decision
- **Resolved topic:** {payment-integration | push-notifications | recaptcha-integration | webhook-handling}
- **Depth:** {quick | deep}
- **Playbook read:** {references/<topic>.md}  _(exactly one — confirm no others loaded)_
- **Provider(s):** {Stripe/PayPal | FCM/Web Push | reCAPTCHA v3 + App Check | <provider>}
- **Routing rationale:** {keyword(s) that resolved the topic} [INFERENCIA]

## 2. Discover
- Use cases / surfaces in scope: {…}
- Provider account / config state: {…} [CONFIG]
- Anti-scope flagged: {outbound webhooks | in-app messaging | payouts | …} [SUPUESTO]

## 3. Analyze
- Key design decisions (with trade-offs): {…} [INFERENCIA]
- Lifecycle / states handled: {…} [DOC]
- The one failure that loses money or drops events: {…}

## 4. Execute
| Step | What was wired | Evidence |
|------|----------------|----------|
| {…} | {…} | [CÓDIGO] |
| Secrets source | env / Firebase secrets — not inlined | [CÓDIGO] |
| Verification | {raw-body HMAC / siteverify / webhook-driven fulfillment} | [DOC] |
| Idempotency | dedup keyed on {event.id / content hash} | [INFERENCIA] |

## 5. Validation gate
- [ ] Exactly one playbook read; `topic ∈ enum`. [CONFIG]
- [ ] Secrets/keys referenced from config/env, never inlined or client-side. [CÓDIGO]
- [ ] Signature/origin verification before trusting any external payload. [DOC]
- [ ] Idempotency on money/event paths; replays safe. [INFERENCIA]
- [ ] Topic-specific checks (from `agents/guardian.md`): {…}
- [ ] Evidence tags applied; no mixed tag families.

## 6. Open items
- `[SUPUESTO]` to confirm against current provider docs: {…}
- `[VACIO_CRITICO]` blocking secrets (if any): {…}

## 7. Gate result
**gate = {pass | fail}** — {if fail, list the unmet checks with missing evidence}.
