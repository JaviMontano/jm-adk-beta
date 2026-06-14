# Deep Prompt — claude-md-architecture

Full treatment for a large monorepo or a memory that has accreted for months.

## 1. Inventory
Grep the entire memory surface: root `CLAUDE.md`, any existing `module/CLAUDE.md`,
and `~/.claude/CLAUDE.md`. Build a complete rule census with current location.

## 2. Classify with cache reasoning
For each rule, decide universal / per-module / per-user. For every candidate
*universal*, justify why it belongs in the cacheable prefix — remember a single
volatile or subtree-only line invalidates the KV prefix for **every** turn. Reject
weak universals down to module scope.

## 3. Precedence model
Enumerate all overlapping globs (`src/**` vs `src/api/**`, etc.). Order by
specificity; where specificity is ambiguous, declare an explicit tie-break. Produce
the full precedence table.

## 4. Import topology
Draw the `@import` graph. Prove it is a DAG (no cycles). Confirm every import path
exists; mark any post-rename break as a hard failure, not a silent degrade.

## 5. Ontology-first compile
Populate `assets/architecture-schema.json` + `architecture-policy.json`, then run
`scripts/compile-claude-md-architecture.py <arch.json> --output <report.md>`.

## 6. Gate with evidence
Run `bash skills/claude-md-architecture/scripts/check.sh`. Capture the functional
output — do not accept a bare exit code. Walk every acceptance checkbox in
`SKILL.md`.

## 7. Upgrade-safe merge
Diff before/after each `module/CLAUDE.md`; preserve manual edits.

Tag everything `[DOC] [CONFIG] [CÓDIGO] [INFERENCIA] [SUPUESTO]`. Single-brand;
no client PII; no invented prices.
