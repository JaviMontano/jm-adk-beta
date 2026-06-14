# Integration routing & gate checklist

Run this before declaring an integration done. Ties to `assets/quality-rubric.json`.

## Route
- [ ] `topic` resolved to one enum value (payment / push / recaptcha / webhook).
- [ ] Exactly ONE playbook read from `routes:`; no other playbook loaded.
- [ ] Two requested topics sequenced (one playbook each), not merged.
- [ ] `depth` chosen (`quick` | `deep`) and applied.

## Verify before trust
- [ ] Webhook: raw-body signature, constant-time compare, timestamp tolerance.
- [ ] reCAPTCHA: server-side `siteverify` checking `success`+`action`+`score`+`hostname`.
- [ ] Payment: fulfillment driven by verified webhook events, not client callback.
- [ ] Push: server credentials stay server-side; tokens validated before reuse.

## Replay safety
- [ ] Money/event path idempotent (atomic dedup on provider event id).
- [ ] Replayed event processed exactly once (no double charge/email/provision).

## Secrets
- [ ] Secrets/keys from env / Firebase secrets — never inlined, never client-side.
- [ ] Missing required secret halted as `[VACIO_CRITICO]`, not placeholdered.

## Topic failure mode
- [ ] The one money/event-losing failure for this topic is explicitly closed.

## Governance
- [ ] Every claim carries an Alfa-core tag; no mixed tag families.
- [ ] Provider-version-dependent facts flagged `[SUPUESTO]` with a docs pointer.
- [ ] Gate reported with evidence, never green-by-default.
