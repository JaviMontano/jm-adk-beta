<!-- distilled from alfa skills/realtime-architecture -->
<!-- > -->
# Realtime Architecture

> "Real-time is not about speed. It's about relevance." — Unknown

## TL;DR

Designs real-time data synchronization architectures using Firestore listeners, Firebase RTDB, WebSockets, and SSE for live collaborative features, dashboards, and notifications. Use this skill when building chat systems, live dashboards, collaborative editing, or any feature requiring instant data propagation. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify features requiring real-time updates vs. polling
- Assess data update frequency and payload sizes
- Review current real-time infrastructure and connection limits
- Map real-time data flows: who produces updates, who consumes them

### Step 2: Analyze
- Choose the right technology per use case:
  - **Firestore Listeners**: document/collection sync with offline support
  - **Firebase RTDB**: low-latency presence, typing indicators, counters
  - **WebSockets**: custom binary protocols, gaming, full-duplex communication
  - **SSE**: server-to-client streaming, event logs, notifications
- Design data granularity: listen to documents vs. collections vs. queries
- Plan connection management: reconnection, exponential backoff, connection pooling
- Address conflict resolution: last-write-wins, operational transform, CRDTs

### Step 3: Execute
- Implement Firestore snapshot listeners with proper unsubscribe lifecycle
- Design real-time data models optimized for listener performance (small documents)
- Implement presence system using Firebase RTDB for online/offline status
- Build optimistic UI updates with rollback on server rejection
- Set up connection monitoring and user feedback for connectivity changes
- Implement fan-out patterns for multi-recipient real-time updates

### Step 4: Validate
- Verify listeners are detached on component unmount (no memory leaks)
- Test reconnection behavior after network interruption
- Confirm real-time updates are received within acceptable latency (<500ms)
- Check Firestore read costs are manageable with current listener patterns

## Quality Criteria

- [ ] Listeners have proper lifecycle management (subscribe/unsubscribe)
- [ ] Optimistic updates show immediate feedback with error rollback
- [ ] Connection state changes are communicated to users
- [ ] Real-time data models minimize document size for efficient sync
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Listening to entire collections when only a subset is needed
- Missing listener cleanup causing memory leaks and phantom updates
- Using real-time sync for data that only needs periodic refresh

## Related Skills

- `state-management` — integrating real-time data with client state
- `event-architecture` — server-side event patterns feeding real-time clients
- `auth-architecture` — Firestore security rules for real-time access control

## Usage

Example invocations:

- "/realtime-architecture" — Run the full realtime architecture workflow
- "realtime architecture on this project" — Apply to current context


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
