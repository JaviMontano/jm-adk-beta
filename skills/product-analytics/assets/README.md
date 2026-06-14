# Assets — product-analytics

Reusable, deterministic artifacts that the router and its agents consume. These
are the contract surface: same input → same gate result. [CONFIG]

## Bundle
- **quality-rubric.json** — the scored gate the **guardian** (`agents/guardian.md`)
  applies before any deliverable ships. Each criterion declares whether it is
  required and which route(s) it applies to (`all` or a specific topic).
- **routing-checklist.md** — the one-in/one-out routing guard the **lead**
  (`agents/lead.md`) runs to resolve a single `topic`, apply tie-breakers, and
  enforce the contract guards. Referenced from `SKILL.md`.

## How they're used
1. `SKILL.md` points readers here for the routing checklist.
2. The lead resolves the topic against `routing-checklist.md` before reading a playbook.
3. Support assembles the deliverable via `templates/output.md`.
4. The guardian scores it against `quality-rubric.json`; any required criterion
   false → `block` with the failing criterion named.

## Conventions
- JSON assets are the machine-checkable oracle; Markdown assets are the
  human-readable checklist. Keep them in sync when routes change.
- No invented numbers, no client PII, single-brand. Evidence tags everywhere.
