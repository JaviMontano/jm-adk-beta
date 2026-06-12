# Quick variation — architecture (depth=quick)

Fast path for a single, well-scoped architecture decision. Essentials only;
explicitly name what you skip.

## Run
1. Resolve to one `topic`; if ambiguous, ask one question, then stop.
2. Load the one playbook.
3. Apply ONLY its core decision rule(s):
   - api-design → style pick + versioning + pagination + error envelope.
   - caching-strategy → tier + TTL-vs-invalidation + staleness budget.
   - domain-driven-design → subdomain classification + bounded contexts.
   - event-architecture → delivery semantics + outbox/idempotency.
   - migration-planning → strategy pick + per-stage rollback.
   - performance-architecture → p50/p95/p99 budget + named bottleneck.
   - realtime-architecture → transport pick + reconnection plan.
   - system-architecture → C4 Context+Container + 1 ADR.
   - trade-off-analysis → 3-option weighted matrix + recommendation.
4. Tag each non-obvious claim; pair any `[ASSUMPTION]` with a verification step.
5. **Name what you skipped** (e.g. "skipped full ATAM, deep schema evolution").

## Guardrails
One playbook only. Every recommendation names its rejected alternative + cost.
No invented prices. Scenarios use number + unit.
