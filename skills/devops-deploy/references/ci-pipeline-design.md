<!-- distilled from alfa skills/ci-pipeline-design -->
<!-- > -->
# Ci Pipeline Design
> "Method over hacks."
## TL;DR
Design CI pipelines: stage topology, parallelization, caching, artifact promotion. Optimize for fast feedback (fail cheapest checks first) and reproducibility. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory triggers (push, PR, tag, schedule), target runtimes, test suites, and current pipeline duration baseline. [EXPLICIT]
### Step 2: Analyze
- Map the stage DAG and evaluate parallelization/caching options per Constitution XIII/XIV. Identify the critical path. [EXPLICIT]
### Step 3: Execute
- Implement stages with evidence tags; pin tool/image versions; gate deploy on green required checks. [EXPLICIT]
### Step 4: Validate
- Re-run on a clean cache to prove reproducibility; confirm wall-clock and quality criteria met. [EXPLICIT]

## Reference Design
- **Stage order (fail-fast):** lint/format → unit → build → integration → package → deploy. Cheapest, most-likely-to-fail checks run first to shorten feedback loops. [EXPLICIT]
- **Parallelization:** fan out independent jobs (lint ∥ unit ∥ typecheck); shard slow test suites by file/timing. Converge before build. Speedup is bounded by the longest single job, not the sum. [INFERENCIA]
- **Caching:** key on a lockfile hash (e.g. `deps-${hash(lockfile)}`); restore-then-save; scope to dependencies and build outputs only. Never cache secrets or test results. [EXPLICIT]
- **Artifacts:** build once, promote the same immutable artifact across stages/environments. Tag with commit SHA; never rebuild per environment. [EXPLICIT]

## Worked Example
Node service, baseline 18 min serial. Split into lint ∥ unit ∥ typecheck (3 min, parallel) → build w/ cached `node_modules` (2 min) → integration sharded ×4 (4 min) → package+push image → deploy gated on all-green. Result ~9 min critical path; cache miss adds ~3 min for dependency install. [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Fail-fast stage ordering (cheapest checks first) [EXPLICIT]
- [ ] Cache key includes lockfile hash; no secrets cached [EXPLICIT]
- [ ] Build-once / promote-artifact across environments [EXPLICIT]
- [ ] Deploy gated on required green checks [EXPLICIT]

## Usage

Example invocations:

- "/ci-pipeline-design" — Run the full ci pipeline design workflow
- "ci pipeline design on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and CI config (e.g. `.github/workflows`, `.gitlab-ci.yml`) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: not a CD/release-promotion runbook, not infra provisioning, not secrets-management design [EXPLICIT]
- CI-platform-agnostic; concrete syntax (GitHub Actions, GitLab CI, etc.) is left to implementation [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Flaky tests on critical path | Quarantine/retry the flaky job; do not block deploy on known-flaky, but track it [INFERENCIA] |
| Cache poisoning or stale cache | Bump cache key prefix; validate restore on clean runner [EXPLICIT] |
| Cross-job artifact too large | Pass an artifact reference/registry digest, not the blob inline [INFERENCIA] |

## Failure Modes
- **Cache key too broad** → stale dependencies silently used; pin to lockfile hash. [EXPLICIT]
- **Rebuild per environment** → drift between tested and deployed artifact; promote one build. [EXPLICIT]
- **Slow checks first** → wasted minutes before a 2-second lint fails; reorder fail-fast. [EXPLICIT]
- **Unpinned tool/image versions** → non-reproducible builds; pin and validate on clean cache. [EXPLICIT]
