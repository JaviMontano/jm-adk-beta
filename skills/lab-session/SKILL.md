---
name: lab-session
version: 0.2.0
description: "Scaffold a JM Labs Lab session: the 4 canonical files (notas, hipotesis, referencias, decision) per protocol P08, missing-only and never overwriting local edits."
owner: "JM Labs"
triggers:
  - lab-session
  - crear-lab
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Lab Session

Materializes one Lab session as the four canonical files of protocol P08:
`notas.md`, `hipotesis.md`, `referencias.md`, `decision.md`. [DOC] One run
creates one session folder; reruns are additive (missing-only). [INFERENCE]

## When to Use

- User asks to start / create a Lab, an experiment, or a P08 session. [DOC]
- A loose idea or hypothesis needs a structured place to live before it
  becomes a project. [INFERENCE]
- Use when the four-file scaffold is the goal. NOT for: editing an existing
  session's content (use Read+Edit directly), producing client deliverables
  (wrong brand — see Anti-Scope), or running the experiment itself. [INFERENCE]

## Inputs

| Input | Required | Default if absent |
|---|---|---|
| Session topic / objective | yes | STOP and ask — terminal gap [ASSUMPTION] |
| Session slug (kebab-case) | no | derive from topic [INFERENCE] |
| Target Lab root path | no | current working dir [ASSUMPTION] |
| Initial hypothesis | no | `hipotesis.md` left as a prompt stub [INFERENCE] |
| Seed references | no | empty `referencias.md` skeleton [INFERENCE] |

Empty objective is a critical gap: do not invent a topic — ask. [INFERENCE]

## Outputs

A `<lab-root>/<slug>/` folder containing exactly four files:

- `notas.md` — running log, observations, dated entries.
- `hipotesis.md` — the claim under test, framed falsifiably. [INFERENCE]
- `referencias.md` — sources, links, prior art; each entry carries a tag.
- `decision.md` — the verdict (keep / pivot / kill) once the Lab closes;
  starts empty/`{POR_CONFIRMAR}`. [INFERENCE]

Plus a one-line console summary of created vs. skipped (pre-existing) files.

## Procedure

### 1. Discover
Resolve slug and target path. `Bash` a check for an existing
`<slug>/` folder and any of the four files. [INFERENCE]

### 2. Plan
Classify each of the four target paths as CREATE (absent) or SKIP (present).
Never plan an overwrite without an explicit `--force` from the user. [DOC]

### 3. Execute
`Write` only the CREATE files using the canonical skeleton per file (see
Outputs). Touch nothing classified SKIP. Keep folder scope to the one session.

### 4. Validate
Re-list the folder; confirm all four files exist and CREATE files are
non-empty. Emit the created/skipped summary.

## Validation Gate (acceptance criteria)

- [ ] Exactly the four canonical files present after run. [DOC]
- [ ] No pre-existing file was modified (byte-compare or mtime on SKIPs). [INFERENCE]
- [ ] `hipotesis.md` states a falsifiable claim or an explicit stub. [INFERENCE]
- [ ] Every `referencias.md` entry and every non-obvious note carries one
      Alfa-core tag (`[DOC]`/`[CONFIG]`/`[CODE]`/`[INFERENCE]`/`[ASSUMPTION]`),
      one spelling throughout. [DOC]
- [ ] Summary line reports created vs skipped counts.

Fail any box → fix before declaring done; do not green-light partial scaffolds.
Machine-readable gate + per-file skeletons: `assets/` (see `assets/README.md`). [DOC]

## Edge Cases

- **Folder exists, all four files present**: report "already scaffolded",
  change nothing, exit 0. [INFERENCE]
- **Partial scaffold** (some files present): create only the missing ones. [INFERENCE]
- **Slug collision with a different topic**: surface the conflict, ask before
  reusing the folder. [INFERENCE]
- **Non-writable target path**: stop with the path error, do not fall back to a
  surprise location. [ASSUMPTION]
- **Empty objective**: terminal gap — ask, never auto-fill. [INFERENCE]

## Anti-Scope

- Not a deliverable generator and not a brand-rendered document — Lab files are
  internal JM Labs scratch, never client-facing. [INFERENCE]
- Single-brand: JM Labs only. Do NOT emit MetodologIA or MetodologIA framing,
  palettes, or footers here. [DOC]
- Never introduce green as a success signal in any sample content. [DOC]
- Does not run, score, or conclude the experiment — only the verdict file is
  scaffolded; the human writes `decision.md`. [INFERENCE]

## Self-Correction Triggers

- About to overwrite a present file → STOP, reclassify as SKIP. [INFERENCE]
- Tempted to fabricate a topic from thin context → STOP, ask. [INFERENCE]
- More or fewer than four files in the plan → the P08 contract is broken; fix. [DOC]
- Mixed tag spellings or families → normalize to one before delivery. [DOC]

## Update-Safety Notes

- All four files are missing-only by default. [DOC]
- `--force` regenerates a file only after the user reviews the diff. [DOC]
- Local/experimental variants live under `.local/` and are never overwritten. [INFERENCE]

## Related Skills

- `workspace-governance` — where the Lab folder fits in the workspace tree.
- `workflow-forge` — promoting a kept Lab into a real workflow.
- `quality-guardian` — independent check of the validation gate.

## Evidence Convention

Alfa core set (kit-facing), EN spelling, one tag per claim:
`[CODE]` / `[CONFIG]` / `[DOC]` / `[INFERENCE]` / `[ASSUMPTION]`. Canon and
homologation: `references/verification-tags.md`. [DOC]
