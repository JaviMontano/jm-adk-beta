# ADR-0001 — ICM first-prompt routing on the harness (runtime, not adapter)

- **Date:** 2026-08-02
- **Status:** Accepted
- **Sources:** ICM paper (notebook 13845882 §3.2), harness-engineering (notebook c94c6afa), local context-management-wiki `05-orquestacion/router.md`
- **Evidence:** [DOC] [CONFIG]

## Context

The `jm-adk-beta` harness is a thin, catalog-driven, generated adapter. From a
vibe-coder's first prompt it gave no deterministic create-vs-resume / new-vs-ongoing
routing — the model explored the filesystem (anti-pattern "blind searching", notebook 2).
A `docs/pristino-beta/prompt-parametrico-empezar.md` parametric prompt existed but had to
be pasted manually.

## Decision

Add an **ICM Layer-1 routing layer as RUNTIME behavior** (not adapter structure):

1. `scripts/first-prompt-router.sh` — deterministic, read-only, inspects
   `.jm-adk.json` + `workspace/.workspace-registry.json` + `tasks/T-NNN`, emits
   `ROUTE-*` KEY:VALUE. Reuses `task-subfolder` convention P33.
2. `scripts/workspace-bootstrap.sh` — instantiates `workspace/<id>/` from
   `workspace/_template/` (ICM Layer-2 stage contracts `01_discovery`..`04_validate`).
3. `runtime/delta-claude.md` — canonical source for the first-turn block protocol
   (ENTENDIDO/MODO/SUPUESTOS/GAPS/PERFIL/SKILL/TAREA/GATE). Regenerated into
   `CLAUDE.md`/`AGENTS.md` — **never hand-edited**.
4. `scripts/session-init.sh` invokes the router; `scripts/stop-validator.sh` is the
   SENSOR that vetoes (exit 1) when the block is absent from the transcript.
5. Gate `--phase p6` in `check-prerequisites.sh`.

## Consequences

- Anti-scope respected: routing is runtime behavior (delta + hooks + scripts), not
  building the adapter generator.
- Edit-source principle (ICM): routing misbehavior is fixed in the script/delta,
  not in outputs.
- Sensor enforces the vibe-coder-ally contract (explicit understanding, assumptions,
  gaps) on every session, automatically — no manual prompt paste.
- Lost-in-the-middle mitigated: stages load 2-8k tok, not whole workspace.

## Rejected alternative

Hand-editing `CLAUDE.md` with a Triggers table (v1 plan) — **rejected**: violates the
generated-adapter contract ("Do NOT hand-edit — regenerated on every build").