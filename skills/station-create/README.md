# station-create

Scaffold a Jarvis OS **station** — a long-lived operating surface — into a
placed, governance-compliant skeleton: its folder, its own `CLAUDE.md`, and the
P06/P23/P24 structure for the chosen type. One job: placement. Routing,
cadences, execution, and reporting belong to downstream skills. [DOC]

## What it does

- Turns an intent ("set up a station for X") into a station folder bound to a
  slug, a type, and a path.
- Decides **universal** (shared, cross-cutting) vs **dedicated** (bound to one
  sector) — the first real decision, never guessed. [INFERENCE]
- Writes **missing-only**: existing files stay byte-for-byte intact unless
  `--force` is passed after a reviewed diff. [DOC]
- Registers the `station ↔ slug ↔ type ↔ path` binding, idempotently.

## When to use

- The station does not yet exist at its target path and an operating surface is
  being stood up.
- Invoked by `jarvis-os` routing or directly via the `station-create` /
  `crear-estacion` trigger.

**Do NOT use** when the station already exists (route to its cadence), when the
target is a project (`project-create`) or a sector, or for a one-off task inside
an existing surface (task scaffolder).

## How it routes / executes

1. **Discover** — resolve name → kebab-case slug; read registry + parent
   `CLAUDE.md` before writing.
2. **Type-resolve** — universal vs dedicated; dedicated requires a bound sector.
3. **Guard** — target path must not exist; never overwrite.
4. **Scaffold** — write only absent files; `CLAUDE.md` ≤70 lines by
   construction (Rule-9).
5. **Register** — confirm the `station ↔ slug ↔ type ↔ path` entry.
6. **Validate** — run the acceptance gate before declaring done.

## References & companion files

- `SKILL.md` — full procedure, inputs/outputs, acceptance gate, edge cases.
- `knowledge/body-of-knowledge.md` — station vs project, type model, P06/P23/P24,
  Rule-9, missing-only semantics.
- `knowledge/knowledge-graph.json` — concept graph over the skill's vocabulary.
- `templates/output.md` — the scaffold-summary deliverable.
- `agents/` — role contracts (lead, specialist, support, guardian).
- `prompts/` — primary, meta, and quick/deep variations.
- `examples/` — a worked universal-station scaffold.
- `assets/` — quality rubric and acceptance checklist used by the guardian gate.

## Evidence & safety

Tag non-obvious claims with one Alfa-core family
(`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`). Missing-only by
default; no prices; single-brand (JM Labs). [DOC]
