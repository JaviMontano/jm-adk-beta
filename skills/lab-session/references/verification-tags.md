# Verification Tags — Alfa core (canon for lab-session)

The evidence taxonomy used across every lab-session file. One tag per claim,
one spelling throughout a session.

## The five tags

| Tag | Use for |
|---|---|
| `[CODE]` | A fact established by code or a filesystem operation actually run. |
| `[CONFIG]` | A fact from a config value, flag, or declared setting (e.g. ISO dates, offline mode). |
| `[DOC]` | A documented fact: protocol P08, prior internal docs, stated source. |
| `[INFERENCE]` | A reasoned read not directly stated — labeled so it can be challenged. |
| `[ASSUMPTION]` | A working assumption pending confirmation (e.g. default Lab root, metric choice). |

## Homologation rules

- **One family, one spelling.** Do not mix `[INFERENCE]` and `[INFERENCIA]`, or
  `[CODE]` and `[CODIGO]`, within a session. lab-session uses the EN core set.
- **One tag per claim.** If a sentence carries two evidence kinds, split it.
- **Mandatory on references.** Every `referencias.md` entry MUST carry exactly
  one tag. Non-obvious `notas.md` lines carry one too.
- **No tag on stubs.** `{POR_CONFIRMAR}` and `{HIPOTESIS_POR_DEFINIR}` are
  placeholders, not claims — they take no tag.

## Why EN core here

lab-session is kit-facing JM Labs scratch tooling; the EN core set keeps the
scaffold consistent with the skill's agents, prompts, and validation gate. The
guardian's tag-hygiene check (`assets/quality-rubric.json`) enforces this.
