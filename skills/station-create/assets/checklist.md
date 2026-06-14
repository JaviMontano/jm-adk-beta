# Acceptance checklist — station-create

The guardian scores each item against `assets/quality-rubric.json`. All must be
**met (2)** to pass. Green is never assumed — each box needs evidence.

## Identity & placement
- [ ] Target path resolved and the station is placed there. [CONFIG]
- [ ] Slug matches `^[a-z0-9]+(-[a-z0-9]+)*$`. [CONFIG]
- [ ] Empty intent was refused (`{VACIO_CRITICO}`), not auto-named. [DOC]

## Type
- [ ] Type recorded: universal | dedicated. [DOC]
- [ ] Type was confirmed, never defaulted to universal. [INFERENCIA]
- [ ] If dedicated, a single owning sector is bound. [DOC]

## Structure (P06/P23/P24)
- [ ] Structure matches the requirement for the chosen type. [SUPUESTO]
- [ ] Every folder traces to the governing ontology; no invented folders. [SUPUESTO]

## CLAUDE.md (Rule-9)
- [ ] `CLAUDE.md` exists. [DOC]
- [ ] ≤70 lines, achieved by linking out, not inlining. [DOC]

## Upgrade safety
- [ ] Missing-only: no pre-existing file modified without `--force`. [DOC]
- [ ] Partial scaffolds filled only where absent. [DOC]

## Registry
- [ ] `station ↔ slug ↔ type ↔ path` upserted. [INFERENCIA]
- [ ] No duplicate slug or path; re-run is idempotent. [INFERENCIA]

## Governance
- [ ] One Alfa-core tag family per file. [DOC]
- [ ] No prices; single-brand (JM Labs); no client PII. [DOC]
