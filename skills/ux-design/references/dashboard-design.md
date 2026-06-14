<!-- distilled from alfa skills/dashboard-design -->
<!-- > -->
# Dashboard Design
> "Method over hacks."
## TL;DR
Layout patterns, data hierarchy, drill-down, and real-time for dashboards: pick a type, lead with the decision, layer detail F-pattern top-left, and only add live data when staleness changes a decision. [EXPLICIT]

## Procedure
### Step 1: Discover
- Name the ONE decision the viewer makes and the action it triggers; a dashboard with no decision is a report. [EXPLICIT]
- Capture viewer role, refresh expectation (live / hourly / daily), and device (wall display vs laptop vs mobile). [EXPLICIT]
- Classify the type: **strategic** (KPIs, low frequency), **operational** (real-time, alerting), **analytical** (exploration, drill-down). Mixing types in one view is the top failure mode. [INFERENCIA]
### Step 2: Analyze
- Build the data hierarchy: ≤5 headline metrics → supporting trends → granular tables. Eyes scan top-left first (F-pattern), so place the highest-stakes metric there. [INFERENCIA]
- Design drill-down as a path, not a wall: summary → segment → row. Each click answers "why is this number what it is?" Keep ≤3 levels. [EXPLICIT]
- Choose encodings per question: trend→line, comparison→bar, part-to-whole→stacked/100%-bar (not pie >5 slices), distribution→histogram, correlation→scatter. [INFERENCIA]
- Evaluate options per Constitution XIII/XIV. [EXPLICIT]
### Step 3: Execute
- Implement with evidence tags. Show absolute value + delta + direction together (e.g. `1,240  ▲12% vs prior`); a number with no comparator is undecidable. [EXPLICIT]
- Real-time only where staleness flips a decision; otherwise poll on a cadence and stamp "updated Xs ago". Push (WebSocket/SSE) for alerting, poll for monitoring. [INFERENCIA]
- States are first-class: design loading (skeleton), empty (what to do next), error (retry + last-good), and stale explicitly — never a blank panel. [EXPLICIT]
- Accessibility: don't encode meaning by color alone (add icon/label); target WCAG AA contrast; make tables keyboard-navigable. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met. Run the 5-second test: can a new viewer name the headline and the action it implies? [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Drives exactly one named decision; headline metric is top-left
- [ ] Every metric carries a comparator (target / prior / benchmark)
- [ ] Loading, empty, error, and stale states designed
- [ ] Color is not the sole carrier of meaning (WCAG AA)
- [ ] Refresh cadence matches decision tempo, not "as fast as possible"

## Usage

Example invocations:

- "/dashboard-design" — Run the full dashboard design workflow
- "dashboard design on this project" — Apply to current context

## Worked Example
Ops on-call dashboard, decision = "page someone or not?" Type: operational. Headline top-left: error-rate % with target line. Supporting: latency p95 trend + request volume. Drill: spike → service → endpoint. Live via SSE (alerting); rows poll at 30s with "updated 12s ago". Red/green also carry ▲/▼ icons for color-blind viewers. [INFERENCIA]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not BI tool selection, pipeline/ETL design, or visual brand theming — only layout, hierarchy, drill-down, and refresh behavior. [EXPLICIT]
- Real-time guidance assumes a backend that can push/poll; offline/batch-only sources cap at "last refreshed" stamps. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| >7 headline metrics demanded | Split into tabs/views by decision; one view = one decision [INFERENCIA] |
| High-cardinality category (100s of items) | Top-N + "other" rollup with search/filter, never render all [INFERENCIA] |
| Real-time asked but data updates daily | Drop live polling; show "updated Xh ago" to set honest expectations [EXPLICIT] |
| Mobile + dense table | Collapse to headline cards; defer table to drill-down [INFERENCIA] |
