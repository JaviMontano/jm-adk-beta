# firebase — Body of Knowledge

Domain knowledge for the Firebase platform router. Concepts, standards, and
decision rules that the playbooks share. Evidence-tagged throughout.

## 1. Platform surface (in scope)
Auth, Firestore (Native mode), Cloud Functions (2nd gen, Node 20), Hosting,
Storage, Extensions, the Emulator Suite, deployment, and cost. Adjacent GCP that
Firebase pulls in: Cloud Tasks, Pub/Sub, Secret Manager, Cloud Storage lifecycle.
Out of scope: raw GCP IAM/VPC/networking, multi-cloud (AWS/Azure), Docker/K8s. [EXPLICIT]

## 2. The immutable laws
- **Law of Queries / Read Reduction.** Firestore bills per document read/write/delete,
  not per query. Model schema for the read pattern; never read more docs than the UI
  renders; paginate always. [EXPLICIT]
- **Law of Denormalization.** Firestore rewards reading over writing. Duplicate fields
  a read needs rather than join; reconcile duplicates via a Firestore-trigger on the
  source. Trade-off: write amplification + consistency lag. [EXPLICIT]
- **Law of Rules.** Security Rules are mandatory, deny-by-default, and the *last* line
  not the only line. Design them before implementation; they cannot join or call out. [EXPLICIT]
- **Law of Triggers.** Cloud Functions react to events; design event chains, not request
  chains. Triggers are at-least-once and unordered → every handler must be idempotent. [EXPLICIT]
- **Law of Cost.** Every query is N document reads + index reads; `minInstances` bills
  idle 24/7. Estimate read/write volume per feature before committing the schema. [INFERENCIA]
- **Law of Storage Hygiene.** Unused Storage objects bill monthly until deleted;
  deletes are free, storage accrues silently. [EXPLICIT]

## 3. Security Rules mechanics (canonical)
- `request.auth` is null when unauthenticated — gate writes on `request.auth != null` first.
- `request.auth.token.<claim>` = custom claims for roles; set via Admin SDK; propagates
  only after token refresh (up to ~1h on live sessions). [EXPLICIT]
- `resource.data` = document **as stored** (pre-write); `request.resource.data` = the
  **incoming** state. Use both to validate diffs and enforce immutable fields. [EXPLICIT]
- `allow read` = `get` + `list`; `allow write` = `create` + `update` + `delete`. Split
  for field- or operation-level control. [EXPLICIT]
- Rules do NOT filter queries. A `list` rule must be satisfiable by the query's
  constraints or the whole query is rejected — never a partial set. [INFERENCE]
- Each `get()`/`exists()` in a rule is a billed read and counts against the
  10-call-per-request limit. [EXPLICIT]

## 4. Firestore query constraints
- Compound queries require a composite index in `firestore.indexes.json`; absence
  surfaces as `FAILED_PRECONDITION` at runtime, not at deploy. [INFERENCIA]
- No OR across fields, no multiple range filters in one query — split reads or
  denormalize a query field. [EXPLICIT]
- `in` operator batches up to 30 values; `count()`/`sum()`/`average()` aggregations
  bill ~1 read per 1000 matched docs — far cheaper than reading them. [EXPLICIT]

## 5. Cloud Functions (2nd gen)
- Idempotency via a processed-marker doc/field (at-least-once delivery). [EXPLICIT]
- Lazy-import heavy SDKs inside the handler; colocate region with Firestore;
  `concurrency: 80` serves many requests per instance for I/O-bound work. [CONFIG]
- `minInstances: 1` removes cold starts on latency-critical paths but bills idle. [INFERENCIA]
- Trigger write-loop hazard: a function writing the doc that triggered it recurses —
  short-circuit when source == self. [INFERENCIA]

## 6. Cost & billing controls
- Billing alerts at 50/80/100% notify but do NOT stop spend; the only hard stop is a
  budget Pub/Sub trigger that disables billing (non-prod only). [EXPLICIT]
- Spark (free) tier hard caps: 50k reads/day, 20k writes/day, 1 GiB stored. [EXPLICIT]
- Egress free within a region; cross-region reads incur charges. [EXPLICIT]
- **No prices** ever — emit FTE-months / usage estimates with disclaimers. [DOC]

## 7. Decision rules (routing + design)
| Question | Rule |
|----------|------|
| Which topic? | scheduled → `scheduled-functions`; handler code → `functions`; schema → `firestore-modeling`; index/read → `firestore-queries`; access → `firestore-security-rules` |
| Denormalize or not? | High read:write ratio → yes; else avoid write amplification |
| Counter contention? | >1 write/sec → shard counter across N subdocs |
| Cross-doc invariant? | Enforce in trusted server code, not Rules |
| Ship to prod? | Emulator pass + dry-run/preview first; never emulator-only |

## 8. Validation standard
Discover → Analyze → Execute → Validate. Rules tested in emulator (allow AND deny),
deploys dry-run first, cost claims backed by billing/usage data — never asserted.
Constitution v6.0.0; single-brand; no client PII.
