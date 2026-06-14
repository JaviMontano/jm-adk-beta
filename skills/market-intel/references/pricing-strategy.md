<!-- distilled from alfa skills/pricing-strategy -->
<!-- tags: Alfa core set (kit-facing) per references/verification-tags.md -->
# Pricing Strategy

> "Method over hacks. Evidence over assumption."

## TL;DR

Design pricing pages and tier architecture using anchoring, value-based
framing, and behavioral decoys. Output follows MetodologIA brand standards and
Alfa-core evidence tagging. NEVER emit a concrete price — recommend structure,
positioning, and ranges-as-placeholders only; the client sets the number. [DOC]

## Scope & Anti-Scope

- IN: page layout, tier count/naming, anchor placement, framing copy, feature
  fencing, decoy design, willingness-to-pay (WTP) discovery method. [DOC]
- OUT: setting the actual dollar amount, tax/billing/invoicing logic, payment
  integration, legal terms, discount approvals. Redirect or escalate. [DOC]

## Levers (the moves you actually have)

| Lever | Mechanism | When it wins | Risk |
|---|---|---|---|
| Anchor | Show high tier first/largest so others read cheap | Wide value spread | Anchor too high → distrust [INFERENCIA] |
| Decoy | Add a dominated option to steer to target tier | 3-tier pages | Looks manipulative if obvious [SUPUESTO] |
| Value-based framing | Price vs. outcome ($/seat saved) not vs. cost | Quantifiable ROI | Needs a credible metric [INFERENCIA] |
| Feature fencing | Gate features to separate segments | Distinct personas | Over-fencing churns SMB [SUPUESTO] |
| Tier count | 3 default; 4 if a clear enterprise split exists | Mixed buyer sizes | >4 = choice paralysis [INFERENCIA] |

## Procedure

### Step 1: Discover
- Gather offer, target segments, and the buyer's value metric (what unit they
  associate with getting value: seats, GB, transactions). [DOC]
- Read existing pricing page, analytics on tier selection, and competitor
  pages. Capture current anchor and tier spread. [DOC]
- Surface WTP signal: prior deal sizes, willingness questions, or Van
  Westendorp if data exists; otherwise tag the gap `[SUPUESTO]`. [INFERENCIA]

### Step 2: Analyze
- Evaluate options against Constitution principles (XIII Think First, XIV
  Simple First) — fewest tiers that still segment buyers. [DOC]
- Pick the value metric that scales with customer success, not with your cost. [INFERENCIA]
- Choose anchor tier and (if 3+ tiers) whether a decoy is warranted; document
  the trade-off, don't just assert it. [DOC]

### Step 3: Execute
- Lay out tiers left→right by ascending value; highlight the target ("Most
  popular") tier — recommendation badges lift conversion to it. [INFERENCIA]
- Apply evidence tags to every non-obvious claim. Use brand template for HTML
  outputs (references/brand/). [CONFIG]
- Use ranges or placeholders for amounts (e.g. "$X / $2–3X / Contact us"),
  never invented figures. [DOC]

### Step 4: Validate
- Verify the anchor reframes (cheapest tier reads as a deal, not a downgrade). [INFERENCIA]
- Check evidence-tag coverage and single-family consistency (Alfa core only). [DOC]
- Confirm no concrete price leaked and Constitution compliance holds. [DOC]

## Worked Example (SaaS, 3 tiers)

Buyer value metric = active seats. Recommendation: Starter / **Pro (anchor,
"Most popular")** / Enterprise (Contact us). Pro carries the headline features;
Starter is fenced to 3 seats to push teams up; Enterprise has no listed price so
it never caps the anchor. Framing copy on Pro: "$X per seat — replaces ~Y hours
of manual work / seat / month." Amounts shown as placeholders for the client to
fill. [INFERENCIA]

## Quality Criteria

- [ ] Follows Constitution principles (Think First, Simple First)
- [ ] Evidence tags on all non-obvious claims, single Alfa-core family
- [ ] No concrete price emitted — ranges/placeholders only
- [ ] Each tier maps to a distinct buyer segment (no orphan tiers)
- [ ] Value metric scales with customer success, not vendor cost
- [ ] Output is actionable and specific; no redundancy or padding

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|---|---|---|
| Acting without understanding | Wastes effort on wrong solution | Think First (XIII) |
| Over-engineering tiers | Choice paralysis, no segmentation gain | Simple First (XIV); 3 tiers default |
| Emitting a concrete price | Violates governance; not our call | Ranges/placeholders, client decides |
| Cost-plus framing | Ignores buyer-perceived value | Value-based framing ($/outcome) |
| Obvious decoy | Reads as manipulation, erodes trust | Decoy must be plausibly real |
| Missing evidence tags | Claims without basis | Tag every assertion (Alfa core) |

## Related Skills

- `skills/market-intel` references (this kit): competitive-analysis, WTP discovery.

## Usage

Example invocations:

- "/pricing-strategy" — Run the full pricing strategy workflow
- "pricing strategy on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (offer, analytics, competitor pages). [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Does not set the final price or replace domain-expert/commercial judgment. [DOC]
- Behavioral effects (anchor, decoy) are directional heuristics, not guarantees;
  validate with the client's own conversion data when available. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|---|---|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No value metric identifiable | Tag `[SUPUESTO]`, propose WTP discovery step, do not invent one |
| Single undifferentiated segment | Recommend 1–2 tiers, not 3; skip the decoy |
| User demands a specific price | Decline per governance; offer ranges + the inputs they'd need |
