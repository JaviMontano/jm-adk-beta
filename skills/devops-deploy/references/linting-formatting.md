<!-- distilled from alfa skills/linting-formatting -->
<!-- > -->
# Linting & Formatting

> "Arguing about code style in reviews is a waste of time — let the machines decide." — Unknown

## TL;DR

Guides the setup of automated code quality tools — ESLint for code correctness, Prettier for formatting, Stylelint for CSS, pre-commit hooks with Husky/lint-staged, and CI integration. Use when establishing or improving code quality tooling for a project. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check existing linting/formatting configuration files
- Review `package.json` for installed lint/format dependencies
- Identify IDE integration setup (VS Code extensions, settings)
- Check for pre-commit hooks (Husky, pre-commit)

### Step 2: Analyze
- Evaluate ESLint config: which preset (airbnb, standard, recommended)?
- Determine Prettier preferences (semi, single quotes, tab width, trailing commas)
- Assess Stylelint needs for CSS/SCSS projects
- Plan integration strategy: IDE save → pre-commit → CI

### Step 3: Execute
- Configure ESLint with appropriate plugins (react, typescript, a11y, import)
- Set up Prettier with project-wide `.prettierrc` config
- Add Stylelint for CSS/SCSS with standard config
- Install Husky for Git hooks and lint-staged for pre-commit linting
- Configure lint-staged to run ESLint + Prettier only on staged files
- Add lint and format scripts to `package.json`
- Set up CI step that fails on lint errors (no auto-fix in CI)
- Add `.editorconfig` for cross-IDE consistency

### Step 4: Validate
- Pre-commit hook runs and catches formatting issues before commit
- CI fails on lint errors and formatting inconsistencies
- IDE shows lint errors inline and auto-formats on save
- No conflicting rules between ESLint and Prettier (use eslint-config-prettier)

## Quality Criteria

- [ ] ESLint, Prettier, and Stylelint configured and non-conflicting
- [ ] Pre-commit hooks catch issues before code enters the repository
- [ ] CI enforces lint/format rules (no auto-fix, just fail)
- [ ] IDE integration provides instant feedback during development
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Running linters only in CI (too late — should catch at save and pre-commit)
- Conflicting ESLint and Prettier rules (use eslint-config-prettier to resolve)
- Auto-fixing in CI (masks issues — developers should see and understand fixes)

## Related Skills

- `code-review` — linting removes style debates from code reviews
- `github-actions-ci` — lint step in CI pipeline

## Usage

Example invocations:

- "/linting-formatting" — Run the full linting formatting workflow
- "linting formatting on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
