# Official Source Verifier

Verify a technical decision against **official sources** before changing code, docs, or
architecture criteria. The skill ranks official documentation over secondary material
(blogs, forum answers, issues, gists, AI summaries), cites every claim with a URL plus an
ISO access date, records which change each finding justifies, and refuses to elevate a
secondary source to authority.

## What it does

- Builds a `source_registry` that tags every source as `official=true|false` with
  `source_type`, `publisher`, `url`, and `accessed_date`.
- Maps each `claim` to `official_source_ids`; a claim without an official source stays
  `unverified` and cannot authorize a change.
- Applies a fixed priority order — **official > vendor > spec > repo > secondary** — and
  records conflicts between official sources as `blocking_gaps` instead of resolving them
  silently.
- Emits a `decision` block (`change_authorized`, `justified_change`, `scope`,
  `blocking_gaps`) that ties the authorized change to verified evidence only.

## When to use it

- A decision depends on current ADK, Agent Skills spec, GitHub/Git, framework, SDK, API,
  or cloud documentation.
- A proposal cites a secondary source and you must confirm whether an official source
  backs it or contradicts it.
- A repo change needs a recorded official source that justifies the finding.
- Two official sources disagree and explicit prioritization is required.

**Do not use** for trivial local-code facts checkable with Read/Grep/Glob, or for design
opinions with no authoritative document behind them. See `SKILL.md` → "No la uses".

## How it routes / executes

1. **lead** frames the `question`, opens the `source_registry`, and sequences the loop.
2. **specialist** judges source authority, version currency, and conflict between official
   docs.
3. **support** runs `WebSearch` → `WebFetch` of the canonical doc and records citations.
4. **guardian** enforces the validation gate before the report is delivered.

Deterministic certification: when the deliverable is JSON, validate offline with
`scripts/validate_official_source_verifier.py`; run the full smoke with `scripts/check.sh`.

## References

- `SKILL.md` — capability, procedure, validation gate, self-correction triggers.
- `knowledge/body-of-knowledge.md` — source taxonomy, priority policy, citation standard.
- `knowledge/knowledge-graph.json` — concept graph over the verification model.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the verification report scaffold.
- `examples/` — a worked GitHub CLI verification case.
- `assets/` — contract, policies, and quality rubric used by SKILL.md and the guardian.

Governance: harness voice; evidence tags `[DOC] [CÓDIGO] [CONFIG] [INFERENCIA] [SUPUESTO]`
on every claim; no invented prices; green is never success by default; no client PII;
single brand (JM Labs).
