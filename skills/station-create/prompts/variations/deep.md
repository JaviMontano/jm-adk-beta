# Deep variation — station-create

Thorough path for ambiguous intent, contested type, or uncertain P06/P23/P24
mapping.

## Use when

- Type is unstated or arguable (universal vs dedicated both defensible).
- Sector binding is unclear or multiple sectors are implied.
- The required protocol structure cannot be traced to the ontology at a glance.
- A partial scaffold or possible collision is suspected.

## Expanded flow

1. **Discover deeply** — read the station registry, the parent `CLAUDE.md`, and
   any sibling stations to learn the local convention. Resolve name → slug.
2. **Type adjudication** — lay out the universal vs dedicated decision
   explicitly with the request's evidence. If unresolved → `{POR_CONFIRMAR}`,
   ask; never default. For dedicated, confirm the single owning sector.
3. **Structure tracing** — map type → P06/P23/P24 folders, each traced to the
   governing ontology. Any untraceable folder → `{POR_CONFIRMAR}`; do not invent.
4. **Collision analysis** — check slug AND path. On collision, surface the
   existing station and ask reuse vs rename. On partial scaffold, plan
   missing-only fill, listing present-and-untouched files.
5. **CLAUDE.md design** — draft, count lines; if >70, factor into linked files
   before writing (Rule-9).
6. **Scaffold, register, validate** — missing-only writes, idempotent registry
   upsert, full acceptance gate.

## Output

Full `templates/output.md` including the type rationale, the structure-trace
table, collision findings, and the gate results. One Alfa-core tag family. No
prices, single-brand (JM Labs), no client PII.
