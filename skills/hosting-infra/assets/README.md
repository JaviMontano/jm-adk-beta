# assets/ — hosting-infra bundle

Reusable, skill-specific assets consumed by this skill's contracts. [EXPLICIT]

## Contents
- **`quality-rubric.json`** — pass/fail criteria for the validation gate: five
  blocking global criteria (single-playbook, topic-match, evidence-tags,
  no-invented-values, secrets-safe) plus per-topic criteria for all nine routes.
  Consumed by `agents/guardian.md` and referenced from `SKILL.md`.
- **`checklist.md`** — the per-invocation pre-flight + gate checklist run by the
  guardian/support agents along Discover → Analyze → Execute → Validate.
  Referenced from `README.md`.

## How it's wired
`manifest.json` records each asset's `path`, `type`, `purpose`, and `used_by`
targets. Every `used_by` target is an existing file in this skill. Update the
manifest whenever an asset is added or its consumer changes. [CONFIG]

## Governance
Assets carry no secrets, no invented hosts/IPs/prices, and stay single-brand. The
rubric never treats "green" as automatic success — each criterion needs cited
evidence. [DOC]
