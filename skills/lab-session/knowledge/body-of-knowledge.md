# Body of Knowledge — lab-session (Protocol P08)

Domain knowledge for scaffolding a single JM Labs Lab session. This is internal
JM Labs scratch work — never a client deliverable. [DOC]

## 1. Protocol P08 — the four-file Lab contract

A Lab session is a thin, structured home for an idea under test. P08 fixes
**exactly four** files per session folder `<lab-root>/<slug>/`:

| File | Purpose | Starting state |
|---|---|---|
| `notas.md` | Running log: dated observations, open questions | Skeleton with a first dated entry stub |
| `hipotesis.md` | The claim under test, framed falsifiably | The claim, or an explicit `{HIPOTESIS_POR_DEFINIR}` stub |
| `referencias.md` | Sources, links, prior art; one tag per entry | Empty tagged skeleton |
| `decision.md` | Verdict (keep / pivot / kill) at Lab close | `{POR_CONFIRMAR}` — human-written later |

More or fewer than four files means the P08 contract is broken. [DOC]

## 2. Key concepts

- **Session = folder, not file.** One run materializes one `<slug>/` folder. [DOC]
- **Missing-only writes.** Every file is created only if absent. Reruns are
  additive and complete partial scaffolds; they never overwrite. [DOC]
- **Falsifiability.** `hipotesis.md` must state what outcome would refute the
  claim. A claim that cannot fail is reframed or stubbed. [INFERENCE]
- **Verdict is a human act.** The skill scaffolds `decision.md` but never writes
  keep/pivot/kill; that judgment belongs to the human at Lab close. [INFERENCE]
- **Slug derivation.** When unsupplied, the slug is kebab-cased from the topic;
  slug collisions with a different topic must be surfaced, not silently reused. [INFERENCE]

## 3. Standards

- **Evidence tags (Alfa core, EN):** `[CODE]` / `[CONFIG]` / `[DOC]` /
  `[INFERENCE]` / `[ASSUMPTION]`. One tag per claim, one spelling throughout.
  Canon: `references/verification-tags.md`. [DOC]
- **Determinism:** ISO dates (`YYYY-MM-DD`); offline; identical inputs produce
  identical CREATE bytes. [CONFIG]
- **Decision vocabulary (closed set):** keep / pivot / kill. [DOC]
- **Brand:** single-brand JM Labs. No MetodologIA or MetodologIA framing. [DOC]
- **Signal hygiene:** never use green as a success signal in sample content. [DOC]

## 4. Decision rules

1. Empty objective → STOP and ask; never auto-fill a topic. [INFERENCE]
2. Path present → classify SKIP; only `--force` (after diff review) may
   regenerate it. [DOC]
3. Hypothesis present but unfalsifiable → reframe before write. [INFERENCE]
4. Reference entry without a tag → block until tagged. [DOC]
5. Non-writable target → stop with the path error; no surprise fallback path. [ASSUMPTION]
6. Folder fully scaffolded → report "already scaffolded", change nothing. [INFERENCE]

## 5. Flow spine

Discover (probe slug/path/files) → Plan (CREATE vs SKIP per path) →
Execute (Write CREATE only) → Validate (re-list, confirm four files,
emit created/skipped summary). [DOC]

## 6. Where it sits

- Upstream: a loose idea or hypothesis that needs structure before it is a
  project.
- Downstream: a kept Lab is promoted into a real workflow (`workflow-forge`);
  its place in the workspace tree is governed by `workspace-governance`. [INFERENCE]
