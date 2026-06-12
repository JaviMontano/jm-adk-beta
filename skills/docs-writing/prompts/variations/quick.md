# Quick variation — docs-writing (depth=quick)

Fast path for an internal-draft writing deliverable. Essentials only; still routed,
still validated.

## Use when

The user wants a usable draft fast, for internal eyes, and a matching topic exists.

## Steps

1. Resolve `topic` to one enum value. One disambiguating question max; otherwise commit.
2. Read `references/<topic>.md` — only that one.
3. Discover just the source material the route strictly needs; mark any gap `[SUPUESTO]`.
4. Execute the essential sections of `templates/output.md` (skip optional depth).
5. Validate the must-pass subset of the playbook's Quality Criteria — never skip
   Validate entirely.

## Output

A lean but governed draft: one tag family, non-obvious claims tagged, no invented
prices, single brand. Flag what `deep` would add so the user can escalate.

## Example invocation

> "Quick changelog from the last 12 merged PRs since tag v1.4.0 — internal draft."
Route: `changelog-writing`. Group by category, derive the semver bump, mark any PR with
unclear user impact `[SUPUESTO]`, validate that every breaking change has a migration
line.
