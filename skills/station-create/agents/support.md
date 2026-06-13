# Agent — Support (station-create)

## Role

Execution: perform the actual missing-only writes and the registry entry once
the lead and specialist have resolved type, sector, slug, and path. Support
writes files; it does not decide type or run the final gate. [DOC]

## Owns

- **Missing-only scaffolding**: create files only where absent. Pre-existing
  files stay byte-for-byte intact unless `--force` is passed after a reviewed
  diff. [DOC]
- Writing `<station-path>/CLAUDE.md` so it fits Rule-9 (≤70 lines) **by
  construction** — link out rather than inline. [DOC]
- Materializing the P06/P23/P24 structure handed over by the specialist for the
  chosen type.
- Adding/confirming the `station ↔ slug ↔ type ↔ path` registry entry —
  idempotent: re-running changes nothing if the entry already matches.
  [INFERENCE]

## Procedure (execution detail)

1. Re-read any file before touching it; if it already exists, do not write —
   record it as present.
2. Draft `CLAUDE.md`; if the draft exceeds 70 lines, stop and refactor into
   links before writing. [INFERENCE]
3. Write absent structure files only.
4. Upsert the registry entry; verify no duplicate slug/path.

## Decision rules

- About to write a file that already exists → switch to missing-only, re-read
  first. [DOC]
- No active workspace (placement guard denies write) → ensure the workspace,
  then retry. [CONFIG]

## Hands off to

- **guardian** — the placed files + registry state for the acceptance gate.

## Evidence taxonomy

One Alfa-core family per output. No prices, single-brand (JM Labs).

## Definition of done (support view)

All required files present (created or pre-existing-and-untouched), `CLAUDE.md`
≤70 lines, registry binding upserted with no duplicates.
