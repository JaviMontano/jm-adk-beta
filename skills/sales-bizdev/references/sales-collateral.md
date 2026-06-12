<!-- distilled from alfa skills/sales-collateral -->
<!-- > -->
# Sales Collateral

> "Method over hacks. Evidence over assumption."

## TL;DR

Produce four collateral artifacts — one-pager, battle card, ROI calculator, competitive positioning — for a single brand, each evidence-tagged and rendered through the MetodologIA brand template. Output is decision-support material, never a contract or a quote. [DOC]

## Artifacts (what each one is, when to use it)

| Artifact | Audience | Answers | Done when |
|----------|----------|---------|-----------|
| One-pager | Economic buyer | "What is this, why now?" | Problem, approach, proof, next step fit on one page [DOC] |
| Battle card | Sales rep, internal | "How do I win vs. competitor X?" | Per-competitor: their pitch, our counter, traps to avoid, proof point [DOC] |
| ROI calculator | Finance / champion | "What return, on what assumptions?" | Inputs, formula, and every assumption tagged + editable [INFERENCIA] |
| Competitive positioning | Strategy / marketing | "Where do we win, where do we cede?" | Axes named, honest cede-zones, no strawman rivals [SUPUESTO] |

## Procedure

### Step 1: Discover
- Gather target artifact, brand, competitor set, and buyer role from user input. If artifact or brand is unstated, ask before generating — do not default. [DOC]
- Read existing collateral, brand template (`references/brand/`), and any product/proof data in-repo. [CONFIG]
- Identify the single buying question the artifact must answer; one artifact = one question. [INFERENCIA]

### Step 2: Analyze
- Evaluate framing against Constitution principles XIII (Think First) and XIV (Simple First). [DOC]
- Separate proof points by strength: in-repo evidence > documented claim > assumption. Demote anything you cannot point to. [INFERENCIA]
- For competitive artifacts, name at least one zone where a rival legitimately wins — credibility dies on strawmen. [SUPUESTO]
- Record trade-offs (e.g. broad ROI range vs. precise-but-fragile single number) with the chosen side justified. [INFERENCIA]

### Step 3: Execute
- Draft against the artifact's "Done when" row above; cut anything not serving the buying question. [INFERENCIA]
- Tag every claim with one Alfa-core tag (`[DOC]`, `[CÓDIGO]`, `[CONFIG]`, `[INFERENCIA]`, `[SUPUESTO]`); see `references/verification-tags.md` for the canon. [DOC]
- ROI calculators: express value in FTE-months, percentages, or time saved — never currency amounts. State every assumption inline and make it editable. [DOC]
- Render HTML through the brand template; never hand-roll brand styling. [CONFIG]

### Step 4: Validate
- Run the Quality Criteria checklist below; every box must pass before handoff. [DOC]
- Confirm single-brand discipline: no other brand's name, color, or claim appears. [DOC]
- Confirm zero currency figures and zero unverifiable competitor claims. [INFERENCIA]

## Worked example (battle card excerpt)

Request: "Battle card vs. Competitor-A for the one-pager generator." [SUPUESTO]
- **Their pitch:** "Fastest setup, zero config." [SUPUESTO — verify on their live pricing/docs page before shipping]
- **Our counter:** Evidence-tagged output the buyer can audit; setup speed is table stakes, trust is the moat. [INFERENCIA]
- **Trap to avoid:** Don't compete on raw generation speed — you'll lose and it's not the buying criterion. [INFERENCIA]
- **Proof point:** Every claim in our output carries a provenance tag. [CÓDIGO — cite the tagging module in-repo]

## Quality Criteria

- [ ] Answers exactly one buying question; no scope creep [INFERENCIA]
- [ ] Every claim carries exactly one Alfa-core tag, one spelling throughout [DOC]
- [ ] Zero currency amounts; value in FTE-months / % / time [DOC]
- [ ] Single brand only — no mixed brand assets [DOC]
- [ ] Competitor claims are verifiable or tagged `[SUPUESTO]` with a verify step [SUPUESTO]
- [ ] Renders through brand template, not ad-hoc styling [CONFIG]
- [ ] Follows Constitution XIII / XIV; no redundancy or padding [DOC]

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Acting without understanding | Wastes effort on wrong artifact | Think First (XIII) [DOC] |
| Over-engineering the asset | Complexity buries the message | Simple First (XIV) [DOC] |
| Missing evidence tags | Claims without basis fail audit | Tag every assertion [DOC] |
| Quoting a price | Out-of-scope; creates liability | FTE-months + disclaimer [DOC] |
| Strawman competitor | Champion stops trusting the card | Name a real cede-zone [SUPUESTO] |
| Mixing brands in one asset | Breaks single-brand discipline | One brand per output [DOC] |
| Green = success styling | Implies certainty you lack | Neutral framing + tags [INFERENCIA] |

## Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| Unverifiable competitor claim shipped | No citation behind a `[SUPUESTO]` | Hold artifact; gather proof or soften to a hedge [INFERENCIA] |
| Currency leaked into ROI | Any `$`/amount in output | Convert to FTE-months or % before release [DOC] |
| Two brands in one file | Foreign logo/color/name present | Split into per-brand artifacts [DOC] |
| Artifact answers two questions | Buyer confused on next step | Split into two artifacts [INFERENCIA] |

## Related Skills

- Other `skills/sales-bizdev/` references (positioning, pricing-disclaimer, brand render). [SUPUESTO]

## Usage

Example invocations:

- "/sales-collateral" — Run the full sales collateral workflow
- "sales collateral on this project" — Apply to current context
- "battle card vs <competitor>" — Generate a single competitive artifact

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and the brand template. [DOC]
- English-language output unless otherwise specified. [DOC]
- Decision-support only — does not replace domain-expert judgment or constitute a contract/quote. [DOC]
- Brand and target artifact must be known; the skill asks rather than guessing. [INFERENCIA]

## Anti-Scope

- No pricing, discounts, or currency figures of any kind. [DOC]
- No legal terms, SLAs, or contractual commitments. [DOC]
- No multi-brand bundles in a single asset. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [DOC] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [DOC] |
| Out-of-scope request (price, contract) | Redirect to disclaimer pattern or escalate [DOC] |
| Competitor data unavailable | Tag `[SUPUESTO]` and attach a verify step; never invent [SUPUESTO] |
| No brand template present | Stop and request it; do not improvise brand styling [INFERENCIA] |
