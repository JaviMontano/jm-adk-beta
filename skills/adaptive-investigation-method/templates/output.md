# Adaptive Investigation Report

## Goal
<!-- The concrete question being resolved. Not "understand the repo". -->

## Budget
| Field | Value |
|---|---|
| Total (hard) | <N> reads / tokens |
| Used | <k> |
| Remaining | <N - k> |
| Termination guaranteed by | hard budget |

## Surface map (cheap)
<!-- Built with Glob/Grep only; structural; spent zero budget. -->
| Node | Region | How discovered | Candidate? |
|---|---|---|---|
| `path/to/node` | entrypoint / service / lib / test | `Glob`/`Grep -l ...` | yes |

## Ranked hypotheses
| # | Hypothesis | Target node(s) | Value/cost | Confirms if… | Invalidates if… |
|---|---|---|---|---|---|
| H1 | … | `…` | high | … | … |
| H2 | … | `…` | med | … | … |

## Deep-dive log
| Step | Node | Budget after | Verdict (confirm/intact/invalidated) | Evidence | Tag |
|---|---|---|---|---|---|
| 1 | `…` | <N-1> | … | line/symbol/value | [CÓDIGO] |

## Re-plan log
<!-- One row per re-plan. Allowed ONLY on hypothesis_invalidated. -->
| Re-plan | Invalidated hypothesis | Triggering evidence | New top hypothesis |
|---|---|---|---|
| R1 | H1 | `node delegates to …` | H3 → `…` |

## Findings
<!-- Synthesized from the deep-dive log, never from memory. Each node-referenced and tagged. -->
- **<node>** — <finding>. `[CÓDIGO]`
- **<node>** — <finding>. `[INFERENCIA]`

## Deliverable
<!-- The answer to `goal`, reconstructed from findings, citing the nodes. -->

## Stop reason
- `goal_resolved` | `budget_exhausted` | `goal_unresolved`
- Unused budget on resolution is efficiency, not waste.

## Coverage & residual risks
- Coverage: <full | partial — declare what was not explored>.
- Residual risks / assumptions to confirm: … `[SUPUESTO]`

---
Single brand: JM Labs. No invented prices. No client PII. Discover-not-mutate — this report changes nothing in the investigated domain.
