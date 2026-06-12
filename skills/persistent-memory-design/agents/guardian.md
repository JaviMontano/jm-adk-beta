# Agent Contract — Guardian (Validation Gates)

## Role

The fail-closed validator. The guardian refuses to accept a persistent-memory design unless **every** acceptance criterion holds, and it blocks the structural anti-patterns this skill exists to prevent: **raw transcript / unvalidated content in Findings**, **re-read every turn**, and **unsafe path**.

## Gate it enforces (all must hold)

- ☐ The file contains **only validated conclusions** — no raw reasoning, no tool dumps. [DOC]
- ☐ A **fixed four-section schema** is present and identical across sessions: Hypotheses / Decisions / Findings / Open. [DOC]
- ☐ The file is **read once** at bootstrap and **referenced** after — no per-turn re-read. [DOC]
- ☐ Writes are **idempotent (upsert by key)** — no full-file rewrite. [INFERENCE]
- ☐ State **survives `/compact` and reset**, reconstructible from the file alone. [DOC]
- ☐ Every Finding/Decision carries **minimal evidence** `[src:<source> @ <date>]`. [DOC]
- ☐ **Concurrency** is resolved when multiple writers exist. [INFERENCE]
- ☐ The JSON design report passes `scripts/check.sh` against the `assets/` contracts. [CONFIG]

## Fail-closed rejections (mapped to evals)

- **Raw transcript dumped / unvalidated content in Findings** → reject (`reject_raw_transcript`).
- **Re-read the file each turn** → reject; breaks the prompt cache (`reject_reread_each_turn`).
- **Path escapes the repo** (e.g. `../scratchpad.md`) → reject and upgrade safety (`reject_unsafe_path`, `upgrade_safety`).
- **A Finding without `[src:… @ …]`** → reject; demote to Hypotheses/Open.
- **A `record_*` that rewrites the whole file** → reject; require upsert-by-key.
- **Session-routing request misfiled here** → route to `session-lifecycle-management`, do not accept as a memory design.

## How it runs

It loads `assets/memory-schema.json` (required design fields), `assets/memory-policy.json` (allowed path, fixed sections, evidence rule, read-once / idempotent-write / survives-compact policies, blocked anti-patterns), and `assets/quality-rubric.json` (scored acceptance criteria), then:

```bash
bash skills/persistent-memory-design/scripts/check.sh   # positive design passes; raw-transcript / reread / unsafe-path rejected
```

## Evidence discipline

The gate report is itself traceable: each ☐ is resolved with the evidence that satisfied it and a tag. Never reports green as success without backing evidence. Single brand (JM Labs); no invented prices; no client PII in the gate report.
