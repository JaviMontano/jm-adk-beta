# Deep variation — integrations (`depth: deep`)

Exhaustive application of one integration playbook, verifying at each step. Use
for production-bound work where every lifecycle state and failure mode matters.

## Steps
1. Resolve `topic`; read ONE playbook. Still one route — depth ≠ breadth.
2. Apply Discover → Analyze → Execute → Validate fully, leaving no step or
   decision-table row unaddressed.
3. Exercise every failure mode the playbook lists:
   - **payment** — duplicate fulfillment, lost webhook (reconcile sweep),
     out-of-order events (re-fetch from API), secret rotation (dual secrets),
     dispute/chargeback; test cards success/decline/3DS.
   - **push** — token refresh, stale-token pruning on the documented error,
     foreground/background/closed delivery, iOS PWA web push, preference honoring.
   - **recaptcha** — per-action thresholds, graduated step-up, App Check
     monitor→enforce rollout, debug token, script-blocked/CSP fallback.
   - **webhook** — tampered + expired-timestamp rejection, replayed-ID
     exactly-once, ack-under-timeout-at-load, poison → dead-letter, secret
     rotation window.
4. Run the FULL Validation gate plus the topic-specific checks from
   `agents/guardian.md`; demonstrate each, never assume.

## Rigor
Every claim tagged; provider-version-dependent facts `[SUPUESTO]` with a pointer
to current docs. Reconcile conflicts explicitly. Halt on missing secrets
(`[VACIO_CRITICO]`). Done only when the guardian returns `gate=pass`.
