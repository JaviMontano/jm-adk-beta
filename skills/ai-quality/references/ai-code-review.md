<!-- distilled from alfa skills/ai-code-review -->
<!-- > -->
# AI Code Review
> Source evidence before suggestion confidence.

## TL;DR
Use this skill when the user asks for AI-assisted code review, automated review suggestions, diff review, or review-report generation. Produce a review traceable to exact files and lines, separating confirmed findings from hypotheses, and refusing to claim test results without command evidence. Default output is dual: Markdown for humans, JSON packet for machines. [DOC]

## Deterministic Assets
- `assets/review-report-contract.json` defines the machine-checkable review report packet. [CONFIG]
- `assets/severity-policy.json` defines priority, blocking, and escalation rules. [CONFIG]
- `assets/evidence-policy.json` defines allowed evidence tags and source requirements. [CONFIG]
- `assets/scope-policy.json` defines in-scope file matching and generated-file handling. [CONFIG]
- `assets/false-positive-policy.json` defines suppression, confidence, and degradation rules. [CONFIG]
- `scripts/validate_ai_code_review_report.py` validates report packets offline. [CÓDIGO]

Assets are the source of truth: when this doc and an asset disagree, the asset wins and this doc is the bug. [INFERENCIA]

## Procedure
### Step 1: Activate Intentionally
- Activate only for code review, diff review, static review, AI-assisted suggestion generation, or review-report requests.
- Do not activate for unrelated AI writing, weather, project management, or general coding questions unless the user explicitly requests code review.

### Step 2: Establish Review Scope
- Identify reviewed commit, branch, diff, files, or directories. If two interpretations exist (e.g. "this PR" vs. working tree), state the chosen one as a `[SUPUESTO]` and proceed. [INFERENCIA]
- Record `scope.includes` and `scope.excludes` in the output contract.
- Treat generated files, vendored files, lockfiles, and snapshots as excluded unless the user explicitly asks to review them.

### Step 3: Gather Evidence
- Read source files before judging behavior. A finding that cites a file you did not open is a `[SUPUESTO]`, not a finding. [INFERENCIA]
- Cite exact `file` and `line_start` for every finding.
- Use evidence tags from `assets/evidence-policy.json`. This is a kit-facing doc, so use the Alfa core set (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`); never mix tag families in one report. [DOC]
- If a finding depends on runtime behavior, include command output in `validation.commands_run` or mark the finding `needs-verification`. Never infer pass/fail from reading code alone. [DOC]

### Step 4: Review With Stable Categories
- Check correctness, security, data integrity, concurrency, performance, maintainability, observability, tests, accessibility, and AI-specific risks when relevant.
- Assign priorities using `assets/severity-policy.json`.
- One finding per root cause; group duplicates under the strongest evidence so a single fix closes one finding. [INFERENCIA]

### Step 5: Filter False Positives
- Reject findings based only on style preference, broad suspicion, or missing context.
- Downgrade low-confidence issues to `needs-verification` rather than dropping silently — the suppression itself is signal. [INFERENCIA]
- Include `false_positive_notes` when a tempting issue was suppressed, so a human can re-open it.

### Step 6: Produce The Report
- Prefer Markdown for human review and JSON for machine validation; emit both when the consumer is unknown. [SUPUESTO]
- JSON packets must follow `assets/review-report-contract.json`.
- Run `bash skills/ai-code-review/scripts/check.sh` before marking local DoD evidence.

## Worked Example (minimal finding)
Input: diff touching `src/auth/token.py` line 42, where a JWT is decoded without signature verification. [DOC]
```json
{
  "id": "F-001", "priority": "blocker", "category": "security",
  "status": "confirmed", "file": "src/auth/token.py", "line_start": 42,
  "evidence_id": "E-001",
  "observation": "jwt.decode called with verify=False on an externally supplied token.",
  "impact": "Forged tokens accepted; full auth bypass.",
  "recommendation": "Verify signature against the configured key; reject on failure.",
  "confidence": "high", "false_positive_notes": null
}
```
Contrast: the same call inside a clearly-marked test fixture is suppressed with a `false_positive_notes` entry, not raised as `blocker`. [INFERENCIA]

## Quality Criteria
- [ ] Every finding has exact file-line evidence.
- [ ] Priority follows the severity policy.
- [ ] False positives and low-confidence claims are filtered or downgraded.
- [ ] Test-pass or test-fail claims cite executed commands.
- [ ] Output includes validation status, remaining risks, and review limits.
- [ ] Machine-readable packets pass `scripts/validate_ai_code_review_report.py`.
- [ ] All findings use one tag family (Alfa core), consistently spelled. [DOC]

## Output Contract
Required top-level JSON fields:
- `schema`: `jm-labs.ai-code-review.report.v1`
- `target`, `scope`, `review_mode`, `evidence`, `findings`, `summary`, `validation`, `risks`

Each finding requires:
- `id`, `priority`, `category`, `status`, `file`, `line_start`, `evidence_id`, `observation`, `impact`, `recommendation`, `confidence`, `false_positive_notes`

`status` ∈ {`confirmed`, `needs-verification`, `suppressed`}; `validation` ∈ {`pass`, `warn`, `block`}. A report whose `validation` is `block` cannot be marked DoD-complete. [SUPUESTO]

## Usage
Example invocations:
- "/ai-code-review review this PR"
- "Run an AI-assisted code review on the current diff"
- "Review this patch for correctness, security, and test gaps"
- "Generate a machine-checkable review report for these files"

## Decisions & Trade-offs
| Decision | Rationale | Trade-off accepted |
|----------|-----------|--------------------|
| Exclude generated/vendored files by default | Noise dominates signal; authors don't own them. [INFERENCIA] | A real bug in vendored code is missed until explicitly requested. |
| Require executed commands for any pass/fail claim | Read-only inference of test status is the top false-confidence failure. [DOC] | Slower; some obvious-looking results still need a run. |
| One finding per root cause | Keeps fix-to-finding ratio honest; avoids inflated counts. [INFERENCIA] | A root cause with many symptoms looks "small" in the count. |
| Downgrade, never drop, weak findings | Preserves auditability of suppression. [INFERENCIA] | Report is longer than a drop-everything pass. |

## Assumptions & Limits
- Assumes access to the files, diff, or report inputs under review. [SUPUESTO]
- Does not replace maintainer judgment; it produces source-backed review evidence. [DOC]
- Does not claim tests passed, failed, or reproduced unless commands were executed and recorded. [DOC]
- Network research is out of scope unless the user explicitly allows it and source attribution is recorded. [DOC]
- Anti-scope: does not auto-apply fixes, push commits, or approve/merge PRs; output is advisory evidence only. [SUPUESTO]
- Cannot assert runtime, performance, or flakiness properties without execution evidence in `validation.commands_run`. [INFERENCIA]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty diff or no files | Produce a clean-review packet with scope evidence and no findings. |
| Missing line numbers | Block machine validation until each finding has a stable line. |
| Generated or vendored files | Exclude by default and record the exclusion. |
| High suspicion but weak evidence | Mark `needs-verification`, reduce confidence, avoid blocking priority. |
| Test status mentioned without commands | Mark validation `warn` or `block`; do not claim pass/fail. |
| User asks for broad refactor ideas | Separate advisory notes from review findings. |
| Binary, minified, or non-UTF8 file in scope | Exclude with reason; do not invent line-level findings. [INFERENCIA] |
| Diff too large to read fully | State coverage limit in `risks`; review highest-priority paths first, never claim full coverage. [SUPUESTO] |
| Secret/credential spotted in diff | Raise as `blocker`, do not echo the secret value in the report. [DOC] |
| File renamed/moved in diff | Cite the new path; note the rename so line numbers resolve against the post-diff file. [INFERENCIA] |
