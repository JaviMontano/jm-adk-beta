# Body of Knowledge — Official Source Verification

Domain knowledge for verifying a technical decision against authoritative documentation
before changing code, docs, or architecture criteria.

## Key concepts

- **Question**: the concrete decision that depends on external authority (e.g. "does
  `gh pr merge` delete the branch by default?"). If the decision does not depend on an
  external document, there is no official source to consult and the skill does not apply.
- **Source registry**: the typed list of every source consulted. Each entry carries
  `source_id`, `source_type`, `url`, `accessed_date`, `publisher`, `official`, and `role`.
- **Claim**: a single verifiable statement the decision rests on, mapped to
  `source_ids` and `official_source_ids`, with a `status` of `verified` or `unverified`.
- **Decision block**: `change_authorized`, `justified_change`, `scope`, `blocking_gaps` —
  the change a verified finding authorizes, and the gaps that block it.

## Source taxonomy

| Class | Examples | Role allowed |
|-------|----------|--------------|
| official | vendor canonical docs, Agent Skills spec, ADK reference, GitHub/Git official manuals, producer-owned SDK/API reference | authority (`verified` evidence) |
| secondary | blogs, StackOverflow/forum answers, GitHub issues/discussions, gists, tutorials, AI summaries | discovery `role=lead` only — never authority |

A secondary source may reveal a path or vocabulary that points to the official doc. It is
recorded with `official=false`, `role=lead`. It never becomes authority "because it agrees
with the official one" — in that case cite the official directly or not at all. [DOC]

## Priority order (decision rule)

**official > vendor > spec > repo > secondary.** Prefer the document closest to the
affected product. [INFERENCIA]

- When a generic **spec** is more correct than a vendor doc on a contested point,
  prioritize the spec and record the rationale (SKILL.md step 6).
- A genuine contradiction between two official sources is escalated to `blocking_gaps`,
  not resolved silently.

## Citation standard

- Every claim cites a `url`, an `accessed_date` in ISO `YYYY-MM-DD`, and a short
  extract/paraphrase of the relevant passage. [CONFIG]
- Without `accessed_date`, the claim cannot pass to `verified` — live docs change and the
  claim must be reproducible.
- A future or absent date is a self-correction trigger, not a warning.

## Version currency rule

If a doc states a version or date, confirm it applies to the version the repo uses. A doc
from a different major is `unverified` for the case at hand and is flagged as a version
conflict. [INFERENCIA]

## Decision authorization rule

`decision.change_authorized=true` only when every supporting claim is `verified`. A single
high-impact claim should seek a second official corroboration. Any open `blocking_gaps`
forces a status other than `pass`. The default posture under doubt is `unverified`:
blocking a correct change costs less than authorizing a false one. [SUPUESTO]

## Evidence taxonomy

Every registry entry, claim, and verdict carries a provenance tag: `[DOC]` for fetched
official text, `[CÓDIGO]`/`[CONFIG]` for local repo facts, `[INFERENCIA]` for version and
conflict reasoning, `[SUPUESTO]` for assumptions. A claim with no fetched text behind it is
`unverified` regardless of how confident the wording reads.

## Anti-patterns (out of scope)

- Elevating a secondary source to authority.
- Inferring a doc's stance without fetching the text.
- Resolving official-vs-official contradictions silently.
- Using the skill to validate local business logic, code style, or design opinions with no
  authoritative document behind them.
- Marking `pass` with open gaps under pressure to advance — green is not success by
  default.

The human pre-delivery list mirroring these rules is `assets/verification-checklist.md`;
the scored gate is `assets/quality-rubric.json`.
