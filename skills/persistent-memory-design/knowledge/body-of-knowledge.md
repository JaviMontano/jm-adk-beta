# Body of Knowledge — Persistent Memory Design

## 1. Core concepts

- **Persistent scratchpad** — a fixed-schema Markdown file on disk that is the agent's durable memory. It holds *state*, not a log. [DOC]
- **Volatile vs persistent memory** — the conversation is working memory (lost at `/compact`/reset); the file is audited persistent memory (survives). The skill's whole job is the boundary between them. [DOC]
- **Validated conclusion** — a claim confirmed with minimal evidence (`source` + `date`). Only these enter Findings/Decisions. [DOC]
- **Provenance tag** — `[src:<source> @ <date>]` appended to every Finding/Decision. No tag → not a finding. [DOC]
- **Read-once / reference-after** — the file is parsed into cached state once at bootstrap; later turns reference that state instead of re-reading. [DOC]
- **Idempotent write (upsert by key)** — each entry has a stable key; writing replaces that entry, never the whole file. [INFERENCE]
- **Survives-compact invariant** — after `/compact` or reset, state reconstructs from the file alone. [DOC]

## 2. The fixed schema (invariant)

| Section | Holds | Evidence required |
|---|---|---|
| `## Hypotheses` | candidate claims, explicitly **not** validated | no |
| `## Decisions` | choices made + rationale; records contradictions | yes |
| `## Findings` | validated conclusions | yes (`[src:… @ …]`) |
| `## Open` | unresolved questions / pending threads | no |

The set of sections never changes between sessions; only the content evolves. A variable schema breaks the bootstrap parser. [DOC]

## 3. Standards & decision rules

- **R1 — Entry filter.** An entry without `[src:… @ …]` may not enter Findings/Decisions; it drops to Hypotheses/Open. [DOC]
- **R2 — Read-once.** Reading the scratchpad more than once per session means state is not being cached → fix bootstrap. [INFERENCE]
- **R3 — No full rewrite.** A `record_*` that rewrites the whole file invalidates the prompt cache → switch to upsert-by-key. [INFERENCE]
- **R4 — Contradiction handling.** A contradicted finding is **replaced** by its key, and the change is logged in Decisions — never keep both versions. [INFERENCE]
- **R5 — Path safety.** The path is stable and repo-relative; reject `../` escapes that leak memory across repos. [INFERENCE]
- **R6 — Absent file.** Missing file at bootstrap is empty state, not an error: create the section skeleton. [INFERENCE]
- **R7 — Corruption.** An unparseable file fails loud and stops; never blind-overwrite. [SUPUESTO]
- **R8 — Bounded growth.** Prune resolved Open and collapse stale Findings by key; the file is state, not a log. [INFERENCE]
- **R9 — Concurrency.** With multiple writers, last upsert-by-key wins or use a simple lock; no blind text merge. [INFERENCE]

## 4. Trade-offs

- **Markdown over JSON/DB** — human- and agent-legible, clean git diffs, no fragile parser; pays with weaker schema validation, compensated by the `assets/` checker. [INFERENCE]
- **Upsert-by-key over append-only** — append grows without bound and duplicates corrected findings; upsert keeps one truth per entry at the cost of a stable key per finding. [INFERENCE]
- **Read-once over re-read** — re-read guarantees freshness but breaks the cache and reintroduces noise; read-once assumes all mutation flows through the agent's own write layer. [SUPUESTO]

## 5. Boundary (what this is NOT)

Not for ephemeral single-turn notes, raw transcript storage, or a high-churn mutable task queue (use a task store). Deciding *which* session to resume/fork/restart is `session-lifecycle-management`, not this skill. [DOC]

## 6. Evidence taxonomy

`[DOC]` documented in this skill · `[CONFIG]` from an asset/contract · `[INFERENCE]` derived · `[SUPUESTO]` assumption. Single brand (JM Labs); no invented prices; no client PII.
