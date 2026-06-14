# Pre-delivery Checklist — Persistent Memory Design

Human-facing mirror of the acceptance gate. Resolve each ☐ with evidence and a tag before delivery.

## File contract
- ☐ Path is stable and **repo-relative** (no `../`, no absolute home path). [INFERENCE]
- ☐ Absent-file bootstrap creates the section skeleton instead of erroring. [INFERENCE]

## Schema
- ☐ Exactly four sections: `## Hypotheses / ## Decisions / ## Findings / ## Open`. [DOC]
- ☐ Schema is identical to prior sessions (no drift that breaks the parser). [DOC]

## Entry filter
- ☐ Findings/Decisions contain **only validated conclusions**. [DOC]
- ☐ No raw transcript, no unconfirmed tool output. [DOC]
- ☐ Every Finding/Decision carries `[src:<source> @ <date>]`. [DOC]

## Read protocol
- ☐ File is read **once** at bootstrap and **referenced** afterward. [DOC]
- ☐ No per-turn re-read (would break the prompt cache). [INFERENCE]

## Write discipline
- ☐ Writes are **upsert-by-key**; no full-file rewrite. [INFERENCE]
- ☐ Contradicted finding replaced by key + logged in Decisions (no duplicate versions). [INFERENCE]
- ☐ Concurrency resolved if multiple writers. [INFERENCE]

## Survival & growth
- ☐ State reconstructs from the file alone after `/compact` and reset. [DOC]
- ☐ Resolved Open pruned; stale Findings collapsed (file is state, not a log). [INFERENCE]

## Deterministic gate
- ☐ JSON design report passes `bash scripts/check.sh` against `assets/` contracts. [CONFIG]

---
Single brand (JM Labs); no invented prices; no client PII.
