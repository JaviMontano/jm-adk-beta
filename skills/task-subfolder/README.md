# task-subfolder

Scaffold or resume a canonical **T-NNN** multi-session sub-task folder under a
workspace `tasks/` root. Convention **P33**. The folder is the durable memory
for a task that outlives a single conversation: it carries the operating
contract, the goal + acceptance criteria, and an append-only session journal.

## What it does

Given a one-line goal, it resolves the next free `T-NNN` id (or resumes a named
one), slugs the goal, and writes three artifacts **missing-only** (idempotent):

| File | Role |
|---|---|
| `CLAUDE.md` | Local operating contract: scope boundary, allowed tools, tag family, "read `log.md` first each session", links to parent memory. |
| `task.md` | Goal, context, constraints, audience, and an acceptance checklist (`- [ ]`). Unknowns become `{POR_CONFIRMAR}`. |
| `log.md` | Header plus the first dated append-only entry recording creation or resumption. |

## When to use

- A task is **multi-session** or needs its own persistent memory.
- Operator says "crear subtarea / task-subfolder / T-NNN".

## When NOT to use

- A single-turn deliverable (no folder needed).
- Authoring a *skill* under `skills/` → that is `skill-creator`, not this.

## How it routes / executes

1. Resolve id + path (read before write): list parent dir, find highest `T-NNN`,
   assign N+1; if an existing id is named, **resume** it.
2. Probe the three files for existence — write only the absent ones unless
   `--force`.
3. Write `CLAUDE.md`, `task.md`, `log.md`; append the first `log.md` entry.
4. Run the validation gate (see `SKILL.md` §4) before declaring "done".

## Evidence taxonomy (Jarvis OS tag family)

`{MEMORIA}` `{EXTRAIDO_HILO}` `{INFERENCIA}` `{SUPUESTO}` `{POR_CONFIRMAR}`
`{VACIO_CRITICO}` `{AUTOCOMPLETADO}`. Never mix in Alfa `[…]` tags inside the
generated task folder. Full rules: `references/verification-tags.md`.

## References

- `SKILL.md` — full procedure, gate, edge cases, anti-patterns.
- `references/verification-tags.md` — the Jarvis vs Alfa tag boundary.
- `knowledge/body-of-knowledge.md` — P33 convention, idempotency model, decision rules.
- `templates/output.md` — the deliverable scaffold (the three artifacts + summary).
- `assets/` — deterministic checklist + quality rubric used by the gate.
- `prompts/` — primary, meta, and quick/deep variations.
- `evals/evals.json` — behavioral test cases.

## Related skills

- `naming-and-slugging` — deterministic T-NNN slugs.
- `skill-creator` — when the artifact is a skill, not a task folder.
- `workflow-forge` — chaining multiple T-NNN tasks.
