# Deep Variation — Runtime Routing (full evidence pass)

For ambiguous, multi-capability, or cross-runtime-portable tasks where the
capability boundary must be made explicit.

## Expanded procedure

1. **Inventory** — Enumerate every required capability and split model-capability
   (multimodal, large-context) from repo-capability (adapters, MCP, scripts).
2. **Evidence sweep** — Grep/Read `AGENTS.md`, `CODEX.md`, `.agent/`, MCP config,
   and scripts. For each capability per candidate runtime, record:
   `{capability, runtime, status, evidence_id|null, source}`.
3. **Promote / downgrade** — Promote to `supported` only with a `[DOC]`/`[CONFIG]`/
   `[CÓDIGO]` id. Downgrade any `supported` row lacking one to `validation pending`.
4. **Filter & rank** — Keep runtimes whose required capabilities are all
   `supported`; rank by permission level from `assets/runtime-catalog-policy.json`;
   tie → local + Markdown.
5. **Cross-runtime portability** — If output must stay portable, state which
   capabilities survive on each runtime and which become pending elsewhere.
6. **Fallback design** — Build the local-first fallback: Markdown-first +
   repo-local scripts, no-`gh`-auth path, `Dato requerido` / `validation pending`
   markers, secret-boundary note.
7. **Gate** — Run `bash skills/runtime-routing/scripts/check.sh` (or the manual
   equivalent). Do not emit on a dirty gate.

## Adversarial self-test

- Inject a fabricated evidence id — does Guardian catch it?
- Inject a higher-permission runtime — is it rejected for a lower-permission one?
- Remove the fallback — is the report blocked?

## Output

Full `templates/output.md`: recommendation, complete capability matrix with
evidence ids, portability notes, fallback, gate result. Tag every claim.
