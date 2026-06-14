# Station Scaffold Summary — {{station-name}}

## Identity

| Field | Value |
|---|---|
| Station name | {{name}} |
| Slug | {{slug}} (matches `^[a-z0-9]+(-[a-z0-9]+)*$`) |
| Type | {{universal \| dedicated}} |
| Bound sector | {{sector \| N/A (universal)}} |
| Target path | {{station-path}} |
| One-line purpose | {{purpose \| {POR_CONFIRMAR}}} |

## Files (missing-only)

| Path | Status | Note |
|---|---|---|
| {{station-path}}/CLAUDE.md | created \| pre-existing-untouched | ≤70 lines (Rule-9) |
| {{p06/p23/p24 structure file}} | created \| pre-existing-untouched | per {{type}} |
| ... | ... | ... |

> No pre-existing file modified without `--force` + reviewed diff. [DOC]

## P06/P23/P24 structure trace

| Folder/file | Protocol | Traced to ontology? |
|---|---|---|
| {{folder}} | {{P06 \| P23 \| P24}} | yes \| {POR_CONFIRMAR} |

## Registry

- Entry: `station ↔ slug ↔ type ↔ path` → {{upserted \| already-matched}}
- Duplicate slug/path check: {{pass}}

## Acceptance gate

- [ ] Path correct; slug matches regex
- [ ] Type recorded; dedicated has bound sector
- [ ] Structure matches P06/P23/P24 for type
- [ ] CLAUDE.md exists, ≤70 lines
- [ ] No file clobbered without --force
- [ ] Registry binding clean, no duplicates
- [ ] One Alfa-core tag family used consistently

**Gate verdict:** {{pass \| fail}}

## Next step

Invoke {{next cadence/skill}} — e.g. route back to `jarvis-os` for the station's
first cadence. station-create does not operate the surface. [DOC]

---
*Evidence: one Alfa-core family per file. No prices, single-brand (JM Labs).*
