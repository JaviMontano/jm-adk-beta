# iikit — Intent Integrity Kit Router

`iikit` is a router skill for the **Intent Integrity Kit (IIK)**: a spec-driven
development pipeline that converts intent into shipped code through ordered,
hash-locked gates. It reads exactly one stage playbook per invocation and applies
it at the requested depth. [DOC]

## What it does

Resolves a `topic` (a named pipeline stage or its `00`–`08` number, plus the
off-spine helpers `clarify`, `bugfix`, `core`) and dispatches to the single
matching playbook under `references/`. Each stage emits one artifact that feeds
the next stage; the kit's value is that nothing downstream can silently drift
from upstream intent. [DOC]

The spine, in order:

| # | Topic | Artifact produced |
|---|-------|-------------------|
| 00 | `00-constitution` | `CONSTITUTION.md` (tech-agnostic governing principles) |
| 01 | `01-specify` | `spec.md`, `checklists/requirements.md`, `qa/acceptance-criteria.md` |
| 02 | `02-plan` | `plan.md` (architecture, tech choices, contracts) |
| 03 | `03-checklist` | quality checklist gates |
| 04 | `04-testify` | hash-locked Gherkin `.feature` files + `qa/test-coverage.md` |
| 05 | `05-tasks` | ordered task breakdown |
| 06 | `06-analyze` | cross-artifact consistency + quality-gate analysis |
| 07 | `07-implement` | code held to the locked scenarios |
| 08 | `08-taskstoissues` | GitHub issues seeded from tasks |

Off-spine helpers: `clarify` (resolve `[NEEDS CLARIFICATION]`), `bugfix` (fix
existing broken behavior, not new capability), `core` (init / status / use /
help). [DOC]

## When to use

Trigger on any spec-driven request: authoring a constitution, a spec, a plan,
a checklist, tests, a task list, or driving implementation/bugfix. A named stage
(or its number) routes to that topic; a described intent routes to the earliest
unmet stage. Do **not** use for ad-hoc coding with no spec artifact in play. [INFERENCE]

## How it routes and executes

1. Resolve `topic` — the enum is authoritative and numbers map 1:1. Ask only on
   genuine ambiguity; never fan out across playbooks. [CONFIG]
2. Read **exactly one** playbook from the `routes:` map. Loading the whole
   cluster defeats the router and burns context. [INFERENCE]
3. Apply by `depth`: `deep` → exhaustive, verify each step and each gate;
   `quick` → essentials, single pass. [CONFIG]
4. Honor the predecessor rule — never run a stage on a missing predecessor
   artifact; create it explicitly or stop. [INFERENCE]

## Evidence taxonomy

Outputs carry the IIK provenance tags: `[EXPLICIT]` (stated in source playbook),
`[DOC]`, `[CONFIG]`, `[INFERENCE]`/`[INFERENCIA]`, `[ASSUMPTION]`/`[SUPUESTO]`.
Use exactly one family per artifact; never mix Spanish and English tag sets. [CONFIG]

## References

- [SKILL.md](SKILL.md) — router contract, params, validation gate
- [references/core.md](references/core.md) — init / status / use / help
- [references/00-constitution.md](references/00-constitution.md) — governing principles
- [references/01-specify.md](references/01-specify.md) — feature spec (WHAT/WHY)
- [references/02-plan.md](references/02-plan.md) — architecture & tech (HOW)
- [references/03-checklist.md](references/03-checklist.md) — quality gates
- [references/04-testify.md](references/04-testify.md) — hash-locked Gherkin
- [references/05-tasks.md](references/05-tasks.md) — task breakdown
- [references/06-analyze.md](references/06-analyze.md) — consistency analysis
- [references/07-implement.md](references/07-implement.md) — implementation
- [references/08-taskstoissues.md](references/08-taskstoissues.md) — GitHub issues
- [references/bugfix.md](references/bugfix.md), [references/clarify.md](references/clarify.md)

## Bundle

- `agents/` — role contracts (lead, specialist, support, guardian)
- `knowledge/` — body of knowledge + concept graph
- `prompts/` — primary, meta, and quick/deep variations
- `templates/output.md` — stage-routing deliverable scaffold
- `evals/evals.json` — routing and gate-enforcement test cases
- `examples/` — a worked routing example
- `assets/` — quality rubric + routing checklist (see [assets/README.md](assets/README.md))
