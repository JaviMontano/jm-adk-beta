# Body of Knowledge — integrations

Domain knowledge for wiring third-party services (payments, push, reCAPTCHA,
inbound webhooks) into an application. The router loads one playbook; this file
holds the cross-topic concepts, standards, and decision rules that every route
shares.

## Key concepts

### The security boundary
External payloads, client-side scores, and redirect callbacks are *untrusted*
until verified. Every integration crosses a boundary: money in (payments),
identity of an inbound event (webhooks), bot-risk of a request (reCAPTCHA), or a
device target (push). Trust is established by server-side verification, never by
the client. [DOC]

### Verification before trust
- **Webhooks:** verify the HMAC/RSA signature over the *raw* request body with a
  constant-time comparison, enforce a timestamp tolerance (≤5 min), before
  parsing any field. [CÓDIGO]
- **Payments:** fulfillment is driven by signature-verified webhook events
  (`checkout.session.completed`, `invoice.paid`), not by client confirmation. [DOC]
- **reCAPTCHA:** verify the token server-side via `siteverify`, checking
  `success` AND `action` AND `score` AND `hostname` — never the client score. [DOC]
- **Push:** server credentials (Admin SDK key, server key) stay server-side;
  tokens are validated against the not-registered error before reuse. [INFERENCIA]

### Idempotency
Money and event paths must be replay-safe. Key on the provider event ID with an
atomic check-and-insert; on duplicate, ack `200` without re-processing. Stripe
and most providers retry until they get a 2xx, so a non-idempotent handler
double-fulfills, double-charges, or double-notifies. [DOC]

### Fast-ack + async
Acknowledge inbound events fast (`200` within the provider timeout, typically
5–30 s), then do heavy work in a queue/task. Blocking the ack on downstream I/O
causes timeout → retry storms. [EXPLICIT]

### Secrets handling
Secrets and signing keys are referenced from Firebase secrets / env, never
inlined and never shipped to the client. A missing required secret is a
`[VACIO_CRITICO]` — stop and ask, do not placeholder. [SUPUESTO]

## Standards & references
- **PCI DSS SAQ-A** — keep card data (PAN) off your servers by using hosted
  Checkout / Elements; reduces compliance scope. [DOC]
- **SCA / 3D Secure** — Strong Customer Authentication for EU/UK card payments. [DOC]
- **HMAC-SHA256 / constant-time compare** — `crypto.timingSafeEqual` /
  `hmac.compare_digest`; `==` leaks via timing. [CÓDIGO]
- **VAPID / Web Push** — voluntary application server identification for browser
  push; FCM abstracts VAPID/APNs differences across platforms. [INFERENCIA]
- **reCAPTCHA v3 scoring** — `0.0` bot … `1.0` human; default cut `0.5`, tuned
  per action; v3 is a risk signal, not a verdict. [DOC]
- **Firebase App Check** — backend attestation; roll out in monitor mode before
  enforcing. [CONFIG]

## Decision rules
| Question | Rule |
|----------|------|
| Trust client or server? | Server verification is authoritative; client is a UX hint. [DOC] |
| Hosted vs embedded checkout? | Hosted Checkout by default (SAQ-A); Elements only when brand-controlled in-page is required. [INFERENCIA] |
| Handle ordering by arrival? | No — order by payload state/version, not delivery order. [INFERENCIA] |
| Bad signature → retry? | No — signature failure is never transient; return 400, do not invite retry. [INFERENCIA] |
| Transient downstream error? | Return 5xx so the provider retries; safe only because the handler is idempotent. [INFERENCIA] |
| Block on a low reCAPTCHA score? | No flat block — graduated step-up (email/SMS/v2) before a hard deny. [EXPLICIT] |
| Permission prompt timing? | Contextual, after an intent signal — never on first page load. [EXPLICIT] |
| Two topics in one request? | Sequence them; one playbook each; never merge across the boundary. [SUPUESTO] |

## Evidence taxonomy
`[CÓDIGO]` code-level fact · `[CONFIG]` configuration/gate fact · `[DOC]`
documented provider behavior · `[INFERENCIA]` reasoned conclusion · `[SUPUESTO]`
provider-version-dependent assumption to confirm. Never mix tag families in one
claim. `[VACIO_CRITICO]` marks a blocking missing secret.

## Anti-scope (route elsewhere)
Outbound webhooks you emit, in-app messaging, SMS/email channels, marketplace
Connect payouts, Apple/Google in-app purchase billing, crypto rails, and edge
WAF/DDoS — none are covered here. [SUPUESTO]
