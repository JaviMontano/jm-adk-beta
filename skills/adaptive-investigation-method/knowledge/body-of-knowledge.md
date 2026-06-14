# Body of Knowledge — Adaptive Investigation Method

Domain knowledge for building agents that investigate unknown domains under a bounded exploration budget. All claims carry provenance tags.

## 1. Key concepts

- **Surface map.** A cheap, structural index of the domain built with `Glob`/`Grep` (names, paths, entrypoints, symbol hits). It captures *where signal might be*, not file bodies. Mapping is free against the budget. [DOC]
- **Hard budget.** A fixed integer of expensive reads (or tokens) set **before** mapping. It is the termination guarantee: the loop must stop when the counter hits zero even if the domain is infinite. [DOC]
- **Expensive read (deep-dive).** A full `Read` of one node's body. Each one decrements the budget by one (or by token cost). [DOC]
- **Ranked hypotheses.** An ordered list by expected value / cost; each hypothesis names the map nodes that would confirm or invalidate it. No deep-dive without a hypothesis pointing at the node. [INFERENCIA]
- **Typed scratchpad.** Persisted state separating `plan`, `hypotheses`, `findings`, `replans`, `budget.remaining`, `stop_reason`. Replaces fuzzy prose memory. [INFERENCIA]
- **Disciplined re-plan.** Re-prioritization that fires **only** on `hypothesis_invalidated`. Confirmation or no-change keeps momentum. [DOC]
- **Provenance tag.** `[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]` attached to every finding so the deliverable is reconstructable. [DOC]
- **Stop reason.** `goal_resolved` or `budget_exhausted`. Unused budget on `goal_resolved` is success, not waste. [INFERENCIA]

## 2. Standards and invariants

- **Budget-first invariant.** Budget is fixed and visible before the first deep-dive; absent budget → `{VACIO_CRITICO}`, stop and ask, never auto-fill. [DOC]
- **Cheap-map invariant.** The map phase issues zero full reads; if content is needed, that is a deep-dive and must be justified. [DOC]
- **Hypothesis-before-read invariant.** Every expensive read is justified by a ranked hypothesis it confirms or refutes. [INFERENCIA]
- **Replan-only-on-invalidation invariant.** The only legal re-plan trigger is `hypothesis_invalidated`. [DOC]
- **Traceable-deliverable invariant.** The deliverable is synthesized from `findings`, each with a node reference and a provenance tag. [DOC]
- **Discover-not-mutate invariant.** The method discovers and reports; it never writes to or changes the investigated domain. [DOC]

## 3. Decision rules

| Situation | Rule | Tag |
|---|---|---|
| Domain < ~15 files / fits one context window | Do **not** use the method; read it whole. | [SUPUESTO] |
| `goal` or `budget` missing | Emit `{VACIO_CRITICO}`; stop and request. | [DOC] |
| Map returns no hits | Report "no detectable surface"; review `surface_root`; no blind deep-dives. | [INFERENCIA] |
| Deep-dive confirms or leaves hypothesis intact | Continue to next node; do **not** re-plan. | [DOC] |
| Deep-dive invalidates active hypothesis | Re-prioritize; record `replan` with invalidating evidence. | [DOC] |
| Node delegates (re-export / call-out) | Treat as a lead; follow the delegate, partially invalidate "it happens here". | [INFERENCIA] |
| Two hypotheses tied in rank | Prefer the one **cheapest to invalidate** (max info per budget unit). | [SUPUESTO] |
| All hypotheses invalidated, budget remains | Generate new hypotheses from findings; else close `goal_unresolved` honestly. | [INFERENCIA] |
| Goal resolved on first deep-dive | Close immediately; unused budget is success. | [INFERENCIA] |
| Domain edited mid-investigation | Invalidate affected map region; consider fork vs fresh (`session-lifecycle-management`). | [SUPUESTO] |

## 4. Trade-offs (engineering rationale)

- **Hard vs adaptive budget.** Hard bound guarantees termination and is auditable; cost is that a deeper-than-expected domain may stay partially mapped — declared, not hidden. [INFERENCIA]
- **Cheap map vs read-everything.** The map loses body-level detail but covers N× more surface per budget unit; justified when signal lives in structure. [INFERENCIA]
- **Replan-on-invalidation vs every-turn.** Always-replan maximizes adaptation but causes loops of doubt and wastes reasoning; invalidation-only conserves momentum at the cost of one extra turn for a "nearly refuted" hypothesis. [INFERENCIA]

## 5. Anti-patterns (blocked by the gate)

- Rigid full upfront plan with no adaptation. [DOC]
- Reading every file (blows the context budget). [DOC]
- Reflexive re-plan every turn. [DOC]
- Deep-diving "what looks interesting" without a hypothesis. [INFERENCIA]
- Re-mapping the whole domain each turn. [INFERENCIA]
- Synthesizing the deliverable from memory instead of findings. [INFERENCIA]

## 6. Related knowledge

- `provenance-engineering` — trace each finding to its source. [DOC]
- `session-lifecycle-management` — fork vs fresh when the world changes mid-investigation. [DOC]
- Kata 19 / `katas-adaptive-investigation` — practice loop for budgeted investigation. [DOC]
