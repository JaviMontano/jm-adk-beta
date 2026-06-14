# persistent-memory-design

## What it does

Designs a **persistent on-disk scratchpad** that acts as an agent's durable memory: a fixed-schema Markdown file (`## Hypotheses` / `## Decisions` / `## Findings` / `## Open`) holding **only validated conclusions** with minimal evidence (source + date). The file survives `/compact` and full session resets, is **read once** at session bootstrap, and thereafter is **referenced** — never re-read per turn — so it does not break the prompt cache. This is context engineering: it separates volatile working memory (the conversation) from audited persistent memory (the file). [DOC]

## When to use it

- A long investigation or task that exceeds one context window and must survive compaction. [DOC]
- Multi-session work that must resume tomorrow without re-deriving everything. [DOC]
- The agent repeats work because it "forgets" already-validated conclusions. [INFERENCE]
- An existing scratchpad is re-read every turn and breaks the prompt cache. [INFERENCE]

Do **not** use it for single-turn ephemeral notes, raw transcript dumps, or a high-churn mutable task queue (that belongs in a task store, not audited memory). [INFERENCE]

## How it routes / executes

1. **Define the file contract** — stable, repo-relative path (e.g. `.agent/scratchpad.md`) and the invariant four-section schema.
2. **Filter what enters** — only validated conclusions with `[src:… @ …]`; unconfirmed items go to `## Hypotheses` / `## Open`, never `## Findings` / `## Decisions`.
3. **Write idempotently** — upsert by stable key; never full-rewrite (a total rewrite invalidates the prompt cache of everything before it).
4. **Read once, reference after** — parse the file into cached state at bootstrap; later turns reference sections.
5. **Verify survival** — confirm state reconstructs from the file alone after `/compact` and reset.
6. **Resolve concurrency** — last upsert-by-key wins; no blind text merges.

Adjacent requests that are really *which* session to resume, fork, or restart route to `session-lifecycle-management`; this skill owns the **memory artifact**, not the session-routing decision. [CONFIG]

## Deterministic backbone

The design is validated against offline contracts in `assets/` (allowed path, fixed sections, minimal evidence, read-once policy, idempotent-write policy, survives-compact reconstruction) indexed by `assets/manifest.json`. A produced JSON design report is checked with `scripts/check.sh` before acceptance. [CONFIG]

## References

- `SKILL.md` — capability, build steps, correct/anti-patterns, acceptance gate.
- `knowledge/body-of-knowledge.md` — concepts, standards, decision rules.
- `knowledge/knowledge-graph.json` — concept graph.
- `agents/` — lead, specialist, support, guardian role contracts.
- `prompts/` — primary, meta, quick, deep.
- `templates/output.md` — design-report deliverable scaffold.
- `examples/` — worked input + output.
- `assets/` — offline contracts and quality rubric (see `assets/README.md`).

## Evidence convention

Every claim carries a tag: `[DOC]` (documented in this skill), `[CONFIG]` (from an asset/contract), `[INFERENCE]` (derived), `[SUPUESTO]` (assumption). Single brand (JM Labs); no invented prices; no client PII; never report green as success without backing evidence.
