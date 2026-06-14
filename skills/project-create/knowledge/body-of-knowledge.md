# Body of knowledge — project-create

Domain knowledge for scaffolding Jarvis OS projects under `02_Proyectos/`.

## 1 · The three governance files

Every Jarvis OS project carries exactly three files, each with a distinct role: [DOC]

- **`CLAUDE.md`** — project memory and router. Hard-capped at **70 lines**
  (Rule-9). It points to detail; it does not contain it. [DOC]
- **`MEMORY.md`** — persistent context: one-line objective, stakeholders,
  decisions, open questions. Unknown objective is recorded as `{POR_CONFIRMAR}`. [DOC]
- **`TAREAS.md`** — task ledger. The active band **NOW must hold ≤ 3 tasks**;
  everything else lives in NEXT/LATER. [DOC]

## 2 · Slug naming policy

- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab-case). [CONFIG]
- Derivation: lowercase, strip accents/diacritics, drop punctuation, collapse
  whitespace runs to a single hyphen, trim leading/trailing hyphens. [INFERENCE]
- Example: `"Atlas — Fase II"` → `atlas-fase-ii`. [INFERENCE]

## 3 · Id allocation (P-NNN)

- Ids are zero-padded (`P-001`, `P-014`, …). [CONFIG]
- Allocate the **next free** id from the registry; on collision, advance and
  report the substitution. Never silently reuse a retired id. [INFERENCE]

## 4 · Registry invariant

The registry binds `P-NNN ↔ slug ↔ path` as a **unique triple**: [INFERENCE]

- No two entries share a `P-NNN`. [INFERENCE]
- No two entries share a `slug`. [INFERENCE]
- Re-running an already-registered project is **idempotent** — a matching entry
  changes nothing. [INFERENCE]

## 5 · Rule-9 (CLAUDE.md ≤ 70 lines)

Rule-9 keeps project memory cheap to load. Construct the file to fit by
linking out, not by trimming after the fact. If a draft exceeds 70 lines,
factor content into `MEMORY.md` or external links **before** writing. [DOC]

## 6 · Missing-only / upgrade-safety

The default mode is **missing-only**: write a file only if absent; leave any
present file byte-for-byte intact. Overwrites require `--force` **after** a
reviewed diff. This is the core safety contract — it protects local edits
across re-runs and upgrades. [DOC]

## 7 · Placement & sectors

- Projects live under `02_Proyectos/`. Default sector is `III Core`
  (`[ASSUMPTION]`) — confirm if the name implies another sector. [ASSUMPTION]
- Writes are subject to the placement guard; if no active workspace, run
  `workspace-manager.sh ensure` and retry. [CONFIG]

## 8 · Evidence taxonomy (Alfa core)

Tag non-obvious claims with exactly one family, never mixing families in a file: [DOC]

| Tag | Meaning |
|---|---|
| `[CODE]` | Asserted by source/script behavior |
| `[CONFIG]` | Stated in configuration / policy |
| `[DOC]` | Stated in documentation / convention |
| `[INFERENCE]` | Derived by reasoning from evidence |
| `[ASSUMPTION]` | Default taken absent confirmation |

## 9 · Decision rules summary

| Situation | Action |
|---|---|
| Empty intent | `{VACIO_CRITICO}` stop, ask objective [DOC] |
| Folder exists | STOP, route to cadence, never re-scaffold [DOC] |
| Slug collision | Surface both, ask reuse/rename [INFERENCE] |
| Id collision | Next free id, report substitution [INFERENCE] |
| Partial scaffold (1–2 files) | Fill only missing ones [DOC] |
| CLAUDE.md > 70 lines | Refactor before writing [INFERENCE] |
