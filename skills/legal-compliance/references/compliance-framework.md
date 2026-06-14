<!-- distilled from alfa skills/compliance-framework -->
<!-- > -->
# Compliance Framework
> "Method over hacks."
## TL;DR
Checklist patterns + evidence mapping for SOC2, ISO 27001, and GDPR. Turns a
control requirement into a verifiable artifact, not a claim. [DOC]

## Scope & anti-scope
- IN: control-to-evidence mapping, gap surfacing, audit-readiness checks. [DOC]
- OUT: legal sign-off, certification issuance, penetration testing, DPIA
  authoring — those need a domain expert or auditor. [SUPUESTO]
- Not a substitute for the certifying body's own audit. [DOC]

## Procedure
### Step 1: Discover — scope the assessment
- Identify framework(s) in play, the entity/system boundary, and the audit
  window. Pull existing policies, configs, and prior audit reports. [DOC]
### Step 2: Analyze — map controls to evidence
- For each control, record: status (met/partial/gap), evidence pointer, owner.
- Evaluate options per Constitution XIII/XIV; flag conflicts, don't resolve
  silently. [INFERENCIA]
### Step 3: Execute — produce the artifact
- Emit a control table with one row per control; tag every status claim with
  its evidence source. A control with no checkable pointer is a gap. [INFERENCIA]
### Step 4: Validate — confirm audit-readiness
- Re-check every "met" row has a real, locatable artifact before sign-off. [DOC]

## Framework evidence anchors (worked examples)
| Framework | Sample control | Acceptable evidence |
|-----------|----------------|---------------------|
| SOC2 (CC6.1) | Logical access controls | IAM policy export + access-review log [CONFIG] |
| ISO 27001 (A.8) | Asset inventory | Versioned asset register + owner field [CONFIG] |
| GDPR (Art.30) | Records of processing | RoPA doc covering every processing activity [DOC] |

## Quality Criteria
- [ ] Every control row carries a status AND an evidence pointer [DOC]
- [ ] No "met" status without a locatable artifact (else downgrade to gap)
- [ ] Evidence tags applied; tag family consistent (Alfa core set) [DOC]
- [ ] Constitution-compliant; conflicts flagged not buried
- [ ] Actionable output (gaps have an owner + next step)

## Failure modes
| Mode | Symptom | Mitigation |
|------|---------|------------|
| Evidence theater | "Met" with no artifact | Force a locatable pointer per row [INFERENCIA] |
| Stale evidence | Artifact predates audit window | Check artifact date vs window in Step 4 [SUPUESTO] |
| Framework drift | Control IDs from wrong version | Pin framework version in Step 1 [DOC] |
| Silent conflict | Two controls demand opposites | Flag explicitly, escalate to owner [DOC] |

## Usage

Example invocations:

- "/compliance-framework" — Run the full compliance framework workflow
- "compliance framework on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs); missing access is
  a `[SUPUESTO]` to confirm, not a met control. [DOC]
- Requires English-language output unless otherwise specified [DOC]
- Single-framework version per run; mixing versions invalidates control IDs [SUPUESTO]
- Does not replace domain expert / auditor judgment for final decisions [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No evidence for a control | Record as gap with owner; never mark met |
