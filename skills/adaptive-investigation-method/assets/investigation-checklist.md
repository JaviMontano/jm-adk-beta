# Investigation Checklist — Adaptive Investigation Method

Run this before declaring an investigation complete. Every box must be checked with backing evidence (provenance tag), or the run is not done.

## Pre-flight
- [ ] `goal` is a concrete question, not "understand the domain". `[DOC]`
- [ ] `budget.total` is set and visible **before** mapping. `[DOC]`
- [ ] `surface_root` is defined. `[CONFIG]`
- [ ] If `goal` or `budget` is missing → `{VACIO_CRITICO}` emitted, run stopped. `[DOC]`

## Map phase
- [ ] Map built with `Glob`/`Grep` only — no full reads. `[CÓDIGO]`
- [ ] Map spent **zero** budget. `[DOC]`
- [ ] Empty map handled: "no detectable surface" reported, no blind deep-dives. `[INFERENCIA]`

## Hypothesis phase
- [ ] Hypotheses ranked by value/cost before the first deep-dive. `[INFERENCIA]`
- [ ] Each hypothesis names the node(s) that confirm or invalidate it. `[INFERENCIA]`
- [ ] Ties broken toward cheapest-to-invalidate. `[SUPUESTO]`

## Deep-dive phase
- [ ] Every deep-dive justified by a ranked hypothesis. `[INFERENCIA]`
- [ ] Each `Read` decremented the budget counter. `[DOC]`
- [ ] Each finding carries node reference + provenance tag. `[DOC]`

## Re-plan phase
- [ ] Re-plan fired **only** on `hypothesis_invalidated`. `[DOC]`
- [ ] `replans` count is well below deep-dive count (no thrash). `[INFERENCIA]`

## Close
- [ ] `stop_reason` recorded (`goal_resolved` | `budget_exhausted` | `goal_unresolved`). `[DOC]`
- [ ] Deliverable synthesized from `findings`, not memory. `[DOC]`
- [ ] Partial coverage declared if budget ran out. `[INFERENCIA]`
- [ ] No writes to the investigated domain. `[DOC]`

Single brand: JM Labs. No invented prices. No client PII.
