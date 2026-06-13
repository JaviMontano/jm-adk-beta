# marketing-content — Overview

Router skill for marketing artifact production. It maps a single request to
exactly one of eight specialist playbooks, then runs that playbook along the
Discover → Analyze → Execute → Validate spine. It never produces the artifact
inline — routing is the whole job. [DOC]

## What it does

Resolves a `topic` (one of 8 enum values) and a `depth` (`quick`|`deep`), loads
**one** reference playbook, and executes it. The eight topics:

| Topic | Output | Playbook |
|-------|--------|----------|
| `case-study-writing` | Problem→Solution→Result client story | [references/case-study-writing.md](references/case-study-writing.md) |
| `content-calendar` | Pillar-mapped editorial calendar | [references/content-calendar.md](references/content-calendar.md) |
| `copywriting-frameworks` | Copy structured via AIDA/PAS/FAB/4Ps/BAB | [references/copywriting-frameworks.md](references/copywriting-frameworks.md) |
| `event-marketing` | Webinar/CFP/follow-up assets | [references/event-marketing.md](references/event-marketing.md) |
| `podcast-prep` | Run-of-show + show-notes brief | [references/podcast-prep.md](references/podcast-prep.md) |
| `press-release` | Inverted-pyramid release with `###` | [references/press-release.md](references/press-release.md) |
| `video-script` | Two-column shot list (VISUAL \| VO) | [references/video-script.md](references/video-script.md) |
| `whitepaper-creation` | Gated, citation-backed authority piece | [references/whitepaper-creation.md](references/whitepaper-creation.md) |

## When to use

Use when producing or revising a marketing artifact in one of the eight domains
above. [DOC]

Do NOT use for: brand voice/tone defaults, internal comms, or sales decks —
those are separate skills, and routing them here loads the wrong playbook. [INFERENCIA]

## How it routes and executes

1. Resolve `topic` from the request. If two topics plausibly fit (e.g. a launch
   that is both a `press-release` and an `event-marketing` follow-up), ask — a
   wrong route wastes the entire run. [INFERENCIA]
2. Read EXACTLY ONE playbook from `routes:` in `routes.json`. Never load the
   cluster "to compare". [CONFIG]
3. Execute Discover → Analyze → Execute → Validate. `depth=deep` applies the
   playbook exhaustively and verifies each step; `quick` covers essentials. [CONFIG]
4. Pass the playbook's own validation gate before returning.

## Governance

Evidence tags on every claim ([EXPLICIT] / [DOC] / [INFERENCIA] / [SUPUESTO]);
no invented prices; never green-as-success; single-brand per output (never mix
MetodologIA). Constitution v6.0.0 enforcement. [DOC]

## Bundle map

- `agents/` — role contracts (lead, specialist, support, guardian) for this router.
- `knowledge/` — routing body-of-knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — routing-decision + delegated-artifact scaffold.
- `evals/evals.json` — routing and governance test cases.
- `examples/` — a worked routing example end to end.
- `assets/` — quality rubric + routing checklist (see `assets/README.md`).
