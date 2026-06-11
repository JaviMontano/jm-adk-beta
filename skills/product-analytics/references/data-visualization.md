<!-- distilled from alfa skills/data-visualization -->
<!-- > -->
# Data Visualization

> "The greatest value of a picture is when it forces us to notice what we never expected to see." — John Tukey

## TL;DR

Implements interactive data visualizations using Chart.js for standard charts, D3.js for custom visualizations, and SVG/Canvas for specialized graphics powering dashboards and data-driven components. Use this skill when building dashboards, presenting analytics data, or when users need to explore data visually. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the data to visualize: structure, volume, update frequency
- Determine visualization goals: comparison, composition, distribution, trend, relationship
- Review existing chart library usage in the codebase
- Gather requirements: interactivity (tooltips, zoom, drill-down), responsive, accessible

### Step 2: Analyze
- Choose the right chart type for the data story:
  - **Bar/Column**: comparison across categories
  - **Line/Area**: trends over time
  - **Pie/Donut**: composition (limit to 5-7 segments)
  - **Scatter**: correlation between variables
  - **Heatmap**: density and patterns in two dimensions
- Select the right library:
  - **Chart.js**: standard charts with minimal configuration
  - **D3.js**: custom, interactive, data-driven visualizations
  - **SVG**: crisp, scalable, accessible graphics
  - **Canvas**: high-performance rendering for large datasets

### Step 3: Execute
- Implement charts with responsive container sizing
- Add interactivity: tooltips, hover states, click handlers, legends
- Implement real-time data updates without full re-render
- Design color palettes that are colorblind-safe (8% of males have CVD)
- Add proper ARIA labels and roles for screen reader accessibility
- Implement loading states and empty states for data-driven charts
- Set up data transformation pipelines: raw data → chart-ready format

### Step 4: Validate
- Verify charts are responsive and readable at all viewport sizes
- Confirm color palette passes colorblind simulation (Sim Daltonism, Coblis)
- Check that interactive elements are keyboard accessible
- Test with real data volumes to ensure performance is acceptable

## Quality Criteria

- [ ] Chart type matches the data relationship being communicated
- [ ] Color palette is colorblind-safe and high contrast
- [ ] Charts are responsive and readable on mobile
- [ ] Interactive elements have keyboard access and ARIA labels
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- 3D charts that distort data perception (never use 3D pie charts)
- Rainbow color palettes that are not colorblind-safe
- Charts without axis labels, legends, or units

## Related Skills

- `responsive-design` — responsive chart container strategies
- `accessibility-design` — accessible chart patterns and alternatives
- `performance-architecture` — canvas rendering for large datasets

## Usage

Example invocations:

- "/data-visualization" — Run the full data visualization workflow
- "data visualization on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
