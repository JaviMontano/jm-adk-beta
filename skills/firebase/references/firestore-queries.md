<!-- distilled from alfa skills/firestore-queries -->
<!-- > -->
# Firestore Queries

> "The right index turns an impossible query into an instant one." — Unknown

## TL;DR

Guides efficient Firestore query implementation — compound `where` filters, composite index management, cursor pagination (`startAfter`/`limit`), server-side aggregation (count/sum/average), and real-time listeners with cleanup. Use when building data-fetching logic against Firestore. [DOC]

## Procedure

### Step 1: Discover
- List all queries the app needs (by screen or feature) and their filter/sort shape
- Read existing `firestore.indexes.json` for declared composite indexes [CONFIG]
- Identify queries combining multi-field filter + `orderBy` (these force a composite index) [DOC]
- Inventory `onSnapshot` listeners and where each unsubscribes

### Step 2: Analyze
- Decide composite-index vs single-field per query (multi-field `where`/range + `orderBy` → composite) [DOC]
- Choose pagination: cursor (`startAfter`) by default; offset only for known-small skips
- Decide server- vs client-side aggregation (prefer server for cost + correctness) [INFERENCIA]
- Identify queries needing `collectionGroup` scope (same-named subcollections across parents)

### Step 3: Execute
- Chain `where()` → `orderBy()` → `limit()`; keep the orderBy field consistent with the cursor field
- Declare composite indexes in `firestore.indexes.json`; the console error link emits the exact JSON [CONFIG]
- Paginate by storing the last `DocumentSnapshot` and passing it to `startAfter(lastDoc)` (not field values, to avoid ties) [DOC]
- Aggregate with `getCountFromServer` / `getAggregateFromServer({ count, sum, average })`
- Register `onSnapshot` and return its `unsubscribe` from the effect/teardown path
- Map errors to user messages: `failed-precondition` → missing index; `permission-denied` → rules [DOC]

### Step 4: Validate
- No "missing index" / `failed-precondition` errors in console or logs
- Pagination boundaries pass: empty result, single page, exact-multiple page, last partial page
- Every listener unsubscribes on unmount (assert no growth in active listener count)
- Profile against a large collection via the emulator before shipping

## Worked Example

Paginated, filtered, sorted query with a composite index:

```js
// Query: active orders for a user, newest first, 20 per page
const q = query(
  collection(db, "orders"),
  where("userId", "==", uid),
  where("status", "==", "active"),
  orderBy("createdAt", "desc"),
  limit(20),
  ...(lastDoc ? [startAfter(lastDoc)] : [])
);
const snap = await getDocs(q);
const lastDoc = snap.docs[snap.docs.length - 1]; // cursor for next page
```

```json
// firestore.indexes.json — required composite index for the query above
{ "collectionGroup": "orders", "queryScope": "COLLECTION", "fields": [
  { "fieldPath": "userId",    "order": "ASCENDING" },
  { "fieldPath": "status",    "order": "ASCENDING" },
  { "fieldPath": "createdAt", "order": "DESCENDING" }
] }
```

## Key Decisions & Trade-offs

| Decision | Choice | Trade-off |
|----------|--------|-----------|
| Pagination | Cursor (`startAfter(snapshot)`) | Stable under inserts; cannot jump to arbitrary page N. [DOC] |
| Aggregation | Server (`getCountFromServer`) | 1 read-equivalent cost, always fresh; no live updates (re-call to refresh). [DOC] |
| Read shape | Narrow `where` + `limit` | Lower cost; needs a matching composite index per filter/sort combo. [INFERENCIA] |
| Listener vs get | `onSnapshot` only when UI must react | Live updates cost continued reads; one-shot `getDocs` is cheaper for static views. [INFERENCIA] |

## Quality Criteria

- [ ] All composite indexes declared in `firestore.indexes.json` and deployed
- [ ] Pagination is cursor-based (snapshot cursor, not field values or offset)
- [ ] Listeners cleaned up on teardown (verified, not assumed)
- [ ] Query errors handled with fallback UI distinguishing index vs rules failures
- [ ] Evidence tags applied to all non-obvious claims

## Anti-Patterns

- `offset(n)` for pagination — reads and bills for every skipped doc [DOC]
- Fetching a whole collection to filter/sort in the client — cost and latency scale with collection size
- Leaving `onSnapshot` unsubscribed — memory leaks plus phantom reads after teardown
- Cursoring on a field value instead of a snapshot — duplicates/skips rows on ties [DOC]
- `!=` / `not-in` / `array-contains-any` assumed cheap — they fan out and have per-query operator limits [DOC]

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `failed-precondition: requires an index` | Missing composite index | Follow console link → paste JSON into `firestore.indexes.json` → deploy [CONFIG] |
| `permission-denied` on a valid-looking query | Rules block the read shape | Align `firestore.rules` with the query; rules are not filters [DOC] |
| Pagination skips/duplicates rows | Cursor on field values across ties | Cursor on the last `DocumentSnapshot` instead [DOC] |
| `invalid-argument` on range + orderBy | First `orderBy` must match the range/inequality field | Order by the inequality field first [DOC] |
| Listener fires forever / leak | No `unsubscribe()` on teardown | Return unsubscribe from effect cleanup |

## Related Skills

- `firestore-modeling` — query efficiency depends on data model design
- `firestore-security-rules` — rules must allow the queries being performed

## Usage

Example invocations:

- "/firestore-queries" — Run the full firestore queries workflow
- "firestore queries on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- English-language output unless otherwise specified [SUPUESTO]
- Targets native-mode Firestore client SDKs (web/mobile); Datastore mode and Admin SDK pagination differ [DOC]
- Does not replace domain expert judgment for final decisions [DOC]
- Anti-scope: index deployment pipelines, billing/quota tuning, and rules authoring (see related skills) [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Query needs index not yet built | Surface the console link; index builds are async and may lag deploy [DOC] |
| `collectionGroup` across deep nesting | Confirm subcollection name uniqueness before scoping [INFERENCIA] |
