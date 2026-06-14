# Deliverable scaffold — T-NNN sub-task folder

The skill produces a folder `T-NNN-<slug>/` plus a console summary. Below are the
three artifact scaffolds and the summary block. Jarvis tags only; no Alfa `[…]`.

---

## Artifact 1 — `T-NNN-<slug>/CLAUDE.md`

```markdown
# T-NNN · <slug> — local contract

## Scope
<one-line boundary of what this task does / does not cover> {EXTRAIDO_HILO}

## Allowed tools
Read, Write, Edit, Bash.

## Session protocol
- Read `log.md` first, then `task.md`, every session.
- Parent memory: <relative link to MEMORY.md / Golden Reference>.
- Log ordering: newest-at-<top|bottom> (fixed for this task's life).

## Tag family (use, do not mix Alfa)
{MEMORIA} {EXTRAIDO_HILO} {INFERENCIA} {SUPUESTO} {POR_CONFIRMAR}
{VACIO_CRITICO} {AUTOCOMPLETADO}
```

## Artifact 2 — `T-NNN-<slug>/task.md`

```markdown
# T-NNN · <slug>

## Goal
<one-line goal> {EXTRAIDO_HILO}

## Context
<context / background>

## Constraints
<constraints, if any>

## Audience
<audience> {AUTOCOMPLETADO if defaulted}

## Acceptance criteria
- [ ] <criterion 1> {POR_CONFIRMAR if drafted}
- [ ] <criterion 2>
```

## Artifact 3 — `T-NNN-<slug>/log.md`

```markdown
# T-NNN · <slug> — session log (append-only)

## YYYY-MM-DD · session 1 — created
- Status: scaffolded; <one-line status>. {INFERENCIA where reasoned}
```

---

## Console summary block

```
task-subfolder · T-NNN · <slug>
path:    <abs path to T-NNN-<slug>/>
written: <files created>
skipped: <files present, missing-only>
forced:  <files overwritten under --force, if any>
open:    <count> {POR_CONFIRMAR} items, <count> {SUPUESTO}
gate:    pass | fail (<reason>)
```
