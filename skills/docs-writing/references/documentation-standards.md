<!-- distilled from alfa skills/documentation-standards -->
<!-- > -->
# Documentation Standards
> "Method over hacks. Evidence over assumption."
## TL;DR
Defines the house contract for project docs: templates, review cycles, SemVer-style versioning, and archival policy. Output is a standards decision (what to apply) plus the conformed doc, not prose. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory existing docs, their formats, owners, and last-updated dates [EXPLICIT]
- Identify the doc type (reference, how-to, tutorial, explanation — Diátaxis quadrant) and audience
### Step 2: Analyze
- Pick the matching template; evaluate gaps vs. options per Constitution XIII (Think First) / XIV (Simple First)
- Decide version bump and archival action before writing (see below)
### Step 3: Execute
- Conform to the template; apply `[EXPLICIT]`/`[INFERENCIA]` evidence tags on every non-trivial claim
- Add front-matter: `title`, `owner`, `version`, `last_updated`, `status` (draft|review|published|archived)
### Step 4: Validate
- Run the acceptance gate; route through the review cycle below

## Quality Criteria
- [ ] Evidence tags applied to all non-trivial claims
- [ ] Front-matter complete (owner + version + status + last_updated)
- [ ] Diátaxis quadrant declared and template matched
- [ ] Constitution-compliant; single-brand, no invented prices
- [ ] Actionable output with at least one worked example

## Templates & Versioning
- **Required sections** per doc: Title, TL;DR, Body (quadrant-specific), Quality Criteria, last_updated. [EXPLICIT]
- **Versioning (SemVer-for-docs)**: MAJOR = breaking restructure or removed guidance; MINOR = new section/material guidance; PATCH = typo/clarification. Bump `version` + `last_updated` together. [EXPLICIT]
- **Review cycle**: draft → peer review (one reviewer min) → owner sign-off → published. Re-review on every MINOR+; PATCH may self-merge. [EXPLICIT]
- **Archival**: superseded docs get `status: archived` + a link to the replacement; never hard-delete (preserve cross-references). Stale = no update in 180 days → flag for owner review. [EXPLICIT]

## Acceptance Criteria
- A doc PASSES only if all Quality Criteria boxes are checkable AND it lints clean (no broken links, no orphaned headings referenced by routes). [EXPLICIT]
- A standards decision PASSES only if it names the quadrant, the template, and the version action explicitly. [EXPLICIT]

## Usage

Example invocations:

- "/documentation-standards" — Run the full documentation standards workflow
- "documentation standards on this project" — Apply to current context

## Related Skills

- `documentation-system` — doc-as-code workflow, CI publishing
- `technical-writing-patterns` — sentence/section-level style
- `changelog-writing` — release-note conventions

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: does not author content, run CI, or publish — only sets and checks the standard [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No template fits the doc type | Default to nearest Diátaxis quadrant; note the deviation in front-matter |
| Doc has no owner | Block publish; assign owner before status advances past draft |
| Version conflict (two edits) | Higher bump wins; reconcile content, re-run review |
