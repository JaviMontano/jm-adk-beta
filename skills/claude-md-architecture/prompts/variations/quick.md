# Quick Prompt — claude-md-architecture

Fast path for a clearly-scoped split. Skip the long discovery; go straight to
classify → declare → compile → gate.

1. Read the current root `CLAUDE.md`.
2. Classify rules: universal (root) / per-module (glob-gated) / per-user (user scope).
3. Emit lean root (universals + `@imports`) + one `module/CLAUDE.md` per subtree with
   `apply to: "<glob>/**"` (recursive).
4. Add a one-line precedence rule: most specific subpath wins; note any tie-break.
5. Run `bash skills/claude-md-architecture/scripts/check.sh`.

Guardrails: no per-turn value in the prefix; no personal pref in the team repo;
recursive globs only; don't clobber existing manual edits. Tag claims
`[DOC] [CONFIG] [INFERENCIA] [SUPUESTO]`. Never green-as-success.
