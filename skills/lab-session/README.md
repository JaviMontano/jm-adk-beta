# lab-session

Scaffolds one JM Labs Lab session as the four canonical files of protocol P08:
`notas.md`, `hipotesis.md`, `referencias.md`, `decision.md`. Missing-only by
default — it never overwrites a file a human already edited. [DOC]

## What it does

Given a session topic and (optionally) a slug, target Lab root, initial
hypothesis, and seed references, it materializes a single
`<lab-root>/<slug>/` folder holding exactly the four P08 files, each with its
canonical skeleton, and prints a one-line `created vs skipped` summary. [DOC]

## When to use

- A user asks to start / create a Lab, an experiment, or a P08 session.
- A loose idea or hypothesis needs a structured home before it becomes a real
  project.
- The four-file scaffold itself is the goal.

Do NOT use it to: edit an existing session's content (Read + Edit directly),
produce a client-facing deliverable (wrong brand — Lab files are internal JM
Labs scratch), or run/score the experiment. [INFERENCE]

## How it routes and executes

One run = one session folder. The flow is a fixed spine:

1. **Discover** — resolve slug + target path; `Bash`-check for an existing
   `<slug>/` and any of the four files.
2. **Plan** — classify each of the four target paths as CREATE (absent) or
   SKIP (present). No overwrite without explicit `--force`.
3. **Execute** — `Write` only CREATE files with the canonical per-file
   skeleton; touch nothing classified SKIP.
4. **Validate** — re-list the folder, confirm all four files exist and CREATE
   files are non-empty, emit the created/skipped summary.

## Agents

- `agents/lead.md` — orchestrates Discover → Plan → Execute → Validate and owns
  the P08 four-file contract.
- `agents/specialist.md` — P08 protocol depth: file semantics, falsifiable
  hypothesis framing, Alfa-core tagging.
- `agents/support.md` — deterministic filesystem execution (classify, Write,
  re-list).
- `agents/guardian.md` — runs the validation gate and blocks partial or
  overwriting scaffolds.

## References

- `references/verification-tags.md` — Alfa-core evidence tag canon and
  homologation rules.
- `knowledge/body-of-knowledge.md` — P08 protocol, file contracts, decision
  vocabulary, missing-only semantics.

## Assets

See `assets/` for the validation rubric and per-file skeleton specs the
guardian and support agents apply.

## Evidence convention

Alfa core set, EN spelling, one tag per claim:
`[CODE]` / `[CONFIG]` / `[DOC]` / `[INFERENCE]` / `[ASSUMPTION]`.
