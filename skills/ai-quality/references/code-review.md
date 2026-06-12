<!-- distilled from alfa skills/code-review -->
<!-- > -->
# Code Review

## TL;DR

Review code changes with deterministic scope, evidence, severity, category,
decision, and remediation rules. Read-only: inspects files, diffs, tests, logs,
CI output; never edits the review target. Output is a severity-ordered,
evidence-bound report (JSON preferred, Markdown mirror allowed). No artifact →
`needs_context`, not invented findings. [CONFIG]

## Scope & Anti-Scope

- IN: code, PRs, patches, diffs, changed files, implementation quality, code
  review comments, test/CI output supplied as evidence. [CONFIG]
- OUT: generic product/book/course reviews, non-code critique, editing target
  code, executing the code, fetching remote/live artifacts, security pentest
  depth (route to `audit-security`), release-gate enforcement (route to
  `quality-gatekeeper`). [CONFIG]
- Read-only invariant: emitting any edit, commit, or write to the target is a
  contract violation even if the user asks; recommend the change instead. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` — assets required by this skill. [CÓDIGO]
- `assets/activation-policy.json` — activation and refusal routing. [CÓDIGO]
- `assets/review-taxonomy.json` — fixed severities, categories, release
  decisions. [CÓDIGO]
- `assets/evidence-policy.json` — evidence tags and source requirements. [CÓDIGO]
- `assets/report-contract.json` — JSON report shape. [CÓDIGO]
- `assets/source-boundary-policy.json` — allowed inputs and no-write boundaries. [CÓDIGO]
- `scripts/check.sh` — runs the report validator against valid and invalid
  fixtures (offline: no network, wall-clock, or RNG). [CÓDIGO]

## Activation

Activate when the user supplies or points to code artifacts (PR, diff, patch,
file path, repo context) and asks to inspect quality or review comments. Do not
activate for non-code critique unless code artifacts are supplied. [CONFIG]

If no code, diff, PR, file path, or repo context is available, emit a
minimum-input request (`needs_context`) instead of inventing findings. [CONFIG]

## Inputs

Accept one or more:

- PR URL, branch name, commit range, staged diff, patch, or code excerpt.
- Issue, requirement, acceptance criteria, test output, or CI result.
- Explicit review depth: `quick`, `standard`, or `deep` (default `standard`). [CONFIG]
- Caller-supplied review date if a dated report is required. Never read the
  system clock; absence of a supplied date means the report is undated. [CONFIG]

### Review depth semantics

| Depth | Covers | Trade-off |
|-------|--------|-----------|
| `quick` | Changed hunks only; BLOCKER/MAJOR triage. | Fast; may miss diffuse maintainability issues. [INFERENCIA] |
| `standard` | Changed hunks + directly touched callers/callees + stated tests. | Default balance of cost vs. coverage. [INFERENCIA] |
| `deep` | Standard + adjacent invariants, error paths, contract/test gaps. | Highest coverage; more `[INFERENCIA]` findings to verify. [INFERENCIA] |

## Review Procedure

1. Establish scope:
   - Identify files, line ranges, diff hunks, tests, and stated intent.
   - Record unavailable artifacts in `minimum_inputs_missing`.
   - Do not rely on unstated intent or invisible files. [CONFIG]
2. Classify findings with the fixed taxonomy:
   - Severities: `BLOCKER`, `MAJOR`, `MINOR`, `NIT`.
   - Categories: `correctness`, `security`, `tests`, `performance`,
     `maintainability`, `accessibility`, `api_contract`, `observability`,
     `style`, `positive`. [CÓDIGO]
3. Gather evidence — every code finding cites `file`, `line`, `claim`,
   `evidence_tag`:
   - `[CÓDIGO]` — inspected code/diff/test/CI evidence.
   - `[CONFIG]` — repo policy, review standard, or user-supplied acceptance
     criteria.
   - `[INFERENCIA]` — a reasoned risk that follows from cited code (must name the
     cited line it follows from).
   - `[DOC]` — behavior asserted by supplied documentation/spec.
   - `[SUPUESTO]` — an assumption the reviewer had to make; surface in
     `Risks and Limits`, never as a BLOCKER. [CONFIG]
4. Apply severity rules:
   - `BLOCKER`: likely correctness/security/data-loss failure, broken contract,
     or required test/CI failure that should block merge.
   - `MAJOR`: material quality or risk issue to address before/near merge but not
     an immediate release blocker.
   - `MINOR`: useful improvement with limited risk.
   - `NIT`: style/readability preference; must not block merge unless it violates
     a cited policy. [CONFIG]
5. Produce a decision (exactly one):
   - `request_changes` — at least one `BLOCKER`.
   - `approve_with_comments` — only `MAJOR`/`MINOR`/`NIT`.
   - `approve` — no blocking/material findings and positive patterns recorded.
   - `needs_context` — minimum input missing. [CONFIG]
6. Validate:
   - `bash skills/code-review/scripts/check.sh` for skill fixtures.
   - `python3 -B scripts/validate-skill-dod.py --skill code-review` before
     marking complete. [CÓDIGO]

## Output Contract

Preferred output is JSON per `assets/report-contract.json`. Markdown reports
must preserve the same sections, in order:

1. `# Code Review Report`
2. `## Scope`
3. `## Findings`
4. `## Positive Patterns`
5. `## Validation`
6. `## Decision`
7. `## Risks and Limits`

Findings ordered by severity (`BLOCKER`, `MAJOR`, `MINOR`, `NIT`), then file
path, then line number. Finding IDs gapless as `CR-NNN` (`CR-001`, `CR-002`, …);
a gap or duplicate ID fails validation. The decision field must equal the value
implied by step 5 — a mismatch is a contract violation. [CONFIG]

### Worked example (one finding, JSON shape)

```json
{
  "id": "CR-001",
  "severity": "BLOCKER",
  "category": "correctness",
  "file": "src/auth/session.ts",
  "line": 42,
  "claim": "Token expiry compared with > instead of >=, so a token expiring exactly now is treated as valid.",
  "evidence_tag": "[CÓDIGO]",
  "remediation": "Use >= for the now-vs-expiry comparison; add a boundary test at exp == now."
}
```

Decision for a report whose worst finding is the above: `request_changes`. [CONFIG]

## Quality Criteria / Acceptance

- [ ] Scope is explicit and source-bound. [CONFIG]
- [ ] No finding lacks file/line evidence unless it is a documented
      context/input gap. [CONFIG]
- [ ] Decision is the single value implied by the highest severity present. [CONFIG]
- [ ] Style-only concerns are never blockers without a cited policy. [CONFIG]
- [ ] Clean-code reports record positive patterns and fabricate nothing. [CONFIG]
- [ ] Every claim carries `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, or
      `[SUPUESTO]`. [CONFIG]
- [ ] Finding IDs gapless; sections present and ordered. [CONFIG]
- [ ] Local deterministic checks pass. [CÓDIGO]

## Edge Cases

- Empty diff / no net change → `approve` with a note, or `needs_context` if even
  the diff is missing. Do not invent findings to look useful. [CONFIG]
- Generated/vendored/lockfile changes → flag as out-of-scope-by-default; review
  only if the user states intent to hand-author them. [INFERENCIA]
- Mixed-language or binary blobs in the diff → review what is human-readable;
  record binaries as `minimum_inputs_missing` (cannot inspect). [CONFIG]
- User claims a test passes but supplies no CI/log → treat as `[SUPUESTO]`, not
  `[CÓDIGO]`; do not upgrade to a clean bill of health. [CONFIG]
- Conflicting requirement vs. code → report as `api_contract`/`correctness`
  finding citing both sources, not as reviewer opinion. [CONFIG]

## Failure Modes (avoid)

- Rubber-stamping a PR without reading the diff. [CONFIG]
- Blocking on a style preference owned by lint/format tooling. [CONFIG]
- Saying "looks good" when required artifacts are missing → use `needs_context`. [CONFIG]
- Fabricating files, tests, CI status, or hidden behavior. [CONFIG]
- Echoing real secrets or sensitive values in review output. [CONFIG]
- Using current time, web research, randomness, or remote assets unless the user
  supplies and the report cites that source. [CONFIG]
- Decision/severity mismatch (e.g. a BLOCKER with `approve_with_comments`). [CONFIG]

## Related Skills

- `code-review-checklist` — reusable checklist generation.
- `audit-security` — deeper security-specific static audit.
- `quality-gatekeeper` — release-gate decision enforcement.
- `assumption-log` — unresolved review assumptions.

## Assumptions & Limits

- Reviews supplied evidence only; cannot prove behavior outside inspected code,
  diff, tests, or CI. Absence of a finding is not proof of correctness. [CONFIG]
- Recommends tests but does not modify target code. [CONFIG]
- Asks for missing minimum inputs rather than inventing findings. [CONFIG]
