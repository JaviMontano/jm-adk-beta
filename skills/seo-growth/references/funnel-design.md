<!-- distilled from alfa skills/funnel-design -->
<!-- > -->
# Funnel Design

> "Method over hacks. Evidence over assumption."

## TL;DR

Deterministic funnel blueprint: TOFU/MOFU/BOFU content mapping, lead scoring, nurture-flow logic, qualification rules, and sales handoff criteria — produced *before* implementation, campaign production, CRM setup, or analytics instrumentation. [EXPLICIT]

This is design, not measurement. It defines what should happen and why; `funnel-analytics` diagnoses what *did* happen after launch. [EXPLICIT]

## Procedure

### Step 1: Discover funnel context
- Capture product, offer, target audience, funnel goal, conversion event, sales motion, and content inventory. [EXPLICIT]
- Separate acquisition intent (TOFU), consideration intent (MOFU), and conversion intent (BOFU). [EXPLICIT]
- Normalize structured data to `assets/funnel-design-schema.json`. [EXPLICIT]
- Sales motion sets nurture aggressiveness: self-serve PLG tolerates shorter, in-product nurture; high-ACV enterprise needs longer multi-touch MOFU with human handoff. [INFERENCE]

### Step 2: Map content by stage
- Use `assets/stage-content-model.json` for awareness, education, evaluation, proof, objection-handling, and decision content. [EXPLICIT]
- Every stage row needs: owner, audience intent, core question, content assets, CTA, success metric. A row missing any field is incomplete, not "good enough". [EXPLICIT]
- Do not place BOFU sales pressure in TOFU unless the input explicitly requires direct response. [EXPLICIT]
- CTA must match intent altitude: TOFU asks for attention (subscribe/read), MOFU for consideration (compare/demo), BOFU for commitment (trial/buy/call). A "Buy now" on an awareness blog post is stage-mismatched. [INFERENCE]

### Step 3: Define lead scoring
- Use `assets/lead-scoring-model.json` across three axes: fit (firmographic), intent (declared need), engagement (behavior). [EXPLICIT]
- Scores map to explicit lifecycle states: cold → engaged → MQL → SQL → sales-ready, each with a numeric threshold and an entry condition. [EXPLICIT]
- Flag missing scoring evidence; never invent behavioral or firmographic data. Tag the gap `[SUPUESTO]` and name the source that would fill it. [EXPLICIT]
- Keep negative scoring explicit: competitors, job-seekers, students, and free-mail-only B2B leads should *lose* points, not silently pass. [INFERENCE]

### Step 4: Design nurture flow
- Use `assets/nurture-flow-schema.json`: triggers, delays, branch conditions, messages, exit criteria. [EXPLICIT]
- Tie every step to a lead-score change or stage-intent shift — no time-only drips without a behavioral hook. [EXPLICIT]
- Include reactivation and disqualification paths. Every flow must terminate: convert, recycle, or suppress. [EXPLICIT]
- Cap touch frequency and honor a global suppression list so a contact in two flows is not double-messaged. [INFERENCE]

### Step 5: Compile deterministic output
- Prefer `scripts/compile-funnel-design.py --input <json> --output <report.md>` when structured data exists; hand-author only when input is unstructured. [EXPLICIT]
- Return content map, scoring rules, nurture paths, gaps, risks, and handoff checklist in `templates/output.md` order. [EXPLICIT]

## Worked example (B2B SaaS, demo conversion) [INFERENCE]

| Stage | Intent | Core question | Asset | CTA | Metric |
|---|---|---|---|---|---|
| TOFU | Awareness | "Is this problem worth solving?" | SEO guide, benchmark report | Subscribe | Organic sessions → email opt-in rate |
| MOFU | Evaluation | "Is *this* the right approach?" | Comparison page, ROI calculator | Watch demo | MQL rate, demo-watch % |
| BOFU | Decision | "Why you, why now?" | Case study, pricing, security one-pager | Book a call | SQL→opportunity rate |

Scoring slice: fit ≥ 40 AND engagement ≥ 30 ⇒ MQL; MQL + demo-watched + ICP title ⇒ SQL (route to AE within 1 business day). [INFERENCE]
Nurture slice: trigger = demo-page visit, no booking in 48h → branch {ICP: AE email + case study | non-ICP: self-serve trial nudge}; exit on booking, trial start, or 3 unanswered touches (→ recycle 90 days). [INFERENCE]

## Quality Criteria

- [ ] TOFU/MOFU/BOFU stages are all present.
- [ ] Every stage has intent, content assets, CTA, metric, and owner.
- [ ] Each CTA matches its stage's intent altitude.
- [ ] Lead scoring is explicit, threshold-based, and includes negative scoring.
- [ ] Every lifecycle state has a numeric threshold and entry condition.
- [ ] Nurture flow has triggers, delays, branch rules, and a terminating exit for every path.
- [ ] Sales handoff criteria are deterministic (SLA + routing + fallback).
- [ ] Gaps are marked `[SUPUESTO]` with a verification step, not invented.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Stage soup | Content mixed without buyer intent | Map every asset to TOFU, MOFU, or BOFU |
| Vanity scoring | Points without qualification meaning | Link scores to lifecycle thresholds + negative scoring |
| Infinite nurture | No exit or handoff | Define trigger, branch, exit, and owner per path |
| CTA mismatch | High-commitment ask at low intent | Match CTA to stage altitude |
| Silent handoff | MQL "thrown over the wall" | Define SLA, routing, and fallback owner |
| Missing evidence tags | Claims without basis | Tag every assertion |

## Failure modes [INFERENCE]

| Symptom (caught at design time) | Root cause | Fix |
|---|---|---|
| Many MQLs, few SQLs | Threshold too low / no negative scoring | Raise fit gate, subtract for non-ICP signals |
| Leads stall mid-funnel | MOFU has no evaluation asset | Add comparison/proof content + score bump |
| Sales ignores MQLs | No SLA or trust in score | Make handoff deterministic; agree score with sales |
| Contacts churn from email | No frequency cap / suppression | Global cap + cross-flow suppression list |

## Related Skills

- `funnel-analytics` for measured conversion/drop-off diagnosis after launch.
- `conversion-optimization` for CRO experiments on a single page within the funnel.

## Usage

Example invocations:

- "/funnel-design" — Run the full funnel design workflow
- "funnel design on this project" — Apply to current context
- "Map TOFU/MOFU/BOFU content for this campaign" — Build content map and CTAs
- "Create lead scoring and nurture flow" — Build scoring thresholds and automation path

## Assumptions & Limits

- Assumes the user can provide audience, offer, goal, and at least one conversion event. [EXPLICIT]
- Does not claim or forecast campaign performance; route measurement to `funnel-analytics`. [EXPLICIT]
- Does not replace legal/privacy review for email, CRM, consent, or tracking (GDPR/CAN-SPAM/CASL opt-in and unsubscribe are out of scope here). [EXPLICIT]
- Scoring weights are starting defaults, not validated truth — they must be tuned against real conversion data post-launch. [SUPUESTO]
- Out of scope: ad-platform setup, creative production, attribution-model selection, and pricing. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request audience, offer, goal, conversion event, and sales motion |
| Missing content inventory | Produce gap map + minimum viable content plan per stage |
| Conflicting funnel goals | Flag conflict; split acquisition, activation, and revenue paths |
| No CRM or email platform | Produce platform-neutral nurture logic (triggers/branches as pseudo-rules) |
| Single-stage / direct-response offer | Collapse to TOFU→BOFU; document why MOFU is skipped |
| PLG / no human sales motion | Replace AE handoff with in-product activation trigger |
| Out-of-scope request | Redirect analytics to `funnel-analytics`, page CRO to `conversion-optimization` |

## Deterministic Assets

- `assets/manifest.json` lists local assets and consumers. [EXPLICIT]
- `assets/funnel-design-schema.json` defines required structured input. [EXPLICIT]
- `assets/stage-content-model.json` defines TOFU/MOFU/BOFU stage requirements. [EXPLICIT]
- `assets/lead-scoring-model.json` defines scoring dimensions and lifecycle thresholds. [EXPLICIT]
- `assets/nurture-flow-schema.json` defines nurture steps, branches, and exits. [EXPLICIT]
- `assets/qualification-rules.json` defines deterministic handoff/disqualification rules. [EXPLICIT]
- `scripts/compile-funnel-design.py` compiles a deterministic Markdown funnel design. [EXPLICIT]
