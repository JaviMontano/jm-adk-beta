<!-- distilled from alfa skills/analytics-implementation -->
<!-- GA4 setup. Firebase Analytics custom events. Conversions. User properties. BigQuery export. Looker Studio dashboards. [EXPLICIT] -->
# Analytics Implementation

Analytics Implementation turns a measurement plan into a verifiable GA4/Firebase implementation package: custom events, conversions, user properties, consent/privacy controls, BigQuery export, and Looker Studio readiness. Output is a spec + QA handoff, not SDK code. [EXPLICIT]

## When To Use

- GA4 setup, Firebase Analytics setup, data streams, custom events, event parameters, conversions, audiences, user properties, BigQuery export, or Looker Studio dashboards.
- Implementation handoff for web, iOS, Android, backend, or Firebase projects.
- Analytics QA plans, DebugView validation, BigQuery export validation, consent mode, or privacy-safe analytics rollout.

## When Not To Use

- Firestore schema design, security rules, indexes, or backups without analytics instrumentation.
- Generic dashboard visual design without analytics implementation.
- Event taxonomy only, unless implementation details are requested.
- Warehouse transformation modeling after data is already exported.
- Server-side GTM container build-out, or ad-platform conversion linking (Google Ads/Floodlight) — out of scope; hand off separately. [INFERENCE]

## Deterministic Contract

Use `assets/` as the offline contract and `scripts/` as the deterministic oracle. The skill must not depend on network access, wall-clock time, random sampling, or unverifiable platform state. [EXPLICIT]

Required assets:
- `assets/analytics-implementation-contract.json` — required sections and validation checks.
- `assets/ga4-policy.json` — GA4/Firebase setup fields.
- `assets/event-policy.json` — custom event and parameter rules.
- `assets/conversion-policy.json` — conversion requirements.
- `assets/bigquery-policy.json` — export and retention requirements.
- `assets/dashboard-policy.json` — Looker Studio source and metric requirements.
- `assets/evidence-policy.json` — evidence tags and provenance fields.

Offline validation:
- `scripts/validate_analytics_implementation.py` — validates structured JSON implementation plans.
- `bash scripts/check.sh` — validates deterministic fixtures.
- Block final delivery when GA4 setup, event contracts, conversions, user properties, export, dashboards, privacy, or QA evidence is missing.

**Validation precedence:** policy JSON in `assets/` is the source of truth; if this doc and a policy disagree, the policy wins and this doc is the defect to fix. [INFERENCE]

## Procedure

### Step 1: Discover

- Identify platforms, GA4 properties, Firebase apps, data streams, destinations, consent constraints, and existing implementation gaps.
- Collect evidence for measurement requirements, current analytics stack, privacy constraints, and dashboard needs.
- Missing a required input (e.g. GA4 property id, target region for consent) → mark the field as a gap and stop before specifying; do not invent ids. [INFERENCE]

### Step 2: Specify Implementation

- Define GA4/Firebase setup, streams, SDK surfaces, consent mode, debug flow, and owners.
- Define custom events with parameters, platform, trigger, owner, and validation method.
- Define conversions and user properties with privacy review.
- Define BigQuery export settings, dataset ownership, retention, partitioning, and PII handling.
- Define Looker Studio dashboards and data source expectations.

### Step 3: QA And Rollout

- Validate events in DebugView or equivalent local/debug flow.
- Validate destination receipt and BigQuery rows.
- Validate conversion marking and dashboard freshness.
- Document rollback or deprecation steps for incorrect events.

## Design Decisions And Trade-offs

- **Spec, not code.** Defining a contract + QA gate (vs. emitting SDK calls) keeps the output platform-agnostic and testable offline, at the cost of one extra integration step by the implementer. [EXPLICIT]
- **Policy-driven validation** over freeform review: deterministic and reproducible, but only as complete as the policy JSON — extend the policy, not the prose, to add a rule. [INFERENCE]
- **BigQuery export default = daily;** choose streaming export only when sub-hour latency is a stated requirement, since streaming changes cost and table shape. Record which was chosen and why. [INFERENCE]

## Edge Cases And Failure Modes

- **Reserved/auto-collected names:** reject custom events or parameters that collide with GA4 reserved prefixes (`ga_`, `google_`, `firebase_`) or auto-collected events (e.g. `session_start`, `first_open`); these silently fail or are dropped. [INFERENCE]
- **Limits:** flag plans exceeding GA4 limits — event-scoped custom dimensions, registered params per event, distinct event names — as a gap, not a pass. Exact ceilings are platform-versioned; cite the policy or platform docs, never hard-code from memory. [ASSUMPTION] (verify against `assets/event-policy.json` / current GA4 limits)
- **Consent gating:** an event marked PII-bearing with no consent-mode mapping is a blocking defect, not a warning.
- **Conversion without source event:** a conversion that references an event absent from the event contract must fail validation (dangling reference).
- **DebugView blind spot:** DebugView confirms client send, not destination receipt — require the BigQuery-row check too before marking an event verified. [INFERENCE]
- **Dashboard staleness:** a dashboard whose data source predates the latest export run is stale; freshness check must compare against export recency, not just existence.

## Worked Example (minimal structured plan)

```json
{
  "ga4_setup": {"property_id": "<id>", "streams": ["web"], "consent_mode": "advanced", "owner": "data-eng", "debug": "DebugView"},
  "events": [{
    "name": "checkout_completed", "platform": "web", "trigger": "purchase success",
    "owner": "growth", "destination": "ga4+bigquery", "validation": "DebugView+bq_row",
    "parameters": [{"name": "value", "type": "number", "pii": "none"},
                   {"name": "order_id", "type": "string", "pii": "pseudonymous"}]
  }],
  "conversions": [{"event": "checkout_completed", "owner": "growth"}],
  "user_properties": [{"name": "plan_tier", "type": "string", "description": "subscription tier", "pii": "none"}],
  "bigquery_export": {"dataset": "analytics_<id>", "location": "US", "retention_days": 60,
                      "partitioning": "event_date", "pii_handling": "pseudonymous-only"},
  "dashboards": [{"name": "Funnel", "source": "bigquery", "metrics": ["conversion_rate"]}]
}
```

This plan passes only if every conversion resolves to a defined event, every parameter carries a PII class, and export + dashboards reference declared sources. Run `scripts/validate_analytics_implementation.py` against it. [EXPLICIT]

## Quality Criteria

- [ ] GA4 or Firebase setup includes property/app, streams, owner, consent, and debug validation.
- [ ] Every custom event has trigger, owner, platform, parameters, destination, and evidence; name avoids reserved prefixes.
- [ ] Every event parameter has type and privacy classification.
- [ ] Every conversion references a known event and has an owner.
- [ ] Every user property has type, description, and PII classification.
- [ ] BigQuery export includes dataset, location, retention, partitioning, and PII handling.
- [ ] Looker Studio dashboards map to known data sources and metrics.
- [ ] Validation covers GA4 setup, event contract, conversions, user properties, BigQuery export, dashboards, privacy, and evidence.
- [ ] PII-bearing events/properties have a consent-mode mapping.
- [ ] Structured JSON passes `scripts/validate_analytics_implementation.py` and `bash scripts/check.sh`.

## Assumptions And Limits

- Assumes the user can provide project, platform, destination, or measurement context. [EXPLICIT]
- Does not replace legal review for consent mode or regulated data handling. [EXPLICIT]
- Does not implement SDK code unless explicitly requested; it defines an implementation and QA handoff. [EXPLICIT]
- Platform-versioned limits and reserved-name lists drift; treat in-doc figures as [ASSUMPTION] and reconcile against current policy/platform docs at delivery. [INFERENCE]
