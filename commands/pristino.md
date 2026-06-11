---
name: pristino
description: "Dispatcher: /pristino <skill> [topic=...] [depth=quick|deep] [args...]. Routes any catalog skill."
argument-hint: "<skill> [params]"
---
# /pristino — dispatcher

Replaces alfa's 215+ per-skill command stubs.

1. Parse `$ARGUMENTS`: first token = skill id (resolve aliases via `catalog/skills.json.aliases`).
2. If unknown id: fuzzy-match tier-0 index, propose top 3, ask.
3. Read `skills/<id>/SKILL.md`. Router → resolve `topic` from remaining args or request context; read ONE playbook.
4. Execute with constitution enforcement; report in compressed register.
