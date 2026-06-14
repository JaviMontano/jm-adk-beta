# Assets — guardrails

Reusable, deterministic resources for producing and self-checking guard verdicts.
These are domain assets for the **guardrails** skill, not generic scaffolding.

## Bundle

- `quality-rubric.json` — weighted criteria a guard verdict must satisfy
  (single-playbook, fail-closed, evidence-tagged, no-green-by-default,
  script-first determinism, secret masking, aggregated violations, rule
  citation). Used by `SKILL.md` to anchor the acceptance bar and by `agents/guardian.md`
  as its gate definition.
- `checklist.md` — operational pre-emit checklist mirroring the rubric, used by
  `templates/output.md` authors and the guardian before any verdict ships.

## How to use

1. Before emitting a verdict, walk `checklist.md`; every blocker item must hold.
2. To score or audit a verdict, map it against `quality-rubric.json`; any failed
   blocker forces a non-pass.
3. Per-topic JSON policies (dangerous-command, token-pattern, gate-criteria,
   constitution principles) live alongside each playbook's own `assets/` in the
   upstream Alfa skills and are the single source of truth at execution time;
   this bundle governs the verdict's quality, not the topic policy itself.

## Manifest

`manifest.json` registers each asset with its type, purpose, and the existing
files that consume it. Every `used_by` target is a file that exists in this skill.
