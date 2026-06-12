<!-- distilled from alfa skills/domain-driven-design -->
<!-- > -->
# Domain-Driven Design

> "The heart of software is its ability to solve domain-related problems for its user." — Eric Evans

## TL;DR

Models complex business domains using DDD strategic and tactical patterns — bounded contexts, aggregates, entities, value objects, domain events, and ubiquitous language. Use this skill when tackling complex business logic, designing microservice boundaries, or when the team and domain experts speak different languages. [EXPLICIT]

**Strategic** patterns (bounded contexts, context maps, subdomain classification) decide *where* boundaries go; **tactical** patterns (aggregates, entities, value objects, events) decide *how* to model inside one. Get strategic design wrong and no tactical polish saves it — boundaries are the expensive mistake. [EXPLICIT]

## When to Use / When NOT

- USE: rich invariant-heavy domains, microservice decomposition, legacy untangling, glossary drift between business and code. [EXPLICIT]
- NOT: CRUD apps with no real business rules (DDD overhead exceeds value), pure data pipelines (use `data-engineering`), technical/infrastructure concerns with no domain language. Applying full DDD to a thin CRUD service is the most common waste. [EXPLICIT]

## Procedure

### Step 1: Discover
- Conduct domain exploration through event storming or domain storytelling sessions
- Identify key business processes, actors, and domain terminology
- Classify subdomains: **Core** (competitive advantage — invest most), **Supporting** (needed, not differentiating — build simply), **Generic** (buy/adopt off-the-shelf, never custom-build). Mis-investing engineering in a generic subdomain is a classic strategic error. [EXPLICIT]
- Search the codebase for existing domain models, entities, and naming conventions

### Step 2: Analyze
- Define bounded contexts by identifying linguistic boundaries (same word, different meaning — e.g., "Customer" means billing entity in Sales, support profile in Service). [EXPLICIT]
- Map context relationships using a Context Map (see matrix below)
- Identify aggregates by grouping entities that share transactional consistency boundaries
- Extract domain events that represent meaningful state transitions

**Context-Mapping Pattern Selector:** [EXPLICIT]

| Pattern | Relationship | Use when |
|---|---|---|
| **Shared Kernel** | Two contexts co-own a small shared model | Tightly aligned teams; willing to coordinate every change |
| **Customer/Supplier** | Downstream's needs prioritized upstream | Upstream team accepts downstream as a stakeholder |
| **Conformist** | Downstream adopts upstream model as-is | No leverage over upstream; their model is good enough |
| **Anti-Corruption Layer (ACL)** | Downstream translates at the boundary | Upstream model is messy/legacy; protect your model |
| **Open Host + Published Language** | Upstream offers a stable public contract | Many downstreams; want to avoid bespoke integrations |
| **Separate Ways** | No integration | Integration cost exceeds value |

Default to ACL when integrating with anything legacy or externally owned — it is the cheapest insurance against upstream model rot. [EXPLICIT]

### Step 3: Execute
- Document the ubiquitous language glossary with precise definitions
- Design aggregate roots with invariant enforcement and consistency boundaries
- Define domain events with clear schemas and publish/subscribe contracts
- Create value objects for concepts defined by attributes rather than identity (Money, DateRange, Address) — immutable, compared by value, self-validating. [EXPLICIT]
- Map bounded context integration patterns (ACL, Published Language, Open Host)

**Aggregate design rules:** [EXPLICIT]
1. One aggregate root per aggregate; external code references the root only, never inner entities.
2. Keep aggregates small — prefer referencing other aggregates by ID, not by object reference.
3. One aggregate = one transaction. Cross-aggregate consistency is eventual, via domain events.
4. The root enforces all invariants; if an invariant spans two aggregates, the boundary is probably wrong.

**Worked example (Order aggregate):** Root `Order` holds `OrderLine` entities + `Money total` value object. Invariant: `total == Σ(line.subtotal)` and `total <= customer.creditLimit`, enforced inside `Order.addLine()`. `Order` references `Customer` by `customerId` (not the Customer object) — Customer is a separate aggregate. Placing a line emits `OrderLinePlaced`; the credit check on another aggregate happens via the event, not a synchronous call inside the transaction. [EXPLICIT]

**Domain-event schema (past tense, immutable fact):** [EXPLICIT]
```
OrderPlaced { eventId, occurredAt, orderId, customerId, total, currency, correlationId }
```
Carry enough data for downstream consumers to act without a callback, but not internal aggregate state. Name in past tense — events are history, not commands.

### Step 4: Validate
- Verify aggregate boundaries enforce all business invariants
- Confirm ubiquitous language is used consistently in code, tests, and documentation
- Check that bounded contexts have clear ownership and integration contracts
- Validate domain events capture all meaningful state transitions

## Decision Trade-offs

| Decision | Enables | Costs | Choose when |
|---|---|---|---|
| **Small aggregates** | Scalability, low contention, clear ownership | More eventual consistency to manage | High concurrency; default choice |
| **Large aggregate** | Strong immediate consistency | Lock contention, scaling limits | Invariants truly span all members |
| **ACL at boundary** | Model isolation from legacy/external | Translation code + mapping maintenance | Upstream model is unstable or messy |
| **Conformist (no ACL)** | Zero translation cost | Upstream changes leak into your model | Upstream is clean and you have no leverage |
| **Event-driven cross-context** | Loose coupling, autonomy | Eventual consistency, harder tracing | Contexts owned by different teams |

## Quality Criteria

- [ ] Bounded contexts have explicit boundaries and documented relationships
- [ ] Subdomains classified (core/supporting/generic) and investment aligned accordingly
- [ ] Aggregates enforce consistency invariants within their boundary; cross-aggregate refs are by ID
- [ ] Ubiquitous language glossary exists and matches code naming
- [ ] Domain events are named in past tense and carry sufficient data
- [ ] Each context-map relationship names its integration pattern
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Anemic domain model: entities with only getters/setters and no behavior — logic leaks into services. [EXPLICIT]
- God aggregate: single aggregate that encompasses the entire domain — kills concurrency and scaling. [EXPLICIT]
- Leaking bounded context: sharing internal models across context boundaries (no ACL/published language). [EXPLICIT]
- Ubiquitous language drift: glossary says one thing, code names another — the model and reality diverge silently. [EXPLICIT]
- Premature DDD: full tactical machinery on a CRUD subdomain where it adds only ceremony. [EXPLICIT]

## Failure Modes

- Aggregate too large -> transaction contention, deadlocks under load. Fix: split by true invariant boundaries. [EXPLICIT]
- Synchronous cross-aggregate writes in one transaction -> distributed-transaction fragility. Fix: domain events + eventual consistency. [EXPLICIT]
- No ACL against legacy upstream -> their schema changes break your core. Fix: translation layer at the boundary. [EXPLICIT]

## Related Skills

- `event-architecture` — implements domain events technically
- `system-architecture` — bounded contexts inform service decomposition
- `flow-mapping` — visualizes the business processes DDD models

## Usage

Example invocations:

- "/domain-driven-design" — Run the full domain driven design workflow
- "domain driven design on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes a real domain with non-trivial business rules; CRUD-only systems are out of scope [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Models the domain — does not provision infrastructure or design transport-layer APIs (use `api-architecture`) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Same term, different meaning across teams | Split into separate bounded contexts; do not force one shared model |
| Invariant spans two aggregates | Re-examine boundaries; relax to eventual consistency via events if the split is correct |
| Legacy/external model you cannot change | Wrap with an Anti-Corruption Layer; never let it leak inward |
