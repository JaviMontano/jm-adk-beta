# Persistent Memory Design — <session/task name>

> Every claim tagged `[DOC] / [CONFIG] / [INFERENCE] / [SUPUESTO]`. State, not a log.

## 1. Context
- **Goal:** <why the task exceeds one context window>
- **Sessions:** <single long / multi-session>
- **Writers:** <one / many → concurrency needed?>

## 2. File contract
- **Path:** `.agent/scratchpad.md`  <!-- repo-relative; reject ../ escapes -->  [DOC]
- **Format:** Markdown, plain (legible, clean git diff, no fragile parser) [INFERENCE]
- **Bootstrap when absent:** create the section skeleton, treat as empty state, never error [INFERENCE]

## 3. Fixed schema (invariant)
```markdown
## Hypotheses
## Decisions
## Findings
## Open
```
Sections never change across sessions; only content evolves. [DOC]

## 4. Entry filter (what may enter)
| Section | Admits | Evidence |
|---|---|---|
| Hypotheses | unvalidated candidate claims | no |
| Decisions | choices + rationale; contradiction ledger | `[src:… @ …]` |
| Findings | validated conclusions | `[src:… @ …]` |
| Open | unresolved questions | no |

Reject: raw reasoning, tool dumps, entries without provenance. [DOC]

## 5. Read protocol
- Read **once** at bootstrap → cached parsed state; reference after, no per-turn re-read (preserves prompt cache). [DOC]

## 6. Write discipline
- Upsert by **stable key**; never full-rewrite (a rewrite invalidates the cache prefix). [INFERENCE]
- Contradicted finding → replace by key + note in Decisions. [INFERENCE]

## 7. Survival check
- After `/compact` and reset, reconstruct state **from the file alone**; assert equality with pre-compact state. [DOC]
- Result: ☐ pass / ☐ fail (+ evidence)

## 8. Concurrency
- Policy: <last upsert-by-key wins | simple lock>; no blind text merge. [INFERENCE]

## 9. Bounded growth
- Prune resolved Open; collapse stale Findings by key. [INFERENCE]

## 10. Acceptance gate (all must hold, with evidence)
- ☐ Only validated conclusions
- ☐ Fixed four-section schema
- ☐ Read-once / reference-after
- ☐ Idempotent upsert, no full rewrite
- ☐ Survives `/compact` + reset
- ☐ Every Finding/Decision has `[src:… @ …]`
- ☐ Concurrency resolved (if multi-writer)
- ☐ JSON report passes `scripts/check.sh` [CONFIG]

---
Single brand (JM Labs); no invented prices; no client PII.
