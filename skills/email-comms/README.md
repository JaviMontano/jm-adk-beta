# email-comms

Router skill for email systems and communication. It resolves a single `topic`
and reads exactly one playbook, so the model never loads the whole cluster "to
be safe." [DOC]

## What it does

Covers four distinct email concerns, each with its own playbook under
`references/`:

- **email-sending** — provider/transactional infrastructure: SendGrid / Mailgun
  / SES setup, SPF/DKIM/DMARC domain auth, bounce/complaint handling, one-click
  unsubscribe, idempotent queued sends. [DOC]
- **email-template-builder** — authoring new responsive HTML: table layout,
  inline CSS, 600px max-width, `firestore-send-email` (Firebase Extensions)
  trigger. [CODE]
- **email-templates** — bulletproof layout patterns across Outlook (Word
  engine), Gmail, Apple Mail; MJML/Maizzle toolchain, fluid-hybrid responsive,
  dark mode. [DOC]
- **newsletter-design** — content architecture (single-feature / digest /
  editorial), subject+preheader pair, engagement metrics (open / CTR / CTOR),
  cadence and list hygiene. [DOC]

## When to use

Any email task: wiring a provider to send, building or picking an HTML template,
or designing a recurring newsletter. NOT for in-app messaging, push, or SMS —
those route elsewhere. [INFERENCE]

## How it routes

1. Map the request to one `topic` enum value. If it maps to two, run the
   prerequisite first: builder → templates → sending; newsletter-design hands
   its layout to email-template-builder. [INFERENCE]
2. Read ONLY that route's playbook (`routes:` in `SKILL.md` / `routes.json`).
3. Set `depth`: `quick` = essentials, `deep` = exhaustive with per-step
   verification.
4. Run the playbook spine: Discover → Analyze → Execute → Validate. [DOC]

If the topic is ambiguous, ask one question — an unresolvable topic is
stop-and-ask, never an [ASSUMPTION]. [DOC]

## References

- `references/email-sending.md`
- `references/email-template-builder.md`
- `references/email-templates.md`
- `references/newsletter-design.md`
- `routes.json` — machine-readable route table

## Bundle

- `agents/` — lead, specialist, support, guardian role contracts for this skill.
- `knowledge/` — body of knowledge + concept graph for email comms.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — scenario suite.
- `examples/` — a worked transactional-sending example.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).

## Evidence taxonomy

Alfa core EN only: `[DOC]` `[INFERENCE]` `[CODE]` `[CONFIG]` `[ASSUMPTION]`.
Never mix the Jarvis `{…}` tag family. [DOC]
