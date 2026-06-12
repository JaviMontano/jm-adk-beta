# Meta prompt — station-create

Guidance for the orchestrator routing to or composing station-create. This is
about *whether and how* to invoke the skill, not the scaffolding itself.

## Activate when

- An operating surface is being **stood up** and no station exists at its target
  path yet.
- The intent is long-lived (a surface that runs cadences), not a bounded project
  or a one-off task.
- Reached via `jarvis-os` routing or the `station-create` / `crear-estacion`
  triggers.

## Do NOT activate when

- The station **already exists** → route to its cadence/skill; never
  re-scaffold.
- The target is a **project** (`project-create`) or a **sector**.
- The request is a **one-off task** inside an existing surface → task
  scaffolder.

## Pre-flight the orchestrator should resolve

1. Is the abstraction really a station (surface) vs project (effort)?
2. Is the type knowable from the request, or must the skill ask
   (`{POR_CONFIRMAR}`)?
3. For dedicated: is the owning sector named?
4. Does the target path already exist (collision)?

## Hand-off contract

Pass: intent text, declared type (if any), sector (if dedicated), slug (if
fixed), and target path. The skill will stop and ask rather than guess any
missing required input.

## Quality bar

Output must pass the acceptance gate: correct path/slug, recorded type,
P06/P23/P24 structure, `CLAUDE.md` ≤70 lines, no clobbered files, clean registry
binding, consistent Alfa-core tags. No prices, single-brand.
