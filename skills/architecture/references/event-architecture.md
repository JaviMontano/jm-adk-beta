<!-- distilled from alfa skills/event-architecture -->
<!-- This skill should be used when the user asks to "design an event-driven system", -->
# Event Architecture: Catalog, Consistency Patterns & Operational Excellence

Event-driven architecture decouples producers from consumers through asynchronous messaging — enabling scalability, resilience, and temporal flexibility. The skill covers event catalog design, broker selection, schema governance, consistency patterns (sagas, CQRS, event sourcing), and the operational practices that keep event systems reliable. [EXPLICIT]

## Principio Rector

**Los eventos son hechos inmutables — no mensajes descartables.** Un evento publicado es historia del sistema. El catálogo de eventos es el system of record, el schema registry previene breaking changes, y la consistencia eventual es una feature, no un bug.

### Filosofía de Event Architecture

1. **El catálogo de eventos ES el sistema.** Si un evento no está catalogado, no existe. El catálogo es la fuente de verdad que conecta dominios, equipos y contratos. [EXPLICIT]
2. **Schema registry previene breaking changes.** Sin schema registry, cada deploy es una ruleta rusa. La compatibilidad se valida en CI, no en producción a las 3am. [EXPLICIT]
3. **Eventual consistency es una feature, no un bug.** Los sistemas distribuidos son eventualmente consistentes por naturaleza. Diseñarlo explícitamente (sagas, outbox, idempotencia) transforma un problema en una ventaja. [EXPLICIT]

## Inputs

The user provides a system or platform name as `$ARGUMENTS`. Parse `$1` as the **system/platform name** used throughout all output artifacts. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
  - **piloto-auto**: Auto para event catalog y broker config, HITL para saga design y schema compatibility decisions. [EXPLICIT]
  - **desatendido**: Cero interrupciones. Event architecture documentada automáticamente. Supuestos documentados. [EXPLICIT]
  - **supervisado**: Autónomo con checkpoint en broker selection y consistency pattern design. [EXPLICIT]
  - **paso-a-paso**: Confirma cada event definition, schema, saga flow, y operational procedure. [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40% — S1 catalog + S3 schema registry + S4 consistency) | `técnica` (full 6 sections, default)

**Input contract — what blocks vs. what auto-fills:** [INFERRED]
- BLOCKING (stop and ask, never auto-fill): no identifiable domain boundaries; broker already mandated by org policy but undocumented (must extract before recommending); compliance regime that forbids event payload retention (affects sourcing/replay feasibility).
- AUTO-FILLABLE (document the assumption): event volume (assume <10k msg/sec until told otherwise), retention window (assume 7 days), broker (assume cloud-native managed unless event sourcing detected → Kafka). [INFERRED]

Before generating event architecture, detect the codebase context:

```
!find . -name "*.yaml" -o -name "*.json" -o -name "*.avro" -o -name "*.proto" -o -name "*event*" -o -name "*kafka*" -o -name "*rabbit*" | head -30
```

Use detected event definitions, broker configurations, and schema files to tailor catalog structure, pattern recommendations, and operational guidance. [EXPLICIT]

If reference materials exist, load them:

```
Read ${CLAUDE_SKILL_DIR}/references/event-patterns.md
```

---

## When to Use

- Designing event-driven communication between services
- Building an event catalog with taxonomy and schema governance
- Selecting message broker technology (Kafka, RabbitMQ, Pulsar)
- Implementing consistency patterns (sagas, compensating transactions)
- Designing CQRS with event sourcing for complex domains
- Establishing operational practices for event systems (DLQ, monitoring, replay)
- Migrating from synchronous to asynchronous communication

## When NOT to Use

- Internal module structure and code organization — use software-architecture
- REST/GraphQL/gRPC API design — use api-architecture
- Data pipeline and ETL/ELT design — use data-engineering
- Infrastructure and compute platform design — use infrastructure-architecture

**Anti-scope — explicitly out, even when adjacent:** [INFERRED]
- Choosing the event broker's *hosting* (Kubernetes vs. managed) — that is infrastructure-architecture; this skill picks the broker *category* and its reliability config, not the deployment substrate.
- Stream *analytics/aggregation* (Flink, ksqlDB windowing for metrics) — that is data-engineering; this skill covers streams as a transport and event store, not as a computation engine.
- Exactly-once *business semantics* via 2-phase commit / XA transactions — out by design; this skill achieves effectively-once through idempotency + outbox, and treats distributed transactions as an anti-pattern to avoid. [INFERRED]

---

## Delivery Structure: 6 Sections

### S1: Event Catalog & Taxonomy

Establish naming conventions, event types, and a discoverable catalog of all events. [EXPLICIT]

**Event naming:** `<Domain>.<Entity>.<Action>` (e.g., `Order.Payment.Completed`)
- Action is **past tense** — events are facts that already happened (`Completed`, not `Complete`). Present/imperative tense signals a command, not an event; route commands through APIs, not the event bus. [INFERRED]
- Version in the *type*, not the topic: `Order.Payment.Completed.v2`, so consumers self-select and the registry can enforce compatibility per type. [INFERRED]

**Event type classification:**
- **Domain events:** Business-meaningful occurrences (OrderPlaced, InvoiceGenerated)
- **Integration events:** Cross-boundary communication (UserSynced, InventoryReserved)
- **System events:** Operational signals (ServiceStarted, HealthCheckFailed)

Keep domain events private to the owning context; publish a deliberately narrower *integration* event across boundaries. Leaking raw domain events couples external consumers to your internal model — every internal refactor then becomes a breaking change. [INFERRED]

**CloudEvents Standard (CNCF)** — vendor-neutral event envelope for interoperability:
- Required attributes: `id`, `source`, `specversion` (1.0), `type`
- Recommended: `time`, `datacontenttype`, `dataschema`, `subject`
- Protocol bindings: HTTP, Kafka (header mapping), AMQP, MQTT, NATS
- Supported by: AWS EventBridge, Azure Event Grid, GCP Eventarc, Knative
- Adopt when: multi-cloud, multi-broker, or events crossing organizational boundaries
- Without CloudEvents, each team invents its own structure — adopt early to avoid format chaos

**Event Granularity Decision Matrix:**

| Type | Payload | Coupling | Latency | When to use |
|---|---|---|---|---|
| **Notification (thin)** | Signal only: `{ orderId }` | Low (consumer fetches via API) | Higher (API callback) | Default starting point; consumer has API access |
| **State Transfer (fat)** | Full state: `{ orderId, items[], total }` | Higher (schema dependency) | Lower (self-contained) | Consumer needs embedded data; API callback adds unacceptable latency |
| **Delta** | Changed fields only: `{ orderId, status: "shipped" }` | Medium | Lowest | Consumer maintains local state; bandwidth-constrained |

Rule of thumb: start thin, fatten only when consumers demonstrably need embedded data. [EXPLICIT]

**Trade-off — thin vs. fat, stated explicitly:** thin events keep producer and consumer schemas independent but create a *read-amplification* and *temporal-coupling* problem — the consumer must call back, and if the source is down or the entity already changed, the callback returns stale or 404 data (the "dual-write read" race). Fat events remove the callback but make the producer's schema a public contract the registry must now govern. Choose thin until callback latency or source availability provably breaks the SLA. [INFERRED]

**Key decisions:**
- Envelope vs. embedded metadata: separate header from payload (recommended) or merge
- Catalog governance: mandatory registration before publishing (recommended) or passive discovery
- Schema design: envelope (metadata) + payload (business data) with correlationId and causationId
  - `correlationId` = the originating business transaction (constant across the whole chain); `causationId` = the immediate parent event that caused this one. Together they reconstruct the causal tree for tracing and replay. Omitting `causationId` is the most common gap — without it you can group events but not order their causality. [INFERRED]

**Worked example — order flow catalog entry:** [INFERRED]
```
type:    Order.Payment.Completed.v1   (domain event, internal)
envelope: { id, source: "payments-svc", time, correlationId, causationId, specversion: "1.0" }
payload:  { orderId, amount, currency, method }   # thin-ish: no full order graph
emits →   Integration event Billing.Invoice.Requested.v1 (narrowed, cross-boundary)
```

**S1 acceptance criteria:** every event has a registered type following `Domain.Entity.Action` (past tense); each carries `id` + `correlationId`; domain vs. integration boundary is explicit; granularity choice (thin/fat/delta) is justified per event, not blanket. [INFERRED]

**S1 failure modes:** "command-as-event" (imperative naming hiding RPC); orphan events (published, never catalogued); over-fat events that turn the producer into an undocumented public API; CRUD-mirroring events (`Order.Updated` with no business meaning) that force consumers to diff state. [INFERRED]

### S2: Message Broker Architecture

Select and configure the message broker for reliability, throughput, and operational simplicity. [EXPLICIT]

**Broker Selection Matrix:**

| Criterion | Apache Kafka | RabbitMQ | Apache Pulsar | Cloud-native (SNS+SQS, Event Grid, Pub/Sub) |
|---|---|---|---|---|
| Throughput | Millions msg/sec | Tens of thousands | Millions msg/sec | Varies by service |
| Replay | Native (log-based) | Not built-in | Native (tiered storage) | Limited |
| Latency | Low-medium (batching) | Sub-millisecond | Low | Medium |
| Ordering | Per-partition | Per-queue | Per-partition | Varies |
| Multi-tenancy | Topic-level | Vhost-level | Native | Native |
| Ops complexity | High (ZK/KRaft) | Low-medium | Medium-high | Managed |
| Best for | High-volume, event sourcing | Task queues, RPC, simple routing | Multi-tenant, geo-replicated | Serverless, low ops budget |

**Selection heuristic (decision order, not feature-counting):** [INFERRED]
1. Need **replay / event sourcing / audit log**? → Kafka or Pulsar. Eliminates RabbitMQ and most cloud-native primitives immediately.
2. Have **a dedicated platform/SRE team** and >100k msg/sec? → Kafka.
3. Need **complex routing** (topic exchanges, per-message TTL, priority queues) and sub-ms latency? → RabbitMQ.
4. Want **near-zero ops** and volume fits a managed tier? → cloud-native (SNS+SQS / Pub/Sub / Event Grid). Default for teams without a streaming platform team.
5. **Geo-replication + multi-tenancy** first-class? → Pulsar.

Do not pick Kafka by reputation. Kafka's ops burden (partition rebalancing, broker sizing, KRaft/ZK quorum, consumer-lag firefighting) is a standing tax; if you do not need replay or >100k msg/sec, managed cloud-native is the lower-total-cost choice. [INFERRED]

**Critical Kafka Configurations for Reliability:**
- `acks=all` — wait for all in-sync replicas to acknowledge (mandatory for durability)
- `min.insync.replicas=2` — require at least 2 replicas in sync before accepting writes
- `enable.idempotence=true` — prevent duplicate messages from producer retries
- `max.in.flight.requests.per.connection=5` — safe with idempotence enabled
- Replication factor: 3 minimum for production topics

Why `min.insync.replicas=2` with RF=3 specifically: it tolerates exactly one broker loss while still guaranteeing durability. Setting `min.insync.replicas=RF` (=3) means any single broker outage halts all writes — availability collapses. RF=2 with insync=2 leaves zero headroom. RF=3/insync=2 is the standard durability-vs-availability sweet spot. [INFERRED]

`acks=all` without `min.insync.replicas≥2` is a false sense of safety: with insync=1 a single replica can ack and then be lost, silently dropping the write. The two settings only work as a pair. [INFERRED]

**Consumer Group Strategies:**
- One group per downstream service (independent offsets, independent scaling)
- Scale consumers by adding instances (max instances = number of partitions)
- Use **cooperative sticky rebalancing** (`partition.assignment.strategy=cooperative-sticky`) to minimize partition shuffling during scaling
- Create temporary groups with `auto.offset.reset=earliest` for isolated replay
- Separate groups for real-time vs. batch consumers on the same topic

**Partitioning:** By entity ID (ordering guarantee), by tenant (isolation), round-robin (max throughput)
- Partition count is hard to *decrease* — over-provision modestly (e.g. 2–3× expected consumer instances) rather than reshard later, since changing partition count rehashes keys and breaks per-key ordering for in-flight data. [INFERRED]
- Hot-partition risk: a single high-volume key (one whale tenant) saturates one partition while others idle. Detect via per-partition lag skew; mitigate with composite keys or a dedicated partition for the whale. [INFERRED]

**Retention:** Time-based (7-30 days typical) or log compaction for latest-state topics
- Compaction keeps the *latest* value per key forever (good for "current state" topics consumed by new joiners) but you lose the full history — incompatible with event-sourcing replay. Do not compact an event-sourced topic. [INFERRED]

**S2 acceptance criteria:** broker choice traces to the selection heuristic with the deciding factor named; for Kafka, durability quartet (`acks=all`, RF≥3, `min.insync.replicas=2`, `enable.idempotence=true`) is set; partition key chosen with ordering requirement stated; retention mode matches consumption pattern (compaction vs. time vs. infinite-for-sourcing). [INFERRED]

**S2 failure modes:** Kafka chosen with no replay/throughput need (ops tax for nothing); `acks=1`/insync=1 silent data loss; hot partition from skewed keys; eager rebalancing causing stop-the-world pauses during autoscale; compacted event-source topic destroying replay. [INFERRED]

### S3: Event Schema Registry

Govern schema evolution to prevent producer-consumer contract breaks. [EXPLICIT]

**Platforms:** Confluent Schema Registry, AWS Glue Schema Registry, Apicurio
**Formats:** Avro (compact, best Kafka integration), Protobuf (strong typing, gRPC bridge), JSON Schema (readable, flexible)

Format trade-off: Avro needs the writer schema at read time (registry lookup) — most compact, tightest Kafka fit. Protobuf carries field tags so it self-describes ordinally and bridges to gRPC — best when the same contract serves sync and async. JSON Schema is human-debuggable and tooling-ubiquitous but largest on the wire and weakest on enforced typing. Default Avro on Kafka; Protobuf when sharing contracts with gRPC services; JSON Schema only for low-volume or human-facing event streams. [INFERRED]

**Compatibility Modes:**

| Mode | Rule | Safe changes | Use when |
|---|---|---|---|
| **Backward** (recommended default) | New schema reads old data | Add optional fields, remove fields with defaults | Consumers upgrade before producers |
| **Forward** | Old schema reads new data | Remove optional fields, add fields with defaults | Producers upgrade before consumers |
| **Full** | Both directions | Only add/remove optional fields with defaults | Maximum safety, most restrictive |
| **None** | No checks | Anything | Never in production |

`*-transitive` variants check the new schema against the *entire* version history, not just the previous version. Prefer the transitive form for long-lived topics — non-transitive lets a slow consumer that skipped a version break. [INFERRED]

**Breaking changes no mode makes safe** (require a new event version + dual-publish, never an in-place edit): renaming a field, narrowing a type (string→int), changing a field's semantic meaning while keeping its name, making an optional field required. Treat these as `Order.Payment.Completed.v2` and run both versions until all consumers cut over. [INFERRED]

**CI/CD integration:** Block deployments that break schema compatibility. Run schema validation on every PR that modifies event definitions.

**Worked example — safe vs. unsafe under Backward:** [INFERRED]
```
SAFE:    add optional `discountCode` with default ""      → old consumers ignore it
SAFE:    remove `legacyFlag` that had a default            → old data still readable
UNSAFE:  rename `amount` → `amountCents`                    → old data has no amountCents
UNSAFE:  change `amount` string "10.00" → integer 1000      → type narrowing; new version required
```

**S3 acceptance criteria:** registry chosen and wired into producers; compatibility mode set (Backward-transitive default) and justified by deploy order; CI gate rejects incompatible schemas on PR; semantic-breaking changes are versioned (`.vN`) with a dual-publish window, never edited in place. [INFERRED]

**S3 failure modes:** `None` mode "temporarily" left on in prod; non-transitive mode bypassed by a lagging consumer; rename treated as backward-compatible; producer deployed before consumers under Backward (deploy-order inversion); schema lives only in code, not the registry, so the gate validates nothing. [INFERRED]

### S4: Consistency Patterns

Manage distributed consistency without distributed transactions. [EXPLICIT]

**Saga Pattern Comparison:**

| Aspect | Orchestration | Choreography |
|---|---|---|
| Coordination | Central orchestrator | Decentralized, event-driven |
| Visibility | Clear flow, centralized state | Emergent, hard to trace |
| Coupling | Orchestrator depends on all services | Services loosely coupled |
| Error handling | Centralized compensation logic | Distributed, each service handles own |
| Best for | Complex multi-step (4+ services), financial | Simple 2-3 step workflows |

**Compensation is not rollback.** A saga cannot undo a committed local transaction — it issues a *new* compensating action that semantically reverses it (refund, not un-charge; cancel-reservation, not un-reserve). Compensations must themselves be idempotent and must tolerate the forward action having partially succeeded. Some actions are *uncompensatable* (email sent, physical shipment dispatched) — design those as the last step, or gate them behind a confirmation event. [INFERRED]

**Outbox Pattern for Reliable Publishing:**
1. Write domain change + event to `outbox` table in **one DB transaction** (atomicity guaranteed)
2. Relay process reads outbox rows and publishes to broker, marks as sent
3. Purge published rows after retention (e.g., 7 days)

Outbox table schema: `id, aggregate_type, aggregate_id, event_type, payload, created_at, published_at`

The outbox solves the **dual-write problem**: writing to the DB and publishing to the broker are two systems that cannot share one transaction, so a crash between them either loses the event or emits a phantom for a rolled-back change. The outbox collapses both writes into the *one* transactional store, then publishes asynchronously. The relay guarantees *at-least-once* delivery (a crash after publish but before marking `published_at` re-sends) — which is exactly why every consumer must be idempotent (below). [INFERRED]

**Relay Options:**

| Method | Latency | Complexity | When to use |
|---|---|---|---|
| **Polling** | Higher (poll interval) | Low (simple query) | Small-medium volume, ops simplicity |
| **CDC (Debezium)** | Near-real-time | Higher (Kafka Connect, connector config) | High volume, low-latency requirement |

Polling pitfall: `SELECT ... WHERE published_at IS NULL ORDER BY id` under concurrency must use `FOR UPDATE SKIP LOCKED` (or a single relay instance) or two relays double-publish the same row. Index on `published_at` (partial index `WHERE published_at IS NULL`) or the poll table-scans as the outbox grows. [INFERRED]

Debezium reads the database WAL/binlog and streams outbox rows to Kafka. Use the `outbox.event.router` SMT to transform CDC records into clean business events. [EXPLICIT]

CDC pitfall: WAL/binlog retention must outlast any Debezium downtime, or the connector resumes from a purged log position and silently skips events. Size log retention to your worst-case connector outage. [INFERRED]

**Inbox pattern:** Consumer writes received event to inbox table, deduplicates by event ID, processes idempotently.

**Idempotency:** Every consumer must safely process the same event twice. Use idempotency keys stored in a deduplication table with TTL.
- Key choice matters: dedup on the *producer's* `event.id` (stable across redelivery), not a consumer-generated receipt time. TTL must exceed the broker's max redelivery window (retention + max retry backoff) or a late redelivery slips past an expired key and double-processes. [INFERRED]
- The dedup write and the business write must be atomic (same DB transaction or an UPSERT on the dedup key) — otherwise a crash between "process" and "record processed" reintroduces the duplicate. [INFERRED]

**Pattern stack — how S4 composes end-to-end:** producer uses **outbox** (no lost/phantom events) → broker delivers **at-least-once** → consumer uses **inbox/idempotency** (no double-effect) → multi-step flows coordinated by **saga** with idempotent **compensations**. Each layer assumes the next handles its weaker guarantee; skip one and the chain leaks duplicates or lost work. [INFERRED]

**S4 acceptance criteria:** saga style matches step count/criticality; every saga step has a defined (idempotent) compensation, uncompensatable steps placed last; outbox used for any event that must not be lost, with relay (poll vs. CDC) justified and its concurrency/retention pitfall handled; every consumer idempotent with dedup key = producer event id and TTL > max redelivery window. [INFERRED]

**S4 failure modes:** dual-write (DB committed, event lost or phantom-published); compensation assumed to be a rollback; relay double-publish under concurrency (`SKIP LOCKED` missing); dedup TTL shorter than redelivery window; idempotency record written non-atomically with the business effect; uncompensatable side effect placed mid-saga. [INFERRED]

### S5: CQRS & Event Sourcing

Separate read and write models; optionally store state as a sequence of events. [EXPLICIT]

**CQRS:**
- Command side: validates writes, emits domain events
- Query side: optimized read models (denormalized views, materialized projections)
- Sync: domain events update query-side projections asynchronously

CQRS inescapably makes the read model *eventually consistent* with the write model — a user who writes then immediately reads may not see their own change. Mitigate per-flow: read-your-writes via session-pinned reads from the write model, or optimistic UI that assumes success. Do not pretend the lag is zero. [INFERRED]

**Event Sourcing:**
- State stored as immutable event sequence, not current state
- Aggregates reconstruct state by replaying events
- Snapshots: capture state every N events (100-500) to avoid full replay
- Temporal queries: "what was the state at time T?"
- Event upcasting: transform old event formats during replay

**Decision criteria:**
- CQRS without event sourcing: simpler, valuable for read/write optimization
- Event sourcing without CQRS: possible but loses optimized-reads benefit
- Full event sourcing: only when audit trail, temporal queries, or replay are hard requirements
- Event store options: EventStoreDB (purpose-built), Kafka (with compaction), PostgreSQL, DynamoDB

**The cost nobody budgets for: schema evolution of stored events.** In event sourcing the event log is *forever*, so every old event format must remain replayable forever via upcasting — you can never simply "migrate the table." This is the single biggest reason not to adopt event sourcing casually. Adopt it only when audit/temporal/replay is a *hard* requirement, and version events from day one. [INFERRED]

**Concurrency in event sourcing:** appends to one aggregate's stream must use optimistic concurrency (expected version) — two commands reading version N and both appending N+1 corrupt the stream. The event store's conditional-append (compare-and-set on stream version) is non-negotiable, not optional. [INFERRED]

**S5 acceptance criteria:** read/write split justified by divergent access patterns, not fashion; read-model staleness has a named mitigation per user-facing flow; event sourcing adopted only against a hard audit/temporal/replay requirement; if sourced — snapshot cadence set, upcasting strategy defined, optimistic-concurrency append in place. [INFERRED]

**S5 failure modes:** event sourcing adopted for "it's modern" with no temporal/audit need (permanent complexity tax); read-your-writes ignored (users see stale data after their own action); no snapshots → replay time grows unbounded; missing optimistic concurrency → corrupted aggregate streams; un-versioned events that become unreplayable after the first schema change. [INFERRED]

### S6: Operational Excellence

Ensure event systems are reliable, observable, and recoverable in production. [EXPLICIT]

**Dead-Letter Topic (DLT) Management:**
- Route events that fail after max retries (3-5 attempts with exponential backoff)
- DLT schema: original event + error metadata (reason, timestamp, consumer, attempt count)
- Monitor: alert on DLT depth >0 (new), age of oldest message >1h (stale)
- Categorize failures: schema mismatch (fix schema), business rule (fix logic), transient (auto-retry)
- Replay workflow: fix consumer -> replay DLT to original topic -> verify processing

Retry vs. DLT routing depends on error class: transient (network, timeout, 5xx) → in-place retry with backoff; deterministic (schema mismatch, failed validation, business-rule reject) → straight to DLT, because retrying a deterministic failure just burns the retry budget and head-of-line-blocks the partition. Classify *before* retrying, not after. [INFERRED]

**Poison Pill Detection:**
- Circuit breaker: stop processing after 3 consecutive failures on same partition
- Quarantine: move poison pills to separate topic for manual analysis

A poison pill (one event that always fails deserialization/processing) head-of-line-blocks its whole partition under strict ordering — every later event behind it stalls. This is the failure that takes down a whole consumer group silently: lag climbs on one partition while others are healthy. Quarantine-and-skip restores flow; the trade-off is that skipping breaks per-key ordering for that key, so flag it for manual reconciliation. [INFERRED]

**Consumer Lag Monitoring:**
- Warning threshold: 1000 messages behind
- Critical threshold: 10000 messages behind
- Auto-scale trigger: add consumer instances when lag exceeds warning for >5 minutes
- Tool: Burrow, Kafka Lag Exporter, or built-in consumer group describe

Lag thresholds are starting defaults, not laws — calibrate to *time-to-drain*, not raw count. 10k messages behind is fine at 100k msg/sec (0.1s) and catastrophic at 10 msg/sec (16 min). Alert on `lag / throughput = projected delay` where the SLA lives, and remember autoscaling consumers past `partition count` adds idle instances, not throughput — repartition or shard instead. [INFERRED]

**Event Replay:**
- Selective: by aggregate ID, time range, or event type
- Isolation: replay into separate projection, validate, then switch
- Safety: idempotent handlers prevent side effects; use replay flag header

Replay safety depends on consumers distinguishing replayed from live events (the `replay` header): a replay must *not* re-fire external side effects (re-charge a card, re-send an email) — only rebuild internal projections. Replaying through a consumer that calls external systems, without gating on the flag, causes real-world double-effects. This is why side-effecting and projection-building handlers should be separate consumers. [INFERRED]

**Observability:** Distributed tracing with correlationId through entire event chain. Metrics: producer rate, consumer rate, lag, DLT depth, processing duration histograms.

The four signals that catch most event-system incidents: (1) **consumer lag** per partition (skew reveals hot partitions/poison pills); (2) **DLT depth + oldest-age** (silent processing failures); (3) **end-to-end latency** via correlationId span (producer-emit → consumer-commit, not just per-hop); (4) **redelivery/duplicate rate** (rising = a non-idempotent consumer or a relay double-publishing). Without (1)+(2) wired to alerts, failures surface as downstream data drift hours later. [INFERRED]

**S6 acceptance criteria:** DLT defined with error-class-aware routing (transient→retry, deterministic→DLT) and monitored on depth+age; poison-pill circuit breaker + quarantine in place; lag alerting expressed as projected time-delay against SLA, not raw count; replay gated by a `replay` header that suppresses external side effects; the four core signals wired to alerts. [INFERRED]

**S6 failure modes:** deterministic errors retried into a head-of-line block; poison pill stalls a partition undetected; lag alert on raw count fires false/late across volume changes; autoscaling past partition count (idle consumers, no gain); replay double-firing external side effects; DLT growing with no alert until downstream drift is reported by users. [INFERRED]

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Kafka** | High throughput, replay, persistence | Ops complexity, partition management | High-volume, event sourcing, log-based |
| **RabbitMQ** | Flexible routing, low latency, simpler ops | No replay, limited persistence | Task queues, RPC, moderate volume |
| **Cloud-native (Pub/Sub, SNS+SQS)** | Near-zero ops, managed scaling | Limited replay, vendor lock-in | Low ops budget, serverless, volume fits tier |
| **Orchestrated Saga** | Clear flow, centralized error handling | Coordinator coupling | Complex multi-step, financial transactions |
| **Choreographed Saga** | Loose coupling, independent deployment | Hard to trace, debug | Simple 2-3 service workflows |
| **Event Sourcing** | Full audit, temporal queries, replay | Complexity, storage growth, forever-replayable schema | Financial, compliance, audit-critical domains |
| **CQRS without ES** | Read/write optimization, simpler | Projection sync, eventual consistency | Reporting-heavy, different read/write patterns |
| **Outbox Pattern** | Reliable publishing, transactional guarantee | Additional table, relay infrastructure | Any event system needing reliability |
| **Thin (notification) event** | Schema independence, small payload | Read amplification, temporal coupling | Default; consumer has API access |
| **Fat (state-transfer) event** | Self-contained, low latency | Producer schema becomes public contract | Callback latency/availability breaks SLA |

---

## Assumptions

- System has multiple services needing asynchronous communication
- Team understands distributed systems trade-offs (CAP, eventual consistency)
- Infrastructure supports message broker deployment (managed or self-hosted)
- Event volume and latency requirements are quantifiable
- At-least-once delivery is the baseline guarantee; "exactly-once business effect" is achieved by idempotency, not by the broker [INFERRED]
- The team can run a schema registry in CI; without it, compatibility claims are unenforceable [INFERRED]

## Limits

- Focuses on event-driven architecture patterns, not infrastructure provisioning
- Does not design REST/GraphQL APIs
- Does not implement data pipelines
- Event sourcing adds significant complexity — not recommended unless audit/temporal queries required
- Distributed tracing across event chains requires dedicated tooling investment
- Does not cover stream *processing/analytics* (windowed aggregation, joins) — transport and store only [INFERRED]
- Does not size brokers (broker count, instance type, disk) — that is a provisioning/infra exercise downstream of the category choice [INFERRED]

---

## Edge Cases

**Migrating from Synchronous to Event-Driven:** Strangler fig pattern. Identify highest-value async boundaries first (long-running processes, fan-out notifications). Run sync and async in parallel during transition. Dual-run with the sync path as source of truth and the async path shadow-writing; compare outputs before cutting over — the parallel window is where you catch missing events and ordering bugs cheaply. [INFERRED]

**Schema Evolution in Production:** Consumers at different versions. Backward-compatible changes only. Deploy consumers before producers when adding required fields. Schema registry enforces compatibility.

**Event Ordering Across Partitions:** Global ordering is expensive. Most systems need per-entity ordering (same partition key). If cross-entity ordering matters, single partition (throughput trade-off) or timestamp-based reconciliation. Note: timestamp reconciliation needs a *trusted* clock source — wall-clock skew across producers reorders events; prefer a logical sequence/version on the entity over raw timestamps. [INFERRED]

**High-Volume Event Storms:** Burst traffic overwhelms consumers. Use backpressure, consumer auto-scaling, circuit breakers. DLT prevents one bad event from blocking the stream. Cap autoscaling at partition count and shed/queue beyond it — scaling consumers past partitions buys nothing. [INFERRED]

**Multi-Region:** Cross-region replication adds latency. Define global vs. regional events. Use CRDTs or last-writer-wins for cross-region consistency. Decide replication topology explicitly — active-active needs conflict resolution (CRDT/LWW); active-passive needs a defined failover and offset-reset story or replay re-fires events post-failover. [INFERRED]

**Late / Duplicate Events:** A redelivery arrives after the entity has moved on (e.g. `Cancelled` after `Shipped`). Consumers must be not just idempotent but *order-tolerant* — guard state transitions on the entity's current version, dropping events that target a stale version rather than blindly applying them. [INFERRED]

---

## Validation Gate

Before finalizing delivery, verify:

- [ ] Event catalog covers all domain and integration events with schemas
- [ ] CloudEvents envelope adopted or justified alternative documented
- [ ] Naming conventions consistent (`Domain.Entity.Action`, past tense, versioned in type)
- [ ] Domain vs. integration event boundary explicit (no leaked internal events) [INFERRED]
- [ ] Broker selection justified via the heuristic with the deciding factor named (acks, replication, retention specified)
- [ ] Kafka durability quartet set where Kafka chosen (`acks=all`, RF≥3, `min.insync.replicas=2`, `enable.idempotence=true`) [INFERRED]
- [ ] Schema registry enforces backward(-transitive) compatibility with CI/CD gating; semantic-breaking changes versioned `.vN` [INFERRED]
- [ ] Saga type matches workflow complexity (orchestration vs. choreography)
- [ ] Every saga step has an idempotent compensation; uncompensatable steps last [INFERRED]
- [ ] Outbox pattern specified for reliable publishing with relay choice justified and concurrency/retention pitfall handled [INFERRED]
- [ ] Idempotency designed into every consumer (dedup key = producer event id, TTL > max redelivery window, written atomically) [INFERRED]
- [ ] DLT monitoring (depth + age), error-class routing, categorization, and replay procedures defined
- [ ] Replay gated by a header that suppresses external side effects [INFERRED]
- [ ] Consumer lag alerting expressed as projected delay vs. SLA with auto-scaling triggers (capped at partition count) [INFERRED]

---

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | ✅ | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

Default output is Markdown with embedded Mermaid diagrams. HTML generation requires explicit `{FORMATO}=html` parameter. [EXPLICIT]

## Output Artifact

**Primary:** `A-01_Event_Architecture.html` — Executive summary, event catalog, broker architecture, schema registry design, consistency patterns, CQRS/event sourcing design, operational runbook.

**Secondary:** AsyncAPI specifications, event schema definitions, saga flow diagrams, DLT handling procedures, consumer lag dashboard configuration.

---
**Author:** Javier Montano | **Last updated:** June 11, 2026
