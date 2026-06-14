# Example output — firebase (topic: firestore-security-rules, deep)

> Resolved topic: `firestore-security-rules` · depth: `deep`

## 1. Request & scope
- **Ask:** owner-only read/edit of notes, admin read-any, immutable `ownerId`, and a
  "newest first" own-notes listing (FR-031).
- **Topic resolution:** access control + immutable-field invariant → `firestore-security-rules`.
  The listing's ordering needs a composite index — flagged for `firestore-queries`. [INFERENCE]
- **Out of scope:** Storage/RTDB rules (different semantics); raw GCP IAM.

## 2. Service / context matrix
| Requirement | Firebase service | Adjacent GCP | Notes |
|-------------|------------------|--------------|-------|
| FR-031 access control | Firestore + Auth | — | admin via custom claim `role=admin` |
| FR-031 listing | Firestore index | — | composite `(ownerId, createdAt)` |

## 3. Design
### Security Rules (`firestore.rules`)
```
match /databases/{db}/documents {
  function signedIn() { return request.auth != null; }
  function isOwner(uid) { return signedIn() && request.auth.uid == uid; }
  function isAdmin() { return signedIn() && request.auth.token.role == 'admin'; }

  match /notes/{noteId} {
    allow get:    if isOwner(resource.data.ownerId) || isAdmin();
    allow list:   if isOwner(request.query.where.ownerId);  // forces own-notes query
    allow create: if isOwner(request.resource.data.ownerId)
                  && request.resource.data.keys().hasAll(['ownerId','body','createdAt'])
                  && request.resource.data.createdAt == request.time;
    allow update: if isOwner(resource.data.ownerId)
                  && request.resource.data.ownerId == resource.data.ownerId; // ownerId immutable
    allow delete: if isOwner(resource.data.ownerId) || isAdmin();
  }
}
```
The `list` rule is stricter than `get`; the client MUST scope its query
`where('ownerId','==',uid)` or the entire list is rejected — rules don't filter. [EXPLICIT]

### Composite index (`firestore.indexes.json`) — flag for firestore-queries
```json
{ "collectionGroup": "notes", "queryScope": "COLLECTION",
  "fields": [ { "fieldPath": "ownerId", "order": "ASCENDING" },
              { "fieldPath": "createdAt", "order": "DESCENDING" } ] }
```
Without it the ordered query throws `FAILED_PRECONDITION` at runtime. [INFERENCIA]

## 4. Emulator tests (allow AND deny)
| Path | Allow case | Deny case |
|------|-----------|-----------|
| get | owner reads own note | other user reads it → denied |
| list | `where ownerId==uid` query | unscoped list → denied |
| create | owner with `createdAt==request.time` | spoofed `ownerId` → denied |
| update | body edit by owner | changing `ownerId` → denied |
| delete | owner or admin | other user → denied |
Run with the rules-unit-testing SDK, NOT the Admin SDK (Admin bypasses rules). [EXPLICIT]

## 5. Cost estimate (no prices)
~5,000 users × 50 list loads/day. With `limit(20)` + cursor the list bills ~20 reads/load
→ ~5M reads/day before caching; client persistence (~40% repeat-view hit) trims it. Use
`count()` for any "total notes" badge instead of reading docs. Estimate at stated scale,
not a quote; verify quotas in the pricing console. [SUPUESTO]

## 6. Validation Gate
- [x] Every operation (get/list/create/update/delete) ruled; deny-by-default [EXPLICIT]
- [x] `ownerId` immutable asserted across `resource.data` / `request.resource.data` [EXPLICIT]
- [x] `list` rule satisfiable by the real client query [EXPLICIT]
- [x] Composite index defined for the ordered listing [INFERENCIA]
- [x] Emulator covers allow AND deny per path [EXPLICIT]
- [x] No price quoted; single brand; no client PII [DOC]

## 7. Evidence log
`[EXPLICIT]` rules mechanics from references/firestore-security-rules.md ·
`[INFERENCIA]` missing-index runtime failure · `[SUPUESTO]` cost estimate vs live quotas.
