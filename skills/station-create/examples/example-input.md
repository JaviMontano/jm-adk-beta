# Example input — station-create

A realistic invocation that exercises the universal path end to end.

## Trigger

```
station-create
```

## Intent

> "Stand up a station for Knowledge Ops — a shared place where any sector's
> research, notes, and synthesis cadences live. It should be reusable across
> sectors, not tied to one."

## What the skill must infer / confirm

| Input | Value | Source |
|---|---|---|
| Station name | Knowledge Ops | stated |
| Type | universal | "reusable across sectors, not tied to one" → universal [INFERENCE] |
| Bound sector | N/A | universal stations bind no sector [DOC] |
| Slug | `knowledge-ops` | derived kebab-case [INFERENCE] |
| One-line purpose | "Shared research, notes, and synthesis surface." | stated |
| Target path | (resolved from workspace + universal placement) | registry/parent CLAUDE.md [CONFIG] |

## Pre-conditions

- No station exists yet at the resolved `knowledge-ops` path. [INFERENCE]
- Active workspace present; placement guard allows the write. [CONFIG]

## Expected behavior

The skill derives the slug, confirms type=universal (no sector prompt needed),
guards the path, scaffolds missing-only with a Rule-9 `CLAUDE.md`, upserts the
registry binding, and runs the acceptance gate. See `example-output.md`.
