# Dispatch Decision — session-workspace

> Router deliverable. Records how a session-lifecycle request was routed to a
> single playbook. The routed playbook owns its own artifact; this file records
> only the dispatch.

## 1. Request
- **Lifecycle moment (one line):** <restate the user's intent> [<tag>]
- **Repo / branch / brand:** <repo @ branch · brand> [CONFIG]

## 2. Topic resolution
- **Resolved topic:** `<one of the seven>` [<tag>]
- **Discriminator applied:** <the rule that selected this topic over the others> [<tag>]
- **Rejected candidates:** <topic — reason excluded> [<tag>]  *(omit if unambiguous)*
- **Clarifying question asked:** <question | none — intent was unambiguous> [INFERENCE]

## 3. Depth
- **depth:** `quick` | `deep` [CONFIG]
- **Effect:** quick = essentials · deep = exhaustive + per-step verification + full check.sh

## 4. Route loaded
- **Single route Read:** `references/<topic>.md` [CONFIG]
- **Siblings deliberately NOT loaded:** <list> [CONFIG]
- **Playbook deterministic resources surfaced:** `assets/*.json` policies · `scripts/check.sh` [CONFIG]

## 5. Anti-scope check
- [ ] No content authoring done by the router. [INFERENCE]
- [ ] No `.specify/context.json` write outside the `session-manager` route. [CONFIG]
- [ ] No multi-topic merge / fan-out. [INFERENCE]

## 6. Guardian decision
- **Decision:** `proceed` | `blocked` | `needs-confirmation` [DOC]
- **If not proceed — failing gate + evidence + corrective next step:** <...> [<tag>]

## 7. Handoff
- **Next action (handed to the playbook):** <concrete first step the routed playbook runs> [<tag>]
