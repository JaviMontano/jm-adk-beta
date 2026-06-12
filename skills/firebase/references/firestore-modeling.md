<!-- distilled from alfa skills/firestore-modeling -->
<!-- > -->
# Firestore Modeling

> "In NoSQL, you model for your queries — not for your data." — Unknown

## TL;DR

Guides Firestore data modeling decisions — choosing between subcollections and root collections, when to denormalize, how to structure document references, and managing document size limits. Use when designing or refactoring Firestore database schemas for scalability and query efficiency. [EXPLICIT]

## Scope & Anti-Scope

- IN: collection layout, embed-vs-reference, denormalization, counters, document-size budgeting, collection-group access. [EXPLICIT]
- OUT: writing the security rules themselves (→ `firestore-security-rules`), query/index tuning (→ `firestore-queries`), backups, multi-region/replication strategy. [SUPUESTO]

## Hard Limits (design against these, not around them) [DOC]

- Document max size: **1 MiB**; field value max depth: 20 levels; max 40k index entries/doc.
- Single document write rate: **~1 write/sec sustained** before contention — the root cause of the counter-sharding pattern below. [INFERENCIA]
- `in` / `array-contains-any` queries cap at **30 values**; `!=`/`not-in` scan-heavy. Model so hot reads avoid them.
- Collection-group queries match subcollections by **collection ID**, not path — IDs must be unique-by-intent across the tree. [DOC]

## Procedure

### Step 1: Discover
- List all data entities and their relationships (1:1, 1:N, N:N).
- Identify the primary queries the application needs to perform; rank by frequency.
- Check current data access patterns (reads vs writes ratio) — write-heavy fields resist denormalization. [INFERENCIA]
- Review existing data model if migrating from SQL or another NoSQL.

### Step 2: Analyze
- Map each query to the collection structure that serves it with a single read.
- Decide subcollection vs root collection (query scope: within parent vs across all).
- Identify denormalization opportunities (user name on posts, counts on parent docs).
- Evaluate document size constraints (1 MiB limit, avoid unbounded arrays).
- Decision rule: **read-frequency × fan-out** drives denormalization; **write-frequency** drives against it. [INFERENCIA]

### Step 3: Execute
- Design root collections for independently queryable entities.
- Use subcollections when data is naturally scoped to a parent (user → orders).
- Denormalize frequently read fields to avoid extra lookups; record the source of truth.
- Use collection group queries for cross-parent subcollection access.
- Implement counters with distributed counter pattern (for high write throughput).
- Add `createdAt` and `updatedAt` server timestamps (`serverTimestamp()`) to all documents.
- Document the data model with entity relationship diagrams.

### Step 4: Validate
- Verify every screen's data needs can be met with 1-2 Firestore reads.
- Check that no document exceeds 1 MiB or contains unbounded arrays.
- Confirm denormalized data has update propagation strategy (Cloud Function triggers).
- Test query performance with realistic data volumes (1000+ documents).

## Decision Matrix [INFERENCIA]

| Question | Choose | Rationale |
|----------|--------|-----------|
| Need to query entity on its own, across all parents? | Root collection | Subcollection scope is per-parent unless collection-group + index |
| Data only meaningful inside one parent, bounded count? | Subcollection | Natural scoping, cheaper rules |
| 1:N where N is large/unbounded (comments, events)? | Subcollection (never array) | Arrays hit 1 MiB; subcollections page |
| 1:N where N is tiny + always read with parent (≤ ~20 tags)? | Embedded array/map | Saves a read; stays well under limit |
| N:N (users ↔ groups)? | Join via membership docs or dual arrays of IDs | Mirror writes; pick by which side queries hot |
| Field read on every list view but owned elsewhere? | Denormalize + propagate | Trade write cost for read count |

## Worked Examples [INFERENCIA]

**Blog — denormalize author onto post.** `posts/{id}` stores `authorId`, plus `authorName`+`authorPhotoUrl` copied from `users/{authorId}`. Feed renders in 1 read instead of N+1. Propagation: Cloud Function on `users/{id}` update fan-outs to that author's posts. Trade-off: stale name until trigger completes (seconds) — acceptable for display, not for auth. [SUPUESTO]

**E-commerce — orders under user.** `users/{uid}/orders/{orderId}`: scoped, secured by `request.auth.uid == uid`, no index gymnastics. Admin "all orders today" view uses a **collection-group** query on `orders` + composite index on `createdAt`. [DOC]

**Likes — sharded counter.** A viral post exceeds 1 write/sec on `posts/{id}.likeCount`. Split into `posts/{id}/counterShards/{0..N}`, each `+1` to a random shard; read = sum of shards. Pick N ≈ peak writes/sec. [DOC]

## Quality Criteria

- [ ] Every primary query served by a single collection/subcollection read.
- [ ] No unbounded arrays in documents (use subcollections instead).
- [ ] Denormalized data has a documented update propagation strategy + named source of truth.
- [ ] Document structure supports required security rules without custom claims gymnastics.
- [ ] No single hot document expected to exceed ~1 write/sec (else shard).
- [ ] Subcollection nesting ≤ 2 levels.
- [ ] Evidence tags applied to all claims.

## Anti-Patterns

- Modeling Firestore like a relational database with normalized tables and joins.
- Storing arrays that grow without limit inside documents.
- Deep nesting subcollections beyond 2 levels (queries become complex).
- Denormalizing a field that changes more often than it is read (write amplification > read savings). [INFERENCIA]
- Sequential or monotonic document IDs on a high-write collection (hotspots the index). [DOC]
- Using a single document as a global counter/aggregate under load (see sharded counter). [INFERENCIA]

## Failure Modes [INFERENCIA]

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `RESOURCE_EXHAUSTED` / contention on writes | Hot single document > 1 write/sec | Shard the document/counter |
| Document write rejected | > 1 MiB, often an unbounded array | Move array to subcollection |
| Cross-parent query returns nothing | Used path query, needed collection-group + index | Switch to `collectionGroup()`, add index |
| Stale denormalized field | No/failed propagation trigger | Add Cloud Function; treat copy as cache, not truth |
| List view does N+1 reads | Under-denormalized | Copy the display field onto the listed doc |

## Related Skills

- `firestore-queries` — query patterns depend on data model design.
- `firestore-security-rules` — rules must align with document structure.

## Usage

Example invocations:

- "/firestore-modeling" — Run the full firestore modeling workflow.
- "firestore modeling on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Limits reflect Firestore Native mode; Datastore mode differs. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Read-heavy field owned by another entity | Denormalize; name source of truth + propagation trigger |
| N:N relationship | Membership-doc join or dual ID arrays; mirror writes |
| Hot single-doc counter | Distributed/sharded counter, N ≈ peak writes/sec |
