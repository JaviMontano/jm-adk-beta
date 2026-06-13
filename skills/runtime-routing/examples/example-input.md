# Example Input — Runtime Routing

## Scenario

A maintainer wants to harden a repository and open a pull request. The work is:

> "I need to apply a small refactor across three files, run the repo's lint and
> unit-test scripts to prove it's green, then open a PR with `gh`. I'm currently
> in VS Code but I don't care where it runs — just pick the safest place. Some of
> these files reference API keys, so don't leak anything."

## Stated context

- **Requested runtime / current IDE:** VS Code (current), runtime choice open.
- **Output surface:** a pull request + a passing local validation run.
- **Constraints:** secrets must not leave the local boundary; `gh` auth status is
  unknown (may fail).

## Repo evidence available (what discovery would find)

- `AGENTS.md` — present, documents a Codex/local CLI adapter and the lint + test
  scripts. [DOC]
- `CODEX.md` — present, documents the file-edit + `git` PR flow. [DOC]
- `.agent/` — **absent** (no Antigravity/VS Code IDE-rule evidence). [DOC]
- MCP config — **absent** (no MCP server evidence). [DOC]
- `gh auth status` — **not executed this session** (auth unverified). [SUPUESTO]

## Required capabilities

1. Multi-file edits.
2. Shell validators (lint + unit tests).
3. `git` + `gh` PR flow.
4. Secret-boundary enforcement.

## Question to the skill

Which runtime should this run on, what is the capability boundary, and what is the
fallback if `gh` auth turns out to be unavailable?
