# Verification Tags

Inline provenance tags for claims and outputs. Two homologated families: the
Jarvis OS runbook set (operator-facing) and the Alfa core set (kit-facing).
Mark every non-obvious claim; for `{SUPUESTO}`/`{POR_CONFIRMAR}` propose the
next step that would verify it.

**Scope.** This file defines the tags and their homologation. It does not
define rendering, enforcement, or the prompts that emit them — those live in
the consumers listed at the bottom. [DOC]

**When to tag** [DOC]
- Tag any claim a reader could not reproduce from the prompt alone: external
  facts, derived numbers, defaults you chose, anything needing validation.
- Do NOT tag trivially self-evident statements, restated user input, or the
  output's own structure — over-tagging defeats scannability. [INFERENCIA]
- One tag per claim. If two could apply, pick the weaker (least-certain) one —
  a `{SUPUESTO}` dressed as `{MEMORIA}` is the failure mode that matters. [INFERENCIA]
- Pick the family by audience, not by content: operator output → Jarvis set;
  kit/repo output → Alfa set. Never mix families in one document. [SUPUESTO]

## Jarvis OS set (operator)

| Tag | Meaning |
|---|---|
| `{MEMORIA}` | From MEMORY.md / persistent context |
| `{ADJUNTO}` | From an attached/pasted file |
| `{EXTRAIDO_HILO}` | From the current conversation |
| `{WEB}` | Web search, with citation |
| `{CONOCIMIENTO}` | Pre-cutoff general knowledge |
| `{SUPUESTO}` | Explicit assumption |
| `{INFERENCIA}` | Derived reasoning, not fact |
| `{AUTOCOMPLETADO}` | Filled default without asking |
| `{POR_CONFIRMAR}` | Needs human validation |
| `{VACIO_CRITICO}` | Missing data; execution stopped |

`{WEB}` without a citation is invalid — degrade to `{CONOCIMIENTO}` or drop the
claim. `{VACIO_CRITICO}` is terminal: stop and ask, never auto-fill past it. [DOC]

## Alfa core set (kit)

| Tag | Meaning |
|---|---|
| `[CÓDIGO]` / `[CODE]` | Code/config present in repo |
| `[CONFIG]` | Configuration reference |
| `[DOC]` | Documentation/spec |
| `[INFERENCIA]` / `[INFERENCE]` | Logical deduction |
| `[SUPUESTO]` / `[ASSUMPTION]` | Claim without direct evidence |

`[CÓDIGO]`/`[CONFIG]` require the claim be checkable in-repo; if you cannot
point to it, it is `[SUPUESTO]`. ES and EN spellings are aliases, not distinct
tags — pick one spelling per document. [DOC]

## Mapping

Lossy by design: the Alfa set is coarser, so several Jarvis tags collapse into
one. Homologate Jarvis → Alfa, never the reverse (you cannot recover the
finer distinction). [INFERENCIA]

| Jarvis OS | Alfa core |
|---|---|
| `{CONOCIMIENTO}` / `{WEB}` | `[DOC]` |
| `{MEMORIA}` / `{ADJUNTO}` / `{EXTRAIDO_HILO}` | `[CONFIG]` / `[CÓDIGO]` |
| `{INFERENCIA}` | `[INFERENCIA]` |
| `{SUPUESTO}` / `{AUTOCOMPLETADO}` / `{POR_CONFIRMAR}` | `[SUPUESTO]` |
| `{VACIO_CRITICO}` | (stop + ask) |

Disambiguation for the split row: source from a file/repo artifact →
`[CÓDIGO]`; source from a settings/config value → `[CONFIG]`. [SUPUESTO]

## Acceptance criteria (for a tagged output)
- Every non-obvious claim carries exactly one tag from a single family. [DOC]
- No `{WEB}` without citation; no `{VACIO_CRITICO}` followed by fabricated data.
- Every `{SUPUESTO}`/`{POR_CONFIRMAR}` is paired with a concrete verification step.
- Tag spelling (ES vs EN) is consistent throughout the document.

Used by: `skills/revisor-veracidad`, `agents/jarvis-orchestrator`, `skills/jarvis-os`.
