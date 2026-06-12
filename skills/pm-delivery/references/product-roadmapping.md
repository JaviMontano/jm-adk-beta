<!-- distilled from alfa skills/product-roadmapping -->
<!-- > -->
# Product Roadmapping

> "Plans are useless, but planning is indispensable." — Dwight D. Eisenhower

## TL;DR

Builds strategic product roadmaps with evidence-based prioritization (RICE, MoSCoW, or Kano) aligned to business value streams and user needs. Use when planning a new product, defining release strategy, or when a backlog needs strategic ordering beyond gut feeling. Output is a Now/Next/Later roadmap plus a scored backlog with rationale — not a dated feature list. [DOC]

## Anti-Scope

- Not a delivery plan: no sprint breakdown, capacity allocation, or Gantt — hand off to `cost-estimation` and sprint planning. [SUPUESTO]
- Not requirements: roadmap items stay at outcome/theme altitude; specs live in `requirements-engineering`. [SUPUESTO]
- Not a commitment device: horizons express intent and confidence, not contractual dates. Selling Later items as fixed dates is the top misuse. [INFERENCIA]

## Procedure

### Step 1: Discover
- Gather product vision, business objectives, and measurable success metrics (the metric, not "improve X").
- Inventory existing backlog, feature requests, and technical debt; tag each with its source so confidence is traceable. [INFERENCIA]
- Identify market pressures, hard deadlines (regulatory, contractual), and competitive dynamics.

### Step 2: Analyze
- Apply a prioritization framework. RICE: `(Reach × Impact × Confidence) ÷ Effort`. Use one framework per roadmap — mixing scales breaks comparability. [INFERENCIA]
- Categorize items with MoSCoW (Must/Should/Could/Won't) **per release**, not globally — "Must" is meaningless without a release boundary. [INFERENCIA]
- Map features to value streams and user-journey stages; flag items that touch no journey stage as candidate cuts. [INFERENCIA]
- Identify dependencies and the critical path; a high-RICE item blocked by a low-RICE prerequisite inherits the prerequisite's timing. [INFERENCIA]

### Step 3: Execute
- Build a Now/Next/Later roadmap aligned to OKRs. **Now** = committed, high confidence; **Next** = directional, sized; **Later** = hypothesis, unsized. [SUPUESTO]
- Define release themes with measurable outcomes, not feature lists ("cut checkout abandonment", not "add Apple Pay").
- Produce a prioritized backlog with scores and rationale for top items.
- Document trade-offs and what was deprioritized, with the reason and the metric that would reopen it. [INFERENCIA]

### Step 4: Validate
- Verify scores are data-driven; spot-check Confidence inputs — it is the most-gamed RICE factor. [INFERENCIA]
- Confirm dependencies are feasible within the proposed horizon ordering.
- Check that each release delivers user-facing value (no pure-tech releases unless explicitly a debt/platform horizon).
- Review with stakeholders for alignment on trade-offs, not just the accepted list.

## Worked Example (RICE)

| Item | Reach (users/qtr) | Impact (0.25–3) | Confidence | Effort (pw) | Score | Horizon |
|---|---|---|---|---|---|---|
| One-click checkout | 8,000 | 2 | 80% | 4 | 3,200 | Now |
| Saved carts | 5,000 | 1 | 100% | 2 | 2,500 | Next |
| AI size advisor | 12,000 | 3 | 30% | 9 | 1,200 | Later |

Read: AI advisor has the widest reach yet ranks last — low Confidence and high Effort sink it. The fix is not to drop it but to move a discovery spike into Now to raise Confidence before committing build effort. [INFERENCIA]

## Framework Selection

| Use | When | Trade-off |
|---|---|---|
| RICE | Comparing many items on one scale | Needs numeric Reach/Effort; false precision if inputs are guesses [SUPUESTO] |
| MoSCoW | Scoping a single fixed release | No ranking within a tier; "Must" inflation [INFERENCIA] |
| Kano | Differentiation / satisfaction trade-offs | Requires user research input; heavier to run [SUPUESTO] |

## Quality Criteria

- [ ] Roadmap uses outcome-oriented themes, not feature laundry lists.
- [ ] One documented prioritization framework, applied consistently.
- [ ] Dependencies mapped and validated against team capacity.
- [ ] Each horizon has measurable success criteria.
- [ ] Deprioritized items carry a reason and a reopen trigger. [INFERENCIA]
- [ ] Evidence tags applied to all non-obvious claims (single Alfa family). [DOC]

## Acceptance Criteria

- Every Now item maps to an OKR and a named owner. [SUPUESTO]
- Every roadmap horizon names the metric it moves; no horizon is feature-only.
- Confidence inputs for top-5 RICE items are sourced (data, research, or stated assumption), not bare percentages. [INFERENCIA]
- The trade-off log lists at least the top deprioritized item and why.

## Anti-Patterns & Failure Modes

- **Feature factory**: roadmap as a feature list without strategic themes.
- **Date-driven roadmap** that ignores scope uncertainty — Later items sold as fixed dates. [INFERENCIA]
- **HiPPO prioritization**: Highest-Paid-Person's-Opinion overriding the framework.
- **Confidence inflation**: every item at 100% — the score collapses to Reach×Impact÷Effort and stops discriminating. Cap unsourced Confidence at 50%. [SUPUESTO]
- **Global MoSCoW**: applying Must/Should without a release boundary, so everything becomes Must. [INFERENCIA]
- **Theme-washing**: a feature list relabeled with theme headers but no measurable outcome behind each.

## Related Skills

- `cost-estimation` — effort estimates feeding roadmap feasibility.
- `requirements-engineering` — detailed specs for roadmap items.
- `executive-pitch` — presenting the roadmap to leadership.

## Usage

Example invocations:

- "/product-roadmapping" — Run the full product roadmapping workflow.
- "product roadmapping on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Requires English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final decisions. [SUPUESTO]
- RICE/Kano outputs are only as good as their inputs; garbage Reach/Confidence yields confidently-wrong rankings. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No quantitative data for RICE | Fall back to MoSCoW or T-shirt sizing; mark scores `[SUPUESTO]` and flag for validation |
| Hard external deadline (regulatory/contractual) | Treat as a fixed constraint, schedule backward from it, surface scope at risk |
| Single dominant stakeholder (HiPPO) | Keep the framework visible; record overrides as explicit trade-offs, not silent reorders |
| Backlog too large to score fully | Score the top tier; bucket the rest into Later without per-item scores |
