<!-- distilled from alfa skills/social-proof -->
<!-- > -->
# Social Proof

> "Method over hacks. Evidence over assumption."

## TL;DR

Design and place trust signals — testimonials, case studies, ratings, logos, counts, certifications — so they reduce buyer risk at the exact moment of hesitation. Outputs follow MetodologIA brand standards and evidence tagging. [DOC]
Use when a page has traffic but visitors stall at a trust gate (signup, pay, book a call). Anti-scope: writing the offer itself, paid-media, A/B execution (see `conversion-optimization`), and full page layout (see `landing-page-builder`). [DOC]
Social proof influences; it does not manufacture credibility. A weak product with strong proof converts once, then churns — out of scope to fix that. [INFERENCE]

## Proof-Type Selection

Match the proof to the dominant objection, never decorate. [DOC]

| Objection | Strongest proof | Why it works |
|-----------|-----------------|--------------|
| "Does it actually work?" | Outcome testimonial / case study with a number | Concrete result beats adjectives |
| "Is it for someone like me?" | Testimonial from a matched persona/segment | Similarity drives identification |
| "Are others doing this?" | Usage counts, ratings, recent-activity | Consensus + recency cues |
| "Is this a real company?" | Client logos, press, certifications | Authority/legitimacy transfer |
| "What if it goes wrong?" | Guarantee, return policy, security badge | Risk reversal (pairs with proof) |

## Procedure

### Step 1: Discover
- Identify the single trust gate and the dominant objection at it; read exit surveys, support tickets, and session replays before guessing. [DOC]
- Inventory existing proof assets: real quotes, named clients, verifiable metrics, ratings, certifications — flag which are usable vs. need consent. [DOC]
- If no real proof exists, that is a `[VACIO_CRITICO]`-class gap: collect proof, never fabricate a quote, logo, or count. [ASSUMPTION]

### Step 2: Select & qualify
- Pick the proof type that answers the gate's dominant objection (table above); one primary type per gate, supporting types secondary. [DOC]
- Prefer specific over generic: a named person + role + company + number ("cut onboarding 40%, Maria L., Ops Lead, Acme") outconverts "Great product!". [INFERENCE]
- Verify every claim is true and consented: attributable source, real metric, written permission to publish name/logo. [DOC]
- Evaluate against Constitution principles (XIII Think First, XIV Simple First); record trade-offs. [DOC]

### Step 3: Place & execute
- Put proof adjacent to the action it de-risks: testimonial beside the CTA, security badge at the pay button, logos near the headline claim. [DOC]
- Lead the page with the strongest single proof; cluster the rest into a scannable band — quantity without relevance dilutes. [INFERENCE]
- Apply evidence tags to all claims; use the brand template for HTML outputs (references/brand/). [DOC]

### Step 4: Validate
- Confirm every displayed claim is verifiable, consented, and attributed; remove any orphan or paraphrased quote. [DOC]
- Check proof sits at the gate, not buried in a footer; check evidence-tag coverage and Constitution compliance. [DOC]
- Hand the placement to `conversion-optimization` for A/B validation; do not assert lift here — placement is a hypothesis, not a result. [INFERENCE]

## Worked Example

Pricing page: trial signups stall at the plan-select CTA; exit surveys cite "will this work for a team my size?". [DOC]
Dominant objection = fit, not legitimacy → primary proof is a segment-matched outcome testimonial, not more logos. [INFERENCE]
Selected: "Onboarded 30 reps in a week — Sara K., RevOps @ midmarket SaaS," placed beside the CTA; 3 client logos kept as a secondary band. [DOC]
Consent confirmed in writing; the 30-reps figure traces to a signed case study. The generic "Best tool ever!" quote is cut for being unattributable. [DOC]
Placement is then routed to `conversion-optimization` to test; this file does not claim the lift. [INFERENCE]

## Quality Criteria

- [ ] Follows Constitution principles (Think First, Simple First).
- [ ] Proof type matches the gate's dominant objection, not page decoration.
- [ ] Every claim is true, attributed (name/role/company), and consented to publish.
- [ ] Primary proof sits adjacent to the action it de-risks.
- [ ] No fabricated quotes, logos, counts, ratings, or "as seen in" claims.
- [ ] Evidence tags on all claims; gaps marked, never invented.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Acting without understanding | Wastes effort on wrong proof | Think First (XIII); start from the real objection |
| Over-engineering | Wall of badges dilutes signal | Simple First (XIV); one primary proof per gate |
| Fabricated / stock testimonials | Fraud + legal/reputational risk | Use only real, consented, attributable proof |
| Generic praise ("Love it!") | No information, no persuasion | Demand specificity: person, role, number |
| Vanity counts ("10,000+ users") with no context | Unverifiable, easily disbelieved | Tie the number to a verifiable source |
| Proof far from the action | Read after the decision is made | Place adjacent to the trust gate |
| Mismatched persona | Reader can't identify | Match testimonial segment to visitor segment |
| Missing evidence tags | Claims without basis | Tag every assertion |

## Related Skills

- `conversion-optimization` for ICE-ranking trust gaps and A/B-validating placements.
- `landing-page-builder` and `landing-pages` for executing the proof band in-page.
- `funnel-design` for which gate in the funnel needs proof first.

## Usage

Example invocations:

- "/social-proof" — Run the full social proof workflow
- "social proof on this pricing page" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and real, consented proof assets. [DOC]
- Requires English-language output unless otherwise specified. [DOC]
- Designs and places proof; it does not run the A/B test that proves the lift (see `conversion-optimization`). [DOC]
- Does not generate, paraphrase, or embellish testimonials, logos, or metrics — fabrication is a hard stop. [DOC]
- Does not replace domain expert judgment for final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No real proof available | Stop; recommend a proof-collection plan, never fabricate |
| Proof exists but no publish consent | Anonymize to segment-level or withhold until consent obtained |
| Negative / mixed reviews surfaced | Address objection honestly; do not suppress or cherry-pick deceptively |
| Regulated claims (health, finance) | Add required disclaimers; route claim wording to compliance review |
