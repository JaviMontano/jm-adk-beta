# Body of Knowledge — product-analytics

Domain reference for the product-analytics router. Concepts, standards, and
decision rules shared across the eight topic playbooks. [DOC]

## 1. Core concepts

- **Event** — a user-observable or system-confirmed fact, named `object_action`
  in lower snake_case, past tense for completed facts (`checkout_completed`).
- **Property** — a typed attribute on an event with a PII classification and a
  cardinality bound. Free text and full URLs are high-cardinality risks.
- **Identity** — `user_id` (authenticated) and `anonymous_id` (pre-auth) with a
  merge/alias rule so pre-auth events stitch to the user after sign-in.
- **Metric** — a computed quantity with a unit, aggregation (count/sum/rate/
  unique/p50/p95), and scope (event/user/session/item).
- **KPI** — a metric that is owned, defined, instrumented, comparable over time,
  and tied to a decision. Failing any of these makes it a vanity metric.
- **North Star / metric tree** — one root outcome metric, decomposed into input
  metrics and levers a team can actually move.
- **Funnel** — an ordered set of steps over one unit with a conversion window.
- **Cohort** — users grouped by a shared acquisition event, tracked over time
  aligned to that event.
- **Experiment (A/B)** — a randomized comparison with a pre-declared hypothesis,
  primary metric, guardrails, and decision rule.

## 2. Standards & conventions

- **Naming:** `object_action`, lower snake_case; reject `click`/`submit`/`page`/
  `success`/`error` without an object, PascalCase, spaces, and reserved tokens
  (`identify`, `track`, `group`, `page`, `screen`, `alias`).
- **Evidence tags (Alfa-core):** `[DOC] [CONFIG] [CÓDIGO] [INFERENCIA]
  [SUPUESTO]`; every `[SUPUESTO]` is paired with a verification step.
- **Currency:** ISO-4217 codes; store revenue in minor units where instrumented.
- **Statistics:** two-proportion z-test for binary conversion; t-test /
  Mann-Whitney for continuous; CUPED for variance reduction; sequential tests
  for valid early stopping.

## 3. Decision rules

- **Leading vs lagging:** pair every lagging KPI (retention, revenue) with ≥1
  leading driver (activation, time-to-first-value) that moves within a sprint.
- **Denominator policy (funnels):** state step-to-step OR overall once and apply
  uniformly; mixing them yields contradictory totals.
- **Sample size scales ≈ 1/MDE²:** halving the detectable effect ~quadruples N.
  If traffic can't reach N within the runtime, declare it underpowered.
- **SRM:** if the observed split deviates from intended (chi-square p < 0.01),
  results are untrustworthy regardless of the primary p-value.
- **Cohort denominators:** fix at cohort size at t0, never current size; exclude
  empty late-period cells of immature cohorts.
- **Client vs server capture:** revenue/entitlement/state → server (system of
  record); UI interactions → client; when both fire, declare one canonical +
  a `dedup_key`.
- **Transport (real-time):** poll for <1 update/5s; SSE for read-only dashboards;
  WebSocket only for interactivity. Window + propagation + render must fit the SLO.
- **Chart choice:** the goal (comparison/composition/distribution/trend/
  relationship), not the data shape, picks the chart; library by data size.

## 4. Validity threats to catch

- Peeking and stopping early; extending a flat test to "find" a win.
- Sample ratio mismatch (SRM); overlapping experiments on one surface.
- Simpson's paradox — a blended rate moving opposite every segment on mix shift.
- Survivorship in late cohort periods; identity resets mid-funnel.
- Schema drift from one event name with divergent properties per platform.
- Hue-only encoding invisible to colorblind users; truncated y-axis baselines.

## 5. Hard prohibitions

- Never claim significance, lift, ROI, or causality without the data + method.
- Never invent baselines, traffic, conversion rates, or benchmark numbers.
- Never emit direct PII (raw email/phone/IP) in events or deliverables.
- Never load more than one playbook per run. [CONFIG]
