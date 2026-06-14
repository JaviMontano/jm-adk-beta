<!-- distilled from alfa skills/realtime-architecture -->
<!-- > -->
# Realtime Architecture

> "Real-time is not about speed. It's about relevance." — Unknown

## TL;DR

Designs real-time data synchronization architectures using Firestore listeners, Firebase RTDB, WebSockets, and SSE for live collaborative features, dashboards, and notifications. Use this skill when building chat systems, live dashboards, collaborative editing, or any feature requiring instant data propagation. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify features needing push (sub-second relevance) vs. those a 30–60s poll serves more cheaply [EXPLICIT]
- Quantify update frequency, payload size, fan-out ratio (1 writer → N readers), and peak concurrent connections — these drive cost and tech choice [EXPLICIT]
- Review current infrastructure and connection limits (Firestore: ~1M concurrent listeners/db; RTDB: 200k concurrent connections/instance) [EXPLICIT]
- Map data flows: who produces updates, who consumes them, and the acceptable staleness per flow

### Step 2: Analyze — technology selection

Pick per use case using the matrix; mixing technologies per-flow is expected, not a smell. [EXPLICIT]

| Tech | Best for | Trade-off accepted | Avoid when |
|------|----------|--------------------|------------|
| **Firestore listeners** | Document/collection sync, offline-first, security-rule-gated reads | Cost scales with reads × listeners; ~1s typical latency | High-frequency counters/presence (read-cost blowup) |
| **Firebase RTDB** | Presence, typing, counters, sub-100ms low-latency | Weaker querying; JSON-tree modeling discipline required | Complex relational queries, large documents |
| **WebSockets** | Full-duplex, binary protocols, gaming, custom ordering | You own reconnection, scaling, auth, backpressure | A managed listener already fits (avoid rebuilding it) |
| **SSE** | Server→client streams: event logs, notifications, AI token streaming | Unidirectional; one HTTP connection per stream | Client must also push frequently (use WS) |

- Design granularity: prefer query/document listeners over whole-collection; narrower scope = fewer reads and tighter security rules [EXPLICIT]
- Plan connection management: reconnection with exponential backoff + jitter, heartbeat/keepalive, connection pooling
- Choose conflict resolution by need: last-write-wins (simple, lossy), operational transform (text editing), CRDTs (offline-heavy multi-writer). Decide before coding — retrofitting is expensive. [EXPLICIT]

### Step 3: Execute
- Implement Firestore snapshot listeners with explicit unsubscribe tied to component/lifecycle teardown
- Model data for listener efficiency: small documents, denormalized read shapes, no unbounded arrays that re-send on every change [EXPLICIT]
- Implement presence via RTDB `onDisconnect()` so offline status fires even on ungraceful drop [EXPLICIT]
- Build optimistic UI: apply locally, reconcile/rollback on server rejection, surface the rollback to the user
- Monitor connection state and signal connectivity changes (online/offline/reconnecting) in the UI
- Implement fan-out for multi-recipient updates (write-time fan-out to per-recipient paths) when read-time fan-in would over-read

### Step 4: Validate
- Verify every listener detaches on unmount — assert zero active listeners after teardown (no leaks, no phantom updates)
- Test reconnection after forced network interruption: backoff bounded, no thundering-herd reconnect, state re-syncs correctly
- Confirm propagation latency within target (default budget <500ms p95; tighten/loosen per flow and record the number) [EXPLICIT]
- Project Firestore read cost at peak: `concurrent_listeners × writes/sec × matched_docs`; confirm it stays within budget [EXPLICIT]

## Quality Criteria

- [ ] Each real-time flow has a documented tech choice + justification from the matrix
- [ ] Listeners have explicit subscribe/unsubscribe lifecycle; teardown verified
- [ ] Optimistic updates show immediate feedback with error rollback surfaced to the user
- [ ] Connection-state changes are communicated to users
- [ ] Conflict-resolution strategy chosen and documented before implementation
- [ ] Read-cost projection computed and within budget
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Listening to entire collections when a query/subset suffices (read-cost and security-rule blowup)
- Missing listener cleanup → memory leaks and phantom updates
- Real-time sync for data that only needs periodic refresh (push where poll would do)
- Unbounded documents (growing arrays) that re-transmit fully on every small change
- Reconnect storms: synchronized retries with no jitter after a mass disconnect
- Rebuilding reconnection/auth/scaling on raw WebSockets when a managed listener already fits

## Failure Modes

| Symptom | Likely cause | Mitigation |
|---------|--------------|------------|
| Firestore bill spikes | Broad collection listeners on hot-write docs | Narrow query scope; move counters/presence to RTDB |
| Memory grows over session | Listeners not unsubscribed on navigation | Tie unsubscribe to lifecycle; assert zero on teardown |
| Stale UI after reconnect | No re-sync on reconnection | Re-fetch/re-attach and reconcile on `connected` event |
| Presence stuck "online" | Relying on graceful disconnect only | RTDB `onDisconnect()` server-side cleanup |
| Duplicate/echoed local writes | Optimistic write not de-duped vs. server echo | Tag local mutations; reconcile by id |

## Worked Example — chat with presence

- Messages: Firestore listener on `rooms/{id}/messages` ordered query, limited to last N; new docs stream in [EXPLICIT]
- Typing + online status: RTDB under `presence/{room}/{user}` with `onDisconnect()` cleanup (avoids Firestore read-cost for high-churn signals) [EXPLICIT]
- Send: optimistic insert with client-generated id → reconcile on server ack, rollback + retry affordance on failure
- Result: relational message history (Firestore) and high-frequency ephemeral signals (RTDB) each on the fitting tech [EXPLICIT]

## Related Skills

- `state-management` — integrating real-time data with client state
- `event-architecture` — server-side event patterns feeding real-time clients
- `auth-architecture` — Firestore/RTDB security rules for real-time access control

## Usage

Example invocations:

- "/realtime-architecture" — Run the full realtime architecture workflow
- "realtime architecture on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes a Firebase-centric stack; raw WebSocket/SSE guidance is provider-agnostic but examples lean Firebase [EXPLICIT]
- Connection/concurrency limits cited are platform defaults and change over time — confirm against current quotas before sizing [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Anti-Scope

- Backend event-bus / pub-sub topology → `event-architecture`
- Security-rule authoring depth → `auth-architecture`
- Client-state container design → `state-management`
- Cost-optimization beyond read-projection sizing → out of scope; escalate to a cost review

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Offline-first multi-writer | Default to CRDT/OT; flag if last-write-wins data loss is acceptable [EXPLICIT] |
| Fan-out to very large audiences | Move from per-client listeners to write-time fan-out or a broadcast channel |
