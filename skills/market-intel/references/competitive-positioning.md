<!-- distilled from alfa skills/competitive-positioning -->
<!-- > -->
# Competitive Positioning

> "Method over hacks. Evidence over assumption."

## TL;DR

Frameworks to map competitors, build feature/capability comparisons, and articulate defensible differentiation. Outputs follow MetodologIA brand standards and carry Alfa-core evidence tags (`[DOC]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`, canon in `references/verification-tags.md`). [DOC]

**Use when** you need a positioning statement, a battle card, or a comparison matrix grounded in checkable evidence — not a generic SWOT. **Don't use** for pricing strategy, GTM sequencing, or win/loss interview design (those are separate skills). [SUPUESTO] — confirm scope with requester if the ask blends these.

## Procedure

### Step 1: Scope the competitive set
- Name the buyer, the job-to-be-done, and the decision the analysis informs (deal, roadmap, pitch). [SUPUESTO]
- Classify rivals: **direct** (same JTBD, same buyer), **indirect** (different solution, same JTBD), **substitute** (status quo / build-it-yourself). Tag each. [INFERENCIA]
- Cap the set at 3–5 named rivals plus "status quo". More dilutes signal; fewer misses the real alternative the buyer weighs. [INFERENCIA]

### Step 2: Gather evidence per competitor
- Pull from project artifacts, public docs, and prior analyses; cite the source for every factual claim. Mark inferred capability as `[INFERENCIA]`, unverified as `[SUPUESTO]`. [DOC]
- For each rival capture: positioning claim (their words), proof points, target segment, pricing model (model only — never invent figures), and observable weaknesses. [DOC]
- Flag any claim you cannot source rather than asserting it. A `[SUPUESTO]` with a verification step beats a confident guess. [DOC]

### Step 3: Build the comparison
- Choose axes that map to **buyer decision criteria**, not to your own feature list — otherwise the matrix flatters you and persuades no one. [INFERENCIA]
- Score each rival per axis with a consistent rubric (e.g. ✓ / partial / ✗, or 0–3). Define the rubric inline so scores are reproducible. [DOC]
- Identify the 1–2 axes where you are both **differentiated and the buyer cares** — that intersection is the positioning, not the longest column of checkmarks. [INFERENCIA]

### Step 4: Articulate & validate
- Draft a positioning statement: _For [buyer] who [need], [product] is the [category] that [differentiator], unlike [primary alternative]._ [DOC]
- Stress-test: would the named competitor disagree with your weakness claim? If not, it's table stakes, not an edge. Demote it. [INFERENCIA]
- Verify evidence-tag coverage and brand compliance before HTML render (`references/brand/`). [CONFIG]

## Worked Example (abridged)

Buyer: mid-market RevOps lead. JTBD: forecast accuracy.

| Axis (buyer criterion) | Us | Rival A (direct) | Status quo (spreadsheet) |
|---|---|---|---|
| Forecast accuracy | ✓ ML-backed [DOC] | partial, rules-only [INFERENCIA] | ✗ manual [DOC] |
| Setup time | partial (2 wk) | ✓ (3 days) | ✓ (none) |
| Audit trail | ✓ [CONFIG] | ✗ | ✗ |

Positioning lands on **forecast accuracy + audit trail** (differentiated AND valued), not setup time (where Rival A wins). [INFERENCIA]

## Quality Criteria

- [ ] Competitive set scoped to buyer + JTBD, status quo included
- [ ] Axes derive from buyer decision criteria, with a stated scoring rubric
- [ ] Every factual claim sourced; inferred/unverified claims tagged accordingly
- [ ] Differentiation sits at "differentiated ∧ buyer-valued", not feature count
- [ ] No invented prices; pricing expressed as model only
- [ ] Single evidence-tag family, consistent spelling; brand template applied to HTML

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|---|---|---|
| Feature-list comparison | Flatters you, ignores what the buyer weighs | Axes = buyer decision criteria |
| Everyone is a competitor | Dilutes signal, no real alternative surfaces | 3–5 rivals + status quo (Simple First, XIV) |
| Asserting weaknesses you can't source | Battle card collapses on first objection | Tag `[SUPUESTO]` + verification step |
| Claiming table stakes as differentiation | Persuades no one; rival agrees | Demote to parity; keep only contested edges |
| Inventing competitor pricing | Governance breach, erodes trust | Pricing model only, never figures |
| Acting without scoping the decision | Wrong analysis for the actual need | Think First (XIII) |

## Assumptions & Limits

- Assumes access to project artifacts and public competitor material; gaps surface as `[SUPUESTO]`. [SUPUESTO]
- Snapshot in time — competitor positioning drifts; re-validate before reuse in a new deal. [INFERENCIA]
- English-language output unless otherwise specified. [DOC]
- Informs but does not replace domain-expert and sales judgment for the final call. [DOC]
- Anti-scope: pricing strategy, GTM/launch sequencing, win/loss program design. [DOC]

## Edge Cases

| Scenario | Handling |
|---|---|
| Empty or minimal input | Request buyer, JTBD, and named rivals before proceeding |
| No named competitor (new category) | Position against status quo / substitute; state the category you're creating |
| Conflicting requirements | Flag explicitly, propose resolution, do not silently pick |
| Competitor claim unverifiable | Tag `[SUPUESTO]`, attach verification step, never assert as fact |
| Single dominant incumbent | Focus on the wedge: the one axis where the incumbent is structurally weak |
| Out-of-scope request | Redirect to the appropriate skill or escalate |

## Related Skills

- `market-intel` siblings for sizing and trend inputs that feed Step 1 scoping
- `references/verification-tags.md` — evidence-tag canon
- `references/brand/` — HTML output template

## Usage

- "/competitive-positioning" — Run the full workflow
- "competitive positioning on this project" — Apply to current context
- "build a battle card vs <rival>" — Steps 2–4 against one named competitor
