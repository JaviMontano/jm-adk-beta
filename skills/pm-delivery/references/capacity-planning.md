<!-- distilled from alfa skills/capacity-planning -->
<!-- > -->
# Resource Capacity Planning & Demand Forecasting

**TL;DR**: Analyzes resource supply against demand to identify capacity gaps, over-allocations, and optimization opportunities. Produces time-phased capacity models that forecast resource needs, enabling proactive hiring, training, or reallocation decisions before bottlenecks impact delivery.

## Principio Rector
La capacidad real es siempre menor que la teórica. Un recurso al 100% de utilización no tiene capacidad para absorber variabilidad — ese es el camino al retraso sistémico. La regla: planificar al 80% de capacidad, reservar 20% para variabilidad, reuniones, y trabajo no planificado. La previsibilidad nace de la holgura deliberada. [EXPLICIT]

## Assumptions & Limits
- Assumes resource availability data is current and reflects actual calendars [SUPUESTO]
- Assumes demand data comes from approved project schedules, not wishful planning [PLAN]
- Breaks when resource data is >2 weeks stale — capacity model becomes fiction; refuse to publish, refresh first [EXPLICIT]
- Does not account for unplanned work unless historical unplanned-work ratio is provided [SUPUESTO]
- Planning at 80% utilization is a guideline; organizational policy may override [SUPUESTO]
- Multi-project capacity requires portfolio-level demand aggregation across all active projects [PLAN]

**Anti-scope** (this skill does NOT do): individual performance evaluation; salary/cost budgeting (use `cost-estimation`); recruiting execution or candidate sourcing; legal leave-policy interpretation. It outputs the *signal* (gap, timing, magnitude); the staffing *decision* belongs to resource managers and the sponsor. [EXPLICIT]

## Capacity Math (canonical formulas)
- **Net available hours** = calendar_hours − holidays − PTO − statutory leave [SCHEDULE]
- **Effective capacity** = net_available_hours × productivity_factor × (1 − context_switch_penalty) [INFERENCIA]
- **Productivity factor** baseline 0.70–0.80 of theoretical; never assume 1.0 [SUPUESTO]
- **Context-switch penalty** ≈ 0.20 per additional concurrent project beyond the first, capped (see Edge Case 2) [INFERENCIA]
- **Utilization** = committed_demand_hours ÷ effective_capacity. >0.80 = over-allocated; >1.0 = infeasible [METRIC]
- **Gap** = demand − effective_capacity, computed **per skill per period** (never aggregate-only) [METRIC]
- Agile variant: capacity = team_velocity × sprints_in_horizon, discounted for known PTO/ceremonies [METRIC]

## Usage

```bash
# Build capacity model for a project
/pm:capacity-planning $PROJECT --type=model --horizon="6-months"

# Detect over-allocations across the portfolio
/pm:capacity-planning $PROJECT --type=over-allocation --threshold=80

# Run what-if scenario for resource changes
/pm:capacity-planning $PROJECT --type=scenario --change="add-2-devs"
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `$PROJECT` | Yes | Project or portfolio identifier |
| `--type` | Yes | `model`, `over-allocation`, `scenario`, `gap-analysis` |
| `--horizon` | No | Planning horizon (3-months, 6-months, 12-months) |
| `--threshold` | No | Utilization threshold for over-allocation detection (default: 80) |
| `--change` | No | Scenario description for what-if modeling |

## Service Type Routing
`{TIPO_PROYECTO}`: Agile uses velocity-based capacity; Waterfall uses hours-based resource calendars; SAFe uses PI-level capacity allocation; Portfolio uses aggregate capacity across projects.

## Before Planning

1. **Read** the resource pool data to confirm current availability and skill assignments
2. **Read** the project schedule to extract demand by role and time period
3. **Glob** `skills/capacity-planning/references/*.md` for capacity planning models and benchmarks
4. **Grep** for historical utilization data to calibrate realistic capacity assumptions

## Entrada (Input Requirements)
- Resource pool with skills and availability
- Project demand (schedule + resource plan)
- Organizational calendar and leave policies
- Other project commitments per resource
- Historical utilization data

## Proceso (Protocol)
1. **Supply modeling** — Calculate available capacity per resource (hours/FTE per period)
2. **Demand modeling** — Aggregate resource demand from all project activities
3. **Gap analysis** — Compare supply vs. demand per skill/role per time period
4. **Over-allocation detection** — Flag resources allocated > 80%
5. **Bottleneck identification** — Identify critical skill shortages and timing
6. **Scenario modeling** — Model what-if scenarios (delays, scope changes, resource additions)
7. **Optimization recommendations** — Suggest reallocation, cross-training, or hiring
8. **Hiring/training plan** — If gaps require new resources, define acquisition timeline
9. **Dashboard creation** — Build capacity heatmap (role x time period)
10. **Review cadence** — Establish periodic capacity review schedule

## Edge Cases

1. **Single point of failure resource**: Flag immediately. Design cross-training plan with ≥1 backup per critical skill. Document bus factor risk in risk register. [PLAN]
2. **Resource shared across >3 projects**: Cap effective allocation at 60% per project to account for context-switching overhead. Document productivity loss assumption. [INFERENCIA]
3. **Demand exceeds supply with no budget for hiring**: Prioritize demand using WSJF or sponsor input. Present trade-off: scope reduction, timeline extension, or quality compromise. [STAKEHOLDER]
4. **Resource availability data is unreliable**: Use historical average availability (typically 70-75% of theoretical) as baseline. Tag as [SUPUESTO] and recommend improving data collection. [SUPUESTO]
5. **Part-time / fractional resource**: Model as effective FTE (e.g., 0.6), not headcount; a 0.6 FTE at 80% utilization gives 0.48 FTE of usable capacity. Never count a part-timer as a full backup for bus-factor. [INFERENCIA]
6. **Skill mismatch (right count, wrong skills)**: Aggregate headcount looks sufficient but per-skill gap analysis reveals shortage. Always resolve gaps at skill granularity; a surplus of one role does not offset a deficit in another. [EXPLICIT]
7. **Ramp-up of new hires**: Apply a productivity ramp (e.g., 30% → 60% → 90% over first three months) so a hire approved in M1 does not show full capacity until M3+. Align hiring lead time accordingly. [SUPUESTO]

## Failure Modes
- **Theoretical-100% trap**: planning at full availability hides all variability slack → systemic slippage. Mitigate via 80% rule. [EXPLICIT]
- **Aggregate-averaging trap**: portfolio looks balanced while a single skill in a single month is 200% over. Always time-phase per skill. [METRIC]
- **Stale-data fiction**: model reports green while reality diverged; never signal readiness with green color. Gate on data freshness ≤2 weeks. [EXPLICIT]
- **Optimistic-demand trap**: demand pulled from wishful roadmaps inflates need; accept only approved schedules. [PLAN]

## Example: Good vs Bad

**Good Capacity Plan:**

| Attribute | Value |
|-----------|-------|
| Supply model | Per-resource with skills, availability, and calendar |
| Demand model | Aggregated from all active project schedules |
| Gap analysis | Per role per month with visual heatmap |
| Over-allocations | Flagged with ≥80% threshold, 4 resources identified |
| Scenarios modeled | 3 what-if scenarios with impact analysis |
| Recommendations | Specific: cross-train 2 devs, hire 1 QA by Month 3 |

**Bad Capacity Plan:**
A spreadsheet showing "we need 10 developers" without supply analysis, no time-phasing, no skill breakdown, no over-allocation detection. Fails because it provides no actionable insight about when gaps occur, which skills are short, or what trade-offs exist. [EXPLICIT]

**Worked example (single role, one month)** [METRIC]
3 backend devs, 22 working days × 8h = 528 theoretical h. Subtract 5 PTO days (40h) → 488 net. Productivity 0.75 → 366 effective h. One dev also on a second project: context-switch penalty 0.20 on her share (~122h × 0.20 = 24h lost) → ~342 effective h. Committed demand = 410h. Utilization = 410 ÷ 342 = **1.20 → infeasible**. Signal: 68h gap (~0.4 FTE) for the month → recommend deferring 68h of scope, or pulling the dual-project dev fully onto this project (recovers 24h) plus a contractor for the rest.

## Key Decisions & Trade-offs
- **80% planning target vs higher utilization**: choosing 80% trades raw throughput for predictability and absorption of variability; only override above 85% for short, well-bounded crunch periods with explicit sponsor sign-off. [STAKEHOLDER]
- **Cross-train vs hire**: cross-training is cheaper and de-risks bus-factor but is slower to yield and dilutes the source role; hiring adds net capacity but carries ramp-up lag (Edge Case 7) and lead-time risk. Prefer cross-train for persistent low-grade gaps, hire for sustained structural shortfall. [INFERENCIA]
- **Buffer placement**: hold the 20% slack at the *constraint* role, not spread evenly — slack on a non-bottleneck resource buys nothing. [INFERENCIA]

## Validation Gate
- [ ] Supply model reflects actual resource calendars, not theoretical 100% availability
- [ ] Demand aggregated from ≥1 approved project schedule with role-level granularity
- [ ] Gap analysis produced per role AND per time period — not just aggregate totals
- [ ] Every resource >80% utilization flagged with specific over-allocation periods
- [ ] ≥2 what-if scenarios modeled with quantified impact on delivery dates
- [ ] Single-point-of-failure resources identified with cross-training recommendations
- [ ] Capacity heatmap visualization produced (role x period, color-coded by gap severity)
- [ ] Hiring or training plan includes acquisition timeline aligned with demand peaks
- [ ] Resource managers can plan proactively from the capacity model [STAKEHOLDER]
- [ ] Capacity review cadence established and aligned with methodology [PLAN]

## Escalation Triggers
- Critical skill gap with no available resource within 4 weeks
- Resource utilization > 100% for extended period
- Key resource departing with no succession plan
- Capacity model shows project deadline unachievable

## Salida (Deliverables)

- Primary deliverable: capacity plan with resource allocation model
- All outputs tagged with evidence markers
- Mermaid diagrams where applicable
- Executive summary for stakeholder consumption

## Additional Resources

| Resource | When to read | Location |
|----------|-------------|----------|
| Body of Knowledge | Before building model to understand capacity patterns | `references/body-of-knowledge.md` |
| State of the Art | When evaluating capacity planning tools | `references/state-of-the-art.md` |
| Knowledge Graph | To link capacity to resource plan and schedule | `references/knowledge-graph.mmd` |
| Use Case Prompts | When facilitating capacity workshops | `prompts/use-case-prompts.md` |
| Metaprompts | To generate capacity model templates | `prompts/metaprompts.md` |
| Sample Output | To calibrate expected capacity plan format | `examples/sample-output.md` |

## Output Configuration
- **Language**: Spanish (Latin American, business register)
- **Evidence**: [PLAN], [SCHEDULE], [METRIC], [INFERENCIA], [SUPUESTO], [STAKEHOLDER], [EXPLICIT]
- **Branding**: #2563EB royal blue, #F59E0B amber (NEVER green), #0F172A dark
