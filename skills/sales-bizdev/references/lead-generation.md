<!-- distilled from alfa skills/lead-generation -->
<!-- > -->
# Lead Generation

> "Method over hacks. Evidence over assumption."

## TL;DR

Design and ship lead-capture systems: lead magnets, gated content, signup-flow optimization, and qualification scoring — each tagged for evidence and rendered to MetodologIA brand standards. Scope is capture-to-qualified-handoff; nurture/closing belong downstream. [EXPLICIT]

## Procedure

### Step 1: Discover
- Gather ICP, offer, channel, and funnel stage from user input; name the conversion event being optimized [EXPLICIT]
- Read existing assets (landing copy, forms, analytics, CRM fields) before proposing anything [EXPLICIT]
- Identify current state, baseline conversion (if known), and the single biggest gap [INFERRED]

### Step 2: Analyze
- Evaluate options against Constitution principles (XIII Think First, XIV Simple First) [EXPLICIT]
- Pick the lever with best evidence and lowest build cost; prefer one strong magnet over many weak ones [INFERRED]
- Document trade-offs and the decision, including what was rejected and why [EXPLICIT]

### Step 3: Execute
- Implement following established patterns; instrument the conversion event so results are measurable [EXPLICIT]
- Apply evidence tags to every claim and projection [EXPLICIT]
- Use brand template for HTML outputs (references/brand/) [EXPLICIT]

### Step 4: Validate
- Verify against Quality Criteria and Acceptance Criteria below [EXPLICIT]
- Check evidence-tag coverage and Constitution compliance [EXPLICIT]
- Confirm the qualification handoff is unambiguous (who/what/when) [INFERRED]

## Qualification Scoring

Score = fit (ICP match) × intent (observed signal). Default model unless the user supplies one [INFERRED]:

| Band | Fit + Intent | Action |
|------|--------------|--------|
| Hot | Strong fit, explicit intent (demo/pricing) | Route to sales same-day |
| Warm | Fit but low intent, or intent but partial fit | Nurture sequence, re-score on next signal |
| Cold | Weak fit regardless of intent | Hold; do not route |
| Disqualified | Out of ICP, fake/bot, or competitor | Drop; suppress from sequences |

Never auto-promote on intent alone — high intent + poor fit wastes sales capacity [INFERRED]. State the scoring fields explicitly; if any are missing, flag rather than guess [EXPLICIT].

## Worked Example

Input: B2B SaaS, ICP = mid-market RevOps leads, baseline form converts 2%.
Decision: replace generic "Contact us" with a gated ROI calculator (high fit-signal, captures intent) [INFERRED].
Output: calculator + 3-field form (work email, company size, current tooling) feeding the scoring table; work-email + size ≥ 200 → Hot [INFERRED].
Trade-off: calculator costs more to build than an ebook but yields intent data the ebook cannot [INFERRED].

## Quality Criteria

- [ ] Follows Constitution principles
- [ ] Evidence tags on all claims
- [ ] Output is actionable and specific
- [ ] No redundancy or padding
- [ ] Conversion event is named and measurable
- [ ] Qualification handoff is unambiguous

## Acceptance Criteria

- Every recommendation maps to a named conversion event and a scoring band [EXPLICIT]
- No projected conversion lift stated without an `[INFERRED]` tag and a stated basis [EXPLICIT]
- Brand template applied to any HTML deliverable [EXPLICIT]
- No PII captured beyond what the named conversion event requires [EXPLICIT]

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Acting without understanding | Wastes effort on wrong solution | Think First (XIII) |
| Over-engineering | Complexity without value | Simple First (XIV) |
| Missing evidence tags | Claims without basis | Tag every assertion |
| Scoring on intent alone | Floods sales with bad-fit leads | Score fit × intent |
| Over-gating top-of-funnel | Kills volume for low-intent traffic | Gate only high-value, high-intent assets |
| Vanity-metric optimization | Sign-ups that never qualify | Optimize the qualified-lead event |

## Related Skills

- `client-prospecting` — sourcing target accounts that feed this funnel
- `b2b-outreach` — activating leads once qualified
- `proposal-writing` — converting Hot leads downstream

## Usage

Example invocations:

- "/lead-generation" — Run the full lead generation workflow
- "lead generation on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs, analytics) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Conversion-lift figures are projections, not guarantees — A/B test before claiming [INFERRED]
- Scope ends at qualified handoff; nurture and closing are out of scope [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No baseline metrics available | Proceed but label all projections `[INFERRED]`; recommend instrumentation first |
| Missing scoring fields | Flag the gap; do not fabricate fit/intent values |
| Regulated/PII-sensitive vertical | Minimize captured fields; defer to compliance before launch |
