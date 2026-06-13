# Quick variation — station-create

Fast path for when type, sector (if any), and name are already unambiguous.

## Use when

- The intent clearly names the station and its type.
- No collision suspected; this is a fresh surface.

## Compressed flow

1. Slug = kebab-case of name (`^[a-z0-9]+(-[a-z0-9]+)*$`).
2. Confirm type in one line: universal (no binding) | dedicated (+sector).
3. Guard: assert target path does not exist — if it does, **abort to cadence**.
4. Scaffold missing-only: folder, `CLAUDE.md` (≤70 lines), P06/P23/P24 structure.
5. Upsert registry `station ↔ slug ↔ type ↔ path`.
6. Emit the summary + next cadence/skill.

## Still non-negotiable

- Never guess the type — if unstated, fall back to the full flow and ask
  (`{POR_CONFIRMAR}`).
- Never overwrite an existing file without `--force` + reviewed diff.
- One Alfa-core tag family. No prices, single-brand (JM Labs).

## Output

One-screen `templates/output.md`: slug, type, path, created vs pre-existing,
registry status, gate pass/fail, next step.
