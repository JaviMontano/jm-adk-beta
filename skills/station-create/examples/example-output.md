# Example output — station-create

Worked result for the `knowledge-ops` universal station from
`example-input.md`.

## Station Scaffold Summary — Knowledge Ops

### Identity

| Field | Value |
|---|---|
| Station name | Knowledge Ops |
| Slug | `knowledge-ops` (matches `^[a-z0-9]+(-[a-z0-9]+)*$`) |
| Type | universal |
| Bound sector | N/A (universal) |
| Target path | `stations/knowledge-ops/` |
| One-line purpose | Shared research, notes, and synthesis surface. |

### Files (missing-only)

| Path | Status | Note |
|---|---|---|
| `stations/knowledge-ops/CLAUDE.md` | created | 38 lines, ≤70 (Rule-9) [DOC] |
| `stations/knowledge-ops/` (folder) | created | universal placement [SUPUESTO] |
| `stations/knowledge-ops/` P06/P23/P24 structure | created | universal variant [SUPUESTO] |

> No pre-existing file modified; `--force` not needed. [DOC]

### P06/P23/P24 structure trace

| Folder/file | Protocol | Traced to ontology? |
|---|---|---|
| memory contract (CLAUDE.md) | P06 | yes [DOC] |
| cadence anchor | P23 | yes [SUPUESTO] |
| reporting anchor | P24 | yes [SUPUESTO] |

### Registry

- Entry `Knowledge Ops ↔ knowledge-ops ↔ universal ↔ stations/knowledge-ops/`
  → upserted [INFERENCE]
- Duplicate slug/path check: pass

### Acceptance gate

- [x] Path correct; slug matches regex
- [x] Type recorded (universal); no sector required
- [x] Structure matches P06/P23/P24 for universal
- [x] CLAUDE.md exists, 38 lines (≤70)
- [x] No file clobbered without --force
- [x] Registry binding clean, no duplicates
- [x] One Alfa-core tag family used consistently

**Gate verdict:** pass

### Next step

Route back to `jarvis-os` to seed the station's first research/synthesis
cadence. station-create stops at placement. [DOC]

---
*Evidence: Alfa-core family only. No prices, single-brand (JM Labs).*
