# Pristino Beta Private Preview

## Teaser

Pristino Beta is the next Pristino harness line: smaller, catalog-driven and
profile-based. [DOC] It is designed for two primary users:

- Vibe coder: builds mini/super apps through short build-run-observe loops. [DOC]
- AI-native knowledge worker: delegates research, synthesis, documents,
  decisions and operations to agents with provenance. [DOC]

Beta is not public yet. [CONFIG] It is planned for public release with Ciclo 2
of the 2026 Programa de Empoderamiento, subject to gates. [SUPUESTO]

## Functional Direction

Beta consolidates the Alfa skill surface into a smaller catalog. [DOC] The repo
states `611 alfa skills -> 73 beta skills`, with `catalog/skills.json` as the
single source of truth. [DOC]

The core idea is not "more prompts". [INFERENCIA] It is a harness that resolves
the active profile first, then routes work through a compact skill catalog and
runtime-specific adapters.

## Technical Shape

- `catalog/skills.json`: source of truth for skills and aliases. [DOC]
- `runtime/core.md`: common runtime contract. [DOC]
- `runtime/delta-*`: runtime-specific behavior for Claude Code, Antigravity and
  Codex. [DOC]
- `profiles/`: active profile layer for brand, quality and persona behavior.
  [DOC]
- `harness/manifest.json`: harness metadata, outputs, token budgets and MCP
  server declarations. [DOC]
- `references/ontology/constitution-v7.0.0.md`: domain-neutral constitution
  with personas, estimation integrity and profile-driven deliverable quality.
  [DOC]

## Current Gate Status

- `python3 scripts/validate-coverage.py`: PASS on inspected branch. [CONFIG]
- `python3 scripts/check-token-budget.py`: FAIL on inspected branch. [CONFIG]
  Current measured failures: `claude-code 3075/2600`, `antigravity 4514/4000`,
  `codex 3118/2300`.
- `validate-evals.py` and 3-runtime smoke remain required before public release.
  [CONFIG]

## What Can Be Said Publicly

- Beta exists as a private pre-release. [CONFIG]
- It is related to Alfa but separate. [CONFIG]
- It is aimed at vibe coders and AI-native knowledge workers. [DOC]
- It is planned for Ciclo 2 2026, subject to validation. [SUPUESTO]

## What Must Not Be Said

- Do not say Beta is generally available. [CONFIG]
- Do not promise public access dates beyond the Ciclo 2 framing. [CONFIG]
- Do not hide failing release gates. [CONFIG]
- Do not grant or imply collaborator access. [CONFIG]
