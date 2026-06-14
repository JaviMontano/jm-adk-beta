<!-- distilled from alfa skills/data-validation -->
<!-- Client-side Zod/Yup schemas. Server-side Cloud Functions validation. Firestore rules validation. End-to-end type safety. [EXPLICIT] -->
# data-validation {Data} (v1.1)
> **"Data is the product. Model it for queries, secure it with rules, back it up daily."**
## Purpose
End-to-end type safety across three enforcement layers: client (Zod/Yup), server (Cloud Functions), and Firestore Security Rules. [EXPLICIT]
**When to use:** Database design, data management, or analytics within the Firebase ecosystem.
**Anti-scope:** Not for relational/SQL modeling, not a substitute for Rules (client validation is UX, never a security boundary), not for analytics pipeline validation (see data-quality.md). [EXPLICIT]

## Core Principles
1. **Law of Queries:** Design schema for read patterns. Firestore charges per document read/write — denormalize to serve a screen in one query. [EXPLICIT]
2. **Law of Rules:** Security Rules are mandatory and are the only real security boundary. No collection ships without rules. [EXPLICIT]
3. **Law of Backups:** Production data gets scheduled backups. No exceptions. [EXPLICIT]
4. **Law of Single Source:** Define the schema once (Zod), derive client types and the server validator from it — never hand-maintain three copies. [INFERENCIA]

## Defense in Depth (why three layers)
| Layer | Enforces | Trusts client? | Failure if skipped |
|-------|----------|----------------|--------------------|
| Client (Zod/Yup) | UX, fast feedback | n/a | Slow round-trips, poor errors — NOT a breach |
| Cloud Function | Business invariants, cross-doc checks | No | Invalid writes via direct SDK; corrupt state |
| Security Rules | Auth + shape at the DB | No | **Data breach** — any client can read/write |
Decision: client validation never authorizes; Rules + Functions assume the client is hostile. Trade-off: schema duplication cost is paid to keep the DB closed by default. [EXPLICIT]

## Core Process
### Phase 1: Design data model from requirements.
Enumerate every read (screen → query). Shape collections around those reads; accept controlled duplication.
### Phase 2: Implement with security rules and indexes.
Author Rules per collection (deny-by-default), define composite indexes for every compound/order-by query, derive the server validator from the Zod schema.
### Phase 3: Test with emulator. Validate rules. Set up backups.
Run the Rules unit-test suite in the emulator (allow + deny cases), confirm indexes, schedule backups.

## Validation Gate (acceptance criteria)
- [ ] Schema designed for actual query patterns (each screen ≤ 1-2 queries)
- [ ] Security rules cover **all** collections; default is `allow read, write: if false`
- [ ] Composite indexes defined for every compound/order-by query
- [ ] Backup strategy documented with cadence + restore-tested
- [ ] No SQL-style normalized design in Firestore
- [ ] Same schema source drives client types and server validator
- [ ] Rules test suite has both passing (authorized) and failing (denied) assertions

## Worked Example (single source → three layers)
```ts
// schema.ts — single source of truth
export const Order = z.object({
  uid: z.string(),                 // owner
  total: z.number().nonnegative(), // invariant
  status: z.enum(["pending","paid","shipped"]),
});
// client: Order.parse(form)  → typed, instant errors
// function: Order.parse(req.data) → reject bad writes, enforce total ≥ 0
```
```js
// firestore.rules — the security boundary
match /orders/{id} {
  allow read, write: if request.auth.uid == resource.data.uid;
}
```

## Usage

Example invocations:

- "/data-validation" — Run the full data validation workflow
- "data validation on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes Firestore (not Realtime DB or external SQL) as the store [INFERENCIA]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Rules and indexes are environment-scoped — verify per project/env before promoting [INFERENCIA]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Client validates but Rules don't | **Breach** — treat as critical; Rules must re-check everything |
| Compound query with no index | Firestore throws at runtime — add composite index, never strip the query |
| Schema changed, old docs remain | Validators must tolerate legacy shapes; plan a migration (see schema-evolution.md) |
| Read pattern needs a join | Denormalize or fan-out; do not normalize to SQL-style refs |
