<!-- distilled from alfa skills/firestore-modeling -->
<!-- > -->
# Firestore Modeling

> "In NoSQL, you model for your queries — not for your data." — Unknown

## TL;DR

Guides Firestore data modeling decisions — choosing between subcollections and root collections, when to denormalize, how to structure document references, and managing document size limits. Use when designing or refactoring Firestore database schemas for scalability and query efficiency. [EXPLICIT]

## Procedure

### Step 1: Discover
- List all data entities and their relationships (1:1, 1:N, N:N)
- Identify the primary queries the application needs to perform
- Check current data access patterns (reads vs writes ratio)
- Review existing data model if migrating from SQL or another NoSQL

### Step 2: Analyze
- Map each query to the collection structure that serves it with a single read
- Decide subcollection vs root collection (query scope: within parent vs across all)
- Identify denormalization opportunities (user name on posts, counts on parent docs)
- Evaluate document size constraints (1MB limit, avoid unbounded arrays)

### Step 3: Execute
- Design root collections for independently queryable entities
- Use subcollections when data is naturally scoped to a parent (user → orders)
- Denormalize frequently read fields to avoid extra lookups
- Use collection group queries for cross-parent subcollection access
- Implement counters with distributed counter pattern (for high write throughput)
- Add `createdAt` and `updatedAt` server timestamps to all documents
- Document the data model with entity relationship diagrams

### Step 4: Validate
- Verify every screen's data needs can be met with 1-2 Firestore reads
- Check that no document exceeds 1MB or contains unbounded arrays
- Confirm denormalized data has update propagation strategy (Cloud Function triggers)
- Test query performance with realistic data volumes (1000+ documents)

## Quality Criteria

- [ ] Every primary query served by a single collection/subcollection read
- [ ] No unbounded arrays in documents (use subcollections instead)
- [ ] Denormalized data has a documented update propagation strategy
- [ ] Document structure supports required security rules without custom claims gymnastics
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Modeling Firestore like a relational database with normalized tables and joins
- Storing arrays that grow without limit inside documents
- Deep nesting subcollections beyond 2 levels (queries become complex)

## Related Skills

- `firestore-queries` — query patterns depend on data model design
- `firestore-security-rules` — rules must align with document structure

## Usage

Example invocations:

- "/firestore-modeling" — Run the full firestore modeling workflow
- "firestore modeling on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
