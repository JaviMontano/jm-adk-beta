<!-- distilled from alfa skills/firebase-cost-optimization -->
<!-- Firestore read/write reduction, Functions cold start mitigation, Storage lifecycle rules, and billing alerts -->
# 100 — Firebase Cost Optimization {Performance}

## Purpose
Minimize Firebase operational costs while maintaining application performance. Reduce Firestore reads/writes via efficient query patterns, mitigate Cloud Functions cold starts, and enforce storage lifecycle management. [EXPLICIT]

**Anti-scope** (out of bounds): query *correctness* or data modeling for features (separate concern); CDN/Hosting bandwidth tuning; BigQuery export costs; security-rule design except where it forces redundant reads. Optimize cost only after a feature works — premature denormalization is a common own-goal. [INFERENCIA]

## Physics — 3 Immutable Laws

1. **Law of Read Reduction**: Every Firestore document read bills. Cache aggressively, paginate always, denormalize strategically. Never read more documents than the UI renders. A `count()` aggregation bills 1 read per 1000 matched docs — far cheaper than reading them. [EXPLICIT]
2. **Law of Function Efficiency**: Cloud Functions bill per invocation AND per GB-second of compute. Minimize cold starts, cut execution duration, suppress unnecessary triggers (a write that fires a function that writes can loop). [EXPLICIT]
3. **Law of Storage Hygiene**: Unused Storage objects bill monthly until deleted. Lifecycle rules delete temp files; user-uploaded originals are removed after processing. Deletes are free; storage accrues silently. [EXPLICIT]

## Protocol

### Phase 1 — Firestore Optimization
1. **Pagination**: Every list query uses `limit()` + cursor (`startAfter`). Never `getDocs()` unbounded. [EXPLICIT]
2. **Caching**: Enable persistence (`enablePersistence()` / `persistentLocalCache`). Try `getDocFromCache()` before `getDocFromServer()`. [EXPLICIT]
3. **Denormalization**: Store computed/aggregated fields to avoid fan-out reads; maintain via Function triggers. Trade-off: write amplification + consistency lag — justified only when read:write ratio is high (read-heavy lists, counters). [INFERENCIA]
4. **Composite queries**: Replace N queries with composite indexes; `in` operator batches lookups (max 30 values per query). [EXPLICIT]
5. **Aggregations over reads**: Use `count()`/`sum()`/`average()` aggregation queries instead of reading docs to tally. [EXPLICIT]
6. **Listener management**: `onSnapshot` MUST unsubscribe on unmount. Orphan listeners re-bill on every server change. [EXPLICIT]

### Phase 2 — Cloud Functions Optimization
1. **Min instances**: `minInstances: 1` on latency-critical functions removes cold starts. Trade-off: you pay for idle warm instances 24/7 — apply only where p99 latency matters, not batch jobs. [INFERENCIA]
2. **Lazy imports**: Import heavy SDKs inside the handler, not at module top, so cold starts skip unused code paths. [EXPLICIT]
3. **Regional colocation**: Deploy functions in the same region as Firestore — cuts latency and avoids cross-region egress. [EXPLICIT]
4. **Batch triggers**: Prefer `onWrite` batch handling over per-doc `onCreate` for bulk operations. [EXPLICIT]
5. **Right-size memory/timeout**: Start at 128MB; raise only if profiling shows CPU/OOM. Set timeout to observed max +20%. More memory = more vCPU = sometimes *cheaper* if it cuts duration. [INFERENCIA]
6. **Concurrency (Gen2)**: Set `concurrency: 80` so one instance serves many requests, slashing instance count for I/O-bound work. [CONFIG]
7. **Idempotency**: Triggers can fire more than once (at-least-once delivery). Guard writes with a processed-marker to avoid double-billing side effects. [INFERENCIA]

### Phase 3 — Storage & Billing Controls
1. **Lifecycle rules**: Auto-delete temp objects after 7 days via Cloud Storage lifecycle policy. [EXPLICIT]
2. **Image cleanup**: Delete the original once the resize extension emits derivatives (keep resized only). [EXPLICIT]
3. **Billing alerts**: Set at 50%, 80%, 100% of monthly budget in Cloud Console. Alerts notify; they do NOT stop spend. [EXPLICIT]
4. **Hard cap**: For non-prod projects, wire a budget Pub/Sub trigger to a Function that disables billing — the only true stop. [CONFIG]

## I/O

| Input | Output |
|-------|--------|
| Firestore query patterns | Paginated, cached, aggregation-backed queries |
| Cloud Functions config | Right-sized memory/timeout, min instances, concurrency |
| Storage file inventory | Lifecycle rules + post-process cleanup |
| Monthly budget | Alerts at 50/80/100% + hard-cap on non-prod |

## Worked Example — Cost Driver Math
A list view reads 500 docs/page-load, 10k loads/day = 5M reads/day. Adding `limit(20)` + cursor → 20 reads/load = 200k reads/day (25x cut). Layering client persistence (≈40% cache hit on repeat views) → ≈120k/day. The `in`-batch and `count()` swaps remove the remaining per-row fan-out reads. [INFERENCIA]

## Quality Gates — 6 Checks
1. **Every query bounded** — `limit()` present; no unbounded `getDocs`. [EXPLICIT]
2. **Persistence enabled** — offline cache active on client. [EXPLICIT]
3. **No orphan listeners** — every `onSnapshot` has a matching unsubscribe. [EXPLICIT]
4. **Min instances on critical paths** — measured cold start < 500ms. [EXPLICIT]
5. **Billing alerts at 50/80/100%** — plus hard-cap on non-prod. [EXPLICIT]
6. **Storage lifecycle active** — temp objects auto-expire ≤ 7 days. [EXPLICIT]

## Failure Modes
- **Trigger write-loop**: a Function writing the doc that triggered it recurses → runaway invocations. Gate on a changed-field check or short-circuit when source == self. [INFERENCIA]
- **Min-instances bill shock**: warm instances priced 24/7; a forgotten `minInstances` on a rarely-used function quietly drains budget. [INFERENCIA]
- **Cache staleness**: `getDocFromCache()` can serve stale data; never use cache-first for money/auth-critical reads. [SUPUESTO] Verify by comparing cached vs server doc on a sentinel field.
- **Lifecycle deletes live data**: an over-broad prefix in the lifecycle rule deletes production objects. [SUPUESTO] Verify rule against a dry-run inventory before enabling.

## Edge Cases
- **Listener explosion**: share one listener per collection via context/store, not one per component instance. [EXPLICIT]
- **Spark (free) tier limits**: 50k reads/day, 20k writes/day, 1GiB stored — hard caps, not overage-billed. Monitor before launch. [EXPLICIT]
- **Egress**: free within the same region; cross-region reads incur egress charges. [EXPLICIT]
- **Aggregation ceiling**: `count()` still bills ≥1 read and has its own index needs on large sets. [INFERENCIA]

## Self-Correction Triggers
- Billing > 80% budget → audit top cost drivers in Cloud Console reports first.
- Firestore reads > 50k/day → review queries, add caching/aggregation, increase denormalization.
- Function cold start > 2s → add min instances, lazy-import, re-profile memory.
- Storage cost trending up → run inventory, confirm lifecycle, purge unused assets.

## Usage
- `/firebase-cost-optimization` — run the full workflow.
- "firebase cost optimization on this project" — apply to current context.

## Assumptions & Limits
- Assumes access to project artifacts (code, configs, billing console). [EXPLICIT]
- Pricing tiers and free-tier quotas change; verify current rates in the Firebase/GCP pricing console before acting on numbers here. [SUPUESTO]
- English-language output unless otherwise specified. [EXPLICIT]
- Advises, does not replace, domain-expert judgment on final cost/architecture trade-offs. [EXPLICIT]
