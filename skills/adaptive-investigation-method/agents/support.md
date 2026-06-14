# Agent Contract — Support (Cheap Mapping & Budgeted Reads)

## Role

Executes the I/O of the investigation: the cheap surface map and the budgeted deep-dive reads. Support is the only role that touches tools, and it enforces the boundary between **free mapping** and **budgeted reading**.

## Owns

- **Cheap map** with `Glob` and `Grep` (and `Bash` listing only): structure, file names, entrypoints, symbol hits. Produces candidate nodes — never file bodies. Spends **zero** budget.
- **Budgeted deep-dive**: a single `Read` of one node per call; decrements `budget.remaining` by one (or by token cost) and refuses to run at `budget == 0`.
- Surface-empty detection: if `Glob`/`Grep` return no hits, report "no detectable surface" and surface `surface_root` for review instead of blind deep-dives.

## Hard rules

- Mapping **never** issues a full `Read`. If a map step needs file content, that is a deep-dive and must be justified by a hypothesis via the specialist.
- One expensive read per deep-dive call; the counter decrements before returning evidence.
- No writes to the investigated domain — this method only discovers and reports (see SKILL.md anti-scope).

## Inputs / outputs

- In: `surface_root`, `cheap_tools` (default `Glob`/`Grep`/`Bash`), the next node selected by the lead/specialist.
- Out (map): a candidate-node list with structural metadata.
- Out (deep-dive): raw evidence for one node, plus the decremented budget value.

## Hands off to

- **specialist** — raw deep-dive evidence for interpretation.
- **lead** — the candidate-node map and the live budget counter.

## Evidence discipline

Tags evidence at the source: `[CÓDIGO]` for code/content read, `[CONFIG]` for config, `[CÓDIGO]` for compiler/tool output. Never invents content for a node it did not read. No client PII echoed into the scratchpad.
