# Example Input — Auth Validation in a Monorepo

## Request

> Where is the auth token actually validated in our backend monorepo? It's ~4000 files and I can't read it all. Give me the exact node that verifies the token, and don't burn more than 8 file reads doing it.

## Parsed contract

| Field | Value | Tag |
|---|---|---|
| `goal` | "Locate the node that verifies the auth token (signature + expiry)." | [DOC] |
| `budget` | 8 expensive reads (hard). | [DOC] |
| `surface_root` | repo root (`**`). | [CONFIG] |
| `cheap_tools` | `Glob`, `Grep -l`. | [CONFIG] |

## Notes

- `goal` is concrete ("verify the token"), not "understand auth". [DOC]
- Budget is supplied, so no `{VACIO_CRITICO}`. [DOC]
- Domain is far larger than one context window → the method applies (not a small-domain false positive). [INFERENCIA]
- Expected shape: cheap map → ranked hypotheses → 2 deep-dives following a delegation chain → resolve well under budget. [INFERENCIA]
