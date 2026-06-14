# Body of Knowledge — station-create

Domain knowledge for scaffolding Jarvis OS stations. Scope is **placement
only**: standing up the surface, not operating it.

## 1. Station vs project vs sector

- **Station** — a long-lived **operating surface**. It persists, accrues state,
  and runs cadences over time. [DOC]
- **Project** — a bounded effort with a start and an end; use `project-create`.
- **Sector** — a domain grouping; a dedicated station binds *to* a sector but is
  not itself one.

Choosing the wrong abstraction picks the wrong scaffolder and the wrong
lifecycle. A one-off task inside an existing surface is neither — it goes to the
task scaffolder. [DOC]

## 2. The type model: universal vs dedicated

The first real decision the skill makes, and it is never guessed. [INFERENCE]

| Type | Binding | Placement | Scope |
|---|---|---|---|
| **Universal** | none | shared | cross-cutting capability shared across sectors |
| **Dedicated** | exactly one sector | under/with that sector | single-sector/domain |

Decision rule: if the request names or implies a single owning sector, it is
**dedicated** and that sector must be bound; otherwise confirm whether the
surface is genuinely shared before treating it as **universal**. Unstated type →
`{POR_CONFIRMAR}`, ask. Dedicated without a sector → stop, ask. [DOC]

## 3. Governing protocols: P06 / P23 / P24

The materialized structure must satisfy the P06/P23/P24 requirements for the
chosen type. Universal and dedicated stations differ in scope and binding, so
they differ in the structure produced. [SUPUESTO]

**Rule**: structure must be **traceable** to the governing ontology. If the
P06/P23/P24 semantics for a folder cannot be traced, mark it `{POR_CONFIRMAR}`
and confirm — never invent structure to fill a gap. [SUPUESTO]

## 4. Rule-9 — CLAUDE.md ≤ 70 lines

Every station gets its own `CLAUDE.md` as its memory contract, capped at **70
lines**. The cap is honored **by construction**: when a draft would exceed it,
factor content into linked files *before* writing, not after. Inlining cadence
or report content to "save a file" is an anti-pattern that breaks Rule-9. [DOC]

## 5. Missing-only / upgrade safety

Default write mode is **missing-only**: create files where absent, leave
existing files byte-for-byte intact. `--force` overwrites only after a reviewed
diff. This makes re-runs and upgrades safe — a partial scaffold is completed,
never clobbered. Local edits and `.local` overrides survive. [DOC]

## 6. Slug & naming policy

Slug derivation is kebab-case and must match
`^[a-z0-9]+(-[a-z0-9]+)*$`. Empty intent is `{VACIO_CRITICO}` — stop and ask;
never auto-name. Slug/path collisions stop the flow and surface the existing
station for reuse-vs-rename. [CONFIG]

## 7. Registry binding

The skill maintains a `station ↔ slug ↔ type ↔ path` mapping. It is
**idempotent**: re-running with a matching entry changes nothing, and duplicate
slugs or paths are rejected. [INFERENCE]

## 8. Decision rules (quick reference)

1. Path exists → stop, route to cadence, never re-scaffold.
2. Type unstated → `{POR_CONFIRMAR}`, ask.
3. Dedicated, no sector → stop, ask.
4. CLAUDE.md > 70 lines → refactor into links first.
5. Structure not traceable to P06/P23/P24 → `{POR_CONFIRMAR}`, do not invent.
6. File exists → missing-only, re-read before any write.

## 9. Evidence taxonomy

One Alfa-core family per file:
`[CÓDIGO]` (code/scripts), `[CONFIG]` (config/policy),
`[DOC]` (documented), `[INFERENCIA]` (reasoned), `[SUPUESTO]` (assumption).
Never mix families in one file. No prices, single-brand (JM Labs), no client
PII. See `references/verification-tags.md` if present. [DOC]
