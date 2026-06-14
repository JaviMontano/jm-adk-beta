# How to Install Private Beta

## Access Requirement

You need explicit access to `JaviMontano/jm-adk-beta`. [CONFIG] If you do not
have access, GitHub may return 404 when you open or clone the repo. That is
expected for a private repository.

## Clone

```bash
git clone https://github.com/JaviMontano/jm-adk-beta.git
cd jm-adk-beta
```

If the clone fails with repository not found, stop. [CONFIG] Do not debug SSH,
tokens or remotes until access is confirmed by the owner.

## First Commands

Run from the repo root:

```bash
python3 scripts/build-indexes.py
python3 scripts/validate-coverage.py
python3 scripts/check-token-budget.py
python3 scripts/validate-evals.py
```

Expected private-preview behavior on the inspected universal branch:

- `validate-coverage.py` passes. [CONFIG]
- `check-token-budget.py` fails and blocks public release. [CONFIG]
- A clean GA candidate must regenerate surfaces with no diff. [CONFIG]

## Runtime Start

Beta generates runtime adapters for Claude Code, Antigravity and Codex. [DOC]
Use the adapter your runtime reads:

- Claude Code: `CLAUDE.md`.
- Codex: `AGENTS.md`.
- Gemini/Antigravity: `GEMINI.md` and `.agent/rules/GEMINI.md`.

Do not hand-edit generated adapters. [CONFIG] Change the catalog, runtime core,
delta or profiles, then regenerate.

## Minimum Smoke

Before trusting a local install:

```bash
git status --short
python3 scripts/validate-coverage.py
python3 scripts/check-token-budget.py || true
python3 scripts/validate-evals.py
```

Record failures honestly. [CONFIG] A red token budget is not a runtime bug; it is
a release gate.

## Security

Do not commit secrets, local auth files or MCP tokens. [CONFIG] Use the
documented wrapper or runtime-specific auth flow when needed.
