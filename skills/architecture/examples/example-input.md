# Example input — architecture

A concrete request that routes to the `api-design` topic.

---

> We're launching a public REST API for our **orders** service. Consumers are a
> web frontend, a partner integration, and our own mobile app. We expect order
> lists to grow into the tens of thousands per merchant. We need: a versioning
> strategy we won't regret, pagination that doesn't skip rows when orders are
> being created concurrently, a consistent error format, and retry-safe order
> creation. Give us the contract decisions, not an implementation.

Parameters the router should infer:
- `topic`: **api-design** (contract design for a REST API — not system
  decomposition, not caching).
- `depth`: **deep** (public contract, hard to reverse → exhaustive).
