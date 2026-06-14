<!-- distilled from alfa skills/reporting-templates -->
<!-- > -->
# Reporting Templates
> "Method over hacks."
## TL;DR
Design executive reports, operational dashboards, and compliance reports: pick the template for the audience, fill it from evidenced artifacts, validate before ship. [EXPLICIT]

## When to use which template
| Template | Audience | Cadence | Core question answered |
|----------|----------|---------|------------------------|
| Executive report | Leadership / sponsors | Periodic, milestone | "Are we on track, what changed, what's the ask?" [EXPLICIT] |
| Operational dashboard | Delivery / ops teams | Live / daily | "What is the current state of the system or work?" [EXPLICIT] |
| Compliance report | Auditors / regulators | On-demand, fixed | "Do we meet control X, with what evidence?" [EXPLICIT] |

## Procedure
### Step 1: Discover
- Gather context and requirements; confirm audience, the decision the report drives, and cadence [EXPLICIT]
- Identify source-of-truth artifacts (code, configs, metrics) feeding each figure [EXPLICIT]
### Step 2: Analyze
- Evaluate template options per Constitution XIII/XIV; pick one from the table above [EXPLICIT]
- Map each claim to its evidence tag; flag any figure without a verifiable source [INFERRED]
### Step 3: Execute
- Implement with evidence tags; lead with the decision/ask, supporting detail after [EXPLICIT]
- State the as-of timestamp and data window on every metric [SUGGESTED]
### Step 4: Validate
- Verify quality criteria met; reconcile totals against source before ship [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied to every non-trivial claim and figure
- [ ] Constitution-compliant; single-brand, no invented prices
- [ ] Actionable output: decision or ask is explicit and up top
- [ ] As-of date and data source stated for each metric
- [ ] Status is neutral and honest — green is never a default

## Anti-scope (this skill does NOT)
- Generate the underlying data or run the analytics pipeline [EXPLICIT]
- Render to PDF/PPTX/XLSX — hand off to the brand-output skills [EXPLICIT]
- Decide red/amber/green thresholds — those come from the project [INFERRED]

## Acceptance criteria
- A reader who only sees the report can name the decision and its evidence [EXPLICIT]
- Every number traces to a named artifact; zero unsourced figures [EXPLICIT]
- Re-running with the same inputs yields the same report [SUGGESTED]

## Failure modes
| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Vanity green | All-green status hiding a slip | Require a "what changed / at risk" line every period [SUGGESTED] |
| Orphan metric | Figure with no traceable source | Block ship; tag or remove the figure [EXPLICIT] |
| Audience mismatch | Execs get ops detail, or vice versa | Re-pick template from the table; resize altitude [EXPLICIT] |
| Stale data | Numbers without an as-of date | Stamp data window on every metric [EXPLICIT] |

## Usage

Example invocations:

- "/reporting-templates" — Run the full reporting templates workflow
- "reporting templates on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate [EXPLICIT] |
| No baseline to compare against | Report absolute values; mark trend N/A, not zero [SUGGESTED] |
