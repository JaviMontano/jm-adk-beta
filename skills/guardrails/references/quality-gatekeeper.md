<!-- distilled from alfa skills/quality-gatekeeper -->
<!-- Validates deliverables at JM-ADK quality gates G0-G3 using deterministic criteria, evidence tags, sequential gate order, score-history entry contracts, remediation, and fail-closed missing-evidence handling. Use before phase transitions, release decisions, `/jm:advance`, PR readiness, or any request asking whether a gate can pass. -->
# Quality Gatekeeper

Validate one artifact or release packet against JM-ADK G0-G3 quality gates. A
valid gate report evaluates every required criterion for the scoped gate(s),
uses evidence tags, blocks on failures or missing evidence, and emits a
score-history entry contract without mutating project state unless an
orchestrator explicitly requests a write. [EXPLICIT]

## Deterministic Assets

Use these local assets before producing or validating a report. They are the
single source of truth; this playbook only summarizes them. On any conflict
between this prose and an asset, the asset wins. [EXPLICIT]

| Path | Use |
|---|---|
| `assets/gate-criteria.json` | Canonical G0-G3 criteria, required evidence, and phase order |
| `assets/report-contract.json` | Required report sections, statuses, severities, and decision rules |
| `assets/evidence-policy.json` | Evidence tag vocabulary and assumption-ratio warning policy |
| `assets/score-history-schema.json` | Required score-history entry fields |
| `assets/activation-policy.json` | Activation and false-positive routing rules |
| `scripts/validate_gate_report.py` | Offline JSON gate report validator |
| `scripts/check.sh` | Deterministic fixture check for pass, block, and false-pass cases |

The validator reads only explicit local JSON paths. It does not call the
network, current time, model providers, MCP tools, or random sources — so two
runs over the same inputs always agree. This is intentional: gate decisions
must be reproducible and auditable, which forbids any nondeterministic input.
A criterion needing live data (e.g. a running emulator) is supplied as a
captured artifact, never fetched at validation time. [EXPLICIT]

**Assets missing or unreadable.** If a required asset is absent or invalid
JSON, do not improvise the criterion list from memory: stop and return
`needs_evidence` naming the missing asset. Fabricating criteria defeats the
determinism guarantee. [INFERENCE]

## When To Activate

Activate for JM-ADK quality gate decisions, phase transitions, `/jm:advance`,
release readiness, PR gate readiness, score-history entry validation, or
requests asking whether G0, G1, G2, or G3 can pass. [EXPLICIT]

Do not activate for:

- generic writing quality review without JM-ADK gate scope
- generic CI log explanation unless the user asks for a G0-G3 decision
- Lighthouse-only audits; route to performance/accessibility skills unless tied
  to G3
- creating or editing the Constitution; route to constitution workflows
- human role assignment such as "find a gatekeeper"

## Required Inputs

At least one artifact or explicit missing-evidence statement is required.
[EXPLICIT]

| Input | Rule |
|---|---|
| `gate_id` | `G0`, `G1`, `G2`, `G3`, or a scoped list; if absent, infer from artifact type and mark inference |
| `source_stage` | Current phase before transition; used to enforce sequential gate order |
| `target_stage` | Requested phase after gate approval |
| `artifacts` | Files, PR checks, reports, commands, or user-provided evidence |
| `score_history` | Existing entry when re-evaluating; otherwise emit a proposed `score_history_entry` |

If required evidence is absent, mark the criterion `not_verified`. Never mark a
criterion `pass` from silence — this is the core fail-closed invariant: absence
of a failure signal is not a pass. [EXPLICIT]

**Assumptions about inputs.** Artifacts are trusted as supplied; the gatekeeper
does not re-run tests or re-scan code, it evaluates the evidence presented. A
green check whose log is not attached is `not_verified`, not `pass` — a claim
is only as strong as its attached evidence. If `gate_id` is inferred, the
report header states the inference and its basis. [ASSUMPTION]

## Gate Process

1. Load `assets/gate-criteria.json`, `assets/report-contract.json`,
   `assets/evidence-policy.json`, and `assets/score-history-schema.json`.
2. Identify the requested gate(s) and enforce order `G0 -> G1 -> G2 -> G3`.
3. Evaluate every required criterion for each scoped gate.
4. Require evidence tags on every factual criterion row.
5. Classify criterion status as `pass`, `fail`, `not_verified`, or
   `not_applicable`.
6. Block advancement when any required criterion is `fail` or `not_verified`.
7. Add remediation for every `fail` or `not_verified` criterion.
8. Emit a score-history entry contract with gate, branch/commit when available,
   evidence summary, blocked flag, decision, and evaluator.
9. If a JSON report is available, run `scripts/validate_gate_report.py` before
   final delivery.

## Gate Criteria Summary

| Gate | Required Criteria | Pass Condition |
|---|---|---|
| G0 Pre-flight | secrets scan, branch isolation, Constitution compliance | zero blocking findings |
| G1 Analysis | spec complete, evidence tags, stakeholder/checklist coverage | all analysis artifacts evidenced |
| G2 Architecture | data model, API/contracts, security rules, BDD traceability, design tokens | architecture evidence complete |
| G3 Deploy-ready | tests, Lighthouse >= 90, emulator/security checks, accessibility audit, brand voice/monitoring | all release checks green |

Use `assets/gate-criteria.json` as the canonical criterion list. The four rows
above are a memory aid, not the contract; never evaluate from them alone. [EXPLICIT]

## Worked Example

Request: "Can G2 pass? source `analysis`, target `architecture`." Artifacts:
data-model.md, openapi.yaml; no security-rules file; BDD specs present but
untraceable to scenarios; design tokens attached. [EXPLICIT]

Evaluation (per `gate-criteria.json` G2 rows):

| Criterion | Status | Evidence | Remediation |
|---|---|---|---|
| data model | `pass` | data-model.md [DOC] | — |
| API/contracts | `pass` | openapi.yaml [DOC] | — |
| security rules | `not_verified` | no file supplied [ASSUMPTION] | add firestore.rules + test |
| BDD traceability | `fail` | specs present, no scenario IDs [DOC] | map each spec to a scenario ID |
| design tokens | `pass` | tokens.json [DOC] | — |

Decision: **block**. `overall_status: blocked` (one `fail`, one `not_verified`).
Severities: BDD `P1`, security rules `P1`. `assumption_ratio` = 1/5 = 0.20, below
0.30, no banner. Proposed `score_history_entry`: `{gate: G2, blocked: true,
decision: block, not_verified_count: 1, evaluator: quality-gatekeeper}`. No
project state written. Note the contrast: three `pass` rows do NOT yield "mostly
pass" — a single `fail` or `not_verified` blocks the whole gate. [EXPLICIT]

## Report Contract

Every report must include: [EXPLICIT]

1. Summary with `gate_scope`, `source_stage`, `target_stage`,
   `overall_status`, `blocking_findings`, `not_verified_count`,
   `assumption_ratio`, and confidence.
2. Gate results for all scoped gates.
3. Criterion results for every required criterion in scoped gates.
4. Violations table.
5. Missing evidence table.
6. Remediation plan.
7. Proposed `score_history_entry`.
8. Decision: `allow`, `block`, or `needs_evidence`.
9. Caveats and explicit assumptions.

## Validation Gate

- [ ] Gate scope is explicit.
- [ ] Sequential gate order is checked.
- [ ] Every required criterion for scoped gates is represented exactly once.
- [ ] Every `pass` row has tagged evidence.
- [ ] Every `fail` row has severity and remediation.
- [ ] Every `not_verified` row lists missing evidence and remediation.
- [ ] Overall status is `blocked` when required criteria fail or are missing.
- [ ] Assumption ratio above 0.30 emits a warning banner.
- [ ] Score-history entry includes required fields.
- [ ] No external network, clock, or random value is needed to validate the
  report.

## Severity Policy

| Severity | Meaning | Delivery Decision |
|---|---|---|
| `P0` | Secret, security, data integrity, or forbidden stack breach | Block |
| `P1` | Required gate criterion failed, missing, or out-of-sequence | Block |
| `P2` | Important gap with bounded workaround outside the current gate | Conditional |
| `P3` | Low-risk wording or documentation gap | Warn |
| `none` | Criterion passes or does not apply | Allow |

## Key Decisions and Trade-offs

- **Fail-closed over fail-open.** Missing evidence blocks rather than waves
  through. Trade-off: more false blocks (annoying) but zero silent gate
  bypasses (dangerous). A blocked gate is recoverable by attaching evidence; a
  falsely-passed gate ships the defect. [INFERENCE]
- **Stateless by default.** No write unless explicitly permitted. Trade-off:
  the orchestrator must do a second step to persist, but the gatekeeper can
  never corrupt `.specify/score-history.json` on a dry run or a misread. [EXPLICIT]
- **Assets as source of truth, prose as summary.** Trade-off: this file can
  drift from the JSON; mitigated by the "asset wins" rule and `check.sh`
  fixtures that pin behavior. [INFERENCE]
- **Binary gate, no partial credit.** One `fail`/`not_verified` blocks the
  gate. Trade-off: loses nuance ("90% ready") but removes the judgment call
  that lets borderline work advance. [EXPLICIT]

## Edge Cases and Failure Modes

- **G3 requested before G1:** block with a sequential gate violation (`P1`),
  even if all G3 artifacts look complete — order is non-negotiable. [EXPLICIT]
- **Skipped intermediate gate (G0+G2, no G1):** block; G1 is a prerequisite,
  not optional. Report the gap as out-of-sequence. [INFERENCE]
- **No files or docs yet:** return `not_verified` for each criterion, not
  `pass`, and overall `needs_evidence`. [EXPLICIT]
- **Partial green checks:** block the gate; no "mostly pass" language. [EXPLICIT]
- **Assumption-heavy report:** if more than 30% of criterion evidence is
  `[ASSUMPTION]`, add a warning banner and avoid `allow`. The ratio counts
  criterion rows, not sentences. [EXPLICIT]
- **Lighthouse 90 exactly:** passes (`>= 90`); 89 fails. Boundary is inclusive. [EXPLICIT]
- **Score-history file absent:** emit a valid proposed entry; do not invent that
  it was written or assume prior scores. [EXPLICIT]
- **Conflicting evidence (passing test log + failing CI badge):** take the
  stricter signal; classify `fail` and cite both. Never average. [INFERENCE]
- **Duplicate criterion rows:** each required criterion appears exactly once; a
  duplicate is a malformed report, not extra confidence — flag it. [EXPLICIT]
- **Explicit write request:** only update `.specify/score-history.json` after
  the user/orchestrator permits writes AND a valid report exists. A write with
  an invalid report is refused. [EXPLICIT]
- **Stale source_stage (claims `architecture` but no G1 record):** treat the
  unproven prior gate as `not_verified`; do not assume earlier gates passed. [ASSUMPTION]

## Reference Files

| File | Content | Load When |
|---|---|---|
| `assets/gate-criteria.json` | G0-G3 criteria and sequence | Always |
| `assets/report-contract.json` | Report schema and decision rules | Always |
| `assets/evidence-policy.json` | Evidence tags and warning thresholds | Always |
| `assets/score-history-schema.json` | Score-history entry requirements | When emitting score history |
| `scripts/check.sh` | Fixture-backed deterministic check | When local scripts can run |

---
**Author:** Javier Montano | **Last updated:** 2026-06-11
