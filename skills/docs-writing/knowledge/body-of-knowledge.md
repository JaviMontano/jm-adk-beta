# Body of Knowledge — docs-writing

Domain knowledge for the documentation and professional-writing router. Concepts,
standards, and decision rules the routed playbooks rely on. [DOC]

## 1. Core model: router + spine

`docs-writing` is a dispatcher, not a monolith. It resolves one `topic`, loads one
playbook, and runs a four-stage spine that every route shares:

- **Discover** — inventory source material; record gaps as `[SUPUESTO]`.
- **Analyze** — choose the approach; log the trade-off accepted, not just the winner.
- **Execute** — produce the artifact into the template; tag non-obvious claims.
- **Validate** — run the route's Quality Criteria; block on any unchecked item.

Mixing playbooks dilutes the spine and is an explicit anti-pattern. [INFERENCIA]

## 2. Key concepts and standards

### Diátaxis (documentation quadrants)

Four documentation kinds, each with a different shape: **tutorial** (learning-oriented),
**how-to** (task-oriented), **reference** (information-oriented), **explanation**
(understanding-oriented). Declaring the quadrant up front selects the template and the
audience expectation. Source of `documentation-standards` and `-system`. [DOC]

### Keep a Changelog + SemVer

Changelog entries group into Added / Changed / Deprecated / Removed / Fixed / Security.
SemVer bumps follow impact: breaking → MAJOR, feature → MINOR, fix → PATCH. Every
breaking change carries a before→after migration note. Drives `changelog-writing`. [CONFIG]

### OpenAPI 3.0

API reference is generated against the OpenAPI 3.0 shape: `info`, `servers`, `paths`
(verbs with `parameters`/`requestBody`/`responses`), `components.schemas`,
`components.securitySchemes`. Code-first generation resists drift; spec-first reads
cleaner but rots — pick one per surface. Drives `api-documentation`. [CÓDIGO]

### BLUF (Bottom Line Up Front)

Memos and status reports lead with the ask/decision in ≤2 sentences, before context. One
memo = one decision or one status. Every action item needs owner + deadline + done-
criteria. Drives `internal-memo`, `meeting-notes`, `reporting-templates`. [DOC]

### SemVer-for-docs and review cycle

Docs version like code: MAJOR = breaking restructure, MINOR = new guidance, PATCH =
clarification. Review cycle: draft → peer review → owner sign-off → published. Stale =
no update in 180 days. Drives `documentation-standards`. [DOC]

### Evidence taxonomy (Alfa core)

Every non-obvious claim carries one tag from a single family: `[CÓDIGO]` `[CONFIG]`
`[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Legacy playbooks may use `[EXPLICIT]`/`[INFERENCE]`
— never mix families in one document. When two tags apply, pick the weaker. Every
`[SUPUESTO]` is paired with the step that would confirm it. [DOC]

## 3. Decision rules

| Situation | Rule |
|-----------|------|
| Request maps to one topic | Load that playbook only; run the spine |
| Ambiguous between two topics | Ask one disambiguating question, then commit |
| Topic not in the enum | Stop; re-route from the request; never invent a topic |
| Compound request | Split into one run per route |
| Code vs README/CI conflict | Trust the drift-resistant source (code/CI); flag drift |
| Critical gap in source | Mark `[SUPUESTO]`; name the verifying step; do not fabricate |
| Price/cost requested | Refuse figures; express effort in FTE-months + disclaimer |
| Validate would fail | Block publish; never report green-as-success |

## 4. Governance constraints

Constitution v6.0.0: evidence tags on every non-obvious claim; script-first rule; no
invented prices; never green-as-success; no client PII; single brand per output. These
bind every route. [CONFIG]
