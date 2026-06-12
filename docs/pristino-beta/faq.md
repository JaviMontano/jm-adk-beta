# Pristino Beta FAQ

## Is Beta public?

No. [CONFIG] It is a private pre-release repository.

## When will it be public?

The planned framing is Ciclo 2 of the 2026 Programa de Empoderamiento. [SUPUESTO]
The exact publication decision depends on release gates.

## Why do I see 404?

GitHub returns 404 for private repos when the user lacks access. [CONFIG] Confirm
access before debugging credentials.

## Is Beta replacing Alfa?

Not today. [CONFIG] Alfa remains the public operational harness. Beta is a
separate private track that generalizes the harness through catalog and profiles.

## What is the biggest technical difference?

Beta uses `catalog/skills.json` as the source of truth and generates runtime
surfaces. [DOC] Alfa exposes a larger direct skill/agent/prompt surface. [DOC]

## What is currently blocking public release?

On the inspected universal branch, `validate-coverage.py` passes but
`check-token-budget.py` fails. [CONFIG] 3-runtime smoke and eval validation also
belong to the release checklist. [CONFIG]

## Can I edit AGENTS.md or CLAUDE.md?

No. [CONFIG] They are generated runtime surfaces. Edit the canonical source and
regenerate.

## Which persona should I use first?

Use vibe-coder for runnable software and knowledge-worker for sourced research
or documents. [CONFIG]

## Can Beta show prices?

Pricing is profile-scoped. [DOC] The MetodologIA profile forbids client-facing
prices and requires effort units with disclaimers. [DOC]

## What should a first task look like?

Small, real and verifiable. [INFERENCIA] Example: "Create a one-page operating
brief from these notes" or "Build a tiny app slice that solves this weekly
friction."
