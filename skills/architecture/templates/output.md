# Architecture Deliverable — <topic>

> Fill every field. No required field may stay `TBD`; if unknown, write the best
> `[ASSUMPTION]` and attach a verification step. Tags: one Alfa-core family, one
> spelling.

## 1. Routing record
- **Resolved topic:** <one of the nine enum values>
- **Depth:** quick | deep
- **Why this topic (not the near neighbor):** <one line> [INFERENCE]
- **Skipped (quick only):** <what was deliberately left out> | n/a

## 2. Context & drivers
- **Goal / request restated:** <...>
- **Ranked drivers (1 = top):**
  1. <driver> [DOC|INFERENCE]
  2. <driver>
- **Constraints:** <team, timeline, stack, compliance> [DOC]
- **Consumers / integrations:** <services, jobs, partners> [DOC]

## 3. Analysis
- **Patterns / selectors applied:** <from the playbook's tables> [DOC]
- **Quality-attribute scenarios (measure = number + unit):**
  - *source → stimulus → response → measure*: <e.g. "p95 < 300 ms at 1000 req/s"> [DOC]

## 4. Decision
| # | Option | Key criterion scores | Weighted / verdict |
|---|--------|----------------------|--------------------|
| 1 | <chosen> | <...> | **selected** |
| 2 | <rejected> | <...> | rejected |
| 3 | <baseline / do-nothing> | <...> | rejected |

- **Trade-off pair:** chose **<X>** over **<Y>** because **<quality attribute>**
  outranks **<other>** here. [INFERENCE]
- **Sensitivity / robustness:** <does the choice flip under ±20% weight or a
  changed driver?> [INFERENCE]

## 5. Architecture Decision Record (ADR)
- **Status:** proposed | accepted | superseded
- **Context:** <forces and constraints> [DOC]
- **Decision:** <what we will do> [DOC]
- **Consequences:** <costs paid, follow-on work, what gets harder> [DOC]
- **Rejected alternatives:** <option + reason> [INFERENCE]

## 6. Artifacts (topic-specific)
<OpenAPI fragment / context map / event flow / cache-tier table / migration
runbook / C4 refs — whatever the playbook prescribes> [CODE|DOC]

## 7. Assumptions & verification
| Assumption | How to verify | Owner |
|------------|---------------|-------|
| <[ASSUMPTION] claim> | <test / check / ask> | <who> |

## 8. Acceptance gate (guardian)
- [ ] One playbook loaded; topic ∈ enum; no cross-playbook bleed
- [ ] Every non-obvious claim tagged; one family, one spelling
- [ ] Each `[ASSUMPTION]` paired with a verification step
- [ ] Every recommendation names a rejected alternative + cost
- [ ] Scenarios use number + unit, not adjectives
- [ ] No invented prices (FTE-months only)
- [ ] Revisit trigger recorded: <condition to re-open the decision>
