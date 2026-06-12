<!-- distilled from alfa skills/firestore-security-rules -->
<!-- Rules authoring: request.auth, request.resource, resource.data. Custom claims. Role-based. Rate limiting in rules. [EXPLICIT] -->
# firestore-security-rules {Data} (v1.1)
> **"Data is the product. Model it for queries, secure it with rules, back it up daily."**
## Purpose
Author and validate Firestore Security Rules: `request.auth`, `request.resource`, `resource.data`, custom claims, role-based access, in-rules rate limiting. [EXPLICIT]
**When to use:** Database design, data management, or analytics within the Firebase ecosystem.

## Core Principles
1. **Law of Queries:** Design schema for read patterns. Firestore bills per document read/write/delete, not per query. [EXPLICIT]
2. **Law of Rules:** Rules are mandatory and deny-by-default; an unmatched path is denied. No collection ships without an explicit rule. [EXPLICIT]
3. **Law of Backups:** Production data gets scheduled backups (PITR or scheduled export). No exceptions. [EXPLICIT]
4. **Rules are auth, not validation-only:** they cannot call out, cannot aggregate a query, and run per-document. Enforce cross-doc invariants in trusted server code (Admin SDK bypasses rules). [EXPLICIT]

## Core Process
### Phase 1: Design data model from requirements.
### Phase 2: Implement with security rules and indexes.
### Phase 3: Test with emulator. Validate rules. Set up backups.

## Rules Mechanics (canonical)
- `request.auth` — null when unauthenticated; gate every write on `request.auth != null` first. [EXPLICIT]
- `request.auth.token.<claim>` — custom claims for roles; set via Admin SDK, propagates after token refresh (up to 1h on existing sessions). [EXPLICIT]
- `resource.data` — the document **as stored** (pre-write on update/delete). `request.resource.data` — the **incoming** state. Use both to validate diffs. [EXPLICIT]
- `allow read` = `get` + `list`; split them when list must be narrower than get. `allow write` = `create` + `update` + `delete`; split for field-level control. [EXPLICIT]
- Rules do not filter queries. A `list` rule must be satisfiable by the query's constraints, or the whole query is rejected — it never returns a partial set. [INFERENCE]

## Worked Examples
```
// Owner-only doc, role-gated admin override, immutable owner field
match /databases/{db}/documents {
  function signedIn()  { return request.auth != null; }
  function isOwner(uid){ return signedIn() && request.auth.uid == uid; }
  function isAdmin()   { return signedIn() && request.auth.token.role == 'admin'; }

  match /notes/{noteId} {
    allow get:    if isOwner(resource.data.ownerId) || isAdmin();
    allow list:   if isAdmin();                          // forces narrow query for non-admins
    allow create: if isOwner(request.resource.data.ownerId)
                  && request.resource.data.keys().hasAll(['ownerId','body','createdAt'])
                  && request.resource.data.createdAt == request.time;
    allow update: if isOwner(resource.data.ownerId)
                  && request.resource.data.ownerId == resource.data.ownerId; // owner immutable
    allow delete: if isOwner(resource.data.ownerId) || isAdmin();
  }
}
```
Rate-limit by writing `createdAt == request.time` and checking the prior doc's timestamp via `get(/databases/$(db)/documents/...)`; note each `get()`/`exists()` call is a billed read and counts against the 10-call-per-request limit. [EXPLICIT]

## Validation Gate
- [ ] Schema designed for actual query patterns
- [ ] Every collection AND subcollection has an explicit rule (no reliance on parent match)
- [ ] Writes validate `request.resource.data.keys()` (reject unexpected fields) and types
- [ ] Immutable fields asserted equal between `resource.data` and `request.resource.data`
- [ ] `list` rules satisfiable by real client queries (tested, not assumed)
- [ ] Indexes defined for compound queries
- [ ] Backup strategy documented (PITR window or export schedule)
- [ ] No SQL-style normalized design in Firestore
- [ ] Emulator unit tests cover allow AND deny for each path

## Failure Modes
| Failure | Cause | Fix |
|---------|-------|-----|
| Query rejected, single `get` works | `list` rule stricter than query; rules don't filter | Add query constraints that satisfy the `list` rule |
| Custom claim ignored after role change | Token not refreshed | Force `getIdToken(true)` or wait for refresh; don't expect instant propagation |
| Write passes emulator, fails prod | Admin SDK used in test (bypasses rules) | Test with the rules-unit-testing client SDK, not Admin SDK |
| `request.resource.data` null on delete | Delete carries no incoming data | Gate deletes on `resource.data`, never `request.resource.data` |

## Anti-Scope
- Not query-level row filtering (rules gate access, never slice result sets) nor cross-document aggregate limits at scale — enforce server-side. [EXPLICIT]
- Does not cover Storage or RTDB rules (different syntax/semantics). [EXPLICIT]

## Usage
- "/firestore-security-rules" — Run the full firestore security rules workflow
- "firestore security rules on this project" — Apply to current context

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
