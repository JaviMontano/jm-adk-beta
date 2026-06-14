<!-- distilled from alfa skills/conversion-optimization -->
<!-- > -->
# Conversion Optimization

> "Method over hacks. Evidence over assumption."

## TL;DR

Deterministic CRO for friction-point analysis, trust-signal placement, funnel-step optimization, and A/B test design. Outputs follow MetodologIA brand standards and evidence tagging. [EXPLICIT]
Use when a page or funnel underconverts and you need a prioritized, testable intervention plan — not after-the-fact rationalization of a redesign already shipped. [EXPLICIT]
Anti-scope: paid-media bidding, SEO ranking (see `seo-architecture`), and post-launch funnel diagnosis on live traffic (see `funnel-analytics`). [EXPLICIT]

## Procedure

### Step 1: Discover
- Capture the single conversion event, its current rate, monthly volume at the leaking step, and the device/traffic mix. [EXPLICIT]
- Read existing page code, copy, analytics events, and prior test history; never re-test a settled question. [EXPLICIT]
- Map the funnel step-by-step with the drop-off rate at each transition; the worst transition is the only valid starting point. [EXPLICIT]
- If no baseline rate exists, mark it as a gap and instrument before testing — do not invent a number. [EXPLICIT]

### Step 2: Analyze friction & trust
- Classify every friction point as cognitive (unclear value/next step), effort (form length, steps, load time), or trust (risk, credibility, ambiguity). [EXPLICIT]
- Score each candidate by ICE: Impact x Confidence x Ease, 1–5 each; rank descending and act on the top item only. [EXPLICIT]
- Match each trust gap to a signal: testimonials/logos (social proof), guarantees/returns (risk reversal), security badges/HTTPS (safety), specificity/numbers (credibility). [EXPLICIT]
- Evaluate against Constitution principles (XIII Think First, XIV Simple First) and record trade-offs. [EXPLICIT]

### Step 3: Design the test
- State one hypothesis: "Because [evidence], changing [element] will [direction] [metric] for [segment]." [EXPLICIT]
- Pre-register the primary metric, minimum detectable effect (MDE), required sample size per arm, and stop date — before launch. [EXPLICIT]
- Change ONE variable per A/B arm; bundle changes only in an explicitly labeled redesign test where you accept losing attribution. [EXPLICIT]
- Apply evidence tags to every claim; use the brand template for HTML deliverables (references/brand/). [EXPLICIT]

### Step 4: Validate
- Verify the test reached pre-registered sample size and ran ≥1 full business cycle (typically 2 weeks) before reading results. [EXPLICIT]
- Confirm significance at the pre-set threshold; a flat or negative result is a kept learning, not a failure to hide. [EXPLICIT]
- Check evidence-tag coverage and Constitution compliance; ship the winner, document, then return to Step 2 for the next-ranked item. [EXPLICIT]

## Worked Example

Checkout step converts 38%; cart→checkout is the worst transition (62% drop). [EXPLICIT]
Friction: 11-field form (effort) + no return policy near the CTA (trust). [INFERRED]
ICE ranks "surface free-returns guarantee at CTA" (4x4x5=80) above "cut form to 6 fields" (4x3x3=36). [EXPLICIT]
Hypothesis: because exit surveys cite return risk, adding a returns guarantee at the pay button will raise checkout completion for mobile buyers. [EXPLICIT]
MDE +3pp, ~4,200/arm, 2-week run, single variable. Ship if significant; else keep the learning and test form length next. [EXPLICIT]

## Quality Criteria

- [ ] Follows Constitution principles (Think First, Simple First).
- [ ] Targets the measured worst funnel transition, not a guess.
- [ ] Every friction point classified (cognitive / effort / trust) and ICE-ranked.
- [ ] Exactly one hypothesis with one variable, pre-registered metric, MDE, and sample size.
- [ ] Result interpreted only at pre-set sample and duration; learning recorded regardless of outcome.
- [ ] Evidence tags on all claims; gaps marked, never invented.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Acting without understanding | Wastes effort on wrong solution | Think First (XIII); start from measured drop-off |
| Over-engineering | Complexity without value | Simple First (XIV); one variable per arm |
| Peeking / early stop | Inflates false positives | Pre-register sample size and stop date |
| Multi-change A/B | Cannot attribute the lift | Isolate one variable, or label it a redesign test |
| Copying competitor "best practices" | Their context isn't yours | Test the change on your own traffic |
| Missing evidence tags | Claims without basis | Tag every assertion |

## Related Skills

- `funnel-design` for the pre-launch funnel blueprint; `funnel-analytics` for live drop-off diagnosis.
- `social-proof` and `landing-page-builder` for trust-signal and page execution.

## Usage

Example invocations:

- "/conversion-optimization" — Run the full conversion optimization workflow
- "conversion optimization on this checkout" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and analytics with a measurable conversion event. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Statistical guidance assumes a standard frequentist A/B test; sequential/Bayesian methods need their own stop rules. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Never reports a lift as confirmed below the pre-registered sample size. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No analytics baseline | Instrument and capture a baseline before any test; mark as gap |
| Low traffic (< MDE sample feasible) | Recommend qualitative research or sequential testing, not an underpowered A/B |
| Inconclusive / flat result | Record as a learning, keep control, advance to next ICE-ranked item |
