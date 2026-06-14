<!-- distilled from alfa skills/constitution-compliance -->
<!-- Validates outputs, plans, PRs, reports, or workflows against JM-ADK Constitution v7.0.0 using an 11-principle matrix, G0-G3 gate impact, evidence tags, severity, remediation, and fail-closed missing-evidence handling. Use when the user asks for constitution compliance, constitutional audit, Pristino governance validation, pre-delivery compliance, or whether an artifact violates JM-ADK principles. -->
# Constitution Compliance

Validate an artifact against JM-ADK Constitution v7.0.0. A valid compliance
report covers all 11 principles, maps findings to G0-G3 gates, classifies
severity, requires remediation for every failure, and treats missing evidence as
`not_verified` rather than a pass. [EXPLICIT]

**Core invariant — fail closed:** silence is never a pass. Absent artifact,
absent evidence, or absent gate context downgrades the affected rows to
`not_verified` and the overall status away from `pass`. [EXPLICIT]

## Deterministic Assets

Load these local assets before producing a report; the report's machine claims
must trace to them, not to model recall. [EXPLICIT]

| Path | Use | Load |
|---|---|---|
| `assets/constitution-v7-principles.json` | Canonical 11-principle map + G0-G3 gates, derived from `references/ontology/constitution-v7.0.0.md` | Always |
| `assets/compliance-report-contract.json` | Required sections, status enum, evidence tags, blocked phrases | Always |
| `assets/severity-policy.json` | P0-P3 severity mapping and gate-impact rules | Always |
| `assets/activation-policy.json` | Activation, false-positive, version-drift, missing-evidence rules | When deciding to activate or to suppress a finding |
| `references/ontology/constitution-v7.0.0.md` | Canonical v7.0.0 text + v6.0.0 crosswalk | When verifying source text or version drift |
| `scripts/validate_constitution_report.py` | Offline JSON report validator | When a JSON report exists |
| `scripts/check.sh` | Positive + negative fixture check | When local scripts can run |

The validator reads only explicit local JSON files. It does not call the
network, current time, model providers, MCP tools, or random sources; a report
that depends on any of those is itself non-compliant. [EXPLICIT]

## When To Activate

Activate for constitutional audits, pre-delivery checks, Pristino governance
validation, gate compliance, evidence-tag checks, or requests asking whether an
artifact violates the JM-ADK Constitution. [EXPLICIT]

Do **not** activate for (anti-scope):

- viewing or amending the Constitution itself — route to `/jm-adk:constitution`
- creating an agent constitution — route to `agent-constitution-creator`
- generic legal or political constitution questions
- generic quality review without JM-ADK/Pristino governance scope — route to a
  quality-review skill

**Boundary case:** a request that mixes governance audit with editing the
Constitution audits here, then hands the edit to `/jm-adk:constitution`; do not
silently amend canon from within an audit. [INFERENCE]

## Required Inputs

At least one input must be explicit. [EXPLICIT]

| Input | Rule |
|---|---|
| `artifact` | Text, path, PR summary, report, workflow, plan, or implementation output to audit. Required; if absent → `not_verified`, do not proceed. |
| `gate` | Optional `G0`/`G1`/`G2`/`G3`; if absent, infer from artifact type and tag the inference `[INFERENCE]`. |
| `evidence_sources` | Files, command outputs, review docs, or an explicit statement that evidence is missing |
| `claim_tag_policy` | Repo tags `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, `[ASSUMPTION]`; Spanish tags allowed only in user-facing summaries, never in the matrix |

Gate inference defaults (when `gate` absent): plan/spec → `G0`; PR/code/impl
output → `G1`; report/delivery artifact → `G2`; release/sign-off → `G3`. Tag
each as `[INFERENCE]` and let the owner override. [ASSUMPTION]

If the artifact or evidence sources are missing, return `not_verified` findings
and name the missing input. Never mark a principle `pass` from silence. [EXPLICIT]

## Compliance Process

1. Confirm the target Constitution version is v7.0.0. If the artifact cites
   v6.0.0, classify as version drift (P1) and audit via the v6.0.0 crosswalk. [EXPLICIT]
2. Load the three Always assets plus `activation-policy.json`. [EXPLICIT]
3. Inspect the artifact and evidence sources. Cite file paths, command output,
   or explicit user statements — every factual matrix claim carries a tag. [EXPLICIT]
4. Produce one matrix row per principle, status
   `pass|fail|not_verified|not_applicable`. Exactly 11 rows, each principle once.
5. For every `fail`: severity, gate impact, evidence, remediation (all non-empty).
6. For every `not_verified`: the missing evidence and the next command, file, or
   decision that would resolve it.
7. Block delivery when any P0/P1 failure exists, or when a required gate has
   `not_verified` evidence. [EXPLICIT]
8. If a JSON report exists, run `scripts/validate_constitution_report.py` before
   delivery; a validator failure blocks regardless of matrix status.

**False-positive control:** before raising a finding, confirm the principle
actually applies to this artifact type (per `activation-policy.json`). A
principle that cannot apply is `not_applicable` with a one-line reason — not a
`fail`. Over-flagging erodes trust as much as under-flagging. [INFERENCE]

## Report Contract

Every report includes, in order: [EXPLICIT]

1. Constitution version `v7.0.0`.
2. Artifact description and audit gate (mark if inferred).
3. Overall status: `pass`, `blocked`, or `not_verified`.
4. Matrix with all 11 principles.
5. G0-G3 gate impact.
6. Violations table.
7. Missing-evidence table.
8. Remediation plan.
9. Decision and confidence.
10. Explicit caveats.

**Overall-status resolution (apply top-down, first match wins):** [EXPLICIT]

| Condition | Overall status |
|---|---|
| Any P0 or P1 `fail` present | `blocked` |
| Any required-gate evidence is `not_verified` | `not_verified` |
| Only P2/P3 gaps, all evidence present | `pass` (with caveats) |
| All 11 `pass` / `not_applicable`, evidence complete | `pass` |

## Severity Policy

| Severity | Meaning | Delivery |
|---|---|---|
| `P0` | Security, secret, data-integrity, or hard constitutional breach | Block |
| `P1` | Gate-blocking missing evidence, stale version, broken process, or false pass | Block |
| `P2` | Important compliance gap with a bounded workaround | Conditional |
| `P3` | Low-risk documentation or wording gap | Warn |
| `none` | Principle passes or does not apply | Allow |

Severity is set by impact, not by how many principles a finding touches: one P0
blocks even if 17 principles pass. [EXPLICIT]

## Validation Gate

Checklist the report must satisfy before delivery (superset of the contract;
each item is independently checkable): [EXPLICIT]

- [ ] Constitution version is `v7.0.0`; no stale `v6.0.0` target except as a drift finding.
- [ ] All 11 principles represented exactly once.
- [ ] Every row has status, evidence, severity, remediation, and gate impact.
- [ ] Every `fail` row has non-empty remediation.
- [ ] Every `not_verified` row names the missing evidence and the next step.
- [ ] Overall status `blocked` when any P0/P1 failure is present.
- [ ] Overall status not `pass` when required evidence is missing.
- [ ] G0-G3 impact is explicit.
- [ ] Evidence tags appear on every factual claim.
- [ ] No blocked phrase from `compliance-report-contract.json` appears.

## Worked Example

Audit input: a PR summary claiming "added auth, tests green" with no test log
attached; `gate` absent. [INFERENCE]

- Gate inferred `G1` (PR/code) → tagged `[INFERENCE]`.
- Principle "evidence-backed claims": test log not provided → `not_verified`;
  missing evidence = CI output or `scripts/check.sh` run; next step = attach log.
- Principle "no secrets in output": PR diff not provided → `not_verified`, not
  `pass` (cannot confirm absence from silence).
- Overall status `not_verified` (required-gate evidence missing), not `blocked`
  and never `pass`. Remediation: attach CI log + diff, re-audit.

## Edge & Failure Cases

- **Artifact cites v6.0.0:** audit against v7.0.0, raise a version-drift finding (P1).
- **Missing artifact:** `not_verified`, not `pass`; request the artifact.
- **Partial evidence:** mark only evidenced principles `pass`; the rest `not_verified`.
- **Conflicting requirements:** map each conflict to its principles and require an
  owner decision; do not auto-resolve.
- **Non-JM-ADK constitution question:** decline and route to a generic/legal skill.
- **Asset missing or unreadable:** treat as a process failure (P1) — cannot audit
  deterministically without the canonical map; report the missing asset, do not
  improvise the principle list from memory. [INFERENCE]
- **JSON report fails the validator but matrix looks clean:** trust the validator;
  status `blocked` until the schema error is fixed. [EXPLICIT]
- **Green-but-unverified:** a "green" or "all clear" claim without evidence is a
  P1 false-pass, not a `pass`. [EXPLICIT]

---
**Author:** Javier Montano | **Last updated:** 2026-06-11
