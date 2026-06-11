---
name: iikit
description: "Spec-driven pipeline: /iikit <constitution|specify|plan|checklist|testify|tasks|analyze|implement|taskstoissues|bugfix|clarify> [args]"
argument-hint: "<phase> [args]"
---
# /iikit

Phase wrapper over `skills/iikit` router. Phase = topic. Gates: artifact existence
(`scripts/check-prerequisites.sh`), constitution enforcement from `plan` onward,
hard checklist gate before `implement`. Semantic diff on re-run: preserve [x],
show downstream impact, confirm overwrite.
