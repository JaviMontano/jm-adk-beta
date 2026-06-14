# Body of Knowledge — Intent Integrity Kit (iikit)

Domain knowledge the router relies on. Grounded in the IIK playbooks under
`references/`. [DOC]

## 1. Core concept: intent integrity

The kit exists to prevent **intent drift** — the silent divergence between what a
project was meant to do (intent) and what its code actually does. Each stage
produces an artifact that constrains the next, so downstream work cannot
contradict upstream intent without a detectable, deliberate change. [DOC]

## 2. The pipeline spine (ordered gates)

```
00-constitution → 01-specify → 02-plan → 03-checklist →
04-testify → 05-tasks → 06-analyze → 07-implement → 08-taskstoissues
```

Each arrow is a hard dependency: a stage consumes its predecessor's artifact.
Off-spine helpers — `clarify`, `bugfix`, `core` — branch off the spine but do
not replace a stage. [DOC]

| Stage | Boundary it enforces |
|-------|----------------------|
| constitution | governance vs. implementation (no tech/stack) |
| specify | WHAT/WHY vs. HOW (no architecture, no code) |
| plan | HOW lives here: stack, contracts, architecture |
| testify | requirements → tests; everything downstream is held to locked scenarios |
| implement | code is fixed to pass tests, tests are never edited to pass code |

## 3. Key standards and rules

- **Phase separation.** Tech-agnostic principles in the constitution; tech
  choices only in the plan. A stack reference in the constitution is a defect to
  auto-fix or route to plan. [EXPLICIT]
- **Constitution semver.** MAJOR = remove/redefine a principle; MINOR = add a
  principle; PATCH = clarify. First ratification is `1.0.0`. When in doubt,
  bump higher — under-bumping hides breaking changes. [EXPLICIT]
- **Traceability.** Every Success Criterion (SC-XXX) maps to ≥1 Functional
  Requirement (FR-XXX); orphan SCs are defects. In testify, every scenario
  carries `@TS-XXX` + `@FR/@SC/@US` + one priority + one test-type tag. [EXPLICIT]
- **Assertion integrity (hash lock).** Testify stores a SHA256 of assertion
  content in `context.json` AND a git note. `07-implement` verifies it before
  coding; a mismatch means the `.feature` files were tampered with → block. The
  hash covers steps + tags, not comments/ordering. [EXPLICIT]
- **TDD determination.** Scanned from the constitution: mandatory / optional /
  forbidden. Conflicting MUST-for and MUST-against → treat as forbidden, cite
  both, halt. [EXPLICIT]
- **Script-first.** Deterministic `iikit-core` scripts are the source of truth
  for environment detection, prerequisites, feature stage, hashing, and
  next-step routing. Do not re-derive their logic in-model. [CONFIG]

## 4. Decision rules

| Question | Rule |
|----------|------|
| Which topic? | Named stage/number → that topic; described intent → earliest unmet stage; ambiguous → ask once. [INFERENCE] |
| Bug or feature? | Judge primary intent contextually, not by keywords. [EXPLICIT] |
| Predecessor missing? | Stop or create it explicitly; never run a stage on a missing predecessor. [INFERENCE] |
| How many playbooks to read? | Exactly one. Re-route if wrong; never stack a second. [INFERENCE] |
| Constitution vs. plan content? | Principles → constitution; stack/tools/versions → plan. [EXPLICIT] |
| GitHub issues / repo create? | Require explicit user confirmation; never auto-create. [EXPLICIT] |

## 5. Evidence taxonomy

IIK provenance tags: `[EXPLICIT]` (stated in playbook), `[DOC]`, `[CONFIG]`,
`[INFERENCE]`/`[INFERENCIA]`, `[ASSUMPTION]`/`[SUPUESTO]`. Use one family per
artifact; never mix Spanish and English tag sets. [CONFIG]

## 6. Anti-patterns

- Loading the whole reference cluster "to be safe". [INFERENCE]
- Guessing `topic` instead of asking on genuine ambiguity. [ASSUMPTION]
- Skipping a predecessor stage to reach implementation faster. [INFERENCE]
- Manually re-hashing edited `.feature` assertions (defeats the lock). [EXPLICIT]
- Leaving a `[PLACEHOLDER]` to "fill later" in PREMISE.md or the constitution. [EXPLICIT]
