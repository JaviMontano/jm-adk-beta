# Deep Variation: email-comms

`depth=deep`. Exhaustive execution with per-step verification, for production
sends and broken-render diagnosis. [DOC]

## Use when

The work is going live or is failing in production: standing up a new sending
domain, shipping a transactional template across all clients, or rescuing a
newsletter with declining metrics.

## Expanded procedure

1. Resolve the topic; if it spans two, sequence prerequisites explicitly and run
   both spines in order (builder → templates → sending; newsletter-design →
   email-template-builder). [INFERENCE]
2. **Discover** fully: volume estimates, existing infra, client traffic share,
   baselines (open/CTR/CTOR/unsub/complaint for newsletters). [DOC]
3. **Analyze** with trade-offs stated: provider choice, IP strategy, responsive
   strategy, content architecture — each justified, not asserted. [DOC]
4. **Execute** the complete artifact set: DNS records, queued idempotent send,
   bounce/complaint webhooks, MSO/VML Outlook fixes, UTM-instrumented links,
   Firestore `mail`-doc payload. [CODE]
5. **Validate** the full matrix:
   - email-sending → mail-tester score, multi-provider seed test, DMARC `rua`
     review before raising policy, live unsubscribe round-trip. [DOC]
   - templates → Litmus/Email-on-Acid 20+ combos, images-off, dark mode,
     <100 KB, bulletproof button in Outlook. [DOC]
   - newsletter-design → measurement plan wired, A/B significance check. [DOC]
6. Confirm every Validate gate from `agents/guardian.md` with evidence. [DOC]

## Discipline

Mark vendor-specific thresholds `[ASSUMPTION]` and verify against current docs.
Never declare done until the guardian emits `pass`. [DOC]
