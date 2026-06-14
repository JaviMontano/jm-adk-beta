<!-- distilled from alfa skills/analytics-events -->
<!-- > -->
# Analytics Events

Design deterministic product and marketing event taxonomies: naming conventions, property contracts, identity rules, tracking plans, implementation handoffs, and validation gates. Output is a contract, not SDK code. [EXPLICIT]

## When To Use

- Event taxonomy, tracking plan, instrumentation spec, funnel/clickstream events, naming conventions, or Segment/RudderStack/Amplitude/Mixpanel/GA4 event design.
- Need event names, triggers, owners, property schemas, identity resolution, destinations, QA checks, or privacy review.
- Rationalizing duplicate/inconsistent events across web, mobile, backend, or server-side tracking.

## When Not To Use

- Dashboard visual design only → `data-visualization`.
- Warehouse/dbt modeling without event design → analytics-engineering cluster.
- Wiring the SDK/server emit code → `metrics-instrumentation` (this skill stops at the contract).
- Ad copy, campaign strategy, or attribution modeling without a tracking plan.
- Generic SQL debugging.

## Deterministic Contract

Treat `assets/` as the contract and `scripts/` as the offline oracle. No network, wall-clock time, random sampling, or undocumented product assumptions. Same input → same deliverable. [EXPLICIT]

Required assets (read before designing; if absent, mark `not verified` and request them rather than inventing rules): [EXPLICIT]
- `assets/analytics-events-contract.json` — required report sections and validation checks.
- `assets/naming-policy.json` — naming rules, allowed actions, reserved/forbidden tokens.
- `assets/property-policy.json` — property schema, types, PII classification, required fields.
- `assets/identity-policy.json` — user and anonymous identity requirements + merge behavior.
- `assets/tracking-plan-policy.json` — destination, owner, trigger, QA requirements.
- `assets/evidence-policy.json` — evidence tags and provenance fields.

Offline validation:
- `scripts/validate_analytics_events.py` — validates structured JSON handoffs against the policies.
- `bash scripts/check.sh` — deterministic fixture validation.
- BLOCK final delivery when any event lacks owner, trigger, properties, identity policy, evidence, privacy handling, or validation checks. A partial plan ships as an explicit gap report, never as silent omission. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify product surfaces, user journeys, destinations, implementation platforms, and current instrumentation.
- Extract evidence for source artifacts, product requirements, existing events, privacy constraints, QA constraints.
- Record unknowns explicitly as `not verified`. Never invent events, properties, volumes, or owners. [EXPLICIT]

### Step 2: Design Taxonomy
- Define domains: acquisition, activation, checkout, retention, billing, support, admin.
- Name events `object_action` in lower snake_case (e.g. `checkout_completed`, `subscription_canceled`). Verb is past-tense for completed facts. [EXPLICIT]
- Prefer events that represent user-observable or system-confirmed facts.
- Reject vague events — `click`, `submit`, `page`, `success`, `error` — without object context. Reject PascalCase, spaces, double-underscores, and reserved analytics keywords (`identify`, `track`, `group`, `page`, `screen`, `alias`). [EXPLICIT]

### Step 3: Define Event Contract

For each event specify, in one row: name · domain · action · trigger (the exact user/system condition that fires it, fired exactly once) · owner · platforms · destinations · required properties · identity requirements · privacy classification · evidence references. [EXPLICIT]

Worked example:

| field | value |
|---|---|
| name | `checkout_completed` |
| domain · action | checkout · completed |
| trigger | server confirms payment authorization; fired once per `order_id` |
| owner | Payments team |
| platforms · destinations | web, ios, server → Amplitude, warehouse |
| properties | `order_id` (string, req), `revenue` (number, req), `currency` (ISO-4217 string, req), `coupon_code` (string, opt) |
| identity | requires `user_id`; `anonymous_id` carried if pre-auth |
| privacy | no PII; `revenue` is business-sensitive, not personal |
| evidence | `[EXPLICIT]` from checkout PRD §3 |

### Step 4: Produce Tracking Plan
- Map each event to implementation owner, destination, QA method, rollout phase, validation rule.
- Specify server vs client placement and the rationale.
- Handle duplicates via alias + deprecation plan, not deletion.

### Step 5: Validate
- Verify naming, property, identity, tracking-plan, privacy, and evidence coverage.
- For JSON handoffs, run `scripts/validate_analytics_events.py` or mirror its checklist exactly.

## Key Decisions And Trade-offs

- **Server vs client emit.** Client captures intent and UI context but is lossy (ad-blockers, crashes, tampering); server is authoritative for money/state but blind to UI. Decide per event: revenue, entitlement, and state changes are server system-of-record; UI interactions are client. When both fire, define one as system of record and a `dedup_key` (e.g. `order_id`). [EXPLICIT]
- **Past-tense `object_action` vs present.** Past tense (`order_placed`) encodes a settled fact and reads unambiguously in funnels; present/imperative invites duplicate firing. Trade-off: more verbose names, accepted for determinism. [EXPLICIT]
- **Alias vs rename for duplicates.** Renaming breaks historical continuity in the warehouse; aliasing preserves trend lines at the cost of a deprecation window. Default to alias. [EXPLICIT]
- **Strict property typing vs flexibility.** Enforced types + enums catch drift at validation but require upfront spec; chosen because schema-on-read drift is the top cause of broken dashboards. [EXPLICIT]

## Acceptance Criteria (done = all true)

- [ ] Every event uses lower snake_case `object_action`; no reserved/forbidden tokens.
- [ ] Every event has domain, action, single-fire trigger, owner, platforms, properties, and evidence tag.
- [ ] Every required property has type, description, requirement status, and PII classification.
- [ ] Identity policy covers `user_id`, `anonymous_id`, and pre→post-auth merge behavior.
- [ ] Sensitive/PII properties carry a blocking privacy review and safe-identifier proposal.
- [ ] Tracking plan maps every event to destination, implementation owner, and QA method.
- [ ] Server/client duplicates have a declared system of record + `dedup_key`.
- [ ] Validation covers naming, properties, identity, tracking plan, privacy, evidence.
- [ ] If a JSON handoff is requested, it passes `scripts/validate_analytics_events.py`.

## Assumptions And Limits

- Assumes the user can supply product journeys, surfaces, existing tracking, or desired funnel outcomes. [EXPLICIT]
- Does not replace legal/privacy review for regulated personal data (GDPR/CCPA/HIPAA). [EXPLICIT]
- Does not write analytics SDK code unless explicitly requested — defines the contract and handoff only. [EXPLICIT]
- Does not validate live event volume or in-production firing; validation is static against fixtures/policies. [EXPLICIT]

## Failure Modes (anti-patterns to catch)

- Designing from a sibling tool's UI instead of the policy assets → unenforceable naming.
- Emitting `success`/`error`/`click` without an object → uncountable, unjoinable events.
- Same fact fired client and server with no dedup → double-counted revenue.
- Reusing one event name with divergent properties per platform → schema drift, broken charts.
- Putting raw email/phone/IP in properties → PII leak; must use hashed/opaque identifiers.
- Trigger that fires N times per intent (e.g. on every render) → inflated counts.
- Renaming a live event without an alias → severed historical trend.

## Edge Cases

| Scenario | Handling |
|---|---|
| Empty or minimal input | Produce a gap report and minimum evidence request; do not invent events. |
| Conflicting event names | Preserve legacy aliases; propose canonical name with deprecation window. |
| PII requested in properties | Mark privacy review blocking; propose hashed/opaque safe identifiers. |
| Multi-platform drift | Require platform coverage matrix and per-destination QA checks. |
| Server/client duplication | Choose system of record; define `dedup_key`. |
| Anonymous→authenticated user | Define merge/alias rule so pre-auth events stitch to `user_id`. |
| High-cardinality property (e.g. free text, full URL) | Bucket, truncate, or move to a separate property to protect destination limits/cost. |
| Retroactive taxonomy change | Version the event; map old→new in the tracking plan, never silently overwrite. |
