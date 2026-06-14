# Architecture — Body of Knowledge

Domain knowledge for the nine routable topics. Evidence tags use the Alfa-core
family: `[DOC]` `[CONFIG]` `[CODE]` `[INFERENCE]` `[ASSUMPTION]`. [DOC]

## 1. Routing model
The skill is a **router**: one request → one `topic` → one playbook. A request
that spans concerns is decomposed into the dominant topic plus a chained second
invocation; playbooks are never merged. Ambiguity between two topics is resolved
by asking, not guessing. [DOC]

## 2. Cross-cutting key concepts

### Evidence-tagged claims
Every non-obvious claim carries exactly one tag, one family, one spelling.
`[ASSUMPTION]` always pairs with a verification step. This makes recommendations
auditable and falsifiable. [DOC]

### Trade-offs are mandatory
"Every architecture is the result of trade-offs." A recommendation without a
named rejected alternative and its cost is rejected at the gate. [DOC]

### Quality-attribute scenarios
Form: *source → stimulus → artifact → environment → response → measure*. The
**measure** is a number + unit (e.g. "p95 < 300 ms at 1000 req/s"), never an
adjective. Untestable scenarios ("highly available") are invalid. [DOC]

## 3. Topic decision rules

### api-design
- Style pick precedes contract: REST (default, resource CRUD), GraphQL (many
  client-shaped views, mobile bandwidth — cost: query-complexity + N+1),
  gRPC (internal low-latency streaming — cost: weak browser support). [DOC]
- Cursor pagination over offset (offset drifts under concurrent writes). [INFERENCE]
- Additive changes are non-breaking; remove/rename/type-change/tighten-validation
  is breaking → new version. Gate breaking diffs in CI (oasdiff/Spectral). [INFERENCE]
- Make POST retry-safe with `Idempotency-Key`. [INFERENCE]

### caching-strategy
- Place cache at the cheapest correct tier: CDN/edge for public immutable, app
  cache for shared computed reads, client cache for per-user views. [DOC]
- Choose TTL vs. explicit invalidation by staleness tolerance; guard against
  cache stampede (request coalescing / early recompute). [INFERENCE]

### domain-driven-design
- Strategic design (where boundaries go) dominates tactical polish — boundaries
  are the expensive mistake. [DOC]
- Classify subdomains: Core (invest), Supporting (build simply), Generic (buy).
  Custom-building a generic subdomain is a classic waste. [DOC]
- Context-map patterns: Shared Kernel, Customer/Supplier, Conformist, ACL,
  Open Host + Published Language. ACL protects a clean model from legacy. [DOC]
- Aggregate = transactional consistency boundary; one aggregate per transaction. [DOC]

### event-architecture
- Delivery is at-least-once by default; achieve exactly-once *effects* via
  consumer idempotency, not exactly-once delivery. [INFERENCE]
- Use the **outbox pattern** to avoid dual-write inconsistency between DB and
  broker. [DOC]
- Choreography decouples; orchestration centralizes control — pick per
  traceability vs. autonomy. [DOC]

### migration-planning
- Default bias: incremental over big bang; reversible over irreversible; never
  migrate and decommission in the same change. [INFERENCE]
- Strategy selector: Strangler Fig (seams, lowest risk), Parallel Run (prove
  correctness, doubles compute), Big Bang (small/coupled, tested restore only). [DOC]
- Capture pre-migration baselines (p50/p95/p99, throughput, row counts) — parity
  is unprovable without them. [INFERENCE]

### performance-architecture
- Set budgets before optimizing; measure p50/p95/p99 separately (tail ≠ mean).
- Isolate the bottleneck with evidence before changing architecture; load-shed
  rather than collapse under overload. [INFERENCE]

### realtime-architecture
- Transport pick: WebSocket (bidirectional, stateful), SSE (server→client,
  simple, auto-reconnect), long-poll (fallback). Plan reconnection/resume and
  backpressure for fan-out. [DOC]

### system-architecture
- C4 levels: Context, Container (minimum), Component, Code (when needed). Diagrams
  must be consistent — no phantom systems. [DOC]
- ADRs capture status/context/decision/consequences — not just the decision. [DOC]
- Default to the simplest style meeting ranked drivers; escalate on evidence.
  "We might need to scale" is `[ASSUMPTION]`, not a driver. [INFERENCE]

### trade-off-analysis
- Weighted decision matrix: ≥3 options, weights sum to 1.0, per-cell rationale,
  weighted score = Σ(weight × score). [INFERENCE]
- ATAM surfaces sensitivity points and trade-offs. Run a ±20% weight sensitivity
  check; if the winner flips, the result is fragile. [INFERENCE]

## 4. Standards & references
- C4 model (Simon Brown); ADR (Michael Nygard); ATAM (SEI). [DOC]
- OpenAPI 3.1; RFC 9457 problem details; RateLimit header drafts. [DOC]
- Evans DDD strategic/tactical patterns; transactional outbox (microservices.io). [DOC]

## 5. Decision rule summary
Pick the least operationally costly option that satisfies *ranked* drivers; name
the cost of every chosen pattern; tag every non-obvious claim; verify every
assumption; never invent prices; never declare done without the acceptance gate. [DOC]
