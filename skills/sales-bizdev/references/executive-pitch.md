<!-- distilled from alfa skills/executive-pitch -->
<!-- This skill should be used when the user asks to "create a pitch", -->
# Executive Pitch & Business Case

Generates C-level presentations with quantified problem statements, 4-pillar value propositions, 3-option comparison analysis, investment summaries with financial models (NPV, IRR, payback), and decision frameworks. Uses Problem-Agitate-Solve (PAS) persuasion architecture. [EXPLICIT]

## Principio Rector

**Un pitch sin números es una opinión. Un pitch sin urgencia es un informe.** El executive pitch transforma meses de análisis técnico en una narrativa de decisión que un C-level puede aprobar en 30 minutos. Cada slide, cada dato, cada visual tiene un solo propósito: que el decisor diga "sí" con confianza.

**Scope.** Esta referencia define la arquitectura de persuasión, la estructura de 7 secciones, el modelado financiero y los gates de validación de un pitch ejecutivo. NO genera por sí sola los números base (vienen de fases previas o se declaran como supuestos), NO sustituye revisión de auditor financiero, y NO produce HTML salvo `{FORMATO}=html`. [DOC]

### Filosofía de Persuasión Ejecutiva

1. **Datos > opiniones.** Cada afirmación lleva un número. Cada número lleva una fuente o supuesto explícito. Sin números no hay credibilidad. [EXPLICIT]
2. **Costo de inacción > costo de acción.** El anchor no es el precio — es lo que pasa si NO se actúa. La urgencia no se declara, se demuestra con el burn rate de inacción. [EXPLICIT]
3. **Opciones, no mandatos.** 3 opciones con trade-offs claros. El decisor elige — el consultor recomienda con evidencia, no con presión. [EXPLICIT]
4. **Una decisión por pitch.** Si el ask contiene >1 decisión irreversible, divídelo: el decisor que duda en cualquier sub-decisión bloquea todo el aprobado. [INFERENCIA]

**Anti-objetivos** (lo que un buen pitch NO hace): no oculta riesgos para forzar el sí; no infla proyecciones para ganar mindshare a costa de credibilidad post-firma; no usa urgencia falsa (deadline inventado); no mezcla marcas MetodologIA en el mismo entregable. [DOC]

## Inputs

- `$1` — Decision-maker type: `cfo`, `cto`, `ceo`, `board` (default: `ceo`)
- `$2` — Budget range indicator: `under1m`, `1m-5m`, `over5m` (default: `1m-5m`)

Parse from `$ARGUMENTS`. Adapts emphasis based on audience. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
  - **piloto-auto**: Auto para construcción de narrativa y modelado financiero, HITL para validación de claims y call to action. [EXPLICIT]
  - **desatendido**: Cero interrupciones. Pitch completo auto-generado. Supuestos documentados. [EXPLICIT]
  - **supervisado**: Autónomo con checkpoint en financial model y call to action. [EXPLICIT]
  - **paso-a-paso**: Confirma problem statement, cada value pillar, financial model, y call to action. [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40% — S1 hero + S5 investment + S6 call to action) | `técnica` (full 7 sections, default)

## Conditional Logic by Audience

```
IF decision-maker is CFO:
  -> Lead with financial case: NPV, IRR, payback, cost avoidance
  -> Minimize technical detail; focus on financial metrics

IF decision-maker is CTO:
  -> Lead with technical modernization and risk reduction
  -> Include architecture summary; tech debt elimination path

IF decision-maker is CEO:
  -> Lead with strategic alignment and competitive advantage
  -> Market positioning, capability expansion, board-ready narrative

IF decision-maker is Board:
  -> Lead with governance, fiduciary responsibility, risk-adjusted ROI
  -> Include sensitivity analysis and worst-case scenarios

IF budget > $1M:
  -> Add sensitivity analysis: +/-20% cost, +/-10% timeline variance
  -> Include phased funding gates

IF budget > $5M:
  -> Add board-level governance section
  -> Quarterly re-calibration gates mandatory
  -> Kill criteria explicit per phase
```

**Precedence when signals conflict.** Audience-by-role wins over budget-by-size for *lead emphasis* (a CFO at $6M still leads with the financial case, then adds governance). Budget rules are *additive* (sections you append), audience rules are *ordering* (what comes first). If `$1` is `board`, treat as the strictest superset: financial + governance + sensitivity regardless of budget. [INFERENCIA]

**Worked example.** `$1=cfo`, `$2=over5m`: Section 1 hero leads with NPV/IRR/payback; Sections 4–5 carry full sensitivity (+/-20% cost, +/-10% benefit) and Monte Carlo; append board-governance + quarterly gates + per-phase kill criteria from the `>$5M` branch. [INFERENCIA]

## Financial Modeling

- **NPV:** Sum[(Year N benefit - Year N cost) / (1 + discount_rate)^N]. Discount rate: 10-15% for enterprise tech. Use the client's WACC if known; otherwise default 12% and tag the choice. [SUPUESTO]
- **IRR:** Internal rate of return where NPV = 0. Target >25% for 3-year payback. IRR is unreliable when cash-flow signs alternate (multiple roots) — fall back to NPV at a stated rate in that case. [INFERENCIA]
- **Payback Period:** Months until cumulative benefits = cumulative costs. Target <12 months. Report *both* simple and discounted payback when budget >$1M; they diverge as discount rate rises. [INFERENCIA]
- **Sensitivity Analysis:** +/-20% cost variance and +/-10% benefit variance on payback/NPV. Present as a 3x3 grid (low/base/high on each axis), not a single number. [DOC]
- **Break-Even:** What adoption rate or efficiency gain needed to break even.

Every financial input must cite its source or state its assumption explicitly. [EXPLICIT]

**Input contract.** Year-0 capex, per-year opex, per-year benefit stream, discount rate, and horizon (default 3 years) are required. Any missing input is a `{SUPUESTO}` paired with its verification step (e.g., "confirm savings rate with Finance"), never silently zeroed. [SUPUESTO]

**Failure modes to guard.** Double-counting a benefit across two value pillars (Section 3) and the comparison matrix (Section 4); benefits realized in Year 1 that physically require Year-1 implementation to finish first (phase the benefit curve to the delivery timeline); discount rate applied to nominal cash flows mixed with real ones. [INFERENCIA]

**No invented prices.** Estimate effort in FTE-months with disclaimers; do not assert dollar rates the client has not provided. Monetary figures in examples are illustrative placeholders, not quotes. [DOC]

## Persuasion Architecture (PAS)

1. **Problem:** Quantified pain metrics (current state numbers)
2. **Agitate:** Emotional impact + cost of inaction (monthly burn rate of inaction)
3. **Solve:** Proposed solution with clear benefits and ROI

**Anchoring:** Show worst-case first (inaction cost), then recommended option.
**Social proof:** Industry benchmarks, peer company results.
**Urgency:** Cost of delay quantified per month.

**Acceptance criteria for PAS.** Problem cites >=3 current-state metrics; Agitate states a per-month inaction burn rate (not a vague "soon"); Solve maps each benefit back to a Problem metric it closes. A Solve that introduces benefits with no Problem anchor is filler — cut it. [DOC]

## 7-Section Delivery Structure

### Section 1: Executive Summary (Hero)
3-4 hero KPIs: Cost Savings, Timeline, ROI Payback, Risk Reduction. 150-word narrative: opportunity, urgency, recommendation. [EXPLICIT]

### Section 2: Problem Statement & Current Pain
Business impact metrics table (current vs target vs gap vs annual impact). Pain points severity-rated (CRITICAL/HIGH/MEDIUM). Root cause analysis (technical, process, resource). Cost of inaction table (3-year projection). [EXPLICIT]

### Section 3: Strategic Value — 4-Pillar Proposition
Four value cards: Cost Reduction, Revenue Acceleration, Risk Mitigation, Technical Modernization. Each with metric, mechanism, ROI timeline, Year 1 impact. Cumulative 3-year financial metrics (TCO, NPV, IRR, payback). [EXPLICIT]

### Section 4: Approach Comparison (3+ Options)
Comparison matrix: Do Nothing vs Alternative vs Recommended. Dimensions: upfront cost, annual cost, 3-year TCO, payback, risk reduction, tech debt, scalability, compliance, velocity, implementation risk. Each option with pros/cons/outcome/financial impact. [EXPLICIT]

### Section 5: Investment Summary
Timeline and team table. Budget breakdown card (services, infrastructure, contingency, monthly burn). Phased investment table with gates. [EXPLICIT]

### Section 6: Call to Action & Decision Framework
What we ask for (approach, budget range, timeline, decision deadline). Approval checklist (CFO, CTO, business sponsor, steering). Next steps timeline (week-by-week post-approval). Cost of delay (monthly consequences). [EXPLICIT]

### Section 7: Risk Assessment & Mitigation
Risk table: probability, impact, mitigation, owner. Linked to findings from prior analysis phases. [EXPLICIT]

**Section sourcing map** (what each section consumes — prevents the "no prior phases" gap from going unnoticed):

| Section | Primary input source | If source missing |
|---|---|---|
| 1 Hero | Aggregates S2–S6 KPIs | Generate last, never first |
| 2 Problem | As-is analysis, current cost data | Use industry benchmarks, tag all `{SUPUESTO}` |
| 3 Value pillars | To-be design, savings model | Estimate from comparable engagements |
| 4 Comparison | Solution-roadmap options | Minimum viable: Do-Nothing vs Recommended |
| 5 Investment | Cost-estimation (FTE-months) | Stop — `{VACIO_CRITICO}`, ask before fabricating budget |
| 6 Call to action | Stakeholder map (decision owner) | Ask who signs; do not guess the approver |
| 7 Risk | Risk register from prior phases | Derive top-5 from option trade-offs |

Section 5 budget is the one input that must not be auto-filled: a fabricated number anchors the entire negotiation wrong. [INFERENCIA]

## Edge Cases

- **No CFO exists:** Lead with operational metrics (time savings, reduced risk) not NPV.
- **Budget pre-approved:** Skip financial justification; focus on execution confidence.
- **Competitor actively pitching:** Add competitive urgency section.
- **Multiple conflicting decision-makers:** Generate value cards per stakeholder concern.
- **Non-technical executive audience:** Zero jargon; business outcomes only; no architecture diagrams.
- **No prior phases completed:** Use industry benchmarks for all metrics; flag everything as estimated `{SUPUESTO}` with a verification step. Do NOT fabricate the Section-5 budget — stop and ask.
- **Tiny budget (<$200K):** Simplify to 3-section pitch (problem, solution, ask). Skip sensitivity analysis.
- **Mandated solution (no real choice):** Drop the 3-option matrix theater; lead with execution confidence and risk, frame the "do nothing" cost honestly. Faking options when the decision is made erodes trust. [INFERENCIA]
- **Hostile / skeptical CFO:** Lead with the conservative (worst-case) projection, not best-case; pre-empt the "your numbers are optimistic" objection by owning the downside first. [INFERENCIA]
- **Audience is the same person across roles** (e.g., founder = CEO + CFO): merge the financial and strategic leads into one Section 1; do not duplicate framing. [SUPUESTO]

## Trade-off Matrix

| Decision | Option A | Option B | When to Choose A | When to Choose B |
|----------|----------|----------|------------------|------------------|
| **Length** | 3-page executive summary | 15-page full business case | Time-constrained C-level; board pre-read | CFO deep-dive; formal procurement process |
| **Projections** | Aggressive (best-case) | Conservative (worst-case) | Competitive pitch; need to win mindshare | Risk-averse board; regulated industry |
| **Tone** | Push (prescriptive "do this") | Pull (consultative options) | Single decision-maker; clear mandate | Multiple stakeholders; consensus culture |
| **Financial depth** | Summary metrics (NPV, payback) | Full model (sensitivity, Monte Carlo) | CEO/CTO audience; budget < $1M | CFO/Board audience; budget > $5M |
| **Anchor** | Cost of inaction first | Recommended ROI first | Status-quo bias is the enemy; must create urgency | Audience already bought-in; needs the path, not the why |

**Default trade-off resolution.** When `{MODO}=desatendido` and no signal disambiguates: choose conservative projections, pull tone, summary financial depth, and inaction-cost anchor. These are the lowest-regret defaults — they cost mindshare but never credibility, and credibility is unrecoverable. [INFERENCIA]

## Assumptions & Limits

- Financial inputs (current costs, savings projections) sourced from prior phases or stated as assumptions
- NPV/IRR calculations use stated discount rate; sensitivity analysis covers variance
- Cannot replace financial auditor review for actual investment decisions
- Persuasion architecture is ethical: no misleading data, no false urgency, no suppressed risks
- Audience-specific framing adjusts emphasis, not facts
- Output quality is bounded by input quality: with all-benchmark inputs the pitch is directional, not commitment-grade — label it so
- Discount rate, horizon, and benefit-realization timing are the three assumptions that move NPV most; surface them, do not bury them in a footnote [INFERENCIA]

## Output Artifact

- `06_Pitch_Ejecutivo_Deep.{md|html}` — Executive pitch narrative (7-section or variante ejecutiva)
- `06b_Business_Case_Deep.{md|html}` — Detailed financial analysis with full sensitivity model
- Format determined by `{FORMATO}` parameter; default is Markdown

## Validation Gate

- [ ] Problem statement quantified with 3+ metrics (current to target with gap %)
- [ ] Financial impact calculated (annual cost of inaction, 3-year TCO, payback period)
- [ ] Value proposition across 4 pillars with specific metrics per pillar
- [ ] 3+ options compared with financial comparison
- [ ] Recommendation clear and strongly positioned with rationale
- [ ] Investment summary shows timeline, team, budget breakdown, phased funding gates
- [ ] Financial assumptions documented and justified; sources cited
- [ ] Sensitivity analysis for budgets >$1M
- [ ] Call to action names decision maker, deadline, and consequences of delay
- [ ] PAS framework applied (problem to agitate to solve)
- [ ] Every claim has a number; every number has a source or stated assumption
- [ ] No benefit double-counted between value pillars and the comparison matrix
- [ ] Benefit curve phased to the delivery timeline (no Year-1 benefit before Year-1 delivery)
- [ ] Decision owner in Section 6 matches a named person, not a role placeholder
- [ ] No fabricated budget: Section 5 sourced from cost-estimation or stopped for input
- [ ] Single brand throughout; no invented dollar prices (FTE-months + disclaimer)

**Gate is blocking.** Any unchecked box on the financial or sourcing items (budget, double-count, phasing, assumptions) fails the pitch — ship `{POR_CONFIRMAR}` rather than a confident wrong number. Cosmetic items (tone, length) are advisory. [DOC]

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | ✅ | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

Default output is Markdown with embedded Mermaid diagrams. HTML generation requires explicit `{FORMATO}=html` parameter. [EXPLICIT]

### Diagrams (Mermaid)
- Mindmap: 4 value pillars with key metrics
- Gantt chart: investment timeline by phase

---
**Author:** Javier Montano | **Last updated:** June 11, 2026

## Usage

Example invocations:

- "/executive-pitch" — Run the full executive pitch workflow
- "executive pitch on this project" — Apply to current context
