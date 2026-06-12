<!-- distilled from alfa skills/google-analytics -->
<!-- > -->
# Google Analytics

## TL;DR

Use this skill to produce a deterministic offline GA4/GTM measurement plan
before any live analytics tagging. Start with
`scripts/compile-google-analytics.py` whenever the request can be expressed as
structured JSON. The compiler reads only local `assets/` and fixture/input
JSON; it never calls Google Analytics, Google Tag Manager, OAuth, MCP, or the
network. Live tagging is a separate, human-reviewed step gated by
`assets/tag-mutation-confirmation-policy.json`. [CODE]

**Scope.** Plan + validate a measurement design (events, key events, tags,
consent, debug expectations). **Anti-scope:** this skill does not create,
publish, or mutate any GA4 property, GTM container, or key event; does not
prove those resources exist; and is not legal/privacy sign-off. [CODE]

**Pick the right skill.** `google-analytics` = plan a measurement design
offline; `analytics-implementation` = execute GA4/Firebase/BigQuery setup;
`funnel-analytics` = interpret data after collection is safe. Routing on the
wrong key produces a plan with no executor (or an executor with no plan). [INFERENCE]

## Source Order

Read in order; each gate must pass before the next is meaningful. [INFERENCE]

1. `assets/source-map.md` — the official Google source set. [CODE]
2. `assets/ga4-gtm-plan-schema.json` — the structured input contract. [CODE]
3. `assets/event-taxonomy-policy.json` — event classes, naming, parameters,
   Measurement Protocol, key-event rules. [CODE]
4. `assets/privacy-consent-policy.json` — read before recommending any
   collection or tag mutation. [CODE]
5. `assets/tag-mutation-confirmation-policy.json` — read before recommending
   any live tag/container/key-event mutation. [CODE]
6. `assets/debug-checklist-policy.json` — GTM Preview, Tag Assistant, GA4
   DebugView, Realtime, publish checks. [CODE]

## Procedure

### Step 1: Discover Measurement State

- Confirm whether GA4 account, property, web data stream, measurement ID, and
  enhanced-measurement review are known. Unknown identity is a planning
  assumption to flag, not a blocker — plan proceeds, mutation does not. [DOC]
- Identify primary business goal, reporting questions, KPIs, implementation
  surface, and owner. Missing owner ⇒ no one can confirm a mutation later;
  flag it now, not at publish time. [CODE]
- Treat Measurement Protocol as supplemental to tagging, never a standalone
  replacement for a web stream. [DOC]

### Step 2: Design Event Taxonomy

- Classify each event as automatic, enhanced measurement, recommended, or
  custom — in that priority order. [DOC]
- Prefer official recommended events (`login`, `sign_up`, `generate_lead`,
  `purchase`, checkout events) when the business action matches. Rationale:
  recommended events unlock prebuilt GA4 reports and reduce schema drift;
  custom names forfeit that. [DOC]
- Use custom events only when no automatic/enhanced/recommended event fits, and
  record the gap that justifies the custom name. [DOC]
- Enforce lowercase `snake_case` for event and parameter names via the local
  schema. [CODE]
- Reject high-risk PII parameters before emitting a mutation-ready plan. [CODE]

### Step 3: Plan Key Events And Tags

- Map each key event to an event already in the taxonomy — never to an
  unplanned name. [CODE]
- For every key event document: business reason, value strategy, currency
  requirement, expected volume, owner. A key event without value strategy is
  unmeasurable ROI; without owner it cannot be confirmed for mutation. [CODE]
- Plan GTM/Google tag work as a checklist first: platform, tag type, tag name,
  trigger, consent checks, verification, mutation flag. [CODE]
- Require human confirmation before recommending any live
  tag/container/key-event mutation. [CODE]

### Step 4: Validate Privacy And Debugging

- Document region profile, CMP state, Consent Mode plan, default-denied
  behavior, ads-personalization review, data-redaction review, PII policy,
  legal-review owner. [CODE]
- Verify in GTM Preview and Tag Assistant before publish. [DOC]
- Verify event receipt and parameters in GA4 DebugView and Realtime. [DOC]
- Keep the compiler offline; live execution is a separate human-reviewed
  step. [CODE]

## Worked Example (plan fragment)

A SaaS lead-gen form submit, planned offline. [INFERENCE]

```json
{
  "event": "generate_lead",
  "class": "recommended",
  "parameters": { "currency": "USD", "value": 50, "form_id": "demo_request" },
  "key_event": {
    "business_reason": "qualified demo pipeline",
    "value_strategy": "static 50 placeholder until CRM win-rate known",
    "currency_required": true, "expected_volume": "~200/mo", "owner": "growth@"
  },
  "tag": {
    "platform": "gtm-web", "type": "ga4_event", "name": "GA4 - generate_lead",
    "trigger": "form_submit:#demo", "consent_checks": ["analytics_storage"],
    "verification": "DebugView shows generate_lead with value=50",
    "mutation": false
  }
}
```

Why `generate_lead` over a custom `demo_form_done`: it is an official
recommended event, so currency/value semantics and reports are built in;
`mutation:false` keeps it plan-only until a human confirms. [INFERENCE]

## Offline Compiler

```bash
python3 skills/google-analytics/scripts/compile-google-analytics.py \
  --input skills/google-analytics/scripts/fixtures/google-analytics-input.json
```

Run the deterministic fixture suite:

```bash
bash skills/google-analytics/scripts/check.sh
```

Determinism contract: same input JSON ⇒ byte-identical output; no clock,
random, or network reads. A diff between two runs of the same fixture is a
compiler bug, not a plan change. [CODE]

## Quality Criteria

- [ ] Output includes schema-stable GA4/GTM measurement strategy. [CODE]
- [ ] Each event names class, recommended-event fit (or documented gap),
      trigger, parameters, privacy review, and debug expectation. [CODE]
- [ ] Every key event is tied to a named event plus business value, owner,
      value strategy, and expected volume. [CODE]
- [ ] Privacy/consent checks are explicit before collection or mutation. [CODE]
- [ ] GTM/Google tag checklist covers platform, tag type, trigger, consent
      checks, verification, and publish/debug gates. [CODE]
- [ ] Human-confirmation gate blocks every mutating
      tag/container/key-event recommendation (`mutation:false` until met). [CODE]
- [ ] No direct PII appears in any event parameter. [CODE]
- [ ] Script checks stay offline and deterministic. [CODE]
- [ ] Every claim carries exactly one Alfa-set tag. [CODE]

## Anti-Patterns

- Treating Measurement Protocol as the only collection method for a web
  stream. [DOC]
- Creating a custom event when an official recommended event matches the
  action. [DOC]
- Duplicating automatic/enhanced events without a documented gap. [DOC]
- Sending email, phone, full name, raw address, or other direct PII as event
  parameters. [CODE]
- Recommending GTM publish or GA4 key-event changes without human
  confirmation. [CODE]
- Using UI copy, campaign names, or temporary labels as event names. [INFERENCE]
- Marking `mutation:true` in plan output to "save a step" — defeats the
  confirmation gate. [INFERENCE]

## Failure Modes

| Symptom | Likely cause | Resolution |
|---|---|---|
| Compiler output differs between runs | Non-deterministic input (timestamp/order) | Normalize input; re-run `check.sh`. [CODE] |
| Schema validation fails on event name | CamelCase/spaced/UI-copy name | Re-map to `snake_case` recommended event. [CODE] |
| Plan emitted with `mutation:true` | Confirmation gate skipped | Reject; force `false` until owner confirms. [CODE] |
| DebugView shows no events at publish | Consent default-denied blocks tag, or trigger never fires | Check Consent Mode + trigger in Preview. [DOC] |
| Key event with no value | Missing value strategy | Block plan until value/currency set. [CODE] |

## Related Skills

- `funnel-analytics` — interpret funnel performance after collection is
  safe. [INFERENCE]
- `landing-pages` — conversion-surface design that feeds GA4 events. [INFERENCE]
- `google-sheets-mcp` — deterministic reporting exports after data is read
  safely. [INFERENCE]
- `analytics-implementation` — execute the plan this skill produces. [INFERENCE]

## Assumptions & Limits

- The compiler validates a plan/checklist contract; it does not prove a GA4
  property, web stream, GTM container, OAuth grant, or browser tag exists. [CODE]
- Live implementation depends on account permissions, site-code access, GTM
  workspace state, consent tooling, and user confirmation. [INFERENCE]
- Not legal advice; privacy/legal sufficiency stays with the accountable human
  owner. [INFERENCE]
- Recommended-event list and consent semantics track Google's current docs;
  re-read `assets/source-map.md` if Google changes the catalog. [ASSUMPTION]

## Edge Cases

| Scenario | Handling |
|---|---|
| Measurement Protocol only | Reject; restate MP supplements tagging. |
| CamelCase or spaced event names | Reject via schema; use lowercase `snake_case`. |
| Mark every event as key event | Require business reason, owner, expected volume, value strategy per key event. |
| PII parameter supplied | Block plan until removed or replaced with non-PII surrogate. |
| Publish GTM changes | Return confirmation gate + debug checklist before any live mutation. |
| Region with consent default-denied | Plan Consent Mode + default-denied behavior before any tag fires. |
| Unknown property/stream identity | Proceed with plan; flag identity as `[ASSUMPTION]`; block mutation. |
