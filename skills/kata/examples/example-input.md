# Example input

> Our customer-support agent sometimes never stops — it keeps calling tools in a
> loop — and other times it halts early as soon as it writes "all done" in its
> reply. We gate the loop by scanning the model's text for phrases like "done" or
> "task complete". How should we fix the loop control? Apply the right kata.

Context provided by the user:

- The loop calls the Messages API each iteration and dispatches tools.
- Halt is currently decided by `any(p in reply_text for p in ["done","task complete","listo"])`.
- There is no iteration cap.
- They want predictable turn control, not heuristics.

Expected routing: `deterministic-agent-loop` (the failure is text-based halt
control + no budget), at `depth=deep`. [INFERENCIA]
