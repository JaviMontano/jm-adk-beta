# Meta Prompt — claude-md-architecture

Use this to decide whether and how to invoke claude-md-architecture, and to
self-correct mid-flight.

## Activate when
- Root `CLAUDE.md` exceeded ~300 lines and now carries module-only rules.
- Rules should be scoped to `frontend/**`, `infra/**`, or `tests/**` but live in one
  global file.
- Personal preferences are leaking into the versioned team repo.
- Explicit trigger: `claude md architecture`, `hierarchical memory`,
  `path scoped rules`, `memory imports`.

## Do NOT activate when
- The repo is a single module with no divergent subtrees (hierarchy = over-engineering).
- The real problem is rule *content*, not *location*.
- The request asks to dump every rule into one root file and ignore precedence/validation
  (conflicting with the skill's own contract) — decline and explain.
- The request is unrelated to Claude Code memory architecture.

## Self-correction triggers (stop and reclassify)
- A rule appears in both root and module → dedupe to the correct level.
- Root regrows >300 lines → a universal was misassigned.
- An `@import` points at something non-versioned inside the team repo → scope leak.
- A glob lacks `**` while its subtree has subfolders → fix the glob.

## Reasoning checks
- Did I protect the cacheable prefix (no per-turn / subtree-only lines up top)?
- Is the import graph a DAG with no broken imports?
- Is precedence predictable and documented with explicit tie-breaks?
- Did I preserve existing manual edits (upgrade safety)?

Tag every reasoning step with the evidence taxonomy. Never green-as-success.
