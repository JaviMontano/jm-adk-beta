# Routing checklist — architecture

Run before producing any deliverable. All boxes must hold. [DOC]

## Resolve the topic
- [ ] Mapped the request to EXACTLY one `topic` in the enum
      (`api-design`, `caching-strategy`, `domain-driven-design`,
      `event-architecture`, `migration-planning`, `performance-architecture`,
      `realtime-architecture`, `system-architecture`, `trade-off-analysis`).
- [ ] If ambiguous between two topics → asked one sharp question, did NOT guess.
- [ ] If the request spans topics → picked the dominant one, will chain the
      second invocation, did NOT merge playbooks.

## Load
- [ ] Read EXACTLY one file from `routes:`.
- [ ] Did NOT load a second playbook "to be safe".

## Depth
- [ ] Set `depth` (`quick` default | `deep`).
- [ ] If `quick`, will name what is skipped.

## Common mis-routes to avoid
- [ ] Contract shape (versioning/pagination/errors) → `api-design`, not
      `system-architecture`.
- [ ] Read-traffic relief → `caching-strategy`, not `performance-architecture`
      (unless the bottleneck is broader).
- [ ] Service boundaries / ubiquitous language → `domain-driven-design`, not
      `system-architecture`.
- [ ] Contested, hard-to-reverse choice → `trade-off-analysis`, then chain.

## Before done
- [ ] Acceptance gate in `assets/quality-rubric.json` passes.
- [ ] No invented prices; no client PII; single brand.
