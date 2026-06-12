# Assets: email-comms

Reusable, machine- and human-readable assets that support the email-comms
router. [DOC]

## Contents

- **`quality-rubric.json`** — weighted scoring rubric across five dimensions
  (routing correctness, deliverability, render fidelity, content/measurement,
  evidence governance). Used by `agents/guardian.md` to grade a run and by
  `evals/evals.json` cases that assert `quality_criteria`.
- **`routing-checklist.md`** — pre-flight checklist that enforces one topic per
  run, prerequisite sequencing, and the deliverability-vs-content diagnosis.
  Used by `prompts/primary.md` and the lead agent at topic-resolution time.
- **`manifest.json`** — declares each asset, its type, purpose, and which
  existing skill files consume it.

## How to use

1. At routing time, run `routing-checklist.md` to lock exactly one topic.
2. At the Validate gate, score the deliverable against `quality-rubric.json`;
   `pass` requires every dimension at `pass` (or justified `partial`).

All assets follow the Alfa core EN evidence taxonomy and single-brand rule. [DOC]
