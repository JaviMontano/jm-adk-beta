# ai-quality — Routing & Execution Record

> Deliverable scaffold for the `ai-quality` router. Fill every section. The
> Routing Decision and Validation Gate sections are mandatory; the Deliverable
> body follows the resolved playbook's own contract.

## 1. Request summary
- **Request (verbatim or paraphrased):** <what the user asked>
- **Artifact under review:** <diff / model output / spec / pipeline / content / workflow>
- **Stakes / reversibility:** <low-reversible | high-irreversible>  [CONFIG]

## 2. Routing decision
| Field | Value | Tag |
|-------|-------|-----|
| Resolved `topic` | `<one enum value>` | [CÓDIGO] |
| `depth` | `quick` \| `deep` | [CONFIG] |
| Playbook read | `references/<topic>.md` (exactly one) | [CÓDIGO] |
| Justification | <one line: why this topic> | [INFERENCIA] |
| Rejected near-collision | <other topic considered + why rejected> | [INFERENCIA] |

## 3. Spine execution
- **Discover:** <inputs gathered, baselines/scope, gaps recorded>  [CÓDIGO]
- **Analyze:** <method/oracle/metric/severity/control choice + trade-off>  [INFERENCIA]
- **Execute:** <the deliverable — see §4>
- **Validate:** <see §5>

## 4. Deliverable (per resolved playbook contract)
> Use the resolved playbook's required shape. Examples of the body:
> - code review → findings table (id, severity, category, file, line, claim,
>   evidence_tag, remediation) + decision.
> - llm-evaluation → metric, baseline, score, judge config, spot-check result.
> - ai-safety → risk → control → jailbreak → metric chain (no orphan ids).
> - ai-testing-strategy → 6×6 matrix with per-cell verdict.
> - ai-documentation → evidence-mapped sections + drift findings.
> - ai-workflow-automation → gated plan with contracts and bounded retries.

<deliverable body here>

## 5. Validation gate
- [ ] Resolved topic ∈ enum; exactly one playbook read.  [CÓDIGO]
- [ ] One Alfa tag family throughout; no `[CÓDIGO]` without an in-repo referent.  [DOC]
- [ ] `depth` honored (deep verified each step; quick stayed essential).  [CONFIG]
- [ ] Topic acceptance criteria met (list the topic-specific checks).  [CÓDIGO]
- [ ] `scripts/check.sh` ran offline (if present): result `<pass|warn|block>`.  [DOC]
- **Gate verdict:** `pass` \| `warn` \| `block`  [DOC]

## 6. Risks & limits
- <residual risk; a passing check is well-formedness, NOT a safety/correctness guarantee>  [INFERENCIA]
- <coverage limits, assumptions, items needing human review>  [SUPUESTO]
