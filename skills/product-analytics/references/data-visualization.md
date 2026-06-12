<!-- distilled from alfa skills/data-visualization -->
<!-- > -->
# Data Visualization

> "The greatest value of a picture is when it forces us to notice what we never expected to see." — John Tukey

## TL;DR

Implements interactive data visualizations using Chart.js for standard charts, D3.js for custom visualizations, and SVG/Canvas for specialized graphics powering dashboards and data-driven components. Use this skill when building dashboards, presenting analytics data, or when users need to explore data visually. [EXPLICIT]

## Scope & Anti-Scope

- **In scope**: chart selection, rendering library choice, interactivity, accessibility, real-time updates, data-to-chart transformation. [EXPLICIT]
- **Out of scope**: data pipeline/ETL ownership (→ `data-engineering`), metric/event definition, statistical modeling, BI tool config (Looker/Tableau/PowerBI), print/PDF export. Redirect or escalate. [SUPUESTO]

## Procedure

### Step 1: Discover
- Identify the data: structure, volume (rows × series), update frequency, source latency. [EXPLICIT]
- Determine the goal — one of: comparison, composition, distribution, trend, relationship. The goal, not the data shape, picks the chart. [INFERENCIA]
- Review existing chart-library usage to avoid introducing a second library for one chart. [INFERENCIA]
- Gather requirements: interactivity (tooltips, zoom, drill-down), responsive breakpoints, accessibility target (WCAG AA). [EXPLICIT]

### Step 2: Analyze
- Choose chart type for the data story:
  - **Bar/Column**: comparison across categories (sort by value unless category order is meaningful).
  - **Line/Area**: trends over time (stacked area only when parts sum to a meaningful whole).
  - **Pie/Donut**: composition, 5–7 segments max; above that, use a sorted bar chart. [INFERENCIA]
  - **Scatter**: correlation between two continuous variables.
  - **Heatmap**: density and patterns in two dimensions.
- Select the rendering library by dataset size and customization, not preference:
  - **Chart.js**: standard charts, minimal config, ≲10k points.
  - **D3.js**: custom/bespoke interactions and layouts; highest control, highest cost.
  - **SVG**: crisp, scalable, accessible (DOM-inspectable) — degrades past ~1–2k nodes. [INFERENCIA]
  - **Canvas**: high-performance for large datasets (≳10k points); trades DOM accessibility for speed. [INFERENCIA]

### Step 3: Execute
- Implement charts with responsive container sizing (ResizeObserver, not fixed px). [EXPLICIT]
- Add interactivity: tooltips, hover states, click handlers, legends — each keyboard-reachable. [EXPLICIT]
- Update real-time data in place (mutate datasets + redraw), not full re-render, to preserve animation state and FPS. [INFERENCIA]
- Design colorblind-safe palettes (~8% of males have CVD; never encode meaning by hue alone — pair with shape/label/position). [EXPLICIT]
- Add ARIA labels/roles and a text or table fallback for the chart's data. [EXPLICIT]
- Implement loading, empty, and error states for every data-driven chart. [EXPLICIT]
- Set up the transformation pipeline: raw data → validated → chart-ready format. [EXPLICIT]

### Step 4: Validate
- Verify responsiveness and readability across viewport sizes (mobile → desktop). [EXPLICIT]
- Confirm palette passes colorblind simulation (Sim Daltonism, Coblis) for all three CVD types. [EXPLICIT]
- Confirm interactive elements are keyboard-reachable AND operable (focus, activate, dismiss). [EXPLICIT]
- Test with production-scale data volumes to confirm acceptable render/interaction latency. [EXPLICIT]

## Worked Example

Goal: show 12-month signups by plan tier for a dashboard card, ~10k rows, updates hourly.
1. Goal = trend over time, split by category → **multi-series line** (not stacked area: tiers don't sum to a meaningful total). [INFERENCIA]
2. ~10k points after monthly aggregation is small → **Chart.js**. [INFERENCIA]
3. 3 tiers → Okabe–Ito subset (blue/orange/green) + distinct dash patterns so lines read without color. [INFERENCIA]
4. Aggregate raw rows → 12 monthly buckets per tier before render; hourly refresh mutates the dataset in place. [INFERENCIA]
5. Validate: Coblis check, keyboard-toggle legend, ARIA `role="img"` + `<table>` fallback. [EXPLICIT]

## Decisions & Trade-offs

| Decision | Choose when | Trade-off accepted |
|----------|-------------|--------------------|
| SVG over Canvas | accessibility + interactivity matter, ≲2k nodes | slower past a few thousand nodes [INFERENCIA] |
| Canvas over SVG | ≳10k points, pan/zoom | loses DOM a11y → must add text fallback [INFERENCIA] |
| Chart.js over D3 | standard chart, speed to ship | limited bespoke layouts [INFERENCIA] |
| D3 over Chart.js | custom interaction/layout required | higher build + maintenance cost [INFERENCIA] |

## Failure Modes

- **Pie with >7 slices** → unreadable; switch to sorted bar. [INFERENCIA]
- **Full re-render on each tick** → flicker, dropped frames; mutate + redraw instead. [INFERENCIA]
- **Hue-only encoding** → invisible to CVD users; add shape/pattern/label. [EXPLICIT]
- **Fixed-px chart in flex/grid** → overflow/clipping on resize; use ResizeObserver. [INFERENCIA]
- **Unaggregated 100k+ points to SVG** → DOM stall; aggregate or move to Canvas. [INFERENCIA]
- **Dual y-axes with mismatched scales** → implies false correlation; avoid or annotate. [INFERENCIA]

## Quality Criteria

- [ ] Chart type matches the data relationship being communicated. [EXPLICIT]
- [ ] Palette is colorblind-safe, high-contrast, and not hue-dependent. [EXPLICIT]
- [ ] Charts are responsive and readable on mobile. [EXPLICIT]
- [ ] Interactive elements have keyboard access and ARIA labels. [EXPLICIT]
- [ ] A non-visual data fallback (table/text) exists. [EXPLICIT]
- [ ] Loading, empty, and error states are implemented. [EXPLICIT]
- [ ] Evidence tags applied to all non-obvious claims. [EXPLICIT]

## Anti-Patterns

- 3D charts that distort perception (never use 3D pie charts). [EXPLICIT]
- Rainbow / non-colorblind-safe palettes. [EXPLICIT]
- Charts without axis labels, legends, or units. [EXPLICIT]
- Truncated y-axis baselines that exaggerate differences. [INFERENCIA]

## Related Skills

- `responsive-design` — responsive chart container strategies
- `accessibility-design` — accessible chart patterns and alternatives
- `performance-architecture` — canvas rendering for large datasets

## Usage

Example invocations:

- "/data-visualization" — Run the full data visualization workflow
- "data visualization on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Assumes a web/JS runtime; native/mobile-only charting is out of scope. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Dataset exceeds renderer limit | Aggregate/sample, or switch SVG→Canvas |
| All-null / single-point series | Show empty state, not a misleading axis |
| Real-time stream faster than frame budget | Throttle/debounce updates to redraw cadence |
