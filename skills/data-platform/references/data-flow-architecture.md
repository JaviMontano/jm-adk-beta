<!-- distilled from alfa skills/data-flow-architecture -->
<!-- Firebase real-time sync patterns. Firestore triggers to Cloud Functions event chains. Data pipeline design. [EXPLICIT] -->
# data-flow-architecture {Architecture} (v1.1)
> **"Architecture is decisions. Document every one."**
## Purpose
Firebase real-time sync patterns. Firestore triggers to Cloud Functions event chains. Data pipeline design. [EXPLICIT]
**When to use:** Designing or reviewing data-flow architecture for Firebase/Google stack projects.
**When NOT to use (anti-scope):** multi-cloud or AWS/Azure targets (violates R-002); pure UI/state design with no data movement; infra provisioning (use an IaC skill); cost modeling (out of scope — no prices). [INFERENCE]
## Core Principles
1. **Law of Firebase-First:** All decisions constrained to Firebase/Google ecosystem (R-002). [EXPLICIT]
2. **Law of Evidence:** Every claim tagged `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, or `[ASSUMPTION]` — one tag per claim, EN spelling throughout (canon: references/verification-tags.md). [EXPLICIT]
3. **Law of Diagrams:** Architecture without diagrams is incomplete. Use Mermaid for C4, sequence, flow. [EXPLICIT]
## Core Process
### Phase 1: Analyze requirements and constraints.
Capture data volume, latency target, read/write ratio, consistency need, and trigger fan-out. Flag any non-Firebase dependency now. [INFERENCE]
### Phase 2: Design architecture with Firebase/Google services.
Map each data movement to a service (Firestore, Realtime DB, Cloud Functions, Pub/Sub, BigQuery export). Decide sync vs. async per hop. [INFERENCE]
### Phase 3: Document with C4 diagrams, decision records, and evidence tags.

## Key Decisions & Trade-offs
| Decision | Choose | Trade-off accepted | Tag |
|----------|--------|--------------------|-----|
| Firestore vs Realtime DB | Firestore for queries/scale; RTDB for low-latency presence | Firestore charges per-doc read; RTDB lacks rich queries | [INFERENCE] |
| Trigger chain vs Pub/Sub fan-out | Pub/Sub when >2 consumers or retries needed | Extra topic to operate; at-least-once delivery | [INFERENCE] |
| Sync write vs async trigger | Async trigger for derived/aggregated data | Eventual consistency; client cannot read-after-write | [ASSUMPTION] |

## Failure Modes
- **Trigger loops:** a Function writes a doc that re-fires its own trigger. Guard with a sentinel field or path scoping. [INFERENCE]
- **Duplicate processing:** Functions are at-least-once; make handlers idempotent (dedupe key in event id). [DOC]
- **Fan-out write storms:** one parent update fanning to N children exhausts quota. Batch or debounce. [INFERENCE]
- **Hidden cross-cloud dep:** a "small" API call leaks the design off Firebase, breaking R-002. Reject at Phase 1. [INFERENCE]

## Worked Example
Order placed → `orders/{id}` write → `onCreate` Function validates → publishes `order-confirmed` to Pub/Sub → two subscribers: inventory decrement (idempotent on `orderId`) and BigQuery export. Sequence + C4 container diagram in Mermaid; ADR records the Pub/Sub-over-direct-trigger choice. [INFERENCE]

## Validation Gate
- [ ] Designed within Firebase/Google/Hostinger constraints (R-002)
- [ ] C4 or sequence diagrams produced (Mermaid)
- [ ] One evidence tag per non-obvious claim, single family, consistent spelling
- [ ] ADR created for each significant decision and its trade-off
- [ ] Handlers idempotent; trigger loops and fan-out storms addressed
- [ ] No AWS/Azure/Docker references

## Acceptance Criteria
Output is complete when the Validation Gate passes AND every data hop maps to a named Firebase/Google service with sync-vs-async stated and a failure mode considered. [INFERENCE]

## Usage
Example invocations:
- "/data-flow-architecture" — Run the full data flow architecture workflow
- "data flow architecture on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- No cost/pricing estimates — capacity stated in qualitative terms only [INFERENCE]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Non-Firebase service required | Stop; flag R-002 violation, do not design around it [INFERENCE] |
