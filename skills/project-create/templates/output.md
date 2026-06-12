# Scaffold summary — <Project name>

## Identity

- **P-NNN**: `P-___`
- **Slug**: `<slug>` (matches `^[a-z0-9]+(-[a-z0-9]+)*$`)
- **Path**: `02_Proyectos/<slug>/`
- **Sector**: `III Core` <!-- [ASSUMPTION] unless confirmed otherwise -->
- **Objective**: `<one line>` or `{POR_CONFIRMAR}`

## Files (missing-only)

| File | Action | Notes |
|---|---|---|
| `CLAUDE.md` | written / skipped (present) | lines: __ / 70 (Rule-9) |
| `MEMORY.md` | written / skipped (present) | objective recorded |
| `TAREAS.md` | written / skipped (present) | NOW count: __ / 3 |

## Registry

- Entry: `P-___ ↔ <slug> ↔ 02_Proyectos/<slug>/`
- Status: added / confirmed (idempotent) / collision

## Collisions & substitutions

- Slug collision: none / `<detail>`
- Id collision: none / substituted `P-___` → `P-___`

## Acceptance gate

| Check | Verdict |
|---|---|
| Folder placed, slug regex matches | pass / fail |
| Three files exist; none clobbered without `--force` | pass / fail |
| `CLAUDE.md` ≤ 70 lines | pass / fail |
| `TAREAS.md` NOW ≤ 3 | pass / fail |
| Registry triple unique (no dup id/slug) | pass / fail |
| One Alfa-core tag family used consistently | pass / fail |

**Overall**: PASS / BLOCKED (reason: ____)

## Next step

- Next cadence to invoke: `<skill/cadence>` <!-- e.g. project planning -->

---
Evidence tags: `[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`.
Single-brand (JM Labs). No prices. Missing-only; `--force` only after reviewed diff.
