# Example Output — claude-md-architecture

## 1. Summary
- Repo: `acme-platform` [CONFIG]
- Before: root `CLAUDE.md` = 420 lines, loaded every turn. [CONFIG]
- After: root = 14 lines (universals + imports) + 3 module files + user-scope import.
- Outcome: stable cacheable prefix; frontend/infra/payments rules load on demand. [INFERENCIA]

## 2. Rule census and classification

| Rule | Was | Bucket | Target file |
|------|-----|--------|-------------|
| Conventional commits; never push to main | root | universal | `CLAUDE.md` |
| Design-system tokens; no inline styles | root | per-module | `frontend/CLAUDE.md` |
| Co-locate tests as `*.test.tsx` | root | per-module | `frontend/CLAUDE.md` |
| Terraform must pass `tflint` | root | per-module | `infra/CLAUDE.md` |
| Amounts are integer minor units | root | per-module | `services/payments/CLAUDE.md` |
| Prefer pnpm over npm | root | per-user | `~/.claude/CLAUDE.md` |

Duplicates deduped: none. Personal preference removed from team repo. [INFERENCIA]

## 3. Root team CLAUDE.md (stable prefix)

```markdown
# team CLAUDE.md (versioned, stable prefix)
@import ./CONVENTIONS.md
@import ~/.claude/CLAUDE.md      # pnpm pref now lives here, not in the repo

## Rules (universal)
- Conventional commits; never push to main directly.

## Path-scoped rules
- apply to: "frontend/**"           ->  @import ./frontend/CLAUDE.md
- apply to: "infra/**"              ->  @import ./infra/CLAUDE.md
- apply to: "services/payments/**"  ->  @import ./services/payments/CLAUDE.md
```

No per-turn values, no subtree-only rules in the prefix. 420 → 14 lines. [INFERENCIA]

## 4. Module files

```markdown
# frontend/CLAUDE.md  (loaded only on frontend/** work)
- Use the design-system tokens; no inline styles.
- Co-locate tests as *.test.tsx next to the component.
```
```markdown
# infra/CLAUDE.md  (loaded only on infra/** work)
- All Terraform must pass `tflint` before apply.
```
```markdown
# services/payments/CLAUDE.md  (loaded only on services/payments/** work)
- Amounts are integer minor units; never floats.
- [PRESERVED] Existing manual edits merged, not overwritten.   # upgrade safety
```

All globs recursive (`**`). No empty module files created. [DOC]

## 5. Precedence table

| Glob (most → least specific) | Wins over | Tie-break |
|------------------------------|-----------|-----------|
| `services/payments/**` | `services/**` | specificity |
| `frontend/**` | (root universals) | most-specific subpath |

## 6. Import graph (DAG)
- Nodes: root, `frontend/CLAUDE.md`, `infra/CLAUDE.md`, `services/payments/CLAUDE.md`, `~/.claude/CLAUDE.md`.
- Cycle check: PASS (no edges form a loop). Broken-import check: PASS. [DOC]

## 7. Upgrade safety
- `services/payments/CLAUDE.md` manual edits preserved via merge; diff shows only
  additions, no clobbered lines. [CÓDIGO]

## 8. Validation gate
- `bash skills/claude-md-architecture/scripts/check.sh` → DAG ok, globs recursive,
  precedence defined, no per-turn values in prefix, no versioned personal pref. [CONFIG]
- All SKILL.md acceptance boxes checked with the evidence above.

## 9. Assumptions
- `services/payments` had ≥1 own rule, so a module file is justified (not graph noise). [SUPUESTO]
