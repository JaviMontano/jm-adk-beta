# Quick Variation — persistent-memory-design

Fast path when the user just needs the scratchpad contract, not a full design report.

## Ask only if missing
- Destination path? (default `.agent/scratchpad.md`, repo-relative)
- One writer or many?

## Emit (≤ 1 screen)
1. **Path** — repo-relative, no `../`.
2. **Schema skeleton** —
   ```markdown
   ## Hypotheses
   ## Decisions
   ## Findings
   ## Open
   ```
3. **Three rules** —
   - Findings/Decisions need `[src:<source> @ <date>]`; unvalidated → Hypotheses/Open.
   - Read once at bootstrap; reference after (no per-turn re-read → keeps the prompt cache).
   - Upsert by key; never full-rewrite.
4. **One survival line** — after `/compact`, reconstruct state from this file alone.

Tag claims `[DOC]/[INFERENCE]`. Refuse raw-transcript dumps and per-turn re-reads. If the real question is which session to resume/fork, route to `session-lifecycle-management`.
