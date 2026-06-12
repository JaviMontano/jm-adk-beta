---
name: vibe-coder
version: 1.0.0
owner: harness (persona default)
applies-to: solo iterative builders shipping working software in tight build-run-observe loops
---

# Profile — Vibe Coder (persona default)

> Persona-default deliverable-quality profile. No brand mandates. Satisfies Constitution
> Principle 9 (an active profile must declare the bar) for the fast-builder persona.
> Evidence tags: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`.

## Defaults
- **Depth**: `quick` — understand the blast radius of the change, not the whole repo.
- **Output**: working code first, minimal prose. Show the diff/snippet over a narrative.
- **Ceremony is proportional**: a one-line typo fix skips full spec/plan (record the skip in `tasklog.md`); a real feature still earns spec → plan → tests.

## Estimation
- Style: **decomposition + deterministic scripts** (sum of sized sub-tasks; compute the computable).
- Units: **hours or story points**. No mandated currency — price freely or not at all.
- Every estimate states its decomposition and `[ASSUMPTION]`s; no token-count/gut numbers.

## Non-negotiable (never bends for speed)
- **Tests**: production behavior is test-first; assertions are never weakened to pass.
- **Security**: secrets scan clean; access control at the data layer; input sanitized at the boundary.
- **Evidence**: technical claims carry evidence tags; `[ASSUMPTION]` ratio ≤ 30%.

## No brand mandates
No design tokens, voice, or content-authority rules. If a brand profile is also active, its standards apply on top of these.

**Acceptance**: change ships working + tested; security clean; estimate decomposed in effort units; ceremony matched to blast radius.
