<!-- distilled from alfa skills/changelog-writing -->
<!-- > -->
# Changelog Writing
> "Method over hacks."
## TL;DR
Author user-facing changelogs: semantic grouping, consistent tone, and migration guides for breaking changes. Optimize for the reader scanning to answer "does this affect me, and what must I do?" [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather raw deltas: merged PRs, commits, issue closures, version range (last tag → HEAD) [EXPLICIT]
- Identify audience (end users vs API consumers vs operators) — drives grouping and tone [INFERENCE]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV [EXPLICIT]
- Classify each change: Added / Changed / Deprecated / Removed / Fixed / Security (Keep a Changelog) [EXPLICIT]
- Flag breaking changes; each requires a migration note (before → after) [EXPLICIT]
- Derive semver bump: breaking→major, feature→minor, fix→patch [INFERENCE]
### Step 3: Execute
- Write entries with evidence tags; one line per change, imperative-past ("Added X"), no commit hashes in user-facing copy [EXPLICIT]
- Group by category, order categories Security→Removed→Changed→Added→Fixed (impact-first) [INFERENCE]
- Date the release `YYYY-MM-DD`; link version to its diff/tag [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied [EXPLICIT]
- [ ] Constitution-compliant [EXPLICIT]
- [ ] Actionable output (reader knows what changed and what to do) [EXPLICIT]
- [ ] Every breaking change has a migration path [EXPLICIT]
- [ ] No internal jargon, ticket IDs, or raw commit hashes in user-facing entries [INFERENCE]
- [ ] Semver bump matches the highest-impact change [INFERENCE]

## Usage

Example invocations:

- "/changelog-writing" — Run the full changelog writing workflow
- "changelog writing on this project" — Apply to current context

## Worked Example

```markdown
## [2.0.0] - 2026-06-11
### Security
- Patched token leak in session refresh (CVE-2026-1234)
### Removed
- Dropped Node 16 support — upgrade to Node 18+ (see Migration)
### Added
- Bulk export endpoint `POST /exports`
### Migration (1.x → 2.0)
- Replace `client.auth(token)` with `client.auth({ token })`
```
Trade-off: grouping by category (above) beats chronological — readers filter by concern faster, at the cost of losing commit order. [INFERENCE]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes a discoverable version boundary (tags, releases, or stated range); without one, treat all input as one unreleased block [ASSUMPTION]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not a release-automation tool, not a commit linter, does not publish or tag releases [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No version boundary found | Emit a single `[Unreleased]` section; ask for the target version |
| Breaking change with no migration steps | Block: hold the entry, request before/after from author |
| Internal-only / no user impact (chore, refactor, CI) | Omit from user-facing log; optionally note under a separate internal section |
| Hundreds of trivial deltas | Summarize by theme; link to full diff rather than listing each |
| Security fix | Lead with it; state severity and required action, withhold exploit detail until patched |
