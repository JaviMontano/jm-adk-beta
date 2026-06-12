# Delivery Checklist — Prompt / Prompt-System

Run before delivering any prompt-and-meta-prompting output. Tag results
`[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]` `[ASSUMPTION]`.

## Structure

- [ ] Objective is single and testable. [DOC]
- [ ] Audience named. [DOC]
- [ ] Context, constraints, allowed tools, privacy boundaries captured or flagged
      `Dato requerido`. [DOC]
- [ ] Ordered task sequence present. [DOC]
- [ ] Output contract is an explicit shape (schema/template + minimal example). [DOC]
- [ ] Anti-drift rules embedded in the prompt text. [INFERENCE]
- [ ] Missing-data handling specified (placeholder | ask | stop). [DOC]

## Quality

- [ ] Acceptance criteria are verifiable, each mapped to a check. [DOC]
- [ ] Evals cover happy path, minimal input, conflicting requirements, false
      positive, unsafe injection. [DOC]
- [ ] Meta-prompt (if any) defines explicit review dimensions. [DOC]

## Safety

- [ ] No hidden chain-of-thought exposure. [DOC]
- [ ] No credential capture or unsafe automation. [DOC]
- [ ] No live PII or secrets in prompt or examples. [DOC]
- [ ] On safety/requirement conflict: Guardian block, `expected_activation: false`,
      no partial comply. [CONFIG]

## Evidence

- [ ] Every load-bearing claim carries an Alfa-core tag. [DOC]
- [ ] If a JSON report exists, `scripts/check.sh` is green and reported with its
      reason, not as bare success. [CODE]
