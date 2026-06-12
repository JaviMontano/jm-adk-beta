<!-- distilled from alfa skills/real-time-analytics -->
<!-- > -->
# Real Time Analytics
> "Method over hacks."
## TL;DR
Live dashboards, streaming transport (WebSocket/SSE/poll), alert-threshold config. Optimize for time-to-glass under a stated latency budget, not raw throughput. [EXPLICIT]

## Scope & Anti-Scope
- IN: sub-minute event-to-dashboard pipelines, push transports, threshold/anomaly alerting, live KPI tiles. [EXPLICIT]
- OUT: batch/warehouse reporting (use kpi-framework), experiment readouts (ab-testing), retroactive cohorting (cohort-analysis). Real-time is for *operational* decisions, not statistical ones. [EXPLICIT]

## Procedure
### Step 1: Discover
- Capture the **latency budget** (event→glass) and **freshness SLO**; these drive every later choice. [EXPLICIT]
- Identify event volume (events/s, peak:avg ratio) and consumer count (dashboards, alert rules). [EXPLICIT]
- Confirm the decision the live view enables — if no one acts in <5 min, real-time is likely over-engineering. [INFERENCIA]
### Step 2: Analyze
- Pick transport per Constitution XIII/XIV trade-offs (see Transport Decision). [EXPLICIT]
- Size aggregation window vs budget: window + propagation + render must fit the SLO. [EXPLICIT]
### Step 3: Execute
- Implement with evidence tags; instrument the pipeline's own lag as a first-class metric. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria; load-test at peak volume, not average. [EXPLICIT]

## Transport Decision
| Transport | Use when | Trade-off | Tag |
|-----------|----------|-----------|-----|
| Polling | <1 update/5s, simple infra, firewalled clients | Wasted requests, staleness = interval | [DOC] |
| SSE | Server→client only, HTTP/2, auto-reconnect wanted | One-way; ~6-conn limit on HTTP/1.1 | [DOC] |
| WebSocket | Bidirectional or high-frequency push | Stateful; needs LB sticky/affinity + heartbeat | [DOC] |
Default to SSE for dashboards (read-only); reserve WebSocket for interactivity. [INFERENCIA]

## Alert Thresholds
- Prefer **rate-of-change / anomaly bands** over static cutoffs; static thresholds page on every seasonal peak. [INFERENCIA]
- Require N consecutive breaches (debounce) before firing to suppress single-spike noise. [EXPLICIT]
- Set hysteresis: clear threshold < fire threshold, else alerts flap. [DOC]
- Route by severity; every alert names the owning metric and a runbook link. [EXPLICIT]

## Worked Example
Checkout-error live tile, budget = 30s, peak 2k events/s.
1. Transport: SSE (read-only dashboard). [DOC]
2. Window: 10s tumbling error-rate; 10s window + ~3s propagation + render < 30s budget. ✓ [EXPLICIT]
3. Alert: error-rate > 2x trailing-1h baseline for 3 consecutive windows → page; clear at 1.3x. [INFERENCIA]
4. Validate: replay a 2k-events/s burst; confirm tile lag p95 < 30s. [EXPLICIT]

## Quality Criteria
- [ ] Latency budget + freshness SLO stated and met at peak load [EXPLICIT]
- [ ] Transport choice justified against Transport Decision table [EXPLICIT]
- [ ] Alerts debounced + hysteresis set; no static-only thresholds without rationale [EXPLICIT]
- [ ] Pipeline lag self-instrumented [EXPLICIT]
- [ ] Evidence tags applied, Constitution-compliant, actionable output [EXPLICIT]

## Usage

Example invocations:

- "/real-time-analytics" — Run the full real time analytics workflow
- "real time analytics on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and a live event source. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Real-time ≠ exactly-once: at-least-once delivery means tiles must tolerate duplicate/out-of-order events. [SUPUESTO]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Late / out-of-order events | Define watermark + grace period; drop or side-output stragglers |
| Backpressure / consumer lag | Shed load (sample) or buffer with bounded queue; alert on lag, never block ingest |
| Transport drop / reconnect | Resume from last offset or re-snapshot; never silently show stale data as live |
| Threshold flapping | Apply hysteresis + debounce window |
