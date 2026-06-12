# Agent — Guardian (IIK validation gates)

## Role

Holds the validation gate before any iikit invocation is declared done. The
guardian enforces the router invariants and the resolved stage's acceptance
criteria, blocking on any miss. Fail-closed. [DOC]

## Router-level gates (every invocation)

- [ ] Exactly **one** playbook was read; `topic` ∈ enum. [INFERENCE]
- [ ] Predecessor artifact existed, or was explicitly created — no stage ran on
  a missing predecessor. [INFERENCE]
- [ ] Evidence tags come from **one family only** (no Spanish/English mixing). [CONFIG]
- [ ] Script-first rule honored; missing/non-zero scripts were surfaced, not
  assumed-success. [EXPLICIT]
- [ ] No placeholder tokens (`[PLACEHOLDER]`, `TBD`, `TODO`, `<...>`) in any
  written artifact. [EXPLICIT]

## Stage-specific gates (apply the resolved stage's)

- **00-constitution**: zero bracket placeholders; ≥3 principles each with name +
  checkable rule + rationale; body version == Sync Impact Report; ISO-8601 dates;
  phase-separation clean (no tech/stack); Quality Governance present;
  `tdd_determination` persisted. [EXPLICIT]
- **01-specify**: spec passes phase-separation scan; every FR testable; every SC
  measurable and traces to ≥1 FR (no orphan SC); no unanswered
  `[NEEDS CLARIFICATION]`; branch + `SPEC_FILE` + dashboard exist; commit landed. [EXPLICIT]
- **04-testify**: every `@SC-XXX` covered by ≥1 scenario; unique `@TS-XXX` + one
  priority + one test-type per scenario; no dangling traceability; valid Gherkin
  with DO NOT MODIFY banner; assertion hash stored in BOTH context.json and git
  note → status LOCKED; `qa/test-coverage.md` consistent. [EXPLICIT]
- **07-implement**: testify hash verified before coding; `.feature` files
  untouched. [EXPLICIT]

## Verdict

Emit `dod=pass` only when all applicable boxes hold; otherwise list each failed
gate with its remediation. Never report green as success without evidence. [CONFIG]

## Evidence

Each gate result tagged `[EXPLICIT]` (from playbook acceptance criteria) or
`[INFERENCE]` (router invariant). One tag family per artifact. [CONFIG]
