<!-- distilled from alfa skills/firebase-architecture -->
<!-- End-to-end Firebase project architecture. Firestore schema strategy, Cloud Functions topology, Hosting config, Security Rules design. C4 diagram output. [EXPLICIT] -->
# firebase-architecture {Architecture} (v1.0)
> **"Firebase is the platform. Architecture is how you use it without hitting walls."**
## Purpose
Designs complete Firebase project architecture covering Firestore data model, Cloud Functions topology, Hosting configuration, Security Rules strategy, and service integration patterns. [EXPLICIT]
**When to use:**
- Starting a new Firebase project
- Redesigning an existing Firebase architecture
- When `/jm:design-architecture` targets Firebase
## Core Principles
1. **Law of Denormalization:** Firestore rewards reading over writing. Model for your queries, not your entities. Duplicate fields a read needs rather than join. Trade-off: writes fan out to N copies; reconcile via a Firestore-trigger that updates duplicates on source change. [EXPLICIT]
2. **Law of Triggers:** Cloud Functions react to events. Design event chains, not request chains. Triggers are at-least-once and unordered — every handler must be idempotent (guard on a processed-marker doc/field). [EXPLICIT]
3. **Law of Rules:** Security Rules are your last line, not your only line. Design them BEFORE implementation; they cannot do joins or call out, so push authorization data (role, ownership) into the document or custom claims. [EXPLICIT]
4. **Law of Cost:** Every query is N document reads + index reads. A collection-group query over millions of docs is a billing event, not just a perf event. Estimate read/write volume per feature before committing the schema. [INFERENCIA]
## Core Process
### Phase 1: Service Selection
1. Map FR-XXX requirements to Firebase services (Auth, Firestore, Functions, Hosting, Storage). [EXPLICIT]
2. Identify Google Cloud services needed (Cloud Tasks, Pub/Sub, Secret Manager). [EXPLICIT]
3. Identify third-party integrations (Algolia, SendGrid, Stripe). [EXPLICIT]
### Phase 2: Architecture Design
1. Design Firestore collection hierarchy (top-level collections, subcollections, composite indexes). [EXPLICIT]
2. Design Cloud Functions topology (HTTP triggers, Firestore triggers, Auth triggers, scheduled). [EXPLICIT]
3. Design Security Rules strategy (role-based via custom claims, resource-based). [EXPLICIT]
4. Design Hosting config (rewrites for SPA, headers, preview channels). [EXPLICIT]
5. Produce C4 context and container diagrams (Mermaid). [EXPLICIT]
### Phase 3: Document
1. Write architecture document with service matrix. [EXPLICIT]
2. Create ADR for significant decisions. [EXPLICIT]
3. Estimate Firebase costs (reads/writes/invocations). [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| spec.md or requirements | File/Text | Yes | FR-XXX list with query/access patterns [EXPLICIT] |
| Existing Firebase config | `firebase.json`, `firestore.rules`, `firestore.indexes.json` | No | Present when redesigning; read before changing [SUPUESTO] |
| Expected scale | Text | No | Doc counts + read/write rates; drives cost + index design. Absent → flag `[SUPUESTO]` and design for the stated tier [INFERENCIA] |

| Output | Type | Description |
|--------|------|-------------|
| Architecture document | Markdown | Service matrix + Firestore schema + Functions topology + Rules strategy |
| C4 diagrams | Mermaid | Context + container; embedded in the doc |
| ADR(s) | File | One per significant decision, with rejected alternatives |
| Cost estimate | Table | Reads/writes/invocations per feature at expected scale |

## Worked Example (mini)
Requirement FR-012: "users see their own orders, newest first." [EXPLICIT]
- **Schema:** top-level `orders/{orderId}` with `userId`, `createdAt`, denormalized `userName` (avoids a second read). Not a subcollection under `users/` — keeps a single collection-group query simple. [EXPLICIT]
- **Index:** composite `(userId ASC, createdAt DESC)` in `firestore.indexes.json`. Without it the query throws `FAILED_PRECONDITION` at runtime, not at deploy. [INFERENCIA]
- **Rule:** `allow read: if request.auth.uid == resource.data.userId;` — ownership lives on the doc, no join needed. [EXPLICIT]
- **Trigger:** `onUpdate(users/{uid})` reconciles `userName` across that user's orders; idempotent (writes only if changed). [EXPLICIT]

## Validation Gate
- [ ] Every FR-XXX maps to ≥1 Firebase/GCP service in the matrix [EXPLICIT]
- [ ] Each Firestore query has a backing collection shape AND composite index [INFERENCIA]
- [ ] Each denormalized field names the trigger that keeps it consistent [EXPLICIT]
- [ ] Security Rules cover read + write per collection; default-deny confirmed [EXPLICIT]
- [ ] Every Functions trigger handler is idempotent (at-least-once safe) [EXPLICIT]
- [ ] C4 context + container diagrams render (valid Mermaid) [EXPLICIT]
- [ ] Cost estimate present at expected scale; hotspots flagged [EXPLICIT]
- [ ] No AWS/Azure references (R-002); no Docker/K8s (R-003) [EXPLICIT]
## 5. Self-Correction Triggers
> [!WARNING]
> IF designing SQL-style normalized schema THEN **STOP**. Firestore requires denormalization.
> IF adding Docker/K8s to architecture THEN **STOP**. Use Firebase Hosting + Hostinger (R-003).

## Usage

Example invocations:

- "/firebase-architecture" — Run the full firebase architecture workflow
- "firebase architecture on this project" — Apply to current context


## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs); English output unless specified [EXPLICIT]
- Designs architecture only — does not write app code, deploy, or run migrations [EXPLICIT]
- Cost figures are estimates from stated scale, not a quote; no prices, FTE-months only [SUPUESTO]
- Does not replace domain-expert judgment for final decisions [EXPLICIT]

## Anti-Scope (out of bounds)
- Multi-cloud / AWS / Azure designs (R-002) and Docker/K8s topologies (R-003) [EXPLICIT]
- Relational/SQL schema modeling — Firestore is the target store [EXPLICIT]
- Live data migration plans, load testing, or production deploys — separate skills [SUPUESTO]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification; do not auto-invent requirements [EXPLICIT] |
| Conflicting requirements | Flag explicitly, propose resolution, get sign-off before designing [EXPLICIT] |
| Out-of-scope request | Redirect to the appropriate skill or escalate [EXPLICIT] |
| Query needs OR / multiple range filters | Firestore cannot; split into reads or denormalize a query field [INFERENCIA] |
| Read needs data across many docs | Use a denormalized aggregate doc updated by trigger, not a fan-out read [INFERENCIA] |
| Hot document (counter, leaderboard) | >1 write/sec contends; shard the counter across N subdocs [INFERENCIA] |
| Unbounded subcollection growth | Document write/storage cost; consider TTL or archival collection [SUPUESTO] |
| Cross-doc atomicity required | Use a transaction or batched write; Rules alone cannot enforce it [INFERENCIA] |
