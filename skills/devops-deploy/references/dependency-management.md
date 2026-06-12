<!-- distilled from alfa skills/dependency-management -->
<!-- Lockfiles, update cadence, Renovate/Dependabot automation, and vulnerability scanning -->
# Dependency Management {DevOps}
> "Method over hacks."

## TL;DR
Commit lockfiles, automate updates via Renovate/Dependabot, gate merges on vulnerability scans, and keep upgrade risk proportional to semver scope. [EXPLICIT]

## Physics — 3 Immutable Laws
1. **Law of Reproducibility**: A committed lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) is the single source of truth. CI installs with `npm ci` / `pnpm i --frozen-lockfile` — never `install`, which mutates the lock. [EXPLICIT]
2. **Law of Proportional Risk**: Patch/minor bumps auto-merge after green CI; majors require human review (breaking changes, peer-dep conflicts). Risk gating follows semver, not convenience. [EXPLICIT]
3. **Law of Visible Provenance**: Every dependency change lands via PR with a changelog/diff link — never an unscoped manual edit to the manifest. [EXPLICIT]

## Protocol

### Phase 1 — Lockfile Discipline
1. Commit the lockfile; one package manager per repo (mixing `npm` + `pnpm` locks corrupts resolution). [EXPLICIT]
2. CI uses frozen installs; fail the build if the lock is out of sync with the manifest. [EXPLICIT]
3. Pin the package-manager version via `packageManager` field or `.nvmrc`/`.tool-versions`. [EXPLICIT]

### Phase 2 — Automated Updates
1. Choose one bot: Renovate (granular grouping, monorepo-aware) or Dependabot (zero-config GitHub-native). Do not run both — duplicate PRs. [INFERENCE]
2. Group low-risk updates (lint/test/types devDeps) into one PR; isolate runtime + major bumps. [EXPLICIT]
3. Enable auto-merge for patch/minor once required checks pass; assign reviewers for majors. [EXPLICIT]
4. Cap PR concurrency (`prConcurrentLimit`) to avoid CI saturation. [EXPLICIT]

### Phase 3 — Vulnerability Scanning
1. Run `npm audit --audit-level=high` (or `pnpm audit`, Snyk, `osv-scanner`) in CI; fail on high/critical. [EXPLICIT]
2. Triage advisories: patch if a fix exists; else apply an override/resolution or accept-with-justification. [EXPLICIT]
3. Schedule a weekly scan independent of code changes — new CVEs land against unchanged deps. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Manifest + lockfile | Reproducible, frozen install in CI |
| Bot config (`renovate.json` / `dependabot.yml`) | Scheduled, grouped, risk-gated update PRs |
| Audit advisory feed | Pass/fail gate + triaged remediation PRs |
| Semver range of a bump | Auto-merge (patch/minor) vs review (major) |

## Quality Gates — 5 Checks
1. **Lockfile committed and in sync** — frozen install succeeds. [EXPLICIT]
2. **Single package manager** — exactly one lockfile type present. [EXPLICIT]
3. **One update bot active** — no duplicate Renovate/Dependabot PRs. [EXPLICIT]
4. **Audit gate enforced** — high/critical CVEs block merge. [EXPLICIT]
5. **Majors human-reviewed** — no auto-merged breaking upgrades. [EXPLICIT]

## Decisions & Trade-offs
- **Renovate vs Dependabot**: Renovate for monorepos/fine-grained grouping; Dependabot for low-setup single repos. Trade-off: Renovate config is powerful but verbose. [INFERENCE]
- **Auto-merge minors**: speeds patching but trusts the test suite — only enable with meaningful CI coverage. [EXPLICIT]
- **Pin (`=`) vs caret (`^`)**: pin apps for determinism; use ranges in libraries to avoid forcing transitive conflicts on consumers. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Transitive CVE, no direct fix | `overrides`/`resolutions` to force a patched sub-dependency; document the pin |
| Major bump breaks peer deps | Hold PR, upgrade the peer first, or split into a coordinated batch |
| Bot PR storm saturates CI | Lower `prConcurrentLimit`; widen grouping; pin a schedule window |
| Lockfile merge conflict | Regenerate from manifest (`npm i --package-lock-only`); never hand-edit the lock |
| Abandoned/unmaintained dependency | Flag for replacement; pin current version and add to tech-debt register |
| Empty or minimal input | Request clarification before proceeding |

## Self-Correction Triggers
- CI install differs from local → lockfile drift; commit the regenerated lock. [EXPLICIT]
- Repeated audit failures on one dep → escalate to override or replacement. [EXPLICIT]
- Auto-merged minor broke prod → tighten the gate or demote to review-required. [EXPLICIT]

## Usage
Example invocations:
- "/dependency-management" — Run the full dependency management workflow
- "lockfile/upgrade/audit on this project" — Apply to current context

## Assumptions & Limits
- Assumes a JS/TS package-manager ecosystem (npm/pnpm/yarn); adapt commands for other stacks. [EXPLICIT]
- Assumes CI with required status checks and merge protection enabled. [EXPLICIT]
- Anti-scope: does not cover license compliance or SBOM generation — separate concern. [EXPLICIT]
- Does not replace domain expert judgment for major-version migration decisions. [EXPLICIT]
