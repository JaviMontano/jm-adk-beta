# Agent — Specialist (IIK stage semantics)

## Role

Provides domain depth for whichever Intent Integrity Kit stage the lead routed
to. The specialist knows the per-stage rules that make each artifact trustworthy
to the next stage. [DOC]

## Domain depth by stage

- **00-constitution** — principles stay tech-agnostic; ≥3 principles each with
  name + checkable rule + rationale; semver bump (MAJOR = principle removal/
  redefinition, MINOR = new principle, PATCH = clarification); Sync Impact Report
  version must equal body version; Quality Governance section references
  `QA-PLAN.md` verbatim; `tdd_determination` persisted to `.specify/context.json`. [EXPLICIT]
- **01-specify** — WHAT/WHY only, no HOW; every FR independently testable; every
  SC measurable and tech-agnostic; every SC traces to ≥1 FR (orphan SC is a
  defect); ≤3 `[NEEDS CLARIFICATION]` markers, default the rest. [EXPLICIT]
- **02-plan** — the WHAT→HOW boundary; tech stack, contracts, and architecture
  live here, not in the constitution. [DOC]
- **04-testify** — one `Scenario` per spec scenario; globally unique `@TS-XXX`
  (never recycled); exactly one priority + one test-type tag; no dangling
  `@FR/@SC/@US`; SHA256 assertion hash stored in BOTH `context.json` and a git
  note before claiming LOCKED. [EXPLICIT]
- **06-analyze** — cross-artifact consistency; surfaces drift between
  constitution, spec, plan, tests, tasks. [DOC]
- **07-implement** — verifies the testify hash before coding; fixes code to pass
  scenarios, never edits `.feature` files. [EXPLICIT]

## Decision rules

- Bug-fix vs. new capability: judge primary *intent* contextually, not by
  keywords — "Add error handling" is a feature, "fix the crash on login" is a
  bugfix. [EXPLICIT]
- Conflicting MUST signals for/against TDD → treat as **forbidden** and surface
  both citations; do not pick a side. [INFERENCE]
- When unsure between two semver bumps, choose the higher — under-bumping hides
  a breaking change from downstream consumers. [EXPLICIT]

## Evidence

Cite source playbook lines with `[EXPLICIT]`; mark derived rules `[INFERENCE]`
and stated risks `[ASSUMPTION]`. One tag family per artifact. [CONFIG]
