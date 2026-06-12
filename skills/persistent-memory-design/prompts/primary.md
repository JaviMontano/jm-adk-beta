# Primary Prompt — persistent-memory-design

You are designing a **persistent on-disk scratchpad** that serves as an agent's durable memory for a long or multi-session task.

## Inputs to extract from the request
- Session goal and why one context window is not enough.
- A destination path candidate for the file (default `.agent/scratchpad.md` if unspecified).
- The evidence the agent will produce (sources, dates) that must accompany conclusions.
- Whether more than one step/agent will write (concurrency needed?).

## Produce
A design report with these parts, every claim tagged `[DOC] / [CONFIG] / [INFERENCE] / [SUPUESTO]`:

1. **File contract** — stable, repo-relative path; reject any `../` escape.
2. **Fixed schema** — `## Hypotheses / ## Decisions / ## Findings / ## Open`, invariant across sessions.
3. **Entry filter** — only validated conclusions with `[src:<source> @ <date>]` enter Findings/Decisions; unvalidated items go to Hypotheses/Open.
4. **Write discipline** — idempotent upsert by stable key; never full-rewrite (it invalidates the prompt cache).
5. **Read protocol** — read once at bootstrap into cached state; reference after, never re-read per turn.
6. **Survival check** — describe how state reconstructs from the file alone after `/compact` and reset.
7. **Concurrency** — if multiple writers, define upsert order or lock (last upsert-by-key wins, no blind merge).
8. **Acceptance gate** — the validation checklist, each item resolved with evidence; note that the JSON report passes `scripts/check.sh`.

## Refuse / redirect
- Refuse to store raw transcript or per-turn re-reads — explain that both defeat the design.
- Refuse unsafe paths; upgrade to a safe repo-relative path.
- If the request is really about choosing a session to resume/fork/restart, route to `session-lifecycle-management`.

Use the template in `templates/output.md`. Keep it lean; output state, not a log.
