<!-- distilled from alfa skills/rate-limiting -->
<!-- > -->
# Rate Limiting
> "Method over hacks."
## TL;DR
Design API rate limits, throttling, quota management, and abuse prevention. Pick an algorithm, choose an identity key, set limits from real traffic, enforce at the edge, and fail safe. [EXPLICIT]

## Algorithm Selection
| Algorithm | Burst handling | Memory/key | Use when | Trade-off |
|-----------|----------------|-----------|----------|-----------|
| Token bucket | Allows bursts up to bucket size | O(1): tokens + timestamp | Default for APIs; smooth + bursty | Tuning two params (rate, capacity) [INFERENCIA] |
| Leaky bucket | Smooths to constant outflow | O(1) | Strict downstream rate caps (queues) | Adds latency; drops on overflow [INFERENCIA] |
| Fixed window | None (resets on boundary) | O(1) counter | Cheapest, coarse quotas | 2x burst at window edges [DOC] |
| Sliding window log | Exact | O(n) per key (timestamps) | Low-volume, precision-critical | Memory grows with traffic [INFERENCIA] |
| Sliding window counter | Approximate | O(1) | High-volume APIs needing accuracy | ~0.003% error vs exact [DOC] |

Decision: token bucket is the default; switch to sliding-window-counter when window-edge bursts cause incidents. [INFERENCIA]

## Procedure
### Step 1: Discover
- Identify the limit key: API key > user ID > session > IP. IP-only is last resort (NAT/CGNAT collisions, trivial rotation). [EXPLICIT]
- Baseline from logs: p50, p99, peak RPS per key. Set initial limit ≈ p99 × 1.5. [INFERENCIA]
### Step 2: Analyze
- Choose algorithm (table above) per Constitution XIII/XIV. Define tiers (anon/free/paid) and per-endpoint overrides for expensive routes. [EXPLICIT]
### Step 3: Execute
- Enforce at the edge (gateway/CDN) before app compute; centralize counters (e.g. Redis INCR+EXPIRE or atomic Lua) so limits hold across instances. [INFERENCIA]
- Return `429` + headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, and `Retry-After` on block. [DOC]
### Step 4: Validate
- Load-test at and above the limit; confirm `429` triggers exactly at threshold and counters are shared across nodes. [EXPLICIT]

## Quality Criteria
- [ ] Limit key chosen and justified (not IP-only) [EXPLICIT]
- [ ] Algorithm + limits traceable to baseline traffic [EXPLICIT]
- [ ] Distributed counter is atomic (no read-modify-write race) [EXPLICIT]
- [ ] `429` + `Retry-After` + `RateLimit-*` headers returned [DOC]
- [ ] Fail-open vs fail-closed decision documented [EXPLICIT]

## Failure Modes
| Failure | Consequence | Mitigation |
|---------|-------------|------------|
| Counter store (Redis) down | All requests blocked or all allowed | Decide fail-open (availability) vs fail-closed (protection); default fail-open with alert [SUPUESTO] |
| Non-atomic increment | Race lets limit be exceeded under load | Atomic INCR / Lua / token-bucket script [INFERENCIA] |
| Per-instance counters | Effective limit = N × intended | Centralize or shard deterministically by key [INFERENCIA] |
| Clock skew across nodes | Windows misalign, uneven enforcement | Use store-side TTL/time, not app clock [INFERENCIA] |
| Retry storm after 429 | Thundering herd at reset | `Retry-After` + jittered backoff guidance [DOC] |

## Usage
Example invocations:
- "/rate-limiting" — Run the full rate limiting workflow
- "rate limiting on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and traffic logs for baselining [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Covers application-layer limiting only; volumetric DDoS needs network/CDN scrubbing upstream [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Trusted internal/service traffic | Allowlist by key or bypass with audit, never by IP alone [INFERENCIA] |
| Shared IP behind NAT/CGNAT | Prefer authenticated key; widen IP limits to avoid blocking legit users [INFERENCIA] |
| Counter backend unavailable | Apply documented fail-open/closed policy; emit alert [SUPUESTO] |
