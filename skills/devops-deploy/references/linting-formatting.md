<!-- distilled from alfa skills/linting-formatting -->
<!-- > -->
# Linting & Formatting

> "Arguing about code style in reviews is a waste of time — let the machines decide." — Unknown

## TL;DR

Sets up automated code-quality tooling: ESLint (correctness), Prettier (formatting), Stylelint (CSS), pre-commit hooks via Husky + lint-staged, and a CI gate. Use when establishing or hardening quality tooling on a JS/TS project. Layered defense — IDE-on-save → pre-commit → CI — so issues die as early and cheaply as possible. [EXPLICIT]

**Scope.** JS/TS/CSS ecosystems (Node toolchain). For Python/Go/Rust, the layering principle holds but tools differ (ruff/black, gofmt, rustfmt) — out of scope here. [SUPUESTO]

## Procedure

### Step 1: Discover
- Locate existing configs: `.eslintrc*` / `eslint.config.*`, `.prettierrc*`, `.stylelintrc*`, `.editorconfig`. [CONFIG]
- Read `package.json` for installed lint/format deps and `engines.node` (drives ESLint flat-vs-legacy choice). [CONFIG]
- Identify IDE setup (`.vscode/settings.json`, recommended extensions in `.vscode/extensions.json`). [CONFIG]
- Check for pre-commit hooks (`.husky/`, `.pre-commit-config.yaml`, `package.json#lint-staged`). [CONFIG]

### Step 2: Analyze
- ESLint preset choice: `airbnb` (strict, opinionated), `standard` (no-semi), or `eslint:recommended` + `@typescript-eslint` (minimal, composable). [DOC]
- **Decision — flat config (`eslint.config.js`) vs legacy (`.eslintrc`):** prefer flat config on ESLint v9+ (it is the default and legacy is deprecated); stay on legacy only if a critical plugin lacks flat support. [INFERENCIA]
- Prettier options to pin explicitly: `semi`, `singleQuote`, `tabWidth`, `trailingComma`, `printWidth` — pin them so the config is the single source of truth, not tool defaults that drift across versions. [INFERENCIA]
- Stylelint needed only if the repo ships CSS/SCSS/styled-components; skip otherwise to avoid dead config. [INFERENCIA]
- Integration order is fixed: IDE save → pre-commit → CI (cheapest feedback first). [DOC]

### Step 3: Execute
- Configure ESLint with the plugins the stack actually uses (`react`, `@typescript-eslint`, `jsx-a11y`, `import`). [CONFIG]
- Add `.prettierrc` with all style options pinned; add `.prettierignore` (build output, lockfiles, generated code). [CONFIG]
- If styling exists, add Stylelint with `stylelint-config-standard` (+ `-scss`). [CONFIG]
- Install Husky for Git hooks + lint-staged; run `husky init` so the hook is committed and reproducible for every clone. [CÓDIGO]
- Scope lint-staged to staged files only (`*.{ts,tsx,js}` → `eslint --fix`; `*.{ts,tsx,js,css,md,json}` → `prettier --write`) — fast hooks survive; slow hooks get bypassed with `--no-verify`. [INFERENCIA]
- Add `package.json` scripts: `lint`, `lint:fix`, `format`, `format:check`. [CONFIG]
- Add a CI step that runs `lint` + `format:check` (check mode, **no** `--fix`). [CONFIG]
- Add `.editorconfig` for cross-IDE consistency (charset, EOL, final newline, indent). [CONFIG]

### Step 4: Validate
- Pre-commit hook blocks a deliberately mis-formatted commit. [DOC]
- CI fails on a lint error and on a formatting drift (`format:check` exits non-zero). [DOC]
- IDE shows lint errors inline and formats on save. [DOC]
- No ESLint/Prettier rule conflicts: `eslint-config-prettier` is last in the extends/config array, disabling stylistic ESLint rules Prettier owns. [INFERENCIA]

## Quality Criteria

- [ ] ESLint, Prettier, and (if needed) Stylelint configured and non-conflicting. [DOC]
- [ ] Pre-commit hooks catch issues before code enters the repo, and are committed (not local-only). [DOC]
- [ ] CI enforces lint/format in check mode — fail, never auto-fix. [DOC]
- [ ] IDE integration gives instant in-editor feedback. [DOC]
- [ ] Evidence tags applied to all non-trivial claims. [EXPLICIT]

## Acceptance Criteria (binary, verifiable)

- `npm run lint` exits 0 on a clean tree and non-zero on an introduced error. [DOC]
- `npm run format:check` exits non-zero when a tracked file is unformatted. [DOC]
- A fresh `git clone` + install reproduces the pre-commit hook without manual steps. [INFERENCIA]
- Running `eslint` and `prettier` on the same file yields zero overlapping/conflicting complaints. [INFERENCIA]

## Anti-Patterns

- Linting only in CI — too late; catch at save and pre-commit. [DOC]
- Conflicting ESLint/Prettier rules — resolve with `eslint-config-prettier` placed last. [INFERENCIA]
- Auto-fixing in CI — masks the problem and can push unreviewed diffs; surface failures, let the dev fix locally. [INFERENCIA]
- Heavy pre-commit hooks (full type-check, whole-repo lint) — devs bypass them; keep hooks to staged files. [INFERENCIA]
- Leaving Prettier defaults implicit — version bumps silently change formatting and churn diffs. [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| ESLint and Prettier fight over the same line | `eslint-config-prettier` missing or not last | Add it; place last in config chain. [INFERENCIA] |
| Hook works locally, not after clone | Husky not installed via committed `prepare` script | Add `"prepare": "husky"`; commit `.husky/`. [INFERENCIA] |
| CI green but local red (or vice-versa) | Different ESLint/Node versions | Pin versions in `package.json`; use `npm ci`. [INFERENCIA] |
| Lint passes, formatting still drifts | CI runs `lint` but not `format:check` | Add a separate `format:check` CI step. [DOC] |
| Pre-commit painfully slow | Linting whole repo, not staged files | Scope globs in lint-staged to staged paths. [INFERENCIA] |

## Related Skills

- `code-review` — linting removes style debates from code reviews.
- `github-actions-ci` — lint step in CI pipeline.

## Usage

Example invocations:

- "/linting-formatting" — Run the full linting formatting workflow.
- "linting formatting on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes a Node-based JS/TS toolchain; non-JS stacks need different tools (anti-scope). [SUPUESTO]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- Does not author rule content for a specific in-house style guide — assumes a published preset as the base. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request | Redirect to appropriate skill or escalate. |
| Monorepo with mixed configs | Root base config + per-package overrides; do not force one global config. [INFERENCIA] |
| Legacy repo, huge first-format diff | Format in one isolated commit; add SHA to `.git-blame-ignore-revs`. [INFERENCIA] |
| ESLint v9 + plugin lacking flat-config support | Stay on legacy config or use the compat shim until the plugin migrates. [SUPUESTO] |
