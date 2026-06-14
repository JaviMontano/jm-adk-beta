# Example Input — claude-md-architecture

## Context
A monorepo `acme-platform` whose root `CLAUDE.md` has grown to 420 lines and loads
on every turn. Three subtrees have divergent rules. A personal preference has leaked
into the versioned team file.

## Repo layout
```
acme-platform/
  CLAUDE.md            # 420 lines, always loaded
  frontend/            # React app
  infra/               # Terraform
  services/payments/   # Go service
```

## Current root CLAUDE.md (excerpt)
```markdown
- Conventional commits; never push to main directly.        # universal
- Use the design-system tokens; no inline styles.           # frontend only
- Co-locate tests as *.test.tsx next to the component.      # frontend only
- All Terraform must pass `tflint` before apply.            # infra only
- Payments amounts are integer minor units; never floats.   # payments only
- Prefer pnpm over npm.                                      # personal preference
- ...380 more lines mixing universal and subtree rules...
```

## Request
"Our root CLAUDE.md is 420 lines and reloads every turn. Split it into a
user/team/module hierarchy with @imports and path-scoped rules. Keep the root prefix
cache-stable, scope the frontend / infra / payments rules to their subtrees, and get
the pnpm preference out of the team repo. Don't overwrite any manual edits we already
have in services/payments."

## Known subtrees with own rules
- `frontend/**` — design-system tokens, test co-location.
- `infra/**` — `tflint` gate.
- `services/payments/**` — integer minor units rule.
